"""Versioned A-WORLD builder; isolated background Blender only.

Original T5/T6 files are read-only. Product mesh/refs remain exact. Consumers
link immutable libraries; their local instances own placement and animation.
"""
import bpy, math, json, hashlib, sys, time, platform, os
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[5]
PROD=ROOT/'04-Production'; ASSET=PROD/'Shared/Assets'; WORLD=ASSET/'World'
TASK=PROD/'Records/Tasks/T-044'; EVID=TASK/'Evidence'; TEST=TASK/'ReuseTests'
for p in [WORLD,EVID,TEST,TASK/'Previews'] : p.mkdir(parents=True,exist_ok=True)
T5=ASSET/'ECCO/ECCO_master_temporary-plugs_v002.blend'
T6=ASSET/'WellAssembly/WellAssembly_variants_v003.blend'
EXPECTED={T5:'704a91cb478a1a38304835786fa62d549df5bf5833e457cbc4da094fd6557fd7',T6:'6bdacfefa6b999d941d0e2a93a75b26563be8e46141ee761114fdb81dae754c4'}
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def relative(p): return p.relative_to(ROOT).as_posix()
def dump(p,data): p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data,indent=2),encoding='utf-8')
def clean():
 bpy.ops.wm.read_factory_settings(use_empty=True)
 s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1
 return s
def coll(name,parent=None):
 c=bpy.data.collections.new(name);c.use_fake_user=True
 if parent:parent.children.link(c)
 return c
def empty(name,col):
 o=bpy.data.objects.new(name,None);col.objects.link(o);o.empty_display_size=.08;return o
def mat(name,color,metal=0,rough=.45,noise=None):
 m=bpy.data.materials.get(name) or bpy.data.materials.new(name);m.use_nodes=True
 ns=m.node_tree.nodes;ns.clear();out=ns.new('ShaderNodeOutputMaterial');bs=ns.new('ShaderNodeBsdfPrincipled')
 bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Metallic'].default_value=metal;bs.inputs['Roughness'].default_value=rough
 m.diffuse_color=(*color,1);m.node_tree.links.new(bs.outputs['BSDF'],out.inputs['Surface'])
 if noise:
  tex=ns.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=noise
  tex.inputs['Detail'].default_value=2;tex.inputs['Roughness'].default_value=.7
  tc=ns.new('ShaderNodeTexCoord');m.node_tree.links.new(tc.outputs['Object'],tex.inputs['Vector'])
  bump=ns.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.26;bump.inputs['Distance'].default_value=.002
  m.node_tree.links.new(tex.outputs['Fac'],bump.inputs['Height']);m.node_tree.links.new(bump.outputs['Normal'],bs.inputs['Normal'])
 return m
def assign(o,m):o.data.materials.clear();o.data.materials.append(m)
def save(path):
 if path.exists(): raise RuntimeError('Refuse candidate overwrite: '+str(path))
 for l in bpy.data.libraries:l.filepath=bpy.path.relpath(bpy.path.abspath(l.filepath),start=str(path.parent))
 bpy.context.scene['task']='T44 A-WORLD; reusable illustration, not engineering certification or full film shot'
 bpy.ops.wm.save_as_mainfile(filepath=str(path),relative_remap=False)
def linkcoll(path,names):
 with bpy.data.libraries.load(str(path),link=True) as (a,b):
  assert all(n in a.collections for n in names),(path,names,a.collections)
  b.collections=names
 return b.collections
def instance(c,col,name,location=(0,0,0)):
 o=empty(name,col);o.instance_type='COLLECTION';o.instance_collection=c;o.location=location;return o
def mesh(name,verts,faces,col,m=None):
 d=bpy.data.meshes.new(name);d.from_pydata(verts,[],faces);d.update()
 o=bpy.data.objects.new(name,d);col.objects.link(o)
 if m:assign(o,m)
 return o
def lathe(name,profile,col,m,n=64,sector=(0,2*math.pi)):
 vs=[];fs=[]
 for x,r in profile:
  for j in range(n+1):
   a=sector[0]+(sector[1]-sector[0])*j/n;vs.append((x,r*math.cos(a),r*math.sin(a)))
 for i in range(len(profile)-1):
  for j in range(n):
   z=i*(n+1)+j;fs.append((z,z+1,z+n+2,z+n+1))
 o=mesh(name,vs,fs,col,m)
 for p in o.data.polygons:p.use_smooth=True
 return o
