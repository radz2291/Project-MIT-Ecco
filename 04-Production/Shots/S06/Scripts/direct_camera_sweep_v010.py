"""Replace the stepped S06 opening travel with one continuous camera sweep."""

from hashlib import sha256
import json
from math import degrees
from pathlib import Path

import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Quaternion, Vector


shot = Path(__file__).resolve().parents[1]
source = shot / "Scenes/S06_overlapped-reveal_v009.blend"
output = shot / "Scenes/S06_direct-sweep_v010.blend"
assert Path(bpy.data.filepath).resolve() == source and not output.exists()
join = 145
checks = (1, 25, 48, 70, 90, 110, 132, 144, 145, 150)


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


def spherical_curve(a, b, c, d, t):
    ab, bc, cd = a.slerp(b, t), b.slerp(c, t), c.slerp(d, t)
    return ab.slerp(bc, t).slerp(bc.slerp(cd, t), t)


scene = bpy.context.scene
camera = scene.camera
old = states(scene)
p0, q0 = old[1][:2]
p3, q3 = old[join][:2]
following, following_q = old[join + 1][:2]
span = join - 1
p1 = p0 + Vector((0.0, -0.86, 0.06))
p2 = p3 - (following - p3) * (span / 3)
q1 = q0.slerp(q3, 0.20)
exit_turn = q3.rotation_difference(following_q)
if exit_turn.w < 0:
    exit_turn.negate()
axis, angle = exit_turn.to_axis_angle()
q2 = q3 @ Quaternion(axis, -angle * span / 3)

edits = {1: (p0, q0)}
for frame in range(2, join):
    t = (frame - 1) / span
    r = 1 - t
    position = p0 * r**3 + p1 * (3 * r**2 * t) + p2 * (3 * r * t**2) + p3 * t**3
    edits[frame] = position, spherical_curve(q0, q1, q2, q3, t)

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
    assert changed == join - 1
    curve.update()

scene.frame_set(1)
scene.render.filepath = "//../Cache/v010/preview/S06_"
bpy.ops.wm.save_as_mainfile(filepath=str(output), relative_remap=False)
bpy.ops.wm.open_mainfile(filepath=str(output), load_ui=False)
scene = bpy.context.scene
new = states(scene)
assert new[1] == old[1]
assert all(new[f] == old[f] for f in range(join, 289))
assert all(new[f][2:] == old[f][2:] for f in range(1, 289))
assert (scene.frame_start, scene.frame_end, scene.render.fps) == (1, 288, 24)
assert len(bpy.data.libraries) == 6 and all(
    lib.filepath.startswith("//") and Path(bpy.path.abspath(lib.filepath)).is_file()
    for lib in bpy.data.libraries)
chord = (p3 - p0).normalized()
assert all((new[f + 1][0] - new[f][0]).dot(chord) > 0 for f in range(1, join))
samples = {}
for f in checks:
    scene.frame_set(f)
    obj = scene.objects["A | reconstructed wall beginning to open"].evaluated_get(
        bpy.context.evaluated_depsgraph_get())
    uv = [world_to_camera_view(scene, scene.camera, obj.matrix_world @ v.co)
          for v in list(obj.data.vertices)[::15]]
    samples[str(f)] = {
        "camera_location": list(new[f][0]),
        "guide_fade": new[f][5],
        "surface_bounds": [min(p.x for p in uv), min(p.y for p in uv),
                           max(p.x for p in uv), max(p.y for p in uv)],
    }
join_steps = [(new[f + 1][0] - new[f][0]).length for f in range(join - 3, join + 3)]
join_turns = [degrees(new[f][1].rotation_difference(new[f + 1][1]).angle)
              for f in range(join - 3, join + 3)]
assert abs(join_steps[2] - join_steps[3]) < 0.01
assert abs(join_turns[2] - join_turns[3]) < 0.25
(shot / "Notes/v010-direct-sweep.json").write_text(json.dumps({
    "source": source.name,
    "scene": output.name,
    "native_sha256": sha256(output.read_bytes()).hexdigest(),
    "camera_edit_frames": [1, join - 1],
    "matched_camera_frames": [join, 288],
    "position_curve_controls": [list(v) for v in (p0, p1, p2, p3)],
    "join_steps_m": join_steps,
    "join_turn_degrees": join_turns,
    "grid_visibility_matched": True,
    "samples": samples,
}, indent=2) + "\n", encoding="utf-8")
