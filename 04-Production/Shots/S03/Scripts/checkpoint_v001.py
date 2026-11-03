"""Save the S03 collaboration baseline, then reopen and test selected frames."""
import bpy
import json
import sys
from pathlib import Path
from time import perf_counter

root = Path(__file__).resolve().parents[1]
candidate = root / "Scenes/S03_production_v001.blend"

def inspect():
    scene = bpy.context.scene
    return {
        "scene": scene.name,
        "range": [scene.frame_start, scene.frame_end],
        "fps": scene.render.fps / scene.render.fps_base,
        "camera": scene.camera.name,
        "markers": [[m.frame, m.name] for m in scene.timeline_markers],
        "actions": len(bpy.data.actions),
        "objects": len(scene.objects),
        "libraries": {lib.name: str(Path(bpy.path.abspath(lib.filepath)).resolve())
                      for lib in bpy.data.libraries},
        "missing": [p for p in bpy.utils.blend_paths(absolute=True, packed=False, local=False)
                    if p and not Path(p).exists()],
    }

source = inspect()
if candidate.exists() and "--verify-existing" not in sys.argv:
    raise FileExistsError(candidate)
bpy.context.scene.frame_set(source["range"][0])
bpy.ops.wm.save_as_mainfile(filepath=str(candidate), relative_remap=True)
bpy.ops.wm.open_mainfile(filepath=str(candidate))
saved = inspect()
assert source == saved, (source, saved)
assert all(Path(path).name == "S03_v006_amplitude-test.blend" for path in saved["missing"]), saved["missing"]
assert not any(lib.is_missing for lib in bpy.data.libraries)
scene = bpy.context.scene
timings = []
for frame in (1, 216, 241, 432):
    start = perf_counter()
    scene.frame_set(frame)
    scene.camera.data.update_tag()
    bpy.context.view_layer.update()
    scene.render.filepath = str(root / f"Previews/S03_v001_f{frame:04d}.png")
    bpy.ops.render.render(write_still=True)
    seconds = perf_counter() - start
    timings.append({"frame": frame, "seconds": round(seconds, 3)})
    if seconds >= 5:
        break
evidence = {"saved": saved, "engine": scene.render.engine,
            "resolution": [scene.render.resolution_x, scene.render.resolution_y,
                           scene.render.resolution_percentage],
            "render_to_png": timings}
(root / "Notes/verification_v001.json").write_text(json.dumps(evidence, indent=2) + "\n")
