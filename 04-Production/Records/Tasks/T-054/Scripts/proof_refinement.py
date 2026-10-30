import bpy
from pathlib import Path
R=Path(__file__).resolve().parents[5];T=R/'04-Production/Records/Tasks/T-054';p=R/'04-Production/Shared/Assets/MeasurementReveal/Measurement_reveal_v001.blend'
bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False)
g=bpy.data.node_groups['ECCO Stored Surface Reveal v001'];attrs=[n for n in g.nodes if n.bl_idname=='GeometryNodeInputNamedAttribute'];delete=next(n for n in g.nodes if n.bl_idname=='GeometryNodeDeleteGeometry');old=delete.inputs['Selection'].links[0].from_socket
both=g.nodes.new('FunctionNodeBooleanMath');both.operation='AND'
g.links.new(attrs[0].outputs['Exists'],both.inputs[0]);g.links.new(attrs[1].outputs['Exists'],both.inputs[1]);neg=g.nodes.new('FunctionNodeBooleanMath');neg.operation='NOT';g.links.new(both.outputs[0],neg.inputs[0]);either=g.nodes.new('FunctionNodeBooleanMath');either.operation='OR';g.links.new(neg.outputs[0],either.inputs[0]);g.links.new(old,either.inputs[1]);g.links.new(either.outputs[0],delete.inputs['Selection'])
g['missing_attributes']='Fail closed: no geometry shown unless both receipt and reveal-order attributes exist.'
m=bpy.data.materials.new('S06 fine-point guide reference v001');m.use_nodes=True;m.diffuse_color=(.2,.46,.72,1);nt=m.node_tree;nt.nodes.clear();e=nt.nodes.new('ShaderNodeEmission');e.inputs[0].default_value=(.2,.46,.72,1);e.inputs[1].default_value=1.4;out=nt.nodes.new('ShaderNodeOutputMaterial');nt.links.new(e.outputs[0],out.inputs[0]);m['source']='Exact S06 v004 A guide color .2,.46,.72 emission1.4'
style=bpy.data.node_groups['ECCO Fine Surface Style v001']
for n in style.nodes:
 if n.bl_idname=='GeometryNodeSetMaterial' and n.inputs['Material'].default_value and 'translucent' not in n.inputs['Material'].default_value.name:n.inputs['Material'].default_value=m
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(p))
f=T/'Consumers/Reveal_two-shapes_v001.blend';bpy.ops.wm.open_mainfile(filepath=str(f),load_ui=False);s=bpy.context.scene;s.camera.data.ortho_scale=5.2;s.world.use_nodes=True;s.world.node_tree.nodes.get('Background').inputs[0].default_value=(.004,.008,.014,1);s.world.node_tree.nodes.get('Background').inputs[1].default_value=.2;s.view_settings.view_transform='Standard';bpy.ops.wm.save_as_mainfile(filepath=str(f))
print('PROOF_REFINED')
