import bpy,pathlib,json,numpy as np,hashlib
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
R=pathlib.Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');T=R/'04-Production/Records/Tasks/T-056';s=bpy.context.scene;p=json.loads((T/'ribbon-build_v010.json').read_text());a=Vector(p['path_start']);b=Vector(p['path_end']);axis=b-a;D=axis.length;direction=axis.normalized();records=[]
for f in [1,24,30,37,42,48,54,65,66,78,90,102,114,118,123,124,140,168]:
 s.frame_set(f);dep=bpy.context.evaluated_depsgraph_get();row={'frame':f,'packets':[]}
 for name,echo in [('OUTGOING_FINITE_PACKET',False),('RETURN_FINITE_PACKET',True)]:
  ob=bpy.data.objects[name];ev=ob.evaluated_get(dep);n=len(ev.data.vertices);co=np.empty(n*3);ev.data.vertices.foreach_get('co',co);co=co.reshape(-1,3);route=np.empty(n);ob.data.attributes['route_u'].data.foreach_get('value',route);front=(f-(66 if echo else 18))/(36 if echo else 30);phase=(front-(1-route if echo else route))/.44;active=(phase>0)&(phase<1);projection=[]
  if active.any():
   for u in [float(route[active].min()),float(route[active].max())]:projection.append(list(world_to_camera_view(s,s.camera,a+axis*u)))
  row['packets'].append({'name':name,'geometry_hash':hashlib.sha256(co.tobytes()).hexdigest(),'matrix':[list(r) for r in ob.matrix_world],'active_route_bounds':[float(route[active].min()),float(route[active].max())] if active.any() else None,'active_screen_endpoints':projection,'height_m':float(np.ptp(co[active,2])) if active.any() else 0,'route_coordinate_error_max_m':float(np.max(abs(co@np.array(direction)-route*D)))})
 row['cues']={name:not bpy.data.objects[name].hide_render for name in ['EMISSION_ON_SAME_SENSOR','EXACT_WALL_CONTACT_RIPPLE','SAME_SENSOR_RECEIPT','POST_RECEIPT_WALL_MEASUREMENT']};records.append(row)
(T/'causal-verification_v012.json').write_text(json.dumps({'records':records,'sensor_screen':list(world_to_camera_view(s,s.camera,a)),'wall_screen':list(world_to_camera_view(s,s.camera,b))},indent=2));print('TRAJECTORY',[(r['frame'],[(x['name'],x['active_route_bounds'],round(x['height_m'],5)) for x in r['packets']],r['cues']['POST_RECEIPT_WALL_MEASUREMENT']) for r in records])
