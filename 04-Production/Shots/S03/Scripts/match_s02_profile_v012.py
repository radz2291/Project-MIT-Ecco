"""Fit the S03 bore surface to the actual S02 reveal carrier by depth and azimuth."""
import bpy
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from math import hypot
from time import perf_counter

shot = Path(__file__).resolve().parents[1]
source = shot.parent / "S01-S02/Scenes/S01-S02_production_v027_clean.blend"
candidate = shot / "Scenes/S03_matched-S02-proof_v012.blend"
if candidate.exists():
    raise FileExistsError(candidate)

bpy.ops.wm.open_mainfile(filepath=str(source))
bpy.context.scene.frame_set(756)
carrier = bpy.data.objects["ONE WALL - old history and current cells share topology"]
mesh = carrier.data
mesh.calc_loop_triangles()
points = [carrier.matrix_world @ vertex.co for vertex in mesh.vertices]
triangles = [tuple(face.vertices) for face in mesh.loop_triangles]
surface = BVHTree.FromPolygons(points, triangles, all_triangles=True)
low, high = min(p.z for p in points), max(p.z for p in points)
print("S02_SOURCE", len(points), low, high, flush=True)

bpy.ops.wm.open_mainfile(filepath=str(shot / "Scenes/S03_compute-room-proof_v011.blend"))
scene = bpy.context.scene
scene.frame_set(1)
wall = bpy.data.objects["ILLUSTRATIVE CONTINUOUS WALL v009"]
depth_offset = bpy.data.objects["S03 recorded wall"].matrix_world.translation.z
to_world, to_local = wall.matrix_world.copy(), wall.matrix_world.inverted()
changed, misses, max_shift = 0, 0, 0.0
for vertex in wall.data.vertices:
    p = to_world @ vertex.co
    radius = hypot(p.x, p.y)
    if radius < 1e-7:
        continue
    z = p.z - depth_offset
    z = max(low + 0.0001, min(high - 0.0001, z))
    direction = Vector((p.x / radius, p.y / radius, 0))
    hit, _, _, distance = surface.ray_cast(Vector((0, 0, z)), direction, 1.0)
    if hit is None:
        misses += 1
        continue
    vertex.co = to_local @ Vector((hit.x, hit.y, p.z))
    changed += 1
    max_shift = max(max_shift, abs(distance - radius))
wall.data.update()
print("MATCH", changed, misses, round(max_shift, 6), depth_offset, flush=True)
assert misses == 0 and changed > 0
scene.render.resolution_x = 640
scene.render.resolution_y = 360
scene.render.resolution_percentage = 100
scene.eevee.taa_render_samples = 8
bpy.ops.wm.save_as_mainfile(filepath=str(candidate), relative_remap=True)
bpy.ops.wm.open_mainfile(filepath=str(candidate))
assert not bpy.data.libraries
scene = bpy.context.scene
for frame, suffix in ((1, "opening"), (1, "angle")):
    scene.frame_set(frame)
    if suffix == "angle":
        scene.camera = bpy.data.objects["Compute-space review angle"]
    scene.camera.data.update_tag()
    bpy.context.view_layer.update()
    scene.render.filepath = str(shot / f"Previews/S03_matched-S02_v012_{suffix}.png")
    start = perf_counter()
    bpy.ops.render.render(write_still=True)
    print("PROOF", suffix, round(perf_counter() - start, 3), flush=True)
