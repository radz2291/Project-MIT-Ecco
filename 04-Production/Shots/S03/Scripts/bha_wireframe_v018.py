"""Derive an orbit-only wireframe from the shared BHA film assembly."""
import bpy
import bmesh
from math import hypot, radians
from pathlib import Path
from time import perf_counter

shot = Path(__file__).resolve().parents[1]
source = shot.parents[1] / "Shared/Assets/Hardware/BHA/BHA_film_v008.blend"
candidate = shot / "Scenes/S03_orbit-BHA-wireframe_v018.blend"
assert not candidate.exists()
bpy.ops.wm.open_mainfile(filepath=str(source))
deps = bpy.context.evaluated_depsgraph_get()
prefixes = ("ECCO_HOUSING_SOURCE_MESH", "UPHOLE_COLLAR", "DOWNHOLE_COLLAR",
            "UPHOLE_ADAPTER", "DOWNHOLE_ADAPTER", "PDC_WEB_AND_SHANK",
            "PDC_INTEGRAL_BLADE", "TEMP | Imaging")
parts = [(i.object.name, i.object.data, i.matrix_world.copy())
         for i in deps.object_instances if i.object.type == "MESH"
         and i.object.name.startswith(prefixes)]
segments = []
for name, mesh, transform in parts:
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bm.normal_update()
    if len(bm.edges) > 4000:
        bmesh.ops.dissolve_limit(bm, angle_limit=radians(8), verts=list(bm.verts),
                                 edges=list(bm.edges), use_dissolve_boundaries=False)
        bm.normal_update()
    for edge in bm.edges:
        if name.startswith("ECCO_HOUSING") and edge.is_manifold and edge.calc_face_angle() < radians(18):
            continue
        a, b = [transform @ v.co for v in edge.verts]
        if (a - b).length > 0.004:
            segments.append((a, b))
    bm.free()
assert len(parts) >= 10 and 100 < len(segments) < 30000, (len(parts), len(segments))
points = [p for pair in segments for p in pair]
lo, hi = min(p.x for p in points), max(p.x for p in points)
radius = max(hypot(p.y, p.z) for p in points)
print("SOURCE", len(parts), len(segments), lo, hi, radius, flush=True)

bpy.ops.wm.open_mainfile(filepath=str(shot / "Scenes/S03_centered-orbit-closed-room_v017.blend"))
scene = bpy.context.scene
wall = bpy.data.objects["ILLUSTRATIVE CONTINUOUS WALL v009"]
zlo = min((wall.matrix_world @ p.co).z for p in wall.data.vertices)
zhi = max((wall.matrix_world @ p.co).z for p in wall.data.vertices)
center = (zlo + zhi) / 2
axial_scale = min(1.0, (zhi - zlo - 0.22) / (hi - lo))
radial_scale = min(1.0, 0.108 / radius)
curve = bpy.data.curves.new("BHA v008 derived feature edges", "CURVE")
curve.dimensions = "3D"
curve.bevel_depth = 0.0022
curve.bevel_resolution = 0
for pair in segments:
    spline = curve.splines.new("POLY")
    spline.points.add(1)
    for point, p in zip(spline.points, pair):
        point.co = (p.y * radial_scale, p.z * radial_scale,
                    center - (p.x - (hi + lo) / 2) * axial_scale, 1)
material = bpy.data.materials.new("BHA wire | cool cyan")
material.diffuse_color = (0.09, 0.8, 1, 1)
material.use_nodes = True
nodes = material.node_tree.nodes
nodes.clear()
emission = nodes.new("ShaderNodeEmission")
emission.inputs["Color"].default_value = (0.045, 0.67, 1, 1)
emission.inputs["Strength"].default_value = 3.4
output = nodes.new("ShaderNodeOutputMaterial")
material.node_tree.links.new(emission.outputs[0], output.inputs["Surface"])
curve.materials.append(material)
wire = bpy.data.objects.new("BHA wireframe | orbit only", curve)
scene.collection.objects.link(wire)
wire["source"] = "Shared/Assets/Hardware/BHA/BHA_film_v008.blend"
wire["display_radial_scale"] = radial_scale
wire["display_axial_scale"] = axial_scale
for frame, hidden in ((1, True), (269, True), (270, False), (432, False)):
    wire.hide_render = wire.hide_viewport = hidden
    wire.keyframe_insert("hide_render", frame=frame)
    wire.keyframe_insert("hide_viewport", frame=frame)

# Let the existing amplitude wall read as a translucent data skin over the wire.
shell = wall.data.materials[0].copy()
wall.data.materials[0] = shell
tree = shell.node_tree
output = next(n for n in tree.nodes if n.type == "OUTPUT_MATERIAL" and n.is_active_output)
original = output.inputs["Surface"].links[0].from_socket
transparent = tree.nodes.new("ShaderNodeBsdfTransparent")
mix = tree.nodes.new("ShaderNodeMixShader")
mix.label = "Orbit x-ray for BHA"
tree.links.new(original, mix.inputs[1])
tree.links.new(transparent.outputs[0], mix.inputs[2])
tree.links.new(mix.outputs[0], output.inputs["Surface"])
for frame, amount in ((1, 0), (269, 0), (282, 0.78), (432, 0.78)):
    mix.inputs[0].default_value = amount
    mix.inputs[0].keyframe_insert("default_value", frame=frame)

scene.frame_set(372)
bpy.ops.wm.save_as_mainfile(filepath=str(candidate), relative_remap=True)
bpy.ops.wm.open_mainfile(filepath=str(candidate))
scene = bpy.context.scene
wire = bpy.data.objects["BHA wireframe | orbit only"]
for frame in (1, 145, 241, 269, 270, 372, 432):
    scene.frame_set(frame)
    assert wire.hide_render == (frame < 270) and wire.hide_viewport == (frame < 270)
print("VERIFIED", len(segments), radial_scale, axial_scale, flush=True)
scene.render.resolution_x = 480
scene.render.resolution_y = 270
scene.render.resolution_percentage = 100
scene.eevee.taa_render_samples = 4
scene.eevee.use_raytracing = False
scene.render.use_compositing = False
scene.render.filepath = str(shot / "Previews/S03_orbit-BHA-wireframe_v018_f0432.png")
start = perf_counter()
bpy.ops.render.render(write_still=True)
print("STILL", round(perf_counter() - start, 3), flush=True)
