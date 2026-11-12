"""Bring the existing hero turn forward to the close-up cut."""

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


source = candidate.with_name("S07_soft-ending_v008.blend")
successor = candidate.with_name("S07_turn-during-pullback_v009.blend")
first, last = 121, 192


def fade_samples(scene):
    fade = scene.compositing_node_group.nodes["Final fade to nothingness"].inputs[0]
    samples = []
    for frame in range(1, last + 1):
        scene.frame_set(frame)
        samples.append(fade.default_value)
    return samples


def build():
    source_sha = "d24c56dfc81417b2d7a8fb3591dcb00646a1890b3d153e926f8dd617d53fb3a2"
    assert sha256(source.read_bytes()).hexdigest() == source_sha
    scene = open_scene(source)
    camera_and_lights = state_samples(scene, [])
    previous_shots = state_samples(scene, hero_objects(scene))[:first - 1]
    fades = fade_samples(scene)
    control = scene.objects["ECCO_ROTATION_X"]
    animation = control.animation_data
    curves = animation.action.layers[0].strips[0].channelbag(animation.action_slot).fcurves
    curve = curves.find("rotation_euler", index=0)
    assert len(curve.keyframe_points) == 3
    final_angle = degrees(curve.keyframe_points[-1].co.y)
    curve.keyframe_points.clear()
    span = last - first
    coordinates = []
    # Sample a cubic Hermite turn with nonzero entry and exit speeds in degrees per frame.
    for frame in range(first, last + 1):
        t = (frame - first) / span
        angle = (final_angle * (3 * t ** 2 - 2 * t ** 3)
                 + 0.40 * span * t * (1 - t) ** 2
                 + 0.08 * span * t ** 2 * (t - 1))
        coordinates.extend((frame, radians(angle)))
    curve.keyframe_points.add(span + 1)
    curve.keyframe_points.foreach_set("co", coordinates)
    for key in curve.keyframe_points:
        key.interpolation = "LINEAR"
    curve.extrapolation = "CONSTANT"
    curve.update()

    scene.frame_set(1)
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=str(successor), relative_remap=False)
    scene = open_scene(successor)
    control = scene.objects["ECCO_ROTATION_X"]
    objects = hero_objects(scene)
    assert state_samples(scene, []) == camera_and_lights
    assert state_samples(scene, objects)[:first - 1] == previous_shots
    assert fade_samples(scene) == fades
    assert len(bpy.data.libraries) == 2
    assert all(library.filepath.startswith("//") and Path(bpy.path.abspath(library.filepath)).is_file()
               for library in bpy.data.libraries)
    angles = {}
    for frame in range(first, last + 1):
        scene.frame_set(frame)
        angles[frame] = degrees(control.rotation_euler.x)
        if frame >= 156:
            corners = [world_to_camera_view(scene, scene.camera, obj.matrix_world @ Vector(corner))
                       for obj in objects for corner in obj.bound_box]
            assert all(.03 < point.x < .97 and .03 < point.y < .97 for point in corners), frame
    speeds = [angles[frame + 1] - angles[frame] for frame in range(first, last)]
    assert all(a > b > 0 for a, b in zip(speeds, speeds[1:])), speeds
    assert angles[first] == 0 and angles[136] > 5 and abs(angles[last] - 16) < 1e-5
    write_json(evidence / "v009-turn.json", {
        "input_sha256": source_sha, "candidate_sha256": sha256(successor.read_bytes()).hexdigest(),
        "camera_light_and_fade_frames_matched": 192, "earlier_hardware_frames_matched": first - 1,
        "relative_libraries_resolved": len(bpy.data.libraries), "hero_bounds_checked": [156, 192],
        "turn_frames": [first, last], "turn_degrees": angles,
        "initial_degrees_per_frame": speeds[0], "final_degrees_per_frame": speeds[-1],
    })


parser = argparse.ArgumentParser()
parser.add_argument("stage", choices=("build", "preview", "full"))
args = parser.parse_args(sys.argv[sys.argv.index("--") + 1:])
if args.stage == "build":
    build()
elif args.stage == "preview":
    render_preview(960, 540, 16, scene_path=successor, frames=range(first, last + 1),
                   checks=(121, 122, 128, 136, 156, 162, 174, 190, 192), version="v009")
else:
    render_preview(960, 540, 16, scene_path=successor, frames=range(1, 105),
                   checks=(1, 16, 38, 60, 61, 78, 98, 104, 105, 120, 121, 136, 156, 162, 174, 190, 192),
                   version="v009", cache_kind="full")
