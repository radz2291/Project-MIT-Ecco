import bpy
from pathlib import Path
R=Path(__file__).resolve().parents[5];T=R/'04-Production/Records/Tasks/T-054';path=T/'Consumers/S02_shared-reveal_v001.blend';lib=R/'04-Production/Shared/Assets/MeasurementReveal/Measurement_reveal_v001.blend'
bpy.ops.wm.open_mainfile(filepath=str(path),load_ui=False)
source=bpy.data.objects['ONE WALL - old history and current cells share topology']
with bpy.data.libraries.load(str(lib),link=True) as (a,b):b.node_groups=['ECCO Fine Surface Style v001']
g=bpy.data.node_groups.new('S02 shared fine stored-history overlay','GeometryNodeTree');g.interface.new_socket(name='Geometry',in_out='OUTPUT',socket_type='NodeSocketGeometry');l=g.links
oi=g.nodes.new('GeometryNodeObjectInfo');oi.inputs['Object'].default_value=source;oi.transform_space='ORIGINAL'
attr=g.nodes.new('GeometryNodeInputNamedAttribute');attr.data_type='FLOAT';attr.inputs['Name'].default_value='ecco_reveal_order'
less=g.nodes.new('ShaderNodeMath');less.operation='LESS_THAN';l.new(attr.outputs['Attribute'],less.inputs[0]);less.inputs[1].default_value=0
delete=g.nodes.new('GeometryNodeDeleteGeometry');delete.domain='FACE';l.new(oi.outputs['Geometry'],delete.inputs[0]);l.new(less.outputs[0],delete.inputs['Selection'])
fine=g.nodes.new('GeometryNodeGroup');fine.node_tree=b.node_groups[0];fine.inputs['Point radius'].default_value=.00035;fine.inputs['Line radius'].default_value=.00012;l.new(delete.outputs[0],fine.inputs[0]);out=g.nodes.new('NodeGroupOutput');l.new(fine.outputs[0],out.inputs[0])
o=bpy.data.objects.new('Stored history | shared fine display overlay',bpy.data.meshes.new('Overlay carrier'));bpy.context.scene.collection.objects.link(o);o.matrix_world=source.matrix_world;o.modifiers.new('Shared S06-like points lines surface','NODES').node_group=g
o['meaning']='Read-only geometry dependency on local stored-wall evaluated mesh; excludes current acquisition row. Original source sample/material values remain below overlay.'
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(path));print('FINE_OVERLAY_DONE')