def tube(name,x0,x1,ri,ro,col,m,cut=False):
 return lathe(name,[(x0,ri),(x0,ro),(x1,ro),(x1,ri),(x0,ri)],col,m,sector=(-math.pi/2,math.pi/2) if cut else (0,2*math.pi))
def box(name,loc,size,col,m):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=size
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 for c in list(o.users_collection):c.objects.unlink(o)
 col.objects.link(o);assign(o,m);return o
def beam(name,a,b,r,col,m):
 d=Vector(b)-Vector(a);bpy.ops.mesh.primitive_cylinder_add(vertices=8,radius=r,depth=d.length,location=(Vector(a)+Vector(b))/2)
 o=bpy.context.object;o.name=name;o.rotation_euler=d.to_track_quat('Z','Y').to_euler()
 for c in list(o.users_collection):c.objects.unlink(o)
 col.objects.link(o);assign(o,m);return o
def materials_product():
 for m in list(bpy.data.materials):
  if m.name=='Housing_neutral': mat(m.name,(.40,.43,.46),.86,.32)
  elif m.name=='TEMP_CLOSURES_neutral':mat(m.name,(.30,.33,.36),.78,.36)
def build_product():
 s=clean()
 with bpy.data.libraries.load(str(T5),link=False) as (a,b):b.collections=['ECCO_MASTER_v002']
 c=b.collections[0];c.name='ECCO_FILM';s.collection.children.link(c);c['source_sha256']=sha(T5);c['revision']='film_v001 material-only derivative of accepted T5 v002'
 materials_product()
 for o in c.all_objects:
  if o.type=='MESH' and o.name=='ECCO_HOUSING_SOURCE_MESH':
   for p in o.data.polygons:p.use_smooth=True
 c['revision']='film_v002; smooth shading and satin materials; vertex/face topology unchanged'
 save(ASSET/'ECCO/ECCO_film_v002.blend')
def build_hardware():
 s=clean();c=coll('WORLD_HARDWARE');s.collection.children.link(c)
 c['revision']='v002';c['default_travel_m']=.5;c['default_rotation_rad']=0.;c['axes']='metres; +X selected downhole layout; pin/box identity unverified'
 p=linkcoll(ASSET/'ECCO/ECCO_film_v002.blend',['ECCO_FILM'])[0]
 instance(p,c,'ECCO_FILM_LINK')
 anchor=empty('HARDWARE_ORIGIN',c);anchor['interface']='Root placement via consumer collection instance; geometry/sensor refs master-owned'
 steel=mat('WORLD_SatinSteel',(.34,.38,.42),.88,.33);dark=mat('WORLD_AdapterSteel',(.24,.28,.31),.8,.38)
 cutter=mat('WORLD_GenericCutter',(.065,.07,.075),.65,.28)
 # T6 sourced collar OD/ID and illustrative local extents (T6 travel removed).
 for name,x0,x1 in [('UPHOLE_COLLAR',-1.5,-.12),('DOWNHOLE_COLLAR',2.52,2.9)]:
  o=tube(name,x0,x1,.03571875,.104775,c,steel);o['source']='T6 generic collar dimensional reference; lengths/placement illustrative'
 for name,x0,x1 in [('UPHOLE_ADAPTER',-.12,0),('DOWNHOLE_ADAPTER',2.4,2.52)]:
  o=lathe(name,[(x0,.03571875),(x0,.102),(x0+.015,.107),(x1-.015,.107),(x1,.102),(x1,.03571875),(x0,.03571875)],c,dark)
  o['status']='Simplified crossover sleeve; no modeled threads or FH/REG compatibility claim'
 # Generic six-blade fixed-cutter silhouette. Gauge retained from T6, details authored.
 bit=lathe('GENERIC_BIT_BODY',[(2.9,.03),(2.9,.10),(2.95,.14),(3.08,.146),(3.20,.10),(3.24,.035),(2.9,.03)],c,dark)
 bit['status']='Illustrative fixed-cutter silhouette, not selected MIT bit; six blades/cutter placement authored; gauge12.25in'
 bit['reference']='https://www.slb.com/products-and-services/innovating-in-oil-and-gas/well-construction/drilling/drill-bits/pdc-bits'
 for k in range(6):
  vs=[];fs=[]
  stations=[(2.94,.142),(3.04,.155575),(3.15,.133),(3.23,.055)]
  for x,r in stations:
   for dr,da in [(-.013,-.10),(0,-.10),(0,.10),(-.013,.10)]:
    a=k*math.tau/6+.55*(x-2.94)+da;vs.append((x,(r+dr)*math.cos(a),(r+dr)*math.sin(a)))
  for i in range(3):
   for j in range(4):a=i*4+j;b=i*4+(j+1)%4;fs.append((a,b,b+4,a+4))
  fs.extend([(0,3,2,1),(12,13,14,15)]);o=mesh('GENERIC_BIT_BLADE_%02d'%k,vs,fs,c,steel)
  for j,(x,r) in enumerate(stations[1:]):
   a=k*math.tau/6+.55*(x-2.94)-.11;r-=.011
   bpy.ops.mesh.primitive_cylinder_add(vertices=12,radius=.009,depth=.006,location=(x,r*math.cos(a),r*math.sin(a)))
   q=bpy.context.object;q.name='GENERIC_CUTTER_%d_%d'%(k,j);q.rotation_euler=(Vector((.5,-math.sin(a),math.cos(a)))).to_track_quat('Z','Y').to_euler()
   for cc in list(q.users_collection):cc.objects.unlink(q)
   c.objects.link(q);assign(q,cutter)
 for name,x in [('UPHOLE_AXIS',-1.5),('DOWNHOLE_AXIS',3.24)]:a=empty(name,c);a.location.x=x
 save(ASSET/'BHA/BHA_film_v002.blend')
