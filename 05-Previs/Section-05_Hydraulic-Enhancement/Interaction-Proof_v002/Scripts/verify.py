import bpy,math,json,hashlib
from pathlib import Path
from mathutils import Matrix,Vector
from mathutils.bvhtree import BVHTree
B=Path(__file__).resolve().parents[1];ROOT=B.parents[2];s=bpy.context.scene
s.frame_set(1);bpy.context.view_layer.update()
hardware=list(bpy.data.collections['S05_LINKED_HARDWARE'].objects)
root=bpy.data.objects['S05_COMMON_AXIAL_ROTATION'];baseline={o.name:o.matrix_world.copy() for o in hardware}
vv=[];ff=[]
for o in hardware:
 off=len(vv);vv.extend(o.matrix_world@v.co for v in o.data.vertices);ff.extend([[off+i for i in p.vertices] for p in o.data.polygons])
tree=BVHTree.FromPolygons(vv,ff)
fx=list(bpy.data.collections['S05_MOVING_TAPERED_TAILS_v002'].objects)+[o for o in bpy.data.collections['S05_DYNAMIC_FLOW_v002'].objects if 'Rock_' in o.name]
minimum=10;wall=10;overlaps=[];samples=0;radialminimum=10;signedminimum=10
for f in range(1,145):
 s.frame_set(f);bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get()
 expected=Matrix.Rotation(-math.radians(5)*(f-1)/24,4,'Z')
 assert root.location.length==0
 for o in hardware:
  assert o.parent==root
  assert max(abs((expected@baseline[o.name])[i][j]-o.matrix_world[i][j]) for i in range(4) for j in range(4))<1e-6
 inverse=expected.inverted();verts=[];faces=[]
 for o in fx:
  assert o.parent is None
  ev=o.evaluated_get(dg);me=ev.to_mesh();off=len(verts)
  pts=[inverse@ev.matrix_world@v.co for v in me.vertices];verts.extend(pts)
  faces.extend([[off+i for i in p.vertices] for p in me.polygons])
  for p in pts[::3]:
   co,n,idx,d=tree.find_nearest(p);minimum=min(minimum,d);signedminimum=min(signedminimum,(p-co).dot(n));r=math.hypot(p.x,p.y);wall=min(wall,.155575-r);samples+=1
   u=Vector((p.x/r,p.y/r,0));hit=tree.ray_cast(Vector((0,0,p.z))+u*.18,-u,.18)[0]
   if hit is not None:radialminimum=min(radialminimum,r-math.hypot(hit.x,hit.y))
  ev.to_mesh_clear()
 flowtree=BVHTree.FromPolygons(verts,faces);hits=tree.overlap(flowtree)
 if hits:overlaps.append({'frame':f,'pairs':len(hits)})
libs=[{'path':bpy.path.abspath(l.filepath),'relative':l.filepath.startswith('//'),'exists':Path(bpy.path.abspath(l.filepath)).exists()} for l in bpy.data.libraries]
source=ROOT/'04-Production/Shared/Assets/ECCO/ECCO_film_v002.blend'
old=B.parent/'Interaction-Proof_v001/Scenes/S05_twisted-pad_interaction_v001.blend'
result={'frames_checked':144,'effect_objects':len(fx),'triangle_intersections':overlaps,'sampled_vertices':samples,'minimum_sampled_hardware_distance_m':minimum,'minimum_radial_exterior_gap_m':radialminimum,'raw_nearest_normal_signed_min_m':signedminimum,'normal_caveat':'Nearest face normals give ambiguous sign on the supplied CAD. Exterior tested separately by radial first-hit checks, and triangle intersections tested across complete effect meshes.','minimum_sampled_wall_clearance_m':wall,'all_hardware_rigid_rotation_verified':True,'no_axial_translation':True,'clockwise_surface_view':'negative world Z, inherited +Z surface / -Z downhole mapping','hardware_wall_gap_m':.155575-max(math.hypot(v.x,v.y) for v in vv),'libraries':libs,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'v001_sha256':hashlib.sha256(old.read_bytes()).hexdigest(),'limits':'Triangle overlap tests and every-third-vertex nearest-surface plus radial exterior checks at all 144 rendered frames. Subframe interpolation not certified; no CFD or engineering acceptance.'}
(B/'Records/geometry-verification.json').write_text(json.dumps(result,indent=2))
assert not overlaps,result
assert minimum>0 and wall>0 and radialminimum>0
assert all(l['exists'] and l['relative'] for l in libs)
assert result['source_sha256']=='df656a5c4bc48f081a4b6365c7969df55d15c7da53ddb96be20875e931d26584'
assert result['v001_sha256']=='ce359c8ae096e022f53414482f49665cf7dc6a27f37c7010646a0df55860ddb6'
s.frame_set(72)
