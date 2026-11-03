"""Smooth the inspection zoom and the camera handoff into the S03 orbit."""
import bpy
import json
import math
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Quaternion, Vector
from pathlib import Path

shot = Path(__file__).resolve().parents[1]
candidate = shot / "Scenes/S03_camera-polish_v021.blend"
assert not candidate.exists()
scene = bpy.context.scene
camera = scene.camera
original = {}
for f in range(1, 433):
    scene.frame_set(f)
    m = camera.matrix_world
    original[f] = (m.translation.copy(), m.to_quaternion(), camera.data.lens, camera.data.shift_x)

def smooth(x):
    x = max(0, min(1, x))
    return x*x*(3-2*x)

def weights(frame, sigma):
    radius = math.ceil(sigma * 2.5)
    return [(f, math.exp(-0.5 * ((f - frame) / sigma)**2))
            for f in range(frame-radius, frame+radius+1)]

def average(frame, index, sigma):
    kernel = weights(frame, sigma)
    total = sum(w for _, w in kernel)
    if index == 1:
        base = original[frame][1]
        values = []
        for f, weight in kernel:
            q = original[f][1].copy()
            q.make_compatible(base)
            values.append((q, weight))
        return Quaternion(tuple(sum(q[i]*w for q,w in values)/total for i in range(4))).normalized()
    return sum((original[f][index] * w for f, w in kernel),
               Vector() if index == 0 else 0.0) / total

wall = bpy.data.objects["ILLUSTRATIVE CONTINUOUS WALL v009"]
pivot = sum((wall.matrix_world @ Vector(v) for v in wall.bound_box), Vector()) / 8
for f in range(190, 330):
    scene.frame_set(f)
    p, q, lens, shift = original[f]
    if 190 <= f <= 231:
        weight = smooth((f-190)/12) * smooth((231-f)/10)
        camera.data.lens = lens + weight * (average(f, 2, 5) - lens)
        camera.data.keyframe_insert("lens", frame=f)
    if f < 236:
        continue
    weight = smooth((f-236)/12) * smooth((329-f)/14)
    p = p.lerp(average(f, 0, 5), weight)
    q = q.slerp(average(f, 1, 6), weight)
    if f >= 270:
        forward = q @ Vector((0, 0, -1))
        q = forward.rotation_difference((pivot-p).normalized()) @ q
        shift = 0
    else:
        shift = original[258][3] * (1 - smooth((f-247)/23))
    q.make_compatible(camera.rotation_quaternion)
    camera.location = p
    camera.rotation_quaternion = q
    camera.data.shift_x = shift
    camera.keyframe_insert("location", frame=f)
    camera.keyframe_insert("rotation_quaternion", frame=f)
    camera.data.keyframe_insert("shift_x", frame=f)

scene.frame_set(245)
bpy.ops.wm.save_as_mainfile(filepath=str(candidate), relative_remap=True)
bpy.ops.wm.open_mainfile(filepath=str(candidate))
scene = bpy.context.scene
camera = scene.camera
measured = {}
room = bpy.data.collections["S03 RECTANGULAR COMPUTE ROOM"]
planes = []
for obj in room.objects:
    if obj.type == "MESH":
        a, b, c, _ = [obj.matrix_world @ v.co for v in obj.data.vertices]
        normal = (b-a).cross(c-a).normalized()
        if normal.dot(-a) < 0:
            normal.negate()
        planes.append((a, normal))
clearance, center = float("inf"), 0.0
for f in range(190, 433):
    scene.frame_set(f)
    m = camera.matrix_world
    measured[f] = (m.translation.copy(), m.to_quaternion(), camera.data.lens, camera.data.shift_x)
    if f >= 270:
        uv = world_to_camera_view(scene, camera, pivot)
        center = max(center, abs(uv.x-0.5), abs(uv.y-0.5))
        clearance = min(clearance, *(n.dot(m.translation-a) for a,n in planes))
assert center < 0.001 and clearance > 0.1

def metrics(rows):
    return {
        "peak_turn_deg_per_frame_245_275": max(math.degrees(2*math.acos(min(1, abs(
            rows[f-1][1].dot(rows[f][1]))))) for f in range(245,276)),
        "peak_shift_per_frame_245_275": max(abs(rows[f-1][3]-rows[f][3]) for f in range(245,276)),
        "peak_zoom_mm_per_frame_195_225": max(abs(rows[f-1][2]-rows[f][2]) for f in range(195,226)),
        "peak_position_second_difference_270_315": max(
            (rows[f+1][0]-2*rows[f][0]+rows[f-1][0]).length for f in range(270,316)),
    }

report = {"before": metrics(original), "after": metrics(measured),
          "max_orbit_center_error": center, "min_orbit_room_clearance": clearance}
print(json.dumps(report), flush=True)
(shot / "Notes/camera-polish_v021.json").write_text(json.dumps(report, indent=2) + "\n")
