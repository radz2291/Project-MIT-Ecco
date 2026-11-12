"""Recover the approved S06 production starting point and benchmark its opening."""

from array import array
from hashlib import sha256
import json
import os
from pathlib import Path
import sys
from time import perf_counter

import bpy


shot = Path(__file__).resolve().parents[1]
production = shot.parents[1]
study = production / "Studies/S06_Report-Recreation_v004"
baseline = study / "Scenes/S06_cinematic-study_v004_polished.blend"
prior = production / "Records/Tasks/T-054/Consumers/S06_shared-digital_v002.blend"
assets = production / "Shared/Assets"
destination = shot / "Scenes/S06_shared-reconstruction_v005.blend"
cache = shot / "Cache/v005/preview"
bench_frames = (1, 12, 24, 40, 52, 64, 76, 88, 96)
point_names = ("A | indexed reconstruction samples", "B | amplitude samples")
surfaces = ("A | reconstructed wall beginning to open", "B | independent amplitude",
            "C | same geometry reconstruction")
rock_name = "Fixed borehole context | open viewing sector"
context_name = "S06 | physical World live context"
world_asset = assets / "Environment/Borehole/World_environment_v010.blend"
style_asset = assets / "Effects/DigitalEnvironment/Dependencies/Digital_style_v001.blend"


def mesh_hash(mesh, attributes=False):
    digest = sha256()
    fields = [(mesh.vertices, "f", 3, "co"), (mesh.loops, "i", 1, "vertex_index"),
              (mesh.polygons, "i", 1, "loop_total")]
    if attributes:
        for attribute in mesh.attributes:
            if attribute.name in {"sample_id", "illustrative_radius_m", "depth_order",
                                  "azimuth_rad", "reveal_depth", "Col"}:
                kind = attribute.data_type
                fields.append((attribute.data, "i" if kind == "INT" else "f",
                               4 if kind.endswith("COLOR") else 1,
                               "color" if kind.endswith("COLOR") else "value"))
    for values, datatype, width, name in fields:
        buffer = array(datatype, [0]) * (len(values) * width)
        values.foreach_get(name, buffer)
        digest.update(buffer.tobytes())
    return digest.hexdigest()


def open_scene(path):
    bpy.ops.wm.open_mainfile(filepath=str(path), load_ui=False)
    scene = bpy.context.scene
    assert (scene.frame_start, scene.frame_end, scene.render.fps) == (1, 288, 24)
    return scene


def states(scene):
    scene_states = []
    animated = [scene.objects[name] for name in (*surfaces, *point_names)]
    key_sets = [obj.data.shape_keys.key_blocks for obj in animated if obj.data.shape_keys]
    for frame in range(1, 289):
        scene.frame_set(frame)
        camera = scene.camera
        scene_states.append((tuple(tuple(row) for row in camera.matrix_world),
                             camera.data.lens, camera.data.shift_x, camera.data.shift_y,
                             tuple(tuple(block.value for block in keys) for keys in key_sets),
                             tuple((obj.hide_render, tuple(tuple(row) for row in obj.matrix_world))
                                   for obj in animated)))
    return scene_states


def data_hashes(scene):
    return {name: mesh_hash(scene.objects[name].data, attributes=True)
            for name in (*surfaces, *point_names)}


def relocate(path):
    for lib in list(bpy.data.libraries):
        if Path(lib.filepath).name == path.name and not Path(bpy.path.abspath(lib.filepath)).is_file():
            assert bpy.ops.wm.lib_relocate(
                library=lib.name, filepath=str(path), directory=str(path.parent), filename=path.name
            ) == {"FINISHED"}


