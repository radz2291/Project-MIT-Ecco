import bpy,json,hashlib,math
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
B=Path(__file__).resolve().parents[1];p=json.loads((B/'Records/build.json').read_text());frames=[1,40,85,94,104,190,206,216,250,261]
bpy.ops.wm.open_mainfile(filepath=p['source'],load_ui=False,use_scripts=False);s=bpy.context.scene;source={};steel=bpy.data.objects['STEEL - capped true source section'];old=[tuple(v.co) for v in steel.data.vertices];olddepth=[d.value for d in steel.data.attributes['ComputedWearDepth_m'].data]
effect_names=[o.name for o in s.objects if o.name.startswith(('STEEL-ATTACHED resonance band','STEEL THICKNESS response','STEEL-BOUND acquisition segment','S02 sourced','Casing response tail'))]
for f in frames:
 s.frame_set(f);bpy.context.view_layer.update();source[f]={'camera':s.camera.matrix_world.copy(),'lens':s.camera.data.lens,'tool':tuple(bpy.data.objects['WORLD_CONTROL'][k] for k in ['travel_m','rotation_rad']),'effects':{n:(bpy.data.objects[n].hide_render,bpy.data.objects[n].matrix_world.copy()) for n in effect_names}}
bpy.ops.wm.open_mainfile(filepath=p['native'],load_ui=False,use_scripts=False);s=bpy.context.scene;steel=bpy.data.objects['STEEL - capped true source section'];assert olddepth==[d.value for d in steel.data.attributes['ComputedWearDepth_m'].data];radial=max(math.hypot(v.co.y-old[i][1],v.co.z-old[i][2]) for i,v in enumerate(steel.data.vertices));assert radial<1e-8
assert abs(min(v.co.x for v in steel.data.vertices)+5.5)<1e-6 and abs(max(v.co.x for v in steel.data.vertices))<1e-6
for f,a in source.items():
 s.frame_set(f);bpy.context.view_layer.update();assert max(abs(s.camera.matrix_world[i][j]-a['camera'][i][j]) for i in range(4) for j in range(4))<2e-6;assert abs(s.camera.data.lens-a['lens'])<1e-5
 assert max(abs(bpy.data.objects['WORLD_CONTROL'][k]-a['tool'][i]) for i,k in enumerate(['travel_m','rotation_rad']))<1e-6
 for n,(hide,mx) in a['effects'].items():
  o=bpy.data.objects[n];assert o.hide_render==hide;assert max(abs(o.matrix_world[i][j]-mx[i][j]) for i in range(4) for j in range(4))<2e-6
names=set();positions=[];q=[];samples=[];scalar=[d.value for d in steel.data.attributes['ComputedWearDepth_m'].data];matrix=steel.matrix_world.copy()
for f in range(1,433):
 s.frame_set(f);bpy.context.view_layer.update();names.add(s.camera.name);positions.append(s.camera.matrix_world.translation.copy());q.append(s.camera.matrix_world.to_quaternion());assert steel.matrix_world==matrix and not steel.hide_render
 if f in [1,85,206,261,280,300,318,336,365,400,432]:
  sensor=next(i.matrix_world.translation.copy() for i in bpy.context.evaluated_depsgraph_get().object_instances if i.object.name=='ECCO_SENSOR_REF_01');front=steel.data.materials[0].node_tree.nodes['ECCO axial acquisition front'].outputs[0].default_value;assert abs(sensor.x-front)<1e-5;samples.append({'frame':f,'sensor_world_m':list(sensor),'reveal_front_m':front})
assert len(names)==1 and scalar==[d.value for d in steel.data.attributes['ComputedWearDepth_m'].data]
libs=[{'path':l.filepath,'exists':Path(bpy.path.abspath(l.filepath)).is_file(),'relative':l.filepath.startswith('//')} for l in bpy.data.libraries];assert all(x['exists'] and x['relative'] for x in libs)
for k in ['source','D_reference']:assert hashlib.sha256(Path(p[k]).read_bytes()).hexdigest()==p[k+'_sha256']
s.frame_set(432);bpy.context.view_layer.update();worn=[steel.matrix_world@v.co for v,d in zip(steel.data.vertices,scalar) if d>.0015];center=sum(worn,Vector())/len(worn);uv=world_to_camera_view(s,s.camera,center);assert .1<uv.x<.6
profiles=[o for o in s.objects if o.name.startswith('Station ') and o.type=='CURVE'];assert sum(not o.hide_render for o in profiles)>=6
r={'native_reopened':True,'ABC_camera_tool_and_effect_samples_preserved':frames,'one_camera_all432frames':True,'fixed_steel_transform':True,'steel_endpoints_preserved':True,'radial_coordinates_unchanged_error_m':radial,'wear_and_scalar_shift_only':True,'max_authored_depth_mm':1000*max(scalar),'profile_visible_objects_at_end':sum(not o.hide_render for o in profiles),'sensor_reveal_alignment':samples,'camera_peak_height_m':max(x.z for x in positions),'max_perframe_camera_step_m':max((b-a).length for a,b in zip(positions,positions[1:])),'max_perframe_rotation_deg':max(math.degrees(a.rotation_difference(b).angle) for a,b in zip(q,q[1:])),'wear_center_screen_fraction':[uv.x,uv.y],'libraries':libs,'sources_unchanged':True,'render_budget_and_full_decode':'See delivery.json after assembly','human_acceptance':'pending'}
(B/'Records/verification.json').write_text(json.dumps(r,indent=2),encoding='utf-8');print('VERIFIED')
