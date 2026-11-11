"""Use shared ECCO v003 meshes and finish within the existing S04 display."""
from array import array
from hashlib import sha256
import json
from pathlib import Path
import sys

import bpy

master, output, notes = [Path(arg).resolve() for arg in sys.argv[sys.argv.index("--") + 1:]]
source = Path(bpy.data.filepath)
assert source.name == "S04_continuous-opening-camera_v037.blend"
scene = bpy.context.scene
ecco = next(c for c in bpy.data.collections
            if c.name.startswith("ECCO_FILM v022") and c.name.endswith("v033 local display"))
housing = next(obj for obj in ecco.all_objects if obj.name.startswith("ECCO unchanged source housing")
               and obj.type == "MESH")
tracked = (housing.name, "TEMP | Imaging port 1 | removable acoustic cap", "ECCO_SENSOR_REF_01")
frames = (1, 49, 63, 85, 190, 262, 300, 336, 365, 400, 432)
opacity_node = "v033 source surface opacity"


def flat(matrix):
    return tuple(value for row in matrix for value in row)


def snapshot():
    snapshots = {}
    for frame in frames:
        scene.frame_set(frame)
        dg = bpy.context.evaluated_depsgraph_get()
        items = [(item.object.name, flat(item.matrix_world)) for item in dg.object_instances
                 if item.object.name in tracked]
        assert len(items) == len(tracked), (frame, [name for name, _ in items])
        snapshots[frame] = {
            "hardware": dict(items),
            "camera": flat(scene.camera.matrix_world) + (scene.camera.data.lens,),
            "front": scene.objects["STEEL - capped true source section"].data.materials[0]
            .node_tree.nodes["ECCO axial acquisition front"].outputs[0].default_value,
        }
    return snapshots


def fingerprint(mesh):
    digest = sha256()
    coords = array("f", [0]) * (len(mesh.vertices) * 3)
    mesh.vertices.foreach_get("co", coords)
    loops = array("i", [0]) * len(mesh.loops)
    mesh.loops.foreach_get("vertex_index", loops)
    digest.update(coords.tobytes())
    digest.update(loops.tobytes())
    return (len(mesh.polygons), digest.hexdigest())


before = snapshot()
old_housing_materials = tuple(housing.data.materials)
opacities = {}
for frame in frames:
    scene.frame_set(frame)
    opacities[frame] = [
        material.node_tree.nodes[opacity_node].inputs[0].default_value
        for material in old_housing_materials
    ]
    assert max(opacities[frame]) - min(opacities[frame]) < 1e-6

with bpy.data.libraries.load(str(master), link=True) as (_, linked):
    linked.collections = ["ECCO_FILM"]
product = {obj.name: obj for obj in linked.collections[0].all_objects}
old_to_new = {}
for collection in ecco.children:
    for obj in tuple(collection.objects):
        if obj.library and obj.name in product:
            new = product[obj.name]
            old_to_new[obj] = new
            collection.objects.link(new)
            collection.objects.unlink(obj)

finish = {}


def finish_with_existing_fade(stock, previous):
    if stock in finish:
        return finish[stock]
    material = stock.copy()
    material.name = stock.name + " | S04 v038 shared satin with existing fade"
    material.surface_render_method = "BLENDED"
    material.use_transparency_overlap = False
    tree = material.node_tree
    surface = next(node for node in tree.nodes if node.type == "OUTPUT_MATERIAL").inputs["Surface"]
    shader = surface.links[0].from_socket
    transparent = tree.nodes.new("ShaderNodeBsdfTransparent")
    mix = tree.nodes.new("ShaderNodeMixShader")
    mix.name = opacity_node
    tree.links.new(transparent.outputs[0], mix.inputs[1])
    tree.links.new(shader, mix.inputs[2])
    tree.links.new(mix.outputs[0], surface)
    previous_animation = previous.node_tree.animation_data
    animation = tree.animation_data_create()
    animation.action = previous_animation.action
    animation.action_slot = previous_animation.action_slot
    finish[stock] = material
    return material


mapped = []
for obj in tuple(ecco.all_objects):
    if obj.library or obj.type != "MESH":
        continue
    name = "ECCO_HOUSING_SOURCE_MESH" if obj == housing else obj.name
    master_object = product[name]
    assert fingerprint(obj.data) == fingerprint(master_object.data), name
    previous = obj.data.materials[0] if obj.data.materials else None
    basis = obj.matrix_basis.copy()
    inverse = obj.matrix_parent_inverse.copy()
    if obj.parent in old_to_new:
        obj.parent = old_to_new[obj.parent]
        obj.matrix_parent_inverse = inverse
        obj.matrix_basis = basis
    obj.data = master_object.data
    if previous:
        slot = obj.material_slots[0]
        satin = finish_with_existing_fade(master_object.data.materials[0], previous)
        slot.link = "OBJECT"
        slot.material = satin
    mapped.append((obj.name, master_object.name))
assert len(mapped) == 11
assert len(old_to_new) == 7
for library in bpy.data.libraries:
    if not library.filepath.startswith("//"):
        library.filepath = bpy.path.relpath(library.filepath)
scene.frame_set(85)
bpy.context.preferences.filepaths.save_version = 0
bpy.ops.wm.save_as_mainfile(filepath=str(output), relative_remap=True, compress=True)

bpy.ops.wm.open_mainfile(filepath=str(output), use_scripts=False)
scene = bpy.context.scene
after = snapshot()
max_drift = 0
for f in frames:
    assert before[f]["camera"] == after[f]["camera"]
    assert before[f]["front"] == after[f]["front"]
    for name in tracked:
        max_drift = max(max_drift, max(abs(a - b) for a, b in zip(
            before[f]["hardware"][name], after[f]["hardware"][name]
        )))
    scene.frame_set(f)
    actual = bpy.data.objects[tracked[0]].material_slots[0].material
    assert abs(actual.node_tree.nodes[opacity_node].inputs[0].default_value - opacities[f][0]) < 1e-6
assert max_drift < 1e-6, max_drift
reopened = bpy.data.collections[next(c.name for c in bpy.data.collections
    if c.name.startswith("ECCO_FILM v022") and c.name.endswith("v033 local display"))]
for name, master_name in mapped:
    obj = reopened.all_objects[name]
    assert Path(obj.data.library.filepath).name == master.name, (name, master_name)
    if obj.material_slots:
        assert "S04 v038 shared satin" in obj.material_slots[0].material.name
for name in ("ECCO_ROOT", "ECCO_ROTATION_X", "ECCO_SENSOR_REF_01"):
    assert Path(reopened.all_objects[name].library.filepath).name == master.name
libraries = {Path(bpy.path.abspath(lib.filepath)).name: lib.filepath for lib in bpy.data.libraries}
assert all(path.startswith("//") and Path(bpy.path.abspath(path)).is_file() for path in libraries.values())
notes.write_text(json.dumps({
    "source": source.name, "candidate": output.name, "master": master.name,
    "mesh_matches": mapped, "v003_controls_and_sensor_markers": 7,
    "verification_frames": frames, "hardware_matrix_max_difference": max_drift,
    "camera_unchanged_at_samples": True, "acquisition_front_unchanged_at_samples": True,
    "housing_fade_unchanged_at_samples": True, "relative_links": libraries,
}, indent=2) + "\n")
print("ECCO_V003_READY", len(mapped), max_drift, list(libraries), flush=True)
