"""Temporary inspection camera in a background process; source is never saved."""
import bpy,sys
from mathutils import Vector
s=bpy.context.scene
camera_data=bpy.data.cameras.new('A02 inspection camera')
camera=bpy.data.objects.new('A02 inspection camera',camera_data)
s.collection.objects.link(camera)
camera.location=(1.2,-3.5,1.4)
camera.rotation_euler=(Vector((1.2,0,0))-camera.location).to_track_quat('-Z','Y').to_euler()
camera_data.type='ORTHO';camera_data.ortho_scale=2.85;s.camera=camera
s.render.engine='BLENDER_WORKBENCH'
s.display.shading.light='STUDIO';s.display.shading.color_type='SINGLE';s.display.shading.single_color=(0.55,0.58,0.62)
s.display.shading.show_cavity=True;s.display.shading.cavity_type='BOTH'
s.display.shading.background_type='VIEWPORT';s.display.shading.background_color=(0.08,0.08,0.08)
s.render.resolution_x=1200;s.render.resolution_y=420;s.render.resolution_percentage=100
s.render.image_settings.file_format='PNG';s.render.filepath=sys.argv[sys.argv.index('--')+1]
bpy.ops.render.render(write_still=True)
