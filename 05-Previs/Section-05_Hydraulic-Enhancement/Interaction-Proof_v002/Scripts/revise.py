"""Bounded v002: moving world-space packets, geometric advection, common rotation.
Kinematic illustration, not a momentum/pressure or CFD solver.
"""
import bpy,math,json,random,hashlib,time
from pathlib import Path
from mathutils import Vector,Matrix,Quaternion
from mathutils.bvhtree import BVHTree
B=Path(__file__).resolve().parents[1];ROOT=B.parents[2];OLD=B.parent/'Interaction-Proof_v001'
OUT=B/'Scenes/S05_twisted-pad_interaction_v002.blend'
assert not OUT.exists(),'Preserve existing candidate'
assert Path(bpy.data.filepath).resolve()==(OLD/'Scenes/S05_twisted-pad_interaction_v001.blend').resolve()
assert not bpy.data.is_dirty,'Preserve unsaved work'
s=bpy.context.scene;s.frame_set(1);bpy.context.view_layer.update()
sourcehash=hashlib.sha256((OLD/'Scenes/S05_twisted-pad_interaction_v001.blend').read_bytes()).hexdigest()
hardware=list(bpy.data.collections['S05_LINKED_HARDWARE'].objects)
vv=[];ff=[];original={o.name:o.matrix_world.copy() for o in hardware}
for o in hardware:
 off=len(vv);vv.extend(o.matrix_world@v.co for v in o.data.vertices);ff.extend([[off+i for i in p.vertices] for p in o.data.polygons])
tree=BVHTree.FromPolygons(vv,ff)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
s.name='S05_Hydraulic_Interaction_v002'
root=bpy.data.objects.new('S05_COMMON_AXIAL_ROTATION',None);s.collection.objects.link(root)
OMEGA=-math.radians(5);R=.155575
for o in hardware:o.parent=root;o.matrix_parent_inverse=Matrix.Identity(4);o.matrix_basis=original[o.name]
root.rotation_mode='XYZ'
for f in [1,145]:root.rotation_euler=(0,0,OMEGA*(f-1)/24);root.keyframe_insert('rotation_euler',frame=f)
root['rotation_meaning']='Clockwise viewed from +Z surface toward -Z downhole; authored 5 degrees/second; not measured RPM'
root['no_translation']=True
for layer in root.animation_data.action.layers:
 for strip in layer.strips:
  for bag in strip.channelbags:
   for fc in bag.fcurves:
    for k in fc.keyframe_points:k.interpolation='LINEAR'
