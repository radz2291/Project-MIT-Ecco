"""Add the Section 3 room treatment to S05 and render the three requested looks."""

import json
import math
from pathlib import Path
from time import perf_counter

import bpy


shot = Path(__file__).resolve().parents[1]
output = shot / "Scenes/S05_navy-room_v023.blend"
frames = (50, 205, 432)
scene = bpy.context.scene
room_name = "S05 Navy room"
assert Path(bpy.data.filepath).name == "S05_shared-bha_v022.blend"
assert not output.exists()


def subject_state(scene):
    fixed = scene.objects["S05_FixedHalfBorehole"]
    hydraulics = scene.collection.children["S05_v018_ContinuousHydraulics"]
    hardware = [scene.objects[name] for name in ("S05 Shared BHA v008", "S05 Shared uphole joint")]
    subjects = [fixed, *hardware, *sorted(hydraulics.all_objects, key=lambda obj: obj.name)]
    states = []
    for frame in frames:
        scene.frame_set(frame)
        camera = scene.camera
        states.append((
            tuple(tuple(row) for row in camera.matrix_world),
            camera.data.lens, camera.data.dof.focus_distance, camera.data.shift_x, camera.data.shift_y,
            [(obj.name, tuple(tuple(row) for row in obj.matrix_world), obj.hide_render,
              tuple(slot.material.name for slot in obj.material_slots if slot.material))
             for obj in subjects],
        ))
    return states


def emission(name, rgb):
    material = bpy.data.materials.new(name)
    material.diffuse_color = (*rgb, 1)
    material.use_nodes = True
    tree = material.node_tree
    tree.nodes.clear()
    shader = tree.nodes.new("ShaderNodeEmission")
    shader.inputs["Color"].default_value = (*rgb, 1)
    output_node = tree.nodes.new("ShaderNodeOutputMaterial")
    tree.links.new(shader.outputs[0], output_node.inputs["Surface"])
    return material


def panel(name, corners):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(corners, [], [(0, 1, 2, 3)])
    mesh.materials.append(navy)
    room.objects.link(bpy.data.objects.new(name, mesh))


def grid(name, segments, material):
    curve = bpy.data.curves.new(name, "CURVE")
    curve.dimensions = "3D"
    curve.bevel_depth = 0.0028
    curve.bevel_resolution = 0
    curve.materials.append(material)
    for start, end in segments:
        stroke = curve.splines.new("POLY")
        stroke.points.add(1)
        stroke.points[0].co = (*start, 1)
        stroke.points[1].co = (*end, 1)
    room.objects.link(bpy.data.objects.new(name, curve))


before = subject_state(scene)
room = bpy.data.collections.new(room_name)
scene.collection.children.link(room)
# Reproduce S03's panel and grid palette in S05's existing AgX view.
navy_rgb = (0.007, 0.016, 0.031)
navy = emission("S05 room | navy", navy_rgb)
floor_blue = emission("S05 room | floor grid", (0.010, 0.031, 0.055))
wall_blue = emission("S05 room | wall grid", (0.009, 0.027, 0.048))

back, front = -3.2, 3.6
left, right = -2.0, 2.0
bottom, top = -2.24, 4.56
pitch = 0.4
offset = 0.001
panel("Navy floor", [(back, left, bottom), (front, left, bottom),
                    (front, right, bottom), (back, right, bottom)])
panel("Navy back wall", [(back, left, bottom), (back, right, bottom),
                        (back, right, top), (back, left, top)])
for side, label in ((left, "left"), (right, "right")):
    panel(f"Navy {label} wall", [(back, side, bottom), (front, side, bottom),
                                (front, side, top), (back, side, top)])

def divisions(low, high):
    return [low + i * pitch for i in range(1, round((high - low) / pitch))]


floor_lines, wall_lines = [], []
for y in divisions(left, right):
    meeting = (back + offset, y, bottom + offset)
    floor_lines.append((meeting, (front, y, bottom + offset)))
    wall_lines.append((meeting, (back + offset, y, top)))
for x in divisions(back, front):
    a = (x, left + offset, bottom + offset)
    b = (x, right - offset, bottom + offset)
    floor_lines.append((a, b))
    wall_lines.extend(((a, (x, left + offset, top)), (b, (x, right - offset, top))))
for z in divisions(bottom, top):
    a = (back + offset, left + offset, z)
    b = (back + offset, right - offset, z)
    wall_lines.extend(((a, b), (a, (front, left + offset, z)), (b, (front, right - offset, z))))
grid("S05 aligned floor grid", floor_lines, floor_blue)
grid("S05 aligned wall grid", wall_lines, wall_blue)

min_clearance = math.inf
for frame in range(scene.frame_start, scene.frame_end + 1):
    scene.frame_set(frame)
    x, y, z = scene.camera.matrix_world.translation
    min_clearance = min(min_clearance, x - back, front - x, y - left, right - y, z - bottom, top - z)
assert min_clearance > 0.2, min_clearance

scene.frame_set(frames[0])
scene.render.filepath = "//../Cache/v023/S05_"
bpy.ops.wm.save_as_mainfile(filepath=str(output), relative_remap=False)
bpy.ops.wm.open_mainfile(filepath=str(output))
scene = bpy.context.scene
assert subject_state(scene) == before
assert len(scene.collection.children[room_name].objects) == 6
libraries = {lib.name: lib.filepath for lib in bpy.data.libraries}
assert len(libraries) == 4
for path in libraries.values():
    assert path.startswith("//") and Path(bpy.path.abspath(path)).is_file(), path

record = {
    "source": "S05_shared-bha_v022.blend",
    "look_reference": "S03_restored-interior-labels_v040",
    "scene": output.name,
    "review_frames": frames,
    "minimum_camera_to_room_plane_m": min_clearance,
    "grid_pitch_m": pitch,
    "relative_libraries": libraries,
    "preserved": "Matched camera optics and transforms, BHA, custom cutaway, and section hydraulics at all three frames.",
    "stills": [],
}
scene.render.image_settings.file_format = "PNG"
for frame in frames:
    scene.frame_set(frame)
    path = shot / "Previews" / f"S05_navy-room_v023_f{frame:04d}.png"
    scene.render.filepath = str(path)
    started = perf_counter()
    bpy.ops.render.render(write_still=True)
    record["stills"].append({"frame": frame, "seconds": perf_counter() - started})
    (shot / "Notes/v023-navy-room.json").write_text(
        json.dumps(record, indent=2) + "\n", encoding="utf-8")
