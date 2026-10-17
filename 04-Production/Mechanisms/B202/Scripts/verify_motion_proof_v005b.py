import bpy,sys,json,hashlib,math,bmesh
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
R=Path(__file__).resolve().parents[4];B=R/'04-Production/Mechanisms/B202';E=R/'04-Production/Records/Tasks/T-027/Evidence';sys.path.insert(0,str(B/'Scripts'))
from acquisition_core_v009 import read_json,reconstruct,digest
M=read_json(E/'replay_manifest_v005b.json');events=read_json(B/'Data/v009/irregular_layers_events_v009.json.gz');C=read_json(B/'acquisition_config_v009.json');points=reconstruct(events,C)
bpy.ops.wm.open_mainfile(filepath=str(R/M['scene']));s=bpy.context.scene;c=bpy.data.objects['B202_CONTROL'];checks=[]
def check(label,ok):checks.append({'check':label,'pass':bool(ok)});assert ok,label
check('14s bounded proof',s.frame_end==336 and s.render.fps==24)
check('all4212 source events retained',len(M['events'])==4212 and [x['id'] for x in M['events']]==[e['id'] for e in events])
index=read_json(B/'Data/v009/index_v009.json')
check('raw event values match original v009 indexed content hash',digest(events)==index['cases']['irregular_layers']['content_sha256']['events'])
check('three sensors with own receiver',{e['sensor_id'] for e in events}=={0,1,2} and all(e['sensor_id']==e['receiver_sensor_id'] for e in events))
for path,digest in M['source_hashes'].items():check('preserved '+path,hashlib.sha256((R/path).read_bytes()).hexdigest()==digest)
for lib in bpy.data.libraries:check('relative library resolves '+lib.name,lib.filepath.startswith('//') and Path(bpy.path.abspath(lib.filepath)).exists())
rock=bpy.data.objects['T27_CONTINUOUS_ENCLOSING_ROCK_CUTAWAY'];full=bpy.data.objects['B202_GEOMETRY_irregular'];nv=M['rock_inner_source_vertices']
check('inner wall unchanged source T6 vertices',nv==len(full.data.vertices) and all((rock.data.vertices[i].co-full.data.vertices[i].co).length<1e-8 for i in range(nv)))
bm=bmesh.new();bm.from_mesh(rock.data);check('solid rock cutaway has closed boundary surfaces',all(e.is_manifold for e in bm.edges));bm.free()
cloud=bpy.data.objects['B202_v009_irregular_layers_acquired_points'];check('registered inverse point cloud remains world fixed',cloud.parent is None and cloud.matrix_world.translation.length<1e-8 and all((v.co-Vector(p['position_m'])).length<2e-6 for v,p in zip(cloud.data.vertices,points)))
previous=-1.;samples=[]
for row in M['timeline']:
    f=row['frame'];s.frame_set(f);bpy.context.view_layer.update();cutoff=c['event_time_s'];available={e['id'] for e in events if e['timestamp_s']<=cutoff};expected={e['id'] for e in M['events'] if e['receipt_frame']<=f}
    check(f'{f} exact evidence cutoff',available==expected and cutoff>=previous);previous=cutoff
    check(f'{f} point registration',cloud.parent is None and all((v.co-Vector(p['position_m'])).length<2e-6 for v,p in zip(cloud.data.vertices,points)))
    visible=[x for x in M['segments'] if not bpy.data.objects[x['object']].hide_render]
    check(f'{f} contour causality',all(set(x['event_ids'])<=available for x in visible))
    radius=bpy.data.objects['B202_v009_irregular_layers_radius'].evaluated_get(bpy.context.evaluated_depsgraph_get());me=radius.to_mesh();at=me.attributes.get('ready_timestamp_s')
    check(f'{f} no future averages',not len(me.vertices) or (at is not None and all(p.value<=cutoff+1e-5 for p in at.data)));radius.to_mesh_clear()
    check(f'{f} distinct quantity controls / explicit comparison view',c['show_reconstruction']==(0 if 105<=f<=204 else 1) and c['show_echo_strength']==0 and c['show_interpolated']==0)
    if row['phase']=='transfer' and f>1:check(f'{f} no invented transfer events',row['event_count']==M['timeline'][f-2]['event_count'])
    if f in (1,7,18,60,105,132,168,204,240,336):samples.append({'frame':f,'events':len(available),'contour_edges':len(visible),'travel_m':c['travel_m']})