def build_environment():
 s=clean();root=coll('WORLD_ENV');s.collection.children.link(root)
 with bpy.data.libraries.load(str(T6),link=False) as (a,b): b.collections=['WELL_INTERVALS']
 old=b.collections[0]
 rock=mat('WORLD_WetMineral',(.075,.061,.049),.08,.44,38)
 steel=mat('WORLD_CasingSteel',(.25,.29,.34),.8,.34)
 cement=mat('WORLD_Cement',(.19,.16,.125),0,.83,90)
 groups=[]
 for o in list(old.all_objects):
  if o.type!='MESH':continue
  o.animation_data_clear();o.hide_render=False;o.hide_viewport=False
  if o.data.shape_keys:
   o.data.shape_keys.animation_data_clear();o.data.shape_keys.key_blocks[1].value=1
  for cc in list(o.users_collection):cc.objects.unlink(o)
  c=coll('WORLD_'+o.name);c.objects.link(o);groups.append(c)
  assign(o,steel if o.name.startswith('CASING') else cement if o.name.startswith('CEMENT') else rock)
  if o.name in ['IRREGULAR_CUTAWAY','CASING_CUTAWAY','CEMENT_CUTAWAY']:root.children.link(c)
  o['source_sha256']=sha(T6);o['profile_state']='Exact T6 mesh and authored profile; material-only refinement'
 # Delete non-environment dependencies imported transitively, including ECCO instance.
 keep=set(root.all_objects)
 for c in groups:keep.update(c.all_objects)
 for o in list(bpy.data.objects):
  if o not in keep:bpy.data.objects.remove(o,do_unlink=True)
 for c in list(bpy.data.collections):
  if c not in groups and c!=root:bpy.data.collections.remove(c)
 host=coll('WORLD_UPPER_FORMATION');root.children.link(host)
 tube('UPPER_HOST_ROCK',-5.5,0,.22225,.30,host,rock,True)
 shoe=coll('WORLD_SHOE');root.children.link(shoe)
 o=lathe('ILLUSTRATIVE_SHOE_RIM',[(-.07,.1589405),(-.07,.1698625),(-.015,.1698625),(0,.165),(0,.1589405),(-.07,.1589405)],shoe,steel,sector=(-math.pi/2,math.pi/2))
 o['status']='Bounded rim at T6 interval boundary; not certified shoe/float equipment or connection bore'
 media=coll('WORLD_MUD');root.children.link(media)
 mud=mat('WORLD_FluidOpticalProxy',(.035,.048,.043),.06,.2)
 bs=mud.node_tree.nodes.get('Principled BSDF');bs.inputs['Alpha'].default_value=.08
 mud.surface_render_method='DITHERED';mud.diffuse_color=(.035,.048,.043,.08)
 o=lathe('MUD_REAR_FILM',[(0,.1547),(6,.1547)],media,mud,sector=(-math.pi/2,math.pi/2))
 o['status']='Bounded optical proxy on rear annulus, no calibrated opacity, dry cave or CFD claim. Hidden for data-only views.'
 a=empty('ENV_DEFAULTS',root);a['variant']='IRREGULAR';a['cutaway']=1;a['fluid_present']=1
 a['annulus_domain']='Between source hardware envelope and WELL inner surface; rear film is optical treatment, not full simulated volume'
 root['revision']='v003';root['source_sha256']=sha(T6);root['interface']='Link named WORLD_* collections as local instances; no ECCO in environment'
 save(ASSET/'WellAssembly/World_environment_v003.blend')
 # Bounded shared refinement: grain/catchlight density and roughness, unchanged shape.
 rock.node_tree.nodes.get('Noise Texture').inputs['Scale'].default_value=62
 rock.node_tree.nodes.get('Principled BSDF').inputs['Roughness'].default_value=.34
 rock['revision']='v004; grain38->62/m and roughness.44->.34; geometry/refs unchanged'
 root['revision']='v004';save(ASSET/'WellAssembly/World_environment_v004.blend')
