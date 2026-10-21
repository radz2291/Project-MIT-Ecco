import bpy,time,json
from pathlib import Path
B=Path(__file__).resolve().parents[1];CACHE=Path(json.loads((B/'Records/storage.json').read_text())['cache_work_root'])
def render_batch(frames):
 s=bpy.context.scene;assert bpy.data.filepath==str(B/'Scenes/S04_continuous_ABCD_v034.blend').replace('\\','/') or Path(bpy.data.filepath)==B/'Scenes/S04_continuous_ABCD_v034.blend'
 rows={r['frame']:r for r in json.loads((B/'Records/timings-render.json').read_text())};done=[];stopped=False
 for f in frames:
  s.frame_set(f);s.render.filepath=str(CACHE/'Frames'/f'S04_{f:04d}.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t;rows[f]={'frame':f,'seconds':dt,'execution':'running Blender'};done.append({'frame':f,'seconds':dt});(B/'Records/timings-render.json').write_text(json.dumps(sorted(rows.values(),key=lambda r:r['frame']),indent=2))
  if dt>=5:stopped=True;break
 return {'completed_total':len(rows),'new_frames':done,'stopped_over_budget':stopped}
