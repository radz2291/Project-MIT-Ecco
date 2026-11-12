"""Fit the shared BHA around the registered ECCO housing in Section 5."""

from array import array
from hashlib import sha256
import json
import math
from pathlib import Path
from time import perf_counter

import bpy


shot = Path(__file__).resolve().parents[1]
master = shot.parents[1] / "Shared/Assets/Hardware/BHA/BHA_film_v008.blend"
destination = shot / "Scenes/S05_shared-bha_v022.blend"
scene = bpy.context.scene
legacy = scene.collection.children["S05_LINKED_HARDWARE"]
rig = scene.objects["S05_COMMON_AXIAL_ROTATION"]
fixed = scene.objects["S05_FixedHalfBorehole"]
flow = scene.collection.children["S05_v018_ContinuousHydraulics"]
housing_name = "ECCO_HOUSING_SOURCE_MESH"
sample_frames = (1, 50, 72, 120, 165, 205, 246, 330, 390, 432)
old_frame = scene.frame_current


def matrix_values(matrix):
    return tuple(value for row in matrix for value in row)


def geometry(mesh):
    digest = sha256()
    for field, dtype, size, attr in (
        (mesh.vertices, "f", 3, "co"),
        (mesh.loops, "i", 1, "vertex_index"),
        (mesh.polygons, "i", 1, "loop_total"),
    ):
        data = array(dtype, [0]) * (len(field) * size)
        field.foreach_get(attr, data)
        digest.update(data.tobytes())
    return digest.hexdigest()


def local_state():
    scene_state = {}
    for frame in sample_frames:
        scene.frame_set(frame)
        camera = scene.camera
        scene_state[frame] = (
            matrix_values(camera.matrix_world), camera.data.lens, camera.data.dof.focus_distance,
            camera.data.shift_x, camera.data.shift_y,
            [(obj.name, matrix_values(obj.matrix_world), obj.hide_render)
             for obj in sorted([fixed, *flow.all_objects], key=lambda item: item.name)],
        )
    return scene_state


def instances(roots):
    result = {}
    for item in bpy.context.evaluated_depsgraph_get().object_instances:
        if item.is_instance and item.parent.original in roots and item.object.type == "MESH":
            if item.show_self and not item.object.hide_render:
                name = item.object.name
                assert name not in result, name
                result[name] = item.object.original.data, item.matrix_world.copy()
    return result


assert Path(bpy.data.filepath).name == "S05_shared-hardware_v021.blend"
assert not destination.exists()
before = local_state()
scene.frame_set(old_frame)
originals = {obj.name.removeprefix("S05_"): obj for obj in legacy.objects}
with bpy.data.libraries.load(str(master), link=True) as (available, linked):
    collections = ["WORLD_HARDWARE", "WORLD_UPHOLE_JOINT"]
    assert all(name in available.collections for name in collections)
    linked.collections = collections

roots = []
for name, collection in zip(("S05 Shared BHA v008", "S05 Shared uphole joint"), linked.collections):
    root = bpy.data.objects.new(name, None)
    root.instance_type = "COLLECTION"
    root.instance_collection = collection
    scene.collection.objects.link(root)
    roots.append(root)
stock = instances(roots)
registration = originals[housing_name].matrix_basis @ stock[housing_name][1].inverted()
assert max(abs(value - 1.0) for value in registration.to_scale()) < 1e-6
for name, original in originals.items():
    assert geometry(stock[name][0]) == geometry(original.data), name
for root in roots:
    root.parent = rig
    root.matrix_basis = registration

errors = []
for frame in sample_frames:
    scene.frame_set(frame)
    shared = instances(roots)
    for name, original in originals.items():
        _, placed = shared[name]
        errors.append(max(abs(a - b) for a, b in zip(
            matrix_values(placed), matrix_values(original.matrix_world))))
assert max(errors) < 1e-6, max(errors)
for obj in originals.values():
    bpy.data.objects.remove(obj, do_unlink=True)
bpy.data.collections.remove(legacy)
assert not any(f"S05_{name}" in scene.objects for name in originals)
assert local_state() == before

cutaway_radii = sorted({round(math.hypot(v.co.x, v.co.y), 5) for v in fixed.data.vertices})
new_meshes = {name: value for name, value in shared.items() if name not in originals}
accessories = [placed @ v.co for mesh, placed in new_meshes.values() for v in mesh.vertices]
in_cutaway = [p for p in accessories if fixed.bound_box[0][2] <= p.z <= fixed.bound_box[6][2]]
max_radius = max(math.hypot(p.x, p.y) for p in in_cutaway)
assert max_radius < cutaway_radii[0] - 0.001, (max_radius, cutaway_radii)

for library in bpy.data.libraries:
    if library.parent is None and not library.filepath.startswith("//"):
        library.filepath = bpy.path.relpath(library.filepath)
scene.frame_set(old_frame)
scene.render.filepath = "//../Cache/v022/S05_"
bpy.ops.wm.save_as_mainfile(filepath=str(destination), relative_remap=False)
bpy.ops.wm.open_mainfile(filepath=str(destination))
scene = bpy.context.scene
fixed = scene.objects["S05_FixedHalfBorehole"]
flow = scene.collection.children["S05_v018_ContinuousHydraulics"]
roots = [scene.objects[name] for name in ("S05 Shared BHA v008", "S05 Shared uphole joint")]
assert local_state() == before
assert set(instances(roots)) == set(shared)
libraries = {Path(lib.name).name: lib.filepath for lib in bpy.data.libraries}
for lib in bpy.data.libraries:
    assert lib.filepath.startswith("//"), lib.filepath
    assert Path(bpy.path.abspath(lib.filepath)).is_file(), lib.filepath

record = {
    "source": "S05_shared-hardware_v021.blend",
    "scene": destination.name,
    "relative_libraries": libraries,
    "registered_ecco_parts": len(originals),
    "max_ecco_matrix_component_delta": max(errors),
    "shared_accessory_meshes": len(new_meshes),
    "sample_frames": sample_frames,
    "cutaway_inner_radius_m": cutaway_radii[0],
    "max_added_radius_inside_cutaway_m": max_radius,
    "proof_renders": [],
}
scene.render.image_settings.file_format = "PNG"
for frame in (1, 50, 205, 390, 432):
    scene.frame_set(frame)
    path = shot / "Previews" / f"S05_shared-bha_v022_f{frame:04}.png"
    scene.render.filepath = str(path)
    start = perf_counter()
    bpy.ops.render.render(write_still=True)
    record["proof_renders"].append({"frame": frame, "seconds": perf_counter() - start})
    (shot / "Notes/v022-shared-bha.json").write_text(
        json.dumps(record, indent=2) + "\n", encoding="utf-8")
