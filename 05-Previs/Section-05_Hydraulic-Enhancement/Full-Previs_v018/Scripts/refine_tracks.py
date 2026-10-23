"""Preserve v017 evaluated motion; plan smooth safe extensions around rotation."""
import bpy,math,json,time
from pathlib import Path
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
import numpy as np
B=Path(__file__).resolve().parents[1];s=bpy.context.scene
oldgroup=bpy.data.collections['S05_TRACKED_COHORT_v013'];oldgroup.hide_viewport=False
sources=sorted(oldgroup.objects,key=lambda o:o.name);core=[]
for f in range(1,97):
 s.frame_set(f);bpy.context.view_layer.update();core.append([(o.location.copy(),o.rotation_euler.copy()) for o in sources])
assert core[-1][0][0].z-core[0][0][0].z>.5
oldgroup.hide_viewport=True
s.frame_set(151);bpy.context.view_layer.update();vv=[];ff=[]
for o in bpy.data.collections['S05_LINKED_HARDWARE'].objects:
 off=len(vv);vv.extend(o.matrix_world@v.co for v in o.data.vertices);ff.extend([[off+i for i in p.vertices] for p in o.data.polygons])
steel=BVHTree.FromPolygons(vv,ff);R=.155575;OM=-math.radians(5)
routes=json.loads((B.parent/'Interaction-Proof_v004/Records/planned-routes.json').read_text())
def smooth(x):
 x=max(0,min(1,x));return x*x*(3-2*x)
def influence(z):return .32+.43*smooth((z+.15)/.23)*(1-smooth((z-.65)/.25))
def route(z):return float(np.interp(z,np.arange(131)*.01-.3,routes[2]))
def surface(z,a):
 u=Vector((math.cos(a),math.sin(a),0));hit=steel.ray_cast(Vector((0,0,z))+u*.18,-u,.18)[0]
 return math.hypot(hit.x,hit.y) if hit else .105
def linear(o):
 for layer in o.animation_data.action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for fc in bag.fcurves:
     for k in fc.keyframe_points:k.interpolation='LINEAR'
offsets=np.radians(np.arange(-60,61,2));K=len(offsets);record=[]
for o in sorted(bpy.data.collections['S05_v018_ContinuousHydraulics'].objects,key=lambda o:o.name):
 if 'Cutting' not in o.name:continue
 group,i=map(int,o.name.rsplit('_',2)[-2:]);shift=[0,-.7,.7][group];radius=max(v.co.length for v in o.data.vertices)+.0003
 points=np.zeros((432,K,3));angles=np.zeros((432,K));cost=np.full((432,K),1e12);orientations=[]
 for f in range(1,433):
  t=(f-151)/24;z=-.005+.135*t+[.022,0,-.022][i]+shift
  fixed=group==0 and 151<=f<=246
  if fixed:
   p,orientation=core[f-151][i];desired=math.atan2(p.y,p.x)
  else:desired=route(z)+OM*t*influence(z);orientation=(i*.7+.16*t,.4+i+.12*t,.3-.15*t)
  orientations.append(orientation)
  for k,delta in enumerate(offsets):
   a=desired+delta;angles[f-1,k]=a
   if fixed:
    if k==30:points[f-1,k]=p;cost[f-1,k]=0
    continue
   local=a-OM*t
   rs=max(surface(z+dz,local+da) for dz in [-radius,0,radius] for da in [-radius/.12,0,radius/.12])
   lo=rs+radius+.0015;hi=R-radius-.0017
   if lo>hi:continue
   rr=(lo+hi)/2;q=Vector((rr*math.cos(local),rr*math.sin(local),z))
   if steel.find_nearest(q)[3]<radius+.001:continue
   points[f-1,k]=(rr*math.cos(a),rr*math.sin(a),z);cost[f-1,k]=float(delta*delta)*2
 score=cost[0].copy();backs=[]
 for f in range(1,432):
  da=angles[f,:,None]-angles[f-1,None,:]
  transition=score[None,:]+18*da*da
  if not (group==0 and 151<=f<=245):transition[np.abs(da)>math.radians(5)]=1e12
  parent=transition.argmin(axis=1);backs.append(parent);score=cost[f]+transition[np.arange(K),parent]
  assert score.min()<1e10,('No continuous path',o.name,f+1)
 k=int(score.argmin());indices=[k]
 for f in range(430,-1,-1):k=int(backs[f][k]);indices.append(k)
 indices.reverse();o.animation_data_clear();positions=[]
 for f,k in enumerate(indices,1):
  o.location=points[f-1,k];o.rotation_euler=orientations[f-1]
  for prop in ['location','rotation_euler']:o.keyframe_insert(prop,frame=f)
  positions.append(list(o.location))
 linear(o);record.append({'name':o.name,'heads':positions,'max_frame_step_m':max(math.dist(a,b) for a,b in zip(positions,positions[1:]))})
(B/'Records/cutting-tracks-refined.json').write_text(json.dumps(record));s.frame_set(198);bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
result={'tracks':[{k:v for k,v in r.items() if k!='heads'} for r in record],'approved_core_restored':True,'extension_method':'Globally connected angle candidates checked against actual turning solid; maximum5deg per frame for added motion; original core preserved; no rigid parenting.'}
(B/'Records/track-refinement.json').write_text(json.dumps(result,indent=2))
