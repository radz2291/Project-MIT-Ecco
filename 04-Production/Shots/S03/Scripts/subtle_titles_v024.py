"""Reduce the two fixed S03 title overlays."""
import bpy
from pathlib import Path

shot = Path(__file__).resolve().parents[1]
candidate = shot / "Scenes/S03_subtle-titles_v024.blend"
assert not candidate.exists()
material = bpy.data.materials.new("S03 titles | muted blue-white")
material.diffuse_color = (0.45, 0.58, 0.64, 1)
material.use_nodes = True
tree = material.node_tree
tree.nodes.clear()
emission = tree.nodes.new("ShaderNodeEmission")
emission.inputs["Color"].default_value = material.diffuse_color
emission.inputs["Strength"].default_value = 0.72
output = tree.nodes.new("ShaderNodeOutputMaterial")
tree.links.new(emission.outputs[0], output.inputs["Surface"])
names = ("GEOMETRY THROUGH DEPTH", "ACOUSTIC AMPLITUDE  |  RECORDED DATA")
for name in names:
    title = bpy.data.objects[name]
    title.data.size = 0.021
    title.data.materials.clear()
    title.data.materials.append(material)

bpy.context.scene.frame_set(380)
bpy.ops.wm.save_as_mainfile(filepath=str(candidate), relative_remap=True)
bpy.ops.wm.open_mainfile(filepath=str(candidate))
for name in names:
    title = bpy.data.objects[name]
    assert abs(title.data.size - 0.021) < 1e-6
    assert title.parent == bpy.context.scene.camera
    assert title.data.materials[0].name == "S03 titles | muted blue-white"
assert not bpy.data.objects[names[1]].hide_render
