import bpy,math,json,hashlib
from pathlib import Path
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
B=Path(__file__).resolve().parents[1];ROOT=B.parents[2];s=bpy.context.scene
s.frame_set(1);bpy.context.view_layer.update();hardware=list(bpy.data.collections['S05_LINKED_HARDWARE'].objects);base={o.name:o.matrix_world.copy() for o in hardware}
vv=[];ff=[]
for o in hardware:
 off=len(vv);vv.extend(o.matrix_world@v.co for v in o.data.vertices);ff.extend([[off+i for i in p.vertices] for p in o.data.polygons])
steel=BVHTree.FromPolygons(vv,ff);domain=bpy.data.objects['S05_v007_AnnularFluidDomain'];dv=[domain.matrix_world@v.co for v in domain.data.vertices];df=[list(p.vertices) for p in domain.data.polygons];fluid=BVHTree.FromPolygons(dv,df)
hits=steel.overlap(fluid);assert not hits,('domain steel overlap',len(hits))
minimum=1;radial=1;wall=1
for p in dv:
 minimum=min(minimum,steel.find_nearest(p)[3]);r=math.hypot(p.x,p.y);wall=min(wall,.155575-r);u=Vector((p.x/r,p.y/r,0));h=steel.ray_cast(Vector((0,0,p.z))+u*.18,-u,.18)[0]
 if h is not None:radial=min(radial,r-math.hypot(h.x,h.y))
assert min(minimum,radial,wall)>0,(minimum,radial,wall)
rockmin=1;rockwall=1;insidefluid=1;rockintersections=[];times=[1+i*.5 for i in range(191)]
cam_base=s.camera.matrix_world.copy();camera_change=0
rocks=list(bpy.data.collections['S05_TRACKED_COHORT_v010'].objects)+list(bpy.data.collections['S05_INTERNAL_WISPS_v010'].objects)
for f in times:
 s.frame_set(int(f),subframe=f-int(f));bpy.context.view_layer.update();expected=Matrix.Rotation(-math.radians(5)*(f-1)/24,4,'Z');inverse=expected.inverted()
 assert max(abs(domain.matrix_world[i][j]-expected[i][j]) for i in range(4) for j in range(4))<1e-6
 for o in hardware:assert max(abs(o.matrix_world[i][j]-(expected@base[o.name])[i][j]) for i in range(4) for j in range(4))<1e-6
 camera_change=max(camera_change,max(abs(s.camera.matrix_world[i][j]-cam_base[i][j]) for i in range(4) for j in range(4)))
 dg=bpy.context.evaluated_depsgraph_get()
 for o in rocks:
  assert o.parent is None;ev=o.evaluated_get(dg);me=ev.to_mesh();pv=[inverse@ev.matrix_world@v.co for v in me.vertices];pf=[list(p.vertices) for p in me.polygons];ev.to_mesh_clear();rtree=BVHTree.FromPolygons(pv,pf);h=steel.overlap(rtree);fh=fluid.overlap(rtree)
  if h or fh:rockintersections.append({'frame':f,'object':o.name,'steel_pairs':len(h),'fluid_boundary_pairs':len(fh)})
  for p in pv:
   r=math.hypot(p.x,p.y);u=Vector((p.x/r,p.y/r,0));h=fluid.ray_cast(Vector((0,0,p.z)),u,.17)[0];assert h is not None
   insidefluid=min(insidefluid,r-math.hypot(h.x,h.y),.154575-r,p.z+.45,1.05-p.z)
   rockmin=min(rockmin,steel.find_nearest(p)[3]);rockwall=min(rockwall,.155575-r)
assert not rockintersections,rockintersections
assert insidefluid>0,(insidefluid,rockmin,rockwall)
prior=B.parent/'Interaction-Proof_v008/Scenes/S05_internal-flow_v008.blend';source=ROOT/'04-Production/Shared/Assets/ECCO/ECCO_film_v002.blend'
assert hashlib.sha256(prior.read_bytes()).hexdigest()=='0c3e0864eab93105494fe1790ff9f8a1bf97ab024fcb60b6387e6b4e8df6ac4f'
assert hashlib.sha256(source.read_bytes()).hexdigest()=='df656a5c4bc48f081a4b6365c7969df55d15c7da53ddb96be20875e931d26584'
result={'time_samples':len(times),'domain_triangle_intersections':len(hits),'domain_vertices_checked':len(dv),'minimum_domain_steel_distance_m':minimum,'minimum_domain_radial_exterior_m':radial,'minimum_domain_wall_gap_m':wall,'moving_element_intersections':rockintersections,'minimum_moving_element_steel_distance_m':rockmin,'minimum_moving_element_wall_gap_m':rockwall,'minimum_moving_element_fluid_boundary_gap_m':insidefluid,'camera_matrix_max_change':camera_change,'hardware_and_domain_common_rigid_rotation_verified':True,'source_and_v008_hash_unchanged':True,'domain_method':'Complete static triangle and all-vertex exterior checks; common rigid rotation preserves steel/domain separation. Cylinder radius and axial limits are invariant. Fluid field and rocks move independently of this boundary.','moving_elements_method':'Full triangle and all-vertex steel/fluid containment checks at 96 output frames and 95 halfway samples; not a guarantee at every unsampled instant.','limits':'Geometric verification only; no CFD or measured performance claim.'}
(B/'Records/geometry-verification.json').write_text(json.dumps(result,indent=2));s.frame_set(36)
