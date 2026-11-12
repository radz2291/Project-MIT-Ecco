"""Benchmark and render the complete picture-only S05 v028 frame sequence."""

from hashlib import sha256
import json
from pathlib import Path
import shutil
from time import perf_counter

import bpy


native = Path(bpy.data.filepath)
scene = bpy.context.scene
assert native.name == "S05_stretched-grid_v028.blend"
assert (scene.frame_start, scene.frame_end, scene.frame_step, scene.render.fps, scene.render.fps_base) == (
    1, 432, 1, 24, 1.0)
assert (scene.render.resolution_x, scene.render.resolution_y, scene.render.resolution_percentage) == (960, 540, 100)
assert scene.render.engine == "BLENDER_EEVEE"
assert len(bpy.data.libraries) == 4 and all(
    lib.filepath.startswith("//") and Path(bpy.path.abspath(lib.filepath)).is_file()
    for lib in bpy.data.libraries)
cache = native.parent.parent / "Cache/v028/full-vulkan"
cache.mkdir(parents=True, exist_ok=True)
assert shutil.disk_usage(cache).free > 6 * 1024**3
report = cache / "timings.json"
bench_frames = (1, 25, 50, 72, 96, 120, 144, 165, 185, 205, 222, 246, 270, 300, 330, 360, 390, 416, 432)

scene.render.image_settings.file_format = "PNG"
settings = {
    "source": native.name,
    "native_sha256": sha256(native.read_bytes()).hexdigest(),
    "engine": scene.render.engine,
    "backend": "Vulkan",
    "resolution": [960, 540],
    "fps": 24,
    "samples": scene.eevee.taa_render_samples,
    "ray_tracing": scene.eevee.use_raytracing,
    "compositing": scene.render.use_compositing,
}
state = json.loads(report.read_text(encoding="utf-8")) if report.exists() else {
    "settings": settings, "setup": [], "benchmark": {}, "frames": {}, "over_cap_attempts": [],
}
assert state["settings"] == settings


def save_report():
    pending = report.with_suffix(".tmp")
    pending.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    pending.replace(report)


def render_still(frame, target):
    scene.frame_set(frame)
    scene.render.filepath = str(target)
    start = perf_counter()
    bpy.ops.render.render(write_still=True)
    return perf_counter() - start


scene.frame_set(205)
start = perf_counter()
bpy.ops.render.render()
state["setup"].append(perf_counter() - start)
save_report()
print("SETUP", round(state["setup"][-1], 3), flush=True)

if not state["benchmark"]:
    benchmarks = {}
    for frame in bench_frames:
        elapsed = render_still(frame, cache / "benchmark.png")
        print("BENCH", frame, round(elapsed, 3), flush=True)
        assert elapsed < 5.0, ("Benchmark over the frame cap", frame, elapsed)
        benchmarks[str(frame)] = elapsed
    state["benchmark"] = benchmarks
    save_report()
assert sorted(map(int, state["benchmark"])) == list(bench_frames)
assert max(state["benchmark"].values()) < 5.0

for frame in range(1, 433):
    key = str(frame)
    final = cache / f"S05_{frame:04d}.png"
    if key in state["frames"] and final.is_file() and final.stat().st_size:
        continue
    pending = cache / "pending.png"
    for attempt in range(2):
        elapsed = render_still(frame, pending)
        if elapsed < 5.0:
            break
        state["over_cap_attempts"].append({"frame": frame, "seconds": elapsed})
        save_report()
        print("RETRY", frame, round(elapsed, 3), flush=True)
    assert elapsed < 5.0, ("Two attempts exceeded the frame cap", frame, elapsed)
    pending.replace(final)
    state["frames"][key] = elapsed
    save_report()
    if frame == 1 or frame % 24 == 0:
        print("FRAME", frame, round(elapsed, 3), flush=True)

assert sorted(map(int, state["frames"])) == list(range(1, 433))
assert max(state["frames"].values()) < 5.0
print("COMPLETE", len(state["frames"]), round(max(state["frames"].values()), 3), flush=True)
