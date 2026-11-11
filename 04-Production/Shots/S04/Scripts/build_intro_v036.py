"""Build the v005 entry and one approved shared exchange as a separate S04 preview."""
import json
from pathlib import Path
import sys

import bpy
from mathutils import Quaternion, Vector
from mathutils.bvhtree import BVHTree
from bpy_extras.object_utils import world_to_camera_view

stage, mapping_path, production, output = (
    Path(arg).resolve() for arg in sys.argv[sys.argv.index("--") + 1:]
)
shared = production / "Shared/Assets"
wave = shared / "Effects/Waveform"
sys.path.insert(0, str(wave / "Scripts"))
from approved_exchange_api import apply_approved_preset, create_contact_patch
from pulse_asset_api import duplicate_instance, set_input

bpy.ops.wm.open_mainfile(filepath=str(stage), use_scripts=False)
scene = bpy.context.scene
expected_paths = {
    Path(key).name: Path(value).resolve(strict=True)
    for key, value in json.loads(mapping_path.read_text(encoding="utf-8-sig")).items()
}
for library in bpy.data.libraries:
    library.filepath = bpy.path.relpath(str(expected_paths[Path(library.filepath).name]))

start = 97
end = 153
assembly = scene.objects["WORLD_HARDWARE_INSTANCE"]
camera = scene.camera
steel = scene.objects["Steel - unchanged source with viewing window"]


def instance_pose(token):
    matches = [(item.object.original, item.matrix_world.copy())
               for item in bpy.context.evaluated_depsgraph_get().object_instances
               if item.object.name.startswith(token)]
    assert len(matches) == 1, (token, len(matches))
    return matches[0]


sensor_id = "ECCO_SENSOR_REF_01"
pose_frames = (1, 49, 73, start)
original = {}
for frame in pose_frames:
    scene.frame_set(frame)
    original[frame] = instance_pose(sensor_id)[1]
with bpy.data.libraries.load(str(shared / "Hardware/BHA/BHA_film_v008.blend"), link=True) as (_, loaded):
    loaded.collections = ["WORLD_HARDWARE"]
assembly.instance_collection = loaded.collections[0]
for frame, old in original.items():
    scene.frame_set(frame)
    new = instance_pose(sensor_id)[1]
    assert max(abs(a - b) for row1, row2 in zip(old, new)
               for a, b in zip(row1, row2)) < 1e-6

# Keep v005 entry travel, then hold through the longer approved exchange.
world = scene.objects["WORLD_CONTROL"]
scene.frame_set(start)
held_travel = world["travel_m"]
for frame in range(start, end + 1):
    world["travel_m"] = held_travel
    world.keyframe_insert(data_path='["travel_m"]', frame=frame)
for obj in scene.objects:
    if obj.name.startswith(("s04-v005-", "ACOUSTICS_CONTROL_s04-v005-")) or any(
        collection.name == "S04 qualitative response comparison" for collection in obj.users_collection
    ):
        obj.animation_data_clear()
        obj.hide_render = obj.hide_viewport = True

scene.frame_set(start)
_, sensor = instance_pose(sensor_id)
cap, cap_matrix = instance_pose("TEMP | Imaging port 1")
axis = (sensor.to_3x3() @ Vector((0, 0, 1))).normalized()
reference = sensor.translation.copy()
cap_tree = BVHTree.FromPolygons(
    [cap_matrix @ vert.co for vert in cap.data.vertices],
    [tuple(poly.vertices) for poly in cap.data.polygons],
)
source, _, cap_face, _ = cap_tree.ray_cast(reference + axis * 0.025, -axis, 0.05)
assert source is not None, "No exit point on shared ECCO cap"
wall_tree = BVHTree.FromPolygons(
    [steel.matrix_world @ vert.co for vert in steel.data.vertices],
    [tuple(poly.vertices) for poly in steel.data.polygons],
)


def steel_hit(origin, direction):
    point, _, face, _ = wall_tree.ray_cast(origin, direction, 0.06)
    assert point is not None
    return point, face


