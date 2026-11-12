"""Bring the wider v018 establishing angle into the v028 Section 5 render."""

from hashlib import sha256
import json
from math import degrees
import os
from pathlib import Path
import shutil
from time import perf_counter

import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree


native = Path(bpy.data.filepath)
assert native.name == "S05_stretched-grid_v028.blend"
shot = native.parents[1]
root = shot.parents[2]
previs = root / "05-Previs/Section-05_Hydraulic-Enhancement/Full-Previs_v018/Scenes/S05_full-cinematic_v018.blend"
destination = shot / "Scenes/S05_establishing-opening_v029.blend"
source_cache = shot / "Cache/v028/full-vulkan"
cache = shot / "Cache/v029/full-vulkan"
cache.mkdir(parents=True, exist_ok=True)
assert shutil.disk_usage(cache).free > 6 * 1024**3
source_timings = json.loads((source_cache / "timings.json").read_text(encoding="utf-8"))
assert source_timings["settings"]["native_sha256"] == sha256(native.read_bytes()).hexdigest()
assert len(source_timings["frames"]) == 432 and max(source_timings["frames"].values()) < 5
end_opening = 56
blend_start = 9
opening = range(1, end_opening + 1)
tail = range(end_opening + 1, 433)


def pose(camera):
    return (camera.location.copy(), camera.rotation_quaternion.copy(),
            (camera.data.lens, camera.data.shift_x, camera.data.shift_y))


def signature(scene, frame, subframe=0.0):
    scene.frame_set(frame, subframe=subframe)
    camera = scene.camera
    return (tuple(tuple(row) for row in camera.matrix_world), camera.data.lens,
            camera.data.shift_x, camera.data.shift_y)


def fcurves(id):
    data = id.animation_data
    return data.action.layers[0].strips[0].channelbag(data.action_slot).fcurves


def ease(frame):
    t = max(0.0, min(1.0, (frame - blend_start) / (end_opening + 1 - blend_start)))
    return t**3 * (10 + t * (-15 + 6 * t))


def coverage(scene):
    ground = scene.objects["S05 Continuous borehole and ground"]
    mesh = ground.data
    surface = BVHTree.FromPolygons([ground.matrix_world @ v.co for v in mesh.vertices],
                                  [tuple(p.vertices) for p in mesh.polygons])
    count = 0
    for frame in opening:
        scene.frame_set(frame)
        camera = scene.camera
        corners = camera.data.view_frame(scene=scene)
        xs, ys = sorted({v.x for v in corners}), sorted({v.y for v in corners})
        assert len(xs) == len(ys) == 2
        for x in (xs[0], sum(xs) / 2, xs[1]):
            for y in (ys[0], sum(ys) / 2, ys[1]):
                direction = camera.matrix_world.to_3x3() @ Vector((x, y, corners[0].z))
                assert surface.ray_cast(camera.matrix_world.translation, direction.normalized())[0] is not None
                count += 1
    return count


bpy.ops.wm.open_mainfile(filepath=str(previs))
scene = bpy.context.scene
wide = {}
for frame in opening:
    scene.frame_set(frame)
    assert scene.camera.parent is None and not scene.camera.constraints
    wide[frame] = pose(scene.camera)
first_shot = signature(scene, 1)
bpy.ops.wm.open_mainfile(filepath=str(native))
scene = bpy.context.scene
camera = scene.camera
assert camera.parent is None and not camera.constraints
baseline_tail = {(frame, sub): signature(scene, frame, sub)
                 for frame in tail for sub in (0.0, 0.5) if frame < 432 or not sub}
target = {}
for frame in opening:
    scene.frame_set(frame)
    target[frame] = pose(camera)
assert (scene.frame_start, scene.frame_end, scene.render.fps, scene.render.fps_base) == (1, 432, 24, 1.0)
assert (scene.render.resolution_x, scene.render.resolution_y, scene.render.resolution_percentage) == (960, 540, 100)

if not destination.exists():
    opening_values = {}
    for frame in opening:
        weight = ease(frame)
        a, qa, optics_a = wide[frame]
        b, qb, optics_b = target[frame]
        opening_values[frame] = {
            "location": a.lerp(b, weight),
            "rotation_quaternion": qa if not weight else qa.slerp(qb, weight),
            **{name: [x + (y - x) * weight] for name, x, y
               in zip(("lens", "shift_x", "shift_y"), optics_a, optics_b)},
        }
    for fc in (*fcurves(camera), *fcurves(camera.data)):
        changed = set()
        for key in fc.keyframe_points:
            frame = round(key.co.x)
            if frame in opening_values:
                key.co.y = opening_values[frame][fc.data_path][fc.array_index]
                changed.add(frame)
        assert len(changed) == end_opening, fc.data_path
        fc.update()
    assert signature(scene, 1) == first_shot
    for marker in scene.timeline_markers:
        if marker.frame == 1:
            marker.name = "A / wide establishing view"
    scene.timeline_markers.new("A / rejoin close tracking", frame=end_opening + 1)
    scene.frame_set(1)
    scene.render.filepath = "//../Cache/v029/full-vulkan/S05_"
    bpy.ops.wm.save_as_mainfile(filepath=str(destination), relative_remap=False)
