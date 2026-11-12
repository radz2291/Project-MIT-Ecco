"""Replace only the two S04 wave packets with the linked S02 waveform."""
from hashlib import sha256
import json
from pathlib import Path
import sys

import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree

wave_dir, output, record = [Path(x).resolve() for x in sys.argv[sys.argv.index("--") + 1:]]
source_file = Path(bpy.data.filepath)
assert source_file.name == "S04_continuous-shared-bha-environment_v039.blend"
scene = bpy.context.scene
master = wave_dir / "Waveform_shared_v021.blend"
sys.path.insert(0, str(wave_dir / "Scripts"))
from approved_exchange_api import apply_approved_preset
from pulse_asset_api import arrival_readouts, duplicate_instance, set_input

previous_prefixes = ("S02 sourced SEND front ", "S02 sourced ECHO front ")
impact_prefixes = ("STEEL-ATTACHED resonance band", "STEEL THICKNESS response",
                   "STEEL-BOUND acquisition segment", "Casing response tail")
samples = (1, 63, 73, 81, 82, 85, 91, 100, 141, 175, 185, 193, 194,
           198, 206, 229, 235, 261, 300, 336, 370, 432)


def instance(name):
    matches = [(item.object.original, item.matrix_world.copy())
               for item in bpy.context.evaluated_depsgraph_get().object_instances
               if item.object.name == name]
    assert len(matches) == 1, (name, len(matches))
    return matches[0]


def snapshot():
    result = {}
    impacts = sorted((obj for obj in scene.objects if obj.name.startswith(impact_prefixes)),
                     key=lambda item: item.name)
    assert len(impacts) == 293
    for frame in samples:
        scene.frame_set(frame)
        state = [(obj.name, obj.hide_render, obj.hide_viewport, tuple(obj.location),
                  tuple(obj.scale), tuple(tuple(m.diffuse_color) for m in obj.data.materials if m))
                 for obj in impacts]
        result[frame] = {
            "impact_digest": sha256(repr(state).encode()).hexdigest(),
            "camera": tuple(tuple(row) for row in scene.camera.matrix_world),
            "lens": scene.camera.data.lens,
            "sensor": tuple(tuple(row) for row in instance("ECCO_SENSOR_REF_01")[1]),
        }
    return result


def first_visible(prefix, low, high):
    group = [obj for obj in scene.objects if obj.name.startswith(prefix)]
    for frame in range(low, high + 1):
        scene.frame_set(frame)
        if any(not obj.hide_render for obj in group):
            return frame
    raise RuntimeError(prefix)


def ray_surface(obj, matrix):
    return BVHTree.FromPolygons(
        [matrix @ vertex.co for vertex in obj.data.vertices],
        [tuple(face.vertices) for face in obj.data.polygons],
    )


before = snapshot()
events = []
for label, low, high in (("Supported", 63, 140), ("Reduced support", 175, 261)):
    launch = first_visible(previous_prefixes[0], low, high)
    impact = first_visible(impact_prefixes[0], low, high)
    events.append((label, launch, impact, high))
assert [(launch, hit) for _, launch, hit, _ in events] == [(73, 82), (185, 194)]

with bpy.data.libraries.load(str(master), link=True) as (_, loaded):
    loaded.objects = ["WF_MASTER_CONTROLS", "WF_PULSE_FIELD"]
controller, template = loaded.objects
collection = bpy.data.collections.new("S04 | shared v021 waveforms")
scene.collection.children.link(collection)
collection.objects.link(controller)
steel = scene.objects["STEEL - capped true source section"]
wall = ray_surface(steel, steel.matrix_world)
data = []
for label, launch, impact, hold_end in events:
    scene.frame_set(launch)
    _, sensor = instance("ECCO_SENSOR_REF_01")
    cap, cap_pose = instance("TEMP | Imaging port 1 | removable acoustic cap")
    axis = (sensor.to_3x3() @ Vector((0, 0, 1))).normalized()
    centre = sensor.translation.copy()
    cap_tree = ray_surface(cap, cap_pose)
    origin, _, cap_face, _ = cap_tree.ray_cast(centre + axis * 0.025, -axis, 0.05)
    assert origin is not None and Path(cap.data.library.filepath).name == "ECCO_film_v003.blend"
    hit, _, wall_face, _ = wall.ray_cast(origin, axis, 0.075)
    assert hit is not None
    gap = (hit - origin).length
    assert 0.02 < gap < 0.04
    side = axis.cross(Vector((0, 0, 1))).normalized()
    up = side.cross(axis).normalized()

    field = duplicate_instance(template, collection, label + " | shared v021 waveform")
    field.location = origin
    modifier = field.modifiers[0]
    # The approved packet opens over five frames, launches at +6, then travels
    # twelve frames. Scale its clock so the head meets the original glitch.
    speed = 12 / (impact - launch)
    start = launch - 6 / speed
    marks = apply_approved_preset(modifier, start)
    for key, value in {
        "Gap length m": gap, "Route axis": tuple(axis), "Transverse axis": tuple(side),
        "Up axis": tuple(up), "Speed": speed,
    }.items():
        set_input(modifier, key, value)
    marks = {key: start + (frame - start) / speed for key, frame in marks.items()}
    assert marks["feedback_complete"] < hold_end
    scene.frame_set(int(marks["feedback_complete"]))
    assert (instance("ECCO_SENSOR_REF_01")[1].translation - centre).length < 1e-6
    scene.frame_set(impact)
    readouts = arrival_readouts(field, scene)
    assert readouts
    data.append({
        "case": label, "start": start, "speed": speed, "launch": launch, "glitch": impact,
        "cap_face": cap_face, "steel_face": wall_face, "gap_mm": gap * 1000,
        "source_m": list(origin), "target_m": list(hit), "preset_landmarks": marks,
        "native_readouts_at_glitch": readouts,
    })

old = [obj for obj in scene.objects if obj.name.startswith(previous_prefixes)]
assert len(old) == 12
for obj in old:
    obj.animation_data_clear()
    obj.hide_render = obj.hide_viewport = True
for lib in bpy.data.libraries:
    if not lib.filepath.startswith("//"):
        lib.filepath = bpy.path.relpath(lib.filepath)
scene.render.filepath = "//../Cache/v040/Frames/S04_"
scene.frame_set(82)
bpy.context.preferences.filepaths.save_version = 0
bpy.ops.wm.save_as_mainfile(filepath=str(output), relative_remap=True, compress=True)
bpy.ops.wm.open_mainfile(filepath=str(output), use_scripts=False)
scene = bpy.context.scene
assert before == snapshot()
assert all(obj.hide_render for obj in scene.objects if obj.name.startswith(previous_prefixes))
libs = [lib.filepath for lib in bpy.data.libraries]
assert all(path.startswith("//") and Path(bpy.path.abspath(path)).is_file() for path in libs)
assert any(Path(path).name == master.name for path in libs)
record.write_text(json.dumps({
    "source": source_file.name, "scene": output.name, "waveform": master.name,
    "events": data, "legacy_wavefronts_hidden": len(old), "impact_objects_retained": 293,
    "impact_camera_and_sensor_match": True, "verification_frames": samples, "relative_links": libs,
}, indent=2) + "\n")
print("S04_WAVEFORM_READY", json.dumps(data), flush=True)