# Retain predecessor effects in the derivative, hidden and clearly labeled.
oldfx=bpy.data.collections['S05_ILLUSTRATIVE_FLOW'];oldfx.hide_render=True;oldfx.hide_viewport=True;oldfx.name='S05_v001_FLOW_RETAINED_HIDDEN'
fx=bpy.data.collections.new('S05_DYNAMIC_FLOW_v002');s.collection.children.link(fx)
def material(name,color,emission=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=.82;p.inputs['Emission Color'].default_value=(*color,1);p.inputs['Emission Strength'].default_value=emission;return m
amber=material('S05_v002_AmberFluid',(.75,.33,.045),.65)
stone=material('S05_v002_MatteRock',(.22,.135,.065))
stone2=material('S05_v002_RockFacet',(.35,.26,.15))
# Existing native captions updated with the newly authorized operating scenario.
bpy.data.objects['S05_Mode'].data.body='Circulation + rotation  /  Slowed illustration'
s['proof_scope']='6 seconds, combined circulation and axial rotation; geometry-aware kinematic illustration, not CFD'
s['palette_status']='Amber approved by owner for v002'
def rot(v,a):
 c=math.cos(a);sn=math.sin(a);return Vector((c*v.x-sn*v.y,sn*v.x+c*v.y,v.z))
def nearest(p,t):
 co,n,idx,d=tree.find_nearest(rot(p,-OMEGA*t));return rot(co,OMEGA*t),rot(n,OMEGA*t),d
def smooth(x):x=max(0,min(1,x));return x*x*(3-2*x)
knots=[(.7,62),(.92,62),(1.04,60),(1.12,69),(1.23,85),(1.32,85),(1.44,74),(1.72,74)]
def base(z):
 x=1.5-z
 for (a,av),(b,bv) in zip(knots,knots[1:]):
  if a<=x<=b:return math.radians(90-av-(bv-av)*smooth((x-a)/(b-a)))
 return math.radians(16 if x>1.72 else 28)
def influence(z):return smooth((z+.18)/.22)*(1-.45*smooth((z-.56)/.24))
def angular_delta(a,b):return (a-b+math.pi)%math.tau-math.pi
def velocity(p,t,lane,rad):
 r=math.hypot(p.x,p.y);a=math.atan2(p.y,p.x);w=influence(p.z)
 target=base(p.z)+lane+OMEGA*t*w
 vz=.19
 deriv=(base(p.z+.001)-base(p.z-.001))/.002
 va=deriv*vz+3.0*angular_delta(target,a)+OMEGA*.3*w
 vr=(.137-r)*4.0
 u=Vector((p.x/r,p.y/r,0));tan=Vector((-u.y,u.x,0))
 v=Vector((0,0,vz))+tan*(r*va)+u*vr
 co,n,d=nearest(p,t);wallv=Vector((-OMEGA*p.y,OMEGA*p.x,0))
 # Moving boundary: remove inward relative normal velocity near actual CAD.
 rel=(v-wallv).dot(n);blend=1-smooth((d-rad-.001)/.009)
 if rel<0:v-=n*(rel*blend)
 if d<rad+.006:v+=n*max(0,(rad+.006-d)*8)
 if r>R-rad-.004:v-=u*max(0,(r-(R-rad-.004))*8)
 return v
corrections=[]
def constrain(p,t,rad):
 start=p.copy()
 for _ in range(16):
  co,n,d=nearest(p,t);signed=(p-co).dot(n)
  if signed<rad+.001:p+=n*(rad+.001-signed)
  r=math.hypot(p.x,p.y)
  if r>R-rad-.001:p.x*= (R-rad-.001)/r;p.y*= (R-rad-.001)/r
  co,n,d=nearest(p,t)
  if (p-co).dot(n)>=rad+.0008:break
 assert (p-co).dot(n)>rad+.0003,(list(p),t,rad,d)
 corrections.append((p-start).length)
 return p
random.seed(123)
particles=[]
for sector in range(3):
 for offset in [-6,0,6]:
  lane=math.radians(sector*120+offset)
  for j in range(3):particles.append({'kind':'fluid','lane':lane,'phase':j/3,'r':.00145,'offset':random.uniform(-.025,.025)})
  if offset==0 or sector==0:
   for j in range(2 if sector==0 else 1):particles.append({'kind':'rock','lane':lane,'phase':(j+.24)/2,'r':.0047 if sector==0 else .0035,'offset':random.uniform(-.025,.025)})
DT=1/120;total=144*5;warm=720
for p in particles:
 z=-.28+p['phase']*1.2;a=base(z)+p['lane']+OMEGA*(-6)*influence(z)
 p['pos']=constrain(Vector((.137*math.cos(a),.137*math.sin(a),z)),-6,p['r']);p['frames']=[]
stats={'min_particle_hardware':1.,'min_particle_wall':1.,'min_axial_step':1.,'reset_count':0}
for step in range(-warm,total):
 t=step*DT
 for p in particles:
  v=velocity(p['pos'],t,p['lane'],p['r']);old=p['pos'].copy()
  p['pos']=constrain(old+v*DT,t+DT,p['r'])
  if p['pos'].z>.94:
   a=math.radians(16)+p['lane'];p['pos']=Vector((.137*math.cos(a),.137*math.sin(a),-.28));stats['reset_count']+=1
  elif step>=0:stats['min_axial_step']=min(stats['min_axial_step'],p['pos'].z-old.z)
  if step>=0:
   co,n,d=nearest(p['pos'],t+DT);stats['min_particle_hardware']=min(stats['min_particle_hardware'],d-p['r']);stats['min_particle_wall']=min(stats['min_particle_wall'],R-math.hypot(p['pos'].x,p['pos'].y)-p['r'])
  if (step+1)>=0 and (step+1)%5==0 and (step+1)<720:
   p['frames'].append(list(p['pos']))
assert all(len(p['frames'])==144 for p in particles)
min_stroke=1.;stroke_center_records=[]
for i,p in enumerate(particles):
 if p['kind']=='rock':
  bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=1);o=bpy.context.object;o.name=f'S05_v002_Rock_{i:02}'
  for c in list(o.users_collection):c.objects.unlink(o)
  fx.objects.link(o)
  for v in o.data.vertices:
   v.co.x*=random.uniform(.7,1.1);v.co.y*=random.uniform(.6,.9);v.co.z*=random.uniform(.7,1.2)
  scale=p['r']/max(v.co.length for v in o.data.vertices)
  for v in o.data.vertices:v.co*=scale
  o.data.materials.append(stone);o.data.materials.append(stone2)
  for face in o.data.polygons:face.material_index=random.randrange(2)
  for f,pos in enumerate(p['frames'],1):
   t=(f-1)/24;o.location=pos;o.rotation_euler=(.16*t+.5*i,.21*t,.25*t+.2*i);edge=min(1,smooth((pos[2]+.28)/.07),smooth((.94-pos[2])/.07));o.scale=(edge,)*3;o.keyframe_insert('location',frame=f);o.keyframe_insert('rotation_euler',frame=f);o.keyframe_insert('scale',frame=f)
  o['motion']='World-space advection shared with fluid; slow illustrative tumbling; no parent to hardware'
 else:
  # Short local flow-direction packet. Rebuilt against CURRENT moving geometry.
  # This is neither a full fixed guide nor a historical trail inside moving metal.
  allverts=[];centres=[];NR=15;SIDES=6
  for f,pos in enumerate(p['frames'],1):
   t=(f-1)/24;center=Vector(pos);v=velocity(center,t,p['lane'],p['r']).normalized();pts=[]
   for j in range(NR):
    d=(j/(NR-1)-.5)*.055;pt=center.copy();ds=d/6
    for _ in range(6):
     tangent=velocity(pt,t,p['lane'],p['r']).normalized();pt=constrain(pt+tangent*ds,t,p['r'])
    pts.append(pt)
   arr=[]
   for j,pt in enumerate(pts):
    tangent=(pts[min(NR-1,j+1)]-pts[max(0,j-1)]).normalized();u=tangent.cross(Vector((0,0,1)))
    if u.length<.01:u=tangent.cross(Vector((1,0,0)))
    u.normalize();v=tangent.cross(u).normalized();radius=p['r']*(.16+.84*math.sin(math.pi*j/(NR-1))**.7)
    edge=min(1,smooth((pt.z+.28)/.06),smooth((.94-pt.z)/.06));radius*=edge
    co,n,dist=nearest(pt,t);min_stroke=min(min_stroke,dist-radius)
    for k in range(SIDES):arr.append(pt+radius*(u*math.cos(k*math.tau/SIDES)+v*math.sin(k*math.tau/SIDES)))
   allverts.append(arr);centres.append([list(q) for q in pts])
  faces=[]
  for j in range(NR-1):
   for k in range(SIDES):faces.append((j*SIDES+k,j*SIDES+(k+1)%SIDES,(j+1)*SIDES+(k+1)%SIDES,(j+1)*SIDES+k))
  me=bpy.data.meshes.new(f'S05_PacketMesh_{i:02}');me.from_pydata(allverts[0],[],faces);me.materials.append(amber);o=bpy.data.objects.new(f'S05_v002_FluidPacket_{i:02}',me);fx.objects.link(o)
  for face in me.polygons:face.use_smooth=True
  basis=o.shape_key_add(name='Basis');o.data.shape_keys.use_relative=False
  for f,arr in enumerate(allverts[1:],2):
   key=o.shape_key_add(name=f'Frame_{f:03}')
   for v,co in zip(key.data,arr):v.co=co
  keys=o.data.shape_keys
  for f in [1,144]:keys.eval_time=(f-1)*10;keys.keyframe_insert('eval_time',frame=f)
  o['motion']='World-space advected short flow packet; current-time geometry constraint; not attached to hardware'
  stroke_center_records.append(centres)
