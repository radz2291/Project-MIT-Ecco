import bpy,json
from mathutils import Vector
s=bpy.context.scene;s.frame_set(240);bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get()
print('CONTROL',dict(bpy.data.objects['B201_CONTROL'].items()))
for n in ['TX_1','TX_4','TX_6','WALL_CONTACT_1','WALL_CONTACT_4','WALL_CONTACT_6','EMITTER_4','EMITTER_6','ASSEMBLY_ROTATION_X','T6_IRREGULAR_VIEW_WINDOW']:
 o=bpy.data.objects[n];print('OBJECT',n,'hidden',o.hide_render,'loc',list(o.matrix_world.translation),'rot',list(o.rotation_euler),'scale',list(o.scale))
 if o.animation_data:
  for f in o.animation_data.drivers:print('DRIVER',f.data_path,f.array_index,f.driver.expression,f.driver.is_valid)
print('RIG rotation',bpy.data.objects['ASSEMBLY_CONTROL']['rotation_rad'])
for ins in dg.object_instances:
 if ins.is_instance and 'Imaging port 1' in ins.object.name:print('CAP INSTANCE',ins.object.name,[list(row) for row in ins.matrix_world])
