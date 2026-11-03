"""Simplify S03 measurement graphics and test orange measured outlines."""
import bpy
import json
from pathlib import Path
from time import perf_counter

shot = Path(__file__).resolve().parents[1]
candidate = shot / "Scenes/S03_clean-orange-rings_v030.blend"
assert not candidate.exists()
scene = bpy.context.scene
removed = []
for obj in list(scene.objects):
    text = obj.data.body.upper() if obj.type == "FONT" else ""
    duplicate = "NOMINAL REFERENCE" in text and obj.name != "Nominal Reference | upper-left third"
    disclaimer = "NOT FIELD DATA" in text
    guide = obj.name.startswith(("Nominal cylinder supporting rail", "Radial witness station"))
    if duplicate or disclaimer or guide:
        removed.append(obj.name)
        bpy.data.objects.remove(obj, do_unlink=True)

orange = (1.0, 0.25, 0.035, 1.0)
for i in range(8):
    material = bpy.data.materials[f"Measured ring station {i}"]
    color = material.node_tree.nodes["Emission"].inputs["Color"]
    for channel in range(3):
        color.driver_remove("default_value",channel)
    color.default_value = orange
    material.diffuse_color = orange
for obj in scene.objects:
    if obj.type == "CURVE" and obj.name.startswith("MEASURED "):
        obj.data.bevel_depth *= 1.65

scene.frame_set(172)
bpy.ops.wm.save_as_mainfile(filepath=str(candidate),relative_remap=True)
bpy.ops.wm.open_mainfile(filepath=str(candidate))
scene = bpy.context.scene
assert all(bpy.data.objects.get(name) is None for name in removed)
assert bpy.data.objects["Nominal Reference | upper-left third"]
for frame in (48,122,172,222):
    scene.frame_set(frame)
    for i in range(3):
        value = bpy.data.materials[f"Measured ring station {i}"].node_tree.nodes["Emission"].inputs["Color"].default_value
        assert abs(value[1] - orange[1]) < 1e-6
(shot/"Notes/clean-orange-rings_v030.json").write_text(json.dumps(
    {"removed_objects":removed,"measured_color":orange,"measured_line_width_multiplier":1.65},
    indent=2)+"\n")
scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.render.resolution_percentage = 100
scene.eevee.taa_render_samples = 8
scene.eevee.use_raytracing = False
scene.render.use_compositing = False
for frame in (48,122,172,222):
    scene.frame_set(frame)
    scene.camera.data.update_tag()
    bpy.context.view_layer.update()
    scene.render.filepath = str(shot/f"Previews/S03_clean-orange-rings_v030_f{frame:04d}.png")
    start = perf_counter()
    bpy.ops.render.render(write_still=True)
    print("STILL",frame,round(perf_counter()-start,3),flush=True)
