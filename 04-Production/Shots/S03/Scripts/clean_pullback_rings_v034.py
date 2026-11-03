"""Keep the middle pullback on the nominal rings and remove stray end contours."""
import bpy
import json
from math import hypot
from pathlib import Path
from time import perf_counter

shot = Path(__file__).resolve().parents[1]
candidate = shot / "Scenes/S03_white-ring-pullback_v034.blend"
assert not candidate.exists()
scene = bpy.context.scene

def factor(material):
    return material.node_tree.nodes["Mix Shader"].inputs[0]

def key(socket, frame, value):
    socket.default_value = value
    socket.keyframe_insert("default_value", frame=frame)

third_ring = bpy.data.objects["NOMINAL 02 arm 1"]
for frame in range(1, 55):
    scene.frame_set(frame)
    if third_ring.data.bevel_factor_end > 0.01:
        third_onset = frame
        break
assert 25 <= third_onset < 49
title = bpy.data.objects["Nominal Reference | upper-left third"]
opacity = factor(title.data.materials[0])
for frame in (1, 15, 49, 78, 552):
    opacity.keyframe_delete("default_value", frame=frame)
for frame, value in ((1,0),(third_onset,0),(third_onset+14,1),(49,1),(78,0),(552,0)):
    key(opacity, frame, value)

for frame in range(241, 275):
    scene.frame_set(frame)
    eye = scene.camera.matrix_world.translation
    if hypot(eye.x, eye.y) >= 0.18:
        exit_frame = frame
        break
assert 245 <= exit_frame <= 269

for obj in list(scene.objects):
    if obj.name == "360 DEGREE actual irregular wall contours" or obj.name.startswith("CLASSIFIED "):
        bpy.data.objects.remove(obj, do_unlink=True)
    elif obj.name.startswith("MEASURED ") or obj.name in ("v018 Near Nominal", "v018 Enlarged", "v018 Tight"):
        for frame in range(exit_frame, 553):
            obj.hide_render = True
            obj.hide_viewport = True
            obj.keyframe_insert("hide_render", frame=frame)
            obj.keyframe_insert("hide_viewport", frame=frame)
    elif obj.name.startswith("NOMINAL ") and obj.type == "CURVE":
        for frame in range(241, 553):
            obj.hide_render = frame >= 337
            obj.keyframe_insert("hide_render", frame=frame)

for i in range(8):
    nominal = factor(bpy.data.materials[f"Nominal ring station {i}"])
    for frame in range(241, 338):
        key(nominal, frame, 0.82 * max(0,min(1,(337-frame)/17)))

scene.frame_set(300)
bpy.ops.wm.save_as_mainfile(filepath=str(candidate), relative_remap=True)
bpy.ops.wm.open_mainfile(filepath=str(candidate))
scene = bpy.context.scene
assert bpy.data.objects.get("360 DEGREE actual irregular wall contours") is None
for frame in (exit_frame, 300, 325, 432, 552):
    scene.frame_set(frame)
    assert all(o.hide_render for o in scene.objects if o.name.startswith("MEASURED "))
    assert all(bpy.data.objects[n].hide_render for n in ("v018 Near Nominal","v018 Enlarged","v018 Tight"))
    assert all(o.hide_render == (frame >= 337) for o in scene.objects
               if o.type == "CURVE" and o.name.startswith("NOMINAL "))
(shot/"Notes/white-ring-pullback_v034.json").write_text(json.dumps(
    {"third_nominal_ring_onset":third_onset,"measured_and_interior_labels_hide":exit_frame,
     "white_ring_fade":[320,337],"full_contour_object_removed":True},indent=2)+"\n")
print("VERIFIED",third_onset,exit_frame,flush=True)
scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.render.resolution_percentage = 100
scene.eevee.taa_render_samples = 8
scene.eevee.use_raytracing = False
scene.render.use_compositing = False
for frame in (42,300,552):
    scene.frame_set(frame)
    scene.camera.data.update_tag()
    bpy.context.view_layer.update()
    scene.render.filepath = str(shot/f"Previews/S03_white-ring-pullback_v034_f{frame:04d}.png")
    start = perf_counter()
    bpy.ops.render.render(write_still=True)
    print("STILL",frame,round(perf_counter()-start,3),flush=True)
