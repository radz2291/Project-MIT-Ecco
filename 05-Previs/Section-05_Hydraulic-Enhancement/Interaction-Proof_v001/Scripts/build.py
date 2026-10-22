"""S05 bounded proof. Run through official Blender MCP; no shared-source writes."""
import bpy, math, json, random, hashlib
from pathlib import Path
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree
B=Path(__file__).resolve().parents[1]; ROOT=B.parents[2]
SOURCE=ROOT/'04-Production/Shared/Assets/ECCO/ECCO_film_v002.blend'
OUT=B/'Scenes/S05_twisted-pad_interaction_v001.blend'
assert not OUT.exists(), 'Preserve candidate; use versioned successor'
s=bpy.data.scenes.get('S05_Hydraulic_Interaction_v001')
if s is None:
 s=bpy.data.scenes.new('S05_Hydraulic_Interaction_v001')
bpy.context.window.scene=s
source=bpy.data.collections.get('ECCO_FILM')
if source is None:
 with bpy.data.libraries.load(str(SOURCE),link=True) as (a,b):b.collections=['ECCO_FILM']
 source=b.collections[0]
if source.name not in s.collection.children:s.collection.children.link(source)
bpy.context.view_layer.update()
housing=source.all_objects['ECCO_HOUSING_SOURCE_MESH']
source_matrices={o.name:o.matrix_world.copy() for o in source.all_objects}
verts=[housing.matrix_world@v.co for v in housing.data.vertices]
tree=BVHTree.FromPolygons(verts,[list(p.vertices) for p in housing.data.polygons])
source_dims=list(housing.dimensions)
def collection(name):
 c=bpy.data.collections.new(name);s.collection.children.link(c);return c
hardware=collection('S05_LINKED_HARDWARE'); env=collection('S05_FIXED_SECTION'); fx=collection('S05_ILLUSTRATIVE_FLOW'); rig=collection('S05_CAMERA_LIGHT')
T=Matrix.Translation((0,0,1.5))@Matrix.Rotation(math.pi/2,4,'Y')
for o in source.all_objects:
 if o.type!='MESH' or o.hide_render or 'CUTTER' in o.name:continue
 n=o.copy(); n.name='S05_'+o.name;hardware.objects.link(n);n.parent=None;n.animation_data_clear();n.matrix_world=T@source_matrices[o.name]
 n['source_object']=o.name
