"""Start the S06 pullback sooner and build the grid during the move."""

from bisect import bisect_right
from hashlib import sha256
import json
from math import degrees, floor
from pathlib import Path

import bpy


shot = Path(__file__).resolve().parents[1]
source = shot / "Scenes/S06_close-swipe_v008.blend"
output = shot / "Scenes/S06_overlapped-reveal_v009.blend"
assert Path(bpy.data.filepath).resolve() == source and not output.exists()
join = 125
camera_times = (
    (1, 1), (9, 16), (21, 57), (32, 79), (52, 97),
    (72, 108), (96, 114), (110, 118), (join, join),
)
guide_start, guide_end = 10, 70
guide_names = ("A guide color", "A seam")


def curves(owner):
    animation = owner.animation_data
    return animation.action.layers[0].strips[0].channelbag(animation.action_slot).fcurves


def gate(material):
    return material.node_tree.nodes["SHOT_VISIBILITY"].inputs[0]


def sample(scene):
    camera = scene.camera
    data = {}
    for frame in range(1, 289):
        scene.frame_set(frame)
        data[frame] = (camera.location.copy(), camera.rotation_quaternion.copy(),
                       camera.data.lens, camera.data.shift_x, camera.data.shift_y,
                       tuple(gate(bpy.data.materials[name]).default_value for name in guide_names))
    return data


def time_remap():
    xs, ys = zip(*camera_times)
    rates = [(b - a) / (xb - xa) for a, b, xa, xb in zip(ys, ys[1:], xs, xs[1:])]
    # Harmonic mean slopes keep the time mapping increasing without overshoot.
    slopes = [rates[0], *(2 * a * b / (a + b) for a, b in zip(rates, rates[1:])), 1.0]
    mapping = {}
    for frame in range(1, join):
        i = bisect_right(xs, frame) - 1
        length = xs[i + 1] - xs[i]
        t = (frame - xs[i]) / length
        mapping[frame] = ((2*t**3 - 3*t**2 + 1) * ys[i] + (t**3 - 2*t**2 + t) * length * slopes[i]
                          + (-2*t**3 + 3*t**2) * ys[i + 1] + (t**3 - t**2) * length * slopes[i + 1])
    mapping[join] = float(join)
    assert all(a < b for a, b in zip(mapping.values(), list(mapping.values())[1:]))
    return mapping


scene = bpy.context.scene
camera = scene.camera
old = sample(scene)
mapping = time_remap()
camera_values = {}
for frame in range(1, join):
    time = mapping[frame]
    before = floor(time)
    t = time - before
    a, b = old[before], old[before + 1]
    camera_values[frame] = (a[0].lerp(b[0], t), a[1].slerp(b[1], t)) if t else a[:2]
assert len(camera_values) == join - 1
for curve in curves(camera):
    if curve.data_path not in ("location", "rotation_quaternion"):
        continue
    part = 0 if curve.data_path == "location" else 1
    changed = 0
    for point in curve.keyframe_points:
        frame = round(point.co.x)
        if frame in camera_values:
            point.co.y = camera_values[frame][part][curve.array_index]
            changed += 1
    assert changed == join - 1
    curve.update()

for name in guide_names:
    tree = bpy.data.materials[name].node_tree
    socket = gate(bpy.data.materials[name])
    curve = next(fc for fc in curves(tree) if fc.data_path == socket.path_from_id("default_value"))
    remapped = {}
    for frame in range(1, 81):
        t = max(0.0, min(1.0, (frame - guide_start) / (guide_end - guide_start)))
        remapped[frame] = curve.evaluate(30 + 50 * t)
    changed = 0
    for point in curve.keyframe_points:
        frame = round(point.co.x)
        if frame in remapped:
            point.co.y = remapped[frame]
            changed += 1
    assert changed == len(remapped)
    curve.update()

scene.frame_set(1)
scene.render.filepath = "//../Cache/v009/preview/S06_"
bpy.ops.wm.save_as_mainfile(filepath=str(output), relative_remap=False)
bpy.ops.wm.open_mainfile(filepath=str(output), load_ui=False)
scene = bpy.context.scene
new = sample(scene)
assert new[1] == old[1]
assert all(new[f] == old[f] for f in range(join, 289))
assert all(new[f][2:5] == old[f][2:5] for f in range(1, 289))
assert all(new[f][5] == old[f][5] for f in range(81, 289))
assert (scene.frame_start, scene.frame_end, scene.render.fps) == (1, 288, 24)
assert len(bpy.data.libraries) == 6 and all(
    lib.filepath.startswith("//") and Path(bpy.path.abspath(lib.filepath)).is_file()
    for lib in bpy.data.libraries)
sample_frames = (1, 10, 21, 32, 42, 52, 64, 70, 80, 96, 112, 125)
samples = {}
for frame in sample_frames:
    samples[str(frame)] = {
        "source_camera_frame": mapping[frame],
        "camera_move_since_start_m": (new[frame][0] - new[1][0]).length,
        "guide_fade": new[frame][5][0],
    }
    assert abs(new[frame][5][0] - new[frame][5][1]) < 1e-6
assert samples["42"]["camera_move_since_start_m"] > 0.35
assert 0.1 < samples["42"]["guide_fade"] < 0.9
assert samples["70"]["guide_fade"] == 1.0
join_motion = [(new[f + 1][0] - new[f][0]).length for f in range(121, 128)]
join_turn = [degrees(new[f][1].rotation_difference(new[f + 1][1]).angle) for f in range(121, 128)]
(shot / "Notes/v009-overlap.json").write_text(json.dumps({
    "source": source.name,
    "scene": output.name,
    "native_sha256": sha256(output.read_bytes()).hexdigest(),
    "matched_later_camera": [join, 288],
    "new_guide_fade_frames": [guide_start, guide_end],
    "samples": samples,
    "join_step_m": join_motion,
    "join_turn_degrees": join_turn,
}, indent=2) + "\n", encoding="utf-8")
