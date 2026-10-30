import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parents[5];A=R/'04-Production/Shared/Assets';T=R/'04-Production/Records/Tasks/T-054';D=A/'DigitalEnvironment';STYLE=D/'Digital_style_v001.blend'
bpy.ops.wm.open_mainfile(filepath=str(STYLE),load_ui=False)
g=bpy.data.node_groups.new('ECCO shared cyan palette v001','ShaderNodeTree');g.use_fake_user=True
for name,typ in [('Color','NodeSocketColor'),('Strength','NodeSocketFloat')]:g.interface.new_socket(name=name,in_out='OUTPUT',socket_type=typ)
out=g.nodes.new('NodeGroupOutput');out.inputs['Color'].default_value=(.025,.22,.29,1);out.inputs['Strength'].default_value=.6
g['source']='Exact S03 v036 HUD restrained cyan contours; local S06 strength/opacity preserved'
m=bpy.data.materials['HUD restrained cyan contours'];n=m.node_tree.nodes.new('ShaderNodeGroup');n.node_tree=g;e=next(x for x in m.node_tree.nodes if x.type=='EMISSION');m.node_tree.links.new(n.outputs['Color'],e.inputs['Color']);m.node_tree.links.new(n.outputs['Strength'],e.inputs['Strength'])
bpy.ops.wm.save_as_mainfile(filepath=str(STYLE))

# Dependent representation: preserve inner local shape; outer X extent comes
# directly from World evaluated mesh bounding box, not a duplicated constant.
bpy.ops.wm.open_mainfile(filepath=str(D/'Digital_world_v001.blend'),load_ui=False)
world_obj=next(o for o in bpy.data.objects if o.library and o.type=='MESH')
g=bpy.data.node_groups.new('ECCO World outer extent adapter v001','GeometryNodeTree');g.use_fake_user=True
for name,typ,side,val in [('Geometry','NodeSocketGeometry','INPUT',None),('Geometry','NodeSocketGeometry','OUTPUT',None),('Keep inner radius','NodeSocketFloat','INPUT',.3),('Original outer X','NodeSocketFloat','INPUT',10)]:
 s=g.interface.new_socket(name=name,in_out=side,socket_type=typ)
 if val is not None:s.default_value=val
i=g.nodes.new('NodeGroupInput');out=g.nodes.new('NodeGroupOutput');l=g.links
def math(op,a,b=None):
 n=g.nodes.new('ShaderNodeMath');n.operation=op
 for k,v in enumerate([a,b]):
  if v is None:continue
  if isinstance(v,(int,float)):n.inputs[k].default_value=v
  else:l.new(v,n.inputs[k])
 return n.outputs[0]
oi=g.nodes.new('GeometryNodeObjectInfo');oi.inputs['Object'].default_value=world_obj;oi.transform_space='ORIGINAL';bb=g.nodes.new('GeometryNodeBoundBox');l.new(oi.outputs['Geometry'],bb.inputs[0]);bs=g.nodes.new('ShaderNodeSeparateXYZ');l.new(bb.outputs['Max'],bs.inputs[0])
p=g.nodes.new('GeometryNodeInputPosition');s=g.nodes.new('ShaderNodeSeparateXYZ');l.new(p.outputs[0],s.inputs[0]);x=s.outputs['X'];inner=i.outputs['Keep inner radius']
ratio=math('DIVIDE',math('SUBTRACT',bs.outputs['Y'],inner),math('SUBTRACT',i.outputs['Original outer X'],inner))
target=math('MULTIPLY',math('ADD',math('MULTIPLY',math('SUBTRACT',math('ABSOLUTE',x),inner),ratio),inner),math('SIGN',x))
combine=g.nodes.new('ShaderNodeCombineXYZ');l.new(target,combine.inputs['X']);l.new(s.outputs['Y'],combine.inputs['Y']);l.new(s.outputs['Z'],combine.inputs['Z'])
sp=g.nodes.new('GeometryNodeSetPosition');l.new(i.outputs[0],sp.inputs[0]);l.new(math('GREATER_THAN',math('ABSOLUTE',x),inner),sp.inputs['Selection']);l.new(combine.outputs[0],sp.inputs['Position']);l.new(sp.outputs[0],out.inputs[0])
g['policy']='Dependent section representation. Inner borehole/data geometry remains local; only outside keep radius expands to current World Y extent. Section axes remain Z. No measured sample replacement.'
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(D/'Digital_world_v001.blend'))

for sid in ['S03','S06']:
 path=T/'Consumers'/f'{sid}_shared-digital_v001.blend';bpy.ops.wm.open_mainfile(filepath=str(path),load_ui=False)
 with bpy.data.libraries.load(str(STYLE),link=True) as (a,b):b.node_groups=['ECCO shared cyan palette v001']
 palette=b.node_groups[0]
 if sid=='S06':
  for m in bpy.data.materials:
   if m.library or not m.name.startswith('T054 local opacity'):continue
   n=m.node_tree.nodes.new('ShaderNodeGroup');n.node_tree=palette
   for e in m.node_tree.nodes:
    if e.type=='EMISSION':m.node_tree.links.new(n.outputs['Color'],e.inputs['Color'])
 with bpy.data.libraries.load(str(D/'Digital_world_v001.blend'),link=True) as (a,b):b.node_groups=['ECCO World outer extent adapter v001']
 ext=b.node_groups[0]
 targets=['SOLID EARTH - borehole cutaway half-space','GROUND FRONT HALF - closes tunnel for interior camera'] if sid=='S03' else ['Rock sectional mass','Rock sectional mass.001']
 for name in targets:
  o=bpy.data.objects[name];m=o.modifiers.new('Shared World outer extent; inner shape retained','NODES')
  wrapper=bpy.data.node_groups.new('Local extent parameters | '+name,'GeometryNodeTree')
  wrapper.interface.new_socket(name='Geometry',in_out='INPUT',socket_type='NodeSocketGeometry');wrapper.interface.new_socket(name='Geometry',in_out='OUTPUT',socket_type='NodeSocketGeometry')
  wi=wrapper.nodes.new('NodeGroupInput');wo=wrapper.nodes.new('NodeGroupOutput');gn=wrapper.nodes.new('GeometryNodeGroup');gn.node_tree=ext
  gn.inputs['Original outer X'].default_value=10 if sid=='S03' else .7517164;gn.inputs['Keep inner radius'].default_value=.3
  wrapper.links.new(wi.outputs[0],gn.inputs[0]);wrapper.links.new(gn.outputs[0],wo.inputs[0]);m.node_group=wrapper
 bpy.context.scene['integration_scope']='Live shared cyan/soil materials and World-driven outer soil extent. Inner local shape, sample values, transforms, opacity and unfold remain local.'
 bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(path))
print('REFINE_DONE')
