"""Bounded v005 treatment: preserve v004 centres, shorter shaded tracers,
matte cuttings without tails, stable camera observation interval."""
import bpy,math,json,hashlib,random
from pathlib import Path
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
B=Path(__file__).resolve().parents[1];OLD=B.parent/'Interaction-Proof_v004'
OUT=B/'Scenes/S05_twisted-pad_interaction_v005.blend';s=bpy.context.scene
assert not OUT.exists()
assert Path(bpy.data.filepath).resolve()==(OLD/'Scenes/S05_twisted-pad_interaction_v004.blend').resolve()
assert not bpy.data.is_dirty
cam=s.camera;poses={}
for f in [55,72,90]:s.frame_set(f);poses[f]=(cam.location.copy(),cam.rotation_quaternion.copy())
s.frame_set(1);bpy.context.view_layer.update();vv=[];ff=[]
for o in bpy.data.collections['S05_LINKED_HARDWARE'].objects:
 off=len(vv);vv.extend(o.matrix_world@v.co for v in o.data.vertices);ff.extend([[off+i for i in p.vertices] for p in o.data.polygons])
tree=BVHTree.FromPolygons(vv,ff);R=.155575
def clearance(pos,f):
 q=Matrix.Rotation(math.radians(5)*(f-1)/24,4,'Z')@Vector(pos);r=math.hypot(q.x,q.y);u=Vector((q.x/r,q.y/r,0));hit=tree.ray_cast(Vector((0,0,q.z))+u*.18,-u,.18)[0]
 return min(tree.find_nearest(q)[3],R-r,r-math.hypot(hit.x,hit.y) if hit else 1)
rows=json.loads((OLD/'Records/tracks.json').read_text());byid={p['index']:p for p in rows}
candidate=[]
for p in rows:
 if p['kind']=='fluid':
  minimum=min(clearance(pt,f) for f,pt in enumerate(p['heads'],1))
  front=sum(1 for x,y,z in p['heads'] if .05<z<.65 and abs((math.atan2(y,x)-.40+math.pi)%math.tau-math.pi)<.9)
  if minimum>.0065:candidate.append((front,minimum,p['index']))
candidate.sort(reverse=True);chosen=[];lanes=set()
for front,d,i in candidate:
 lane=byid[i]['route']
 if lane not in lanes and front>10:chosen.append((i,d));lanes.add(lane)
 if len(chosen)==4:break
