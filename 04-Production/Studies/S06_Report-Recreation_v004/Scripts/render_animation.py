import bpy,time,json,sys
from pathlib import Path
B=Path(__file__).resolve().parents[1];bpy.ops.wm.open_mainfile(filepath=str(B/'Scenes/S06_cinematic-study_v004.blend'));s=bpy.context.scene
bench='--batch' not in sys.argv;start=int(sys.argv[sys.argv.index('--start')+1]) if '--start' in sys.argv else 1
frames=[96,120,160,172,192,204,230,244,250,276] if bench else range(start,289)
folder=B/('Previews/Animation-checks' if bench else 'Cache/animation');folder.mkdir(parents=True,exist_ok=True)
rec=[] if bench or start==1 else [x for x in json.loads((B/'Records/animation-render-timings.json').read_text()) if x['frame']<start]
for f in frames:
    s.frame_set(f);s.render.filepath=str(folder/f'{f:04d}.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);sec=time.perf_counter()-t
    rec.append({'frame':f,'seconds':sec});print('TIMING',f,round(sec,3),flush=True)
    (B/('Records/animation-benchmark.json' if bench else 'Records/animation-render-timings.json')).write_text(json.dumps(rec,indent=2),encoding='utf-8')
    if sec>=5:raise RuntimeError('Frame cost exceeds owner cap: '+str(sec))
print('RENDER COMPLETE',sum(x['seconds'] for x in rec),flush=True)
