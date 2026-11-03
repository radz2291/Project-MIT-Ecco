"""Make the aligned wall grid readable in the S03 orbit."""
import bpy
from pathlib import Path
from time import perf_counter

shot = Path(__file__).resolve().parents[1]
candidate = shot / "Scenes/S03_floor-and-wall-grid_v036.blend"
assert not candidate.exists()
walls = bpy.data.objects["Unified room grid | walls"]
walls.data.bevel_depth = 0.008
emission = walls.data.materials[0].node_tree.nodes["Emission"]
emission.inputs["Strength"].default_value = 0.68
scene = bpy.context.scene
scene.frame_set(552)
bpy.ops.wm.save_as_mainfile(filepath=str(candidate),relative_remap=True)
bpy.ops.wm.open_mainfile(filepath=str(candidate))
scene = bpy.context.scene
assert abs(bpy.data.objects["Unified room grid | walls"].data.bevel_depth - .008) < 1e-6
scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.render.resolution_percentage = 100
scene.eevee.taa_render_samples = 8
scene.eevee.use_raytracing = False
scene.render.use_compositing = False
for frame in (300,552):
    scene.frame_set(frame)
    scene.camera.data.update_tag()
    bpy.context.view_layer.update()
    scene.render.filepath = str(shot/f"Previews/S03_floor-and-wall-grid_v036_f{frame:04d}.png")
    start = perf_counter()
    bpy.ops.render.render(write_still=True)
    print("STILL",frame,round(perf_counter()-start,3),flush=True)
