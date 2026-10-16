import bpy,json,hashlib,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from bpy_extras.object_utils import world_to_camera_view
P=Path(__file__).resolve().parents[3];E=P/'Records/Tasks/T-007/Evidence/Still_04';r=json.loads((E/'build-render_still04_v003.json').read_text());checks=[]
def check(name,value):checks.append({'check':name,'pass':bool(value)})
def snapshot():
 s=bpy.context.scene;c=s.camera;wall=bpy.data.objects['T6_WALL_CONTACT_SECTION']
 return {'camera':[list(c.location),list(c.rotation_euler),c.data.lens,c.data.sensor_width],'wall':[list(v.co) for v in wall.data.vertices],'pose':dict(bpy.data.objects['ASSEMBLY_CONTROL'].items()),'lights':{o.name:[list(o.location),list(o.rotation_euler),o.data.energy,list(o.data.color)] for o in s.objects if o.type=='LIGHT'}}
src=P/r['parent_scene'];bpy.ops.wm.open_mainfile(filepath=str(src));before=snapshot()
out=P/r['scene'];bpy.ops.wm.open_mainfile(filepath=str(out));s=bpy.context.scene;after=snapshot()
for key in before:check('Still03 continuity '+key,before[key]==after[key])
check('selected Still03 preserved',hashlib.sha256(src.read_bytes()).hexdigest()==r['parent_scene_sha256'])
check('saved source hash',hashlib.sha256(out.read_bytes()).hexdigest()==r['scene_sha256'])
check('render hash',hashlib.sha256((P/r['image']).read_bytes()).hexdigest()==r['image_sha256'])
for rel,h in r['inputs'].items():check('accepted master unchanged '+rel,hashlib.sha256((P/rel).read_bytes()).hexdigest()==h)
check('relative libraries resolve',all(x.filepath.startswith('//') and Path(bpy.path.abspath(x.filepath)).is_file() for x in bpy.data.libraries))
check('one 1920x1080 still',s.frame_start==s.frame_end==1 and s.render.resolution_x==1920 and s.render.resolution_y==1080)
check('outgoing fronts faded out',all(o.hide_render for o in s.objects if o.name.startswith('OUTGOING_WAVEFRONT_ILLUSTRATION_')))
echo=bpy.data.objects['RETURNING_ECHO_FIRST_RECEPTION'];wall=Vector(r['wall_origin']);receiver=Vector(r['receiver_surface']);radius=r['return_radius_m']
check('wall-originating thin spherical return',len(echo.modifiers)==0 and all(abs((v.co-wall).length-radius)<1e-6 for v in echo.data.vertices))
check('echo first reaches original sensor surface',min((v.co-receiver).length for v in echo.data.vertices)<1e-6)
check('same emitting sensor correspondence',r['reference_to_surface_m']<.001 and r['receiver_object']=='TEMP | Imaging port 1 | removable acoustic cap')
# Compare all rays of cap against actual receiver geometry: central pole is first contact.
tree=None
for inst in bpy.context.evaluated_depsgraph_get().object_instances:
 o=inst.object
 if inst.is_instance and o.type=='MESH' and o.name==r['receiver_object']:
  me=o.to_mesh();tree=BVHTree.FromPolygons([inst.matrix_world@v.co for v in me.vertices],[list(p.vertices) for p in me.polygons]);o.to_mesh_clear();break
assert tree is not None
check('reception point on actual evaluated cap',tree.find_nearest(receiver)[3]<1e-6)
direction=(receiver-wall).normalized();hit=tree.ray_cast(wall,direction)
check('first central ray contact matches echo radius',hit[0] is not None and abs(hit[3]-radius)<1e-6)
check('faint prior sampled wall patch',abs(bpy.data.objects['ACOUSTIC_CONTACT_CONTROLLER']['scan_fade']-.07)<1e-6)
check('restrained reception material',s.view_layers['Approved model look'].material_override.name.startswith('Still04 preserved product'))
receive_shader=next(n for n in s.view_layers['Approved model look'].material_override.node_tree.nodes if n.bl_idname=='ShaderNodeBsdfPrincipled')
color=receive_shader.inputs['Emission Color'].default_value
check('emerald reception on original sensor',color[1]>color[2]>color[0] and abs(color[1]-.60)<1e-6)
check('no refractive return material',not any(n.bl_idname in ('ShaderNodeBsdfGlass','ShaderNodeBsdfRefraction') for n in echo.data.materials[0].node_tree.nodes))
check('echo smooth',all(p.use_smooth for p in echo.data.polygons))
followers=sorted([o for o in s.objects if o.name.startswith('RETURNING_ECHO_FOLLOWER_')],key=lambda o:o.name)
check('one main front with two faint followers',len(followers)==2)
check('followers closer to wall than main receiver front',all(0<o['radius_m']<radius for o in followers))
check('tight echo spacing',all(abs((radius-o['radius_m'])-.0045*(i+1))<1e-7 for i,o in enumerate(followers)))
check('follower shapes originate at same sampled wall',all(all(abs((v.co-wall).length-o['radius_m'])<1e-6 for v in o.data.vertices) for o in followers))
check('follower strengths taper',abs(followers[0]['relative_strength']-.32)<1e-6 and abs(followers[1]['relative_strength']-.15)<1e-6)
check('emerald return color on all fronts',all(next(n for n in o.data.materials[0].node_tree.nodes if n.bl_idname=='ShaderNodeEmission').inputs[0].default_value[1]>.5 for o in [echo]+followers))
for name in ('B201_PULSE_ECHO','B201_CONTACT_HISTORY','B201_SPATIAL_GRAPHICS'):check('diagnostic layer excluded '+name,bpy.data.collections[name].hide_render)
check('no local object animation',all(o.animation_data is None for o in s.objects if o.library is None))
q=world_to_camera_view(s,s.camera,receiver);check('reception visible within same camera',0<q.x<1 and 0<q.y<1 and q.z>0)
check('physical time and simulation not claimed',not r['physical_time_claim'] and not r['wave_simulation'])
result={'checks':checks,'passed':all(c['pass'] for c in checks),'executor_self_check':True,'visual_approval':'pending','motion_authorized':False,'Still05_authorized':False}
(E/'verification_still04_v003.json').write_text(json.dumps(result,indent=2));assert result['passed'],[x for x in checks if not x['pass']];print('FIRST_RECEPTION_VERIFY_PASS',len(checks))
