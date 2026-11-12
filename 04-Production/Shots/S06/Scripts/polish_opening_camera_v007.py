"""Reframe the S06 opening and smooth the approach to its original unfolding camera."""

from hashlib import sha256
import json
from math import degrees
import os
from pathlib import Path
import shutil
import sys
from time import perf_counter

import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector


shot = Path(__file__).resolve().parents[1]
source = shot / "Scenes/S06_shared-reconstruction_v005.blend"
args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["8"]
destination = shot / "Scenes/S06_camera-polish_v007.blend"
cache = shot / "Cache/v007/preview"
if "--existing" in args:
    version_index = args.index("--existing")
    destination = shot / "Scenes" / args[version_index + 1]
    cache = shot / "Cache" / args[version_index + 2] / "preview"
    assert destination.is_file()
if "--cache-name" in args:
    cache = cache.with_name(args[args.index("--cache-name") + 1])
cache.mkdir(parents=True, exist_ok=True)
assert shutil.disk_usage(cache).free > 6 * 1024**3
join = 125
preview_end = int(args[args.index("--end") + 1]) if "--end" in args else 132
preview_start = int(args[args.index("--start") + 1]) if "--start" in args else 1
reuse_cache = None
reuse_start = preview_end + 1
reuse_end = preview_end
surface_name = "A | reconstructed wall beginning to open"
frames_to_check = (1, 25, 52, 76, 96, 112, 124, 125, 132)
if preview_end > 132:
    frames_to_check += (144, preview_end)
if preview_end > 150:
    frames_to_check += (156, 176, 192, 204, 216, 228, 236, 244, 250, 264, 276)
if preview_start != 1:
    frames_to_check = tuple(sorted({preview_start, preview_end, *(
        f for f in (76, 89, 92, 96, 108, 124, 132) if preview_start <= f <= preview_end
    )}))
