"""Geometry-distributed annular flow proof; illustrative kinematics, not CFD."""
import bpy,math,json,hashlib,numpy as np
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
B=Path(__file__).resolve().parents[1];OLD=B.parent/'Interaction-Proof_v003';V2=B.parent/'Interaction-Proof_v002'
OUT=B/'Scenes/S05_twisted-pad_interaction_v004.blend';s=bpy.context.scene
assert not OUT.exists()
assert Path(bpy.data.filepath).resolve()==(OLD/'Scenes/S05_twisted-pad_interaction_v003.blend').resolve()
# Only frame changes made during read-only inspection are permitted here.
s.frame_set(1);bpy.context.view_layer.update();vv=[];ff=[]
for o in bpy.data.collections['S05_LINKED_HARDWARE'].objects:
 off=len(vv);vv.extend(o.matrix_world@v.co for v in o.data.vertices);ff.extend([[off+i for i in p.vertices] for p in o.data.polygons])
tree=BVHTree.FromPolygons(vv,ff);OMEGA=-math.radians(5);R=.155575
def rot(v,a):
 c=math.cos(a);sn=math.sin(a);return Vector((c*v.x-sn*v.y,sn*v.x+c*v.y,v.z))
def smooth(x):
 x=max(0,min(1,x));return x*x*(3-2*x)
def influence(z):return .32+.43*smooth((z+.15)/.23)*(1-smooth((z-.65)/.25))
def surface(z,a):
 u=Vector((math.cos(a),math.sin(a),0));h=tree.ray_cast(Vector((0,0,z))+u*.18,-u,.18)[0]
 return math.hypot(h.x,h.y) if h else .105
def clearance(pt,t):
 q=rot(pt,-OMEGA*t);r=math.hypot(q.x,q.y);a=math.atan2(q.y,q.x)
 return min(tree.find_nearest(q)[3],r-surface(q.z,a),R-r)
data=json.loads((B/'Records/surface-map.json').read_text());surf=np.array(data['surface_radii_m']);NZ,NA=surf.shape
# Plan representative routes through the measured open envelope. Conservative
# angular dilation covers slip between the field and turning pads.
robust=surf.copy()
for dz in [-1,0,1]:
 shifted=surf[np.clip(np.arange(NZ)+dz,0,NZ-1)]
 for da in range(-6,7):robust=np.maximum(robust,np.roll(shifted,da,axis=1))
gap=R-robust;angles=np.arange(NA)*2.;routes=[]
for seed in range(0,360,20):
 diff=(angles-seed+180)%360-180
 cost=.0007*diff[None,:]**2+.06*(.04/np.maximum(gap,.001))**2
 cost=np.broadcast_to(cost,gap.shape).copy();cost[gap<.014]=1e6
 score=cost[0]+.025*diff**2;back=np.zeros((NZ,NA),dtype=np.int16)
 for z in range(1,NZ):
  choices=np.array([np.roll(score,k)+.035*k*k for k in range(-3,4)])
  best=choices.argmin(axis=0);back[z]=(np.arange(NA)-(best-3))%NA;score=choices.min(axis=0)+cost[z]
 idx=int(score.argmin());path=[idx]
 for z in range(NZ-1,0,-1):idx=int(back[z,idx]);path.append(idx)
 path=np.unwrap(np.radians(np.array(path[::-1])*2))
 for _ in range(2):path=np.convolve(np.pad(path,(2,2),mode='edge'),np.array([1,2,3,2,1])/9,mode='valid')
 routes.append(path)
def route_at(lane,z):return float(np.interp(z,np.arange(NZ)*.01-.3,routes[lane]))
DT=1/120;START=-840;END=715;particles=[]
# Eighteen circumferential routes, independently staggered timing and depth.
for lane in range(18):
 for j in range(3):
  particles.append({'kind':'fluid','lane':lane,'phase':(j/3+lane*.071)%1,'r':.00085,'fraction':[.32,.58,.80][(lane+j)%3],'speed':.19+.012*math.sin(lane*2.4+j),'age':.70+.12*((lane+j)%3)})
