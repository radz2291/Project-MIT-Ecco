import bpy,json
from mathutils import Vector
h=bpy.data.objects['ECCO_HOUSING_SOURCE_MESH']; inv=h.matrix_world.inverted();out=[]
for o in bpy.data.collections['ECCO_TEMPORARY_CLOSURES'].objects:
    if 'Service cover' not in o.name:continue
    p=o.matrix_world.translation;n=Vector((0,p.y,p.z)).normalized();t=Vector((0,-n.z,n.y));hits=[]
    for dx,dt in [(0,0),(-.06,0),(.06,0),(0,-.032),(0,.032),(-.06,-.032),(.06,.032)]:
        start=Vector((p.x+dx,0,0))+n*.3+t*dt
        ok,hit,normal,idx=h.ray_cast(inv@start,inv.to_3x3()@(-n))
        hits.append({'dx':dx,'dt':dt,'hit_m':list(h.matrix_world@hit) if ok else None,'radius':(h.matrix_world@hit).dot(n) if ok else None})
    out.append({'name':o.name,'p':list(p),'hits':hits})
print('COVER_SEATS',json.dumps(out))
