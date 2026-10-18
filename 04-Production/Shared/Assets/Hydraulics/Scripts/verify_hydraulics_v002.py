"""T48v007 resume / preflight5: full finite slab, clipped faces, actual pose.

No rendering/writes to native candidates. Every hardware triangle whose surface
intersects the whole finite display envelope participates in the radial proof.
"""
import bpy,sys,json,hashlib,math,struct
from pathlib import Path
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[4];TASK=ROOT/'04-Production/Records/Tasks/T-048';S=TASK/'Scenes';E=TASK/'Evidence'
sys.path.insert(0,str(HERE));from migrate_continuity_v007 import resolve_library,libraries,sha
from build_hydraulics_v001 import snapshot
EPS=1e-6
def dump(name,data):(E/name).write_text(json.dumps(data,indent=2),encoding='utf-8')
def flat(m):return [float(v) for row in m for v in row]
def close(a,b,tol=2e-6):return max(abs(x-y) for x,y in zip(flat(a),flat(b)))<tol
def clip_x(poly,bound,lower):
 out=[]
 if not poly:return out
 for a,b in zip(poly,poly[1:]+poly[:1]):
  ia=a[0]>=bound if lower else a[0]<=bound;ib=b[0]>=bound if lower else b[0]<=bound
  if ia:out.append(a)
  if ia!=ib:
   t=(bound-a[0])/(b[0]-a[0]);out.append(tuple(a[j]+t*(b[j]-a[j]) for j in range(3)))
 return out
def slab(poly,lo,hi):return clip_x(clip_x(poly,lo,True),hi,False)
def geometry_ids(collection,seen=None):
 seen=set() if seen is None else seen;result=set()
 if collection.as_pointer() in seen:return result
 seen.add(collection.as_pointer())
 for o in collection.objects:
  if o.type=='MESH':result.add(o.as_pointer())
  if o.instance_type=='COLLECTION' and o.instance_collection:result.update(geometry_ids(o.instance_collection,seen))
 for c in collection.children:result.update(geometry_ids(c,seen))
 return result
def housing_matrix(dep):
 matrices=[i.matrix_world.copy() for i in dep.object_instances if i.object.original.name=='ECCO_HOUSING_SOURCE_MESH'];assert len(matrices)==1,len(matrices);return matrices[0]
def eval_points(o,dep,inverse):
 q=o.evaluated_get(dep);m=q.to_mesh();T=inverse@q.matrix_world;points=[T@v.co for v in m.vertices];q.to_mesh_clear();return points
