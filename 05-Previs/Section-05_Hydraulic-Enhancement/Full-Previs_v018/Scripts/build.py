"""Extend approved v017 into owner-released 18s previs. Illustrative, not CFD."""
import bpy, math, json, time, hashlib, shutil
from pathlib import Path
from mathutils import Vector, Quaternion, Matrix
from mathutils.bvhtree import BVHTree
import numpy as np

B=Path(__file__).resolve().parents[1];ROOT=B.parents[2];s=bpy.context.scene
assert Path(bpy.data.filepath).parent.parent==B
R=.155575;OMEGA=-math.radians(5);OFFSET=150;NFR=432
def curves(id):
 if id.animation_data and id.animation_data.action:
  for layer in id.animation_data.action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:yield from bag.fcurves
def linear(id):
 for fc in curves(id):
  for k in fc.keyframe_points:k.interpolation='LINEAR'
def smooth(x):
 x=max(0.,min(1.,x));return x*x*(3-2*x)
def rot(p,a):
 c=math.cos(a);sn=math.sin(a);return Vector((c*p.x-sn*p.y,sn*p.x+c*p.y,p.z))
def influence(z):return .32+.43*smooth((z+.15)/.23)*(1-smooth((z-.65)/.25))
def time_at(f):return (f-1-OFFSET)/24

# Inspect source at its original zero-spin pose before extending timeline.
s.frame_set(1);bpy.context.view_layer.update()
hardware=list(bpy.data.collections['S05_LINKED_HARDWARE'].objects)
vv=[];ff=[]
for o in hardware:
 off=len(vv);vv.extend(o.matrix_world@v.co for v in o.data.vertices);ff.extend([[off+i for i in p.vertices] for p in o.data.polygons])
steel=BVHTree.FromPolygons(vv,ff)
def surface(z,a):
 u=Vector((math.cos(a),math.sin(a),0));h=steel.ray_cast(Vector((0,0,z))+u*.18,-u,.18)[0]
 return math.hypot(h.x,h.y) if h else .105
routes=json.loads((B.parent/'Interaction-Proof_v004/Records/planned-routes.json').read_text())
def route(lane,z):
 x=max(0,min(129.999,(z+.3)*100));i=int(x)
 return routes[lane][i]*(1-x+i)+routes[lane][i+1]*(x-i)

# Same material and density animation; extend at original rates with a time offset.
fluid=bpy.data.objects['S05_v007_AnnularFluidDomain']
fluidmat=fluid.data.materials[0].copy();fluidmat.name='S05_v018_ApprovedAmberFluid';fluid.data.materials[0]=fluidmat
for fc in curves(fluidmat.node_tree):
 for k in fc.keyframe_points:
  k.co.x+=OFFSET;k.handle_left.x+=OFFSET;k.handle_right.x+=OFFSET
 fc.extrapolation='LINEAR'
root=bpy.data.objects['S05_COMMON_AXIAL_ROTATION'];root.animation_data_clear()
for f in [1,NFR]:
 root.rotation_euler.z=OMEGA*time_at(f);root.keyframe_insert('rotation_euler',frame=f)
linear(root)

# Reuse enlarged rock shapes and alter only their permitted mineral materials.
rock_sources=sorted(bpy.data.collections['S05_TRACKED_COHORT_v013'].objects,key=lambda o:o.name)
rockmaterials=[]
for key,col in [('Body',(.32,.235,.145,1)),('Light',(.55,.43,.29,1)),('Dark',(.14,.105,.07,1))]:
 m=bpy.data.materials['S05_v017_Cutting'+key].copy();m.name='S05_v018_Mineral'+key
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=col;p.inputs['Roughness'].default_value=.96;p.inputs['Metallic'].default_value=0;p.inputs['Emission Strength'].default_value=0
 rockmaterials.append(m)
for name in ['S05_INTERNAL_WISPS_v012','S05_TRACKED_COHORT_v013']:
 bpy.data.collections[name].hide_render=True;bpy.data.collections[name].hide_viewport=True
fx=bpy.data.collections.new('S05_v018_ContinuousHydraulics');s.collection.children.link(fx)

