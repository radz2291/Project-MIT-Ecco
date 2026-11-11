"""Fit shared BHA v008 and try the prepared cement and formation finishes in S04."""
from array import array
from hashlib import sha256
import json
from pathlib import Path
import sys

import bpy

master, output, evidence = [Path(x).resolve() for x in sys.argv[sys.argv.index("--") + 1:]]
source = Path(bpy.data.filepath)
assert source.name == "S04_continuous-shared-ecco_v038.blend"
scene = bpy.context.scene
bha = scene.objects["WORLD_HARDWARE_INSTANCE"]
extensions = {"WORLD_UPHOLE_JOINT": scene.objects["WORLD_UPHOLE_JOINT_INSTANCE"],
              "WORLD_UPHOLE_EXTENSION": scene.objects["WORLD_UPHOLE_EXTENSION_INSTANCE"]}
tracked = {"ECCO_SENSOR_REF_01", "TEMP | Imaging port 1 | removable acoustic cap",
           "UPHOLE_COLLAR", "DOWNHOLE_COLLAR", "PDC_WEB_AND_SHANK",
           "UPHOLE_UNIT_COLLAR_EXTENSION", "UPHOLE_SIMPLIFIED_CONNECTION"}
frames = (1, 31, 63, 85, 190, 261, 300, 336, 370, 432)
body_gate = "v033 source surface opacity"


def expand(collection):
    found = {}
    pending = [collection]
    visited = set()
    while pending:
        current = pending.pop()
        if current in visited:
            continue
        visited.add(current)
        pending.extend(current.children)
        for obj in current.objects:
            found[obj.name] = obj
            if obj.instance_collection:
                pending.append(obj.instance_collection)
    return found


def fingerprint(mesh):
    coords = array("f", [0]) * (len(mesh.vertices) * 3)
    indices = array("i", [0]) * len(mesh.loops)
    slots = array("i", [0]) * len(mesh.polygons)
    mesh.vertices.foreach_get("co", coords)
    mesh.loops.foreach_get("vertex_index", indices)
    mesh.polygons.foreach_get("material_index", slots)
    return sha256(coords.tobytes() + indices.tobytes() + slots.tobytes()).hexdigest()


def flat(matrix):
    return tuple(value for row in matrix for value in row)


def poses():
    result = {}
    for frame in frames:
        scene.frame_set(frame)
        items = [(i.object.name, flat(i.matrix_world)) for i in
                 bpy.context.evaluated_depsgraph_get().object_instances if i.object.name in tracked]
        assert len(items) == len({key for key, _ in items}), (frame, items)
        result[frame] = {
            "objects": dict(items),
            "camera": flat(scene.camera.matrix_world) + (scene.camera.data.lens,),
            "acquisition_front": scene.objects["STEEL - capped true source section"].data.materials[0]
            .node_tree.nodes["ECCO axial acquisition front"].outputs[0].default_value,
        }
    return result


def transfer_action(old_tree, tree):
    old = old_tree.animation_data
    new = tree.animation_data_create()
    new.action = old.action
    new.action_slot = old.action_slot


def wrap(stock, suffix):
    material = stock.copy()
    material.name = stock.name + suffix
    material.surface_render_method = "BLENDED"
    material.use_transparency_overlap = False
    tree = material.node_tree
    surface = next(n for n in tree.nodes if n.type == "OUTPUT_MATERIAL").inputs["Surface"]
    shader = surface.links[0].from_socket
    mix = tree.nodes.new("ShaderNodeMixShader")
    trans = tree.nodes.new("ShaderNodeBsdfTransparent")
    tree.links.new(trans.outputs[0], mix.inputs[1])
    tree.links.new(shader, mix.inputs[2])
    tree.links.new(mix.outputs[0], surface)
    return material, mix


before = poses()
old = expand(bha.instance_collection)
with bpy.data.libraries.load(str(master), link=True) as (_, linked):
    linked.collections = ["WORLD_HARDWARE", *extensions]
assembly, *continuation = linked.collections
shared = expand(assembly)
finishes = {}
mapped = []
for name, obj in old.items():
    if obj.type != "MESH" or obj.data.library:
        continue
    ref = shared[name]
    assert fingerprint(obj.data) == fingerprint(ref.data), name
    assert max(abs(x - y) for x, y in zip(flat(obj.matrix_basis), flat(ref.matrix_basis))) < 1e-6
    previous = tuple(slot.material for slot in obj.material_slots)
    stock = tuple(slot.material for slot in ref.material_slots)
    assert len(previous) == len(stock)
    obj.data = ref.data
    for slot, original, finish in zip(obj.material_slots, previous, stock):
        key = (original, finish)
        if key not in finishes:
            material, mix = wrap(finish, " | S04 BHA v008")
            mix.name = body_gate
            transfer_action(original.node_tree, material.node_tree)
            finishes[key] = material
        slot.link = "OBJECT"
        slot.material = finishes[key]
    mapped.append(name)
