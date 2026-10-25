import bpy,sys,time,json
from pathlib import Path
B=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(B/'Scenes/S06_cinematic-study_v002.blend'))
s=bpy.context.scene
bench=[]
for i,f in enumerate((61,142,276),1):
    s.frame_set(f);s.render.filepath=str(B/f'Previews/S06_arrival_{i:02d}_v002.png')
    start=time.perf_counter();bpy.ops.render.render(write_still=True);elapsed=time.perf_counter()-start
    bench.append({'frame':f,'seconds':elapsed,'resolution':[1280,720],'samples':16})
    (B/'Records/benchmark.json').write_text(json.dumps(bench,indent=2),encoding='utf-8')
    if elapsed>=5:raise RuntimeError('Render cap exceeded. Batch not released.')
if '--stills-only' not in sys.argv:
    folder=B/'Cache/journey';folder.mkdir(exist_ok=True,parents=True);timings=[]
    for f in range(1,289):
        s.frame_set(f);s.render.filepath=str(folder/f'{f:04d}.png')
        start=time.perf_counter();bpy.ops.render.render(write_still=True);elapsed=time.perf_counter()-start
        timings.append({'frame':f,'seconds':elapsed})
        (B/'Records/render-timings.json').write_text(json.dumps(timings),encoding='utf-8')
        if elapsed>=5:raise RuntimeError('Batch render cap exceeded.')
    print('RENDER COMPLETE',len(timings),sum(x['seconds'] for x in timings))