# A bounded extension of the v004/v012 geometry-aware route field.
# Query the actual solid with a finite footprint; select a nearby open passage
# only when rotation closes the originally chosen route. No steel scaling.
def position(lane,z,t,side=0,depth=0,radius=.0035,previous_angle=None):
 target=route(lane,z)+OMEGA*t*influence(z)
 local=target-OMEGA*t
 dzs=(-radius,0,radius);das=(-radius/.12,0,radius/.12)
 def candidate(a):
  rs=max(surface(z+dz,a+da) for dz in dzs for da in das)
  lo=rs+radius+.0015;hi=R-radius-.0017
  if lo>hi:return None
  rr=min(hi,max(lo,(lo+hi)/2+depth))
  world=a+OMEGA*t;p=Vector((rr*math.cos(world),rr*math.sin(world),z))
  p+=Vector((-math.sin(world),math.cos(world),0))*side
  q=rot(p,-OMEGA*t)
  if R-math.hypot(p.x,p.y)<radius+.001 or steel.find_nearest(q)[3]<radius+.001:return None
  return p,world
 best=candidate(local)
 if best is None:
  options=[]
  for delta in range(1,61):
   for sign in [-1,1]:
    a=local+sign*math.radians(delta);hit=candidate(a)
    if hit:
     score=abs(a-local)+(abs(hit[1]-previous_angle)*.7 if previous_angle is not None else 0)
     options.append((score,hit))
   if options and delta>5:break
  assert options,('No passage',lane,z,t,radius)
  best=min(options,key=lambda x:x[0])[1]
 p,a=best;return p,Vector((math.cos(a),math.sin(a),0)),Vector((-math.sin(a),math.cos(a),0)),a

# Keep the exact original three-rock core from v017 during the signature beat.
core_states=[]
for f in range(1,97):
 s.frame_set(f);bpy.context.view_layer.update()
 core_states.append([(o.location.copy(),o.rotation_euler.copy()) for o in rock_sources])
rocks=[];trackrows=[]
for group,offset in enumerate([0,-.70,.70]):
 for i,old in enumerate(rock_sources):
  o=old.copy();o.data=old.data.copy();o.animation_data_clear();o.name=f'S05_v018_Cutting_{group}_{i}';fx.objects.link(o);o.parent=None;o.data.materials.clear()
  for m in rockmaterials:o.data.materials.append(m)
  support=max(v.co.length for v in o.data.vertices);previous=None;heads=[]
  for f in range(1,NFR+1):
   t=time_at(f);dz=[.022,0,-.022][i];z=-.005+.135*t+dz+offset
   if group==0 and 1<=f-OFFSET<=96:
    p,orientation=core_states[f-OFFSET-1][i]
   else:
    p,u,v,previous=position(2,z,t,side=[-.004,.005,-.001][i],depth=0,radius=support+.0003,previous_angle=previous)
    orientation=(i*.7+.16*t,.4+i+.12*t,.3-.15*t)
   o.location=p;o.rotation_euler=orientation;o.scale=(1,1,1)
   for prop in ['location','rotation_euler']:o.keyframe_insert(prop,frame=f)
   heads.append(list(p))
  linear(o);rocks.append(o);trackrows.append({'name':o.name,'support_radius':support,'heads':heads,'persistent':True,'group_axial_offset':offset})
(B/'Records/cutting-tracks.json').write_text(json.dumps(trackrows))

# Build v012-style finite tapered wisps, extending longitudinal distribution.
# Key every two frames for compact editable source; verify intervening frames.
NR=25;SIDES=10;sampleframes=list(range(1,NFR+1,2))+[NFR]
wmat=bpy.data.materials['S05_v017_RichAmberWisp'];wisps=[]
configs=[]
for routeid in [2,0,4,16]:
 for j,zstart in enumerate(np.arange(-1.15,1.51,.27)):
  configs.append((routeid,j,float(zstart),0,.0015,.055*1.875))
for j,zstart in enumerate([-.19,-.025,.16]):
 for k,(side,depth,length) in enumerate([(-.004,.0005,.052),(.004,.0045,.046)]):configs.append((2,20+j*2+k,zstart,side,depth,length*1.875))
