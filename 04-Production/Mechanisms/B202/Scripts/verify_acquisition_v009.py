"""Acceptance tests 1–9. Test10 is explicitly deferred to T27 by owner.
All tests are implementation self-checks, not calibrated sonic validation.
"""
import bpy,math,sys,json,hashlib,statistics
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[4];BASE=ROOT/'04-Production/Mechanisms/B202';DATA=BASE/'Data/v009';E=ROOT/'04-Production/Records/Tasks/T-008/Evidence/v009';sys.path.insert(0,str(BASE/'Scripts'))
from acquisition_core_v009 import *
from build_acquisition_v009 import load_sources,bvh_wall,acquire,changed_wall,tight_wall
C=read_json(BASE/'acquisition_config_v009.json');INDEX=read_json(DATA/'index_v009.json');checks=[];metrics={}
def check(test,name,passed,detail=None):
    c={'spec_test':test,'check':name,'pass':bool(passed)}
    if detail is not None:c['detail']=detail
    checks.append(c)
def data(case,kind):return read_json(DATA/INDEX['cases'][case]['files'][kind])
events={case:data(case,'events') for case in INDEX['cases']};grids={case:data(case,'grid') for case in INDEX['cases']}
check(8,'effective case parameters match event counts and known poses',all(len(events[name])==len(C['depths_m'])*meta['case_parameters']['orientations_per_depth']*3 and all(abs(e['tool_pose']['translation_m'][j+1]-v)<1e-9 for e in events[name] for j,v in enumerate(meta['case_parameters']['known_eccentric_yz_m'])) for name,meta in INDEX['cases'].items()))
processed={case:reconstruct(es,C) for case,es in events.items()}
walls,sensors=load_sources();walls['irregular_changed']=(changed_wall(walls['irregular'][0]),walls['irregular'][1]);walls['tight']=(tight_wall(walls['irregular'][0]),walls['irregular'][1])
for case in INDEX['cases']:
    truth=data(case,'truth');errs=[]
    for p in processed[case]:errs.append((Vector(p['position_m'])-Vector(truth[p['sample_id']]['hit_position_m'])).length)
    metrics[case]={'events':len(events[case]),'valid_events':len(processed[case]),'measured_bins':sum(p['measured'] for p in grids[case]['cells']),'maximum_inverse_hit_error_m':max(errs,default=0.)}
    check(1,'inverse point consistency '+case,max(errs,default=0.)<=C['tolerances']['inverse_point_error_m'])
    check(8,'stored grid reproducible from measurement records '+case,digest(grid_samples(processed[case],C,case))==digest(grids[case]))
    evlookup={e['id']:e for e in events[case]};plookup={p['sample_id']:p for p in processed[case]};ok=True
    for cell in grids[case]['cells']:
        if cell['measured']:
            ps=[plookup[i] for i in cell['event_ids']];r=sum(p['radius_m']*w for p,w in zip(ps,cell['weights']))
            ok &= abs(r-cell['radius_m'])<1e-12 and abs(sum(cell['weights'])-1)<1e-12 and all(evlookup[i]['valid_tof'] for i in cell['event_ids'])
            if cell['valid_amplitude']:
                val=sum(evlookup[i]['echo_strength']*w for i,w in zip(cell['amplitude_event_ids'],cell['amplitude_weights']));ok &= abs(val-cell['echo_strength'])<1e-12
        else:ok &= not cell['valid_geometry'] and cell['radius_m'] is None and cell['echo_strength'] is None
    check(8,'every displayed field traces to source events '+case,ok)
    vs,fs,ids=mesh_from_grid(grids[case]);check(8,'mesh coordinates are reconstructed radius field '+case,all(abs(math.hypot(v[1],v[2])-grids[case]['cells'][i]['radius_m'])<1e-12 for v,i in zip(vs,ids)))
    check(9,'synthetic origin and same-emitter receiver '+case,all(e['source_kind']=='synthetic_illustrative' and e['sensor_id']==e['receiver_sensor_id'] for e in events[case]))
    if processed[case]:
        wallname=INDEX['cases'][case]['wall'];bvh=bvh_wall(*walls[wallname]);errors=[]
        for p in grids[case]['cells']:
            if not p['measured']:continue
            theta=p['azimuth_rad'];hit,*_=bvh.ray_cast(Vector((p['x_m'],0,0)),Vector((0,math.cos(theta),math.sin(theta))),.5)
            if hit is None:errors.append(float('inf'))
            else:errors.append(abs(math.hypot(hit.y,hit.z)-p['radius_m']))
        maximum=max(errors);metrics[case]['maximum_grid_vs_triangle_ground_truth_error_m']=maximum
        check(1,'grid versus independent axis ray triangle truth '+case,maximum<=C['tolerances']['grid_triangle_reference_error_m'],maximum)