def build_surface():
 s=clean();c=coll('WORLD_SURFACE');s.collection.children.link(c)
 steel=mat('SURFACE_RigSteel',(.07,.085,.095),.65,.52);deck=mat('SURFACE_Deck',(.18,.14,.09),.3,.55)
 water=mat('SURFACE_QuietWater',(.035,.07,.09),.58,.3,0.08)
 box('QUIET_SEA',(0,0,-.2),(1600,1600,.15),c,water)
 box('PLATFORM_DECK',(0,0,8),(34,25,2),c,deck)
 for x in (-12,12):
  for y in (-8,8):beam('RIG_LEG',(x,y,-8),(x,y,8),1,c,steel)
 for x,y,w,d,h in [(8,4,8,7,6),(-9,5,7,6,5),(10,-7,6,5,4)]:box('UNBRANDED_MODULE',(x,y,9+h/2),(w,d,h),c,steel)
 levels=[(9,4),(20,3),(31,2),(40,1.3)]
 for i in range(3):
  z0,r0=levels[i];z1,r1=levels[i+1]
  for j in range(4):
   signs=[(-1,-1),(-1,1),(1,1),(1,-1)];x,y=signs[j];u,v=signs[(j+1)%4]
   beam('DERRICK_LEG',(x*r0,y*r0,z0),(x*r1,y*r1,z1),.18,c,steel)
   beam('DERRICK_BRACE',(x*r0,y*r0,z0),(u*r1,v*r1,z1),.10,c,steel)
   beam('DERRICK_RING',(x*r0,y*r0,z0),(u*r0,v*r0,z0),.13,c,steel)
 beam('SURFACE_STRING',(0,0,-3),(0,0,31),.09,c,steel)
 a=empty('SURFACE_ROUTE_ANCHOR',c);a.location=(0,0,-3);a.rotation_euler=(0,math.pi/2,0)
 c['status']='Director-selected illustrative offshore context, no field location, engineering dimensions or deployment claim'
 c['route']='Source +X maps to local -Z using +90deg about Y. Match cut to metre-scale downhole world; no kilometer-scale mesh.'
 save(ASSET/'Surface/Surface_context_v001.blend')