faces=[(j*SIDES+k,j*SIDES+(k+1)%SIDES,(j+1)*SIDES+(k+1)%SIDES,(j+1)*SIDES+k) for j in range(NR-1) for k in range(SIDES)]
faces.extend([tuple(reversed(range(SIDES))),tuple((NR-1)*SIDES+k for k in range(SIDES))])
for routeid,j,zstart,side,depth,length in configs:
 states=[]
 for f in sampleframes:
  t=time_at(f);head=zstart+.135*t;verts=[]
  for k in range(NR):
   u01=k/(NR-1);z=head-length*u01
   p,u,v,a=position(routeid,z,t,side,depth,radius=.004)
   taper=max(.018,math.sin(math.pi*u01)**.8)
   for q in range(SIDES):
    angle=math.tau*q/SIDES;verts.append(p+taper*1.35*(.00125*math.cos(angle)*u+.0024*math.sin(angle)*v))
  states.append(verts)
 me=bpy.data.meshes.new(f'S05_v018_WispMesh_{routeid}_{j}');me.from_pydata(states[0],[],faces);me.materials.append(wmat)
 alpha=me.attributes.new('wisp_opacity','FLOAT','POINT')
 for k in range(NR):
  for q in range(SIDES):alpha.data[k*SIDES+q].value=(.58 if routeid==2 else .30)*math.sin(math.pi*k/(NR-1))**.65
 o=bpy.data.objects.new(f'S05_v018_Wisp_{routeid}_{j}',me);fx.objects.link(o)
 for p in me.polygons:p.use_smooth=True
 o.shape_key_add(name='Basis');me.shape_keys.use_relative=False
 for index,verts in enumerate(states[1:],1):
  key=o.shape_key_add(name=f'Frame_{sampleframes[index]:03}');key.data.foreach_set('co',np.array(verts,dtype=np.float32).ravel())
 for key in me.shape_keys.key_blocks:key.interpolation='KEY_LINEAR'
 for index,f in enumerate(sampleframes):me.shape_keys.eval_time=index*10;me.shape_keys.keyframe_insert('eval_time',frame=f)
 linear(me.shape_keys);wisps.append(o)

# Extend accepted actual annular volume across the entire photographed system.
# It rotates only its solid-exclusion boundary; density advection remains world-based.
NA=240;NZ=301;Z0=-1.25;Z1=1.75;zs=np.linspace(Z0,Z1,NZ);angles=np.arange(NA)*math.tau/NA
raw=np.array([[surface(float(z),float(a)) for a in angles] for z in zs]);robust=raw.copy()
for dz in [-1,0,1]:
 for da in [-1,0,1]:robust=np.maximum(robust,np.roll(raw[np.clip(np.arange(NZ)+dz,0,NZ-1)],da,axis=1))
inner=robust+.001;outer=R-.001;assert inner.max()<outer
verts=[((outer if outerlayer else inner[j,i])*math.cos(a),(outer if outerlayer else inner[j,i])*math.sin(a),float(z)) for outerlayer in [False,True] for j,z in enumerate(zs) for i,a in enumerate(angles)]
N=NZ*NA;faces=[];mats=[]
for layer in [0,1]:
 for j in range(NZ-1):
  for i in range(NA):
   a=layer*N+j*NA+i;b=layer*N+j*NA+(i+1)%NA;c=b+NA;d=a+NA;faces.append((a,b,c,d) if layer else (d,c,b,a));mats.append(0 if layer else 1)
for j in [0,NZ-1]:
 for i in range(NA):a=j*NA+i;b=j*NA+(i+1)%NA;faces.append((a,b,b+N,a+N));mats.append(1)
me=bpy.data.meshes.new('S05_v018_WholeBodyAnnulus');me.from_pydata(verts,[],faces)
for m in fluid.data.materials:me.materials.append(m)
for p,mi in zip(me.polygons,mats):p.material_index=mi;p.use_smooth=mi!=2
fluid.data=me;fluid.name='S05_v018_AnnularFluidDomain';fluid.animation_data_clear()
for f in [1,NFR]:fluid.rotation_euler.z=OMEGA*time_at(f);fluid.keyframe_insert('rotation_euler',frame=f)
linear(fluid)

