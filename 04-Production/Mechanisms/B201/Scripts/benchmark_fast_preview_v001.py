import bpy,json,time
from pathlib import Path
P=Path.cwd()/'04-Production';E=P/'Records/Tasks/T-007/Evidence/FastPreview_v001';E.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(P/'Mechanisms/B201/Scenes/B201_returning-echo_still04_v003.blend'));s=bpy.context.scene
s.render.engine='BLENDER_EEVEE';s.render.resolution_x=960;s.render.resolution_y=540;s.render.resolution_percentage=100
s.eevee.taa_render_samples=8
s.render.use_persistent_data=True
s.eevee.use_raytracing=False
results=[]
for i in range(3):
 s.frame_set(i+1);s.render.filepath=str(E/f'eevee_test_{i:02d}.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);results.append(time.perf_counter()-t);(E/'benchmark.json').write_text(json.dumps({'engine':s.render.engine,'resolution':[960,540],'samples':8,'render_seconds':results},indent=2));print('BENCHMARK',i,results[-1],flush=True)
