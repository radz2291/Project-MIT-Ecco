"""Check approved-frame continuity and source-bound outgoing illustration."""
import bpy,json,hashlib,math
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
P=Path(__file__).resolve().parents[3];M=P/'Mechanisms/B201';E=P/'Records/Tasks/T-007/Evidence/Still_02b'
src=M/'Scenes/B201_sensor-origin_still01_v004.blend';out=M/'Scenes/B201_spreading-pulse_still02b_v001.blend';record=json.loads((E/'build-render_still02b_v001.json').read_text())
def snapshot():
 s=bpy.context.scene;c=s.camera
 return {'camera':[list(c.location),list(c.rotation_euler),c.data.lens,c.data.type,c.data.sensor_width], 'lights':{o.name:{'location':list(o.location),'rotation':list(o.rotation_euler),'power':o.data.energy,'color':list(o.data.color),'size':o.data.size} for o in s.objects if o.type=='LIGHT'},'rig':dict(bpy.data.objects['ASSEMBLY_CONTROL'].items())}
bpy.ops.wm.open_mainfile(filepath=str(src));approved=snapshot()
bpy.ops.wm.open_mainfile(filepath=str(out));s=bpy.context.scene;bpy.context.view_layer.update();candidate=snapshot();checks=[]
def check(n,v,d=None):checks.append({'check':n,'pass':bool(v),'details':d})
check('approved camera unchanged',approved['camera']==candidate['camera'])
check('approved lighting unchanged',approved['lights']==candidate['lights'])
check('whole-tool pose unchanged',approved['rig']==candidate['rig'])
check('approved saved source unchanged',hashlib.sha256(src.read_bytes()).hexdigest()==record['approved_input_scene_sha256'])
check('approved Still01 image unchanged',hashlib.sha256((M/'Previews/Still_01/B201_sensor-origin_still01_v004.png').read_bytes()).hexdigest()==record['approved_input_image_sha256'])
check('candidate source hash',hashlib.sha256(out.read_bytes()).hexdigest()==record['scene_sha256'])
check('candidate image hash',hashlib.sha256((P/record['image']).read_bytes()).hexdigest()==record['image_sha256'])
check('full-size still only',s.render.resolution_x==1920 and s.render.resolution_y==1080 and s.frame_start==s.frame_end==1)
check('no local object motion added',all(o.animation_data is None for o in s.objects if o.library is None))
check('relative source links resolve',all(l.filepath.startswith('//') and Path(bpy.path.abspath(l.filepath)).is_file() for l in bpy.data.libraries))
for rel,h in record['inputs'].items():check('source unchanged: '+rel,hashlib.sha256((P/rel).read_bytes()).hexdigest()==h)
for n in ('B201_PULSE_ECHO','B201_CONTACT_HISTORY','B201_SPATIAL_GRAPHICS'):check('diagnostic/history/trace group excluded: '+n,bpy.data.collections[n].hide_render)
pulses=[o for o in s.objects if o.name.startswith('OUTGOING_WAVEFRONT_ILLUSTRATION_')];check('three widening contours',len(pulses)==3);origin=Vector(record['origin']);normal=Vector(record['direction']);wall=Vector(record['wall_reference'])
points=[pulse.matrix_world@v.co for pulse in pulses for v in pulse.data.vertices];radial=[(p-origin).dot(normal) for p in points];dist=[(p-origin).length for p in points]
check('contours ordered outward',all(abs((o.matrix_world@o.data.vertices[0].co-origin).dot(normal)-d)<1e-6 for o,(d,r) in zip(pulses,record['contours_distance_radius_m'])))
check('front is detached and before actual wall',min(radial)>.005 and max(radial)<(wall-origin).length,{'outward_m':[min(radial),max(radial)],'max_distance_m':max(dist),'wall_distance_m':(wall-origin).length})
projection=[world_to_camera_view(s,s.camera,p) for p in points]
check('full crescent inside frame',all(0<p.x<1 and 0<p.y<1 and p.z>0 for p in projection))
beauty=s.view_layers['Approved model look'];signal=s.view_layers['Illustrative outgoing pulse']
check('pulse excluded from metal override',beauty.layer_collection.children['STILL02_ILLUSTRATIVE_WAVEFRONT'].exclude and signal.material_override is None)
check('pulse layer only signal and camera',all(c.exclude==(c.name not in ('STILL02_ILLUSTRATIVE_WAVEFRONT','B201_REVIEW_CAMERA')) for c in signal.layer_collection.children))
check('same camera for editable composition',s.compositing_node_group is not None and s.camera.name=='B201_FILM_VIEW')
# Product-only visibility rays: ignore source diagnostic cutter/hidden groups.
dg=bpy.context.evaluated_depsgraph_get();visibility=[]
for p in points[::97]:
 start=s.camera.matrix_world.translation;direction=(p-start).normalized();target_distance=(p-start).length;nearest=None
 for instance in dg.object_instances:
  o=instance.object
  if o.type!='MESH' or o.original.hide_render or not (o.name=='ECCO_HOUSING_SOURCE_MESH' or o.name.startswith('TEMP |')):continue
  inv=instance.matrix_world.inverted();ok,hit,n,idx=o.ray_cast(inv@start,(inv.to_3x3()@direction).normalized())
  if ok:
   d=(instance.matrix_world@hit-start).length
   if d<target_distance-.0002 and (nearest is None or d<nearest[0]):nearest=(d,o.name)
 visibility.append(nearest)
check('source geometry does not occlude front',all(x is None for x in visibility),visibility)
output={'checks':checks,'passed':all(c['pass'] for c in checks),'executor_self_check':True,'Still01_visual_approval':'Radzi explicit, exactv004','Still02_initial_visual_approval':'accepted with spreading arc requirement','Still02b_visual_approval':'pending','motion_authorized':False}
(E/'verification_still02b_v001.json').write_text(json.dumps(output,indent=2));assert output['passed'],[c for c in checks if not c['pass']]
print('STILL02_VERIFY_PASS',len(checks))
