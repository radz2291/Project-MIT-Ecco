"""Extend the custom S05 bore profile into one continuous digital ground mesh."""

import json
import math
from pathlib import Path
from time import perf_counter

import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree


shot = Path(__file__).resolve().parents[1]
output = shot / "Scenes/S05_continuous-ground_v026.blend"
scene = bpy.context.scene
frames = (50, 205, 432)
ground_name = "S05 Continuous borehole and ground"
assert Path(bpy.data.filepath).name == "S05_wireframe-wall_v025.blend"
assert not output.exists()


def foreground_state(scene):
    tracked = [scene.objects[name] for name in ("S05 Shared BHA v008", "S05 Shared uphole joint")]
    tracked.extend(sorted(scene.collection.children["S05_v018_ContinuousHydraulics"].all_objects,
                          key=lambda obj: obj.name))
    result = []
    for frame in frames:
        scene.frame_set(frame)
        camera = scene.camera
        result.append((
            tuple(tuple(row) for row in camera.matrix_world), camera.data.lens,
            camera.data.dof.focus_distance, camera.data.shift_x, camera.data.shift_y,
            [(obj.name, tuple(tuple(row) for row in obj.matrix_world), obj.hide_render,
              tuple(slot.material.name for slot in obj.material_slots if slot.material))
             for obj in tracked],
        ))
    return result


def connect(tree, value, socket):
    if isinstance(value, bpy.types.NodeSocket):
        tree.links.new(value, socket)
    else:
        socket.default_value = value


def math_node(tree, operation, first, second):
    node = tree.nodes.new("ShaderNodeMath")
    node.operation = operation
    connect(tree, first, node.inputs[0])
    connect(tree, second, node.inputs[1])
    return node.outputs[0]


def ramp(tree, signal, start, end, low, high):
    node = tree.nodes.new("ShaderNodeMapRange")
    node.interpolation_type = "SMOOTHSTEP"
    for name, value in (("Value", signal), ("From Min", start), ("From Max", end),
                        ("To Min", low), ("To Max", high)):
        connect(tree, value, node.inputs[name])
    return node.outputs["Result"]


def mix(tree, factor, base, accent):
    node = tree.nodes.new("ShaderNodeMixRGB")
    for i, value in enumerate((factor, base, accent)):
        connect(tree, value, node.inputs[i])
    return node.outputs["Color"]


def periodic_line(tree, coordinate, pitch, width):
    phase = math_node(tree, "PINGPONG", coordinate, pitch / 2)
    return ramp(tree, phase, width * 0.45, width, 1.0, 0.0)


def material(name, inside):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    tree = m.node_tree
    tree.nodes.clear()
    uv = tree.nodes.new("ShaderNodeTexCoord")
    separate = tree.nodes.new("ShaderNodeSeparateXYZ")
    tree.links.new(uv.outputs["UV"], separate.inputs[0])
    u, depth = separate.outputs["X"], separate.outputs["Y"]
    rings = periodic_line(tree, depth, 0.207, 0.0026)
    if inside:
        rails = periodic_line(tree, u, arc_length / 8, 0.0022)
        pattern = math_node(tree, "MAXIMUM", rings, rails)
        color = mix(tree, pattern, (0.010, 0.023, 0.039, 1), (0.023, 0.090, 0.142, 1))
    else:
        to_left = math_node(tree, "MULTIPLY", u, -1.0)
        to_right = math_node(tree, "SUBTRACT", u, arc_length)
        distance = math_node(tree, "MAXIMUM", to_left, to_right)
        falloff = ramp(tree, distance, 0.0, 0.42, 1.0, 0.0)
        base = mix(tree, falloff, (0.010, 0.022, 0.037, 1), (0.013, 0.030, 0.050, 1))
        line = math_node(tree, "MULTIPLY", rings, falloff)
        lip = ramp(tree, distance, 0.0013, 0.0036, 0.9, 0.0)
        color = mix(tree, math_node(tree, "MAXIMUM", line, lip), base, (0.026, 0.098, 0.149, 1))
    shader = tree.nodes.new("ShaderNodeEmission")
    tree.links.new(color, shader.inputs["Color"])
    surface = tree.nodes.new("ShaderNodeOutputMaterial")
    tree.links.new(shader.outputs[0], surface.inputs["Surface"])
    return m


