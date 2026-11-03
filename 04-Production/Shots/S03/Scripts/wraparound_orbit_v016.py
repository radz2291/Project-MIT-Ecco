"""Build the wraparound establishing camera from the owner's overhead sketch."""
import bpy
import math
from pathlib import Path
from mathutils import Matrix, Vector

shot = Path(__file__).resolve().parents[1]
candidate = shot / "Scenes/S03_wraparound-orbit_v016.blend"
assert not candidate.exists()
scene = bpy.context.scene
camera = scene.camera
assert camera.rotation_mode == "QUATERNION"
planes = []
for obj in bpy.data.collections["S03 RECTANGULAR COMPUTE ROOM"].objects:
    if obj.type == "MESH":
        a, b, c, _ = [obj.matrix_world @ v.co for v in obj.data.vertices]
        normal = (b - a).cross(c - a).normalized()
        if normal.dot(-a) < 0:
            normal.negate()
        planes.append((a, normal))
        if obj.name == "Flat room floor":
            up = normal

start, blend_end, end = 270, 309, 432
scene.frame_set(start)
wall = bpy.data.objects["ILLUSTRATIVE CONTINUOUS WALL v009"]
pivot = sum((wall.matrix_world @ Vector(v) for v in wall.bound_box), Vector()) / 8
bore_axis = Vector((0, 0, 1))
side = up.cross(bore_axis).normalized()

original = {}
for frame in range(start, end + 1):
    scene.frame_set(frame)
    original[frame] = camera.matrix_world.copy()

approach = original[blend_end].translation - pivot
start_angle = math.atan2(approach.dot(bore_axis) / 4.9, approach.dot(side) / 6.2)

def smooth(t):
    t = max(0, min(1, t))
    return t * t * (3 - 2 * t)

expected = {}
for frame, base in original.items():
    scene.frame_set(frame)
    progress = smooth((frame - start) / (end - start))
    theta = start_angle + math.radians(265) * progress
    eye = pivot + side * (6.2 * math.cos(theta)) + bore_axis * (4.9 * math.sin(theta)) + up * 0.68
    backward = (eye - pivot).normalized()
    right = up.cross(backward).normalized()
    true_up = backward.cross(right)
    look = Matrix((right, true_up, backward)).transposed().to_quaternion()
    blend = smooth((frame - start) / (blend_end - start))
    location = base.translation.lerp(eye, blend)
    rotation = base.to_quaternion().slerp(look, blend)
    rotation.make_compatible(camera.rotation_quaternion)
    camera.location = location
    camera.rotation_quaternion = rotation
    camera.keyframe_insert("location", frame=frame)
    camera.keyframe_insert("rotation_quaternion", frame=frame)
    expected[frame] = (location, rotation)

scene.frame_set(start)
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type == "VIEW_3D":
            area.spaces.active.region_3d.view_perspective = "CAMERA"
bpy.ops.wm.save_as_mainfile(filepath=str(candidate), relative_remap=True)
bpy.ops.wm.open_mainfile(filepath=str(candidate))
scene = bpy.context.scene
clearance = float("inf")
for frame, (location, rotation) in expected.items():
    scene.frame_set(frame)
    matrix = scene.camera.matrix_world
    assert (matrix.translation - location).length < 0.001
    assert abs(matrix.to_quaternion().dot(rotation)) > 0.99999
    clearance = min(clearance, *(n.dot(location - p) for p, n in planes))
assert clearance > 0.1
print("VERIFIED", len(expected), "frames; minimum room clearance", round(clearance, 3))