if "--reuse-tail" in args:
    index = args.index("--reuse-tail")
    reuse_cache = shot / "Cache" / args[index + 1] / "preview"
    reuse_start = int(args[index + 2])
    assert 1 < reuse_start <= preview_end
    frames_to_check = tuple(dict.fromkeys(1 + (reuse_start - 2) * i // 4 for i in range(5)))
elif "--reuse-range" in args:
    index = args.index("--reuse-range")
    reuse_cache = shot / "Cache" / args[index + 1] / "preview"
    reuse_start, reuse_end = map(int, args[index + 2:index + 4])
    assert preview_start <= reuse_start <= reuse_end <= preview_end
frames_to_check = tuple(sorted(set(frames_to_check)))


def ease(t):
    t = max(0.0, min(1.0, t))
    return t**3 * (10 + t * (-15 + 6 * t))


def open_scene(path):
    bpy.ops.wm.open_mainfile(filepath=str(path), load_ui=False)
    scene = bpy.context.scene
    assert (scene.frame_start, scene.frame_end, scene.render.fps) == (1, 288, 24)
    assert len(bpy.data.libraries) == 6 and all(
        lib.filepath.startswith("//") and Path(bpy.path.abspath(lib.filepath)).is_file()
        for lib in bpy.data.libraries)
    return scene


def camera_pose(scene):
    camera = scene.camera
    return camera.location.copy(), camera.rotation_quaternion.copy(), camera.data.lens


def sample(scene):
    data = {}
    for frame in range(1, 289):
        scene.frame_set(frame)
        data[frame] = camera_pose(scene)
    return data


def aim(reference, location, target):
    forward = reference @ Vector((0, 0, -1))
    return forward.rotation_difference((target - location).normalized()) @ reference


def surface_points(scene):
    obj = scene.objects[surface_name].evaluated_get(bpy.context.evaluated_depsgraph_get())
    return [obj.matrix_world @ v.co for v in list(obj.data.vertices)[::9]]


def bounds(scene, camera, points):
    projected = [world_to_camera_view(scene, camera, p) for p in points]
    return (min(p.x for p in projected), min(p.y for p in projected),
            max(p.x for p in projected), max(p.y for p in projected))


def midpoint(points):
    return Vector(tuple((min(p[i] for p in points) + max(p[i] for p in points)) / 2 for i in range(3)))


def measure(data):
    points = [data[f][0] for f in range(1, join + 2)]
    rotations = [data[f][1] for f in range(1, join + 2)]
    velocity = [b - a for a, b in zip(points, points[1:])]
    return {
        "max_step_m": max(v.length for v in velocity),
        "max_step_change_m": max((b - a).length for a, b in zip(velocity, velocity[1:])),
        "max_rotation_step_deg": max(degrees(a.rotation_difference(b).angle)
                                     for a, b in zip(rotations, rotations[1:])),
    }


if not destination.exists():
    scene = open_scene(source)
    camera = scene.camera
    assert camera.parent is None and not camera.constraints and camera.rotation_mode == "QUATERNION"
    original = sample(scene)
    old_bounds = {}
    targets = {}
    for frame in range(1, join):
        scene.frame_set(frame)
        points = surface_points(scene)
        targets[frame] = midpoint(points)
        if frame in frames_to_check:
            old_bounds[str(frame)] = bounds(scene, camera, points)

    scene.frame_set(1)
    points = surface_points(scene)
    target = targets[1]
    direction = (original[1][0] - target).normalized()
    q0 = aim(original[1][1], original[1][0], target)
    low, high = 2.0, 7.0
    for _ in range(16):
        distance = (low + high) / 2
        camera.location = target + direction * distance
        camera.rotation_quaternion = q0
        bpy.context.view_layer.update()
        x0, y0, x1, y1 = bounds(scene, camera, points)
        if min(x0, y0, 1 - x1, 1 - y1) >= 0.09:
            high = distance
        else:
            low = distance
    start = target + direction * high
    end, q1, _ = original[join]
    end_tangent = (original[join + 1][0] - original[join - 1][0]) * ((join - 1) / 2)

    desired = {}
    for frame in range(1, join):
        t = (frame - 1) / (join - 1)
        loc = (start * (2 * t**3 - 3 * t**2 + 1) + end * (3 * t**2 - 2 * t**3)
               + end_tangent * (t**3 - t**2))
        # Ease extra distance in as the reconstruction fills out, then remove it at the join.
        breathing_room = 0.70 * ease((frame - 10) / 55) * (1 - ease((frame - 93) / 32))
        loc += (loc - targets[frame]).normalized() * breathing_room
        reference = q0.slerp(q1, ease(t))
        rotation = aim(reference, loc, targets[frame])
        rotation = rotation.slerp(original[frame][1], ease((frame - 106) / (join - 106)))
        desired[frame] = (loc, rotation)
    anim = camera.animation_data
    curves = anim.action.layers[0].strips[0].channelbag(anim.action_slot).fcurves
    for curve in curves:
        if curve.data_path not in ("location", "rotation_quaternion"):
            continue
        index = 0 if curve.data_path == "location" else 1
        written = 0
        for point in curve.keyframe_points:
            frame = round(point.co.x)
            if frame in desired:
                point.co.y = desired[frame][index][curve.array_index]
                written += 1
        assert written == join - 1
        curve.update()
    scene.frame_set(1)
    scene.render.filepath = "//../Cache/v007/preview/S06_"
    bpy.ops.wm.save_as_mainfile(filepath=str(destination), relative_remap=False)
    scene = open_scene(destination)
    after = sample(scene)
    assert all(after[f] == original[f] for f in range(join, 289))
    assert all(after[f][2] == original[f][2] for f in range(1, 289))
    new_bounds = {}
    for frame in frames_to_check:
        scene.frame_set(frame)
        new_bounds[str(frame)] = bounds(scene, scene.camera, surface_points(scene))
    assert min(*new_bounds["1"][:2], *(1 - x for x in new_bounds["1"][2:])) >= 0.089
    assert min(min(*v[:2], *(1 - x for x in v[2:])) for v in new_bounds.values()) >= 0.01
    old_measure, new_measure = measure(original), measure(after)
    assert new_measure["max_step_m"] < old_measure["max_step_m"]
    assert new_measure["max_step_change_m"] < old_measure["max_step_change_m"]
    (shot / "Notes/v007-camera.json").write_text(json.dumps({
        "source": source.name,
        "scene": destination.name,
        "native_sha256": sha256(destination.read_bytes()).hexdigest(),
        "edited_camera_frames": [1, join - 1],
        "matching_camera_frames": [join, 288],
        "original_opening_motion": old_measure,
        "revised_opening_motion": new_measure,
        "original_reconstruction_bounds": old_bounds,
        "revised_reconstruction_bounds": new_bounds,
    }, indent=2) + "\n", encoding="utf-8")
else:
    scene = open_scene(destination)

samples = int(args[0])
size = tuple(map(int, args[args.index("--size") + 1:args.index("--size") + 3])) if "--size" in args else (960, 540)
scene.render.resolution_x, scene.render.resolution_y = size
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
settings = {"resolution": list(size), "samples": samples, "backend": "Vulkan",
            "compositing": scene.render.use_compositing, "fps": 24}
timings = cache / "timings.json"
state = json.loads(timings.read_text(encoding="utf-8")) if timings.exists() else {
    "settings": settings, "setup": [], "benchmark": {}, "frames": {}, "over_cap_attempts": [],
    "relative_libraries": {lib.name: lib.filepath for lib in bpy.data.libraries},
}
assert state["settings"] == settings
if reuse_cache:
    previous = json.loads((reuse_cache / "timings.json").read_text(encoding="utf-8"))
    assert previous["settings"] == settings
    state["reused_frames"] = [reuse_start, reuse_end]
    state["reused_from"] = reuse_cache.parent.name


def save():
    temp = timings.with_suffix(".tmp")
    temp.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    temp.replace(timings)


def render(frame, path=None):
    scene.frame_set(frame)
    scene.eevee.taa_render_samples = samples
    if path is not None:
        scene.render.filepath = str(path)
    started = perf_counter()
    bpy.ops.render.render(write_still=path is not None)
    return perf_counter() - started


setup_frames = (1, reuse_start - 1) if "--reuse-tail" in args else (
    preview_start, *(f for f in (76, 96, 112, 132, 192, 216, 236, 250) if preview_start <= f <= preview_end), preview_end
)
state["setup"].append({str(frame): render(frame) for frame in dict.fromkeys(setup_frames)})
save()
if not state["benchmark"]:
    results = {}
    for frame in frames_to_check:
        elapsed = render(frame, cache / "benchmark.png")
        if elapsed >= 5:
            state["over_cap_attempts"].append({"benchmark_frame": frame, "seconds": elapsed})
            save()
            elapsed = render(frame, cache / "benchmark.png")
        print("BENCH", frame, round(elapsed, 3), flush=True)
        assert elapsed < 5, ("Benchmark over cap", frame, elapsed)
        results[str(frame)] = elapsed
    state["benchmark"] = results
    save()
assert max(state["benchmark"].values()) < 5
for frame in range(preview_start, preview_end + 1):
    key = str(frame)
    output = cache / f"S06_{frame:04d}.png"
    if reuse_cache and reuse_start <= frame <= reuse_end:
        existing = reuse_cache / output.name
        if not output.is_file():
            os.link(existing, output)
        assert existing.samefile(output) and previous["frames"][key] < 5
        state["frames"][key] = previous["frames"][key]
        save()
        continue
    if key in state["frames"] and output.is_file() and output.stat().st_size:
        continue
    pending = cache / "pending.png"
    for attempt in range(2):
        elapsed = render(frame, pending)
        if elapsed < 5:
            break
        state["over_cap_attempts"].append({"frame": frame, "seconds": elapsed})
        save()
    assert elapsed < 5, ("Preview frame over cap", frame, elapsed)
    pending.replace(output)
    state["frames"][key] = elapsed
    save()
    if frame == preview_start or frame % 24 == 0:
        print("FRAME", frame, round(elapsed, 3), flush=True)
print("COMPLETE", len(state["frames"]), round(max(state["frames"].values()), 3), flush=True)
