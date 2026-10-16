import bpy,json,hashlib
from pathlib import Path
from mathutils import Vector
P=Path(__file__).resolve().parents[3];E=P/'Records/Tasks/T-007/Evidence/Still_05';r=json.loads((E/'build-render_still05_v001.json').read_text());checks=[]
def check(name,value):checks.append({'check':name,'pass':bool(value)})
def snapshot():
 s=bpy.context.scene;c=s.camera;wall=bpy.data.objects['T6_WALL_CONTACT_SECTION'];mat=s.view_layers['Approved model look'].material_override
 return {'camera':[list(c.location),list(c.rotation_euler),c.data.lens,c.data.sensor_width],'wall':[list(v.co) for v in wall.data.vertices],'pose':dict(bpy.data.objects['ASSEMBLY_CONTROL'].items()),'lights':{o.name:[list(o.location),list(o.rotation_euler),o.data.energy,list(o.data.color)] for o in s.objects if o.type=='LIGHT'},'reception_material':mat.name,'patch_fade':bpy.data.objects['ACOUSTIC_CONTACT_CONTROLLER']['scan_fade']}
src=P/r['parent_scene'];bpy.ops.wm.open_mainfile(filepath=str(src));before=snapshot()
out=P/r['scene'];bpy.ops.wm.open_mainfile(filepath=str(out));s=bpy.context.scene;after=snapshot()
for key in before:check('Still04 continuity '+key,before[key]==after[key])
check('parent scene preserved',hashlib.sha256(src.read_bytes()).hexdigest()==r['parent_scene_sha256'])
check('saved source hash',hashlib.sha256(out.read_bytes()).hexdigest()==r['scene_sha256'])
check('render hash',hashlib.sha256((P/r['image']).read_bytes()).hexdigest()==r['image_sha256'])
for rel,h in r['inputs'].items():check('accepted master unchanged '+rel,hashlib.sha256((P/rel).read_bytes()).hexdigest()==h)
check('relative libraries resolve',all(x.filepath.startswith('//') and Path(bpy.path.abspath(x.filepath)).is_file() for x in bpy.data.libraries))
check('one 1920x1080 still',s.frame_start==s.frame_end==1 and s.render.resolution_x==1920 and s.render.resolution_y==1080)
coll=bpy.data.collections['STILL05_MEASUREMENT_GRAPHICS'];texts=[o for o in coll.objects if o.type=='FONT']
check('only approved minimal labels',sorted(o.data.body for o in texts)==sorted(r['labels']))
check('no formula or numeric data',all(not any(c.isdigit() for c in o.data.body) and '=' not in o.data.body for o in texts))
check('editable native text with available font',all(o.data.font and Path(bpy.path.abspath(o.data.font.filepath)).is_file() for o in texts))
measure=bpy.data.objects['SENSOR_TO_WALL_MEASUREMENT'];points=measure.data.splines[0].points
check('spatial line starts at actual receiver', (Vector(points[0].co[:3])-Vector(r['receiver_surface'])).length<1e-7)
check('spatial line ends at actual wall', (Vector(points[-1].co[:3])-Vector(r['wall_origin'])).length<1e-7)
check('two illustrative signal events',all(bpy.data.objects[n]['illustrative_signal'] and bpy.data.objects[n]['not_amplitude_or_distance_data'] for n in ('PULSE_SENT_TRACE','ECHO_RECEIVED_TRACE')))
check('clean timing bracket exists',bpy.data.objects.get('TWO_WAY_TIMING_BRACKET') is not None)
check('outgoing and return membranes hidden for measurement payoff',all(o.hide_render for o in s.objects if o.name.startswith(('OUTGOING_WAVEFRONT_ILLUSTRATION_','RETURNING_ECHO_'))))
check('graphics separate from product override',s.view_layers['Minimal measurement graphics'].material_override is None and s.view_layers['Approved model look'].layer_collection.children[coll.name].exclude)
for name in ('B201_PULSE_ECHO','B201_CONTACT_HISTORY','B201_SPATIAL_GRAPHICS'):check('diagnostics excluded '+name,bpy.data.collections[name].hide_render)
check('no local object motion',all(o.animation_data is None for o in s.objects if o.library is None))
result={'checks':checks,'passed':all(x['pass'] for x in checks),'executor_self_check':True,'visual_approval':'pending','motion_authorized':False}
(E/'verification_still05_v001.json').write_text(json.dumps(result,indent=2));assert result['passed'],[x for x in checks if not x['pass']];print('MEASURED_WALL_POSITION_VERIFY_PASS',len(checks))