# Fixed cutaway formation: increase only the amount of surrounding rock shown.
wall=bpy.data.objects['S05_FixedHalfBorehole'];wall.data=wall.data.copy()
for v in wall.data.vertices:
 r=math.hypot(v.co.x,v.co.y)
 if r>.20:v.co.x*=.42/r;v.co.y*=.42/r
wall['v018_change']='Outer presentation rock extent .42m; actual borehole inner radius unchanged.'
for old in list(wall.data.materials):
 m=old.copy();m.name=old.name+'_v018';wall.data.materials[list(wall.data.materials).index(old)]=m
 p=next((n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None) if m.use_nodes else None
 if p:
  p.inputs['Base Color'].default_value=(.135,.145,.15,1);p.inputs['Roughness'].default_value=.94

# Three compositions, two motivated cuts; same upward screen direction.
cam=s.camera;cam.animation_data_clear();cam.data.animation_data_clear();cam.data.shift_x=0;cam.data.shift_y=0;cam.data.lens=49
camera_scores=[]
def pose(f,distance,azimuth,zcam,zlook,lens,roll=-48,shift=(0,0)):
 az=math.radians(azimuth);cam.location=(distance*math.cos(az),distance*math.sin(az),zcam)
 cam.rotation_mode='QUATERNION';cam.rotation_quaternion=(Vector((0,0,zlook))-cam.location).to_track_quat('-Z','Y')@Quaternion((0,0,1),math.radians(roll))
 cam.data.lens=lens;cam.data.shift_x,cam.data.shift_y=shift
 for prop in ['location','rotation_quaternion']:cam.keyframe_insert(prop,frame=f)
 for prop in ['lens','shift_x','shift_y']:cam.data.keyframe_insert(prop,frame=f)
 camera_scores.append({'frame':f,'position':list(cam.location),'quaternion':list(cam.rotation_quaternion),'lens':lens,'target_z':zlook})
for f in range(1,NFR+1):
 if f<=120:
  q=smooth((f-1)/119);pose(f,2.15-.45*q,-4+4*q,-.32+.48*q,-.39+.42*q,49,-48)
 elif f<=288:
  q=smooth((f-121)/167);pose(f,1.18-.04*math.sin(math.pi*q),0,.22+.20*q,.15+.20*q,49,-48,(.043687701,.058543459))
 else:
  q=smooth((f-289)/143);follow=smooth((f-289)/48);wide=smooth((f-330)/90)
  pose(f,1.55+2.05*wide,0-5*wide,.80+.17*follow-.40*wide,.73+.17*follow-.60*wide,49,-48+6*wide)
linear(cam);linear(cam.data)
for marker in list(s.timeline_markers):s.timeline_markers.remove(marker)
for name,f in [('A / borehole and accelerator',1),('B / approved pad interaction',121),('C / diffuser then integrated body',289)]:s.timeline_markers.new(name,frame=f)
s.frame_start=1;s.frame_end=NFR;s.render.fps=24;s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.eevee.taa_render_samples=6
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.film_transparent=False
s['production_scope']='Owner-released 18s v018 low-cost Section 5 previs. Three compositions. Illustrative stage mapping, not CFD.'
s['editorial_conflict']='S05 now 58-76s, 18s rather than prior12s; owner resolves S06/S07 and narration later.'
s.frame_set(198);s.render.filepath='//../Previews/interaction.png';bpy.ops.wm.save_as_mainfile(filepath=str(B/'Scenes/S05_full-cinematic_v018.blend'))
(B/'Records/camera-score.json').write_text(json.dumps(camera_scores))
record={'frames':432,'seconds':18,'fps':24,'rotation_deg_per_s':-5,'source_time_offset_frames':150,'core_v017_frames':'151-246 unchanged tracked positions, sizes and speed','wisps':len(wisps),'cuttings':len(rocks),'fluid_grid':[NZ,NA],'stage_mapping_world_z':{'lower':[-.06,.15],'middle':[.15,.62],'upper':[.62,1]},'mapping_status':'Morphological interpretation inherited T48; functional face/end identity unverified','source_length_m':2.4,'borehole_radius_m':R,'source':'Interaction-Proof_v017','no_hardware_translation':True,'all_regions_simultaneous':True,'work_revision':701}
(B/'Records/build.json').write_text(json.dumps(record,indent=2));result=record
