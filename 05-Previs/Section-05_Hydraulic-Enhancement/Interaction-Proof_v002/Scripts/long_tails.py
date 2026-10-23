"""Owner amendment: tapered moving tails preserve the visible flow pattern.
Current-time constrained streamlet tails, not literal fluid histories or CFD.
"""
import bpy,math,json,time
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
B=Path(__file__).resolve().parents[1];s=bpy.context.scene
assert 'v002' in bpy.data.filepath
s.frame_set(1);bpy.context.view_layer.update()
vv=[];ff=[]
for o in bpy.data.collections['S05_LINKED_HARDWARE'].objects:
 off=len(vv);vv.extend(o.matrix_world@v.co for v in o.data.vertices);ff.extend([[off+i for i in p.vertices] for p in o.data.polygons])
tree=BVHTree.FromPolygons(vv,ff);OMEGA=-math.radians(5);R=.155575
src=(B/'Scripts/revise.py').read_text()
exec(src[src.index('def rot('):src.index('random.seed(123)')])
fx=bpy.data.collections['S05_DYNAMIC_FLOW_v002']
for o in list(fx.objects):
 if 'FluidPacket' in o.name:o.hide_render=True;o.hide_viewport=True
tails=bpy.data.collections.new('S05_MOVING_TAPERED_TAILS_v002');s.collection.children.link(tails)
mat=bpy.data.materials['S05_v002_AmberFluid']
particles=json.loads((B/'Records/particle-tracks.json').read_text())
NR=41;SIDES=6;lowest=10;records=[]
for i,p in enumerate(particles):
 length=.19 if p['kind']=='fluid' else .115
 radius=.00115 if p['kind']=='fluid' else .00062
 states=[]
 for f,pos in enumerate(p['frames'],1):
  t=(f-1)/24;pt=Vector(pos);points=[pt.copy()]
  # Head follows the advected centre; tail bends through current pad clearance.
  for j in range(1,NR):
   try:
    for step in range(3):
     tangent=velocity(pt,t,p['lane'],radius).normalized()
     pt=constrain(pt-tangent*length/(NR-1)/3,t,radius)
   except AssertionError:
    break # Shorten at a constrained corner; never force a tail through steel.
   points.append(pt.copy())
  if len(points)<NR:
   assert len(points)>1
   original_points=points
   points=[]
   for j in range(NR):
    q=j/(NR-1)*(len(original_points)-1);a=min(len(original_points)-2,int(q))
    points.append(original_points[a].lerp(original_points[a+1],q-a))
  vertices=[]
  for j,pt in enumerate(points):
   tangent=(points[min(NR-1,j+1)]-points[max(0,j-1)]).normalized()
   u=tangent.cross(Vector((0,0,1)))
   if u.length<.01:u=tangent.cross(Vector((1,0,0)))
   u.normalize();v=tangent.cross(u).normalized()
   # Thin, tapered geometry; no bloom, no opaque band between adjacent paths.
   taper=(1-j/(NR-1))**.8
   edge=min(smooth((pt.z+.28)/.07),smooth((.94-pt.z)/.07))
   rr=radius*(.03+.97*taper)*edge
   co,n,d=nearest(pt,t);lowest=min(lowest,d-rr)
   for k in range(SIDES):vertices.append(pt+rr*(u*math.cos(k*math.tau/SIDES)+v*math.sin(k*math.tau/SIDES)))
  states.append(vertices)
 faces=[(j*SIDES+k,j*SIDES+(k+1)%SIDES,(j+1)*SIDES+(k+1)%SIDES,(j+1)*SIDES+k) for j in range(NR-1) for k in range(SIDES)]
 me=bpy.data.meshes.new(f'S05_TailMesh_{i:02}');me.from_pydata(states[0],[],faces);me.materials.append(mat)
 o=bpy.data.objects.new(f'S05_v002_{p["kind"]}_Tail_{i:02}',me);tails.objects.link(o)
 for poly in me.polygons:poly.use_smooth=True
 o.shape_key_add(name='Basis');me.shape_keys.use_relative=False
 for f,vertices in enumerate(states[1:],2):
  key=o.shape_key_add(name=f'Frame_{f:03}')
  for v,co in zip(key.data,vertices):v.co=co
 for key in me.shape_keys.key_blocks:key.interpolation='KEY_LINEAR'
 for f in [1,144]:me.shape_keys.eval_time=(f-1)*10;me.shape_keys.keyframe_insert('eval_time',frame=f)
 for layer in me.shape_keys.animation_data.action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for fc in bag.fcurves:
     for k in fc.keyframe_points:k.interpolation='LINEAR'
 o['tail_meaning']='Tapered current-time constrained direction trace behind advected element; not literal streakline history'
 records.append({'object':o.name,'kind':p['kind'],'length_m':length,'head_radius_m':radius})
s.frame_set(72);s.render.filepath='//../Work/Frames/S05_'
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
result={'tails':records,'sampled_center_clearance_minus_radius_m':lowest,'owner_amendment':'Retain v001 pattern through long tapered tails attached to moving elements; world-space geometry recomputed around rotating pads'}
(B/'Records/long-tails.json').write_text(json.dumps(result,indent=2))
