import bpy
from pathlib import Path
B=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(B/'Scenes/S04_C_capped-resonance_v008.blend'),use_scripts=False,load_ui=False)
s=bpy.context.scene;s.frame_set(32);s.display.shading.show_backface_culling=True;s.render.filepath=str(B/'Previews/C_culling-test.png');bpy.ops.render.render(write_still=True)
