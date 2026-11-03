"""Match the wall and floor colors in the S03 compute room."""
import bpy
from pathlib import Path
from time import perf_counter

shot = Path(__file__).resolve().parents[1]
candidate = shot / "Scenes/S03_floor-and-wall-grid_v037.blend"
assert not candidate.exists()
room = bpy.data.collections["S03 RECTANGULAR COMPUTE ROOM"]
floor_material = room.objects["Flat room floor"].data.materials[0]
for obj in room.objects:
    if obj.type == "MESH":
        obj.data.materials[0] = floor_material
wall_grid = room.objects["Unified room grid | walls"]
wall_grid.data.materials[0] = room.objects["Unified room grid | floor"].data.materials[0]
scene = bpy.context.scene
scene.frame_set(552)
bpy.ops.wm.save_as_mainfile(filepath=str(candidate),relative_remap=True)
bpy.ops.wm.open_mainfile(filepath=str(candidate))
scene = bpy.context.scene
room = bpy.data.collections["S03 RECTANGULAR COMPUTE ROOM"]
assert len({obj.data.materials[0].name for obj in room.objects if obj.type == "MESH"}) == 1
assert room.objects["Unified room grid | walls"].data.materials[0] == room.objects["Unified room grid | floor"].data.materials[0]
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
    scene.render.filepath = str(shot/f"Previews/S03_floor-and-wall-grid_v037_f{frame:04d}.png")
    start = perf_counter()
    bpy.ops.render.render(write_still=True)
    print("STILL",frame,round(perf_counter()-start,3),flush=True)
