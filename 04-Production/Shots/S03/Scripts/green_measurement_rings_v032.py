"""Try a thinner teal-green measurement line based on the supplied swatch."""
import bpy
from pathlib import Path
from time import perf_counter

shot = Path(__file__).resolve().parents[1]
candidate = shot / "Scenes/S03_green-rings_v032.blend"
assert not candidate.exists()
scene = bpy.context.scene
green = (0.035, 0.72, 0.44, 1)
for i in range(8):
    material = bpy.data.materials[f"Measured ring station {i}"]
    emission = material.node_tree.nodes["Emission"]
    emission.inputs["Color"].default_value = green
    material.diffuse_color = green
for obj in scene.objects:
    if obj.type == "CURVE" and obj.name.startswith("MEASURED "):
        obj.data.bevel_depth *= 1.15 / 1.65

title = bpy.data.objects["Nominal Reference | upper-left third"]
factor = next(n for n in title.data.materials[0].node_tree.nodes if n.type == "MIX_SHADER").inputs[0]
for frame in (1,244,260,552):
    factor.keyframe_delete("default_value",frame=frame)
for frame,value in ((1,1),(49,1),(78,0),(552,0)):
    factor.default_value = value
    factor.keyframe_insert("default_value",frame=frame)

scene.frame_set(172)
bpy.ops.wm.save_as_mainfile(filepath=str(candidate),relative_remap=True)
bpy.ops.wm.open_mainfile(filepath=str(candidate))
scene = bpy.context.scene
assert abs(bpy.data.materials["Measured ring station 1"].node_tree.nodes["Emission"].inputs["Color"].default_value[1] - .72) < 1e-6
scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.render.resolution_percentage = 100
scene.eevee.taa_render_samples = 8
scene.eevee.use_raytracing = False
scene.render.use_compositing = False
factor = next(n for n in bpy.data.objects["Nominal Reference | upper-left third"].data.materials[0].node_tree.nodes if n.type == "MIX_SHADER").inputs[0]
for frame,expected in ((48,1),(78,0),(172,0),(222,0)):
    scene.frame_set(frame)
    assert abs(factor.default_value-expected) < 1e-6
for frame in (48,172,222):
    scene.frame_set(frame)
    scene.camera.data.update_tag()
    bpy.context.view_layer.update()
    scene.render.filepath = str(shot/f"Previews/S03_green-rings_v032_f{frame:04d}.png")
    start = perf_counter()
    bpy.ops.render.render(write_still=True)
    print("STILL",frame,round(perf_counter()-start,3),flush=True)
