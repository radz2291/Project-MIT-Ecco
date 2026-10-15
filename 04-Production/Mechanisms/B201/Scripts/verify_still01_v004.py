"""Reopen the exact still source; check gate scope, source identity and framing."""
import bpy,json,hashlib
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
P=Path(__file__).resolve().parents[3];M=P/'Mechanisms/B201';R=P/'Records/Tasks/T-007/Evidence/Still_01'
path=M/'Scenes/B201_sensor-origin_still01_v004.blend';bpy.ops.wm.open_mainfile(filepath=str(path));s=bpy.context.scene
record=json.loads((R/'build-render_still01_v004.json').read_text());checks=[]
def check(name,value,details=None):checks.append({'check':name,'pass':bool(value),'details':details})
check('exact saved candidate',hashlib.sha256(path.read_bytes()).hexdigest()==record['scene_sha256'])
check('full-size image',list(s.render.resolution_x_y) ==[1920,1080] if hasattr(s.render,'resolution_x_y') else s.render.resolution_x==1920 and s.render.resolution_y==1080)
check('one static frame',s.frame_start==1 and s.frame_end==1)
check('no local object animation',all(o.animation_data is None for o in s.objects if o.library is None))
for rel,h in record['inputs'].items():check('unchanged source: '+rel,hashlib.sha256((P/rel).read_bytes()).hexdigest()==h)
check('relative libraries resolve',all(l.filepath.startswith('//') and Path(bpy.path.abspath(l.filepath)).is_file() for l in bpy.data.libraries))
for n in ('B201_PULSE_ECHO','B201_CONTACT_HISTORY','B201_SPATIAL_GRAPHICS'):
 check('excluded imagery group: '+n,bpy.data.collections[n].hide_render)
inst=bpy.data.objects['ECCO_LINK_v002'];check('actual linked product remains visible',not inst.hide_render and inst.instance_collection.library is not None)
bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();caps=[i.matrix_world.copy() for i in dg.object_instances if i.is_instance and 'Imaging port 1' in i.object.name]
check('actual source cap instance present',len(caps)==1)
if caps:
 point=caps[0].translation;p=world_to_camera_view(s,s.camera,point)
 check('cap framed inside image',.1<p.x<.9 and .1<p.y<.9,list(p))
 check('diagnostic source cutter excluded',bpy.data.objects['ECCO_CUTTER_PREVIEW_ONLY'].hide_render)
check('image matches recorded hash',hashlib.sha256((P/record['image']).read_bytes()).hexdigest()==record['image_sha256'])
output={'checks':checks,'passed':all(c['pass'] for c in checks),'executor_self_check':True,'visual_approval':'pending Radzi, first still only','motion_authorized':False}
(R/'verification_still01_v004.json').write_text(json.dumps(output,indent=2));assert output['passed'],[c for c in checks if not c['pass']]
print('STILL01_VERIFY_PASS',len(checks))
