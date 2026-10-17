import bpy,json
from mathutils import Vector
s=bpy.context.scene;E=json.load(open(bpy.path.abspath('//../../../Records/Tasks/T-007/Evidence/v009/build_v009.json')))
for e in E['events']:
 s.frame_set(e['emit']+5);bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();cam=s.camera;forward=cam.rotation_euler.to_quaternion()@Vector((0,0,-1))
 for name,p in [('origin',Vector(e['origin'])),('mid',Vector(e['origin']).lerp(Vector(e['wall']),.5)),('wall',Vector(e['wall']))]:
  start=p-forward*2;hit,co,no,i,obj,mat=s.ray_cast(dg,start,forward,distance=2.001)
  print('VIS',e['cycle'],name,hit,obj.name if hit else None,round((co-p).length,5) if hit else None)
 print('TX',bpy.data.objects[f'TX_{e["cycle"]}'].hide_render,list(bpy.data.objects[f'TX_{e["cycle"]}'].matrix_world.translation),list(bpy.data.objects[f'TX_{e["cycle"]}'].scale))
