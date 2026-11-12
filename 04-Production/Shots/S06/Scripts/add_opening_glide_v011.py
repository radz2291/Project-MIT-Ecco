"""Add the short product glide before the established S06 camera sweep."""

from hashlib import sha256
import json
from math import degrees, floor, radians
from pathlib import Path

import bpy
from mathutils import Quaternion, Vector


shot = Path(__file__).resolve().parents[1]
source = shot / "Scenes/S06_direct-sweep_v010.blend"
output = shot / "Scenes/S06_opening-glide_v011.blend"
assert Path(bpy.data.filepath).resolve() == source and not output.exists()
glide_end = 15
sweep_end = 145
start_rate = 1.10


def states(scene):
    result = {}
    camera = scene.camera
    gate = bpy.data.materials["A guide color"].node_tree.nodes["SHOT_VISIBILITY"].inputs[0]
    for frame in range(1, 289):
        scene.frame_set(frame)
        result[frame] = (camera.location.copy(), camera.rotation_quaternion.copy(),
                         camera.data.lens, camera.data.shift_x, camera.data.shift_y,
                         gate.default_value)
    return result


def cubic(a, b, c, d, t):
    r = 1 - t
    return a * r**3 + b * (3 * r**2 * t) + c * (3 * r * t**2) + d * t**3


def spherical_curve(a, b, c, d, t):
    ab, bc, cd = a.slerp(b, t), b.slerp(c, t), c.slerp(d, t)
    return ab.slerp(bc, t).slerp(bc.slerp(cd, t), t)


def sweep_time(frame):
    length = sweep_end - glide_end
    t = (frame - glide_end) / length
    return (1 + (sweep_end - 1) * (3 * t**2 - 2 * t**3)
            + length * start_rate * (t**3 - 2 * t**2 + t)
            + length * (t**3 - t**2))


scene = bpy.context.scene
camera = scene.camera
old = states(scene)
anchor, anchor_rotation = old[1][:2]
next_position, next_rotation = old[2][:2]
start = anchor + Vector((0.03, 0.08, 0.68))
span = glide_end - 1
first_control = start.lerp(anchor, 0.42)
last_control = anchor - (next_position - anchor) * (span * start_rate / 3)
start_rotation = Quaternion((0, 0, 1), radians(2.5)) @ anchor_rotation
first_turn = start_rotation.slerp(anchor_rotation, 0.4)
turn_delta = anchor_rotation.rotation_difference(next_rotation)
if turn_delta.w < 0:
    turn_delta.negate()
axis, angle = turn_delta.to_axis_angle()
last_turn = anchor_rotation @ Quaternion(axis, -angle * span * start_rate / 3)

edits = {}
for frame in range(1, glide_end):
    t = (frame - 1) / span
    edits[frame] = (
        cubic(start, first_control, last_control, anchor, t),
        spherical_curve(start_rotation, first_turn, last_turn, anchor_rotation, t),
    )
edits[glide_end] = anchor, anchor_rotation
for frame in range(glide_end + 1, sweep_end):
    time = sweep_time(frame)
    before = floor(time)
    weight = time - before
    a, b = old[before], old[before + 1]
    edits[frame] = a[0].lerp(b[0], weight), a[1].slerp(b[1], weight)

animation = camera.animation_data
curves = animation.action.layers[0].strips[0].channelbag(animation.action_slot).fcurves
for curve in curves:
    if curve.data_path not in ("location", "rotation_quaternion"):
        continue
    part = 0 if curve.data_path == "location" else 1
    changed = 0
    for point in curve.keyframe_points:
        frame = round(point.co.x)
        if frame in edits:
            point.co.y = edits[frame][part][curve.array_index]
            changed += 1
    assert changed == len(edits)
    curve.update()

scene.frame_set(1)
scene.render.filepath = "//../Cache/v011/preview/S06_"
bpy.ops.wm.save_as_mainfile(filepath=str(output), relative_remap=False)
bpy.ops.wm.open_mainfile(filepath=str(output), load_ui=False)
scene = bpy.context.scene
new = states(scene)
assert new[glide_end][:2] == old[1][:2]
assert all(new[f] == old[f] for f in range(sweep_end, 289))
assert all(new[f][2:] == old[f][2:] for f in range(1, 289))
assert (scene.frame_start, scene.frame_end, scene.render.fps) == (1, 288, 24)
assert len(bpy.data.libraries) == 6 and all(
    lib.filepath.startswith("//") and Path(bpy.path.abspath(lib.filepath)).is_file()
    for lib in bpy.data.libraries)
approach = [new[f + 1][0] - new[f][0] for f in range(1, glide_end)]
into_sweep = new[glide_end + 1][0] - new[glide_end][0]
assert all(step.length > 0.01 for step in approach)
assert approach[-1].normalized().dot(into_sweep.normalized()) > 0.75
turns = [degrees(new[f][1].rotation_difference(new[f + 1][1]).angle)
         for f in range(glide_end - 3, glide_end + 3)]
(shot / "Notes/v011-opening-glide.json").write_text(json.dumps({
    "source": source.name,
    "scene": output.name,
    "native_sha256": sha256(output.read_bytes()).hexdigest(),
    "product_glide_frames": [1, glide_end],
    "product_glide_seconds": span / 24,
    "travel_m": sum(step.length for step in approach),
    "glide_end_position_and_aim_match_v010_frame_1": True,
    "glide_join_steps_m": [step.length for step in approach[-3:]] + [into_sweep.length],
    "glide_join_turn_degrees": turns,
    "later_camera_match": [sweep_end, 288],
    "grid_visibility_matched": True,
}, indent=2) + "\n", encoding="utf-8")
