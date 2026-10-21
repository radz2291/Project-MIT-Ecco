import bpy
from pathlib import Path
B=Path(__file__).resolve().parents[1];p=B/'Scenes/S04_continuous_ABCD_v034.blend';bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False,use_scripts=False);s=bpy.context.scene;body=[o for o in bpy.data.objects if o.type=='MESH' and o.library is None and any(m and 'v033 presentation' in m.name for m in o.data.materials)]
for o in body:
 for f,v in [(1,False),(335,False),(336,True),(432,True)]:o.hide_render=v;o.keyframe_insert('hide_render',frame=f)
s.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(p));print('Bodies optimized',len(body))
