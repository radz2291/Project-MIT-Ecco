import bpy,json
from pathlib import Path
B=Path(__file__).resolve().parents[1];p=B/'Scenes/S04_continuous_ABCD_v034.blend';src=B.parent/'Previs_v033/Scenes/S04_continuous_ABCD_v033.blend';bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False,use_scripts=False);bpy.context.scene.frame_set(1);states={o.name:o.hide_render for o in bpy.data.objects if o.type=='MESH' and o.library is None and any(m and 'v033 presentation' in m.name for m in o.data.materials)};bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False,use_scripts=False)
for name,hidden in states.items():
 o=bpy.data.objects.get(name)
 if o:
  for f,v in [(1,hidden),(335,hidden),(336,True),(432,True)]:o.hide_render=v;o.keyframe_insert('hide_render',frame=f)
s=bpy.context.scene;s.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(p));(B/'Records/tool-visibility.json').write_text(json.dumps(states,indent=2));print('Restored',len(states),'original hidden',sum(states.values()))
