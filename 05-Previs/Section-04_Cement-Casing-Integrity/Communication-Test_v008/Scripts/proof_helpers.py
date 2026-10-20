# Exact rendering helper functions retained from the inspected v007 proof.
# The native event API and S02 fan data are preserved; no calibrated model is introduced.
import bpy,math,json,sys
from pathlib import Path
from mathutils import Vector,Matrix
R=Path(r'C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');B=Path(__file__).resolve().parents[1]
BASE=R/'05-Previs/Section-04_Cement-Casing-Integrity/Cinematic-Previs_v006/Scenes/S04_cinematic-previs_v006.blend'
RI=.1589405;RO=.1698625
SHAPES=json.loads((B/'Data/Section2-front-shapes.json').read_text())
sys.path.insert(0,str(R/'04-Production/Shared/Assets/Acoustics/Scripts'))
from acoustic_event_v002 import sample_native_event,validate_native_event
def mat(n,c,a=1):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,a);return m

def addmesh(n,v,faces,m):
 d=bpy.data.meshes.new(n);d.from_pydata(v,[],faces);d.update();o=bpy.data.objects.new(n,d);bpy.context.scene.collection.objects.link(o);d.materials.append(m);return o

def curve(n,pts,m,w=.00012):
 d=bpy.data.curves.new(n,'CURVE');d.dimensions='3D';d.resolution_u=1;d.bevel_depth=w;d.bevel_resolution=0;sp=d.splines.new('POLY');sp.points.add(len(pts)-1)
 for p,co in zip(sp.points,pts):p.co=(*co,1)
 o=bpy.data.objects.new(n,d);bpy.context.scene.collection.objects.link(o);d.materials.append(m);return o

def cube(n,p,size,m):
 h=size/2;verts=[tuple(Vector(p)+Vector((x*h,y*h,z*h))) for x,y,z in [(-1,-1,-1),(-1,-1,1),(-1,1,-1),(-1,1,1),(1,-1,-1),(1,-1,1),(1,1,-1),(1,1,1)]]
 return addmesh(n,verts,[(0,4,6,2),(1,3,7,5),(0,1,5,4),(2,6,7,3),(0,2,3,1),(4,5,7,6)],m)

def visibility(o,alphas):
 m=o.data.materials[0];rgb=list(m.diffuse_color[:3])
 for f,a in enumerate(alphas,1):
  m.diffuse_color=(*rgb,a);m.keyframe_insert('diffuse_color',frame=f);o.hide_render=a<.005;o.hide_viewport=o.hide_render;o.keyframe_insert('hide_render',frame=f);o.keyframe_insert('hide_viewport',frame=f)

def camera(eye,target,leftward=True,lens=45):
 cam=bpy.context.scene.camera;cam.animation_data_clear();cam.data.animation_data_clear();cam.data.lens=lens;cam.data.clip_start=.0005
 f=(Vector(target)-Vector(eye)).normalized();rad=Vector((0,1,0)) if not leftward else Vector((0,math.cos(math.radians(39)),math.sin(math.radians(39))))
 right=(rad-f*rad.dot(f)).normalized()*(-1 if leftward else 1);up=(-f).cross(right).normalized();q=Matrix((right,up,-f)).transposed().to_quaternion();cam.location=eye;cam.rotation_mode='QUATERNION';cam.rotation_quaternion=q;return cam

def fronts(e,tree):
 src=Vector(e['emitter_world_m']);hit=Vector(e['hit_world_m']);d=Vector(e['direction_world']);u=Vector((1,0,0));v=d.cross(u).normalized();L=(hit-src).length;checks=[]
 for role in ['SEND','ECHO']:
  sh=SHAPES[role];returning=role=='ECHO';direction=-d if returning else d
  pts=[u*p[0]+v*p[1]+direction*p[2] for p in sh['shape']]
  for k in range(3):
   m=mat('S02 '+role+str(k),tuple(sh['source_color'][:3]),0);o=curve('S02 sourced '+role+' front '+str(k),pts,m,sh['bevel']);o['source']=sh['source_object'];alph=[]
   for f in range(1,121):
    t=(f-1)/24;start=(1.2 if returning else .6)+k*.07;end=(1.8 if returning else 1.2)+k*.07;q=(t-start)/(end-start);distance=L*max(0,min(1,q));taper=max(0,min(1,distance/.006,(L-distance)/.006));o.location=hit-d*distance if returning else src+d*distance;o.scale=(taper,)*3
    o.keyframe_insert('location',frame=f);o.keyframe_insert('scale',frame=f);alph.append((.85 if returning else 1.)*(1-k*.16) if 0<=q<1 else 0)
    if 0<=q<1:
     for p in pts:
      w=o.location+p*taper
      assert (w-src).dot(d)>=-.00003 and (hit-w).dot(d)>=-.00003,'Front crosses cap or wall plane'
   visibility(o,alph)
   # Small source-style digital samples move with each front, not with backing.
   for j in range(2,len(pts)-2,4):
    node=cube('Fine S02 front sample',pts[j],.00028,m);node.parent=o
