import bpy,json
from mathutils import Vector
s=bpy.context.scene;E=json.load(open(bpy.path.abspath('//../../../Records/Tasks/T-007/Evidence/v009/build_v009.json')))
for e in E['events']:
 s.frame_set(e['emit']+5);bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();forward=s.camera.rotation_euler.to_quaternion()@Vector((0,0,-1))
 for name,p in [('origin',Vector(e['origin'])),('mid',Vector(e['origin']).lerp(Vector(e['wall']),.5)),('wall',Vector(e['wall']))]:
  start=p-forward*2;hits=[]
  for ins in dg.object_instances:
   o=ins.object
   if o.type!='MESH' or o.original.hide_render or 'CUTTER' in o.name or o.name.startswith(('TX','ECHO','EMITTER','WALL_CONTACT','CONTACT_AFTER')):continue
   inv=ins.matrix_world.inverted();ok,co,no,idx=o.ray_cast(inv@start,(inv.to_3x3()@forward).normalized())
   if ok:
    co=ins.matrix_world@co;distance=(co-start).length
    if distance<2.001:hits.append((distance,o.name))
  print(e['cycle'],name,sorted(hits)[:2])
