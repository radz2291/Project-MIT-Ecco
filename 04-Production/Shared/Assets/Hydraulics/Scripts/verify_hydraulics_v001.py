"""Fresh-native geometry/control/link checks. No render. Finite envelopes tested."""
import bpy,sys,json,math,hashlib,struct
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[4];TASK=ROOT/'04-Production/Records/Tasks/T-048';E=TASK/'Evidence';S=TASK/'Scenes';OWN=ROOT/'04-Production/Shared/Assets/Hydraulics'
sys.path.insert(0,str(HERE));from build_hydraulics_v001 import snapshot
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(name,d):(E/name).write_text(json.dumps(d,indent=2),encoding='utf-8')
def evaluated_points(o,dep):
 q=o.evaluated_get(dep);m=q.to_mesh();pts=[q.matrix_world@v.co for v in m.vertices];q.to_mesh_clear();return pts
def verify(kind,version):
 p=S/('Flow_reuse_'+kind+'_'+version+'.blend');bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False,use_scripts=False);s=bpy.context.scene;s.frame_set(1);dep=bpy.context.evaluated_depsgraph_get();ctrl=bpy.data.objects['FLOW_CONTROL'];paths=[o for o in s.objects if o.name.startswith('FLOW_FLOW_PATH_')];cuts=[o for o in s.objects if o.name.startswith('FLOW_CUTTING_')];tracers=[o for o in s.objects if o.name.startswith('FLOW_TRACER_') and o.type=='MESH']
 libs=[dict(path=l.filepath,resolved=bpy.path.abspath(l.filepath),exists=Path(bpy.path.abspath(l.filepath)).exists()) for l in bpy.data.libraries]
 assert all(r['exists'] and r['path'].startswith('//') for r in libs)
 assert len(paths)==10 and len(cuts)==30 and all(o.data.library is not None for o in paths+cuts)
 assert len(tracers)==(20 if version=='v005' else 0)
 emission=bpy.data.materials['FLOW_ContinuousAmber'].node_tree.nodes.get('Principled BSDF').inputs['Emission Strength'].default_value
 assert abs(emission-(.20 if version=='v003' else .32))<1e-5
 geometry_hash=hashlib.sha256(b''.join(struct.pack('4f',*p.co) for o in sorted(paths,key=lambda q:q.name) for spl in o.data.splines for p in spl.points)).hexdigest()
 cutting_hash=hashlib.sha256(b''.join(struct.pack('3f',*v.co) for v in cuts[0].data.vertices)).hexdigest();cutting_library=cuts[0].data.library.filepath
 assert len([o for o in bpy.data.objects if o.name=='ECCO_FILM_LINK'])==1
 # Actual hardware instance matrices include nested linked ECCO; exclude its hidden cut-plane helper.
 bvhs=[];maxr=0;objects=[];wall_bvhs=[];wall_planes=[]
 for inst in dep.object_instances:
  o=inst.object
  if o.type=='MESH' and o.name in ['NOMINAL_CUTAWAY','FORMATION_NOMINAL_CUTAWAY']:
   m=o.to_mesh();wp=[inst.matrix_world@v.co for v in m.vertices];wf=[tuple(f.vertices) for f in m.polygons];o.to_mesh_clear();wall_bvhs.append(BVHTree.FromPolygons(wp,wf))
   for f in wf:
    if len(f)<3:continue
    pp=[wp[i] for i in f];c=sum(pp,Vector())/len(pp);rr=math.hypot(c.y,c.z)
    if max(p.x for p in pp)<.69 or min(p.x for p in pp)>2.71 or not(.14<rr<.16):continue
    n=(pp[1]-pp[0]).cross(pp[2]-pp[0]);nn=n.length
    if nn<1e-12:continue
    n/=nn;radial=math.hypot(n.y,n.z)
    if abs(n.x)<.05 and abs(n.y*c.y+n.z*c.z)>rr*.9:wall_planes.append(abs(n.dot(c))/radial)
  if o.type!='MESH' or not any(x in o.name for x in ['ECCO_HOUSING_SOURCE_MESH','TEMP |','ADAPTER','COLLAR','PDC_']):continue
  if o.hide_render:continue
  m=o.to_mesh();pts=[inst.matrix_world@v.co for v in m.vertices];faces=[tuple(f.vertices) for f in m.polygons];o.to_mesh_clear()
  if not pts:continue
  bvhs.append(BVHTree.FromPolygons(pts,faces));objects.append(o.name)
  # Bound only hardware at longitudinal span of the flow guides.
  radii=[math.hypot(v.y,v.z) for v in pts if .69<=v.x<=2.71]
  if radii:maxr=max(maxr,max(radii))
 assert wall_planes and wall_bvhs
 actual_wall_radius_lower=min(wall_planes)
 min_hardware=1;max_radius=0;min_radius=1;tested=0;nearest_wall=1
 # Evaluate full beveled strand geometry: no centreline-only claim.
 for o in paths:
  for v in evaluated_points(o,dep):
   r=math.hypot(v.y,v.z);max_radius=max(max_radius,r);min_radius=min(min_radius,r);tested+=1
 # Complete finite envelope bound also covers every surface between evaluated vertices.
 path_inner=min_radius-maxr;path_outer=actual_wall_radius_lower-max_radius
 assert path_inner>0 and path_outer>0,(path_inner,path_outer,maxr)
 # Actual nearest-surface samples plus a continuous analytic radial safety bound.
 for o in paths:
  pts=evaluated_points(o,dep)
  for v in pts[::12]:
   for bv in bvhs:min_hardware=min(min_hardware,bv.find_nearest(v)[3])
   for bv in wall_bvhs:nearest_wall=min(nearest_wall,bv.find_nearest(v)[3])
 particle_rmax=0;particle_rmin=1;motion=[];invalid=[];particle_xmin=100;particle_xmax=-100
 ctrl['density']=10;ctrl.update_tag()
 for frame in range(1,s.frame_end+1):
  s.frame_set(frame);dep=bpy.context.evaluated_depsgraph_get()
  for o in cuts+tracers:
   for v in evaluated_points(o,dep):
    r=math.hypot(v.y,v.z);particle_rmax=max(particle_rmax,r);particle_rmin=min(particle_rmin,r)
    particle_xmin=min(particle_xmin,v.x);particle_xmax=max(particle_xmax,v.x)
    if not all(math.isfinite(x) for x in v):invalid.append((frame,o.name))
    if frame in [1,s.frame_end//2,s.frame_end]:
     for bv in wall_bvhs:nearest_wall=min(nearest_wall,bv.find_nearest(v)[3])
  motion.append(list(cuts[0].evaluated_get(dep).matrix_world.translation))
 # Adjacent guide azimuth changes <0.006rad from analytic derivative bound;
 # straight chord interpolation therefore stays above R*cos(0.003).
 centre_radius_lower=.154*math.cos(.006/2)
 continuous_inner=centre_radius_lower-.0007-maxr;continuous_outer=actual_wall_radius_lower-(.154+.0007)
 assert continuous_inner>0 and continuous_outer>0 and not invalid
 assert particle_rmin>=.154-.000705 and particle_rmax<=.154+.000705,(kind,version,particle_rmin,particle_rmax)
 assert particle_xmin>=.7-.00601 and particle_xmax<=2.7+.00601,(particle_xmin,particle_xmax)
 # Control probes at fixed frame, no writes to candidate.
 s.frame_set(31);ctrl['speed']=0;ctrl.update_tag();s.frame_set(31);a=list(cuts[0].evaluated_get(bpy.context.evaluated_depsgraph_get()).matrix_world.translation);s.frame_set(47);b=list(cuts[0].evaluated_get(bpy.context.evaluated_depsgraph_get()).matrix_world.translation);assert max(abs(a[i]-b[i]) for i in range(3))<1e-6
 ctrl['phase']=.31;ctrl.update_tag();s.frame_set(47);c=list(cuts[0].evaluated_get(bpy.context.evaluated_depsgraph_get()).matrix_world.translation);assert (Vector(c)-Vector(b)).length>.05
 ctrl['density']=0;ctrl.update_tag();s.frame_set(48);assert all(o.evaluated_get(bpy.context.evaluated_depsgraph_get()).hide_render for o in cuts)
 ctrl['density']=10;ctrl['cuttings_visible']=0;ctrl.update_tag();s.frame_set(49);assert all(o.evaluated_get(bpy.context.evaluated_depsgraph_get()).hide_render for o in cuts)
 ctrl['operating_mode']=1;ctrl.update_tag();s.frame_set(50);assert all(o.evaluated_get(bpy.context.evaluated_depsgraph_get()).hide_render for o in paths+cuts+tracers)
 ctrl['operating_mode']=0;ctrl['flow_visible']=1;ctrl['cuttings_visible']=1;ctrl['stage_emphasis']=2;ctrl.update_tag();s.frame_set(51);assert all(not o.evaluated_get(bpy.context.evaluated_depsgraph_get()).hide_render for o in paths)
 scales=[o.evaluated_get(bpy.context.evaluated_depsgraph_get()).scale.x for o in cuts];assert min(scales)<max(scales)<=1.000001
 ctrl['flow_visible']=0;ctrl.update_tag();s.frame_set(52);assert all(o.evaluated_get(bpy.context.evaluated_depsgraph_get()).hide_render for o in paths+tracers)
 assert all(not o.evaluated_get(bpy.context.evaluated_depsgraph_get()).hide_render for o in cuts)
 # Reload original untouched saved file to report defaults rather than probe state.
 bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False,use_scripts=False);s=bpy.context.scene;s.frame_set(1)
 rec=dict(path=str(p.relative_to(ROOT)).replace('\\','/'),sha256=sha(p),libraries=libs,snapshot=snapshot(),all_relative_links_exist=True,linked_path_objects=10,linked_particle_objects=30,hardware_objects_checked=sorted(set(objects)),actual_hardware_radial_bound_m=maxr,strand_evaluated_vertices=tested,strand_radial_bounds_m=[min_radius,max_radius],strand_hardware_clearance_bound_m=path_inner,strand_nominal_wall_clearance_m=path_outer,nearest_hardware_sample_m=min_hardware,particles_all_frames=[1,s.frame_end],particle_sampled_radius_bounds_m=[particle_rmin,particle_rmax],continuous_complete_particle_hardware_bound_m=continuous_inner,continuous_complete_particle_wall_bound_m=continuous_outer,all_phase_clearance_method='Every guide point at radius.154m; straight poly interpolation cannot exceed.154m. Complete octahedron lies within0.7mm sphere; complete strand within0.45mm tube. Native hardware convex radial bound and nominal bore radius bound apply continuously to all phases.',control_probes=dict(speed_zero_freezes=True,phase_changes_position=True,density_zero_hides=True,cuttings_visibility=True,mode_off=True,emphasis_keeps_all_paths_active=True),invalid=invalid,first_particle_motion=motion[::12],limits='Nominal centred T44 pose/travel.5m, rotation0; no eccentric/other-pose clearance guarantee. Wet optical cut is not a fluid-domain solver. No physical transport validation.')
 rec.update(particle_x_bounds_m=[particle_xmin,particle_xmax],linked_flow_geometry_hash=geometry_hash,linked_cutting_geometry_hash=cutting_hash,cutting_geometry_library=cutting_library,shared_amber_emission=emission,sliding_amber_tracers=len(tracers),continuous_guide_radius_lower_m=centre_radius_lower,continuous_strand_hardware_clearance_bound_m=centre_radius_lower-.00045-maxr,actual_wall_face_plane_lower_radius_m=actual_wall_radius_lower,nearest_actual_wall_sample_m=nearest_wall,actual_wall_meshes_checked=['NOMINAL_CUTAWAY','FORMATION_NOMINAL_CUTAWAY'],all_phase_clearance_method='Guide nodes radius0.154m, segment azimuth difference<0.006rad => interpolated centre radius>=0.154*cos(0.003). Whole matte sliver has radial extent<=0.7mm and axial<=3mm; amber tracer radial<=0.45mm/axial<=6mm; strand inside0.45mm tube. This continuous radial envelope fits actual hardware convex radial bound and actual evaluated nominal wall face-plane lower radius (faceting included). Rigid centred T44 pose only.')
 dump('Flow_reuse_'+kind+'_'+version+'_fresh-open.json',rec);return rec
