"""Keep hidden endpoint recycling from interpolating through the tool."""
import bpy,json
from pathlib import Path
B=Path(__file__).resolve().parents[1];rows=json.loads((B/'Records/tracks.json').read_text());resets=[]
def curves(block):
 for layer in block.animation_data.action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    yield from bag.fcurves
for p in rows:
 i=p['index'];wraps=[f for f in range(1,144) if p['heads'][f][2]-p['heads'][f-1][2]<-.5]
 tail=bpy.data.objects[f'S05_v004_{p["kind"]}_HistoryTail_{i:02}'];keys=tail.data.shape_keys
 for f in range(1,145):keys.eval_time=(f-1)*10;keys.keyframe_insert('eval_time',frame=f)
 for fc in curves(keys):
  for k in fc.keyframe_points:k.interpolation='CONSTANT' if round(k.co.x) in wraps else 'LINEAR'
 if p['kind']=='rock':
  rock=bpy.data.objects[f'S05_v004_Rock_{i:02}']
  for fc in curves(rock):
   if fc.data_path=='location':
    for k in fc.keyframe_points:k.interpolation='CONSTANT' if round(k.co.x) in wraps else 'LINEAR'
 resets.append({'index':i,'hidden_endpoint_wrap_after_frames':wraps})
bpy.context.scene.frame_set(72);bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
result={'resets':resets,'meaning':'Fade at display endpoints; stepped hidden recycling rather than interpolated travel through the hardware. Not a physical recirculation loop.'}
(B/'Records/interpolation-safety.json').write_text(json.dumps(result,indent=2))
