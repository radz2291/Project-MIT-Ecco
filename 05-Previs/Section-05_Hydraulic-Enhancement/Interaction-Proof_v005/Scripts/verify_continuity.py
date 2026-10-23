import bpy,json,hashlib
from pathlib import Path
from mathutils import Vector
B=Path(__file__).resolve().parents[1];OLD=B.parent/'Interaction-Proof_v004';s=bpy.context.scene
rows=json.loads((OLD/'Records/tracks.json').read_text());s.frame_set(72);hold=s.camera.matrix_world.copy();cam_error=0;head_error=0;routes=set();record_error=0
retained=bpy.data.collections['S05_VOLUME_FLOW_v004'];retained.hide_viewport=False
for f in range(1,145):
 s.frame_set(f);dg=bpy.context.evaluated_depsgraph_get()
 if 25<=f<=120:cam_error=max(cam_error,max(abs(s.camera.matrix_world[i][j]-hold[i][j]) for i in range(4) for j in range(4)))
 for p in rows:
  if p['kind']!='fluid':continue
  o=bpy.data.objects[f'S05_v005_MovingSegment_{p["index"]:02}']
  if o.hide_render:continue
  routes.add(p['route']);ev=o.evaluated_get(dg);me=ev.to_mesh();head=sum((v.co for v in list(me.vertices)[:6]),Vector())/6
  record_error=max(record_error,(head-Vector(p['heads'][f-1])).length);ev.to_mesh_clear()
  previous=bpy.data.objects[f'S05_v004_fluid_HistoryTail_{p["index"]:02}'];pev=previous.evaluated_get(dg);pm=pev.to_mesh();oldhead=sum((v.co for v in list(pm.vertices)[:6]),Vector())/6
  head_error=max(head_error,(head-oldhead).length);pev.to_mesh_clear()
retained.hide_viewport=True
assert cam_error<1e-7 and head_error<1e-6 and len(routes)==18
prior_hash=hashlib.sha256((OLD/'Scenes/S05_twisted-pad_interaction_v004.blend').read_bytes()).hexdigest();assert prior_hash=='a2c19e453bdb164a337ac961b7fcf47950041a69610284919b0bae84afbf361c'
result={'camera_hold_frames':[25,120],'maximum_camera_matrix_change_during_hold':cam_error,'maximum_evaluated_tracer_leading_centre_deviation_from_v004_m':head_error,'maximum_deviation_from_authored_track_records_m':record_error,'record_note':'Comparison uses evaluated v004 geometry because its absolute shape-key evaluation differs slightly from the authored sample records; the source-to-successor difference remains below one micrometre.','all_18_routes_still_represented':True,'prior_v004_sha256':prior_hash,'limits':'Output-frame comparisons; no audience comprehension claim.'}
(B/'Records/continuity-verification.json').write_text(json.dumps(result,indent=2));s.frame_set(72)
