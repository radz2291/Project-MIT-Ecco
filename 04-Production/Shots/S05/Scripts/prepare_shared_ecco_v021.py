"""Prepare the approved S05 previs as a linked production scene and render look checks."""

from array import array
from hashlib import sha256
import json
from pathlib import Path
import os
from time import perf_counter

import bpy


production = Path(__file__).resolve().parents[3]
shot = production / "Shots/S05"
archive = production / "Shared/Archive/2026-10-31/Assets/ECCO/ECCO_film_v002.blend"
master = production / "Shared/Assets/Hardware/ECCO/ECCO_film_v003.blend"
satin = master.parent / "Dependencies/Satin_finish_v001.blend"
output = shot / "Scenes/S05_shared-hardware_v021.blend"
evidence = shot / "Notes/v021-shared-hardware.json"
group_name = "ECCO | Satin finish v001"
source = Path(bpy.data.filepath)


def relocate(library, path):
    assert path.is_file(), path
    result = bpy.ops.wm.lib_relocate(
        library=library.name, filepath=str(path), directory=str(path.parent), filename=path.name
    )
    assert result == {"FINISHED"}, result


def geometry(mesh):
    digest = sha256()
    for field, dtype, count, prop in (
        (mesh.vertices, "f", 3, "co"),
        (mesh.loops, "i", 1, "vertex_index"),
        (mesh.polygons, "i", 1, "loop_total"),
        (mesh.polygons, "i", 1, "material_index"),
    ):
        values = array(dtype, [0]) * (len(field) * count)
        field.foreach_get(prop, values)
        digest.update(values.tobytes())
    return digest.hexdigest()


def active_scene():
    return next(scene for scene in bpy.data.scenes if scene.camera and scene.camera.name == "S05_Camera")


def snapshot(scene):
    fixed = scene.objects["S05_FixedHalfBorehole"]
    hydraulics = scene.collection.children["S05_v018_ContinuousHydraulics"]
    hardware = bpy.data.collections["S05_LINKED_HARDWARE"]
    tracked = [fixed, *sorted(hydraulics.all_objects, key=lambda obj: obj.name),
               *sorted(hardware.objects, key=lambda obj: obj.name)]
    timeline = []
    saved_frame = scene.frame_current
    for frame in (1, 50, 72, 120, 165, 205, 246, 330, 390, 432):
        scene.frame_set(frame)
        camera = scene.camera
        timeline.append((
            frame, tuple(tuple(row) for row in camera.matrix_world), camera.data.lens,
            camera.data.dof.focus_distance, camera.data.shift_x, camera.data.shift_y,
            tuple((obj.name, tuple(tuple(row) for row in obj.matrix_world), obj.hide_render)
                  for obj in tracked),
        ))
    scene.frame_set(saved_frame)
    return (
        scene.frame_start, scene.frame_end, scene.render.fps,
        tuple((marker.name, marker.frame) for marker in scene.timeline_markers), timeline,
        geometry(fixed.data), tuple((material.name, material.library is None) for material in fixed.data.materials),
    )


assert source.name == "S05_continuous-camera_v020.blend"
assert not output.exists(), output
scene = active_scene()
assert bpy.context.scene == scene
original = next(lib for lib in bpy.data.libraries if Path(lib.filepath).name == archive.name)
relocate(original, archive)
hardware = list(bpy.data.collections["S05_LINKED_HARDWARE"].objects)
assert len(hardware) == 10
before = snapshot(scene)
mesh_before = {obj.name: geometry(obj.data) for obj in hardware}
relocate(hardware[0].data.library, master)
assert all(Path(bpy.path.abspath(obj.data.library.filepath)).resolve() == master for obj in hardware)
assert mesh_before == {obj.name: geometry(obj.data) for obj in hardware}

with bpy.data.libraries.load(str(satin), link=True) as (available, linked):
    assert group_name in available.node_groups
    linked.node_groups = [group_name]
group = linked.node_groups[0]
steel = hardware[0].material_slots[0].material
assert all(obj.material_slots[0].material == steel for obj in hardware)

# The finish uses the same linked group as the shared master. Keep the shot's own shader context.
sensor_steel = steel.copy()
steel.name = "S05 shared satin | body"
sensor_steel.name = "S05 shared satin | imaging caps"
for material, sensor in ((steel, False), (sensor_steel, True)):
    tree = material.node_tree
    shader = next(node for node in tree.nodes if node.type == "BSDF_PRINCIPLED")
    finish = tree.nodes.new("ShaderNodeGroup")
    finish.node_tree = group
    finish.name = "Shared satin controls"
    finish.inputs["Sensor face"].default_value = float(sensor)
    for channel in ("Base Color", "Roughness", "Metallic"):
        tree.links.new(finish.outputs[channel], shader.inputs[channel])
for obj in hardware:
    if "Imaging port" in obj.name:
        obj.material_slots[0].material = sensor_steel

assert snapshot(scene) == before
for library in bpy.data.libraries:
    if library.parent is None:
        absolute = Path(bpy.path.abspath(library.filepath)).resolve()
        library.filepath = "//" + Path(os.path.relpath(absolute, output.parent)).as_posix()
scene.render.filepath = "//../Cache/v021/S05_"
bpy.ops.wm.save_as_mainfile(filepath=str(output), relative_remap=False)
bpy.ops.wm.open_mainfile(filepath=str(output))
scene = active_scene()
assert snapshot(scene) == before
hardware = list(bpy.data.collections["S05_LINKED_HARDWARE"].objects)
assert mesh_before == {obj.name: geometry(obj.data) for obj in hardware}
assert all(
    Path(bpy.path.abspath(obj.data.library.filepath)).resolve() == master
    and obj.material_slots[0].material.node_tree.nodes["Shared satin controls"].node_tree.library
    for obj in hardware
)
libraries = []
for library in bpy.data.libraries:
    path = Path(bpy.path.abspath(library.filepath, library=library.parent)).resolve()
    assert library.filepath.startswith("//") and path.is_file(), path
    libraries.append(library.filepath)
assert sorted(Path(path).name for path in libraries) == sorted([master.name, satin.name])

record = {
    "source": str(source),
    "scene": str(output),
    "timeline": [scene.frame_start, scene.frame_end, scene.render.fps],
    "camera_and_object_samples": [item[0] for item in before[4]],
    "tracked_hydraulic_objects": len(scene.collection.children["S05_v018_ContinuousHydraulics"].all_objects),
    "fixed_section_materials": before[6],
    "matching_hardware_mesh_hashes": mesh_before,
    "relative_libraries": libraries,
    "proof_renders": [],
}

scene.render.image_settings.file_format = "PNG"
for frame in (50, 205, 390):
    scene.frame_set(frame)
    image = shot / "Previews" / f"S05_shared-hardware_v021_f{frame:04}.png"
    scene.render.filepath = str(image)
    started = perf_counter()
    bpy.ops.render.render(write_still=True)
    record["proof_renders"].append({"frame": frame, "path": str(image), "seconds": perf_counter() - started})
    evidence.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