s.frame_set(7);cue=bpy.data.objects['T27_v005b_first_same_sensor_return'];check('first recorded wall contact',(cue.location-Vector(points[0]['position_m'])).length<2e-6)
s.frame_set(17);check('first same-sensor return',(cue.location-Vector(events[0]['sensor_origin_m'])).length<2e-6)
s.frame_set(336);obj=bpy.data.objects['B202_v009_irregular_layers_radius'].evaluated_get(bpy.context.evaluated_depsgraph_get());me=obj.to_mesh();check('full acquired 3m depth span',abs(max(v.co.x for v in me.vertices)-min(v.co.x for v in me.vertices)-3)<1e-5);obj.to_mesh_clear()
check('camera no longer tracks tool',abs(bpy.data.objects['T27_v005b_GAZE'].location.x-(c['travel_m']+.73))>2)
grid=read_json(B/'Data/v009/irregular_layers_grid_v009.json.gz');cells=[grid['cells'][i] for i in M['focus']['grid_cell_indices']]
actual=bpy.data.objects['T27_v005b_MEASURED_FOCUS_CONTOUR'];nominal=bpy.data.objects['T27_v005b_EXPECTED_NOMINAL_FOCUS'];band=bpy.data.objects['T27_v005b_ACTUAL_MINUS_EXPECTED']
check('108 valid measured comparison cells',len(cells)==108 and all(x['measured'] and not x['interpolated'] for x in cells))
for i,x in enumerate(cells):
    a=actual.data.splines[0].points[i].co.xyz;n=nominal.data.splines[0].points[i].co.xyz
    expected=Vector((x['x_m'],x['radius_m']*math.cos(x['azimuth_rad']),x['radius_m']*math.sin(x['azimuth_rad'])))
    check(f'comparison cell {i} exact measured position / no magnified geometry',(a-expected).length<2e-6)
    check(f'comparison cell {i} exact nominal baseline',abs(math.hypot(n.y,n.z)-C['nominal_radius_m'])<2e-6 and abs(n.x-x['x_m'])<2e-6)
    check(f'comparison band {i} merely joins actual to expected',(band.data.vertices[i].co-a).length<2e-6 and (band.data.vertices[i+108].co-n).length<2e-6)
s.frame_set(104);check('comparison waits for its scheduled view',actual.hide_render)
s.frame_set(105);check('comparison has all source contributors',not actual.hide_render and c['event_time_s']>=M['focus']['source_ready_timestamp_s'])
for f in (132,168,204):
    s.frame_set(f);bpy.context.view_layer.update()
    screen=[world_to_camera_view(s,s.camera,Vector(p)) for p in M['focus']['actual_positions']]
    check(f'comparison {f} entire outline inside frame',all(.025<v.x<.975 and .025<v.y<.975 for v in screen))
    check(f'comparison {f} meaningful 1:1 held frame',all(abs(v-1)<1e-8 for v in actual.scale) and all(abs(v-1)<1e-8 for v in nominal.scale))
for font in bpy.data.fonts:
    if font.filepath and font.filepath!='<builtin>':check('font dependency resolves '+font.name,Path(bpy.path.abspath(font.filepath)).is_file())
check('focus is strongest existing section, not altered wall',M['focus']['depth_m']==2.75 and max(x['delta_radius_m'] for x in cells)<.0254)
result={'status':'PASS','check_count':len(checks),'checks':checks,'sample_frames':samples,'scope':'Agent synthetic scene/data checks only. Real-time visual comprehension, actual acoustic face/cadence and Radzi D2/D3 approval remain pending.','scene_sha256':hashlib.sha256((R/M['scene']).read_bytes()).hexdigest()}
(E/'verification_motion-proof_v005b.json').write_text(json.dumps(result,indent=2));print('T27_V004C_VERIFY_PASS',len(checks))
