"""Link the shared ECCO to approved S07 and render a benchmarked motion excerpt."""

import argparse
from array import array
from hashlib import sha256
import json
from os.path import relpath
from pathlib import Path
import sys
from time import perf_counter

import bpy


section = Path(__file__).resolve().parents[1]
production = section.parents[1]
baseline = section / "Sequence_v006/Scenes/S07_Monumental-Precision_v006.blend"
master = production / "Shared/Assets/Hardware/ECCO/ECCO_film_v003.blend"
candidate = section / "Scenes/S07_shared-product-hero_v007.blend"
evidence = section / "Notes"
benchmark_frames = (1, 38, 60, 61, 105, 120, 121, 136, 156, 164, 176, 190)
preview_frames = range(105, 177)


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def mesh_digest(mesh):
    digest = sha256()
    for elements, attr, kind, size in (
        (mesh.vertices, "co", "f", 3),
        (mesh.loops, "vertex_index", "i", 1),
        (mesh.polygons, "loop_total", "i", 1),
        (mesh.polygons, "use_smooth", "b", 1),
    ):
        values = array(kind, [0]) * (len(elements) * size)
        elements.foreach_get(attr, values)
        digest.update(values.tobytes())
    return digest.hexdigest()


def open_scene(path):
    bpy.ops.wm.open_mainfile(filepath=str(path), load_ui=False)
    scene = bpy.context.scene
    assert (scene.frame_start, scene.frame_end, scene.render.fps, scene.render.fps_base) == (1, 192, 24, 1)
    return scene


def hero_objects(scene):
    return sorted(
        (obj for obj in scene.objects if obj.type == "MESH" and obj.name.startswith(("ECCO_HOUSING", "TEMP |"))),
        key=lambda obj: obj.name,
    )


def state_samples(scene, objects):
    tracked = [*objects, *(obj for obj in scene.objects if obj.type == "LIGHT")]
    samples = []
    for frame in range(1, 193):
        scene.frame_set(frame)
        graph = bpy.context.evaluated_depsgraph_get()
        camera = scene.camera.evaluated_get(graph)
        data = camera.data
        samples.append((
            camera.name, tuple(map(tuple, camera.matrix_world)), data.lens, data.shift_x, data.shift_y,
            data.dof.focus_distance, data.dof.aperture_fstop,
            tuple((obj.name, obj.hide_render, tuple(map(tuple, obj.evaluated_get(graph).matrix_world)),
                   obj.data.energy if obj.type == "LIGHT" else None) for obj in tracked),
        ))
    return samples


