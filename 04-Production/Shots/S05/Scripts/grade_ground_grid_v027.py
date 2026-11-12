"""Grow the grid cells outward from the existing S05 borehole edge."""

from hashlib import sha256
import json
import math
from pathlib import Path
from time import perf_counter

import bpy


shot = Path(__file__).resolve().parents[1]
output = shot / "Scenes/S05_graded-ground-grid_v027.blend"
ground_name = "S05 Continuous borehole and ground"
frames = (50, 205, 432)
scene = bpy.context.scene
assert Path(bpy.data.filepath).name == "S05_continuous-ground_v026.blend"
assert not output.exists()

growth = 1.43
offset = 0.087
depth_pitch = 0.1035


def connect(tree, value, socket):
    if isinstance(value, bpy.types.NodeSocket):
        tree.links.new(value, socket)
    else:
        socket.default_value = value


def operation(tree, label, operator, a, b=0.0):
    node = tree.nodes.new("ShaderNodeMath")
    node.label = label
    node.operation = operator
    connect(tree, a, node.inputs[0])
    connect(tree, b, node.inputs[1])
    return node.outputs[0]


def ramp(tree, label, value, start, end, low, high):
    node = tree.nodes.new("ShaderNodeMapRange")
    node.label = label
    node.interpolation_type = "SMOOTHSTEP"
    for name, setting in (("Value", value), ("From Min", start), ("From Max", end),
                          ("To Min", low), ("To Max", high)):
        connect(tree, setting, node.inputs[name])
    return node.outputs["Result"]


def tint(tree, label, factor, base, accent):
    node = tree.nodes.new("ShaderNodeMixRGB")
    node.label = label
    for index, setting in enumerate((factor, base, accent)):
        connect(tree, setting, node.inputs[index])
    return node.outputs["Color"]


def mesh_hash(obj):
    mesh = obj.data
    return sha256(repr((
        [tuple(v.co) for v in mesh.vertices],
        [(tuple(p.vertices), p.material_index) for p in mesh.polygons],
        [tuple(p.uv) for p in mesh.uv_layers.active.data],
    )).encode("utf-8")).hexdigest()


def scene_sample(s):
    items = [s.objects[name] for name in ("S05 Shared BHA v008", "S05 Shared uphole joint")]
    items.extend(sorted(s.collection.children["S05_v018_ContinuousHydraulics"].all_objects,
                        key=lambda obj: obj.name))
    result = []
    for frame in frames:
        s.frame_set(frame)
        camera = s.camera
        result.append((
            tuple(tuple(row) for row in camera.matrix_world), camera.data.lens,
            camera.data.dof.focus_distance, camera.data.shift_x, camera.data.shift_y,
            [(obj.name, tuple(tuple(row) for row in obj.matrix_world), obj.hide_render,
              tuple(slot.material.name for slot in obj.material_slots if slot.material))
             for obj in items],
        ))
    return result


def layout(tree, output_node):
    levels = {}

    def visit(node, level):
        if levels.get(node, -1) >= level:
            return
        levels[node] = level
        for socket in node.inputs:
            for link in socket.links:
                visit(link.from_node, level + 1)

    visit(output_node, 0)
    rows = {}
    for node, level in levels.items():
        row = rows.get(level, 0)
        node.location = (-205 * level, -270 * row)
        rows[level] = row + 1


ground = scene.objects[ground_name]
geometry = mesh_hash(ground)
before = scene_sample(scene)
uv_data = ground.data.uv_layers.active.data
arc_length = max(uv_data[index].uv.x for face in ground.data.polygons
                 if face.material_index == 0 for index in face.loop_indices)

wall = ground.data.materials[0].copy()
wall.name = "S05 bore wall | fine grid"
ring = next(node for node in wall.node_tree.nodes if node.type == "MATH"
            and node.operation == "PINGPONG" and abs(node.inputs[1].default_value - 0.1035) < 1e-5)
ring.inputs[1].default_value = depth_pitch / 2
ground.data.materials[0] = wall

surface_material = ground.data.materials[1].copy()
surface_material.name = "S05 ground | graded blue grid"
tree = surface_material.node_tree
tree.nodes.clear()
coords = tree.nodes.new("ShaderNodeTexCoord")
separate = tree.nodes.new("ShaderNodeSeparateXYZ")
tree.links.new(coords.outputs["UV"], separate.inputs[0])
u, axial = separate.outputs["X"], separate.outputs["Y"]

