import bpy
s=bpy.context.scene
print('SCENE COMPOSITOR',hasattr(s,'node_tree'),hasattr(s,'use_nodes'),hasattr(s,'compositing_node_group'))
print('COMPOSITOR PROPERTIES',[p.identifier for p in s.bl_rna.properties if 'composit' in p.identifier or 'node' in p.identifier])
