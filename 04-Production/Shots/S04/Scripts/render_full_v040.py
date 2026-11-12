"""Benchmark or render S04 with resumable, measured output."""
from hashlib import sha256
import json
from pathlib import Path
import shutil
import sys
from time import perf_counter

import bpy

mode, backend, percent = sys.argv[sys.argv.index("--") + 1:]
assert mode in {"bench", "full"} and backend in {"vulkan", "opengl"}
scene = bpy.context.scene
native = Path(bpy.data.filepath)
assert native.name == "S04_continuous-shared-waveform_v040.blend"
assert (scene.frame_start, scene.frame_end, scene.render.fps) == (1, 432, 24)
assert all(lib.filepath.startswith("//") and Path(bpy.path.abspath(lib.filepath)).is_file()
           for lib in bpy.data.libraries)
assert not [item.name for prop in bpy.data.bl_rna.properties if prop.type == "COLLECTION"
            for item in getattr(bpy.data, prop.identifier) if getattr(item, "is_missing", False)]
cache = native.parent.parent / "Cache/v040" / f"{mode}-{backend}-{percent}"
cache.mkdir(parents=True, exist_ok=True)
assert shutil.disk_usage(cache).free > 12 * 1024**3
scene.render.resolution_percentage = int(percent)
report = cache / "timings.json"
settings = {
    "native_sha256": sha256(native.read_bytes()).hexdigest(),
    "backend": backend, "percent": int(percent),
    "resolution": [scene.render.resolution_x * int(percent) // 100,
                   scene.render.resolution_y * int(percent) // 100],
    "samples": scene.eevee.taa_render_samples, "fps": scene.render.fps,
}
state = json.loads(report.read_text()) if mode == "full" and report.exists() else {
    "settings": settings, "setup_attempts": [], "frames": {},
}
assert state["settings"] == settings
if mode == "full":
    proof = json.loads((cache.parent / f"bench-{backend}-{percent}/timings.json").read_text())
    assert proof["settings"] == settings
    assert len(proof["frames"]) == 19 and max(proof["frames"].values()) < 5

setup = {}
for frame in (1, 82, 195, 285, 300, 330, 370):
    scene.frame_set(frame)
    start = perf_counter()
    bpy.ops.render.render()
    setup[str(frame)] = perf_counter() - start
    print("SETUP", frame, round(setup[str(frame)], 3), flush=True)
state["setup_attempts"].append(setup)

def write_report():
    temp = report.with_suffix(".tmp")
    temp.write_text(json.dumps(state, indent=2) + "\n")
    temp.replace(report)

frames = (1, 32, 74, 78, 82, 94, 101, 190, 194, 210, 260, 265, 285, 300, 315, 330, 350, 370, 432)
if mode == "full":
    frames = range(1, 433)
for frame in frames:
    filename = cache / f"S04_{frame:04d}.png"
    key = str(frame)
    if key in state["frames"] and filename.is_file() and filename.stat().st_size > 0:
        continue
    scene.frame_set(frame)
    scene.render.filepath = str(filename)
    start = perf_counter()
    bpy.ops.render.render(write_still=True)
    elapsed = perf_counter() - start
    assert elapsed < 5, (frame, elapsed)
    state["frames"][key] = elapsed
    write_report()
    print("FRAME", frame, round(elapsed, 3), flush=True)
print("COMPLETE", mode, len(state["frames"]), max(state["frames"].values()), cache, flush=True)