# 1. Polygon cylinder is compared to both exact triangles and analytic circle.
nom=grids['nominal_constant'];rs=[p['radius_m'] for p in nom['cells'] if p['measured']];error=max(abs(r-C['nominal_radius_m']) for r in rs);times=[e['tof_2way_s'] for e in events['nominal_constant'] if e['valid_tof']];amps=[e['echo_strength'] for e in events['nominal_constant'] if e['valid_amplitude']]
check(1,'analytic cylinder error bounded by 96-sector mesh tessellation',error<=C['tolerances']['cylinder_analytic_radius_error_m'],error)
check(1,'stable centered cylinder TOF within tessellation bound',max(times)-min(times)<=2*C['tolerances']['cylinder_analytic_radius_error_m']/C['mud_sound_speed_m_s'])
check(1,'constant material echo stable apart from polygon incidence/path',max(amps)-min(amps)<.02*statistics.mean(amps))
# 2. Change actual T6-derived wall triangles, keep material model fixed.
a=events['irregular_constant'];b=events['irregular_changed_constant'];check(2,'physical wall fingerprint changes',INDEX['cases']['irregular_constant']['wall_sha256']!=INDEX['cases']['irregular_changed_constant']['wall_sha256'])
tofchange=max(abs(p['tof_2way_s']-q['tof_2way_s']) for p,q in zip(a,b) if p['valid_tof'] and q['valid_tof']);radiuschange=max(abs(p['radius_m']-q['radius_m']) for p,q in zip(grids['irregular_constant']['cells'],grids['irregular_changed_constant']['cells']) if p['measured'] and q['measured'])
check(2,'geometry change changes simulated echo time',tofchange>1e-6,tofchange);check(2,'geometry change changes reconstruction and silhouette',radiuschange>.003,radiuschange)
check(2,'geometry change does not replace constant reflectivity',all(abs(p['response_factors']['reflectivity']-q['response_factors']['reflectivity'])<1e-12 for p,q in zip(a,b) if p['valid_tof'] and q['valid_tof']))
check(2,'outward change yields no significant shorter stand-off',all(q['tof_2way_s']>=p['tof_2way_s']-1e-9 for p,q in zip(a,b) if p['valid_tof'] and q['valid_tof']))
# 3. Change only material impedance in a defined layer.
b=events['irregular_material_changed'];check(3,'material change keeps triangle geometry identical',INDEX['cases']['irregular_constant']['wall_sha256']==INDEX['cases']['irregular_material_changed']['wall_sha256'])
check(3,'material change keeps TOF identical',all(p['tof_2way_s']==q['tof_2way_s'] for p,q in zip(a,b)))
keys=('x_m','azimuth_rad','radius_m','delta_radius_m','valid_geometry','event_ids')
check(3,'material change keeps reconstructed geometry numerically identical',all(all(p[k]==q[k] for k in keys if k!='event_ids') for p,q in zip(grids['irregular_constant']['cells'],grids['irregular_material_changed']['cells'])))
diff=[abs(p['echo_strength']-q['echo_strength']) for p,q in zip(a,b) if p['valid_amplitude'] and q['valid_amplitude']];check(3,'material change changes echo strength',max(diff)>.01,max(diff))
check(3,'outside changed material interval amplitude stays identical',all(p['echo_strength']==q['echo_strength'] for p,q in zip(a,b) if p['valid_amplitude'] and q['response_factors']['material_zone']=='constant'))
legacy=lambda x,t:.5+.28*math.sin(5*t+9*x)+.16*math.sin(14*x-2*math.cos(t))
legacy_diff=max(abs(legacy(p['x_m'],p['azimuth_rad'])-legacy(q['x_m'],q['azimuth_rad'])) for p,q in zip(processed['irregular_constant'],processed['irregular_material_changed']))
check(3,'legacy sine pipeline fails material-response negative control as expected',legacy_diff==0 and max(diff)>.01,{'legacy_maximum_material_response':legacy_diff,'new_maximum_material_response':max(diff)})
metrics['comparison']={'maximum_geometry_only_tof_change_s':tofchange,'maximum_geometry_only_radius_change_m':radiuschange,'maximum_material_only_echo_change':max(diff),'material_only_geometry_change_m':0.}
# 4. Supplied eccentric pose and fixed known axis, not proprietary estimation.
ecc=events['eccentric_nominal'];check(4,'eccentric pose changes individual travel times',max(abs(p['tof_2way_s']-q['tof_2way_s']) for p,q in zip(events['nominal_constant'],ecc) if p['valid_tof'] and q['valid_tof'])>1e-7)
check(4,'eccentric points remain on fixed cylinder',max(abs(p['radius_m']-C['nominal_radius_m']) for p in processed['eccentric_nominal'])<C['tolerances']['cylinder_analytic_radius_error_m'])
check(4,'eccentric pose and reference axis are explicit inputs',C['axis_yz_m']==[0.,0.] and all(abs(e['tool_pose']['translation_m'][1]-.0007)<1e-9 and abs(e['tool_pose']['translation_m'][2]+.0006)<1e-9 for e in ecc))
# 5. Missing and sparse evidence cannot form a full cylinder.
sparse=grids['sparse_irregular'];coverage=sum(p['measured'] for p in sparse['cells'])/len(sparse['cells']);check(5,'partial angular acquisition remains sparse',0<coverage<.4,coverage)
vs,faces,ids=mesh_from_grid(sparse);check(5,'no mesh vertex in unmeasured bin',all(sparse['cells'][i]['measured'] for i in ids));check(5,'no face bridges an unmeasured cell',all(all(sparse['cells'][ids[v]]['measured'] for v in f) for f in faces))
for case in ['missed_nominal','weak_nominal']:check(5,case+' gives no fabricated wall',not processed[case] and mesh_from_grid(grids[case])==([],[],[]))
cut=.5;partial=grid_samples(processed['irregular_layers'],C,'irregular_layers',cutoff=cut);check(5,'event-time replay excludes all future records',all(p['ready_timestamp_s']<=cut for p in partial['cells'] if p['measured']))
# Explicitly masked one-bin interpolation fixture.
drop=5*C['azimuth_bins']+10;removed=set(grids['irregular_layers']['cells'][drop]['event_ids']);ps=[p for p in processed['irregular_layers'] if p['sample_id'] not in removed];filled=grid_samples(ps,C,'interpolation_fixture',interpolate=True);cell=filled['cells'][drop]
check(5,'interpolation is distinct from measured evidence',cell['interpolated'] and not cell['measured'] and cell['valid_geometry']);check(8,'interpolation retains neighbor lineage and weights',len(cell['interpolation_sources'])==2 and abs(sum(cell['weights'])-1)<1e-12)
check(5,'interpolation hidden by default',drop not in mesh_from_grid(filled)[2] and drop in mesh_from_grid(filled,show_interpolated=True)[2]);write_json(DATA/'interpolation_fixture_grid_v009.json.gz',filled)
# 6. Real inherited sensor phase and plane, transformed whole-tool pose.
angles=sorted(math.atan2(s['local_origin_m'][2],s['local_origin_m'][1]) for s in sensors);check(6,'three references 120deg apart',all(abs((angles[(i+1)%3]-angles[i])%math.tau-math.tau/3)<1e-5 for i in range(3)))
check(6,'one shared sensor plane',max(s['local_origin_m'][0] for s in sensors)-min(s['local_origin_m'][0] for s in sensors)<1e-6)
check(6,'same three sensors repeated over whole-tool poses',{e['sensor_id'] for e in a}=={0,1,2} and len({e['tool_pose']['rotation_xyz_rad'][0] for e in a})==108)
# 7. Triangle faceting makes the new bound slightly more conservative than the
# continuous analytic v008 radius. No bit or operational passage assertion.
v8=read_json(BASE/'config_v008.json');bound=(C['nominal_radius_m']-.0012)*math.cos(math.pi/96)-v8['source_maximum_radial_envelope_m'];minimum=min(p['radius_m'] for p in processed['tight_layers']);check(7,'full-tool centered clearance including triangle faceting',bound>.0015,bound);check(7,'sampled restriction remains below nominal but above conservative tool envelope',minimum<C['nominal_radius_m'] and minimum-v8['source_maximum_radial_envelope_m']>=bound-2e-6)
metrics['clearance']={'analytic_triangle_envelope_radial_clearance_m':bound,'minimum_acquired_tight_radius_m':minimum,'minimum_acquired_radial_clearance_m':minimum-v8['source_maximum_radial_envelope_m'],'nominal_bit_passage':False,'operational_safety_claim':False}
# Deterministic repeat from source BVH, not just reading the same output twice.
repeat,_=acquire('nominal_constant',bvh_wall(*walls['nominal']),sensors,C);check(8,'deterministic fresh forward acquisition',digest(repeat)==digest(events['nominal_constant']))
check(8,'reconstruction has no truth or mesh input',reconstruct([],C)==[] and 'hit_position_m' not in str(events['nominal_constant'][0]))
before=read_json(E/'preservation_before_v009.json');changed=[p for p,h in before.items() if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h];check(9,'all v008/T5/T6/T7 source hashes preserved',not changed,changed)
for path,h in v8['source_hashes'].items():check(9,'source matches accepted v008 baseline '+path,hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==h)
out={'passed':sum(c['pass'] for c in checks),'total':len(checks),'checks':checks,'metrics':metrics,'spec_test_10':{'status':'deferred_to_T27_by_owner','not_passed':True,'reason':'Cinematic animation and playable proof explicitly excluded from T8 v009 scope.'},'limits':'Forward/inverse consistency and synthetic controlled-case tests only. Not independent acoustic accuracy, calibrated field data or proprietary ENP3 processing.'}
write_json(E/'verification_acquisition_v009.json',out);print(json.dumps({'passed':out['passed'],'total':out['total'],'failures':[c for c in checks if not c['pass']],'comparisons':metrics['comparison'],'clearance':metrics['clearance']}));assert all(c['pass'] for c in checks)
