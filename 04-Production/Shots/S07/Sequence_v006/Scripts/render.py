import bpy,json,time,sys,shutil,hashlib
from pathlib import Path
B=Path(__file__).resolve().parents[1];P=B.parent/'Sequence_v005'
bpy.ops.wm.open_mainfile(filepath=str(B/'Scenes/S07_Monumental-Precision_v006.blend'));s=bpy.context.scene
batch='--batch' in sys.argv;frames=range(121,193) if batch else [121,128,136,148,156,164,184,192]
folder=B/('Cache/frames' if batch else 'Previews/Checks');folder.mkdir(parents=True,exist_ok=True);rec=[]
if batch:
 old=json.loads((P/'Records/render-timings.json').read_text())
 for f in range(1,121):
  src=P/f'Cache/frames/{f:04d}.png';dst=folder/f'{f:04d}.png';shutil.copy2(src,dst);assert hashlib.sha256(src.read_bytes()).digest()==hashlib.sha256(dst.read_bytes()).digest();r=old[f-1].copy();r['reused_from']='v005';rec.append(r)
for f in frames:
 s.frame_set(f);s.render.filepath=str(folder/f'{f:04d}.png');start=time.perf_counter();bpy.ops.render.render(write_still=True);sec=time.perf_counter()-start
 rec.append({'frame':f,'seconds':sec});(B/('Records/render-timings.json' if batch else 'Records/benchmark.json')).write_text(json.dumps(rec,indent=2));print('TIMING',f,round(sec,3),flush=True)
 if sec>=5:raise RuntimeError('Five-second render cap exceeded')
print('COMPLETE',flush=True)
