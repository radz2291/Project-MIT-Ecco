import bpy,pathlib,json,math
from mathutils import Vector
T=pathlib.Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/Records/Tasks/T-056');s=bpy.context.scene;axis=Vector((.00880720093846321,-.02294353395700455,0));gap=axis.length;axis.normalize();up=Vector((0,0,1));depth=axis.cross(up).normalized();wall=bpy.data.objects['DEMO_WALL'];material=wall.data.materials[0];bpy.data.objects.remove(wall,do_unlink=True)
bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=.025,depth=.006,location=axis*(gap+.003));wall=bpy.context.object;wall.name='DEMO_WALL';wall.rotation_mode='QUATERNION';wall.rotation_quaternion=up.rotation_difference(axis);wall.data.materials.append(material)
for name,color in [('Demo wall — neutral',(.15,.105,.065,1)),('Demo sensor — neutral',(.22,.27,.31,1))]:
 m=bpy.data.materials[name];m.use_nodes=True;p=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED');p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=.6
target=axis*gap*.5;cam=s.camera;cam.location=target+depth*.13+up*.035-axis*.035;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=50
for name in ['DEMO_KEY','DEMO_FILL']:bpy.data.objects[name].data.energy*=.15
for screen in bpy.data.screens:
 for area in screen.areas:
  if area.type=='VIEW_3D':area.spaces.active.region_3d.view_location=target;area.spaces.active.region_3d.view_rotation=cam.rotation_euler.to_quaternion();area.spaces.active.region_3d.view_distance=.14
bpy.ops.object.select_all(action='DESELECT');ctrl=bpy.data.objects['WF_MASTER_CONTROLS'];ctrl.select_set(True);bpy.context.view_layer.objects.active=ctrl;bpy.data.orphans_purge(do_recursive=True);bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath);print('DEMO_VIEW_FIXED')