def with_shared_satin(scene):
    hardware = [obj for obj in scene.objects if obj.type == "MESH"
                and obj.name.startswith(("ECCO_HOUSING_SOURCE_MESH", "TEMP |"))]
    assert len(hardware) == 10
    hashes = {obj.name: mesh_hash(obj.data) for obj in hardware}
    master = assets / "Hardware/ECCO/ECCO_film_v003.blend"
    with bpy.data.libraries.load(str(master), link=True) as (available, linked):
        names = [obj.data.name for obj in hardware]
        assert set(names) <= set(available.meshes)
        linked.meshes = names
    satin = master.parent / "Dependencies/Satin_finish_v001.blend"
    with bpy.data.libraries.load(str(satin), link=True) as (_, groups):
        groups.node_groups = ["ECCO | Satin finish v001"]
    satin_group = groups.node_groups[0]
    original = hardware[0].material_slots[0].material
    assert all(obj.material_slots[0].material == original for obj in hardware)
    cap_material = original.copy()
    if original.node_tree.animation_data:
        old = original.node_tree.animation_data
        new = cap_material.node_tree.animation_data_create()
        new.action, new.action_slot = old.action, old.action_slot
    for material, dark, name in ((original, 0.0, "S06 shared satin | housing and closures"),
                                 (cap_material, 1.0, "S06 shared satin | imaging caps")):
        material.name = name
        tree = material.node_tree
        bsdf = next(node for node in tree.nodes if node.type == "BSDF_PRINCIPLED")
        group = tree.nodes.new("ShaderNodeGroup")
        group.node_tree = satin_group
        group.label = "Shared satin, local animated visibility"
        group.location = (bsdf.location.x - 275, bsdf.location.y + 200)
        group.inputs["Sensor face"].default_value = dark
        for channel in ("Base Color", "Roughness", "Metallic"):
            tree.links.new(group.outputs[channel], bsdf.inputs[channel])
    for obj, mesh in zip(hardware, linked.meshes):
        assert mesh_hash(mesh) == hashes[obj.name], obj.name
        obj.data = mesh
        slot = obj.material_slots[0]
        slot.link = "OBJECT"
        slot.material = cap_material if "Imaging port" in obj.name else original
    return hashes


def with_shared_fine_contours(scene):
    library = assets / "Effects/MeasurementReveal/Measurement_reveal_v001.blend"
    with bpy.data.libraries.load(str(library), link=True) as (_, linked):
        linked.node_groups = ["ECCO Fine Surface Style v001"]
    style = linked.node_groups[0]
    guides = [obj for obj in scene.objects if obj.type == "CURVE" and
              obj.name.startswith(("A depth contour", "A length contour"))]
    wrappers = {}
    for obj in guides:
        width, material = obj.data.bevel_depth, obj.data.materials[0]
        key = (width, material)
        if key not in wrappers:
            tree = bpy.data.node_groups.new(f"S06 animated fine contour | {width * 1000:.2f} mm",
                                           "GeometryNodeTree")
            wrappers[key] = tree
            for direction in ("INPUT", "OUTPUT"):
                tree.interface.new_socket(name="Geometry", in_out=direction, socket_type="NodeSocketGeometry")
            source, target = tree.nodes.new("NodeGroupInput"), tree.nodes.new("NodeGroupOutput")
            wire = tree.nodes.new("GeometryNodeCurveToMesh")
            shared = tree.nodes.new("GeometryNodeGroup")
            shared.node_tree = style
            shared.inputs["Point radius"].default_value = 0.0
            shared.inputs["Line radius"].default_value = width
            finish = tree.nodes.new("GeometryNodeSetMaterial")
            finish.inputs["Material"].default_value = material
            for index, node in enumerate((source, wire, shared, finish, target)):
                node.location = (index * 205, 0)
            tree.links.new(source.outputs["Geometry"], wire.inputs["Curve"])
            tree.links.new(wire.outputs["Mesh"], shared.inputs["Geometry"])
            tree.links.new(shared.outputs["Geometry"], finish.inputs["Geometry"])
            tree.links.new(finish.outputs["Geometry"], target.inputs["Geometry"])
        modifier = obj.modifiers.new("Shared fine contours, local paths and fade", "NODES")
        modifier.node_group = wrappers[key]
    return [obj.name for obj in guides]


if not destination.exists():
    original = open_scene(baseline)
    original_states = states(original)
    original_hashes = data_hashes(original)
    text_inventory = {o.name: o.data.body for o in original.objects if o.type == "FONT"}
    scene = open_scene(prior)
    for asset in (style_asset, style_asset.with_name("Digital_world_v001.blend"), world_asset):
        relocate(asset)
    hardware = with_shared_satin(scene)
    guides = with_shared_fine_contours(scene)
    for lib in bpy.data.libraries:
        if lib.parent is None:
            path = Path(bpy.path.abspath(lib.filepath)).resolve()
            assert path.is_file(), path
            lib.filepath = "//" + Path(os.path.relpath(path, destination.parent)).as_posix()
    scene["dataset"] = "//" + Path(os.path.relpath(study / "Data/story_field.npz", destination.parent)).as_posix()
    scene.frame_set(1)
    scene.render.filepath = "//../Cache/v005/preview/S06_"
    bpy.ops.wm.save_as_mainfile(filepath=str(destination), relative_remap=False)
    scene = open_scene(destination)
    assert states(scene) == original_states
    assert data_hashes(scene) == original_hashes
    assert {o.name: o.data.body for o in scene.objects if o.type == "FONT"} == text_inventory
    for name, checksum in hardware.items():
        obj = scene.objects[name]
        assert mesh_hash(obj.data) == checksum and obj.data.library, name
    context = scene.objects[context_name]
    checks = {}
    for frame in (1, 52, 96, 106, 124, 144, 220, 250, 288):
        scene.frame_set(frame)
        depsgraph = bpy.context.evaluated_depsgraph_get()
        faces = len(context.evaluated_get(depsgraph).data.polygons)
        assert faces and not scene.objects[rock_name].evaluated_get(depsgraph).data.polygons
        checks[str(frame)] = {"world_faces": faces, "world_hidden": context.hide_render}
    assert not checks["52"]["world_hidden"] and checks["250"]["world_hidden"]
    scene.frame_set(76)
    for name in guides:
        evaluated = scene.objects[name].evaluated_get(bpy.context.evaluated_depsgraph_get())
        mesh = evaluated.to_mesh()
        assert mesh and len(mesh.polygons), name
        evaluated.to_mesh_clear()
    (shot / "Notes/v005-integration.json").write_text(json.dumps({
        "baseline": str(baseline.relative_to(production)),
        "shared_context_source": str(prior.relative_to(production)),
        "source_sha256": sha256(baseline.read_bytes()).hexdigest(),
        "native_sha256": sha256(destination.read_bytes()).hexdigest(),
        "matching_camera_and_data_states": len(original_states),
        "data_hashes": original_hashes,
        "matching_hardware_meshes": hardware,
        "matched_text_objects": len(text_inventory),
        "linked_fine_contours": len(guides),
        "context_states": checks,
    }, indent=2) + "\n", encoding="utf-8")
