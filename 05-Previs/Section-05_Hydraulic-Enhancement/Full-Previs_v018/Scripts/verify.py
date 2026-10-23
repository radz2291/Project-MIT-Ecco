import bpy,math,json,time,hashlib
from pathlib import Path
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
import numpy as np
B=Path(__file__).resolve().parents[1];s=bpy.context.scene;s.frame_set(151);bpy.context.view_layer.update();t0=time.perf_counter()
hardware=list(bpy.data.collections['S05_LINKED_HARDWARE'].objects);base={o.name:o.matrix_world.copy() for o in hardware};vv=[];ff=[]
for o in hardware:
 off=len(vv);vv.extend(o.matrix_world@v.co for v in o.data.vertices);ff.extend([[off+i for i in p.vertices] for p in o.data.polygons])
steel=BVHTree.FromPolygons(vv,ff);R=.155575
fx=bpy.data.collections['S05_v018_ContinuousHydraulics'];rocks=[o for o in fx.objects if 'Cutting' in o.name];wisps=[o for o in fx.objects if 'Wisp' in o.name]
if globals().get('ONLY_ADDED',False):rocks=[];wisps=[o for o in wisps if int(o.name.rsplit('_',1)[-1])>=100]
minimum={'rock_steel':1.,'rock_wall':1.,'wisp_steel_conservative':1.,'wisp_wall_conservative':1.};failures=[];samplecount=0;lastpos={};maxstep={o.name:0 for o in rocks}
times=globals().get('TIMES',[1+i*.5 for i in range(863)])
for f in times:
 s.frame_set(int(f),subframe=f-int(f));bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();a=-math.radians(5)*(f-151)/24;inv=Matrix.Rotation(-a,4,'Z');expected=Matrix.Rotation(a,4,'Z')
 assert all(max(abs(o.matrix_world[i][j]-(expected@base[o.name])[i][j]) for i in range(4) for j in range(4))<1e-5 for o in hardware)
 for o in rocks:
  pts=[inv@(o.matrix_world@v.co) for v in o.data.vertices]
  for p in pts:
   r=math.hypot(p.x,p.y);dist=steel.find_nearest(p)[3];minimum['rock_steel']=min(minimum['rock_steel'],dist);minimum['rock_wall']=min(minimum['rock_wall'],R-r)
   u=Vector((p.x/r,p.y/r,0));hit=steel.ray_cast(Vector((0,0,p.z))+u*.18,-u,.18)[0]
   if (hit is not None and r<math.hypot(hit.x,hit.y)-1e-6) or R-r<0:failures.append({'frame':f,'object':o.name,'type':'rock_inside_solid_or_wall'})
  if o.name in lastpos:maxstep[o.name]=max(maxstep[o.name],(o.location-lastpos[o.name]).length)
  lastpos[o.name]=o.location.copy()
 for o in wisps:
  ev=o.evaluated_get(dg);me=ev.to_mesh();verts=[v.co.copy() for v in me.vertices];ev.to_mesh_clear()
  for j in range(25):
   ring=verts[j*10:(j+1)*10];center=sum(ring,Vector())/10;p=inv@center;rad=max((v-center).length for v in ring);r=math.hypot(p.x,p.y)
   ds=steel.find_nearest(p)[3]-rad;dw=R-r-rad
   minimum['wisp_steel_conservative']=min(minimum['wisp_steel_conservative'],ds);minimum['wisp_wall_conservative']=min(minimum['wisp_wall_conservative'],dw)
   if ds<0 or dw<0:failures.append({'frame':f,'object':o.name,'ring':j,'steel_margin':ds,'wall_margin':dw})
 samplecount+=1
 if len(failures)>80:break
result={'samples':samplecount,'range':[times[0],times[-1]],'min_clearance_m':minimum,'failures':failures[:100],'failure_count':len(failures),'max_sample_displacement_m':maxstep,'connected_rotation_preserved':True,'seconds':time.perf_counter()-t0,'method':'Every integer and half-frame; actual rock vertices and conservative wisp ring spheres against full fixed-source BVH transformed by rigid rotation. Not CFD or continuous-time proof.'}
(B/'Records'/('supply-geometry-verification.json' if globals().get('ONLY_ADDED',False) else 'geometry-verification.json')).write_text(json.dumps(result,indent=2));s.frame_set(198)
