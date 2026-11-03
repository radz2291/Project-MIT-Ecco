"""Match the S03 wire display to the inspected S02 BHA and string sizing."""
import bpy
import json
from math import hypot
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from pathlib import Path

shot = Path(__file__).resolve().parents[1]
candidate = shot / "Scenes/S03_orbit-BHA-source-scale_v020.blend"
assert not candidate.exists()
bpy.ops.wm.open_mainfile(filepath=str(shot.parent / "S01-S02/Scenes/S01-S02_production_v027_clean.blend"))
scene = bpy.context.scene
scene.frame_set(756)
deps = bpy.context.evaluated_depsgraph_get()
assembly = bpy.data.objects["BHA sequence assembly"]
scale = tuple(assembly.matrix_world.to_scale())
assert max(abs(v - 1) for v in scale) < 0.00001
axis = assembly.matrix_world.to_3x3().col[0].normalized()
assert axis.dot(Vector((0, 0, -1))) > 0.999
pipe = bpy.data.objects["Sequence string connected above BHA"].evaluated_get(deps)
pipe_radius = max(hypot(p.x, p.y) for v in pipe.data.vertices
                  for p in [pipe.matrix_world @ v.co])
assert 0.01 < pipe_radius < 0.2
print("S02", scale, tuple(axis), pipe_radius, flush=True)

bpy.ops.wm.open_mainfile(filepath=str(shot / "Scenes/S03_orbit-BHA-context_v019.blend"))
scene = bpy.context.scene
wire = bpy.data.objects["BHA wireframe | orbit only"]
splines = list(wire.data.splines)
parts = [p for spline in splines[:-25] for p in spline.points]
tail = [p for spline in splines[-25:] for p in spline.points]
assert len(parts) == 2 * 7355
radial = wire["display_radial_scale"]
axial = wire["display_axial_scale"]
bit = min(p.co.z for p in parts)
old_join = max(p.co.z for p in parts)
tail_end = wire["tail_display_end_z"]
tail_radius = max(hypot(p.co.x, p.co.y) for p in tail)
for p in parts:
    p.co.x /= radial
    p.co.y /= radial
    p.co.z = bit + (p.co.z - bit) / axial
join = max(p.co.z for p in parts)
for p in tail:
    p.co.x *= pipe_radius / tail_radius
    p.co.y *= pipe_radius / tail_radius
    p.co.z = join + (p.co.z - old_join) * (tail_end - join) / (tail_end - old_join)
wire["display_radial_scale"] = wire["display_axial_scale"] = 1.0
wire["pipe_radius_from_S02"] = pipe_radius

wall = bpy.data.objects["ILLUSTRATIVE CONTINUOUS WALL v009"]
mesh = wall.data
mesh.calc_loop_triangles()
verts = [wall.matrix_world @ v.co for v in mesh.vertices]
low, high = min(p.z for p in verts), max(p.z for p in verts)
surface = BVHTree.FromPolygons(verts, [tuple(t.vertices) for t in mesh.loop_triangles],
                               all_triangles=True)
clearance = []
for p in parts + tail:
    x, y, z, _ = p.co
    r = hypot(x, y)
    if not low < z < high or r < 0.000001:
        continue
    hit, _, _, distance = surface.ray_cast(Vector((0, 0, z)), Vector((x/r, y/r, 0)), 1)
    if hit is not None:
        clearance.append(distance - r)
assert clearance
evidence = {
    "S02_assembly_scale": scale, "S02_pipe_diameter": pipe_radius * 2,
    "S03_BHA_wire_max_diameter": 2 * max(hypot(p.co.x, p.co.y) for p in parts),
    "S03_BHA_wire_length": join - bit, "sampled_min_radial_clearance": min(clearance),
    "sampled_inside_bore": len(clearance),
    "sampled_points_crossing_wall": sum(gap < 0 for gap in clearance),
}
print("SIZING", json.dumps(evidence), flush=True)
(shot / "Notes/bha-source-scale_v020.json").write_text(json.dumps(evidence, indent=2) + "\n")
scene.frame_set(380)
bpy.ops.wm.save_as_mainfile(filepath=str(candidate), relative_remap=True)
bpy.ops.wm.open_mainfile(filepath=str(candidate))
scene = bpy.context.scene
wire = bpy.data.objects["BHA wireframe | orbit only"]
for frame in (1, 269, 270, 380, 432):
    scene.frame_set(frame)
    assert wire.hide_render == (frame < 270)
