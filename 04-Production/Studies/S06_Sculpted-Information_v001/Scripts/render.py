import bpy,sys,time,json
from pathlib import Path
B=Path(__file__).resolve().parents[1]
mode=sys.argv[-1] if sys.argv[-1] in ('proof','journey') else 'proof'
bpy.ops.wm.open_mainfile(filepath=str(B/f'Scenes/S06_{mode}_v001.blend'))
s=bpy.context.scene;cache=B/f'Cache/{mode}';cache.mkdir(exist_ok=True)
bench=[]
for f in ([1,55,120] if mode=='proof' else [1,132,275]):
    s.frame_set(f);s.render.filepath=str(B/f'Previews/{mode}_benchmark_{f:03d}.png')
    t=time.perf_counter();bpy.ops.render.render(write_still=True);sec=time.perf_counter()-t;bench.append({'frame':f,'seconds':sec})
    (B/f'Records/{mode}-benchmark.json').write_text(json.dumps(bench,indent=2))
    if sec>=5:raise RuntimeError('Render cap exceeded; do not batch')
timings=[]
for f in range(1,s.frame_end+1):
    s.frame_set(f);s.render.filepath=str(cache/f'{f:04d}.png')
    t=time.perf_counter();bpy.ops.render.render(write_still=True);sec=time.perf_counter()-t;timings.append({'frame':f,'seconds':sec})
    (B/f'Records/{mode}-timings.json').write_text(json.dumps(timings))
    if sec>=5:raise RuntimeError('Render cap exceeded during batch')
print('RENDER COMPLETE',mode,len(timings))
