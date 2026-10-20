import bpy,json
from pathlib import Path
from mathutils import Vector
R=Path(r'C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco')
p=R/'05-Previs/Section-02_Measurement-History/v011/Continuation/Scenes/S01-S02_continuous_v011.blend'
bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False,use_scripts=False);bpy.context.scene.frame_set(450);bpy.context.view_layer.update()
out=[]
for o in bpy.context.scene.objects:
 if any(x in o.name.lower() for x in ['rock','soil','formation','bore','wall','environment','mud']):
  out.append(dict(name=o.name,type=o.type,location=list(o.location),matrix=[list(r) for r in o.matrix_world],bounds=([list(o.matrix_world@Vector(v)) for v in o.bound_box] if o.type=='MESH' else []),materials=[m.name if m else None for m in o.data.materials] if o.type=='MESH' else [],library=o.library.filepath if o.library else None,hidden=o.hide_render,parent=o.parent.name if o.parent else None))
(Path(__file__).resolve().parents[1]/'Records/S02-inspection.json').write_text(json.dumps(dict(objects=out,world=bpy.context.scene.world.name,collections=[c.name for c in bpy.data.collections]),indent=2))
print(json.dumps(out,indent=2)[:11000])
