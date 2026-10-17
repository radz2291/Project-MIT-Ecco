import bpy
n=bpy.data.node_groups.new('inspect','CompositorNodeTree')
for typ in ['CompositorNodeAlphaOver','CompositorNodeGlare','CompositorNodeRLayers']:
 x=n.nodes.new(typ);print(typ,[(i.name,i.identifier,i.type,str(i.default_value) if hasattr(i,'default_value') else '') for i in x.inputs]);print('props',[(p.identifier,p.type) for p in x.bl_rna.properties if p.identifier in ['glare_type','size','quality','layer']])
