import bpy
s=bpy.context.scene
for name in ['S05_v007_SectionedFluid','S05_v007_InnerFluidInterface','S05_v007_FluidSectionFace']:
 bpy.data.materials[name].surface_render_method='BLENDED'
for name,color in [('Body',(.075,.067,.055)),('Light',(.29,.25,.19)),('Dark',(.018,.016,.012))]:
 bpy.data.materials['S05_v007_Cutting'+name].node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(*color,1)
s.eevee.taa_render_samples=16
s.frame_set(36);s.render.filepath='//../Work/Frames/S05_'
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
result={'samples':16,'surface_method':'BLENDED','native_saved':bpy.data.filepath}
