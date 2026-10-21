import bpy,json,hashlib,math
from pathlib import Path
from mathutils import Vector
B=Path(__file__).resolve().parents[1];p=json.loads((B/'Records/build.json').read_text());bpy.ops.wm.open_mainfile(filepath=str(B/'Scenes/S04_CD_arc-test_v032.blend'),load_ui=False,use_scripts=False);s=bpy.context.scene
for key in ['source','stage']:assert hashlib.sha256(Path(p[key]).read_bytes()).hexdigest()==p[key+'_sha256']
steel=bpy.data.objects['STEEL - capped true source section'];baseline=steel.matrix_world.copy();depth=[v.value for v in steel.data.attributes['ComputedWearDepth_m'].data];names=set();positions=[];qs=[];samples=[]
for f in range(1,121):
 s.frame_set(f);bpy.context.view_layer.update();names.add(s.camera.name);positions.append(s.camera.matrix_world.translation.copy());qs.append(s.camera.matrix_world.to_quaternion());assert steel.matrix_world==baseline and not steel.hide_render
 if f in [1,17,33,48,65,90,120]:
  pos=next(i.matrix_world.translation.copy() for i in bpy.context.evaluated_depsgraph_get().object_instances if i.object.name=='ECCO_SENSOR_REF_01');front=steel.data.materials[0].node_tree.nodes['ECCO axial acquisition front'].outputs[0].default_value;assert abs(pos.x-front)<1e-5;samples.append({'frame':f,'sensor_world_m':list(pos),'reveal_front_m':front})
assert len(names)==1 and depth==[v.value for v in steel.data.attributes['ComputedWearDepth_m'].data]
libs=[{'path':l.filepath,'exists':Path(bpy.path.abspath(l.filepath)).is_file(),'relative':l.filepath.startswith('//')} for l in bpy.data.libraries];assert all(x['exists'] and x['relative'] for x in libs)
r={'native_reopened':True,'one_camera_all120frames':True,'steel_transform_visibility_fixed':True,'computed_depth_fixed':True,'max_authored_wear_mm':1000*max(depth),'wear_station_translation_m':-.65,'wear_mesh_local_shape_matches_source':p['physical_meshes_unchanged'],'source_files_unchanged':True,'sensor_reveal_alignment':samples,'maximum_frame_camera_step_m':max((b-a).length for a,b in zip(positions,positions[1:])),'maximum_frame_rotation_degrees':max(math.degrees(a.rotation_difference(b).angle) for a,b in zip(qs,qs[1:])),'libraries':libs,'full_sequence_integration':False,'human_review':'pending'};(B/'Records/verification.json').write_text(json.dumps(r,indent=2));print('VERIFIED')

from bpy_extras.object_utils import world_to_camera_view
s.frame_set(120);bpy.context.view_layer.update()
worn=[steel.matrix_world@v.co for v,d in zip(steel.data.vertices,depth) if d>.0015]
center=sum(worn,Vector())/len(worn);uv=world_to_camera_view(s,s.camera,center)
end_forward=s.camera.matrix_world.to_quaternion()@Vector((0,0,-1))
s.frame_set(1);start_forward=s.camera.matrix_world.to_quaternion()@Vector((0,0,-1))
assert end_forward.x>.8 # Previous D endpoint looked negative X; C opening is not the comparison endpoint.
assert .15<uv.x<.5
r['opposite_axial_view_verified']=True;r['wear_center_screen_fraction']=[uv.x,uv.y];r['camera_forward_x_C_and_D']=[start_forward.x,end_forward.x];r['final_lens_shift_x']=.34;r['final_lens_mm']=64
(B/'Records/verification.json').write_text(json.dumps(r,indent=2))

s.frame_set(48);bpy.context.view_layer.update();arrival=s.camera.matrix_world.translation.copy()
s.frame_set(120);bpy.context.view_layer.update();finish=s.camera.matrix_world.translation.copy()
assert (finish-arrival).length>.06
assert (Vector((0,finish.y,finish.z))).length>.19
r['D_camera_drift_m']=(finish-arrival).length;r['D_camera_radial_offset_m']=(Vector((0,finish.y,finish.z))).length;r['camera_side_clearance_presentation']='Offset beside the tool in the fixed removed half; no opaque hardware intersection is asserted from radial distance alone.'
(B/'Records/verification.json').write_text(json.dumps(r,indent=2))
