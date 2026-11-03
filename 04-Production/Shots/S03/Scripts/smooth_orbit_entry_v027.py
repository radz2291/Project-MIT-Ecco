"""Remove the frame-270 aim snap and fade in the exposed BHA ends."""
import bpy
import json
import math
from mathutils import Quaternion
from pathlib import Path

shot = Path(__file__).resolve().parents[1]
scene = bpy.context.scene
cam = scene.camera
candidate = shot / "Scenes/S03_smooth-orbit-entry_v027.blend"
assert not candidate.exists()
original = {}
for f in range(242,301):
    scene.frame_set(f)
    original[f] = cam.matrix_world.to_quaternion()

def ease(t):
    t = max(0,min(1,t))
    return t*t*(3-2*t)

for f in range(252,289):
    scene.frame_set(f)
    base = original[f]
    window = []
    for k in range(f-9,f+10):
        q = original[k].copy()
        q.make_compatible(base)
        window.append((q,math.exp(-0.5*((k-f)/3.7)**2)))
    average = Quaternion(tuple(sum(q[i]*w for q,w in window) for i in range(4))).normalized()
    weight = ease((f-252)/10)*ease((288-f)/9)
    q = base.slerp(average,weight)
    q.make_compatible(cam.rotation_quaternion)
    cam.rotation_quaternion = q
    cam.keyframe_insert("rotation_quaternion",frame=f)

wire = bpy.data.objects["BHA wireframe | orbit only"]
tree = wire.data.materials[0].node_tree
output = next(n for n in tree.nodes if n.type == "OUTPUT_MATERIAL" and n.is_active_output)
original_shader = output.inputs["Surface"].links[0].from_socket
transparent = tree.nodes.new("ShaderNodeBsdfTransparent")
fade = tree.nodes.new("ShaderNodeMixShader")
fade.label = "Soft BHA orbit entrance"
tree.links.new(transparent.outputs[0],fade.inputs[1])
tree.links.new(original_shader,fade.inputs[2])
tree.links.new(fade.outputs[0],output.inputs["Surface"])
for f,amount in ((269,0),(270,0),(290,1)):
    fade.inputs[0].default_value = amount
    fade.inputs[0].keyframe_insert("default_value",frame=f)
scene.frame_set(252)
bpy.ops.wm.save_as_mainfile(filepath=str(candidate),relative_remap=True)
bpy.ops.wm.open_mainfile(filepath=str(candidate))
scene = bpy.context.scene
def speed(a,b):
    return math.degrees(2*math.acos(min(1,abs(a.dot(b)))))
after = {}
for f in range(242,301):
    scene.frame_set(f)
    after[f] = scene.camera.matrix_world.to_quaternion()
def metrics(rows):
    values = [speed(rows[f-1],rows[f]) for f in range(258,285)]
    return {"frame_270_turn":speed(rows[269],rows[270]),
            "peak_turn_258_284":max(values),
            "peak_turn_step_258_284":max(abs(b-a) for a,b in zip(values,values[1:]))}
evidence = {"before":metrics(original),"after":metrics(after)}
assert evidence["after"]["frame_270_turn"] < 2.9
assert evidence["after"]["peak_turn_step_258_284"] < evidence["before"]["peak_turn_step_258_284"]
assert scene.frame_end == 552
print("VERIFIED",evidence,flush=True)
(shot/"Notes/smooth-orbit-entry_v027.json").write_text(json.dumps(evidence,indent=2)+"\n")