bpy.ops.wm.open_mainfile(filepath=str(destination))
scene = bpy.context.scene
camera = scene.camera
assert signature(scene, 1) == first_shot
assert all(signature(scene, *sample) == previous for sample, previous in baseline_tail.items())
assert len(bpy.data.libraries) == 4 and all(
    lib.filepath.startswith("//") and Path(bpy.path.abspath(lib.filepath)).is_file()
    for lib in bpy.data.libraries)
rays = coverage(scene)
join = []
for frame in (55, 56, 57, 58, 59):
    scene.frame_set(frame)
    join.append(pose(camera))
step_m = [(a[0] - b[0]).length for a, b in zip(join, join[1:])]
step_deg = [degrees(a[1].rotation_difference(b[1]).angle) for a, b in zip(join, join[1:])]
assert max(step_m) < 0.02 and max(step_deg) < 1.0, (step_m, step_deg)
settings = {**source_timings["settings"], "source": destination.name,
            "native_sha256": sha256(destination.read_bytes()).hexdigest()}
assert settings["samples"] == scene.eevee.taa_render_samples
assert settings["ray_tracing"] == scene.eevee.use_raytracing
assert settings["compositing"] == scene.render.use_compositing
verification = {
    "establishing_reference": previs.name,
    "source": native.name,
    "scene": destination.name,
    "scene_sha256": settings["native_sha256"],
    "changed_camera_frames": [1, end_opening],
    "wide_source_only_frames": [1, blend_start],
    "first_frame_camera_matches_v018": True,
    "unchanged_tail_camera_samples": len(baseline_tail),
    "join_step_m": step_m,
    "join_step_deg": step_deg,
    "camera_coverage_rays": rays,
}
(shot / "Notes/v029-opening-camera.json").write_text(
    json.dumps(verification, indent=2) + "\n", encoding="utf-8")

report = cache / "timings.json"
state = json.loads(report.read_text(encoding="utf-8")) if report.exists() else {
    "settings": settings, "benchmark": {}, "setup": [], "over_cap_attempts": [],
    "frames": {}, "reused_frames": list(tail), "reused_source": native.name,
}
assert state["settings"] == settings


def save():
    temp = report.with_suffix(".tmp")
    temp.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    temp.replace(report)


def render(frame, path):
    scene.frame_set(frame)
    scene.render.filepath = str(path)
    start = perf_counter()
    bpy.ops.render.render(write_still=True)
    return perf_counter() - start


scene.render.image_settings.file_format = "PNG"
scene.frame_set(28)
started = perf_counter()
bpy.ops.render.render()
state["setup"].append(perf_counter() - started)
save()
if not state["benchmark"]:
    benchmarks = {}
    for frame in (1, 9, 16, 23, 28, 34, 42, 49, 56):
        elapsed = render(frame, cache / "bench.png")
        print("BENCH", frame, round(elapsed, 3), flush=True)
        assert elapsed < 5, ("Benchmark over the frame cap", frame, elapsed)
        benchmarks[str(frame)] = elapsed
    state["benchmark"] = benchmarks
    save()
assert len(state["benchmark"]) == 9 and max(state["benchmark"].values()) < 5
for frame in opening:
    path = cache / f"S05_{frame:04d}.png"
    key = str(frame)
    if key in state["frames"] and path.is_file() and path.stat().st_size:
        continue
    pending = cache / "pending.png"
    for attempt in range(2):
        elapsed = render(frame, pending)
        if elapsed < 5:
            break
        state["over_cap_attempts"].append({"frame": frame, "seconds": elapsed})
        save()
        print("RETRY", frame, round(elapsed, 3), flush=True)
    assert elapsed < 5, ("Frame over the cap", frame, elapsed)
    pending.replace(path)
    state["frames"][key] = elapsed
    save()
    if frame == 1 or frame % 12 == 0:
        print("FRAME", frame, round(elapsed, 3), flush=True)
for frame in tail:
    name = f"S05_{frame:04d}.png"
    original, copy = source_cache / name, cache / name
    if not copy.is_file():
        os.link(original, copy)
    assert original.samefile(copy)
    state["frames"][str(frame)] = source_timings["frames"][str(frame)]
save()
assert len(state["frames"]) == 432 and max(state["frames"].values()) < 5
print("COMPLETE", len(opening), len(tail), flush=True)
