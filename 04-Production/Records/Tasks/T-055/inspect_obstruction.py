import bpy,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[4];T=Path(__file__).resolve().parent
src=R/'05-Previs/Section-02_Measurement-History/v011/Continuation/Scenes/S01-S02_continuous_v011.blend'
records=[]
for label,p in [('baseline',src),('candidate',T/'Consumers/S02_shared-descent_v001.blend')]:
 bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False);s=bpy.context.scene
 for f in [90,94,96,98,100]:
  s.frame_set(f);c=s.camera;origin=c.matrix_world.translation;direction=c.matrix_world.to_quaternion()@Vector((0,0,-1));result=s.ray_cast(bpy.context.evaluated_depsgraph_get(),origin,direction)
  records.append({'label':label,'frame':f,'camera':list(origin),'hit':result[4].name if result[0] else None,'location':list(result[1]) if result[0] else None})
(T/'Evidence/obstruction.json').write_text(json.dumps(records,indent=2));print(json.dumps(records))