assert len(chosen)==4,candidate
bpy.ops.wm.save_as_mainfile(filepath=str(OUT));s.name='S05_Hydraulic_Interaction_v005'
oldfx=bpy.data.collections['S05_VOLUME_FLOW_v004'];oldfx.hide_render=True;oldfx.hide_viewport=True
fx=bpy.data.collections.new('S05_READABLE_FLOW_v005');s.collection.children.link(fx)
def material(name,color,roughness,emission=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=roughness;p.inputs['Emission Color'].default_value=(*color,1);p.inputs['Emission Strength'].default_value=emission;return m
amber=material('S05_v005_AmberMovingFluid',(.68,.27,.035),.32,.16)
amber.node_tree.nodes.get('Principled BSDF').inputs['IOR'].default_value=1.33
stone=[material('S05_v005_StoneBody',(.29,.255,.205),.95),material('S05_v005_StoneLightFacet',(.49,.445,.365),.96),material('S05_v005_StoneDarkFacet',(.16,.145,.12),1.)]
def linear(block):
 if block.animation_data and block.animation_data.action:
  for la in block.animation_data.action.layers:
   for st in la.strips:
    for bag in st.channelbags:
     for fc in bag.fcurves:
      for k in fc.keyframe_points:k.interpolation='LINEAR'
records=[]
for p in rows:
 i=p['index']
 if p['kind']!='fluid':continue
 src=bpy.data.objects[f'S05_v004_fluid_HistoryTail_{i:02}'];o=src.copy();o.data=src.data.copy();o.name=f'S05_v005_MovingSegment_{i:02}';fx.objects.link(o);o.data.materials.clear();o.data.materials.append(amber)
 # Keep the existing movement history and exact leading-centre track; retain
 # only 28% of the visible history as a compact volumetric moving segment.
 for key in o.data.shape_keys.key_blocks:
  centres=[sum((key.data[j*6+k].co for k in range(6)),Vector())/6 for j in range(41)]
  oldradius=max((key.data[k].co-centres[0]).length for k in range(6));fade=min(1,oldradius/.00085)
  pts=[]
  for j in range(41):
   q=j*.28;a=min(39,int(q));pts.append(centres[a].lerp(centres[a+1],q-a))
  for j,pt in enumerate(pts):
   tangent=pts[min(40,j+1)]-pts[max(0,j-1)]
   if tangent.length<1e-7:tangent=Vector((0,0,1))
   tangent.normalize();u=tangent.cross(Vector((0,0,1)))
   if u.length<.01:u=tangent.cross(Vector((1,0,0)))
   u.normalize();v=tangent.cross(u).normalized()
   # Rounded leading tip, substantial centre and finely tapering trailing end.
   profile=max(0,math.sin(math.pi*(.08+.92*j/40)))**.75
   rr=.00130*profile*fade
   for k in range(6):key.data[j*6+k].co=pt+rr*(u*math.cos(k*math.tau/6)+v*math.sin(k*math.tau/6))
 # Basis mesh mirrors the edited Basis key.
 for v,k in zip(o.data.vertices,o.data.shape_keys.key_blocks[0].data):v.co=k.co
 o['meaning']='Compact shaded moving tracer, exact v004 leading-centre trajectory and 28 percent of prior visible history; no persistent guide'
records.append({'fluid_segments':54,'leading_centres':'Exact v004 tracks preserved','history_fraction':.28,'maximum_radius_m':.0013})
random.seed(505)
rockdetails=[]
def prepare_rock(o,radius):
 o.data=o.data.copy();o.data.materials.clear()
 for m in stone:o.data.materials.append(m)
 # Flatten and irregularly facet the chip inside the specified support sphere.
 for v in o.data.vertices:v.co.x*=random.uniform(.82,1.18);v.co.y*=random.uniform(.66,.88);v.co.z*=random.uniform(.85,1.15)
 scale=radius/max(v.co.length for v in o.data.vertices)
 for v in o.data.vertices:v.co*=scale
 for poly in o.data.polygons:poly.material_index=random.choices([0,1,2],[5,3,1])[0];poly.use_smooth=False
for p in rows:
 if p['kind']!='rock':continue
 i=p['index'];src=bpy.data.objects[f'S05_v004_Rock_{i:02}'];o=src.copy();o.name=f'S05_v005_Rock_{i:02}';fx.objects.link(o)
 available=min(clearance(pt,f) for f,pt in enumerate(p['heads'],1));radius=min(.0056,available-.0012);assert radius>.0035
 prepare_rock(o,radius);rockdetails.append({'object':o.name,'source_track':i,'support_radius_m':radius})
for n,(i,available) in enumerate(chosen):
 # This selected representative is now a solid cutting. Hide its coincident
 # fluid marker so the chip cannot acquire an apparent glowing spark tail.
 marker=bpy.data.objects[f'S05_v005_MovingSegment_{i:02}'];marker.hide_render=True;marker.hide_viewport=True
 p=byid[i];src=bpy.data.objects['S05_v004_Rock_54'];o=src.copy();o.animation_data_clear();o.name=f'S05_v005_Rock_Added_{n:02}';fx.objects.link(o);radius=min(.0056,available-.0012);prepare_rock(o,radius)
 for f,pos in enumerate(p['heads'],1):
  t=(f-1)/24;o.location=pos;o.rotation_euler=(.19*t+n,.22*t+.7*n,.16*t);z=pos[2]
  def sm(x):x=max(0,min(1,x));return x*x*(3-2*x)
  fade=min(sm((z+.30)/.10),sm((.98-z)/.10));o.scale=(fade,)*3
  for prop in ['location','rotation_euler','scale']:o.keyframe_insert(prop,frame=f)
 linear(o)
 wraps=[f for f in range(1,144) if p['heads'][f][2]-p['heads'][f-1][2]<-.5]
 for la in o.animation_data.action.layers:
  for st in la.strips:
   for bag in st.channelbags:
    for fc in bag.fcurves:
     if fc.data_path=='location':
      for k in fc.keyframe_points:
       if round(k.co.x) in wraps:k.interpolation='CONSTANT'
 rockdetails.append({'object':o.name,'source_fluid_track':i,'support_radius_m':radius})
# Four-second exact hold, surrounded by small eased moves within v004's framing.
cam.animation_data_clear()
for f in range(1,145):
 if f<25:a,b=poses[55],poses[72];u=(f-1)/24
 elif f<=120:a=b=poses[72];u=0
 else:a,b=poses[72],poses[90];u=(f-120)/24
 u=u*u*(3-2*u);cam.location=a[0].lerp(b[0],u);cam.rotation_quaternion=a[1].slerp(b[1],u)
 cam.keyframe_insert('location',frame=f);cam.keyframe_insert('rotation_quaternion',frame=f)
linear(cam);s.frame_set(72);s.render.filepath='//../Work/Frames/S05_';s['proof_scope']='v005 compact shaded tracers, matte recognizable chips, 4-second camera hold; exact v004 flow centres and rotation preserved'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
result={'fluid_segments':50,'cuttings':rockdetails,'camera_hold_frames':[25,120],'camera_hold_seconds':4,'tool_rotation_unchanged':True,'source_v004_sha256':hashlib.sha256((OLD/'Scenes/S05_twisted-pad_interaction_v004.blend').read_bytes()).hexdigest(),'changes':records,'four_markers_represented_as_cuttings':[i for i,d in chosen],'limits':'Illustrative visible tracers and authored chip sizes, not calibrated particles, CFD or hydraulic performance.'}
(B/'Records/build.json').write_text(json.dumps(result,indent=2))
