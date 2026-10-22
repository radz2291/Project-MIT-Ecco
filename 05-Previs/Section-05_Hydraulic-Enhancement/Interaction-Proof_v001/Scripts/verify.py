import bpy,json,math,hashlib
from pathlib import Path
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
B=Path(__file__).resolve().parents[1];ROOT=B.parents[2];s=bpy.context.scene
hardware=list(bpy.data.collections['S05_LINKED_HARDWARE'].objects);vv=[];ff=[]
for o in hardware:
 off=len(vv);vv.extend(o.matrix_world@v.co for v in o.data.vertices);ff.extend([off+i for i in p.vertices] for p in o.data.polygons)
tree=BVHTree.FromPolygons(vv,ff);T=Matrix.Translation((0,0,1.5))@Matrix.Rotation(math.pi/2,4,'Y')
paths=json.loads((B/'Records/paths.json').read_text());minimum=1;wallminimum=1
max_support=0
for o in bpy.data.collections['S05_ILLUSTRATIVE_FLOW'].objects:
 if 'Cutting' in o.name:max_support=max(max_support,max(v.co.length for v in o.data.vertices))
 if 'Tracer' in o.name:max_support=max(max_support,math.hypot(.006,o.data.bevel_depth))
for pp in paths:
 for a,b in zip(pp,pp[1:]):
  for u in [0,.25,.5,.75]:
   p=Vector(a).lerp(Vector(b),u);world=T@p;dist=tree.find_nearest(world)[3]
   # Nearest-distance bound minus whole-effect support covers entire finite mesh.
   minimum=min(minimum,dist-max_support);wallminimum=min(wallminimum,.155575-math.hypot(p.y,p.z)-max_support)
   radial=Vector((world.x,world.y,0)).normalized();hit=tree.ray_cast(Vector((0,0,world.z))+radial*.18,-radial,.18)[0]
   if hit is not None:assert math.hypot(world.x,world.y)>math.hypot(hit.x,hit.y)
assert minimum>0 and wallminimum>0
baseline={o.name:[list(r) for r in o.matrix_world] for o in hardware};stationary=True
for f in range(1,145):
 s.frame_set(f);bpy.context.view_layer.update()
 stationary &= all([list(r) for r in o.matrix_world]==baseline[o.name] for o in hardware)
assert stationary
libs=[{'path':bpy.path.abspath(l.filepath),'exists':Path(bpy.path.abspath(l.filepath)).exists()} for l in bpy.data.libraries]
assert all(l['exists'] for l in libs)
source=ROOT/'04-Production/Shared/Assets/ECCO/ECCO_film_v002.blend'
report={'finite_effect_support_m':max_support,'min_conservative_hardware_clearance_m':minimum,'min_conservative_wall_clearance_m':wallminimum,'centre_samples':21600,'method':'All visible hardware triangles; dense polyline quarter-segment samples; nearest distance minus full tracer/rock bounding sphere. Centre raycast confirms exterior. No fluid solver or collision-response physics claimed.','all_144_frames_stationary_hardware':stationary,'libraries':libs,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'source_hash_unchanged':hashlib.sha256(source.read_bytes()).hexdigest()==json.loads((B/'Records/build.json').read_text())['sha256']}
(B/'Records/geometry-verification.json').write_text(json.dumps(report,indent=2));s.frame_set(72);result=report
