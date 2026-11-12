"""Keep the reconstruction color visible through the S06 context fade."""

from hashlib import sha256
import json
from pathlib import Path

import bpy


shot = Path(__file__).resolve().parents[1]
source = shot / "Scenes/S06_continuous-glide_v012.blend"
output = shot / "Scenes/S06_stable-reconstruction_v013.blend"
assert Path(bpy.data.filepath).resolve() == source and not output.exists()
context_name = "S06 | physical World live context"
surface_name = "A | reconstructed wall beginning to open"


def materials(scene):
    context = scene.objects[context_name]
    assign = next(node for node in context.modifiers[0].node_group.nodes
                  if node.bl_idname == "GeometryNodeSetMaterial")
    return assign.inputs["Material"].default_value, scene.objects[surface_name].data.materials[0]


def states(scene):
    rock, wall = materials(scene)
    result = {}
    for frame in range(64, 136):
        scene.frame_set(frame)
        camera = scene.camera
        result[str(frame)] = (
            rock.node_tree.nodes["SHOT_VISIBILITY"].inputs[0].default_value,
            wall.node_tree.nodes["Mix Shader"].inputs[0].default_value,
            tuple(camera.location), tuple(camera.rotation_quaternion),
        )
    return result


scene = bpy.context.scene
context, texture = materials(scene)
assert context.library is None and context.surface_render_method == texture.surface_render_method == "BLENDED"
before = states(scene)
assert len({round(before[str(f)][1], 6) for f in range(88, 97)}) == 1
context.surface_render_method = "DITHERED"
scene.frame_set(1)
scene.render.filepath = "//../Cache/v013/preview/S06_"
bpy.ops.wm.save_as_mainfile(filepath=str(output), relative_remap=False)
bpy.ops.wm.open_mainfile(filepath=str(output), load_ui=False)
scene = bpy.context.scene
assert states(scene) == before
context, texture = materials(scene)
assert context.surface_render_method == "DITHERED" and texture.surface_render_method == "BLENDED"
assert (scene.frame_start, scene.frame_end, scene.render.fps) == (1, 288, 24)
assert len(bpy.data.libraries) == 6 and all(
    lib.filepath.startswith("//") and Path(bpy.path.abspath(lib.filepath)).is_file()
    for lib in bpy.data.libraries)
record = {
    "source": source.name,
    "scene": output.name,
    "native_sha256": sha256(output.read_bytes()).hexdigest(),
    "material": context.name,
    "previous_method": "BLENDED",
    "revised_method": "DITHERED",
    "reconstruction_material": texture.name,
    "matched_camera_and_fade_frames": [64, 135],
    "reconstruction_fade_at_90_and_92": [before[str(f)][1] for f in (90, 92)],
}
(shot / "Notes/v013-reconstruction-dropout.json").write_text(
    json.dumps(record, indent=2) + "\n", encoding="utf-8")
