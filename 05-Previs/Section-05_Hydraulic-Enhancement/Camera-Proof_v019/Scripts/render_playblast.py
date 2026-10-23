import bpy,time,json
from pathlib import Path
B=Path(__file__).resolve().parents[1];s=bpy.context.scene
F=Path('D:/MIT-ECCO-Render-Recovery/S05-v019-RenderCache/Frames');F.mkdir(parents=True,exist_ok=True)
assert s.render.resolution_x==960 and s.render.resolution_y==540 and s.eevee.taa_render_samples==4
log=B/'Records/render-timings.json';rows=json.loads(log.read_text()) if log.exists() else []
for f in range(START,END+1):
 assert f not in [r['frame'] for r in rows]
 s.frame_set(f);s.render.filepath=str(F/f'S05_{f:04d}.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);duration=time.perf_counter()-t
 rows.append({'frame':f,'seconds':duration});log.write_text(json.dumps(rows,indent=2));assert duration<5,('Frame budget',f,duration)
result={'completed':END,'frame_count':len(rows),'max_seconds':max(r['seconds'] for r in rows),'mean_seconds':sum(r['seconds'] for r in rows)/len(rows)}
