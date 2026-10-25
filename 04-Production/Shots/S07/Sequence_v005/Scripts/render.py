import bpy,json,time,sys
from pathlib import Path
B=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(B/'Scenes/S07_Monumental-Precision_v005.blend'));s=bpy.context.scene
batch='--batch' in sys.argv;frames=range(1,193) if batch else [1,30,60,61,90,120,121,150,178,192]
folder=B/('Cache/frames' if batch else 'Previews/Checks');folder.mkdir(parents=True,exist_ok=True);rec=[]
for f in frames:
 s.frame_set(f);s.render.filepath=str(folder/f'{f:04d}.png');start=time.perf_counter();bpy.ops.render.render(write_still=True);sec=time.perf_counter()-start
 rec.append({'frame':f,'seconds':sec});(B/('Records/render-timings.json' if batch else 'Records/benchmark.json')).write_text(json.dumps(rec,indent=2));print('TIMING',f,round(sec,3),flush=True)
 if sec>=5:raise RuntimeError('Five-second render cap exceeded')
print('COMPLETE',flush=True)


