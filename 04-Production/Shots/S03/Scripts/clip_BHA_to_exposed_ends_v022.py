"""Keep the orbit BHA wire on the exposed ends of the S03 bore."""
import bpy
import json
from pathlib import Path

shot = Path(__file__).resolve().parents[1]
candidate = shot / "Scenes/S03_exposed-BHA-ends_v022.blend"
assert not candidate.exists()
wall = bpy.data.objects["ILLUSTRATIVE CONTINUOUS WALL v009"]
z_values = [(wall.matrix_world @ v.co).z for v in wall.data.vertices]
low, high = min(z_values) - 0.004, max(z_values) + 0.004
wire = bpy.data.objects["BHA wireframe | orbit only"]
curve = wire.data
assert all(s.type == "POLY" for s in curve.splines)
original = [(tuple(p.co.copy() for p in s.points), s.use_cyclic_u) for s in curve.splines]
curve.splines.clear()

def add(points, cyclic=False):
    spline = curve.splines.new("POLY")
    spline.points.add(len(points) - 1)
    spline.use_cyclic_u = cyclic
    for point, coord in zip(spline.points, points):
        point.co = coord

for points, cyclic in original:
    for boundary, sign in ((low, -1), (high, 1)):
        if all(sign * (p.z - boundary) >= 0 for p in points):
            add(points, cyclic)
            continue
        following = points[1:] + (points[:1] if cyclic else ())
        for a, b in zip(points, following):
            a_out, b_out = sign * (a.z - boundary) >= 0, sign * (b.z - boundary) >= 0
            if not (a_out or b_out):
                continue
            if a_out != b_out:
                hit = a.lerp(b, (boundary - a.z) / (b.z - a.z))
                a, b = (a, hit) if a_out else (hit, b)
            if (a - b).length > 0.00001:
                add((a, b))

scene = bpy.context.scene
scene.frame_set(380)
bpy.ops.wm.save_as_mainfile(filepath=str(candidate), relative_remap=True)
bpy.ops.wm.open_mainfile(filepath=str(candidate))
wire = bpy.data.objects["BHA wireframe | orbit only"]
front, rear = 0, 0
for spline in wire.data.splines:
    positions = [p.co.z for p in spline.points]
    if max(positions) <= low + 1e-6:
        front += 1
    else:
        assert min(positions) >= high - 1e-6
        rear += 1
assert front and rear
for frame in (1, 241, 269, 270, 380, 432):
    bpy.context.scene.frame_set(frame)
    assert wire.hide_render == (frame < 270) and wire.hide_viewport == (frame < 270)
evidence = {"excluded_axial_span": [low, high], "front_splines": front,
            "rear_splines": rear, "first_visible_frame": 270}
print("VERIFIED", evidence, flush=True)
(shot / "Notes/exposed-BHA-ends_v022.json").write_text(json.dumps(evidence, indent=2) + "\n")
