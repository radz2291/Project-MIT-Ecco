import bpy,json,time,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from fast_preview import configure
P=Path(__file__).resolve().parents[3];E=P/'Records/Tasks/T-007/Evidence/FastPreview_v003';E.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(P/'Mechanisms/B201/Scenes/B201_returning-echo_still04_v003.blend'));s=bpy.context.scene
root,material,instances=configure(s,32)
results=[]
for i in range(3):
 s.frame_set(i+1);s.render.filepath=str(E/f'eevee_test_{i:02d}.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);results.append(time.perf_counter()-t)
 (E/'benchmark.json').write_text(json.dumps({'engine':s.render.engine,'resolution':[960,540],'samples':32,'native_blended_transparency':True,'render_seconds':results,'product_instances':instances},indent=2));print('BENCHMARK',i,results[-1],flush=True)
