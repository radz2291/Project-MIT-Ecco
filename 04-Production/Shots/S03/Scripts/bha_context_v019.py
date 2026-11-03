"""Keep the orange bore opaque and expose only the contextual BHA ends."""
import bpy
from math import cos, hypot, sin, tau
from pathlib import Path
from time import perf_counter

shot = Path(__file__).resolve().parents[1]
candidate = shot / "Scenes/S03_orbit-BHA-context_v019.blend"
assert not candidate.exists()
scene = bpy.context.scene
wall = bpy.data.objects["ILLUSTRATIVE CONTINUOUS WALL v009"]
tree = wall.data.materials[0].node_tree
mix = next(n for n in tree.nodes if n.label == "Orbit x-ray for BHA")
output = next(n for n in tree.nodes if n.type == "OUTPUT_MATERIAL" and n.is_active_output)
original = mix.inputs[1].links[0].from_socket
transparent = mix.inputs[2].links[0].from_node
mix.inputs[0].keyframe_delete("default_value", frame=1)
for frame in (269, 282, 432):
    mix.inputs[0].keyframe_delete("default_value", frame=frame)
tree.links.new(original, output.inputs["Surface"])
tree.nodes.remove(mix)
tree.nodes.remove(transparent)
assert output.inputs["Surface"].links[0].from_socket == original

wire = bpy.data.objects["BHA wireframe | orbit only"]
curve = wire.data
points = [point for spline in curve.splines for point in spline.points]
bit_end = min(p.co.z for p in points)
bore_end = min((wall.matrix_world @ v.co).z for v in wall.data.vertices)
offset = bore_end - 0.62 - bit_end
for point in points:
    point.co.z += offset
tail_start = max(p.co.z for p in points)
radius = max(hypot(p.co.x, p.co.y) for p in points if p.co.z > tail_start - 0.035)
tail_end = 8.4

def add_trace(coords, cyclic=False):
    trace = curve.splines.new("POLY")
    trace.points.add(len(coords) - 1)
    trace.use_cyclic_u = cyclic
    for point, co in zip(trace.points, coords):
        point.co = (*co, 1)

for i in range(8):
    theta = i * tau / 8
    x, y = radius * cos(theta), radius * sin(theta)
    add_trace([(x, y, tail_start), (x, y, tail_end)])
for i in range(17):
    z = tail_start + (tail_end - tail_start) * i / 16
    add_trace([(radius * cos(j * tau / 24), radius * sin(j * tau / 24), z)
               for j in range(24)], cyclic=True)

material = curve.materials[0]
material.diffuse_color = (0.12, 0.35, 0.46, 1)
emission = next(n for n in material.node_tree.nodes if n.type == "EMISSION")
emission.inputs["Color"].default_value = (0.055, 0.26, 0.4, 1)
emission.inputs["Strength"].default_value = 1.35
curve.bevel_depth = 0.0017
wire["tail_display_end_z"] = tail_end
wire["bit_exposure_scene_units"] = 0.62

scene.frame_set(380)
bpy.ops.wm.save_as_mainfile(filepath=str(candidate), relative_remap=True)
bpy.ops.wm.open_mainfile(filepath=str(candidate))
scene = bpy.context.scene
wire = bpy.data.objects["BHA wireframe | orbit only"]
for frame in (1, 241, 269, 270, 380, 432):
    scene.frame_set(frame)
    assert wire.hide_render == (frame < 270) and wire.hide_viewport == (frame < 270)
wall = bpy.data.objects["ILLUSTRATIVE CONTINUOUS WALL v009"]
assert all(n.label != "Orbit x-ray for BHA" for n in wall.data.materials[0].node_tree.nodes)
print("VERIFIED", round(tail_start, 3), tail_end, round(radius, 4), flush=True)

scene.frame_set(380)
scene.camera.data.update_tag()
bpy.context.view_layer.update()
scene.render.resolution_x = 480
scene.render.resolution_y = 270
scene.render.resolution_percentage = 100
scene.eevee.taa_render_samples = 4
scene.eevee.use_raytracing = False
scene.render.use_compositing = False
scene.render.filepath = str(shot / "Previews/S03_orbit-BHA-context_v019_f0380.png")
start = perf_counter()
bpy.ops.render.render(write_still=True)
print("STILL", round(perf_counter() - start, 3), flush=True)