assert len(mapped) == 126

for instance, collection in zip(extensions.values(), continuation):
    old_meshes = {n: fingerprint(o.data) for n, o in expand(instance.instance_collection).items()
                  if o.type == "MESH"}
    new_meshes = {n: fingerprint(o.data) for n, o in expand(collection).items()
                  if o.type == "MESH"}
    assert old_meshes == new_meshes
    instance.instance_collection = collection

# Apply the prepared finishes to the same shot meshes. Keep their stage-D fade.
env_sources = {
    "cement": scene.objects["CASED_CEMENT_UPHOLE_FULL local window"].data.materials[0],
    "formation": scene.objects["Formation facing inspection window"].data.materials[0],
}
cement_names = ("Cement either side of organic gap A", "Cement either side of organic gap B",
                "Cement uphole continuation", "Cement downhole supported interval")
ground_name = "FORMATION - closed source-guided continuation to frame edge"
env_targets = {"cement": cement_names, "formation": (ground_name,)}
env_material_names = {}
for kind, objects in env_targets.items():
    original = scene.objects[objects[0]].data.materials[0]
    previous = original.node_tree
    old_fade = next(n for n in previous.nodes if n.type == "VALUE")
    material, mix = wrap(env_sources[kind], " | S04 shared " + kind)
    tree = material.node_tree
    fade = tree.nodes.new("ShaderNodeValue")
    fade.name = old_fade.name
    fade.outputs[0].default_value = old_fade.outputs[0].default_value
    alpha = tree.nodes.new("ShaderNodeObjectInfo")
    multiply = tree.nodes.new("ShaderNodeMath")
    multiply.operation = "MULTIPLY"
    tree.links.new(fade.outputs[0], multiply.inputs[0])
    tree.links.new(alpha.outputs["Alpha"], multiply.inputs[1])
    tree.links.new(multiply.outputs[0], mix.inputs[0])
    transfer_action(previous, tree)
    for name in objects:
        obj = scene.objects[name]
        for slot in obj.material_slots:
            slot.link = "OBJECT"
            slot.material = material
    env_material_names[kind] = material.name

for lib in bpy.data.libraries:
    if not lib.filepath.startswith("//"):
        lib.filepath = bpy.path.relpath(lib.filepath)
scene.frame_set(85)
bpy.context.preferences.filepaths.save_version = 0
bpy.ops.wm.save_as_mainfile(filepath=str(output), relative_remap=True, compress=True)
bpy.ops.wm.open_mainfile(filepath=str(output), use_scripts=False)
scene = bpy.context.scene
after = poses()
max_delta = 0
for frame in frames:
    a, b = before[frame], after[frame]
    assert a["camera"] == b["camera"]
    assert a["acquisition_front"] == b["acquisition_front"]
    assert a["objects"].keys() == b["objects"].keys(), frame
    max_delta = max([max_delta] + [abs(x-y) for name in a["objects"] for x,y in
                                  zip(a["objects"][name], b["objects"][name])])
assert max_delta < 1e-6, max_delta
reopened = expand(scene.objects["WORLD_HARDWARE_INSTANCE"].instance_collection)
for name in mapped:
    assert Path(reopened[name].data.library.filepath).name == "BHA_core_satin_v001.blend"
assert Path(reopened["ECCO_SENSOR_REF_01"].library.filepath).name == "ECCO_film_v003.blend"
for name in extensions:
    assert Path(scene.objects[name + "_INSTANCE"].instance_collection.library.filepath).name == master.name
missing = [item.name for prop in bpy.data.bl_rna.properties if prop.type == "COLLECTION"
           for item in getattr(bpy.data, prop.identifier) if getattr(item, "is_missing", False)]
assert not missing, missing
libraries = [lib.filepath for lib in bpy.data.libraries]
assert all(path.startswith("//") and Path(bpy.path.abspath(path)).is_file() for path in libraries)
evidence.write_text(json.dumps({
    "source": source.name, "candidate": output.name, "assembly": master.name,
    "exact_core_mesh_matches": len(mapped), "exact_continuation_mesh_matches": 2,
    "checked_frames": frames, "max_world_matrix_difference": max_delta,
    "camera_and_acquisition_front_match_at_samples": True,
    "cement": "CasedHole_v002 / CASED_CEMENT",
    "formation": "Formation_cased-section_v002 / FORMATION_CasedSection_v005",
    "environment_application": "Prepared shared finishes with existing local cutaway geometry and fade",
    "relative_libraries": libraries,
}, indent=2) + "\n")
print("BHA_AND_GROUND_READY", len(mapped), max_delta, len(libraries), flush=True)
