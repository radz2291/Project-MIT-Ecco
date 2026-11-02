"""Check unchanged signals and wall targets during the restored camera pullback."""
import bpy,json,sys,math
from pathlib import Path
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');Q=R/'04-Production/Shots/S01-S02'
sys.path.insert(0,str(R/'04-Production/Shared/Assets/Effects/Waveform/Scripts'))
from pulse_asset_api import arrival_readouts
bpy.ops.wm.open_mainfile(filepath=str(Q/'Scenes/S01-S02_production_v017.blend'),use_scripts=False)
s=bpy.context.scene;wall=bpy.data.objects['ONE WALL - old history and current cells share topology'];data=json.loads((Q/'Notes/approved_v016_integration.json').read_text());rows=[]
for e in data['events']:
 s.frame_set(e['start']+41);o=bpy.data.objects[f"WF sequence event {e['event']}"];times=arrival_readouts(o)
 assert abs(times['Return tail arrival']-e['landmarks']['feedback_complete'])<.001
 materials={wall.data.polygons[i].material_index for i in e['faces']}
 ev=wall.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();count=sum(p.material_index in materials for p in me.polygons);ev.to_mesh_clear()
 assert count==16,('camera viewing wedge removes scan target',e['event'],count)
 rows.append({'event':e['event'],'return_timing_unchanged':True,'target_faces_retained_during_feedback':count})
speeds=[];angles=[];prev=None
for f in range(474,757):
 s.frame_set(f);m=s.camera.matrix_world.copy()
 if prev:
  speeds.append((m.translation-prev.translation).length);angles.append(math.degrees(m.to_quaternion().rotation_difference(prev.to_quaternion()).angle))
 prev=m
assert max(angles)<5, max(angles)
(Q/'Notes/camera_v017_verification.json').write_text(json.dumps({'six_event_checks':rows,'max_camera_step_m':max(speeds),'max_camera_rotation_step_degrees':max(angles),'first_pullback_step_m':speeds[0],'camera_transition_no_single_frame_jump':True,'scene_seconds':s.frame_end/24},indent=2))
print('CAMERA_V017_VERIFIED')
