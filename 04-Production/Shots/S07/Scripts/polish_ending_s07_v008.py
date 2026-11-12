"""Ease a small axial turn into the final S07 hero pose and soften the fade."""

import argparse
from hashlib import sha256
from math import degrees, radians
from pathlib import Path
import sys

import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prepare_shared_s07_v007 import (
    candidate, evidence, hero_objects, open_scene, render_preview, state_samples, write_json,
)


successor = candidate.with_name("S07_soft-ending_v008.blend")
turn_start, ease_end, turn_end = 142, 154, 192
fade_start, fade_end = 162, 190
turn_degrees = 16


def build():
    previous_sha = "b5003d994df0c0a7f0ccf61aa135d97f6596936cafb67f2a0bb3f2ebcc2f7ed2"
    assert sha256(candidate.read_bytes()).hexdigest() == previous_sha
    scene = open_scene(candidate)
    camera_and_lights = state_samples(scene, [])
    before_turn = state_samples(scene, hero_objects(scene))[:turn_start]
    control = scene.objects["ECCO_ROTATION_X"]
    assert control.rotation_mode == "XYZ" and not control.animation_data
    assert tuple(control.rotation_euler) == (0.0, 0.0, 0.0)

    ease_frames = ease_end - turn_start
    slope = radians(turn_degrees) / (turn_end - ease_end + ease_frames / 2)
    ease_angle = slope * ease_frames / 2
    for frame, angle in ((turn_start, 0.0), (ease_end, ease_angle), (turn_end, radians(turn_degrees))):
        control.rotation_euler.x = angle
        control.keyframe_insert(data_path="rotation_euler", index=0, frame=frame, group="Final hero turn")
    animation = control.animation_data
    curve = animation.action.layers[0].strips[0].channelbag(animation.action_slot).fcurves[0]
    start, eased, end = curve.keyframe_points
    start.interpolation = "BEZIER"
    start.handle_right_type = "FREE"
    start.handle_right = (turn_start + ease_frames / 3, 0)
    eased.handle_left_type = "FREE"
    eased.handle_left = (ease_end - ease_frames / 3, ease_angle - slope * ease_frames / 3)
    eased.interpolation = end.interpolation = "LINEAR"
    curve.update()

    tree = scene.compositing_node_group
    fade = tree.nodes["Final fade to nothingness"].inputs[0]
    action = tree.animation_data
    curves = action.action.layers[0].strips[0].channelbag(action.action_slot).fcurves
    fade_curve = curves.find(fade.path_from_id("default_value"))
    assert fade_curve is not None
    for key in fade_curve.keyframe_points:
        t = max(0, min(1, (key.co.x - fade_start) / (fade_end - fade_start)))
        key.co.y = t ** 3 * (10 - 15 * t + 6 * t ** 2)
    fade_curve.update()
    scene.timeline_markers["Fade to black"].frame = fade_start

    scene.frame_set(1)
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=str(successor), relative_remap=False)
    scene = open_scene(successor)
    control = scene.objects["ECCO_ROTATION_X"]
    objects = hero_objects(scene)
    assert state_samples(scene, []) == camera_and_lights
    assert state_samples(scene, objects)[:turn_start] == before_turn
    assert len(bpy.data.libraries) == 2
    assert all(library.filepath.startswith("//") and Path(bpy.path.abspath(library.filepath)).is_file()
               for library in bpy.data.libraries)

    fade = scene.compositing_node_group.nodes["Final fade to nothingness"].inputs[0]
    angles, fades = [], []
    for frame in range(turn_start, turn_end + 1):
        scene.frame_set(frame)
        angles.append(degrees(control.rotation_euler.x))
        fades.append(fade.default_value)
        if frame >= 156:
            corners = [world_to_camera_view(scene, scene.camera, obj.matrix_world @ Vector(corner))
                       for obj in objects for corner in obj.bound_box]
            assert all(.03 < p.x < .97 and .03 < p.y < .97 for p in corners), frame
    assert abs(angles[-1] - turn_degrees) < 1e-5 and angles[0] == 0
    assert all(b > a for a, b in zip(angles, angles[1:]))
    assert all(b >= a for a, b in zip(fades, fades[1:]))
    assert fades[fade_start - turn_start] == 0 and fades[fade_end - turn_start] == 1
    write_json(evidence / "v008-ending.json", {
        "input_sha256": previous_sha, "candidate_sha256": sha256(successor.read_bytes()).hexdigest(),
        "unchanged_camera_and_light_frames": 192, "unchanged_hardware_frames": turn_start,
        "turn_start": turn_start, "turn_ease_end": ease_end, "turn_end": turn_end,
        "degrees_about_local_x": turn_degrees, "fade": [fade_start, fade_end],
        "hero_bounds_checked": [156, 192], "relative_libraries_resolved": len(bpy.data.libraries),
        "samples": [{"frame": frame, "angle_degrees": angle, "fade": opacity}
                    for frame, angle, opacity in zip(range(turn_start, turn_end + 1), angles, fades)],
    })


parser = argparse.ArgumentParser()
parser.add_argument("stage", choices=("build", "preview"))
args = parser.parse_args(sys.argv[sys.argv.index("--") + 1:])
if args.stage == "build":
    build()
else:
    render_preview(960, 540, 16, scene_path=successor, frames=range(143, 193),
                   checks=(142, 143, 154, 156, 162, 174, 182, 190, 192), version="v008")