else:
    scene = open_scene(destination)

libraries = {lib.name: lib.filepath for lib in bpy.data.libraries}
assert all(path.startswith("//") and Path(bpy.path.abspath(path)).is_file()
           for path in libraries.values()), libraries
assert all((assets_name in str(libraries)) for assets_name in (
    "ECCO_film_v003", "Satin_finish_v001", "World_environment_v010",
    "Digital_style_v001", "Measurement_reveal_v001")), libraries
assert Path(bpy.path.abspath(scene["dataset"])).is_file()
assert (cache.parent / "preview").is_dir()

sample_count = int(sys.argv[sys.argv.index("--") + 1]) if "--" in sys.argv else 8
scene.render.resolution_x, scene.render.resolution_y = 960, 540
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
settings = {"resolution": [960, 540], "samples": sample_count, "backend": "Vulkan",
            "compositing": scene.render.use_compositing, "fps": 24}
timings = cache / "timings.json"
state = json.loads(timings.read_text(encoding="utf-8")) if timings.exists() else {
    "settings": settings, "setup": [], "benchmark": {}, "frames": {}, "over_cap_attempts": [],
    "relative_libraries": libraries,
}
assert state["settings"] == settings


def save():
    temp = timings.with_suffix(".tmp")
    temp.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    temp.replace(timings)


def frame_render(frame, path):
    scene.frame_set(frame)
    scene.eevee.taa_render_samples = sample_count
    scene.render.filepath = str(path)
    started = perf_counter()
    bpy.ops.render.render(write_still=True)
    return perf_counter() - started


setup = {}
for frame in (1, 52, 96):
    scene.frame_set(frame)
    scene.eevee.taa_render_samples = sample_count
    started = perf_counter()
    bpy.ops.render.render()
    setup[str(frame)] = perf_counter() - started
state["setup"].append(setup)
save()
if not state["benchmark"]:
    benchmark = {}
    for frame in bench_frames:
        for attempt in range(2):
            elapsed = frame_render(frame, cache / "bench.png")
            if elapsed < 5:
                break
            state["over_cap_attempts"].append({"benchmark_frame": frame, "seconds": elapsed})
            save()
        print("BENCH", frame, round(elapsed, 3), flush=True)
        assert elapsed < 5, ("Benchmark over cap", frame, elapsed)
        benchmark[str(frame)] = elapsed
    state["benchmark"] = benchmark
    save()
assert len(state["benchmark"]) == len(bench_frames) and max(state["benchmark"].values()) < 5
for frame in range(1, 97):
    key = str(frame)
    image = cache / f"S06_{frame:04d}.png"
    if key in state["frames"] and image.is_file() and image.stat().st_size:
        continue
    pending = cache / "pending.png"
    for attempt in range(2):
        elapsed = frame_render(frame, pending)
        if elapsed < 5:
            break
        state["over_cap_attempts"].append({"frame": frame, "seconds": elapsed})
        save()
    assert elapsed < 5, ("Preview over cap", frame, elapsed)
    pending.replace(image)
    state["frames"][key] = elapsed
    save()
    if frame == 1 or frame % 24 == 0:
        print("FRAME", frame, round(elapsed, 3), flush=True)
print("COMPLETE", len(state["frames"]), round(max(state["frames"].values()), 3), flush=True)
