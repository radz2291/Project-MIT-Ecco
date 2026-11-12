"""Blend the along-tool move directly into the existing S06 camera curve."""

from hashlib import sha256
import json
from math import degrees
from pathlib import Path

import bpy


shot = Path(__file__).resolve().parents[1]
base = shot / "Scenes/S06_direct-sweep_v010.blend"
previous = shot / "Scenes/S06_opening-glide_v011.blend"
output = shot / "Scenes/S06_continuous-glide_v012.blend"
assert Path(bpy.data.filepath).resolve() == previous and not output.exists()
join = 31


def positions(scene):
    data = {}
    for frame in range(1, join + 2):
        scene.frame_set(frame)
        data[frame] = scene.camera.location.copy()
    return data


def key_values(camera):
    data = camera.animation_data
    bag = data.action.layers[0].strips[0].channelbag(data.action_slot)
    return {(curve.data_path, curve.array_index): curve for curve in bag.fcurves}


def snapshot(camera):
    return {key: [(p.co.x, p.co.y, p.interpolation) for p in fc.keyframe_points]
            for key, fc in key_values(camera).items()}


def motion(positions):
    vectors = [positions[f + 1] - positions[f] for f in range(1, join)]
    return {
        "max_direction_step_deg": max(degrees(a.angle(b)) for a, b in zip(vectors, vectors[1:])),
        "max_velocity_step_m": max((b - a).length for a, b in zip(vectors, vectors[1:])),
        "minimum_travel_m_per_frame": min(v.length for v in vectors),
        "travel_frames_14_to_16_m": [v.length for v in vectors[12:15]],
    }


old = positions(bpy.context.scene)
bpy.ops.wm.open_mainfile(filepath=str(base), load_ui=False)
scene = bpy.context.scene
camera = scene.camera
base_positions = positions(scene)
before = snapshot(camera)
offset = old[1] - base_positions[1]
curves = key_values(camera)
for axis in range(3):
    curve = curves["location", axis]
    for point in curve.keyframe_points:
        frame = round(point.co.x)
        if 1 <= frame < join:
            # The glide has zero velocity and acceleration relative to the sweep at frame 31.
            remaining = 1 - (frame - 1) / (join - 1)
            point.co.y = base_positions[frame][axis] + offset[axis] * remaining**3
    curve.update()

scene.frame_set(1)
scene.render.filepath = "//../Cache/v012/preview/S06_"
bpy.ops.wm.save_as_mainfile(filepath=str(output), relative_remap=False)
bpy.ops.wm.open_mainfile(filepath=str(output), load_ui=False)
scene = bpy.context.scene
new = positions(scene)
after = snapshot(scene.camera)
for key, points in before.items():
    assert after[key] == points if key[0] != "location" else (
        [p for p in after[key] if p[0] >= join] == [p for p in points if p[0] >= join])
assert (new[1] - old[1]).length < 1e-6
assert all(new[f + 1].y < new[f].y and new[f + 1].z < new[f].z for f in range(1, join))
assert (scene.frame_start, scene.frame_end, scene.render.fps) == (1, 288, 24)
assert len(bpy.data.libraries) == 6 and all(
    lib.filepath.startswith("//") and Path(bpy.path.abspath(lib.filepath)).is_file()
    for lib in bpy.data.libraries)
old_motion, new_motion = motion(old), motion(new)
assert new_motion["max_direction_step_deg"] < old_motion["max_direction_step_deg"]
assert new_motion["max_velocity_step_m"] < old_motion["max_velocity_step_m"]
(shot / "Notes/v012-continuous-glide.json").write_text(json.dumps({
    "source": base.name,
    "previous_glide_reference": previous.name,
    "scene": output.name,
    "native_sha256": sha256(output.read_bytes()).hexdigest(),
    "changed_camera_positions": [1, join - 1],
    "matching_camera_frames": [join, 288],
    "rotation_keys_match_v010": True,
    "old_first_30_frames": old_motion,
    "new_first_30_frames": new_motion,
}, indent=2) + "\n", encoding="utf-8")
