"""Stretch the continuous S05 ground grid without ending cross-lines at band boundaries."""

from hashlib import sha256
import json
from math import log
from pathlib import Path
from time import perf_counter

import bpy


shot = Path(__file__).resolve().parents[1]
output = shot / "Scenes/S05_stretched-grid_v028.blend"
ground_name = "S05 Continuous borehole and ground"
frames = (50, 205, 432)
scene = bpy.context.scene
assert Path(bpy.data.filepath).name == "S05_graded-ground-grid_v027.blend"
assert not output.exists()

axial_pitch = 0.1035
anchor_z = 0.207
maximum_stretch = 3.1
stretch_radius = 0.36
wall_divisions = 12


def geometry_hash(obj):
    mesh = obj.data
    return sha256(repr((
        [tuple(v.co) for v in mesh.vertices],
        [(tuple(p.vertices), p.material_index) for p in mesh.polygons],
        [tuple(uv.uv) for uv in mesh.uv_layers.active.data],
    )).encode("utf-8")).hexdigest()


def foreground(scene):
    objects = [scene.objects[name] for name in ("S05 Shared BHA v008", "S05 Shared uphole joint")]
    objects.extend(sorted(scene.collection.children["S05_v018_ContinuousHydraulics"].all_objects,
                          key=lambda obj: obj.name))
    result = []
    for frame in frames:
        scene.frame_set(frame)
        camera = scene.camera
        result.append((tuple(tuple(row) for row in camera.matrix_world),
                       camera.data.lens, camera.data.dof.focus_distance,
                       camera.data.shift_x, camera.data.shift_y,
                       [(obj.name, tuple(tuple(row) for row in obj.matrix_world), obj.hide_render,
                         tuple(slot.material.name for slot in obj.material_slots if slot.material))
                        for obj in objects]))
    return result


def layout(tree):
    depths = {}

    def visit(node, depth):
        if depths.get(node, -1) >= depth:
            return
        depths[node] = depth
        for socket in node.inputs:
            for link in socket.links:
                visit(link.from_node, depth + 1)

    visit(next(node for node in tree.nodes if node.type == "OUTPUT_MATERIAL"), 0)
    rows = {}
    for node, depth in depths.items():
        row = rows.get(depth, 0)
        node.location = (-205 * depth, -270 * row)
        rows[depth] = row + 1


def math_value(tree, label, operation, a, b):
    node = tree.nodes.new("ShaderNodeMath")
    node.label = label
    node.operation = operation
    for i, value in enumerate((a, b)):
        if isinstance(value, bpy.types.NodeSocket):
            tree.links.new(value, node.inputs[i])
        else:
            node.inputs[i].default_value = value
    return node.outputs[0]


ground = scene.objects[ground_name]
before = foreground(scene)
geometry = geometry_hash(ground)
arc_length = max(ground.data.uv_layers.active.data[index].uv.x
                 for face in ground.data.polygons if face.material_index == 0
                 for index in face.loop_indices)
seam_width = arc_length / wall_divisions
wall = ground.data.materials[0].copy()
wall.name = "S05 bore wall | aligned grid"
patterns = [n for n in wall.node_tree.nodes if n.type == "MATH" and n.operation == "PINGPONG"]
assert len(patterns) == 2
rails = next(node for node in patterns if node.inputs[0].links[0].from_socket.name == "X")
rails.inputs[1].default_value = seam_width / 2
layout(wall.node_tree)
ground.data.materials[0] = wall

material = ground.data.materials[1].copy()
material.name = "S05 ground | continuous stretched grid"
tree = material.node_tree
labeled = {node.label: node for node in tree.nodes if node.label}
distance = labeled["Distance from bore lip"].outputs[0]
growth = labeled["Grid spacing grows outward"].inputs[1].default_value
offset = seam_width / (growth - 1)
labeled["Offset in grid units"].inputs[1].default_value = 1 / offset
labeled["Local spacing in metres"].inputs[1].default_value = offset * log(growth)
cross = labeled["Distance to cross-line"]
axial = cross.inputs[0].links[0].from_socket
for name in ("Pairs of lengthwise lines", "Cross-line spacing level",
             "Half as many lines per level", "Distance between cross-lines"):
    tree.nodes.remove(labeled[name])

# The stretch starts with zero slope at the bore lip so every cross-line
# continues through the wall-to-ground seam at its original angle.
distance_squared = math_value(tree, "Distance squared", "MULTIPLY", distance, distance)
denominator = math_value(tree, "Soft stretch radius", "ADD", distance_squared, stretch_radius**2)
falloff = math_value(tree, "Gradual stretch", "DIVIDE", distance_squared, denominator)
increase = math_value(tree, "Added stretch", "MULTIPLY", falloff, maximum_stretch - 1)
stretch = math_value(tree, "Axial spacing factor", "ADD", 1, increase)
centered = math_value(tree, "Relative to bore midpoint", "SUBTRACT", axial, anchor_z)
warped = math_value(tree, "Continuous stretched coordinate", "DIVIDE", centered, stretch)
warped_axial = math_value(tree, "Restore bore midpoint", "ADD", warped, anchor_z)
tree.links.new(warped_axial, cross.inputs[0])
cross.inputs[1].default_value = axial_pitch / 2
width = math_value(tree, "Cross-line distance in metres", "MULTIPLY", cross.outputs[0], stretch)
tree.links.new(width, labeled["Soft cross-lines"].inputs["Value"])
layout(tree)
ground.data.materials[1] = material

scene.frame_set(frames[0])
scene.render.filepath = "//../Cache/v028/S05_"
bpy.ops.wm.save_as_mainfile(filepath=str(output), relative_remap=False)
bpy.ops.wm.open_mainfile(filepath=str(output))
scene = bpy.context.scene
assert geometry_hash(scene.objects[ground_name]) == geometry
assert foreground(scene) == before
assert len(bpy.data.libraries) == 4
assert all(lib.filepath.startswith("//") and Path(bpy.path.abspath(lib.filepath)).is_file()
           for lib in bpy.data.libraries)

record = {
    "source": "S05_graded-ground-grid_v027.blend",
    "scene": output.name,
    "frames": frames,
    "geometry_and_uv_sha256": geometry,
    "seam_cell_width_m": seam_width,
    "seam_axial_pitch_m": axial_pitch,
    "axial_anchor_m": anchor_z,
    "axial_stretch_samples": {
        str(d): 1 + (maximum_stretch - 1) * d**2 / (d**2 + stretch_radius**2)
        for d in (0.0, 0.18, 0.36, 0.72, 1.44)
    },
    "stills": [],
}
scene.render.image_settings.file_format = "PNG"
for frame in frames:
    scene.frame_set(frame)
    path = shot / "Previews" / f"S05_stretched-grid_v028_f{frame:04d}.png"
    scene.render.filepath = str(path)
    start = perf_counter()
    bpy.ops.render.render(write_still=True)
    record["stills"].append({"frame": frame, "seconds": perf_counter() - start})
    (shot / "Notes/v028-stretched-grid.json").write_text(
        json.dumps(record, indent=2) + "\n", encoding="utf-8")
