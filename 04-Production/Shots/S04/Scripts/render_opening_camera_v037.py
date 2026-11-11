"""Render the changed camera interval from the saved S04 candidate."""
import json
from pathlib import Path
import sys
from time import perf_counter

import bpy

mode = sys.argv[sys.argv.index("--") + 1]
scene = bpy.context.scene
assert (scene.frame_start, scene.frame_end, scene.render.fps) == (1, 432, 24)
assert all(lib.filepath.startswith("//") and Path(bpy.path.abspath(lib.filepath)).is_file()
           for lib in bpy.data.libraries)
missing = [item.name for prop in bpy.data.bl_rna.properties if prop.type == "COLLECTION"
           for item in getattr(bpy.data, prop.identifier) if getattr(item, "is_missing", False)]
assert not missing, missing
cache = Path(bpy.data.filepath).parent.parent / "Cache/v037" / mode
cache.mkdir(parents=True, exist_ok=True)
scene.render.resolution_percentage = 75
setup = {}
for frame in (1, 62):
    scene.frame_set(frame)
    before = perf_counter()
    bpy.ops.render.render()
    setup[frame] = perf_counter() - before
    print("SETUP", frame, setup[frame], flush=True)

frames = (1, 16, 32, 48, 62, 63, 85) if mode == "bench" else range(1, 63)
timings = {}
for frame in frames:
    scene.frame_set(frame)
    scene.render.filepath = str(cache / f"frame_{frame:04d}.png")
    before = perf_counter()
    bpy.ops.render.render(write_still=True)
    seconds = perf_counter() - before
    assert seconds < 5, (frame, seconds)
    timings[frame] = seconds
    (cache / "timings.json").write_text(json.dumps({"setup": setup, "frames": timings}, indent=2) + "\n")
    print("FRAME", frame, seconds, flush=True)