target, face = steel_hit(source, axis)
gap = (target - source).length
assert 0.02 < gap < 0.04
side = Vector((1, 0, 0))
up = axis.cross(side).normalized()
collection = bpy.data.collections.new("S04 first supported response")
scene.collection.children.link(collection)
with bpy.data.libraries.load(str(wave / "Waveform_shared_v021.blend"), link=True) as (_, loaded):
    loaded.objects = ["WF_MASTER_CONTROLS", "WF_PULSE_FIELD"]
controller, template = loaded.objects
scene.collection.objects.link(controller)
signal = duplicate_instance(template, collection, "S04 shared v021 first exchange")
signal.location = source
modifier = signal.modifiers[0]
marks = apply_approved_preset(modifier, start)
set_input(modifier, "Radius multiplier", 1.35)
for key, value in {
    "Gap length m": gap, "Route axis": tuple(axis), "Transverse axis": tuple(side),
    "Up axis": tuple(up),
}.items():
    set_input(modifier, key, value)

preset = json.loads((wave / "Approved_beam_exchange_v001.json").read_text())
patch = create_contact_patch(collection, target, axis, start_frame=start)
patch_material = patch.data.materials[0]
patch_material.use_nodes = True
shader = patch_material.node_tree.nodes.get("Principled BSDF")
color = preset["contact_patch"]["color"]
shader.inputs["Base Color"].default_value = color
shader.inputs["Emission Color"].default_value = color
shader.inputs["Emission Strength"].default_value = 0.75

# Fit the approved 4-by-4 response to the actual curved wall. These faces are graphics.
profiles = preset["surface"]["color_profiles"]
grid, faces = [], []
pitch = 0.0033
for row in range(4):
    for column in range(4):
        for cx, cy in ((-0.47, -0.47), (0.47, -0.47), (0.47, 0.47), (-0.47, 0.47)):
            probe = source + (column - 1.5 + cx) * pitch * side + (row - 1.5 + cy) * pitch * up
            surface, _ = steel_hit(probe, axis)
            grid.append(surface - 0.00012 * axis)
        j = len(grid)
        faces.append((j - 4, j - 3, j - 2, j - 1))
mesh = bpy.data.meshes.new("Response samples on the casing")
mesh.from_pydata(grid, [], faces)
tiles = bpy.data.objects.new("First supported response tiles", mesh)
collection.objects.link(tiles)
for group in range(4):
    material = bpy.data.materials.new(f"Approved response color group {group + 1}")
    material.use_nodes = True
    material.surface_render_method = "BLENDED"
    nodes = material.node_tree.nodes
    emission = nodes.new("ShaderNodeEmission")
    mix = nodes.new("ShaderNodeMixShader")
    links = material.node_tree.links
    links.new(nodes.new("ShaderNodeBsdfTransparent").outputs[0], mix.inputs[1])
    links.new(emission.outputs[0], mix.inputs[2])
    links.new(mix.outputs[0], nodes.get("Material Output").inputs["Surface"])
    mesh.materials.append(material)
    for key in profiles[str(group)]:
        frame = start + key["frame"]
        emission.inputs["Color"].default_value = (*key["color"][:3], 1.0)
        emission.inputs["Color"].keyframe_insert(data_path="default_value", frame=frame)
        mix.inputs[0].default_value = key["color"][3]
        mix.inputs[0].keyframe_insert(data_path="default_value", frame=frame)
ordered = sorted(mesh.polygons, key=lambda poly: (poly.center - target).length)
for index, poly in enumerate(ordered):
    poly.material_index = index // 4