def linear(idblock):
 if idblock.animation_data and idblock.animation_data.action:
  for layer in idblock.animation_data.action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for fc in bag.fcurves:
      for k in fc.keyframe_points:k.interpolation='LINEAR'
for o in fx.objects:
 linear(o)
 if o.type=='MESH' and o.data.shape_keys:linear(o.data.shape_keys)
s.frame_set(72);s.render.filepath='//../Work/Frames/S05_';bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
stats.update({'max_projection_correction_m':max(corrections),'stroke_center_minus_radius_min_m':min_stroke,'hardware_max_radius_m':max(math.hypot(v.x,v.y) for v in vv),'hardware_radial_wall_gap_m':R-max(math.hypot(v.x,v.y) for v in vv),'root_angular_rate_degrees_per_second':-5,'duration_seconds':6,'frames':144,'source_v001_sha256':sourcehash,'camera_preserved':True,'hardware_count':len(hardware),'fluid_packets':sum(p['kind']=='fluid' for p in particles),'rock_fragments':sum(p['kind']=='rock' for p in particles),'method':'Authored axial/channel steering + partial tangential entrainment; moving-wall relative-normal avoidance; geometric position constraints at120Hz; NOT CFD or predictive cuttings transport','warmup_seconds':6,'palette':'Owner-approved amber'})
(B/'Records/build.json').write_text(json.dumps(stats,indent=2));(B/'Records/particle-tracks.json').write_text(json.dumps(particles,default=lambda o:list(o)));(B/'Records/stroke-centres.json').write_text(json.dumps(stroke_center_records))
result=stats
