"""Save the owned candidate with its intended preview view layer active in Blender."""
import bpy,json,hashlib
from pathlib import Path
P=Path(__file__).resolve().parents[3];E=P/'Records/Tasks/T-007/Evidence/Motion_v002';r=json.loads((E/'build.json').read_text());scene=P/r['scene']
assert hashlib.sha256(scene.read_bytes()).hexdigest()==r['scene_sha256']
bpy.ops.wm.open_mainfile(filepath=str(scene));bpy.context.window.view_layer=bpy.context.scene.view_layers['FAST model and mechanism'];bpy.context.scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(scene),relative_remap=False)
r['scene_sha256']=hashlib.sha256(scene.read_bytes()).hexdigest();r['saved_active_view_layer']='FAST model and mechanism';(E/'build.json').write_text(json.dumps(r,indent=2))