rock_sources=[o for o in bpy.data.collections['S05_HISTORY_FLOW_v003'].objects if '_Rock_' in o.name]
for i,lane in enumerate([0,2,3,4,6,9,12,15]):
 particles.append({'kind':'rock','lane':lane,'phase':(.17+i*.137)%1,'r':.0047 if i<4 else .0035,'fraction':.55,'speed':.19,'age':.48,'rock_source':rock_sources[i].name})
min_head=1;corrections=0
for i,p in enumerate(particles):
 p['history']=[];p['generation']=[];p['radii']=[]
 for step in range(START,END+1):
  t=step*DT;travel=p['phase']*1.28+p['speed']*(t-START*DT);gen=int(travel/1.28);z=-.30+travel%1.28
  a=route_at(p['lane'],z)+OMEGA*t*influence(z)
  local=a-OMEGA*t;pad=p['r']+.0012
  # Sample the finite particle footprint, using actual geometry at this time.
  rs=max(surface(z+dz,local+da) for dz in [-pad,0,pad] for da in [-pad/.13,0,pad/.13])
  low=rs+pad;high=R-pad
  if low>high:
   # Choose the nearest usable side of a constriction, preserving source steel.
   candidates=[]
   for off in [-.07,.07,-.14,.14,-.21,.21,-.28,.28]:
    aa=local+off;rr=max(surface(z+dz,aa+da) for dz in [-pad,0,pad] for da in [-pad/.13,0,pad/.13])
    if rr+pad<high:candidates.append((abs(off),aa,rr+pad))
   assert candidates,(i,step,z,a)
   _,local,low=min(candidates);a=local+OMEGA*t;corrections+=1
  r=low+(high-low)*p['fraction'];pt=Vector((r*math.cos(a),r*math.sin(a),z))
  # Verify centre against actual moving mesh and conservatively lift if needed.
  for _ in range(8):
   d=clearance(pt,t)
   if d>=p['r']+.0007:break
   r+=.0007;assert r<R-p['r']-.0005
   pt=Vector((r*math.cos(a),r*math.sin(a),z))
  assert clearance(pt,t)>p['r']+.0004
  p['history'].append(pt);p['generation'].append(gen);p['radii'].append(r)
  if step>=0:min_head=min(min_head,clearance(pt,t)-p['r'])
bpy.ops.wm.save_as_mainfile(filepath=str(OUT));s.name='S05_Hydraulic_Interaction_v004'
bpy.data.collections['S05_HISTORY_FLOW_v003'].hide_render=True;bpy.data.collections['S05_HISTORY_FLOW_v003'].hide_viewport=True
fx=bpy.data.collections.new('S05_VOLUME_FLOW_v004');s.collection.children.link(fx)
mat=bpy.data.materials['S05_v002_AmberFluid'];NR=41;SIDES=6
def linear(idblock):
 if idblock.animation_data and idblock.animation_data.action:
  for layer in idblock.animation_data.action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for fc in bag.fcurves:
      for k in fc.keyframe_points:k.interpolation='LINEAR'
def point_at(p,index):
 a=max(0,min(len(p['history'])-2,int(index)));return p['history'][a].lerp(p['history'][a+1],max(0,min(1,index-a)))
