import bpy
from pathlib import Path
R=Path(__file__).resolve().parents[5];T=R/'04-Production/Records/Tasks/T-054';p=T/'Consumers/S03_shared-digital_v002.blend';bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False)
target=bpy.data.objects['S03 | physical World live context']
for name in ['Luminous geological strata','Subordinate formation survey grid']:
 o=bpy.data.objects[name]
 for m in list(o.modifiers):
  if m.type=='SHRINKWRAP':o.modifiers.remove(m)
 g=bpy.data.node_groups.new(name+' local sampling for live cap','GeometryNodeTree');g.interface.new_socket(name='Geometry',in_out='INPUT',socket_type='NodeSocketGeometry');g.interface.new_socket(name='Geometry',in_out='OUTPUT',socket_type='NodeSocketGeometry');i=g.nodes.new('NodeGroupInput');out=g.nodes.new('NodeGroupOutput');r=g.nodes.new('GeometryNodeResampleCurve');r.mode='LENGTH';r.inputs['Length'].default_value=.025;g.links.new(i.outputs[0],r.inputs[0]);g.links.new(r.outputs[0],out.inputs[0]);o.modifiers.new('Resample for shared cap contours','NODES').node_group=g
 m=o.modifiers.new('Project context styling onto shared soil cap','SHRINKWRAP');m.target=target;m.wrap_method='PROJECT';m.wrap_mode='ABOVE_SURFACE';m.use_project_x=False;m.use_project_y=True;m.use_project_z=False;m.use_positive_direction=True;m.use_negative_direction=False;m.offset=.008
bpy.ops.wm.save_as_mainfile(filepath=str(p));print('CONTEXT_RESAMPLED')
