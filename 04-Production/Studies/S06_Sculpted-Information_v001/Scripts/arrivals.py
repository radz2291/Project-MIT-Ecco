import bpy,time,json
from pathlib import Path
B=Path(__file__).resolve().parents[1]
timings=[]
for i in (1,2,3):
    bpy.ops.wm.open_mainfile(filepath=str(B/f'Scenes/Arrival_{i}.blend'))
    s=bpy.context.scene;s.render.filepath=str(B/f'Previews/Arrival_{i}.png')
    t=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t
    timings.append({'arrival':i,'seconds':dt,'engine':s.render.engine,'samples':s.eevee.taa_render_samples,'resolution':[960,540]})
    (B/'Records/arrival-benchmark.json').write_text(json.dumps(timings,indent=2))
print('BENCHMARK',timings)
