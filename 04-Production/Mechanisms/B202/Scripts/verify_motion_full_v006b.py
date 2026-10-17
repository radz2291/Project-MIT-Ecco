"""Saved-consumer test10: motion replay, preservation, masks and channel isolation."""
import bpy,sys,json,math,hashlib
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
R=Path(__file__).resolve().parents[4];B=R/'04-Production/Mechanisms/B202';E=R/'04-Production/Records/Tasks/T-027/Evidence';sys.path.insert(0,str(B/'Scripts'))
from acquisition_core_v009 import read_json,reconstruct,mesh_from_grid,digest
M=read_json(E/'replay_manifest_v006b.json');old=read_json(E/'replay_manifest_v005b.json');C=read_json(B/'acquisition_config_v009.json');index=read_json(B/'Data/v009/index_v009.json');checks=[]
def check(label,ok):checks.append({'check':label,'pass':bool(ok)});assert ok,label
def snapshot():
    c=bpy.data.objects['B202_CONTROL'];s=bpy.context.scene;cam=s.camera;g=bpy.data.objects['T27_v005b_GAZE']
    return [c[k] for k in ('travel_m','rotation_rad','event_time_s','data_case','show_reconstruction','show_echo_strength','show_acquired_points','show_tool')]+list(cam.location)+list(g.location)+[cam.data.lens]
def ramp_values(name):return [(float(x.position),list(x.color)) for x in next(n for n in bpy.data.materials[name].node_tree.nodes if n.type=='VALTORGB').color_ramp.elements]
bpy.ops.wm.open_mainfile(filepath=str(R/M['source_scene']));s=bpy.context.scene;opening=[]
for f in range(1,337):s.frame_set(f);bpy.context.view_layer.update();opening.append(snapshot())
ramps={n:ramp_values(n) for n in ('B202_v009_delta_radius','B202_v009_received_echo_strength')}
bpy.ops.wm.open_mainfile(filepath=str(R/M['scene']));s=bpy.context.scene;c=bpy.data.objects['B202_CONTROL'];names=json.loads(c['v009_case_names'])
check('720frame/30second full mechanical candidate',s.frame_end==720 and s.render.fps==24)
for p,h in M['source_hashes'].items():check('source preserved '+p,hashlib.sha256((R/p).read_bytes()).hexdigest()==h)
for lib in bpy.data.libraries:check('relative library resolves '+lib.name,lib.filepath.startswith('//') and Path(bpy.path.abspath(lib.filepath)).exists())
for n,v in ramps.items():check('unchanged original fixed colormap '+n,ramp_values(n)==v)
data={}
for case in ('irregular_layers','spiral_layers','tight_layers','sparse_irregular','missed_nominal','weak_nominal','interpolation_fixture'):
    src='irregular_layers' if case=='interpolation_fixture' else case
    ev=read_json(B/'Data/v009'/index['cases'][src]['files']['events']);grid=read_json(B/'Data/v009'/('interpolation_fixture_grid_v009.json.gz' if case=='interpolation_fixture' else index['cases'][case]['files']['grid']));data[case]=(ev,grid)
    check(case+' indexed original event values',digest(ev)==index['cases'][src]['content_sha256']['events'])
    check(case+' three monostatic sensors',{x['sensor_id'] for x in ev}=={0,1,2} and all(x['sensor_id']==x['receiver_sensor_id'] for x in ev))
    vs,fs,ids=mesh_from_grid(grid,show_interpolated=True)
    for field in ('radius','echo_strength'):
        ob=bpy.data.objects['B202_v009_'+case+'_'+field];me=ob.data;cells=[grid['cells'][i] for i in ids]
        check(case+' '+field+' source positions',len(me.vertices)==len(vs) and all((v.co-Vector(p)).length<2e-6 for v,p in zip(me.vertices,vs)))
        expected=fs if field=='radius' else [f for f in fs if all(cells[j]['valid_amplitude'] for j in f)]
        check(case+' '+field+' no faces across absent/invalid samples',[tuple(p.vertices) for p in me.polygons]==expected)
        check(case+' '+field+' lineage cell IDs',[p.value for p in me.attributes['cell_index'].data]==ids)
        for name,vals in [('measured',[float(x['measured']) for x in cells]),('interpolated',[float(x['interpolated']) for x in cells]),('geometry_display',[(x['delta_radius_m']+.0012)/.0266 for x in cells]),('echo_strength_display',[(x['echo_strength'] or 0)/.4 for x in cells])]:
            check(case+' '+field+' fixed scalar/mask '+name,all(abs(p.value-v)<2e-6 for p,v in zip(me.attributes[name].data,vals)))
    ps=reconstruct(ev,C);cloud=bpy.data.objects['B202_v009_'+case+'_acquired_points'];check(case+' wall fixed inverse points',cloud.parent is None and all((v.co-Vector(p['position_m'])).length<2e-6 for v,p in zip(cloud.data.vertices,ps)))
