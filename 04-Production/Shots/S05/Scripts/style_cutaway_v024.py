"""Shade the existing S05 cutaway to sit with the navy room."""

from hashlib import sha256
import json
from pathlib import Path
from time import perf_counter

import bpy


shot = Path(__file__).resolve().parents[1]
output = shot / "Scenes/S05_stylized-cutaway_v024.blend"
frames = (50, 205, 432)
scene = bpy.context.scene
wall_name = "S05_FixedHalfBorehole"
assert Path(bpy.data.filepath).name == "S05_navy-room_v023.blend"
assert not output.exists()


def geometry_signature(obj):
    mesh = obj.data
    return sha256(repr((
        [tuple(vertex.co) for vertex in mesh.vertices],
        [(tuple(face.vertices), face.material_index) for face in mesh.polygons],
    )).encode("utf-8")).hexdigest()


def shot_state(scene):
    collections = ("S05 Navy room", "S05_v018_ContinuousHydraulics")
    tracked = [scene.objects[name] for name in (wall_name, "S05 Shared BHA v008", "S05 Shared uphole joint")]
    for name in collections:
        tracked.extend(sorted(scene.collection.children[name].all_objects, key=lambda obj: obj.name))
    samples = []
    for frame in frames:
        scene.frame_set(frame)
        camera = scene.camera
        objects = []
        for obj in tracked:
            slots = tuple(slot.material.name for slot in obj.material_slots if slot.material)
            objects.append((obj.name, tuple(tuple(row) for row in obj.matrix_world), obj.hide_render,
                            slots if obj.name != wall_name else ()))
        samples.append((tuple(tuple(row) for row in camera.matrix_world),
                        camera.data.lens, camera.data.dof.focus_distance,
                        camera.data.shift_x, camera.data.shift_y, objects))
    return samples


def wall_material(original, name, dark, light, is_cut_face):
    material = original.copy()
    material.name = name
    material.diffuse_color = (*light, 1)
    tree = material.node_tree
    nodes, links = tree.nodes, tree.links
    for node in list(nodes):
        if node.type in {"TEX_NOISE", "BUMP"}:
            nodes.remove(node)
    shader = next(node for node in nodes if node.type == "BSDF_PRINCIPLED")
    shader.inputs["Roughness"].default_value = 0.86 if is_cut_face else 0.91

    coords = nodes.new("ShaderNodeTexCoord")
    coords.location = (-780, 100)
    mottling = nodes.new("ShaderNodeTexNoise")
    mottling.label = "Stone tone variation"
    mottling.location = (-560, 250)
    mottling.inputs["Scale"].default_value = 26
    mottling.inputs["Detail"].default_value = 3
    links.new(coords.outputs["Object"], mottling.inputs["Vector"])
    palette = nodes.new("ShaderNodeValToRGB")
    palette.location = (-330, 250)
    for element, position, color in zip(palette.color_ramp.elements, (0.23, 0.78), (dark, light)):
        element.position = position
        element.color = (*color, 1)
    links.new(mottling.outputs["Fac"], palette.inputs["Fac"])

    pores = nodes.new("ShaderNodeTexNoise")
    pores.label = "Fine surface grain"
    pores.location = (-560, -140)
    pores.inputs["Scale"].default_value = 120
    pores.inputs["Detail"].default_value = 2
    links.new(coords.outputs["Object"], pores.inputs["Vector"])
    bump = nodes.new("ShaderNodeBump")
    bump.location = (-120, -160)
    bump.inputs["Strength"].default_value = 0.22 if is_cut_face else 0.17
    bump.inputs["Distance"].default_value = 0.0013
    links.new(pores.outputs["Fac"], bump.inputs["Height"])
    links.new(bump.outputs["Normal"], shader.inputs["Normal"])

    color = palette.outputs["Color"]
    if is_cut_face:
        flatten = nodes.new("ShaderNodeVectorMath")
        flatten.operation = "MULTIPLY"
        flatten.inputs[1].default_value = (1, 1, 0)
        flatten.location = (-550, -420)
        links.new(coords.outputs["Object"], flatten.inputs[0])
        radius = nodes.new("ShaderNodeVectorMath")
        radius.operation = "LENGTH"
        radius.location = (-360, -420)
        links.new(flatten.outputs["Vector"], radius.inputs[0])
        edge = nodes.new("ShaderNodeMapRange")
        edge.label = "Soft highlight at existing inner edge"
        edge.interpolation_type = "SMOOTHSTEP"
        edge.location = (-155, -420)
        for label, value in (("From Min", 0.15557), ("From Max", 0.170),
                             ("To Min", 0.62), ("To Max", 0.0)):
            edge.inputs[label].default_value = value
        links.new(radius.outputs["Value"], edge.inputs["Value"])
        mix = nodes.new("ShaderNodeMixRGB")
        mix.location = (80, 250)
        mix.inputs[2].default_value = (0.105, 0.127, 0.145, 1)
        links.new(edge.outputs["Result"], mix.inputs[0])
        links.new(color, mix.inputs[1])
        color = mix.outputs["Color"]
    shader.location = (315, 160)
    next(node for node in nodes if node.type == "OUTPUT_MATERIAL").location = (620, 160)
    links.new(color, shader.inputs["Base Color"])
    return material


wall = scene.objects[wall_name]
before = shot_state(scene)
mesh_signature = geometry_signature(wall)
wall.data.materials[0] = wall_material(
    wall.data.materials[0], "S05 borehole wall | blue charcoal",
    (0.016, 0.023, 0.032), (0.038, 0.048, 0.060), False)
wall.data.materials[1] = wall_material(
    wall.data.materials[1], "S05 cement cut face | slate",
    (0.031, 0.038, 0.047), (0.057, 0.067, 0.079), True)
material_names = [material.name for material in wall.data.materials]

scene.frame_set(frames[0])
scene.render.filepath = "//../Cache/v024/S05_"
bpy.ops.wm.save_as_mainfile(filepath=str(output), relative_remap=False)
bpy.ops.wm.open_mainfile(filepath=str(output))
scene = bpy.context.scene
wall = scene.objects[wall_name]
assert geometry_signature(wall) == mesh_signature
assert [material.name for material in wall.data.materials] == material_names
assert shot_state(scene) == before
libraries = {lib.name: lib.filepath for lib in bpy.data.libraries}
assert len(libraries) == 4
for path in libraries.values():
    assert path.startswith("//") and Path(bpy.path.abspath(path)).is_file(), path

record = {
    "source": "S05_navy-room_v023.blend",
    "scene": output.name,
    "review_frames": frames,
    "cutaway_geometry_and_material_indices_sha256": mesh_signature,
    "cutaway_materials": material_names,
    "relative_libraries": libraries,
    "stills": [],
}
scene.render.image_settings.file_format = "PNG"
for frame in frames:
    scene.frame_set(frame)
    path = shot / "Previews" / f"S05_stylized-cutaway_v024_f{frame:04d}.png"
    scene.render.filepath = str(path)
    start = perf_counter()
    bpy.ops.render.render(write_still=True)
    record["stills"].append({"frame": frame, "seconds": perf_counter() - start})
    (shot / "Notes/v024-stylized-cutaway.json").write_text(
        json.dumps(record, indent=2) + "\n", encoding="utf-8")
