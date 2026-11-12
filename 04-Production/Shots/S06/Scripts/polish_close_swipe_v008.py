"""Lightly polish the original close S06 camera and retain its reveal timing."""

from hashlib import sha256
import json
from math import degrees, exp
from pathlib import Path

import bpy
from mathutils import Quaternion, Vector


shot = Path(__file__).resolve().parents[1]
source = shot / "Scenes/S06_shared-reconstruction_v005.blend"
output = shot / "Scenes/S06_close-swipe_v008.blend"
join = 125
assert Path(bpy.data.filepath).resolve() == source
assert not output.exists()


def ease(t):
    t = max(0.0, min(1.0, t))
    return t**3 * (10 + t * (-15 + 6 * t))


def camera_states(scene):
    camera = scene.camera
    poses = {}
    for frame in range(1, 289):
        scene.frame_set(frame)
        poses[frame] = camera.location.copy(), camera.rotation_quaternion.copy(), camera.data.lens
    return poses


def motion(poses, start, end):
    positions = [poses[frame][0] for frame in range(start, end + 1)]
    rotations = [poses[frame][1] for frame in range(start, end + 1)]
    deltas = [b - a for a, b in zip(positions, positions[1:])]
    return {
        "max_travel_m": max(delta.length for delta in deltas),
        "max_change_of_travel_m": max((b - a).length for a, b in zip(deltas, deltas[1:])),
        "max_turn_deg": max(degrees(a.rotation_difference(b).angle)
                            for a, b in zip(rotations, rotations[1:])),
    }


scene = bpy.context.scene
camera = scene.camera
assert camera.parent is None and not camera.constraints
original = camera_states(scene)
kernel = [(step, exp(-0.5 * (step / 6)**2)) for step in range(-15, 16)]
weight_sum = sum(weight for _, weight in kernel)
edits = {}
for frame in range(1, join):
    loc, rotation, _ = original[frame]
    weight = ease((frame - 51) / 24) * (1 - ease((frame - 114) / (join - 114)))
    if weight:
        nearby = [(original[frame + step], factor / weight_sum) for step, factor in kernel]
        smooth_loc = sum((pose[0] * factor for pose, factor in nearby), Vector((0, 0, 0)))
        smooth_q = Quaternion(tuple(sum(pose[1][i] * factor * (1 if rotation.dot(pose[1]) >= 0 else -1)
                                        for pose, factor in nearby) for i in range(4))).normalized()
        loc, rotation = loc.lerp(smooth_loc, weight), rotation.slerp(smooth_q, weight)
    remaining = max(0.0, 1 - (frame - 1) / 76)
    offset = Vector((-0.025, 0.012, -0.13)) * remaining**2
    if offset.length_squared:
        forward = rotation @ Vector((0, 0, -1))
        gaze = loc + 2.2 * forward + 0.58 * offset
        loc = loc + offset
        rotation = forward.rotation_difference((gaze - loc).normalized()) @ rotation
    edits[frame] = loc, rotation

action = camera.animation_data
curves = action.action.layers[0].strips[0].channelbag(action.action_slot).fcurves
for curve in curves:
    if curve.data_path not in ("location", "rotation_quaternion"):
        continue
    part = 0 if curve.data_path == "location" else 1
    count = 0
    for point in curve.keyframe_points:
        frame = round(point.co.x)
        if frame in edits:
            point.co.y = edits[frame][part][curve.array_index]
            count += 1
    assert count == join - 1
    curve.update()
scene.frame_set(1)
scene.render.filepath = "//../Cache/v008/preview/S06_"
bpy.ops.wm.save_as_mainfile(filepath=str(output), relative_remap=False)
bpy.ops.wm.open_mainfile(filepath=str(output), load_ui=False)
scene = bpy.context.scene
revised = camera_states(scene)
assert all(revised[frame] == original[frame] for frame in range(join, 289))
assert all(revised[frame][2] == original[frame][2] for frame in range(1, 289))
assert len(bpy.data.libraries) == 6 and all(
    lib.filepath.startswith("//") and Path(bpy.path.abspath(lib.filepath)).is_file()
    for lib in bpy.data.libraries)
assert (scene.frame_start, scene.frame_end, scene.render.fps) == (1, 288, 24)
before = motion(original, 72, 126)
after = motion(revised, 72, 126)
assert after["max_change_of_travel_m"] < before["max_change_of_travel_m"]
assert after["max_turn_deg"] < before["max_turn_deg"]
(shot / "Notes/v008-camera.json").write_text(json.dumps({
    "source": source.name,
    "scene": output.name,
    "native_sha256": sha256(output.read_bytes()).hexdigest(),
    "edited_camera_frames": [1, join - 1],
    "exact_camera_match": [join, 288],
    "original_handoff_motion": before,
    "revised_handoff_motion": after,
    "frame_1_offset_m": (revised[1][0] - original[1][0]).length,
}, indent=2) + "\n", encoding="utf-8")
