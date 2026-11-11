"""Fit only the v005 opening camera travel to the approved S04 previs."""
import json
from pathlib import Path
import sys

import bpy
from mathutils import Vector

score, output, evidence = [Path(value).resolve() for value in sys.argv[sys.argv.index("--") + 1:]]
source = Path(bpy.data.filepath)
assert source.name == "S04_continuous_relinked_v035.blend"
scene = bpy.context.scene
camera = scene.camera
join = 63


def camera_state():
    m = camera.matrix_world
    return tuple(value for row in m for value in row) + (
        camera.data.lens, camera.data.shift_x, camera.data.shift_y,
    )


def protected_camera():
    result = []
    for frame in range(join, 433):
        scene.frame_set(frame)
        result.append(camera_state())
        if frame < 432:
            scene.frame_set(frame, subframe=0.5)
            result.append(camera_state())
    return result


protected = protected_camera()
scene.frame_set(join)
anchor = camera.matrix_world.translation.copy()
anchor_rotation = camera.matrix_world.to_quaternion()
forward = anchor_rotation @ Vector((0, 0, -1))
sensor = next(item.matrix_world.translation.copy()
              for item in bpy.context.evaluated_depsgraph_get().object_instances
              if item.object.name == "ECCO_SENSOR_REF_01")
aim = anchor + forward * ((sensor.z - anchor.z) / forward.z)

# The casing cutaway faces a different way in v035. Rotate the v005 route about
# the bore axis and align its end to the existing first sensor camera.
reference = json.loads(score.read_text(encoding="utf-8-sig"))[:92]
base_eye = Vector(reference[-1]["position"])
base_aim = Vector(reference[-1]["target"])
route = Vector(reference[0]["position"]) - base_eye
old_radial = Vector((0, route.y, route.z)).normalized()
new_radial = Vector((0, anchor.y, anchor.z)).normalized()
alignment = old_radial.rotation_difference(new_radial)
scale = 0.72


def sample(index, field):
    first = int(index)
    last = min(first + 1, len(reference) - 1)
    return Vector(reference[first][field]).lerp(Vector(reference[last][field]), index - first)


action = camera.animation_data.action
curves = [
    curve for layer in action.layers for strip in layer.strips
    for bag in strip.channelbags if bag.slot == camera.animation_data.action_slot
    for curve in bag.fcurves if curve.data_path in {"location", "rotation_quaternion"}
]
assert len(curves) == 7
keys = {}
for frame in range(1, join):
    index = (frame - 1) * (len(reference) - 1) / (join - 1)
    eye = anchor + alignment @ ((sample(index, "position") - base_eye) * scale)
    look = aim + alignment @ ((sample(index, "target") - base_aim) * scale)
    rotation = forward.rotation_difference((look - eye).normalized()) @ anchor_rotation
    if rotation.dot(anchor_rotation) < 0:
        rotation.negate()
    keys[frame] = {"location": eye, "rotation_quaternion": rotation}
for curve in curves:
    old = [p for p in curve.keyframe_points if 1 <= p.co.x < join]
    assert len(old) == join - 1 and all(p.co.x == frame for frame, p in enumerate(old, 1))
    for frame, key in enumerate(old, 1):
        key.co.y = keys[frame][curve.data_path][curve.array_index]
    curve.update()

scene.frame_set(1)
bpy.context.preferences.filepaths.save_version = 0
bpy.ops.wm.save_as_mainfile(filepath=str(output), relative_remap=True, compress=True)
bpy.ops.wm.open_mainfile(filepath=str(output), use_scripts=False)
scene = bpy.context.scene
camera = scene.camera
assert all(lib.filepath.startswith("//") and Path(bpy.path.abspath(lib.filepath)).is_file()
           for lib in bpy.data.libraries)
after = protected_camera()
error = max(abs(a - b) for x, y in zip(protected, after) for a, b in zip(x, y))
assert error < 1e-6, error
scene.frame_set(join - 1)
left = camera.matrix_world.copy()
scene.frame_set(join)
right = camera.matrix_world.copy()
payload = {
    "source": source.name, "candidate": output.name, "v005_camera_reference_frames": [1, 92],
    "changed_camera_frames": [1, join - 1], "unchanged_camera_start": join,
    "protected_camera_samples": len(protected), "max_difference": error,
    "frame_62_to_63_camera_step_m": (left.translation - right.translation).length,
    "frame_62_to_63_rotation_radians": left.to_quaternion().rotation_difference(right.to_quaternion()).angle,
    "linked_libraries": [lib.filepath for lib in bpy.data.libraries],
}
evidence.write_text(json.dumps(payload, indent=2) + "\n")
print("CAMERA_CANDIDATE_READY", payload, flush=True)
