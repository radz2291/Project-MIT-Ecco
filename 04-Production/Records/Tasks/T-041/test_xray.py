import bpy
from pathlib import Path
p=Path(__file__).resolve().parents[3]/'Shots/S02/PREVIS-T041'
bpy.ops.wm.open_mainfile(filepath=str(p/'Scenes/S02_previs_T041_v002.blend'))
for o in bpy.data.collections['T41_SYNTHETIC_WALL_READINGS'].objects:o.show_in_front=True
s=bpy.context.scene;s.frame_set(266);s.render.filepath=str(p/'Previews/xray_test.png');bpy.ops.render.render(write_still=True)