s.collection.children.unlink(source)
def mat(name,color,metal=0,rough=.5,emission=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough;p.inputs['Emission Color'].default_value=(*color,1);p.inputs['Emission Strength'].default_value=emission;return m
steel=mat('S05_SatinSteel',(.31,.36,.40),.72,.29)
for o in hardware.objects:
 for slot in o.material_slots:slot.link='OBJECT';slot.material=steel
rock=mat('S05_DarkNeutralFormation',(.047,.056,.062),0,.91)
nodes=rock.node_tree.nodes;links=rock.node_tree.links;bs=nodes.get('Principled BSDF');noise=nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=35;noise.inputs['Detail'].default_value=2;bump=nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.2;bump.inputs['Distance'].default_value=.0015;links.new(noise.outputs['Fac'],bump.inputs['Height']);links.new(bump.outputs['Normal'],bs.inputs['Normal'])
cutface=mat('S05_SectionFace',(.085,.095,.10),0,.85)
amber=mat('S05_FlowAmber',(.56,.25,.052),0,.48,.35)
bright=mat('S05_MovingAmber',(.85,.45,.12),0,.45,.65)
cutmat=mat('S05_RockCuttings',(.29,.235,.16),0,.95)
# Existing T6 nominal 12.25-inch hole, no transverse enlargement.
R=.155575; RO=.215
vv=[];ff=[]; mats=[];N=96
for z in [-1.25,1.65]:
 for r in [R,RO]:
  for i in range(N+1):
   a=math.radians(110+180*i/N);vv.append((r*math.cos(a),r*math.sin(a),z))
stride=N+1
for i in range(N):
 for base in [0,stride]:
  ff.append((base+i,base+i+1,2*stride+base+i+1,2*stride+base+i));mats.append(0)
 for base in [0,2*stride]:ff.append((base+i,base+i+1,base+stride+i+1,base+stride+i));mats.append(1)
for i in [0,N]:ff.append((i,stride+i,3*stride+i,2*stride+i));mats.append(1)
me=bpy.data.meshes.new('S05_SectionedBorehole');me.from_pydata(vv,[],ff);me.materials.append(rock);me.materials.append(cutface)
wall=bpy.data.objects.new('S05_FixedHalfBorehole',me);env.objects.link(wall)
for p,mi in zip(me.polygons,mats):p.material_index=mi;p.use_smooth=mi==0
wall['nominal_hole_ID_m']=2*R;wall['representation']='Fixed half section; simplified formation context; inherited T6 illustrative scenario'
def curve(name,points,radius,material):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.resolution_u=1;cu.bevel_depth=radius;cu.bevel_resolution=1;sp=cu.splines.new('POLY');sp.points.add(len(points)-1)
 for p,v in zip(sp.points,points):p.co=(*v,1)
 cu.materials.append(material);o=bpy.data.objects.new(name,cu);fx.objects.link(o);return o
def smooth_interp(x,knots):
 for (a,av),(b,bv) in zip(knots,knots[1:]):
  if a<=x<=b:
   t=(x-a)/(b-a);t=t*t*(3-2*t);return av+(bv-av)*t
 return knots[0][1] if x<knots[0][0] else knots[-1][1]
knots=[(.70,62),(.92,62),(1.04,60),(1.12,69),(1.23,85),(1.32,85),(1.44,74),(1.72,74)]
paths=[];clearances=[]
for sector in range(3):
 for offset in [-5,0,5]:
  pts=[]
  for j in range(601):
   x=1.72-1.02*j/600;a=math.radians(smooth_interp(x,knots)+120*sector+offset);u=Vector((0,math.cos(a),math.sin(a)))
   hit=tree.ray_cast(Vector((x,0,0))+.18*u,-u,.18)[0];surface=math.hypot(hit.y,hit.z) if hit else .108
   r=max(.128,surface+.006)
   # Guarantee radius can hold a small finite rock cutting; repair locally outward only.
   p=Vector((x,0,0))+r*u
   near=tree.find_nearest(p)[3]
   while near<.0034 and r<.1515:
    r+=.0003;p=Vector((x,0,0))+r*u;near=tree.find_nearest(p)[3]
   assert r+.0028<R,(x,a,r)
   assert near>.0032,(x,a,near)
   clearances.append([near,R-r]);pts.append(p)
  paths.append(pts)
  curve('S05_Guide_%02d'%len(paths),[T@p for p in pts],.00034,amber)
def point_at(points,t):
 q=max(0,min(1,t))*(len(points)-1);i=min(int(q),len(points)-2);return points[i].lerp(points[i+1],q-i)
# Fine tracer dashes and irregular matte fragments use exactly the same path/time field.
random.seed(71); motion=[]
for pi,pts in enumerate(paths):
 for j in range(4):
  o=curve('S05_Tracer_%02d_%d'%(pi,j),[(0,0,-.006),(0,0,.006)],.00065,bright);motion.append((o,pi,j/4,False))
 for j in range(2):
  bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=1)
  o=bpy.context.object;o.name='S05_Cutting_%02d_%d'%(pi,j)
  for c in list(o.users_collection):c.objects.unlink(o)
  fx.objects.link(o)
  for v in o.data.vertices:
   v.co.x*=.0019*random.uniform(.72,1.15);v.co.y*=.0015*random.uniform(.75,1.15);v.co.z*=.0024*random.uniform(.75,1.15)
  o.data.materials.append(cutmat);motion.append((o,pi,(j+.3)/2,True))
