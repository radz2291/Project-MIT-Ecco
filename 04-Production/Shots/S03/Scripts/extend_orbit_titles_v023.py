"""Extend the orbit, smooth its entry, and pin the late titles to camera space."""
import bpy
import json
import math
from pathlib import Path
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Matrix, Quaternion, Vector

shot = Path(__file__).resolve().parents[1]
candidate = shot / "Scenes/S03_extended-orbit_v023.blend"
assert not candidate.exists()
scene = bpy.context.scene
camera = scene.camera
original = {}
for f in range(248, 433):
    scene.frame_set(f)
    original[f] = camera.matrix_world.copy()

room = bpy.data.collections["S03 RECTANGULAR COMPUTE ROOM"]
planes = []
for obj in room.objects:
    if obj.type != "MESH":
        continue
    a, b, c, _ = [obj.matrix_world @ v.co for v in obj.data.vertices]
    normal = (b-a).cross(c-a).normalized()
    if normal.dot(-a) < 0:
        normal.negate()
    planes.append((a, normal))
    if obj.name == "Flat room floor":
        up = normal

wall = bpy.data.objects["ILLUSTRATIVE CONTINUOUS WALL v009"]
pivot = sum((wall.matrix_world @ Vector(v) for v in wall.bound_box), Vector()) / 8
axis = Vector((0, 0, 1))
side = up.cross(axis).normalized()
junction, end = 385, 552

def smooth(t):
    t = min(1, max(0, t))
    return t*t*(3-2*t)

def frame_angle(frame):
    delta = original[frame].translation - pivot
    return math.atan2(delta.dot(axis)/4.9, delta.dot(side)/6.2)

start_angle = frame_angle(junction)
angular_speed = math.remainder(start_angle - frame_angle(junction-1), math.tau)
end_angle = start_angle + math.radians(205)

def continued(f):
    t = (f-junction)/(end-junction)
    theta = (1-smooth(t))*start_angle + smooth(t)*end_angle
    theta += (t**3 - 2*t*t + t) * angular_speed * (end-junction)
    eye = pivot + side*(6.2*math.cos(theta)) + axis*(4.9*math.sin(theta)) + up*0.68
    backward = (eye-pivot).normalized()
    right = up.cross(backward).normalized()
    return eye, Matrix((right, backward.cross(right), backward)).transposed().to_quaternion()

def entry(f):
    m = original[f]
    blend = smooth((f-258)/9) * smooth((306-f)/18)
    radius = 12
    weights = [(k, math.exp(-0.5*((k-f)/5)**2))
               for k in range(max(248,f-radius), min(432,f+radius)+1)]
    total = sum(w for _,w in weights)
    pos = sum((original[k].translation*w for k,w in weights), Vector()) / total
    base = m.to_quaternion()
    samples = []
    for k,w in weights:
        q = original[k].to_quaternion()
        q.make_compatible(base)
        samples.append((q,w))
    rotation = Quaternion(tuple(sum(q[i]*w for q,w in samples)/total for i in range(4))).normalized()
    pos = m.translation.lerp(pos, blend)
    rotation = base.slerp(rotation, blend)
    if f >= 270:
        rotation = (rotation @ Vector((0,0,-1))).rotation_difference((pivot-pos).normalized()) @ rotation
    return pos, rotation

scene.frame_end = end
for f in list(range(258,307)) + list(range(junction+1,end+1)):
    scene.frame_set(f)
    pos, rotation = entry(f) if f <= 306 else continued(f)
    rotation.make_compatible(camera.rotation_quaternion)
    camera.location = pos
    camera.rotation_quaternion = rotation
    camera.keyframe_insert("location", frame=f)
    camera.keyframe_insert("rotation_quaternion", frame=f)

for name in ("GEOMETRY THROUGH DEPTH", "ACOUSTIC AMPLITUDE  |  RECORDED DATA"):
    title = bpy.data.objects[name]
    visibility = {}
    previous = None
    for f in range(1,433):
        scene.frame_set(f)
        if previous != title.hide_render:
            previous = title.hide_render
            visibility[f] = previous
    title.animation_data_clear()
    title.parent = camera
    title.matrix_parent_inverse.identity()
    title.rotation_mode = "XYZ"
    title.rotation_euler = (0,0,0)
    title.location = (0,0.18,-1)
    title.data = title.data.copy()
    title.data.align_x = "CENTER"
    title.data.align_y = "CENTER"
    title.data.size = 0.032
    for f, hidden in visibility.items():
        title.hide_render = title.hide_viewport = hidden
        title.keyframe_insert("hide_render", frame=f)
        title.keyframe_insert("hide_viewport", frame=f)
    for path, index in (("scale",0), ("scale",1), ("location",1)):
        driver = title.driver_add(path,index).driver
        var = driver.variables.new()
        var.name = "lens"
        var.type = "SINGLE_PROP"
        var.targets[0].id_type = "CAMERA"
        var.targets[0].id = camera.data
        var.targets[0].data_path = "lens"
        driver.expression = ("0.18*" if path == "location" else "") + "32/lens"

scene.frame_set(270)
bpy.ops.wm.save_as_mainfile(filepath=str(candidate), relative_remap=True)
bpy.ops.wm.open_mainfile(filepath=str(candidate))
scene = bpy.context.scene
assert scene.frame_end == end
clearance, center = float("inf"), 0
for f in range(270,end+1):
    scene.frame_set(f)
    eye = scene.camera.matrix_world.translation
    uv = world_to_camera_view(scene, scene.camera, pivot)
    center = max(center, abs(uv.x-.5), abs(uv.y-.5))
    clearance = min(clearance, *(n.dot(eye-a) for a,n in planes))
assert clearance > .1 and center < .001, (clearance, center)
evidence = {"frames":end,"fps":24,"orbit_continuation_degrees_after_385":205,
            "min_room_clearance":clearance,"max_bore_center_error":center}
print("VERIFIED",evidence,flush=True)
(shot/"Notes/extended-orbit_v023.json").write_text(json.dumps(evidence,indent=2)+"\n")
