import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parents[5];T=R/'04-Production/Records/Tasks/T-054';A=R/'04-Production/Shared/Assets';style=A/'DigitalEnvironment/Digital_style_v001.blend'
bpy.ops.wm.open_mainfile(filepath=str(style),load_ui=False);src=bpy.data.materials['Digital earth - charcoal layered solid'].node_tree
g=bpy.data.node_groups.new('ECCO digital earth shader v001','ShaderNodeTree');g.use_fake_user=True;g.interface.new_socket(name='Surface',in_out='OUTPUT',socket_type='NodeSocketShader');nodes={}
for n in src.nodes:
 if n.type=='OUTPUT_MATERIAL':
  nodes[n.name]=g.nodes.new('NodeGroupOutput');continue
 q=g.nodes.new(n.bl_idname);q.name=n.name;nodes[n.name]=q
 for prop in ['operation','use_clamp']:
  if hasattr(n,prop):setattr(q,prop,getattr(n,prop))
 for j,s in enumerate(n.inputs):
  if hasattr(s,'default_value'):
   try:q.inputs[j].default_value=s.default_value
   except (TypeError,ValueError):pass
 if hasattr(n,'color_ramp'):
  for j,e in enumerate(n.color_ramp.elements):
   target=q.color_ramp.elements[j] if j<len(q.color_ramp.elements) else q.color_ramp.elements.new(e.position)
   target.position=e.position;target.color=e.color
  q.color_ramp.interpolation=n.color_ramp.interpolation
for link in src.links:
 a=nodes[link.from_node.name];b=nodes[link.to_node.name];oi=list(link.from_node.outputs).index(link.from_socket);ii=0 if link.to_node.type=='OUTPUT_MATERIAL' else list(link.to_node.inputs).index(link.to_socket);g.links.new(a.outputs[oi],b.inputs[ii])
bpy.ops.wm.save_as_mainfile(filepath=str(style))
records=[]
for sid in ['S03','S06']:
 path=T/'Consumers'/f'{sid}_shared-digital_v002.blend';bpy.ops.wm.open_mainfile(filepath=str(path),load_ui=False)
 names=['SOLID EARTH - borehole cutaway half-space','GROUND FRONT HALF - closes tunnel for interior camera'] if sid=='S03' else ['Rock sectional mass','Rock sectional mass.001','Fixed borehole context | open viewing sector']
 # Empty output prevents local visibility animation from resurrecting old soil.
 empty=bpy.data.node_groups.new(sid+' replaced physical context empty output','GeometryNodeTree');empty.interface.new_socket(name='Geometry',in_out='OUTPUT',socket_type='NodeSocketGeometry');empty.nodes.new('NodeGroupOutput')
 for name in names:bpy.data.objects[name].modifiers.new('Replaced by linked physical World','NODES').node_group=empty
 ob=bpy.data.objects[sid+' | physical World live context']
 if sid=='S06':
  source=bpy.data.objects['Fixed borehole context | open viewing sector'];m=source.data.materials[0].copy();m.name='S06 local visibility | shared digital earth'
  with bpy.data.libraries.load(str(style),link=True) as (a,b):b.node_groups=['ECCO digital earth shader v001']
  gn=m.node_tree.nodes.new('ShaderNodeGroup');gn.node_tree=b.node_groups[0]
  bs=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
  links=list(bs.outputs[0].links)
  for link in links:m.node_tree.links.new(gn.outputs[0],link.to_socket)
  for n in ob.modifiers[0].node_group.nodes:
   if n.bl_idname=='GeometryNodeSetMaterial':n.inputs['Material'].default_value=m
  # Keep old physical object's stage visibility controller, but no old geometry.
  drv=ob.driver_add('hide_render').driver;drv.type='SCRIPTED';v=drv.variables.new();v.name='old_hide';v.type='SINGLE_PROP';v.targets[0].id=source;v.targets[0].data_path='hide_render';drv.expression='old_hide'
 s=bpy.context.scene;checks=[]
 for f in ([1,120,220] if sid=='S03' else [1,52,144,250,288]):
  s.frame_set(f);dep=bpy.context.evaluated_depsgraph_get();checks.append({'frame':f,'old_physical_faces':{n:len(bpy.data.objects[n].evaluated_get(dep).data.polygons) for n in names},'new_hide_render':ob.hide_render,'new_faces':len(ob.evaluated_get(dep).data.polygons)})
 bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(path));records.append({'section':sid,'checks':checks})
(T/'Evidence/context-visibility.json').write_text(json.dumps(records,indent=2));print('CONTEXT_VISIBILITY_FIXED')