summary=[];track_record=[]
for i,p in enumerate(particles):
 radius=.00085 if p['kind']=='fluid' else .0005;age=p['age'];maxsteps=age/DT;safe=[]
 for f in range(1,145):
  idx=(f-1)*5-START;t=(f-1)/24;limit=maxsteps
  for k in range(1,int(maxsteps)+1):
   q=p['history'][idx-k]
   if p['generation'][idx-k]!=p['generation'][idx] or clearance(q,t)<radius+.001:
    limit=max(0,k-2);break
  safe.append(limit)
 smoothsafe=[min(safe[g]+abs(f-g)*4 for g in range(max(0,f-9),min(144,f+10))) for f in range(144)]
 states=[];heads=[]
 for f in range(1,145):
  idx=(f-1)*5-START;length=smoothsafe[f-1];points=[point_at(p,idx-length*j/(NR-1)) for j in range(NR)];heads.append(list(points[0]));arr=[]
  for j,pt in enumerate(points):
   tangent=points[min(NR-1,j+1)]-points[max(0,j-1)]
   if tangent.length<1e-7:tangent=Vector((0,0,-1))
   tangent.normalize();u=tangent.cross(Vector((0,0,1)))
   if u.length<.01:u=tangent.cross(Vector((1,0,0)))
   u.normalize();v=tangent.cross(u).normalized();edge=min(smooth((pt.z+.30)/.10),smooth((.98-pt.z)/.10),smooth(length/10))
   rr=radius*(.015+.985*(1-j/(NR-1))**.9)*edge
   for k in range(SIDES):arr.append(pt+rr*(u*math.cos(k*math.tau/SIDES)+v*math.sin(k*math.tau/SIDES)))
  states.append(arr)
 faces=[(j*SIDES+k,j*SIDES+(k+1)%SIDES,(j+1)*SIDES+(k+1)%SIDES,(j+1)*SIDES+k) for j in range(NR-1) for k in range(SIDES)]
 me=bpy.data.meshes.new(f'S05_v004_TrailMesh_{i:02}');me.from_pydata(states[0],[],faces);me.materials.append(mat)
 o=bpy.data.objects.new(f'S05_v004_{p["kind"]}_HistoryTail_{i:02}',me);fx.objects.link(o)
 for poly in me.polygons:poly.use_smooth=True
 o.shape_key_add(name='Basis');me.shape_keys.use_relative=False
 for f,verts in enumerate(states[1:],2):
  key=o.shape_key_add(name=f'Frame_{f:03}')
  for v,co in zip(key.data,verts):v.co=co
 for key in me.shape_keys.key_blocks:key.interpolation='KEY_LINEAR'
 for f in [1,144]:me.shape_keys.eval_time=(f-1)*10;me.shape_keys.keyframe_insert('eval_time',frame=f)
 linear(me.shape_keys)
 if p['kind']=='rock':
  old=bpy.data.objects[p['rock_source']];rock=old.copy();rock.data=old.data.copy();rock.animation_data_clear();rock.name=f'S05_v004_Rock_{i:02}';fx.objects.link(rock)
  scale=p['r']/max(v.co.length for v in rock.data.vertices)
  for v in rock.data.vertices:v.co*=scale
  for f,pos in enumerate(heads,1):
   t=(f-1)/24;rock.location=pos;rock.rotation_euler=(.16*t+.5*i,.21*t,.25*t+.2*i);edge=min(smooth((pos[2]+.30)/.10),smooth((.98-pos[2])/.10));rock.scale=(edge,)*3
   for prop in ['location','rotation_euler','scale']:rock.keyframe_insert(prop,frame=f)
  linear(rock)
 summary.append({'index':i,'kind':p['kind'],'route':p['lane'],'depth_fraction':p['fraction'],'max_history_seconds':age,'mean_visible_history_seconds':sum(smoothsafe)/144*DT})
 track_record.append({'index':i,'kind':p['kind'],'route':p['lane'],'heads':heads,'visible_history_steps':smoothsafe})
s.frame_set(72);s.render.filepath='//../Work/Frames/S05_';s['proof_scope']='v004 six-second distributed annular flow; geometry-derived routes, partial spin influence and multiple passage depths; illustrative not CFD'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
result={'elements':summary,'route_count':18,'fluid_markers':54,'cuttings':8,'map_samples':int(NZ*NA),'head_support_min_clearance_m':min_head,'constriction_side_corrections':corrections,'partial_rotation_fraction_range':[.32,.75],'prior_v003_sha256':hashlib.sha256((OLD/'Scenes/S05_twisted-pad_interaction_v003.blend').read_bytes()).hexdigest(),'method':'Minimum-cost paths across actual circumferential clearance map; depth fractions inside current actual annulus; independent upward progression with partial spatially varying spin; timestamped history tails. Kinematic illustration, not CFD.'}
(B/'Records/build.json').write_text(json.dumps(result,indent=2));(B/'Records/tracks.json').write_text(json.dumps(track_record));(B/'Records/planned-routes.json').write_text(json.dumps([r.tolist() for r in routes]))