def check_coverage(scene, ground):
    mesh = ground.data
    surface = BVHTree.FromPolygons([ground.matrix_world @ v.co for v in mesh.vertices],
                                  [tuple(p.vertices) for p in mesh.polygons])
    count = 0
    for frame in range(scene.frame_start, scene.frame_end + 1):
        scene.frame_set(frame)
        camera = scene.camera
        corners = camera.data.view_frame(scene=scene)
        x0, x1 = min(v.x for v in corners), max(v.x for v in corners)
        y0, y1 = min(v.y for v in corners), max(v.y for v in corners)
        z = corners[0].z
        for i in range(7):
            for j in range(5):
                direction = camera.matrix_world.to_3x3() @ Vector(
                    (x0 + (x1 - x0) * i / 6, y0 + (y1 - y0) * j / 4, z))
                hit = surface.ray_cast(camera.matrix_world.translation, direction.normalized())
                assert hit[0] is not None, (frame, i, j)
                count += 1
    return count


before = foreground_state(scene)
source = scene.objects["S05_FixedHalfBorehole"]
coords = [tuple(vertex.co) for vertex in source.data.vertices]
lo, hi = min(p[2] for p in coords), max(p[2] for p in coords)
radius = min(math.hypot(x, y) for x, y, _ in coords)
arc = [(x, y) for x, y, z in coords
       if abs(z - lo) < 1e-5 and abs(math.hypot(x, y) - radius) < 1e-5]
angles = lambda p: math.atan2(p[1], p[0])
arc.sort(key=angles)
gaps = [(angles(b) - angles(a)) % math.tau for a, b in zip(arc, arc[1:] + arc[:1])]
first = (max(range(len(gaps)), key=gaps.__getitem__) + 1) % len(arc)
arc = arc[first:] + arc[:first]
assert len(arc) == 97
distance = [0.0]
for a, b in zip(arc, arc[1:]):
    distance.append(distance[-1] + math.dist(a, b))
arc_length = distance[-1]
extension = 12.0
outer_a, outer_b = [tuple(c * (1 + extension / radius) for c in p) for p in (arc[0], arc[-1])]
profile = [outer_a, *arc, outer_b]
surface_distance = [-extension, *distance, arc_length + extension]
depths = [lo - 12.0, lo, hi, hi + 12.0]
vertices = [(x, y, depth) for depth in depths for x, y in profile]
stride = len(profile)
faces = [(j * stride + i, j * stride + i + 1, (j + 1) * stride + i + 1, (j + 1) * stride + i)
         for j in range(len(depths) - 1) for i in range(stride - 1)]
mesh = bpy.data.meshes.new(ground_name)
mesh.from_pydata(vertices, [], faces)
mesh.update()
mesh.materials.append(material("S05 digital bore wall", inside=True))
mesh.materials.append(material("S05 plain digital ground", inside=False))
uv = mesh.uv_layers.new(name="Continuous wall and ground coordinates")
for face in mesh.polygons:
    face.material_index = int(face.index % (stride - 1) in (0, stride - 2))
    for index in face.loop_indices:
        row, column = divmod(mesh.loops[index].vertex_index, stride)
        uv.data[index].uv = (surface_distance[column], depths[row])
ground = bpy.data.objects.new(ground_name, mesh)
scene.collection.children["S05_FIXED_SECTION"].objects.link(ground)
ground.matrix_world = source.matrix_world.copy()
for name in ("S05 Navy room", "S05 Digital borehole wall"):
    scene.collection.children[name].hide_render = True
    scene.collection.children[name].hide_viewport = True
assert source.hide_render
coverage = check_coverage(scene, ground)
scene.frame_set(frames[0])
scene.render.filepath = "//../Cache/v026/S05_"
bpy.ops.wm.save_as_mainfile(filepath=str(output), relative_remap=False)
bpy.ops.wm.open_mainfile(filepath=str(output))
scene = bpy.context.scene
assert foreground_state(scene) == before
assert len(scene.objects[ground_name].data.polygons) == len(faces)
assert all(scene.collection.children[name].hide_render
           for name in ("S05 Navy room", "S05 Digital borehole wall"))
libraries = {lib.name: lib.filepath for lib in bpy.data.libraries}
assert len(libraries) == 4
for path in libraries.values():
    assert path.startswith("//") and Path(bpy.path.abspath(path)).is_file(), path

record = {
    "source": "S05_wireframe-wall_v025.blend",
    "scene": output.name,
    "review_frames": frames,
    "source_bore_radius_m": radius,
    "source_arc_samples": len(arc),
    "connected_surface_faces": len(faces),
    "camera_coverage_rays": coverage,
    "relative_libraries": libraries,
    "stills": [],
}
scene.render.image_settings.file_format = "PNG"
for frame in frames:
    scene.frame_set(frame)
    path = shot / "Previews" / f"S05_continuous-ground_v026_f{frame:04d}.png"
    scene.render.filepath = str(path)
    start = perf_counter()
    bpy.ops.render.render(write_still=True)
    record["stills"].append({"frame": frame, "seconds": perf_counter() - start})
    (shot / "Notes/v026-continuous-ground.json").write_text(
        json.dumps(record, indent=2) + "\n", encoding="utf-8")