def reuse_surface():
 import shutil
 folder=ASSET/'Surface/Originals';folder.mkdir(parents=True,exist_ok=True)
 src=Path(r'C:\Users\RZ1\Desktop\RZ\261006-Rolladice\IntoTheInvisible\IntoTheInvisible_Shot01.blend')
 assert sha(src)=='ef669ae4fdd20a74d1d4b6a16e0978c17ae857f5c839dc08128247ff3bf29ab0'
 original=folder/src.name
 if not original.exists():shutil.copy2(src,original)
 assert sha(original)==sha(src)
 s=clean();c=coll('WORLD_SURFACE');s.collection.children.link(c)
 with bpy.data.libraries.load(str(original),link=False) as (a,b):b.collections=['01_SURFACE']
 rig=b.collections[0];rig.name='SURFACE_REUSED_RIG';c.children.link(rig)
 mats={}
 for o in list(rig.all_objects):
  o.animation_data_clear();o.hide_render=o.type=='FONT';o.hide_viewport=False
  if o.type=='MESH':
   old=o.data.materials[0] if o.data.materials else None;name=old.name if old else 'unassigned'
   if name not in mats:
    color=tuple(old.diffuse_color[:3]) if old else (.16,.18,.2)
    mats[name]=mat('SURFACE_Polished_'+name,tuple(min(.6,max(.025,x)) for x in color),.45,.44)
   assign(o,mats[name])
 water=mat('SURFACE_QuietWater',(.025,.055,.078),.58,.3,.08)
 box('QUIET_SEA',(0,0,-.2),(1600,1600,.15),c,water)
 a=empty('SURFACE_ROUTE_ANCHOR',c);a.location=(0,0,14);a.rotation_euler=(0,math.pi/2,0)
 c['revision']='v002 reused owner-designated rig; materials simplified/polished, animation stripped; geometry/layout retained'
 c['source_sha256']=sha(src);c['source']='Originals/IntoTheInvisible_Shot01.blend / 01_SURFACE only'
 c['status']='Illustrative offshore context, not verified ECCO deployment or engineered rig'
 c['route']='Rig source +Z up; source +X downhole maps via +90deg Y. Match cut to local downhole scene; no imported historical well/tool.'
 save(ASSET/'Surface/Surface_context_v002.blend')
 dump(EVID/'rig-reuse_v002.json',dict(original=str(src),preserved_copy=relative(original),sha256=sha(src),unchanged=sha(original)==sha(src),collection='01_SURFACE',objects=len(rig.all_objects),vertices=sum(len(o.data.vertices) for o in rig.all_objects if o.type=='MESH'),changes=['Source collection only; excludes old tool, well, mechanism, lighting, camera, ocean and geology','Retained object transforms/topology/layout','Removed animation on copied objects','Replaced complex materials with restrained PBR equivalents; no textures required','Added simple quiet-water plate and source-axis route anchor']))
def settings(s):
 s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=16;s.eevee.use_raytracing=False
 s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.fps=24
 s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.image_settings.compression=15
 s.render.film_transparent=False;s.render.use_compositing=False
 s.view_settings.view_transform='AgX';s.view_settings.look='AgX - Medium High Contrast'
 w=bpy.data.worlds.new('WORLD_ReviewLighting');w.use_nodes=True;w.node_tree.nodes['Background'].inputs[0].default_value=(.13,.16,.20,1);w.node_tree.nodes['Background'].inputs[1].default_value=.45;s.world=w
def light(name,loc,target,power,size,col,color=(1,1,1)):
 d=bpy.data.lights.new(name,'AREA');d.energy=power;d.shape='DISK';d.size=size;d.color=color;d.use_shadow=False
 o=bpy.data.objects.new(name,d);col.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();return o
def driver(o,path,expression,target,prop,index=None):
 f=o.driver_add(path) if index is None else o.driver_add(path,index);d=f.driver;d.expression=expression
 v=d.variables.new();v.name='v';v.type='SINGLE_PROP';v.targets[0].id=target;v.targets[0].data_path='["'+prop+'"]'
