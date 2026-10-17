import bpy,json
from pathlib import Path
P=Path(__file__).resolve().parents[3]; bpy.ops.wm.open_mainfile(filepath=str(P/'Mechanisms/B201/Scenes/B201_pulse-echo_refinement_v006.blend')); s=bpy.context.scene; s.frame_set(72); bpy.context.window.view_layer=s.view_layers['FAST model and mechanism']
print('TIMING_INSPECT',json.dumps({'cam':list(s.camera.location),'clip':s.camera.data.clip_start,'control':dict(bpy.data.objects['B201_MOTION_CONTROL'].items()),'collections':[(c.name,c.exclude,c.hide_viewport) for c in bpy.context.view_layer.layer_collection.children],'objects':[(o.name,list(o.location),o.hide_render,o.parent.name if o.parent else None) for o in bpy.data.collections['B201_ECHO_TIMING_v006'].objects]}),flush=True)
print('DETAIL',{'cam_hide':s.camera.hide_render,'cam_visibility':s.camera.visible_camera,'mat':[(m.name,[(d.data_path,d.driver.is_valid) for d in m.node_tree.animation_data.drivers] if m.node_tree.animation_data else []) for m in bpy.data.materials if m.name.startswith('TIMING')],'comp':[(n.name,n.scene.name if n.scene else None,n.layer) for n in s.compositing_node_group.nodes if n.bl_idname=='CompositorNodeRLayers'],'scene':s.name,'coll_render':bpy.data.collections['B201_ECHO_TIMING_v006'].hide_render,'layeruse':[(l.name,l.use) for l in s.view_layers]},flush=True)
from bpy_extras.object_utils import world_to_camera_view
bpy.context.view_layer.update()
ob=bpy.data.objects['Timing purpose']; print('PROJECTION',list(s.camera.scale),list(ob.matrix_world.translation),list(world_to_camera_view(s,s.camera,ob.matrix_world.translation)),s.camera.data.clip_end,[(m.name,next(n for n in m.node_tree.nodes if n.bl_idname=='ShaderNodeValue').outputs[0].default_value) for m in bpy.data.materials if m.name.startswith('TIMING')],flush=True)
for c in bpy.context.view_layer.layer_collection.children:
 if c.name not in ('B201_ECHO_TIMING_v006','B201_REVIEW_CAMERA'): c.exclude=True
s.render.filepath=str(P/'Records/Tasks/T-007/Evidence/Motion_v006/timing-isolated.png'); bpy.ops.render.render(write_still=True)
