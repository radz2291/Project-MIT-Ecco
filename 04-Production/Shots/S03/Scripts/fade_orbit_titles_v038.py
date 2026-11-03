"""Ease both camera-fixed titles in and out without overlap."""
import bpy
from pathlib import Path
from time import perf_counter

shot = Path(__file__).resolve().parents[1]
candidate = shot / "Scenes/S03_title-fades_v038.blend"
assert not candidate.exists()
scene = bpy.context.scene
titles = {
    "GEOMETRY THROUGH DEPTH": ((280,0),(290,1),(301,1),(312,0)),
    "ACOUSTIC AMPLITUDE  |  RECORDED DATA": ((313,0),(327,1),(530,1),(552,0)),
}
for name, keys in titles.items():
    obj = bpy.data.objects[name]
    assert obj.parent == scene.camera
    material = obj.data.materials[0].copy()
    obj.data.materials[0] = material
    tree = material.node_tree
    output = next(n for n in tree.nodes if n.type == "OUTPUT_MATERIAL" and n.is_active_output)
    original = output.inputs["Surface"].links[0].from_socket
    transparent = tree.nodes.new("ShaderNodeBsdfTransparent")
    mix = tree.nodes.new("ShaderNodeMixShader")
    mix.label = "Orbit title fade"
    tree.links.new(transparent.outputs[0], mix.inputs[1])
    tree.links.new(original, mix.inputs[2])
    tree.links.new(mix.outputs[0], output.inputs["Surface"])
    for frame,value in keys:
        mix.inputs[0].default_value = value
        mix.inputs[0].keyframe_insert("default_value",frame=frame)

scene.frame_set(320)
bpy.ops.wm.save_as_mainfile(filepath=str(candidate),relative_remap=True)
bpy.ops.wm.open_mainfile(filepath=str(candidate))
scene = bpy.context.scene
for name, keys in titles.items():
    obj = bpy.data.objects[name]
    factor = next(n for n in obj.data.materials[0].node_tree.nodes if n.label == "Orbit title fade").inputs[0]
    for frame,value in keys:
        scene.frame_set(frame)
        assert abs(factor.default_value-value) < 1e-6
    for frame in ((keys[0][0]+keys[1][0])//2,(keys[2][0]+keys[3][0])//2):
        scene.frame_set(frame)
        assert not obj.hide_render and 0 < factor.default_value < 1
print("VERIFIED both title fades",flush=True)
scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.render.resolution_percentage = 100
scene.eevee.taa_render_samples = 8
scene.eevee.use_raytracing = False
scene.render.use_compositing = False
for frame in (286,320,542):
    scene.frame_set(frame)
    scene.camera.data.update_tag()
    bpy.context.view_layer.update()
    scene.render.filepath = str(shot/f"Previews/S03_title-fades_v038_f{frame:04d}.png")
    start = perf_counter()
    bpy.ops.render.render(write_still=True)
    print("STILL",frame,round(perf_counter()-start,3),flush=True)
