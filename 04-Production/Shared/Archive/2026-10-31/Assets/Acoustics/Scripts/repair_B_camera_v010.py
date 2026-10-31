"""Intentional downhole-facing B view after actual finite-rim failure."""
import bpy,json,sys,hashlib
from pathlib import Path
from mathutils import Vector
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[4];T=ROOT/'04-Production/Records/Tasks/T-046';sys.path.insert(0,str(HERE));from build_sensing_v001 import save,dump
src=T/'Scenes/Sensing_reuse_B_v009.blend';beforehash=hashlib.sha256(src.read_bytes()).hexdigest();bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False,use_scripts=False);s=bpy.context.scene;cam=s.camera
events=json.loads((T/'Evidence/events_B_v003.json').read_text())['events'];targets=[(Vector(e['emitter_world_m'])+Vector(e['hit_world_m']))*.5 for e in events];before=[];after=[]
for f in range(1,s.frame_end+1):
 s.frame_set(f);old=cam.location.copy();before.append(list(old));t=(f-1)/24;u=max(0,min(1,(t-1.9)/.45));u=u*u*(3-2*u);target=targets[0].lerp(targets[1],u);cam.location.x=old.x-.12;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.keyframe_insert(data_path='location',frame=f);cam.keyframe_insert(data_path='rotation_euler',frame=f);after.append(list(cam.location))
s.frame_set(17);save(T/'Scenes/Sensing_reuse_B_v010.blend');assert hashlib.sha256(src.read_bytes()).hexdigest()==beforehash
dump(T/'Evidence/intentional-camera-revision_B_v010.json',dict(source=src.relative_to(ROOT).as_posix(),source_sha256=beforehash,source_preserved=True,change='Only camera axial offset+.060→−.060m and look direction; finite uphole rim was actually visible. Same lens, event JSON, source geometry, timing and independently owned motion.',before_locations=before,after_locations=after,lens=cam.data.lens,timing=[s.frame_start,s.frame_end,s.render.fps],event_export='Evidence/events_B_v003.json'))
