import bpy
from bpy_extras.object_utils import world_to_camera_view
s=bpy.context.scene;s.frame_set(1);bpy.context.view_layer.update()
for o in s.objects:
 if o.type=='MESH' and ('CONTACT' in o.name or 'TX_' in o.name or 'ECHO_' in o.name or 'EMITTER_' in o.name):
  p=world_to_camera_view(s,s.camera,o.matrix_world.translation)
  print(o.name,'hide',o.hide_render,o.hide_viewport,'scale',list(o.scale),'pix',int(p.x*1280),int((1-p.y)*720),'color',list(o.color))
s.render.filepath=bpy.path.abspath('//../Previews/v007/fresh-f1.png');bpy.ops.render.render(write_still=True)
