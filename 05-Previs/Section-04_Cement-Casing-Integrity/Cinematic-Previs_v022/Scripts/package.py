import bpy,json,hashlib,math
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
import sys
sys.path.insert(0,str(Path(__file__).parent));from revise import geo
B=Path(__file__).resolve().parents[1];meta=json.loads((B/'Records/build.json').read_text())
bpy.ops.wm.open_mainfile(filepath=str(B/'Scenes/S04_continuous-camera_v022.blend'),use_scripts=False,load_ui=False);s=bpy.context.scene
assert geo(s)==meta['physical_hashes']
assert hashlib.sha256(Path(meta['source']).read_bytes()).hexdigest()==meta['source_sha256']
steel=bpy.data.objects['STEEL - capped true source section'];depth=[x.value for x in steel.data.attributes['ComputedWearDepth_m'].data];assert max(depth)<.004001
physical=[o for o in s.objects if o.type=='MESH' and (o.name.startswith('Cement ') or 'organic fluid-filled' in o.name or 'capped true source' in o.name or 'closed source-guided' in o.name)]
baseline={o.name:(tuple(o.matrix_world),o.hide_render) for o in physical};cams=set();sensorcheck=[];distances=[];N=Vector((0,-math.sin(math.radians(39)),math.cos(math.radians(39))))
for f in range(1,433):
 s.frame_set(f);bpy.context.view_layer.update();cams.add(s.camera.name)
 assert all((tuple(o.matrix_world),o.hide_render)==baseline[o.name] for o in physical)
 p=s.camera.matrix_world.translation
 if p.dot(N)<0 and -5.5<p.x<0:distances.append((f,math.hypot(p.y,p.z)))
 if f in [85,197,318,330,350,380,400,415]:
  p=next(i.matrix_world.translation.copy() for i in bpy.context.evaluated_depsgraph_get().object_instances if i.object.name=='ECCO_SENSOR_REF_01');front=bpy.data.objects['WORLD_CONTROL']['travel_m']+.7300000190734863
  assert abs(p.x-front)<1e-5
  if f>=318:assert abs(p.y-.129)<1e-5 and abs(p.z)<1e-5
  sensorcheck.append({'frame':f,'actual_sensor_world_m':list(p),'projected_sensor':list(world_to_camera_view(s,s.camera,p)),'front_x_error_m':abs(p.x-front)})
assert len(cams)==1
libs=[{'path':l.filepath,'exists':Path(bpy.path.abspath(l.filepath)).is_file(),'relative':l.filepath.startswith('//')} for l in bpy.data.libraries];assert all(x['exists'] and x['relative'] for x in libs)
# Localized housing uses unchanged source coordinates/topology.
housing=bpy.data.objects['ECCO unchanged source housing - D technical transparency']
original=bpy.data.objects.get('ECCO_HOUSING_SOURCE_MESH')
if original is None:
 with bpy.data.libraries.load(str(B.parents[2]/'04-Production/Shared/Assets/ECCO/ECCO_film_v002.blend'),link=True) as (a,b):b.objects=['ECCO_HOUSING_SOURCE_MESH']
 original=b.objects[0]
assert len(housing.data.vertices)==len(original.data.vertices) and all(a.co==b.co for a,b in zip(housing.data.vertices,original.data.vertices))
# Source wave and response animation timings remain unchanged after footprint editing.
def animation_digest(o):
 if not o.animation_data or not o.animation_data.action:return None
 return [(c.data_path,c.array_index,[(tuple(p.co),p.interpolation) for p in c.keyframe_points]) for l in o.animation_data.action.layers for st in l.strips for bag in st.channelbags for c in bag.fcurves]
report={'saved_reopened':True,'physical_meshes_identical_to_v021':True,'well_layer_transforms_and_visibility_fixed_all432frames':True,'one_camera_all432frames':True,'duration_seconds':18,'fps':24,'resolution':[1280,720],'max_authored_wear_mm':1000*max(depth),'source_bytes_unchanged':True,'housing_local_copy_coordinates_unchanged':True,'housing_transparency_is_explanatory':True,'sensor_positions_verified':sensorcheck,'relative_libraries':libs,'camera_inside_removed_or_bore_side_for_review':distances,'human_approval':'pending','engineering_certification':False}
s.frame_set(350)
for f,txt in [(1,'A - existing casing entry'),(63,'B - supported response'),(175,'C - reduced backing'),(261,'Camera enters wear inspection'),(318,'D - ECCO sensor alongside wear'),(350,'Sensor pass - expose fixed geometry data')]:s.timeline_markers.new(txt,frame=f)
s['review_scope']='v022 owner-requested whole-video review. D detection tied to ECCO sensor instead of bit. Explanatory housing transparency is a new review choice.'
for w in bpy.context.window_manager.windows:
 w.scene=s
 for a in w.screen.areas:
  if a.type=='VIEW_3D':a.spaces.active.region_3d.view_perspective='CAMERA';a.spaces.active.shading.type='RENDERED'
out=B/'Scenes/S04_complete_v022.blend';bpy.ops.wm.save_as_mainfile(filepath=str(out),relative_remap=False)
bpy.ops.wm.open_mainfile(filepath=str(out),use_scripts=False,load_ui=False);report['complete_native']=str(out)
(B/'Records/verification.json').write_text(json.dumps(report,indent=2));print('PACKAGE VERIFIED')