# Keep the v005 opening. Ease to an oblique view of both ends of the short signal.
eye = Vector((-0.51, 0.055, 0.39))
look = source.lerp(target, 0.45)
angle = (look - eye).to_track_quat("-Z", "Y") @ Quaternion((0, 0, 1), -0.15707963)
for frame in range(62, end + 1):
    scene.frame_set(frame)
    u = min(1, (frame - 62) / (start - 62))
    u = u**3 * (10 + u * (-15 + 6 * u))
    camera.location = camera.location.lerp(eye, u)
    camera.rotation_quaternion = camera.rotation_quaternion.slerp(angle, u)
    camera.data.lens = 35 + 20 * u
    camera.keyframe_insert("location", frame=frame)
    camera.keyframe_insert("rotation_quaternion", frame=frame)
    camera.data.keyframe_insert("lens", frame=frame)

# Reveal enough of the steel at the strike angle while keeping the cap visible.
window = bpy.data.materials["S04 satin steel - inspection mask"].node_tree
lower = next(n for n in window.nodes if n.type == "MAP_RANGE"
             and abs(n.inputs["From Min"].default_value + 1.435) < 0.002)
for key, opening, close in (("From Min", -1.435, .653), ("From Max", -1.365, .672)):
    socket = lower.inputs[key]
    socket.default_value = opening
    socket.keyframe_insert("default_value", frame=72)
    socket.default_value = close
    socket.keyframe_insert("default_value", frame=start)

# The oblique view crosses the boundary between the two ground halves.
rear_ground = scene.objects["Formation retained rear ground"]
for slot in rear_ground.material_slots:
    slot.link = "OBJECT"
    slot.material = bpy.data.materials["S04 ground viewing access"]

# Open the existing inspection masks toward the oblique camera, leaving the strike on steel.
scene.frame_set(start)
for name, upper_min in (
    ("S04 satin steel - inspection mask", 1.095),
    ("S04 matte cement", 1.095),
    ("S04 ground viewing access", 1.445),
):
    tree = bpy.data.materials[name].node_tree
    node = next(n for n in tree.nodes if n.type == "MAP_RANGE"
                and abs(n.inputs["From Min"].default_value - upper_min) < 0.003)
    for frame in range(62, end + 1):
        u = min(1, (frame - 62) / (start - 62))
        u = u**3 * (10 + u * (-15 + 6 * u))
        for key, offset in (("From Min", 0.0), ("From Max", 0.07)):
            socket = node.inputs[key]
            base = upper_min if name == "S04 ground viewing access" else (
                0.195 + 0.9 * min(1.0, max(0.0, (frame - 34.6) / 24.0))
            )
            socket.default_value = base * (1 - u) + 1.92 * u + offset
            socket.keyframe_insert("default_value", frame=frame)

for library in bpy.data.libraries:
    if not library.filepath.startswith("//"):
        library.filepath = bpy.path.relpath(library.filepath)

scene.name = "S04 v036 – tool entry and first supported exchange"
scene.frame_end = end
scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.render.resolution_percentage = 100
scene.eevee.taa_render_samples = 8
scene.render.filepath = "//../Cache/v036/frame_"
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGB"
scene.render.image_settings.compression = 10
scene.frame_set(start)
pixel_span = (world_to_camera_view(scene, camera, source) - world_to_camera_view(scene, camera, target))
for frame in (start, int(marks["feedback_complete"]), end):
    scene.frame_set(frame)
    assert (instance_pose(sensor_id)[1].translation - reference).length < 1e-6
scene.frame_set(1)
bpy.context.preferences.filepaths.save_version = 0
bpy.ops.wm.save_as_mainfile(filepath=str(output), relative_remap=True, compress=True)
evidence = {
    "source": list(source), "cap_face": cap_face, "target": list(target), "steel_face": face,
    "gap_mm": 1000 * gap, "landmarks": marks, "frame_end": end,
    "preview_span_px_xy": [960 * pixel_span.x, 540 * pixel_span.y],
    "unchanged_v005_sensor_poses": pose_frames,
    "hardware": "BHA_film_v008 / ECCO_film_v003", "waveform": "Waveform_shared_v021",
}
notes = output.parent.parent / "Notes"
notes.mkdir(exist_ok=True)
(notes / "v036-intro-placement.json").write_text(json.dumps(evidence, indent=2) + "\n")
print("INTRO_BUILT", evidence, flush=True)
