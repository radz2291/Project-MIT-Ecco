"""Proof-only EEVEE adapter; model/slice geometry and source camera stay unchanged."""
import bpy,pathlib,json,os
from mathutils import Vector
ROOT=pathlib.Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');TASK=ROOT/'04-Production/Records/Tasks/T-056';OUT=ROOT/'04-Production/Shared/Assets/Acoustics/PressureField_v006';OUT.mkdir(parents=True,exist_ok=True)
s=bpy.context.scene;s.frame_set(305,subframe=.5)
for lib in bpy.data.libraries:lib.filepath=bpy.path.abspath(lib.filepath)
def drive(socket,index,mat,path):
 fc=socket.driver_add('default_value',index) if index is not None else socket.driver_add('default_value')
 var=fc.driver.variables.new();var.name='value';var.type='SINGLE_PROP';var.targets[0].id_type='MATERIAL';var.targets[0].id=mat;var.targets[0].data_path=path;fc.driver.expression='value'
used={m for o in s.objects for m in getattr(o.data,'materials',[]) if m}
adapt=[]
for mat in used:
 if mat.library:continue
 ispressure=mat.name.startswith('PRESSURE_SLICE_')
 mat.use_nodes=True;nt=mat.node_tree;nt.animation_data_clear();nt.nodes.clear()
 out=nt.nodes.new('ShaderNodeOutputMaterial');mix=nt.nodes.new('ShaderNodeMixShader');transparent=nt.nodes.new('ShaderNodeBsdfTransparent')
 shader=nt.nodes.new('ShaderNodeEmission' if ispressure else 'ShaderNodeBsdfDiffuse')
 nt.links.new(transparent.outputs[0],mix.inputs[1]);nt.links.new(shader.outputs[0],mix.inputs[2]);nt.links.new(mix.outputs[0],out.inputs[0])
 for k in range(3):drive(shader.inputs[0],k,mat,f'diffuse_color[{k}]')
 shader.inputs[0].default_value[3]=1
 drive(mix.inputs[0],None,mat,'diffuse_color[3]')
 if ispressure:shader.inputs[1].default_value=5.0
 else:shader.inputs[1].default_value=.6
 mat.surface_render_method='DITHERED';mat.use_transparency_overlap=False
 adapt.append({'material':mat.name,'pressure':ispressure,'alpha':float(mat.diffuse_color[3])})
s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=8
s.render.resolution_x=640;s.render.resolution_y=360;s.render.resolution_percentage=100
for name,offset,power,size in [('Proof_Key',(0,0,0),8,.18),('Proof_Fill',(0,0,.12),3,.25)]:
 data=bpy.data.lights.new(name,'AREA');data.energy=power;data.shape='DISK';data.size=size
 ob=bpy.data.objects.new(name,data);s.collection.objects.link(ob);ob.location=s.camera.matrix_world.translation+Vector(offset)
 target=Vector((.047,-.122,-729.53));ob.rotation_euler=(target-ob.location).to_track_quat('-Z','Y').to_euler()
s.world=bpy.data.worlds.new('Pressure_proof_world');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.08,.09,.11,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.2
path=OUT/'S02_pressure-field-proof_v006.blend';bpy.ops.wm.save_as_mainfile(filepath=str(path),relative_remap=True)
for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(os.path.normpath(bpy.path.abspath(lib.filepath)))
bpy.ops.wm.save_as_mainfile(filepath=str(path))
(TASK/'pressure-adapter_v006.json').write_text(json.dumps({'output':str(path),'source_model':'PressureField_v005/Data','camera_untouched':s.camera.name,'pressure_geometry':'unchanged from v005','adapter':'existing local materials diffuse viewport color and alpha; added simple fixture lighting; pressure emissive transparent mix','resolution':[640,360],'samples':8,'materials':adapt},indent=2))
