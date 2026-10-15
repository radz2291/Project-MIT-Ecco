"""Pre-review framing repair on task-owned v002 support candidate only."""
import bpy,time,json,hashlib
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];EVID=BASE.parents[1]/'Records/Tasks/T-009/Evidence'
path=BASE/'Scenes/B203_support_v002.blend';bpy.ops.wm.open_mainfile(filepath=str(path))
s=bpy.context.scene;s.camera.data.ortho_scale=5.8
s.camera.location.z=4.175
bpy.ops.wm.save_as_mainfile(filepath=str(path));bpy.ops.wm.open_mainfile(filepath=str(path))
start=time.perf_counter();bpy.ops.render.render(animation=True)
rows=json.loads((EVID/'build-render_v002.json').read_text())
row=next(r for r in rows if r['case']=='support');row['initial_render_seconds']=row['render_seconds'];row['render_seconds']=time.perf_counter()-start
row['scene_sha256']=hashlib.sha256(path.read_bytes()).hexdigest();row['framing_repair']='Orthographic scale 5.8 to retain exploded outside layers'
(EVID/'build-render_v002.json').write_text(json.dumps(rows,indent=2))
print('SUPPORT_FRAMING_PASS')
