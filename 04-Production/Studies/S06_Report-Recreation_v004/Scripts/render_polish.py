import bpy,time,json,sys
from pathlib import Path
B=Path(__file__).resolve().parents[1];bpy.ops.wm.open_mainfile(filepath=str(B/'Scenes/S06_cinematic-study_v004_polished.blend'));s=bpy.context.scene
bench='--batch' not in sys.argv;last=int(sys.argv[sys.argv.index('--end')+1]) if '--end' in sys.argv else 288
frames=[90,100,108,120,145,172,192,204,216,228,240,260,288] if bench else range(1,last+1)
folder=B/('Previews/Polish-checks' if bench else 'Cache/polished');folder.mkdir(parents=True,exist_ok=True)
rec=[] if bench or last==288 else [x for x in json.loads((B/'Records/polish-render-timings.json').read_text()) if x['frame']>last]
for f in frames:
 s.frame_set(f);s.eevee.taa_render_samples=48 if 228<=f<=258 else 32 if 90<=f<=144 else 16;s.render.filepath=str(folder/f'{f:04d}.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);sec=time.perf_counter()-t
 rec.append({'frame':f,'seconds':sec,'samples':s.eevee.taa_render_samples});print('TIMING',f,round(sec,3),flush=True)
 (B/('Records/polish-benchmark.json' if bench else 'Records/polish-render-timings.json')).write_text(json.dumps(sorted(rec,key=lambda x:x['frame']),indent=2))
 if sec>=5:raise RuntimeError('Render exceeds five-second cap: '+str(sec))
print('COMPLETE',sum(r['seconds'] for r in rec),flush=True)
