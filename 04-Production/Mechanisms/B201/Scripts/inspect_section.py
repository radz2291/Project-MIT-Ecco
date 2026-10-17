import bpy,json
from mathutils import Vector
s=bpy.context.scene;s.frame_set(21);bpy.context.view_layer.update()
for o in s.objects:
 if not o.hide_render and o.type in ['MESH','CURVE']:
  print(o.name, list(o.dimensions),list(o.matrix_world.translation),len(o.data.vertices) if o.type=='MESH' else '')
