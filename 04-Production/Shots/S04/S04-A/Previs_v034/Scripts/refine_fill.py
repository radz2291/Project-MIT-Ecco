import bpy
from mathutils import Vector
from pathlib import Path
b=Path(__file__).resolve().parents[1];p=b/'Scenes/S04_continuous_ABCD_v034.blend';bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False,use_scripts=False);s=bpy.context.scene;o=next(o for o in s.objects if o.type=='LIGHT' and o.name.startswith('Stage - Low soft inspection fill'));o.location=(-3.2,-.05,.45);o.rotation_euler=(Vector((-3.2,.03,-.159))-o.location).to_track_quat('-Z','Y').to_euler();s.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(p))
