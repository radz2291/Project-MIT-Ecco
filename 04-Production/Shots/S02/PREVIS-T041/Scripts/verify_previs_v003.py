"""Saved-scene executor checks; not an independent engineering review."""
import bpy,json,hashlib,math
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
BASE=Path(__file__).resolve().parents[1];P=BASE.parents[2];E=P/'Records/Tasks/T-041/Evidence'
record=json.loads((E/'build_v003.json').read_text())
path=BASE/'Scenes/S02_previs_T041_v003.blend';bpy.ops.wm.open_mainfile(filepath=str(path));s=bpy.context.scene
checks={};checks['range_fps_aspect']=(s.frame_start,s.frame_end,s.render.fps,s.render.resolution_x,s.render.resolution_y)==(1,288,24,640,360)
checks['relative_libraries_resolve']=all(l.filepath.startswith('//') and Path(bpy.path.abspath(l.filepath)).is_file() for l in bpy.data.libraries)
checks['source_hashes_unchanged']=all(hashlib.sha256((P/k).read_bytes()).hexdigest()==v for k,v in record['sources'].items())
refs=record['refs'];checks['one_sensor_plane']=max(r['source_xyz'][0] for r in refs)-min(r['source_xyz'][0] for r in refs)<1e-6
angles=sorted(r['source_angle']%(2*math.pi) for r in refs)
checks['sensor_spacing_120deg']=all(abs(((angles[(i+1)%3]-angles[i])%(2*math.pi))-2*math.pi/3)<1e-5 for i in range(3))
checks['all_round_trips_ordered']=all(e['emit']<e['contact']<e['receive'] for e in record['events'])
errors=[];visibility=[];positions=[];camera=[];reading_visibility=[]
for e in record['events']:
    tx=bpy.data.objects[e['id']+'_TX'];rx=bpy.data.objects[e['id']+'_ECHO'];dot=bpy.data.objects[e['id']+'_WALL_RECORD']
    for f,ob,expected in [(e['emit'],tx,e['origin']),(e['contact'],tx,e['wall']),(e['contact'],rx,e['wall']),(e['receive'],rx,e['receiver'])]:
        s.frame_set(f);bpy.context.view_layer.update();errors.append((ob.matrix_world.translation-Vector(expected)).length)
    s.frame_set(e['receive']-1);visibility.append(dot.hide_render)
    s.frame_set(e['receive']);visibility.append(not dot.hide_render)
    p=dot.matrix_world.translation.copy();s.frame_set(288);errors.append((dot.matrix_world.translation-p).length)
    positions.append((dot.name,dot.parent is None,list(p)))
checks['pulse_contact_same_sensor_endpoints']=max(errors)<1e-5
checks['records_only_after_reception']=all(visibility)
checks['wall_records_world_fixed']=all(p[1] for p in positions)
checks['three_sector_120degree_scan']=abs(record['rotation_radians'][1]-record['rotation_radians'][2]-2*math.pi/3)<1e-5
for f in range(1,289):
    s.frame_set(f);bpy.context.view_layer.update();camera.append(s.camera.matrix_world.translation.copy())
steps=[(b-a).length for a,b in zip(camera,camera[1:])]
checks['continuous_camera_no_position_jumps']=max(steps)<.04
checks['static_final_recognition_hold']=max((p-camera[-1]).length for p in camera[265:])<1e-5
s.frame_set(288);bpy.context.view_layer.update()
for e in record['events']:
    if e['kind']!='sparse_illustrative_scan':continue
    ndc=world_to_camera_view(s,s.camera,Vector(e['wall']));reading_visibility.append(dict(id=e['id'],xy=list(ndc)[:2],inside=0<ndc.x<1 and 0<ndc.y<1 and ndc.z>0))
checks['complete_ring_inside_frame']=all(v['inside'] for v in reading_visibility)
checks['native_camera_gaze_editable']=len(s.camera.animation_data.action.layers)>0 and bpy.data.objects.get('T41_GAZE_TARGET') is not None
checks['no_external_python_handlers']=not bpy.app.handlers.frame_change_pre and not bpy.app.handlers.frame_change_post
out=dict(checks=checks,passed=all(checks.values()),max_endpoint_or_static_error_m=max(errors),max_camera_step_m=max(steps),ring_projection=reading_visibility,source_hashes=record['sources'],scene_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),self_checks_only=True,human_comprehension='pending',MIT_engineering_review='pending')
(E/'verification_v003.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:v for k,v in out.items() if k!='ring_projection'}))
assert out['passed'],checks