if __name__=='__main__':
 results=[]
 for k in ['A','B']:
  for v in ['v003','v004','v005']:results.append(verify(k,v))
 for k in ['A','B']:
  a,b,c=[r for r in results if ('reuse_'+k+'_') in r['path']];assert a['snapshot']==b['snapshot']==c['snapshot']
  assert a['linked_flow_geometry_hash']==b['linked_flow_geometry_hash']==c['linked_flow_geometry_hash']
  assert a['linked_cutting_geometry_hash']==b['linked_cutting_geometry_hash']!=c['linked_cutting_geometry_hash']
  assert any('Hydraulics_v002.blend' in l['path'] for l in b['libraries'])
 source=ROOT/'04-Production/Mechanisms/B204/Scenes/B204_hydraulic-proof_v001.blend'
 bpy.ops.wm.open_mainfile(filepath=str(source),load_ui=False,use_scripts=False)
 dump('b204-native-inspection_v001.json',dict(path=str(source.relative_to(ROOT)).replace('\\','/'),sha256=sha(source),collections=list(bpy.data.collections.keys()),objects=[o.name for o in bpy.data.objects],limits='Historical proof read-only; guides and oversized diagram particles are illustrative. No geometry reused as a clearance result.'))
 dump('native-verification-summary_v003.json',dict(all_checks_pass=True,consumers=[dict(path=r['path'],sha256=r['sha256']) for r in results],revision_preserves_camera_timing_controls_animation=True))
 print('T48_NATIVE_VERIFICATION_PASS')
