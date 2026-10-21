import bpy,json,time
from pathlib import Path
B=Path(__file__).resolve().parents[1];rows=json.loads((B/'Records/timings-render.json').read_text());bad=json.loads((B/'Records/recovered-frame-check.json').read_text())['bad'];bpy.ops.wm.open_mainfile(filepath=str(B/'Scenes/S04_continuous_ABCD_v033.blend'),load_ui=False,use_scripts=False);s=bpy.context.scene
for item in bad:
 f=item['frame'];s.frame_set(f);s.render.filepath=str(B/'Work/Frames'/f'S04_{f:04d}.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t;assert dt<5;rows[f-1]={'frame':f,'seconds':dt};(B/'Records/timings-render.json').write_text(json.dumps(rows,indent=2));print('REPAIRED',f,dt,flush=True)
