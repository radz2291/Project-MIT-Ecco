import bpy,sys,pathlib,json,math,os,hashlib
from mathutils import Vector
import numpy as np
ROOT=pathlib.Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');TASK=ROOT/'04-Production/Records/Tasks/T-056';OUT=ROOT/'04-Production/Shared/Assets/Acoustics/PressureField_v005'
sys.path.insert(0,str(OUT/'Scripts'));import pressure_model as model
s=bpy.context.scene;original=bpy.data.filepath
for lib in bpy.data.libraries:lib.filepath=bpy.path.abspath(lib.filepath)
projection=json.loads((TASK/'event-projection.json').read_text())
sensor=Vector(projection['frames']['300']['DW 1 SEND front0 core']['world']);wall=Vector(projection['frames']['309']['DW 1 fixed native contact pin']['world']);direction=(wall-sensor).normalized();D=(wall-sensor).length
M=model.Model(gap_m=D);source=model.read_csv(OUT/'Data/source_pulse.csv',OUT/'Data/source_pulse.json')
vertical=Vector((0,0,1));depth=direction.cross(vertical).normalized();col=bpy.data.collections.new('PRESSURE_FIELD_v005');s.collection.children.link(col)
for o in bpy.data.objects:
 if o.name.startswith('DW 1') and any(x in o.name for x in ['SEND','ECHO','contact']):
  o.animation_data_clear();o.hide_render=True;o.hide_viewport=True
ctrl=bpy.data.objects.new('PRESSURE_MODEL_CONTROL_v005',None);col.objects.link(ctrl)
for k,v in model.asdict(M).items():ctrl[k]=v
ctrl['status']='Assumed model-driven proof, NOT measured ECCO or final accepted presentation'
ctrl['physical_time_mapping']='t=(native_frame-300)*(gap/sound_speed)/9; camera animation unchanged'
ctrl['field']='p_out(s,t)+p_reflected(s,t), signed summed pressure sampled at fixed spatial slices'
ctrl['display']='positive cyan / negative blue-violet; opacity and intensity from abs(sum pressure); zero invisible'
ctrl['sample_metadata_json']=json.dumps(source[2])
objects=[];materials=[];positions=np.linspace(.0001,D-.0001,96)
for i,x in enumerate(positions):
 center=sensor+direction*float(x);vertices=[]
 for radius in [.0043,.0045]:
  for j in range(48):
   a=math.tau*j/48;vertices.append(center+vertical*(radius*math.cos(a))+depth*(radius*math.sin(a)))
 faces=[(j,(j+1)%48,(j+1)%48+48,j+48) for j in range(48)]
 mesh=bpy.data.meshes.new(f'PRESSURE_SLICE_{i:03}');mesh.from_pydata(vertices,[],faces);mesh.update()
 ob=bpy.data.objects.new(mesh.name,mesh);col.objects.link(ob);ob['sample_s_m']=float(x)
 mat=bpy.data.materials.new(mesh.name+'_VALUE');mat.diffuse_color=(0,0,0,0);mat.use_nodes=True
 nodes=mat.node_tree.nodes;nodes.clear();em=nodes.new('ShaderNodeEmission');em.name='PressureEmission';output=nodes.new('ShaderNodeOutputMaterial');mat.node_tree.links.new(em.outputs[0],output.inputs[0]);mesh.materials.append(mat)
 objects.append(ob);materials.append(mat)
frames=np.arange(298,324.001,.25);field=[];max_pressure=0
for f in frames:
 physical=(float(f)-300)*(D/M.sound_speed_m_s)/9
 a,b,p=model.components(positions,physical,M,source);field.append(p);max_pressure=max(max_pressure,float(np.max(abs(p))))
 for ob,mat,value in zip(objects,materials,p):
  value=float(value);amplitude=min(1,abs(value)/1.15);visible=abs(value)>=.035
  ob.hide_render=not visible;ob.hide_viewport=not visible;ob.keyframe_insert('hide_render',frame=float(f));ob.keyframe_insert('hide_viewport',frame=float(f))
  ob['signed_pressure']=value;ob.keyframe_insert('["signed_pressure"]',frame=float(f))
  hue=(.10,.88,1.0) if value>=0 else (.38,.30,1.0)
  rgb=tuple(v*amplitude for v in hue);mat.diffuse_color=(*rgb,amplitude);mat.keyframe_insert('diffuse_color',frame=float(f))
  em=mat.node_tree.nodes['PressureEmission'];em.inputs[0].default_value=(*hue,1);em.inputs[0].keyframe_insert('default_value',frame=float(f));em.inputs[1].default_value=4*amplitude;em.inputs[1].keyframe_insert('default_value',frame=float(f))
np.savez_compressed(OUT/'Data/pressure_field_samples.npz',native_frame=frames,physical_time_s=(frames-300)*(D/M.sound_speed_m_s)/9,s_m=positions,signed_pressure=np.asarray(field))
s.render.resolution_x=960;s.render.resolution_y=540;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB'
s.frame_set(305,subframe=.5)
path=OUT/'S02_pressure-field-proof_v005.blend';bpy.ops.wm.save_as_mainfile(filepath=str(path),relative_remap=True)
for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(os.path.normpath(bpy.path.abspath(lib.filepath)))
bpy.ops.wm.save_as_mainfile(filepath=str(path))
checks=[]
for f in [298,303,305.5,309,312,318,324]:
 s.frame_set(math.floor(f),subframe=f%1);bpy.context.view_layer.update()
 geo=[{'matrix':[list(r) for r in o.matrix_world],'vertices':[list(v.co) for v in o.data.vertices]} for o in objects]
 checks.append({'frame':f,'geometry_transform_sha256':hashlib.sha256(json.dumps(geo).encode()).hexdigest(),'visible_slices':sum(not o.hide_render for o in objects)})
(TASK/'pressure-build_v005.json').write_text(json.dumps({'source':original,'output':str(path),'parameters':model.asdict(M),'source_metadata':source[2],'sensor':list(sensor),'wall':list(wall),'sampling_slices':96,'slice_radii_m':[.0043,.0045],'zero_pressure_hidden':True,'display_cutoff':.035,'display_scale':1.15,'max_summed_pressure':max_pressure,'engine':s.render.engine,'camera':s.camera.name,'native_camera_range_preserved':[s.frame_start,s.frame_end],'render_frames':[298,324,.25],'checks':checks,'fixed_geometry_pass':len(set(r['geometry_transform_sha256'] for r in checks))==1,'limits':'1D model; radial discs are display sampling cross-sections, not solved beam width or material displacement'},indent=2))
print('PRESSURE_PROOF_READY',path)
