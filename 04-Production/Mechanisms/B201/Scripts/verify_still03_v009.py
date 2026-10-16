import bpy,json,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from bpy_extras.object_utils import world_to_camera_view
P=Path(__file__).resolve().parents[3];M=P/'Mechanisms/B201';E=P/'Records/Tasks/T-007/Evidence/Still_03'
r=json.loads((E/'build-render_still03_v009.json').read_text());src=M/'Scenes/B201_spreading-pulse_still02c_v001.blend';out=P/r['scene'];checks=[]
def snapshot():
 s=bpy.context.scene;c=s.camera
 return {'camera':[list(c.location),list(c.rotation_euler),c.data.lens,c.data.type,c.data.sensor_width],'rig':dict(bpy.data.objects['ASSEMBLY_CONTROL'].items()),'lights':{o.name:[list(o.location),list(o.rotation_euler),o.data.energy,list(o.data.color),o.data.size] for o in s.objects if o.type=='LIGHT'}}
def check(n,v):checks.append({'check':n,'pass':bool(v)})
bpy.ops.wm.open_mainfile(filepath=str(src));before=snapshot()
bpy.ops.wm.open_mainfile(filepath=str(out));s=bpy.context.scene;bpy.context.view_layer.update();after=snapshot()
check('approved product pose unchanged',before['rig']==after['rig'])
check('approved lights preserved',all(after['lights'].get(k)==v for k,v in before['lights'].items()))
check('new gap camera recorded',after['camera'][2]==32 and after['camera'][0]==r['camera']['location'])
check('approved source preserved',hashlib.sha256(src.read_bytes()).hexdigest()==r['approved_source_sha256'])
check('candidate source hash',hashlib.sha256(out.read_bytes()).hexdigest()==r['scene_sha256'])
check('candidate image hash',hashlib.sha256((P/r['image']).read_bytes()).hexdigest()==r['image_sha256'])
for rel,h in r['inputs'].items():check('unchanged source '+rel,hashlib.sha256((P/rel).read_bytes()).hexdigest()==h)
check('relative libraries resolve',all(x.filepath.startswith('//') and Path(bpy.path.abspath(x.filepath)).is_file() for x in bpy.data.libraries))
check('single full-size still',s.frame_start==s.frame_end==1 and s.render.resolution_x==1920 and s.render.resolution_y==1080)
check('no local object animation',all(o.animation_data is None for o in s.objects if o.library is None))
for n in ('B201_PULSE_ECHO','B201_CONTACT_HISTORY','B201_SPATIAL_GRAPHICS'):check('diagnostics excluded '+n,bpy.data.collections[n].hide_render)
origin=Vector(r['origin']);wall=Vector(r['wall']);fronts=sorted([o for o in s.objects if o.name.startswith('OUTGOING_WAVEFRONT_ILLUSTRATION_')],key=lambda o:o.name)
check('three editable smooth closed envelopes',len(fronts)==3 and all(len(o.data.vertices)==65*128 and all(f.use_smooth for f in o.data.polygons) for o in fronts))
check('outer envelope reaches measured contact',abs(sum(r['wave_envelopes'][-1][:2])-(wall-origin).length)<1e-7)
section=bpy.data.objects['T6_WALL_CONTACT_SECTION'];points=[section.matrix_world@v.co for v in section.data.vertices]
check('wall correspondence to evaluated T6',r['wall_correspondence_max_m']<1e-6)
check('wall contains actual arrival point',min((p-wall).length for p in points)<3e-6)
check('contact and sensor inside frame',all(0<q.x<1 and 0<q.y<1 and q.z>0 for q in [world_to_camera_view(s,s.camera,p) for p in (origin,wall)]))
check('wall material separated from product override',s.view_layers['Wall interaction'].material_override is None and s.view_layers['Approved model look'].layer_collection.children['STILL03_WALL_CONTACT'].exclude)
check('wall emission only localized contact',section.data.color_attributes['ContactWeight'] is not None and len(section.data.materials)==1)
check('continuous wall without plate backing',len(section.modifiers)==0)
check('wall-to-wave depth masking enabled',s.view_layers['Wall interaction'].use_pass_z and s.view_layers['Illustrative outgoing pulse'].use_pass_z and any(n.bl_idname=='ShaderNodeMath' and n.operation=='LESS_THAN' for n in s.compositing_node_group.nodes))
c=s.camera.location;radial=Vector((0,c.y,c.z));tree=BVHTree.FromPolygons(points,[list(f.vertices) for f in section.data.polygons]);hit=tree.ray_cast(Vector((c.x,0,0)),radial.normalized())[0]
check('camera within preserved annular space',hit is not None and .132<radial.length<Vector((0,hit.y,hit.z)).length)
output={'checks':checks,'passed':all(c['pass'] for c in checks),'executor_self_check':True,'human_visual_approval':'pending','motion_authorized':False}
(E/'verification_still03_v009.json').write_text(json.dumps(output,indent=2));assert output['passed'],[x for x in checks if not x['pass']];print('WALL_STILL_VERIFY_PASS',len(checks))
