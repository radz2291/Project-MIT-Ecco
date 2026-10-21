import bpy,json,hashlib,math
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
B=Path(__file__).resolve().parents[1];p=json.loads((B/'Records/build.json').read_text());frames=[63,85,104,206,261,280,300,336,400,432]
def meshhash(o):return hashlib.sha256(repr(([tuple(v.co) for v in o.data.vertices],[tuple(p.vertices) for p in o.data.polygons])).encode()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=p['source'],load_ui=False,use_scripts=False);s=bpy.context.scene;geo={o.name:meshhash(o) for o in s.objects if o.type=='MESH'};depth=[d.value for d in bpy.data.objects['STEEL - capped true source section'].data.attributes['ComputedWearDepth_m'].data];poses={}
for f in frames:
 s.frame_set(f);bpy.context.view_layer.update();poses[f]=(s.camera.matrix_world.copy(),s.camera.data.lens,s.camera.data.shift_x)
bpy.ops.wm.open_mainfile(filepath=p['native'],load_ui=False,use_scripts=False);s=bpy.context.scene;assert geo=={o.name:meshhash(o) for o in s.objects if o.type=='MESH'};steel=bpy.data.objects['STEEL - capped true source section'];assert depth==[d.value for d in steel.data.attributes['ComputedWearDepth_m'].data]
for f,(mx,lens,shift) in poses.items():
 s.frame_set(f);bpy.context.view_layer.update();assert max(abs(mx[i][j]-s.camera.matrix_world[i][j]) for i in range(4) for j in range(4))<3e-6;assert abs(lens-s.camera.data.lens)<1e-6 and abs(shift-s.camera.data.shift_x)<1e-6
for name in p['hidden_helper_curves']:assert bpy.data.objects[name].hide_render
s.frame_set(1);bpy.context.view_layer.update();mx,corners=next((i.matrix_world.copy(),[tuple(x) for x in i.object.bound_box]) for i in bpy.context.evaluated_depsgraph_get().object_instances if i.object.type=='MESH' and i.object.name.startswith('ECCO unchanged source housing'));coords=[mx@Vector(x) for x in corners];uv=[world_to_camera_view(s,s.camera,x) for x in coords];box=[min(x.x for x in uv),max(x.x for x in uv),min(x.y for x in uv),max(x.y for x in uv)];assert box[0]>0 and box[1]<1 and box[2]>0 and box[3]<1
one=set();q=[];samples=[]
for f in range(1,433):
 s.frame_set(f);bpy.context.view_layer.update();one.add(s.camera.name);q.append(s.camera.matrix_world.to_quaternion())
 if f in [85,206,337,400,432]:
  pos=next(i.matrix_world.translation.copy() for i in bpy.context.evaluated_depsgraph_get().object_instances if i.object.name=='ECCO_SENSOR_REF_01');front=steel.data.materials[0].node_tree.nodes['ECCO axial acquisition front'].outputs[0].default_value;assert abs(pos.x-front)<1e-5;samples.append({'frame':f,'sensor_x_m':pos.x,'data_front_x_m':front})
assert len(one)==1;libs=[{'path':l.filepath,'exists':Path(bpy.path.abspath(l.filepath)).is_file()} for l in bpy.data.libraries];assert all(x['exists'] for x in libs);assert hashlib.sha256(Path(p['source']).read_bytes()).hexdigest()==p['source_sha256']
r={'physical_mesh_hashes_identical':True,'computed_wear_values_identical':True,'max_authored_wear_mm':max(depth)*1000,'opening_housing_bbox_screen':box,'camera_from_frame63_unchanged_samples':frames,'one_camera_all432frames':True,'helper_cutting_wire_hidden':p['hidden_helper_curves'],'sensor_data_alignment':samples,'max_rotation_step_degrees':max(math.degrees(a.rotation_difference(b).angle) for a,b in zip(q,q[1:])),'libraries':libs,'previous_version_unchanged':True,'human_visual_review':'pending'};(B/'Records/verification.json').write_text(json.dumps(r,indent=2));print('VERIFIED')
