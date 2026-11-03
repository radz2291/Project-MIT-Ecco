"""Close the compute room and center the existing wraparound camera."""
import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector
from pathlib import Path

shot = Path(__file__).resolve().parents[1]
candidate = shot / "Scenes/S03_centered-orbit-closed-room_v017.blend"
assert not candidate.exists()
scene = bpy.context.scene
room = bpy.data.collections["S03 RECTANGULAR COMPUTE ROOM"]
floor = room.objects["Flat room floor"]
side = room.objects["Flat side wall"]
a, b, c, d = [floor.matrix_world @ v.co for v in floor.data.vertices]
rise = side.matrix_world @ side.data.vertices[3].co - a

def panel(name, corners, material):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(corners, [], [(0, 1, 2, 3)])
    mesh.materials.append(material)
    room.objects.link(bpy.data.objects.new(name, mesh))

panel("Closed front wall", [a, b, b + rise, a + rise], side.data.materials[0])
panel("Closed ceiling", [a + rise, b + rise, c + rise, d + rise], floor.data.materials[0])
panels = [obj for obj in room.objects if obj.type == "MESH"]
assert len(panels) == 6
planes = []
inside = (a + b + c + d) / 4 + rise / 2
for obj in panels:
    p, q, r, _ = [obj.matrix_world @ v.co for v in obj.data.vertices]
    normal = (q - p).cross(r - p).normalized()
    if normal.dot(inside - p) < 0:
        normal.negate()
    planes.append((p, normal))

wall = bpy.data.objects["ILLUSTRATIVE CONTINUOUS WALL v009"]
pivot = sum((wall.matrix_world @ Vector(v) for v in wall.bound_box), Vector()) / 8
camera = scene.camera
original = {}
shifts = {}
for frame in range(258, 433):
    scene.frame_set(frame)
    original[frame] = camera.matrix_world.copy()
    shifts[frame] = (camera.data.shift_x, camera.data.shift_y)
for frame, matrix in original.items():
    scene.frame_set(frame)
    base = matrix.to_quaternion()
    forward = base @ Vector((0, 0, -1))
    toward_center = (pivot - matrix.translation).normalized()
    aimed = forward.rotation_difference(toward_center) @ base
    t = min(1.0, (frame - 258) / 12)
    rotation = base.slerp(aimed, t * t * (3 - 2 * t))
    rotation.make_compatible(camera.rotation_quaternion)
    camera.rotation_quaternion = rotation
    camera.keyframe_insert("rotation_quaternion", frame=frame)
    for prop, value in zip(("shift_x", "shift_y"), shifts[frame]):
        setattr(camera.data, prop, value * (1 - t * t * (3 - 2 * t)))
        camera.data.keyframe_insert(prop, frame=frame)

scene.frame_set(270)
bpy.ops.wm.save_as_mainfile(filepath=str(candidate), relative_remap=True)
bpy.ops.wm.open_mainfile(filepath=str(candidate))
scene = bpy.context.scene
room = bpy.data.collections["S03 RECTANGULAR COMPUTE ROOM"]
assert sum(o.type == "MESH" for o in room.objects) == 6
clearance = float("inf")
max_error = 0.0
for frame in range(270, 433):
    scene.frame_set(frame)
    camera = scene.camera
    eye = camera.matrix_world.translation
    assert (eye - original[frame].translation).length < 0.001
    screen = world_to_camera_view(scene, camera, pivot)
    assert screen.z > 0
    max_error = max(max_error, abs(screen.x - 0.5), abs(screen.y - 0.5))
    clearance = min(clearance, *(n.dot(eye - p) for p, n in planes))
assert clearance > 0.1 and max_error < 0.001
print("VERIFIED", clearance, max_error, flush=True)