def build_consumer(kind):
 s=clean();settings(s);c=coll('LOCAL_REUSE_TEST');s.collection.children.link(c)
 s['consumer']=kind;s['purpose']='T44 linked-library reuse test only; not a completed V3 film shot'
 ctrl=empty('CONSUMER_CONTROL',c)
 if kind=='surface':
  cc=linkcoll(ASSET/'Surface/Surface_context_v002.blend',['WORLD_SURFACE'])[0];instance(cc,c,'SURFACE_INSTANCE')
  loc=(115,-180,75);target=(0,0,24);lens=45;end=48
  s.world.node_tree.nodes['Background'].inputs[0].default_value=(.23,.15,.095,1)
  light('HORIZON_KEY',(-60,-30,70),(0,0,8),250000,70,c,(1,.58,.27));light('SKY_FILL',(20,-50,50),(0,0,12),180000,80,c,(.3,.55,1))
 else:
  hw=linkcoll(ASSET/'BHA/BHA_film_v002.blend',['WORLD_HARDWARE'])[0];h=instance(hw,c,'HARDWARE_INSTANCE')
  ctrl['travel_m']=.5;ctrl['rotation_rad']=.4;ctrl['show_mud']=1
  driver(h,'location','v',ctrl,'travel_m',0);driver(h,'rotation_euler','v',ctrl,'rotation_rad',0)
  names=['WORLD_IRREGULAR_CUTAWAY','WORLD_CASING_CUTAWAY','WORLD_CEMENT_CUTAWAY','WORLD_UPPER_FORMATION','WORLD_SHOE','WORLD_MUD']
  for q in linkcoll(ASSET/'WellAssembly/World_environment_v003.blend',names):
   z=instance(q,c,q.name+'_INSTANCE')
   if q.name=='WORLD_MUD':driver(z,'hide_render','1-v',ctrl,'show_mud')
  if kind=='A':loc=(1.9,-2.0,1.15);target=(1.65,0,0);lens=48;end=72;travel=[.5,.68]
  else:loc=(1.5,-4.5,2.2);target=(.35,0,0);lens=49;end=96;travel=[.5,-1.25]
  for f,t in [(1,travel[0]),(end,travel[1])]:ctrl['travel_m']=t;ctrl.keyframe_insert(data_path='["travel_m"]',frame=f)
  light('BROAD_KEY',(1.2,-1.5,1.4),(1.2,0,0),160,2.4,c,(.66,.82,1))
  light('WARM_EDGE',(2.6,.3,.8),(1.4,0,0),100,1.8,c,(1,.68,.39))
  light('LOW_FILL',(-1,-.7,-.5),(1.0,0,0),55,1.5,c,(.35,.55,.8))
 d=bpy.data.cameras.new('REUSE_CAMERA_'+kind);o=bpy.data.objects.new(d.name,d);c.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();d.lens=lens;d.clip_start=.005;d.clip_end=2500
 s.camera=o;s.frame_start=1;s.frame_end=end
 o.keyframe_insert(data_path='location',frame=1);o.location.x+=.08 if kind!='surface' else 2;o.keyframe_insert(data_path='location',frame=end)
 s.frame_set(1);save(TEST/('Reuse_'+kind+'_before_v003.blend'))
def snapshot():
 s=bpy.context.scene
 def keys(id):
  if not id.animation_data or not id.animation_data.action:return []
  a=id.animation_data.action;out=[]
  for layer in a.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for f in bag.fcurves:out.append([f.data_path,f.array_index,[[round(k.co.x,6),round(k.co.y,6),k.interpolation] for k in f.keyframe_points]])
  return out
 return dict(camera=dict(name=s.camera.name,location=list(s.camera.location),rotation=list(s.camera.rotation_euler),lens=s.camera.data.lens,keys=keys(s.camera)),timing=[s.frame_start,s.frame_end,s.render.fps],local_controls={o.name:dict(properties={k:o[k] for k in o.keys()},keys=keys(o),location=list(o.location),scale=list(o.scale)) for o in bpy.data.objects if not o.library and o.type=='EMPTY'},libraries=[dict(path=l.filepath,resolved=bpy.path.abspath(l.filepath),exists=Path(bpy.path.abspath(l.filepath)).exists()) for l in bpy.data.libraries],mineral=dict(roughness=bpy.data.materials['WORLD_WetMineral'].node_tree.nodes.get('Principled BSDF').inputs['Roughness'].default_value,grain=bpy.data.materials['WORLD_WetMineral'].node_tree.nodes.get('Noise Texture').inputs['Scale'].default_value) if 'WORLD_WetMineral' in bpy.data.materials else None)
def migrate(kind):
 before=TEST/('Reuse_'+kind+'_before_v003.blend');after=TEST/('Reuse_'+kind+'_after_v004.blend')
 bpy.ops.wm.open_mainfile(filepath=str(before),load_ui=False);snap=snapshot()
 targets=[l for l in bpy.data.libraries if Path(bpy.path.abspath(l.filepath)).name=='World_environment_v003.blend'];assert len(targets)==1
 # Single procedure updates the common library, not any copied mesh/material.
 targets[0].filepath=bpy.path.relpath(str(ASSET/'WellAssembly/World_environment_v004.blend'),start=str(TEST));targets[0].reload()
 bpy.context.scene.frame_set(1);post=snapshot();assert snap['camera']==post['camera'];assert snap['timing']==post['timing'];assert snap['local_controls']==post['local_controls']
 save(after);dump(EVID/('migration_'+kind+'_v004.json'),dict(before=snap,after=post,camera_timing_controls_preserved=True,procedure='Reload environment library v003 -> v004; no local object/material edits'))
