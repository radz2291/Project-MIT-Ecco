"""Benchmark or render the saved first-sensor preview, enforcing the render budget."""
import json
from pathlib import Path
import sys
from time import perf_counter

import bpy

mode = sys.argv[sys.argv.index("--") + 1]
scene = bpy.context.scene
assert scene.frame_end == 153 and scene.render.fps == 24
missing = [
    item.name for prop in bpy.data.bl_rna.properties if prop.type == "COLLECTION"
    for item in getattr(bpy.data, prop.identifier) if getattr(item, "is_missing", False)
]
assert not missing, missing
libraries = {Path(bpy.path.abspath(lib.filepath)).name: Path(bpy.path.abspath(lib.filepath)).is_file()
             for lib in bpy.data.libraries}
assert all(libraries.values()), libraries
cache = Path(bpy.path.abspath(scene.render.filepath)).resolve().parent
cache.mkdir(parents=True, exist_ok=True)
output = cache / mode
output.mkdir(exist_ok=True)
print("READY",mode,scene.render.resolution_x,scene.render.resolution_y,libraries,flush=True)
# Initialize renderer/shaders before timed render-to-file frames.
setup = {}
for frame in (1, 134):
    scene.frame_set(frame)
    started = perf_counter()
    bpy.ops.render.render()
    setup[frame] = perf_counter() - started
    print("RENDERER_SETUP", frame, round(setup[frame], 3), flush=True)
(output / "renderer-setup.json").write_text(json.dumps(setup, indent=2) + "\n")
frames = [1, 49, 85, 97, 102, 109, 121, 134, 146, 153] if mode == "bench" else range(1, 154)
timings = {}
for frame in frames:
    scene.frame_set(frame)
    scene.render.filepath = str(output / f"frame_{frame:04d}.png")
    start = perf_counter()
    bpy.ops.render.render(write_still=True)
    seconds = perf_counter() - start
    timings[frame] = seconds
    (output / "timings.json").write_text(json.dumps(timings, indent=2) + "\n")
    print("FRAME",frame,round(seconds,3),flush=True)
    if seconds >= 5:
        raise RuntimeError(f"Frame {frame} exceeded the 5-second cap: {seconds:.3f}")
