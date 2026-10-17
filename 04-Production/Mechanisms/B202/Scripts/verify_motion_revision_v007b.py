"""Source, motion, staged comparison/inset and independent response verification."""
import bpy,sys,json,math,hashlib
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
R=Path(__file__).resolve().parents[4];B=R/'04-Production/Mechanisms/B202';E=R/'04-Production/Records/Tasks/T-027/Evidence';sys.path.insert(0,str(B/'Scripts'))
from acquisition_core_v009 import read_json,reconstruct,mesh_from_grid,digest
M=read_json(E/'replay_manifest_v007b.json');old=read_json(E/'replay_manifest_v005b.json');C=read_json(B/'acquisition_config_v009.json');index=read_json(B/'Data/v009/index_v009.json');checks=[]
def check(label,ok):checks.append({'check':label,'pass':bool(ok)});assert ok,label
def snapshot():
    c=bpy.data.objects['B202_CONTROL'];s=bpy.context.scene;g=bpy.data.objects['T27_v005b_GAZE'];cam=bpy.data.objects['T27 v005b camera']
    return [c[k] for k in ('travel_m','rotation_rad','event_time_s','data_case','show_reconstruction','show_echo_strength','show_acquired_points','show_tool','geometry_opacity')]+list(cam.location)+list(g.location)+[cam.data.lens]
bpy.ops.wm.open_mainfile(filepath=str(R/M['source_scene']));s=bpy.context.scene;opening=[]
for f in range(1,337):s.frame_set(f);bpy.context.view_layer.update();opening.append(snapshot())
bpy.ops.wm.open_mainfile(filepath=str(R/M['scene']));s=bpy.context.scene;c=bpy.data.objects['B202_CONTROL'];names=json.loads(c['v009_case_names']);check('720frame library, final S03 edit stays T15',s.frame_end==720 and s.render.fps==24)
for p,h in M['source_hashes'].items():check('preserved '+p,hashlib.sha256((R/p).read_bytes()).hexdigest()==h)
for lib in bpy.data.libraries:check('relative library resolves '+lib.name,lib.filepath.startswith('//') and Path(bpy.path.abspath(lib.filepath)).exists())
for image in bpy.data.images:
    if image.source=='FILE' and image.filepath:check('image resolves '+image.name,Path(bpy.path.abspath(image.filepath)).exists())
data={}
for case in ('irregular_layers','tight_layers','spiral_layers','sparse_irregular','missed_nominal','weak_nominal','interpolation_fixture'):
    src='irregular_layers' if case=='interpolation_fixture' else case;ev=read_json(B/'Data/v009'/index['cases'][src]['files']['events']);g=read_json(B/'Data/v009'/('interpolation_fixture_grid_v009.json.gz' if case=='interpolation_fixture' else index['cases'][case]['files']['grid']));data[case]=(ev,g)
    check(case+' event content unchanged',digest(ev)==index['cases'][src]['content_sha256']['events']);check(case+' monostatic3sensors',{e['sensor_id'] for e in ev}=={0,1,2} and all(e['sensor_id']==e['receiver_sensor_id'] for e in ev));vs,fs,ids=mesh_from_grid(g,show_interpolated=True);cells=[g['cells'][i] for i in ids]
    for field in ('radius','echo_strength'):
        o=bpy.data.objects['B202_v009_'+case+'_'+field];me=o.data;check(case+' '+field+' original positions',len(me.vertices)==len(vs) and all((v.co-Vector(p)).length<2e-6 for v,p in zip(me.vertices,vs)));expected=fs if field=='radius' else [f for f in fs if all(cells[j]['valid_amplitude'] for j in f)];check(case+' '+field+' masked faces',[tuple(p.vertices) for p in me.polygons]==expected)
        for attr,vals in [('cell_index',ids),('measured',[int(x['measured']) for x in cells]),('interpolated',[int(x['interpolated']) for x in cells]),('geometry_display',[(x['delta_radius_m']+.0012)/.0266 for x in cells]),('echo_strength_display',[(x['echo_strength'] or 0)/.4 for x in cells])]:check(case+' '+field+' fixed original '+attr,all(abs(p.value-v)<2e-6 for p,v in zip(me.attributes[attr].data,vals)))
    ps=reconstruct(ev,C);cloud=bpy.data.objects['B202_v009_'+case+'_acquired_points'];check(case+' inverse points fixed',cloud.parent is None and all((v.co-Vector(p['position_m'])).length<2e-6 for v,p in zip(cloud.data.vertices,ps)))
for name in M['comparison_objects']:
    o=bpy.data.objects[name];case=o['source_case'];cells=data[case][1]['cells'][432:540];nominal=name.endswith('nominal');check(name+' translation-only case staging',all(abs(v-1)<1e-8 for v in o.scale) and all(abs(v-1)<1e-8 for v in o.parent.scale));check(name+' exact source/reference coordinates',all((p.co.xyz-Vector((x['x_m'],(C['nominal_radius_m'] if nominal else x['radius_m'])*math.cos(x['azimuth_rad']),(C['nominal_radius_m'] if nominal else x['radius_m'])*math.sin(x['azimuth_rad'])))).length<2e-6 for p,x in zip(o.data.splines[0].points,cells)))
