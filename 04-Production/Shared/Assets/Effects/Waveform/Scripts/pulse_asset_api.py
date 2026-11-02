"""Optional authoring helper. Saved v017 assets do not need this module to play."""
import bpy
def get_input(modifier,name):
 socket=next(s for s in modifier.node_group.interface.items_tree if getattr(s,'in_out','')=='INPUT' and s.name==name)
 return getattr(modifier.properties.inputs,socket.identifier).value
def set_input(modifier,name,value):
 socket=next(s for s in modifier.node_group.interface.items_tree if getattr(s,'in_out','')=='INPUT' and s.name==name)
 getattr(modifier.properties.inputs,socket.identifier).value=value
 modifier.id_data.update_tag(refresh={'OBJECT','DATA','TIME'})
def duplicate_instance(template,collection,name,settings=None):
 """Local object and independent modifier values; share immutable mesh/node groups."""
 obj=template.copy();obj.name=name;collection.objects.link(obj)
 for key,value in (settings or {}).items():set_input(obj.modifiers[0],key,value)
 return obj
def arrival_readouts(obj,scene=None):
 """First-cycle absolute frames. Evaluate during visible geometry; quiet = empty."""
 scene=scene or bpy.context.scene;bpy.context.view_layer.update();e=obj.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=e.to_mesh()
 try:
  return {name:mesh.attributes['wf17_'+name].data[0].value for name in ['Send head arrival','Send tail arrival','Return start','Return head arrival','Return tail arrival','Cycle frames'] if 'wf17_'+name in mesh.attributes and len(mesh.vertices)}
 finally:e.to_mesh_clear()