def build():
    approved_sha = "62cc6fefc08b75a2506ba8c13297c1a5bcfef2a41d079dd42f1f3584edf2c548"
    assert sha256(baseline.read_bytes()).hexdigest() == approved_sha
    scene = open_scene(baseline)
    objects = hero_objects(scene)
    assert len(objects) == 10
    samples = state_samples(scene, objects)
    markers = [(marker.name, marker.frame) for marker in scene.timeline_markers]
    source_meshes = {obj.name: mesh_digest(obj.data) for obj in objects}
    mesh_names = [obj.data.name for obj in objects]
    material_names = ["ECCO shared satin | " + obj.name for obj in objects]
    with bpy.data.libraries.load(str(master), link=True) as (available, linked):
        assert set(mesh_names) <= set(available.meshes)
        assert set(material_names) <= set(available.materials)
        linked.meshes = mesh_names
        linked.materials = material_names

    for obj, mesh, material in zip(objects, linked.meshes, linked.materials, strict=True):
        assert mesh_digest(mesh) == source_meshes[obj.name], obj.name
        obj.data = mesh
        assert len(obj.material_slots) == 1, obj.name
        obj.material_slots[0].link = "OBJECT"
        obj.material_slots[0].material = material

    candidate.parent.mkdir(parents=True, exist_ok=True)
    scene.frame_set(1)
    for library in bpy.data.libraries:
        if library.parent is None:
            library.filepath = "//" + Path(relpath(master, candidate.parent)).as_posix()
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=str(candidate), relative_remap=False)
    scene = open_scene(candidate)
    objects = hero_objects(scene)
    assert {obj.name: mesh_digest(obj.data) for obj in objects} == source_meshes
    assert state_samples(scene, objects) == samples
    assert [(marker.name, marker.frame) for marker in scene.timeline_markers] == markers
    libraries = {}
    for library in bpy.data.libraries:
        resolved = Path(bpy.path.abspath(library.filepath)).resolve()
        assert library.filepath.startswith("//") and resolved.is_file(), library.filepath
        libraries[resolved.name] = {"link": library.filepath, "path": resolved.relative_to(production).as_posix(),
                                    "sha256": sha256(resolved.read_bytes()).hexdigest()}
    assert set(libraries) == {"ECCO_film_v003.blend", "Satin_finish_v001.blend"}
    for obj in objects:
        assert obj.data.library and obj.data.library.name == master.name, obj.name
        material = obj.material_slots[0].material
        assert material.library and material.library.name == master.name, obj.name
        group = next(node.node_tree for node in material.node_tree.nodes if node.type == "GROUP")
        assert group.library and group.library.name == "Satin_finish_v001.blend", obj.name
    write_json(evidence / "v007-native.json", {
        "baseline": baseline.relative_to(section).as_posix(), "baseline_sha256": approved_sha,
        "candidate": candidate.relative_to(section).as_posix(),
        "candidate_sha256": sha256(candidate.read_bytes()).hexdigest(),
        "frames": [1, 192], "fps": 24, "markers": markers,
        "camera_light_hardware_samples_matched": len(samples), "mesh_digests": source_meshes,
        "libraries": libraries,
    })


def render_preview(width, height, samples, *, scene_path=candidate, frames=preview_frames,
                   checks=benchmark_frames, version="v007"):
    scene = open_scene(scene_path)
    scene.render.resolution_x = width
    scene.render.resolution_y = height
    scene.render.resolution_percentage = 100
    scene.eevee.taa_render_samples = samples
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGB"
    scene.render.image_settings.color_depth = "8"
    cache = section / f"Cache/{version}/preview-{width}x{height}-{samples}spp"
    cache.mkdir(parents=True, exist_ok=True)
    profile = {"size": [width, height], "samples": samples, "fps": 24, "engine": scene.render.engine,
               "compositor": scene.render.use_compositing, "sequencer": scene.render.use_sequencer}

    def render(frame, name):
        scene.frame_set(frame)
        destination = cache / name
        scene.render.filepath = str(destination)
        start = perf_counter()
        bpy.ops.render.render(write_still=True)
        seconds = perf_counter() - start
        assert destination.is_file()
        print(f"S07 {name} {seconds:.3f}s", flush=True)
        return seconds

    profile["warmup_seconds"] = render(121, "warmup.png")
    profile["benchmarks_seconds"] = {frame: render(frame, f"bench-{frame:03d}.png") for frame in checks}
    write_json(cache / "timings.json", profile)
    assert max(profile["benchmarks_seconds"].values()) < 5, "Benchmark exceeded five seconds"
    timings = {}
    for frame in frames:
        seconds = render(frame, f"frame-{frame:03d}.png")
        timings[frame] = seconds
        if seconds >= 5:
            write_json(cache / "timings.json", {**profile, "preview_seconds": timings})
            raise RuntimeError(f"Preview frame {frame} exceeded five seconds")
    write_json(cache / "timings.json", {**profile, "preview_seconds": timings})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("build", "preview"))
    parser.add_argument("--width", type=int, default=960)
    parser.add_argument("--height", type=int, default=540)
    parser.add_argument("--samples", type=int, default=16)
    args = parser.parse_args(sys.argv[sys.argv.index("--") + 1:])
    if args.stage == "build":
        build()
    else:
        render_preview(args.width, args.height, args.samples)