for name in M['spiral_objects']:
    o=bpy.data.objects[name];ids=json.loads(o['grid_cells']);cells=[data['spiral_layers'][1]['cells'][i] for i in ids];check(name+' exact measured sections',all((p.co.xyz-Vector((x['x_m'],x['radius_m']*math.cos(x['azimuth_rad']),x['radius_m']*math.sin(x['azimuth_rad'])))).length<2e-6 for p,x in zip(o.data.splines[0].points,cells)))
crest=bpy.data.objects['T27_v007b_SAMPLED_ENLARGEMENT_CREST'];check('crest13adjacent measured station maxima',M['crest_cells']==[max(data['spiral_layers'][1]['cells'][i*108:(i+1)*108],key=lambda x:x['radius_m'])['index'] for i in range(13)])
for p,i in zip(crest.data.splines[0].points,M['crest_cells']):
    x=data['spiral_layers'][1]['cells'][i];check('crest point '+str(i),(p.co.xyz-Vector((x['x_m'],x['radius_m']*math.cos(x['azimuth_rad']),x['radius_m']*math.sin(x['azimuth_rad'])))).length<2e-6)
inset=M['inset'];check('5x view from source camera, no data scaling',abs(inset['display_plane_width_m']/inset['ortho_window_m']*inset['comparison_ortho_width_m']-5)<1e-8)
for kind in ('nominal','measured'):
    o=bpy.data.objects['T27_v007b_INSET_'+kind];cells=data['tight_layers'][1]['cells'][432:540];check('inset '+kind+' exact source radii',all(abs(math.hypot(p.co.y,p.co.z)-(C['nominal_radius_m'] if kind=='nominal' else x['radius_m']))<2e-6 for p,x in zip(o.data.splines[0].points,cells)))
ramp=next(n for n in bpy.data.materials['B202_v009_received_echo_strength'].node_tree.nodes if n.type=='VALTORGB');check('declared fixed transfer, no frame auto-normalization',all(abs(e.position-p)<2e-6 and all(abs(a-b)<2e-6 for a,b in zip(e.color[:3],color)) for e,(p,color) in zip(ramp.color_ramp.elements,M['echo_palette'])) and M['fixed_echo_range']==[0.,.4]);check('no new source data generated',M['new_data_generated'] is False)
ev=data['irregular_layers'][0];previous=-1
for f in range(1,721):
    s.frame_set(f);bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get()
    if f<=336:
        check(str(f)+' accepted opening state identical',all(abs(a-b)<2e-6 for a,b in zip(snapshot(),opening[f-1])));available={e['id'] for e in ev if e['timestamp_s']<=c['event_time_s']};expected={e['id'] for e in old['events'] if e['receipt_frame']<=f};check(str(f)+' original event receipt',available==expected and c['event_time_s']>=previous);previous=c['event_time_s'];case='irregular_layers'
    else:
        row=M['extension'][f-337];case=row['case'];check(str(f)+' exact independent display state',names[int(c['data_case'])]==case and c['show_reconstruction']==row['show_reconstruction'] and c['show_echo_strength']==row['show_echo_strength']);check(str(f)+' completed cases, no bit/tool passage',c['show_tool']==0 and c['show_acquired_points']==0 and c['event_time_s']==1000)
        for item in M['labels']:
            o=bpy.data.objects[item['object']];want=item['frames'][0]<=f<=item['frames'][1];check(str(f)+' label schedule '+o.name,o.hide_render!=want)
            if want:
                coords=[world_to_camera_view(s,s.camera,o.matrix_world@Vector(v)) for v in o.bound_box];check(str(f)+' label margins '+o.name,all(.01<v.x<.99 and .01<v.y<.99 for v in coords))
        if f<=432:
            for name in M['comparison_objects']:
                o=bpy.data.objects[name];coords=[world_to_camera_view(s,s.camera,o.matrix_world@p.co.xyz) for p in o.data.splines[0].points];check(str(f)+' complete comparison circumference '+name,all(.01<v.x<.99 and .01<v.y<.99 for v in coords))
        if f>=601:
            cam=s.camera;check(str(f)+' acoustic camera circles stationary data',cam.name=='T27_v007b_AMPLITUDE_CAMERA' and abs(cam.location.x-3.25)<2e-6 and abs(math.hypot(cam.location.y,cam.location.z)-4.1)<2e-6)
    check(str(f)+' no interpolation',c['show_interpolated']==0)
    for field in ('radius','echo_strength'):
        raw=bpy.data.objects['B202_v009_'+case+'_'+field]
        if raw.hide_render:continue
        ob=raw.evaluated_get(dg);me=ob.to_mesh();at=me.attributes.get('ready_timestamp_s');check(str(f)+' no future '+field,not len(me.vertices) or at is not None and all(x.value<=c['event_time_s']+1e-5 for x in at.data));ob.to_mesh_clear()
result={'status':'PASS','check_count':len(checks),'checks':checks,'scene_sha256':hashlib.sha256((R/M['scene']).read_bytes()).hexdigest(),'scope':'All-frame synthetic integrity, same opening, fixed ranges, true-source translated comparison/5x view/crest, separate response. Actual human comprehension and MIT calibration remain pending.'};(E/'verification_motion-revision_v007b.json').write_text(json.dumps(result,indent=2));print('VERIFY_V007B_PASS',len(checks))
