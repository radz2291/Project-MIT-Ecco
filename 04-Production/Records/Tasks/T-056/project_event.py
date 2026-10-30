import bpy,json,pathlib
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
root=pathlib.Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco')
s=bpy.context.scene
out={'fps':s.render.fps,'resolution':[s.render.resolution_x,s.render.resolution_y],'frames':{}}
for f in range(294,343):
 s.frame_set(f);bpy.context.view_layer.update()
 d={}
 for name in ['DW 1 SEND front0 core','DW 1 ECHO front0 core','DW 1 fixed native contact pin']:
  o=bpy.data.objects.get(name)
  if o:
   e=o.evaluated_get(bpy.context.evaluated_depsgraph_get()); mesh=e.to_mesh()
   coords=[e.matrix_world@v.co for v in mesh.vertices] if mesh else []
   center=sum(coords,Vector())/len(coords) if coords else o.matrix_world.translation
   e.to_mesh_clear()
   p=world_to_camera_view(s,s.camera,center)
   d[name]={'screen':[p.x,1-p.y],'visible':not o.hide_render,'world':list(center)}
 out['frames'][str(f)]=d
receiver=Vector(out['frames']['318']['DW 1 ECHO front0 core']['world'])
for f in range(294,343):
 s.frame_set(f);bpy.context.view_layer.update()
 p=world_to_camera_view(s,s.camera,receiver)
 out['frames'][str(f)]['receiver_anchor']={'screen':[p.x,1-p.y],'world':list(receiver),'provenance':'First return-front endpoint at frame 318; fixed cycle receiver'}
(root/'04-Production/Records/Tasks/T-056/event-projection.json').write_text(json.dumps(out,indent=2))
