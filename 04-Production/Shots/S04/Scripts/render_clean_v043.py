"""Assemble raw frames for the full-cadence, caption-free v043 delivery."""
import json
import os
from pathlib import Path
from time import perf_counter

import bpy

scene = bpy.context.scene
native = Path(bpy.data.filepath)
assert native.name == "S04_diagonal-composition_v043.blend"
assert (scene.frame_start, scene.frame_end, scene.render.fps) == (1, 432, 24)
cache = native.parent.parent / "Cache"
proof = cache / "v043"
ending = cache / "v042/Full"
out = proof / "CleanFull"
out.mkdir(exist_ok=True)
scene.render.resolution_percentage = 75
assert (scene.render.resolution_x, scene.render.resolution_y) == (1280, 720)
assert all(Path(bpy.path.abspath(lib.filepath)).is_file() for lib in bpy.data.libraries)
times_path = out / "rendered-timings.json"
times = json.loads(times_path.read_text()) if times_path.exists() else {}
for f in (2, 24, 84, 195, 275, 305):
    scene.frame_set(f)
    bpy.ops.render.render()
for frame in range(1, 433):
    name = f"S04_{frame:04d}.png"
    dest = out / name
    reused = (1 <= frame <= 63 and frame % 2 == 1) or (64 <= frame <= 323 and frame % 2 == 0)
    if reused or frame >= 324:
        source = (proof if reused else ending) / name
        assert source.is_file()
        if not dest.exists():
            os.link(source, dest)
        continue
    if str(frame) in times and dest.is_file():
        continue
    scene.frame_set(frame)
    scene.render.filepath = str(dest)
    start = perf_counter()
    bpy.ops.render.render(write_still=True)
    elapsed = perf_counter() - start
    assert elapsed < 5, (frame, elapsed)
    times[str(frame)] = elapsed
    times_path.write_text(json.dumps(times, indent=2) + "\n")
    print("FRAME", frame, round(elapsed, 3), flush=True)
assert len(times) == 161
assert len(list(out.glob("S04_*.png"))) == 432
print("COMPLETE", len(times), max(times.values()), flush=True)
