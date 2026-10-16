"""Preview-only EEVEE consumer of accepted geometry. No source master mutations."""
import bpy
from mathutils import Matrix

def configure(scene,samples=32):
    # Bake only the product's evaluated instances visible in the original model layer.
    # Exact evaluated meshes/transforms retained; presentation material is a local copy.
    original=scene.view_layers['Approved model look'].material_override
    product=bpy.data.collections.new('FAST_PREVIEW_PRODUCT');scene.collection.children.link(product)
    root=bpy.data.objects.new('FAST_PREVIEW_TOOL_ROTATION',None);product.objects.link(root)
    material=original.copy();material.name='FAST_PREVIEW_LOCAL_PRODUCT_LOOK'
    shader=next(n for n in material.node_tree.nodes if n.bl_idname=='ShaderNodeBsdfPrincipled')
    shader.inputs['Metallic'].default_value=.15
    shader.inputs['Roughness'].default_value=.45
    instances=[]
    for inst in bpy.context.evaluated_depsgraph_get().object_instances:
        ob=inst.object
        if not inst.is_instance or ob.type!='MESH' or ob.hide_render:continue
        if not (ob.name.startswith('TEMP |') or ob.name=='ECCO_HOUSING_SOURCE_MESH'):continue
        mesh=ob.to_mesh();copy=mesh.copy();ob.to_mesh_clear()
        o=bpy.data.objects.new('PREVIEW | '+ob.name,copy);product.objects.link(o)
        o.matrix_world=inst.matrix_world.copy();o.parent=root
        copy.materials.clear();copy.materials.append(material)
        instances.append({'source':ob.name,'consumer':o.name,'vertices':len(copy.vertices),'matrix':[list(row) for row in o.matrix_world]})
    assert len(instances)>=10,instances
    for layer in scene.view_layers:layer.use=False
    layer=scene.view_layers.new('FAST model and mechanism');layer.material_override=None
    allowed={product.name,'STILL03_WALL_CONTACT','STILL02_ILLUSTRATIVE_WAVEFRONT','B201_REVIEW_CAMERA','STILL01_LIGHTING'}
    for child in layer.layer_collection.children:child.exclude=child.name not in allowed
    scene.render.engine='BLENDER_EEVEE';scene.eevee.taa_render_samples=samples;scene.eevee.use_raytracing=False
    scene.render.resolution_x=960;scene.render.resolution_y=540;scene.render.resolution_percentage=100
    scene.render.film_transparent=True;scene.render.use_persistent_data=True
    for ob in bpy.data.collections['STILL01_LIGHTING'].objects:
        if ob.type=='LIGHT' and hasattr(ob.data,'use_shadow'):ob.data.use_shadow=False
    for ob in bpy.data.collections['STILL02_ILLUSTRATIVE_WAVEFRONT'].objects:
        if ob.type!='MESH':continue
        for mat in ob.data.materials:
            mat.surface_render_method='BLENDED'
            if hasattr(mat,'use_transparency_overlap'):mat.use_transparency_overlap=True
            nodes=mat.node_tree.nodes;links=mat.node_tree.links
            mix=next((n for n in nodes if n.bl_idname=='ShaderNodeMixShader'),None)
            if mix and mix.inputs[0].is_linked:
                old=mix.inputs[0].links[0].from_socket;gain=nodes.new('ShaderNodeMath');gain.operation='MULTIPLY';gain.inputs[1].default_value=.65;links.new(old,gain.inputs[0]);links.new(gain.outputs[0],mix.inputs[0])
    # Native transparent sorting and opaque depth replace stochastic Z compositing.
    g=scene.compositing_node_group;g.nodes.clear();n=g.nodes;l=g.links
    render=n.new('CompositorNodeRLayers');render.scene=scene;render.layer=layer.name
    black=n.new('CompositorNodeRGB');black.outputs[0].default_value=(0,0,0,1)
    over=n.new('CompositorNodeAlphaOver');l.new(black.outputs[0],over.inputs['Background']);l.new(render.outputs['Image'],over.inputs['Foreground'])
    glow=n.new('CompositorNodeGlare');glow.inputs['Type'].default_value='Fog Glow';glow.inputs['Quality'].default_value='Medium';glow.inputs['Size'].default_value=.05;glow.inputs['Strength'].default_value=.1;l.new(over.outputs[0],glow.inputs['Image'])
    output=n.new('NodeGroupOutput');l.new(glow.outputs[0],output.inputs['Image'])
    return root,material,instances