def verify(path):
 bpy.ops.wm.open_mainfile(filepath=str(path),load_ui=False,use_scripts=False);s=bpy.context.scene;bpy.context.view_layer.update()
 snap=snapshot();linked_product=[o for o in bpy.data.objects if o.name=='ECCO_FILM_LINK'];housing=bpy.data.objects.get('ECCO_HOUSING_SOURCE_MESH')
 rec=dict(path=relative(path),sha256=sha(path),snapshot=snap,one_product_instance=len(linked_product)==1 if s['consumer']!='surface' else None,all_links_relative=all(l.filepath.startswith('//') for l in bpy.data.libraries),all_links_exist=all(x['exists'] for x in snap['libraries']),units=s.unit_settings.scale_length)
 if housing:
  rec['housing_vertices']=len(housing.data.vertices);rec['housing_mesh_hash']=hashlib.sha256(b''.join(__import__('struct').pack('<3f',*v.co) for v in housing.data.vertices)).hexdigest()
  rec['sensor_refs']={o.name:list(o.location) for o in bpy.data.objects if o.name.startswith('ECCO_SENSOR_REF_')}
  deps=bpy.context.evaluated_depsgraph_get();rec['evaluated_housing_instances']=sum(1 for i in deps.object_instances if i.object.original.name=='ECCO_HOUSING_SOURCE_MESH')
 dump(EVID/(path.stem+'_fresh-open.json'),rec);assert rec['all_links_exist'] and rec['all_links_relative'];return rec
def benchmark(path,frames):
 verify(path);s=bpy.context.scene;rows=[]
 label=os.environ.get('T44_BENCH_LABEL','')
 stem=path.stem+('_'+label if label else '')
 import gpu
 hw=dict(gpu='NVIDIA GeForce GTX1060 3GB',driver='560.94 (nvidia-smi)',cpu=platform.processor(),platform=platform.platform())
 for i,f in enumerate(frames):
  s.frame_set(f);s.render.filepath=str(TASK/'Previews'/(stem+'_f%03d.png'%f));start=time.perf_counter()
  bpy.ops.render.render(write_still=True);elapsed=time.perf_counter()-start
  rows.append(dict(frame=f,cold=i==0,seconds=elapsed,output=relative(Path(s.render.filepath)),under_5=elapsed<5))
  dump(EVID/(stem+'_benchmark.json'),dict(hardware=hw,backend=gpu.platform.backend_type_get(),label=label,engine=s.render.engine,resolution=[s.render.resolution_x,s.render.resolution_y],samples=s.eevee.taa_render_samples,color_management=[s.view_settings.view_transform,s.view_settings.look],compositor=s.render.use_compositing,measurement='wall clock around full bpy.ops.render.render(write_still=True), includes render initialization/shaders/compositor if enabled/PNG writing; process/file load excluded; cold means first render in a fresh process using normal existing driver caches, no in-process warmup',renders=rows,all_under_5=all(x['under_5'] for x in rows)))
  print('T44_BENCH',path.name,f,elapsed,flush=True)
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else ['build']
mode=args[0]
if mode=='build':
 for p,h in EXPECTED.items():assert sha(p)==h,(p,'SOURCE HASH MISMATCH')
 for folder in ['BHA','Surface']: (ASSET/folder).mkdir(exist_ok=True)
 build_product();build_hardware();build_environment();reuse_surface()
 for k in ['A','B','surface']:build_consumer(k)
 for k in ['A','B']:migrate(k)
 dump(EVID/'build_v004.json',dict(blender=bpy.app.version_string,source_hashes={relative(p):sha(p) for p in EXPECTED},sources_unchanged=all(sha(p)==h for p,h in EXPECTED.items())))
 print('T44_BUILD_PASS',flush=True)
elif mode=='benchmark':benchmark(TEST/args[1],[int(x) for x in args[2:]])
elif mode=='verify':verify(TEST/args[1])
elif mode=='migrate':migrate(args[1])
elif mode=='consumers':
 reuse_surface()
 for k in ['A','B','surface']:build_consumer(k)
 for k in ['A','B']:migrate(k)
 dump(EVID/'build_v004.json',dict(blender=bpy.app.version_string,source_hashes={relative(p):sha(p) for p in EXPECTED},sources_unchanged=all(sha(p)==h for p,h in EXPECTED.items())))
