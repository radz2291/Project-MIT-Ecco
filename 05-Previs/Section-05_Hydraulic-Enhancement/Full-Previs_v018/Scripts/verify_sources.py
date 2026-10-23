import bpy,math,json,hashlib
from pathlib import Path
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
from bpy_extras.object_utils import world_to_camera_view
B=Path(__file__).resolve().parents[1];ROOT=B.parents[2];s=bpy.context.scene
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
prior=ROOT/'05-Previs/Section-05_Hydraulic-Enhancement/Interaction-Proof_v017/Scenes/S05_rich-amber_v017.blend'
assert sha(prior)=='900fa8fc795a864eb2b6a4727b96817154f65d5678998b886d92fc7992c52abe'
source=ROOT/'04-Production/Shared/Assets/ECCO/ECCO_film_v002.blend'
assert sha(source)=='df656a5c4bc48f081a4b6365c7969df55d15c7da53ddb96be20875e931d26584'
libraries=[{'path':l.filepath,'resolved':bpy.path.abspath(l.filepath),'exists':Path(bpy.path.abspath(l.filepath)).exists(),'relative':l.filepath.startswith('//')} for l in bpy.data.libraries];assert all(r['exists'] and r['relative'] for r in libraries)
s.frame_set(151);bpy.context.view_layer.update();vv=[];ff=[]
for o in bpy.data.collections['S05_LINKED_HARDWARE'].objects:
 off=len(vv);vv.extend(o.matrix_world@v.co for v in o.data.vertices);ff.extend([[off+i for i in p.vertices] for p in o.data.polygons])
steel=BVHTree.FromPolygons(vv,ff);fluid=bpy.data.objects['S05_v018_AnnularFluidDomain'];dv=[fluid.matrix_world@v.co for v in fluid.data.vertices];df=[list(p.vertices) for p in fluid.data.polygons];ftree=BVHTree.FromPolygons(dv,df)
overlaps=steel.overlap(ftree);assert not overlaps,('Fluid intersects steel',len(overlaps))
fluidwall=min(.155575-math.hypot(v.x,v.y) for v in dv);fluidsteel=min(steel.find_nearest(v)[3] for v in dv)
assert min(fluidwall,fluidsteel)>0
body=bpy.data.objects['S05_ECCO_HOUSING_SOURCE_MESH'];zs=[(body.matrix_world@v.co).z for v in body.data.vertices];length=max(zs)-min(zs);assert abs(length-2.4)<1e-5
rocks=[o for o in bpy.data.collections['S05_v018_ContinuousHydraulics'].objects if 'Cutting' in o.name];radius={o.name:max(v.co.length for v in o.data.vertices) for o in rocks};pairhits=[];camera=[]
for frame in [1+i*.5 for i in range(863)]:
 s.frame_set(int(frame),subframe=frame-int(frame));bpy.context.view_layer.update()
 angle=-math.radians(5)*(frame-151)/24;assert abs(fluid.rotation_euler.z-angle)<1e-5
 for i,o in enumerate(rocks):
  for p in rocks[i+1:]:
   if (o.location-p.location).length>radius[o.name]+radius[p.name]:continue
   a=BVHTree.FromPolygons([o.matrix_world@v.co for v in o.data.vertices],[list(q.vertices) for q in o.data.polygons]);b=BVHTree.FromPolygons([p.matrix_world@v.co for v in p.data.vertices],[list(q.vertices) for q in p.data.polygons])
   if a.overlap(b):pairhits.append({'frame':frame,'objects':[o.name,p.name]})
 if frame==int(frame):
  cam=s.camera;pt=Vector((0,0,-.1 if frame<=120 else (.3 if frame<=288 else .8)));low=world_to_camera_view(s,cam,pt);high=world_to_camera_view(s,cam,pt+Vector((0,0,.05)))
  assert high.y>low.y,'Perceived flow reverses'
  camera.append({'frame':frame,'location':list(cam.location),'quaternion':list(cam.rotation_quaternion),'lens':cam.data.lens,'shift':[cam.data.shift_x,cam.data.shift_y],'uphole_screen_delta':[high.x-low.x,high.y-low.y]})
assert not pairhits,pairhits[:5]
result={'prior_v017_unchanged_sha256':sha(prior),'shared_source_unchanged_sha256':sha(source),'source_length_m':length,'borehole_inner_radius_m':.155575,'libraries':libraries,'fluid_steel_surface_intersections':len(overlaps),'fluid_min_steel_distance_m':fluidsteel,'fluid_min_wall_margin_m':fluidwall,'fluid_boundary_rotates_with_solid_exclusion_only':True,'density_field':'World position based upward advection and partial angular entrainment, source v008 restored in v010 and amber treatment v017','rock_pair_overlap_count':len(pairhits),'rock_pair_sample_count':863,'upward_screen_direction_all_432_frames':True,'physical_stage_face_mapping':'Unresolved O07; T48 source-X windows reused as morphological interpretation, not certified faces','world_stage_windows_m':{'lower':[-.06,.15],'middle':[.15,.62],'upper':[.62,1.]},'source_mode':'Owner selected combined circulation and rotation; -5deg/s illustrated, no axial translation; no measured RPM/CFD claims'}
(B/'Records/source-geometry-verification.json').write_text(json.dumps(result,indent=2));(B/'Records/camera-score.json').write_text(json.dumps(camera));s.frame_set(198)
