import bpy,time,json
from pathlib import Path
B=Path(__file__).resolve().parents[1];p=B/'Scenes/S04_cinematic-previs_v006.blend'
bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False,use_scripts=False);s=bpy.context.scene
s.display.render_aa='FXAA';rear=bpy.data.objects['Section 2 retained opposite ground'];rear.hide_render=True;rear.hide_viewport=True
s.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(p))
rows=[]
for f in [23,72,116,292,432]:
 s.frame_set(f);s.render.filepath=str(B/'Previews'/f'S04_{f:04d}.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);rows.append(dict(frame=f,seconds=time.perf_counter()-t))
(B/'Records/timings-fast-benchmark.json').write_text(json.dumps(rows,indent=2));assert max(x['seconds'] for x in rows)<5
