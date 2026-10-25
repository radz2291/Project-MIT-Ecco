import bpy,json,time,sys,shutil
from pathlib import Path
B=Path(__file__).resolve().parents[1];P=B.parent/'Sequence_v001'
bpy.ops.wm.open_mainfile(filepath=str(B/'Scenes/S07_Monumental-Precision_v002.blend'));s=bpy.context.scene
batch='--batch' in sys.argv;frames=range(61,146) if batch else [61,76,94,108,128,145]
folder=B/('Cache/frames' if batch else 'Previews/Checks');folder.mkdir(parents=True,exist_ok=True)
rec=[]
if batch:
 prior=json.loads((P/'Records/render-timings.json').read_text())
 for row in prior:
  f=row['frame']
  if f<=60 or f>=146:
   shutil.copy2(P/f'Cache/frames/{f:04d}.png',folder/f'{f:04d}.png');rec.append(dict(row,reused_from='v001'))
for f in frames:
 s.frame_set(f);s.render.filepath=str(folder/f'{f:04d}.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);sec=time.perf_counter()-t
 rec.append({'frame':f,'seconds':sec});(B/('Records/render-timings.json' if batch else 'Records/benchmark.json')).write_text(json.dumps(sorted(rec,key=lambda x:x['frame']),indent=2));print('TIMING',f,round(sec,3),flush=True)
 if sec>=5:raise RuntimeError('Five-second cap exceeded')
print('COMPLETE',flush=True)