def verify(kind):
 p=S/('Flow_reuse_'+kind+'_v006.blend');bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False,use_scripts=False);s=bpy.context.scene;s.frame_set(1);dep=bpy.context.evaluated_depsgraph_get();ctrl=bpy.data.objects['FLOW_CONTROL'];flow=bpy.data.objects['FLOW_PLACEMENT'];hw=bpy.data.objects['WORLD_HARDWARE_INSTANCE'];H=hw.evaluated_get(dep).matrix_world.copy();Hi=H.inverted();source_housing_basis=bpy.data.objects['ECCO_HOUSING_SOURCE_MESH'].matrix_world.copy();old_snapshot=snapshot()
 # The original imported mesh retains its immutable millimetre-to-metre0.001
 # object conversion. Registration uses the unscaled assembly rigid frame.
 assert close(housing_matrix(dep),H@source_housing_basis)
 assert close(H,flow.evaluated_get(dep).matrix_world)
 assert abs(H.to_3x3().determinant()-1)<1e-5 and all(abs(H.to_scale()[j]-1)<1e-6 for j in range(3))
 assert s.unit_settings.scale_length==1 and abs(ctrl['speed'])>0
 deps=libraries();assert all(x['path'].startswith('//') and Path(x['resolved']).exists() for x in deps)
 assert any(Path(x['resolved']).name=='BHA_film_v007.blend' and x['parent'] is None and x['sha256']=='b6b98f870064f5b9e07640bec9dadaeb457c7e45ebdb5d33d2ac18b6210acdd1' for x in deps)
 assert any(Path(x['resolved']).name=='BHA_film_v006.blend' and x['parent'] and Path(x['parent']).name=='BHA_film_v007.blend' for x in deps)
 roots={role:bpy.data.objects[name] for role,name in [('hardware','WORLD_HARDWARE_INSTANCE'),('extension','WORLD_UPHOLE_EXTENSION_INSTANCE'),('joint','WORLD_UPHOLE_JOINT_INSTANCE')]}
 assert roots['extension'].parent==roots['joint'].parent==hw
 assert abs(bpy.data.objects['UPHOLE_CONTINUATION_CONTROL']['length_m']-12)<1e-9
 role_ids={role:geometry_ids(o.instance_collection) for role,o in roots.items()}
 paths=sorted([o for o in s.objects if o.name.startswith('FLOW_FLOW_PATH_')],key=lambda o:o.name);cuts=[o for o in s.objects if o.name.startswith('FLOW_CUTTING_')];tracers=[o for o in s.objects if o.name.startswith('FLOW_TRACER_') and o.type=='MESH'];moving=cuts+tracers
 assert len(paths)==10 and len(cuts)==30 and len(tracers)==20
 assert all(o.data.library for o in paths+moving)
 nodes=[];angles=[];bevel=max(o.data.bevel_depth for o in paths)
 for o in paths:
  T=Hi@o.matrix_world;ps=[T@Vector(pt.co[:3]) for spl in o.data.splines for pt in spl.points];nodes.extend(ps)
  for a,b in zip(ps,ps[1:]):angles.append(abs(math.atan2(a.y*b.z-a.z*b.y,a.y*b.y+a.z*b.z)))
 node_r=[math.hypot(v.y,v.z) for v in nodes];assert max(node_r)-min(node_r)<2e-7
 axial=max(bevel,max(abs(v.co.x) for o in moving for v in o.data.vertices))
 matte_radial=max(math.hypot(v.co.y,v.co.z) for o in cuts for v in o.data.vertices)
 tracer_radial=max(math.hypot(v.co.y,v.co.z) for o in tracers for v in o.data.vertices)
 finite_lo=min(v.x for v in nodes)-axial-EPS;finite_hi=max(v.x for v in nodes)+axial+EPS
 node_lower=min(node_r)*math.cos(max(angles)/2)-EPS;node_upper=max(node_r)+EPS
 # Regression witness: all triangle vertices lie outside the slab, but its face crosses it.
 witness=[(finite_lo-1,.12,0),(finite_hi+1,.12,0),(finite_hi+1,.12,.01)]
 clipped=slab(witness,finite_lo,finite_hi);assert clipped and all(finite_lo-1e-9<=v[0]<=finite_hi+1e-9 for v in clipped)
 records=[];hardware_max=0;hardware_bvh=[];walls=[];wall_planes=[];role_counts={k:0 for k in roots};crossing=0
 # Every current hardware object is enumerated by collection provenance, not its name.
 for inst in dep.object_instances:
  o=inst.object;original=o.original;roles=[r for r,ids in role_ids.items() if original.as_pointer() in ids]
  wall=original.name in ['NOMINAL_CUTAWAY','FORMATION_NOMINAL_CUTAWAY']
  if o.type!='MESH' or (not roles and not wall):continue
  if roles and o.hide_render:
   records.append(dict(object=original.name,roles=roles,selection='hidden_source_helper_excluded',reason='Source object.hide_render is true'));continue
  m=o.to_mesh();m.calc_loop_triangles();T=Hi@inst.matrix_world;pts=[T@v.co for v in m.vertices];triangles=[tuple(t.vertices) for t in m.loop_triangles];o.to_mesh_clear()
  if roles:
   for r in roles:role_counts[r]+=1
   xlo=min(v.x for v in pts);xhi=max(v.x for v in pts);rec=dict(object=original.name,library=str(resolve_library(original.library)) if original.library else None,roles=roles,vertices=len(pts),triangles=len(triangles),x_bounds=[xlo,xhi],selected_faces=0,crossing_faces_all_vertices_outside=0,radial_bound_m=None)
   if xhi<finite_lo or xlo>finite_hi:rec['selection']='whole_object_x_aabb_disjoint';records.append(rec);continue
   local_max=0
   for face in triangles:
    poly=[tuple(pts[j]) for j in face]
    if max(v[0] for v in poly)<finite_lo or min(v[0] for v in poly)>finite_hi:continue
    clipped=slab(poly,finite_lo,finite_hi)
    if not clipped:continue
    rec['selected_faces']+=1
    if all(v[0]<finite_lo or v[0]>finite_hi for v in poly):rec['crossing_faces_all_vertices_outside']+=1;crossing+=1
    local_max=max(local_max,max(math.hypot(v[1],v[2]) for v in clipped))
   rec['selection']='all_intersecting_triangles_clipped_to_full_finite_x_slab';rec['radial_bound_m']=local_max;hardware_max=max(hardware_max,local_max);records.append(rec)
   hardware_bvh.append(BVHTree.FromPolygons(pts,triangles,all_triangles=True))
  if wall:
   walls.append(BVHTree.FromPolygons(pts,triangles,all_triangles=True))
   for face in triangles:
    poly=[tuple(pts[j]) for j in face]
    if not slab(poly,finite_lo,finite_hi):continue
    a,b,c=[pts[j] for j in face];cent=(a+b+c)/3;rr=math.hypot(cent.y,cent.z);n=(b-a).cross(c-a)
    if n.length<1e-12:continue
    n.normalize();radial=math.hypot(n.y,n.z)
    if .14<rr<.16 and abs(n.x)<.05 and abs(n.y*cent.y+n.z*cent.z)>rr*.9:
     D=n.dot(cent);ds=[abs(D-n.x*x)/radial for x in [finite_lo,finite_hi]]
     if abs(n.x)>1e-12 and finite_lo<=D/n.x<=finite_hi:ds.append(0)
     wall_planes.append(min(ds))
 assert role_counts['extension']==1 and role_counts['joint']==1,role_counts
 assert hardware_bvh and walls and wall_planes
 wall_lower=min(wall_planes)-EPS;hardware_max+=EPS
 finite_radius=max(matte_radial,tracer_radial,bevel)
 inner=node_lower-finite_radius-hardware_max;outer=wall_lower-node_upper-finite_radius
 assert inner>0 and outer>0,(inner,outer,hardware_max,wall_lower)
 # Matrices/finite mesh extrema are evaluated in the actual housing frame.
 ctrl['density']=10;ctrl['stage_emphasis']=0;ctrl.update_tag();ranges=dict(xlo=1e9,xhi=-1e9,rlo=1e9,rhi=0);nearest_hw=1e9;nearest_wall=1e9;motion=[];rigid_checks=0;finite_vertices=0
 for f in range(s.frame_start,s.frame_end+1):
  s.frame_set(f);dep=bpy.context.evaluated_depsgraph_get();currentH=hw.evaluated_get(dep).matrix_world;assert close(currentH,H) and close(currentH,flow.evaluated_get(dep).matrix_world) and close(housing_matrix(dep),currentH@source_housing_basis);rigid_checks+=1
  for o in moving:
   q=o.evaluated_get(dep);R=(Hi@q.matrix_world).to_3x3()
   assert all(abs(R[i][j])<1e-6 for i in range(3) for j in range(3) if i!=j)
   assert all(.8499<=R[i][i]<=1.0001 for i in range(3))
   ps=eval_points(o,dep,Hi)
   for v in ps:
    rr=math.hypot(v.y,v.z);ranges['xlo']=min(ranges['xlo'],v.x);ranges['xhi']=max(ranges['xhi'],v.x);ranges['rlo']=min(ranges['rlo'],rr);ranges['rhi']=max(ranges['rhi'],rr);finite_vertices+=1
    assert finite_lo-EPS<=v.x<=finite_hi+EPS and node_lower-finite_radius-EPS<=rr<=node_upper+finite_radius+EPS
    if f in [1,s.frame_end//2,s.frame_end]:
     nearest_hw=min(nearest_hw,*(bv.find_nearest(v)[3] for bv in hardware_bvh));nearest_wall=min(nearest_wall,*(bv.find_nearest(v)[3] for bv in walls))
  motion.append(list((Hi@cuts[0].evaluated_get(dep).matrix_world.translation)))
 for o in paths:
  for v in eval_points(o,dep,Hi):
   rr=math.hypot(v.y,v.z);assert node_lower-bevel-EPS<=rr<=node_upper+bevel+EPS and finite_lo<=v.x<=finite_hi
   finite_vertices+=1
 # Old controls remain functional, including particles and directional dashes.
 ctrl['speed']=0;ctrl.update_tag();s.frame_set(23);a=cuts[0].evaluated_get(bpy.context.evaluated_depsgraph_get()).matrix_world.translation.copy();s.frame_set(37);b=cuts[0].evaluated_get(bpy.context.evaluated_depsgraph_get()).matrix_world.translation.copy();assert (a-b).length<1e-6
 ctrl['phase']+=.2;ctrl.update_tag();s.frame_set(38);c=cuts[0].evaluated_get(bpy.context.evaluated_depsgraph_get()).matrix_world.translation.copy();assert (c-b).length>.05
 ctrl['operating_mode']=1;ctrl.update_tag();s.frame_set(39);assert all(o.evaluated_get(bpy.context.evaluated_depsgraph_get()).hide_render for o in paths+moving)
 # Read material node state after fresh-open: transient reload warnings are not ignored.
 materials=[]
 for mat in bpy.data.materials:
  if mat.library:
   assert mat.node_tree is not None
   materials.append(dict(name=mat.name,library=str(resolve_library(mat.library)),node_count=len(mat.node_tree.nodes)))
 migration=json.loads((E/('continuity_'+kind+'_migration_v007.json')).read_text());assert migration['preserved_old_controls_camera_timing_animation'] and migration['rigid_registration_preserved']
 record=dict(path=str(p.relative_to(ROOT)).replace('\\','/'),sha256=sha(p),accepted_base='a08d0ecfbd6f3241298f506b3ea42613388b3baf',libraries=deps,snapshot=old_snapshot,one_ecco=True,one_extension=True,one_joint=True,registered_housing_matrix=flat(H),all_frames_rigid_registration_checks=rigid_checks,full_finite_envelope_x_housing_m=[finite_lo,finite_hi],centre_nodes_x_m=[min(v.x for v in nodes),max(v.x for v in nodes)],max_shape_axial_extent_m=axial,full_shape_radial_extent_m=finite_radius,path_angular_step_max_rad=max(angles),guide_radius_lower_m=node_lower,guide_radius_upper_m=node_upper,actual_hardware_clipped_radial_bound_m=hardware_max,actual_wall_facet_radius_lower_m=wall_lower,continuous_complete_shape_hardware_clearance_m=inner,continuous_complete_shape_wall_clearance_m=outer,finite_mesh_sample_extrema=ranges,all_frame_finite_vertices=finite_vertices,nearest_actual_hardware_peak_vertex_m=nearest_hw,nearest_actual_wall_peak_vertex_m=nearest_wall,covered_hardware_meshes=records,hardware_roles_enumerated=role_counts,faces_crossing_slab_with_all_vertices_outside=crossing,clip_regression_witness=dict(all_vertices_outside=True,clipped_surface=clipped if False else slab(witness,finite_lo,finite_hi),included=True),linked_materials_fresh_open=materials,first_particle_housing_frame_motion=motion[::12],control_probes=dict(speed_zero=True,phase=True,mode_off_hides_all=True),source_housing_mesh_hash=hashlib.sha256(b''.join(struct.pack('3f',*v.co) for v in bpy.data.objects['ECCO_HOUSING_SOURCE_MESH'].data.vertices)).hexdigest(),limits='Illustrative centred nominal pose only, every frame static rigid source registration. All relevant hardware provenance enumerated; triangle/slab intersection includes crossing faces and finite axial support. Floating guard1micrometre applied. No CFD/pressure/wake/transport validation; physical end/functional stage mapping remains unverified.')
 dump('Flow_reuse_'+kind+'_v006_fresh-open_v002.json',record);return record
if __name__=='__main__':
 rows=[verify(k) for k in ['A','B']]
 assert rows[0]['source_housing_mesh_hash']==rows[1]['source_housing_mesh_hash']
 dump('native-verification-summary_v007.json',dict(all_checks_pass=True,preflight_item5_repaired=True,method='Collection provenance -> complete finite X slab from actual linked shapes -> triangle clipping -> conservative radial bound; all frames actual pose/finite meshes checked',consumers=[dict(path=r['path'],sha256=r['sha256']) for r in rows]))
 print('T48_V007_FINITE_FACE_NATIVE_PASS')