left = operation(tree, "Distance on left", "MULTIPLY", u, -1.0)
right = operation(tree, "Distance on right", "SUBTRACT", u, arc_length)
distance = operation(tree, "Distance from bore lip", "MAXIMUM", left, right)
scaled = operation(tree, "Offset in grid units", "MULTIPLY_ADD", distance, 1 / offset)
scaled.node.inputs[2].default_value = 1.0
band = operation(tree, "Grid spacing grows outward", "LOGARITHM", scaled, growth)

# Approximate distance to the nearest lengthwise line in metres.
rail_phase = operation(tree, "Nearest lengthwise line", "PINGPONG", band, 0.5)
rail_scale = operation(tree, "Local spacing in metres", "MULTIPLY", scaled, offset * math.log(growth))
rail_distance = operation(tree, "Distance to lengthwise line", "MULTIPLY", rail_phase, rail_scale)
rails = ramp(tree, "Soft lengthwise lines", rail_distance, 0.0007, 0.0019, 1.0, 0.0)

# At every second lengthwise line, let half the cross-lines end.
pair = operation(tree, "Pairs of lengthwise lines", "MULTIPLY", band, 0.5)
level = operation(tree, "Cross-line spacing level", "FLOOR", pair)
multiplier = operation(tree, "Half as many lines per level", "POWER", 2.0, level)
half_pitch = operation(tree, "Distance between cross-lines", "MULTIPLY", multiplier, depth_pitch / 2)
cross_distance = operation(tree, "Distance to cross-line", "PINGPONG", axial, half_pitch)
crosses = ramp(tree, "Soft cross-lines", cross_distance, 0.0008, 0.0021, 1.0, 0.0)
pattern = operation(tree, "Graded grid", "MAXIMUM", rails, crosses)
lip = ramp(tree, "Bore lip", distance, 0.0008, 0.0032, 1.0, 0.0)
strength = ramp(tree, "Soften lines away from the bore", distance, 0.0, 1.5, 0.92, 0.46)
soft_pattern = operation(tree, "Subtle blue lines", "MULTIPLY", pattern, strength)
color = tint(tree, "Blue grid on navy ground", soft_pattern,
             (0.010, 0.022, 0.037, 1), (0.022, 0.090, 0.140, 1))
color = tint(tree, "Bore edge accent", lip, color, (0.025, 0.108, 0.162, 1))
emission = tree.nodes.new("ShaderNodeEmission")
tree.links.new(color, emission.inputs["Color"])
surface = tree.nodes.new("ShaderNodeOutputMaterial")
tree.links.new(emission.outputs[0], surface.inputs["Surface"])
layout(tree, surface)
ground.data.materials[1] = surface_material

scene.frame_set(frames[0])
scene.render.filepath = "//../Cache/v027/S05_"
bpy.ops.wm.save_as_mainfile(filepath=str(output), relative_remap=False)
bpy.ops.wm.open_mainfile(filepath=str(output))
scene = bpy.context.scene
assert mesh_hash(scene.objects[ground_name]) == geometry
assert scene_sample(scene) == before
assert len(bpy.data.libraries) == 4
assert all(lib.filepath.startswith("//") and Path(bpy.path.abspath(lib.filepath)).is_file()
           for lib in bpy.data.libraries)

record = {
    "source": "S05_continuous-ground_v026.blend",
    "scene": output.name,
    "frames": frames,
    "geometry_and_uv_sha256": geometry,
    "outward_cell_widths_m": [offset * (growth - 1) * growth**i for i in range(8)],
    "axial_cell_pitch_m": [depth_pitch * 2**i for i in range(4)],
    "stills": [],
}
scene.render.image_settings.file_format = "PNG"
for frame in frames:
    scene.frame_set(frame)
    path = shot / "Previews" / f"S05_graded-ground-grid_v027_f{frame:04d}.png"
    scene.render.filepath = str(path)
    start = perf_counter()
    bpy.ops.render.render(write_still=True)
    record["stills"].append({"frame": frame, "seconds": perf_counter() - start})
    (shot / "Notes/v027-graded-ground-grid.json").write_text(
        json.dumps(record, indent=2) + "\n", encoding="utf-8")
