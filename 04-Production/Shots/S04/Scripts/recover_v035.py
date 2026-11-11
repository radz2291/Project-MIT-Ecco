"""Recover the selected S04 previs from a staging layout with its original relative links."""
import hashlib
import json
from pathlib import Path
import sys

import bpy

mapping_file, output_file, evidence_file = map(Path, sys.argv[sys.argv.index("--") + 1:])
mapping = {Path(key).name: Path(value).resolve(strict=True)
           for key, value in json.loads(mapping_file.read_text(encoding="utf-8-sig")).items()}
output_file = output_file.resolve()
cache = output_file.parent.parent / "Cache" / "v035"
cache.mkdir(parents=True, exist_ok=True)


def snapshot():
    missing = sorted(
        (prop.identifier, item.name)
        for prop in bpy.data.bl_rna.properties if prop.type == "COLLECTION"
        for item in getattr(bpy.data, prop.identifier) if getattr(item, "is_missing", False)
    )
    assert not missing, missing
    scene = bpy.context.scene
    assert (scene.frame_start, scene.frame_end, scene.render.fps) == (1, 432, 24)
    assert len([obj for obj in scene.objects if obj.type == "CAMERA"]) == 1
    steel = scene.objects["STEEL - capped true source section"]
    depth = [item.value for item in steel.data.attributes["ComputedWearDepth_m"].data]
    mesh_hash = hashlib.sha256(repr(
        ([tuple(v.co) for v in steel.data.vertices],
         [tuple(face.vertices) for face in steel.data.polygons], depth)
    ).encode()).hexdigest()
    effects = sorted(obj.name for obj in scene.objects if obj.name.startswith(
        ("s04-v005-", "STEEL THICKNESS response", "Casing response tail", "Station ")
    ))
    samples = {}
    original_frame = scene.frame_current
    for frame in (1, 63, 85, 94, 104, 175, 190, 206, 216, 261, 300, 336, 365, 400, 432):
        scene.frame_set(frame)
        depsgraph = bpy.context.evaluated_depsgraph_get()
        sensor = next(i.matrix_world.copy() for i in depsgraph.object_instances
                      if i.object.name == "ECCO_SENSOR_REF_01")
        scene_camera = scene.camera
        effects_at_frame = [(name, scene.objects[name].hide_render, tuple(scene.objects[name].scale))
                            for name in effects]
        samples[str(frame)] = {
            "camera_matrix": [list(row) for row in scene_camera.matrix_world],
            "lens_mm": scene_camera.data.lens,
            "sensor_matrix": [list(row) for row in sensor],
            "reveal_x_m": steel.data.materials[0].node_tree.nodes[
                "ECCO axial acquisition front"].outputs[0].default_value,
            "effect_state_sha256": hashlib.sha256(repr(effects_at_frame).encode()).hexdigest(),
        }
    scene.frame_set(original_frame)
    return {"camera": scene.camera.name, "objects": len(scene.objects),
            "steel_mesh_sha256": mesh_hash, "max_authored_wear_mm": max(depth) * 1000,
            "samples": samples}


before = snapshot()
assert {Path(lib.filepath).name for lib in bpy.data.libraries} == set(mapping)
for lib in bpy.data.libraries:
    assert lib.parent is None, lib.filepath
    lib.filepath = bpy.path.relpath(str(mapping[Path(lib.filepath).name]))
scene = bpy.context.scene
scene.render.filepath = "//../Cache/v035/S04_"
scene.frame_set(85)
bpy.context.preferences.filepaths.save_version = 0
bpy.ops.wm.save_as_mainfile(filepath=str(output_file), relative_remap=True)
bpy.ops.wm.open_mainfile(filepath=str(output_file), use_scripts=False)
after = snapshot()
assert before == after
libraries = {}
for lib in bpy.data.libraries:
    assert lib.filepath.startswith("//"), lib.filepath
    target = Path(bpy.path.abspath(lib.filepath)).resolve(strict=True)
    assert target == mapping[target.name], lib.filepath
    libraries[target.name] = lib.filepath
scene = bpy.context.scene
assert Path(bpy.path.abspath(scene.render.filepath)).parent.resolve(strict=True) == cache
evidence_file.write_text(json.dumps({
    "scene": output_file.name, "links": libraries, "reopened_matches_staged_source": True,
    "data": after,
    "render": {"engine": scene.render.engine, "resolution": [scene.render.resolution_x,
              scene.render.resolution_y], "fps": scene.render.fps, "cache": "Cache/v035"},
}, indent=2) + "\n", encoding="utf-8")
print("RECOVERY_OK", len(libraries), scene.camera.name, len(scene.objects))
