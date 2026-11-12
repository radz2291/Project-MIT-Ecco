"""Draw a digital wall from the existing S05 cutaway mesh."""

from hashlib import sha256
import json
import math
from pathlib import Path
from time import perf_counter

import bpy


shot = Path(__file__).resolve().parents[1]
output = shot / "Scenes/S05_wireframe-wall_v025.blend"
scene = bpy.context.scene
wall_name = "S05_FixedHalfBorehole"
room_name = "S05 Navy room"
flow_name = "S05_v018_ContinuousHydraulics"
wire_name = "S05 Digital borehole wall"
frames = (50, 205, 432)
assert Path(bpy.data.filepath).name == "S05_stylized-cutaway_v024.blend"
assert not output.exists()


def sample_scene(scene):
    objects = [scene.objects[name] for name in ("S05 Shared BHA v008", "S05 Shared uphole joint")]
    for name in (room_name, flow_name):
        objects.extend(sorted(scene.collection.children[name].all_objects, key=lambda obj: obj.name))
    result = []
    for frame in frames:
        scene.frame_set(frame)
        camera = scene.camera
        result.append((
            tuple(tuple(row) for row in camera.matrix_world), camera.data.lens,
            camera.data.dof.focus_distance, camera.data.shift_x, camera.data.shift_y,
            [(obj.name, tuple(tuple(row) for row in obj.matrix_world), obj.hide_render,
              tuple(slot.material.name for slot in obj.material_slots if slot.material))
             for obj in objects],
        ))
    return result


def mesh_signature(wall):
    return sha256(repr((
        [tuple(v.co) for v in wall.data.vertices],
        [(tuple(face.vertices), face.material_index) for face in wall.data.polygons],
    )).encode("utf-8")).hexdigest()


def ordered_arc(points):
    angle = lambda point: math.atan2(point[1], point[0])
    ordered = sorted(points, key=angle)
    gaps = [(angle(end) - angle(start)) % math.tau
            for start, end in zip(ordered, ordered[1:] + ordered[:1])]
    start = (max(range(len(gaps)), key=gaps.__getitem__) + 1) % len(ordered)
    return ordered[start:] + ordered[:start]


def at_depth(arc, z):
    return [(x, y, z) for x, y in arc]


def strokes(name, paths, width, color):
    material = bpy.data.materials.new(name)
    material.diffuse_color = (*color, 1)
    material.use_nodes = True
    tree = material.node_tree
    tree.nodes.clear()
    emission = tree.nodes.new("ShaderNodeEmission")
    emission.inputs["Color"].default_value = (*color, 1)
    surface = tree.nodes.new("ShaderNodeOutputMaterial")
    tree.links.new(emission.outputs[0], surface.inputs["Surface"])
    curve = bpy.data.curves.new(name, "CURVE")
    curve.dimensions = "3D"
    curve.bevel_depth = width
    curve.bevel_resolution = 0
    curve.materials.append(material)
    for points in paths:
        spline = curve.splines.new("POLY")
        spline.points.add(len(points) - 1)
        for point, coord in zip(spline.points, points):
            point.co = (*coord, 1)
    obj = bpy.data.objects.new(name, curve)
    wire.objects.link(obj)
    obj.matrix_world = wall.matrix_world.copy()


before = sample_scene(scene)
wall = scene.objects[wall_name]
signature = mesh_signature(wall)
vertices = [tuple(v.co) for v in wall.data.vertices]
lo, hi = min(p[2] for p in vertices), max(p[2] for p in vertices)
radii = [math.hypot(x, y) for x, y, z in vertices]
split = (min(radii) + max(radii)) / 2
end = [(x, y) for x, y, z in vertices if abs(z - lo) < 1e-5]
inner = ordered_arc([p for p in end if math.hypot(*p) < split])
outer = ordered_arc([p for p in end if math.hypot(*p) > split])
assert len(inner) == len(outer) == 97
for a, b in zip(inner, outer):
    assert abs(a[0] * b[1] - a[1] * b[0]) < 1e-6, (a, b)

wire = bpy.data.collections.new(wire_name)
scene.collection.children.link(wire)
stations = [lo + (hi - lo) * i / 14 for i in range(15)]
surface_paths = [at_depth(inner, z) for z in stations[1:-1]]
surface_paths += [[(*p, lo), (*p, hi)] for p in inner[12:-1:12]]
opening_paths = [at_depth(inner, z) for z in (lo, hi)]
opening_paths += [[(*p, lo), (*p, hi)] for p in (inner[0], inner[-1])]
thickness_paths = [at_depth(outer, z) for z in (lo, hi)]
for a, b in ((inner[0], outer[0]), (inner[-1], outer[-1])):
    thickness_paths.append([(*b, lo), (*b, hi)])
    thickness_paths.extend([[(*a, z), (*b, z)] for z in stations[::2]])

strokes("Borehole wall | blue grid", surface_paths, 0.00110, (0.024, 0.105, 0.165))
strokes("Borehole wall | cut opening", opening_paths, 0.00145, (0.032, 0.178, 0.265))
strokes("Borehole wall | cut thickness", thickness_paths, 0.00095, (0.015, 0.068, 0.108))
wall.hide_render = True
wall.hide_set(True)

scene.frame_set(frames[0])
scene.render.filepath = "//../Cache/v025/S05_"
bpy.ops.wm.save_as_mainfile(filepath=str(output), relative_remap=False)
bpy.ops.wm.open_mainfile(filepath=str(output))
scene = bpy.context.scene
wall = scene.objects[wall_name]
assert mesh_signature(wall) == signature and wall.hide_render
assert sample_scene(scene) == before
assert [len(obj.data.splines) for obj in scene.collection.children[wire_name].objects] == [
    len(surface_paths), len(opening_paths), len(thickness_paths),
]
libraries = {lib.name: lib.filepath for lib in bpy.data.libraries}
assert len(libraries) == 4
for path in libraries.values():
    assert path.startswith("//") and Path(bpy.path.abspath(path)).is_file(), path

record = {
    "source": "S05_stylized-cutaway_v024.blend",
    "scene": output.name,
    "frames": frames,
    "cutaway_mesh_and_material_indices_sha256": signature,
    "inner_radius_m": min(radii),
    "outer_radius_m": max(radii),
    "wall_station_count": len(stations),
    "curve_counts": [len(surface_paths), len(opening_paths), len(thickness_paths)],
    "relative_libraries": libraries,
    "stills": [],
}
scene.render.image_settings.file_format = "PNG"
for frame in frames:
    scene.frame_set(frame)
    image = shot / "Previews" / f"S05_wireframe-wall_v025_f{frame:04d}.png"
    scene.render.filepath = str(image)
    start = perf_counter()
    bpy.ops.render.render(write_still=True)
    record["stills"].append({"frame": frame, "seconds": perf_counter() - start})
    (shot / "Notes/v025-wireframe-wall.json").write_text(
        json.dumps(record, indent=2) + "\n", encoding="utf-8")