for f in range(1,145):
 sec=(f-1)/24
 for o,pi,phase,isrock in motion:
  t=(phase+sec/5.5+pi*.033)%1;p=point_at(paths[pi],t);p2=point_at(paths[pi],min(.99999,t+.001));tangent=(T.to_3x3()@(p2-p)).normalized()
  o.location=T@p;o.rotation_mode='QUATERNION';o.rotation_quaternion=tangent.to_track_quat('Z','Y');o.keyframe_insert('location',frame=f);o.keyframe_insert('rotation_quaternion',frame=f)
  edge=max(0,min(1,t/.035,(1-t)/.035));o.scale=(edge,edge,edge);o.keyframe_insert('scale',frame=f)
for o,_,_,_ in motion:
 for layer in o.animation_data.action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for fc in bag.fcurves:
     for k in fc.keyframe_points:k.interpolation='LINEAR'
camdata=bpy.data.cameras.new('S05_Camera');cam=bpy.data.objects.new('S05_Camera',camdata);rig.objects.link(cam);s.camera=cam;camdata.lens=53;camdata.clip_start=.005;camdata.clip_end=100
for f,loc,target in [(1,(1.28,.48,.62),(.01,0,.22)),(72,(1.16,.51,.69),(.01,0,.30)),(144,(1.11,.57,.75),(.01,0,.37))]:
 cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.keyframe_insert('location',frame=f);cam.keyframe_insert('rotation_euler',frame=f)
def light(name,loc,aim,power,size,color):
 d=bpy.data.lights.new(name,'AREA');d.energy=power;d.shape='DISK';d.size=size;d.color=color;o=bpy.data.objects.new(name,d);rig.objects.link(o);o.location=loc;o.rotation_euler=(Vector(aim)-o.location).to_track_quat('-Z','Y').to_euler()
light('S05_Key',(.65,-.42,1.05),(0,0,.3),45,1.1,(.82,.91,1))
light('S05_Fill',(.5,.9,.25),(0,0,.3),22,.85,(1,.90,.76))
light('S05_Rim',(-.2,-.25,.65),(0,0,.3),18,.5,(.55,.72,1))
w=bpy.data.worlds.new('S05_World');w.use_nodes=True;w.node_tree.nodes['Background'].inputs[0].default_value=(.10,.13,.16,1);w.node_tree.nodes['Background'].inputs[1].default_value=.32;s.world=w
s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=16;s.eevee.use_raytracing=False;s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.fps=24;s.frame_start=1;s.frame_end=144;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.image_settings.compression=10;s.render.use_compositing=False;s.render.film_transparent=False;s.view_settings.view_transform='AgX';s.view_settings.look='AgX - Medium High Contrast';s.unit_settings.system='METRIC'
s['proof_scope']='6-second illustrative interaction; stationary tool; upward return; no CFD/stage-face verification'
s['palette_status']='Amber trial from T43; cyan comparison pending owner selection'
s.frame_set(72);bpy.context.view_layer.update()
for lib in bpy.data.libraries:
 if not lib.parent:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(OUT.parent))
bpy.ops.wm.save_as_mainfile(filepath=str(OUT),relative_remap=False)
record={'source':str(SOURCE),'sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'source_dimensions_m':source_dims,'source_unit_conversion':.001,'placement':'Rigid +90deg Y and +1.5m Z; native -X is world +Z; no geometry scaling','hole_ID_m':2*R,'path_points':len(clearances),'min_center_to_hardware_m':min(q[0] for q in clearances),'min_center_to_wall_m':min(q[1] for q in clearances),'path_method':'Authored channel-following angular guide, radial raycast and nearest-surface clearance constraint; NOT CFD','native_range_m':[.7,1.72],'stage_map':'Raised/twisted morphological region inspected; certified functional mapping and physical pin/box identity unresolved','duration':6,'fps':24,'frames':144,'live_source_was_blank':True}
(B/'Records/build.json').write_text(json.dumps(record,indent=2));(B/'Records/paths.json').write_text(json.dumps([[list(p) for p in pts] for pts in paths]))
result=record
