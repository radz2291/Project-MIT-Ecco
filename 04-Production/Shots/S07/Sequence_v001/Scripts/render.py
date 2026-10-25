import bpy,time,json,sys
from pathlib import Path
B=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(B/'Scenes/S07_Monumental-Precision_v001.blend'));s=bpy.context.scene
batch='--batch' in sys.argv;frames=range(1,193) if batch else [1,20,48,80,112,144,192]
folder=B/('Cache/frames' if batch else 'Previews/Checks');folder.mkdir(parents=True,exist_ok=True)
rec=[]
for f in frames:
 s.frame_set(f);s.render.filepath=str(folder/f'{f:04d}.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);sec=time.perf_counter()-t
 rec.append({'frame':f,'seconds':sec});(B/('Records/render-timings.json' if batch else 'Records/benchmark.json')).write_text(json.dumps(rec,indent=2));print('TIMING',f,round(sec,3),flush=True)
 if sec>=5:raise RuntimeError('Per-frame cap exceeded; stop and reduce cost')
print('COMPLETE',sum(x['seconds'] for x in rec),flush=True)
