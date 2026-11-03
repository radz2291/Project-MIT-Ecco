"""Test shared cap lines with the current production camera and local S03 data."""
import bpy
import hashlib
import json
from pathlib import Path
from time import perf_counter

shot = Path(__file__).resolve().parents[1]
assets = shot.parents[1] / "Shared/Assets"
digital = assets / "Effects/DigitalEnvironment"
world = assets / "Environment/Borehole/World_environment_v010.blend"
pin = json.loads((digital / "Metadata/context-derivation.json").read_text(encoding="utf-8-sig"))
assert hashlib.sha256(world.read_bytes()).hexdigest() == pin["world_sha256"]

candidate = shot / "Scenes/S03_shared-lines-proof_v002.blend"
if candidate.exists():
    raise FileExistsError(candidate)
scene = bpy.context.scene
camera = scene.camera.name
collection_name = "ECCO World-derived contextual cap lines v004"
library = digital / "Digital_context_lines_v004.blend"
with bpy.data.libraries.load(str(library), link=True) as (_, target):
    target.collections = [collection_name]
lines = target.collections[0]
assert lines and len(lines.objects) == 2
scene.collection.children.link(lines)

# Mute only the former context curves, including any animated visibility.
empty = bpy.data.node_groups.new("S03 mute legacy context curves", "GeometryNodeTree")
empty.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
empty.nodes.new("NodeGroupOutput")
for name in ("Luminous geological strata", "Subordinate formation survey grid"):
    obj = bpy.data.objects[name]
    obj.modifiers.new("Shared lines proof", "NODES").node_group = empty

bpy.ops.file.make_paths_relative()
bpy.ops.wm.save_as_mainfile(filepath=str(candidate), relative_remap=True)
bpy.ops.wm.open_mainfile(filepath=str(candidate))
scene = bpy.context.scene
assert scene.camera.name == camera
assert len(bpy.data.collections[collection_name].objects) == 2
assert not any(lib.is_missing for lib in bpy.data.libraries)
assert all(lib.filepath.startswith("//") for lib in bpy.data.libraries)
timings = {}
for frame in (1, 216, 241, 432):
    scene.frame_set(frame)
    scene.camera.data.update_tag()
    bpy.context.view_layer.update()
    scene.render.filepath = str(shot / f"Previews/S03_shared-lines_v002_f{frame:04d}.png")
    start = perf_counter()
    bpy.ops.render.render(write_still=True)
    timings[frame] = round(perf_counter() - start, 3)
    if timings[frame] >= 5:
        break
print("PROOF", json.dumps({"world_sha256": pin["world_sha256"],
                          "libraries": [lib.filepath for lib in bpy.data.libraries],
                          "render_to_png_seconds": timings}))