ev,grid=data['irregular_layers'];previous=-1
for f in range(1,721):
    s.frame_set(f);bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get()
    if f<=336:
        check(str(f)+' accepted opening unchanged',all(abs(a-b)<2e-6 for a,b in zip(snapshot(),opening[f-1])))
        available={e['id'] for e in ev if e['timestamp_s']<=c['event_time_s']};expected={e['id'] for e in old['events'] if e['receipt_frame']<=f}
        check(str(f)+' exact original event receipt',available==expected and c['event_time_s']>=previous);previous=c['event_time_s']
        check(str(f)+' coverage contours after their source events',all(set(x['event_ids'])<=available for x in old['segments'] if not bpy.data.objects[x['object']].hide_render))
        case='irregular_layers'
    else:
        row=M['extension'][f-337];case=row['case'];check(str(f)+' completed dataset view and no tool/bit passage',names[int(c['data_case'])]==case and c['show_tool']==0 and c['show_acquired_points']==0 and c['event_time_s']==1000)
        check(str(f)+' independent quantity view',c['show_reconstruction']==row['show_reconstruction'] and c['show_echo_strength']==row['show_echo_strength'] and not(c['show_reconstruction'] and c['show_echo_strength']))
        for item in M['labels']:
            ob=bpy.data.objects[item['object']];want=item['frames'][0]<=f<=item['frames'][1];check(str(f)+' label schedule '+item['text'],ob.hide_render!=want)
            if want:
                coords=[world_to_camera_view(s,s.camera,ob.matrix_world@Vector(v)) for v in ob.bound_box]
                check(str(f)+' label inside frame '+item['text'],all(.01<x.x<.99 and .01<x.y<.99 for x in coords))
    check(str(f)+' interpolation remains off',c['show_interpolated']==0)
    for field in ('radius','echo_strength'):
        raw=bpy.data.objects['B202_v009_'+case+'_'+field]
        if raw.hide_render:continue # Suppressed objects may expose unevaluated raw mesh; no displayed data.
        ob=raw.evaluated_get(dg);me=ob.to_mesh();at=me.attributes.get('ready_timestamp_s');check(str(f)+' '+field+' no future averaged bins',not len(me.vertices) or at is not None and all(x.value<=c['event_time_s']+1e-5 for x in at.data));ob.to_mesh_clear()
for name in M['tight_objects']:
    ob=bpy.data.objects[name];cells=data['tight_layers'][1]['cells'][432:540]
    check(name+' true scale',all(abs(v-1)<1e-8 for v in ob.scale))
    check(name+' exact source/reference section',all(abs(p.co.x-x['x_m'])<2e-6 and abs(math.hypot(p.co.y,p.co.z)-(x['radius_m'] if name.endswith('MEASURED') else C['nominal_radius_m']))<2e-6 for p,x in zip(ob.data.splines[0].points,cells)))
for f in (337,384,432,553,624,720):
    s.frame_set(f);bpy.context.view_layer.update();case='spiral_layers' if f<=432 else 'irregular_layers';ob=bpy.data.objects['B202_v009_'+case+'_radius'];coords=[world_to_camera_view(s,s.camera,ob.matrix_world@v.co) for v in ob.data.vertices];check(str(f)+' full interval fits new wide view',all(.025<v.x<.975 and .025<v.y<.975 for v in coords))
result={'status':'PASS','check_count':len(checks),'checks':checks,'spec_test10':'Saved consumer replay verified across all720frames with original data, separate quantities, no future bins, masked fixtures and accepted opening preservation. Playable decode evidence is separate.','limitations':'Agent synthetic checks; no cold-viewer response, MIT calibration/certification or human full-motion acceptance implied.','scene_sha256':hashlib.sha256((R/M['scene']).read_bytes()).hexdigest()}
(E/'verification_motion-full_v006b.json').write_text(json.dumps(result,indent=2));print('T27_FULL_V006B_VERIFY_PASS',len(checks))
