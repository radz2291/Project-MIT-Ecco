"""Build an editable S03 compute-space look proof on the v001 shot."""
import bpy
from pathlib import Path
from mathutils import Vector, Quaternion
from time import perf_counter

shot = Path(__file__).resolve().parents[1]
scene = bpy.context.scene
candidate = shot / "Scenes/S03_compute-box-proof_v007.blend"
if candidate.exists():
    raise FileExistsError(candidate)

empty = bpy.data.node_groups.new("S03 remove geological context", "GeometryNodeTree")
empty.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
empty.nodes.new("NodeGroupOutput")
for name in ("Luminous geological strata", "Subordinate formation survey grid",
             "SOLID EARTH - borehole cutaway half-space",
             "GROUND FRONT HALF - closes tunnel for interior camera",
             "Geological cut faces - fade away inside", "Borehole cutaway cyan rim",
             "Subtle bounded atmosphere"):
    obj = bpy.data.objects[name]
    obj.modifiers.new("Compute-space replacement", "NODES").node_group = empty

space = bpy.data.collections.new("S03 RECTANGULAR COMPUTE ROOM")
scene.collection.children.link(space)

def emission(name, color, strength):
    material = bpy.data.materials.new(name)
    material.use_nodes = True
    nodes = material.node_tree.nodes
    nodes.clear()
    glow = nodes.new("ShaderNodeEmission")
    glow.inputs["Color"].default_value = (*color, 1)
    glow.inputs["Strength"].default_value = strength
    output = nodes.new("ShaderNodeOutputMaterial")
    material.node_tree.links.new(glow.outputs[0], output.inputs["Surface"])
    return material

def traces(name, segments, width, material):
    curve = bpy.data.curves.new(name, "CURVE")
    curve.dimensions = "3D"
    curve.bevel_depth = width
    curve.bevel_resolution = 0
    curve.materials.append(material)
    for points in segments:
        line = curve.splines.new("POLY")
        line.points.add(len(points) - 1)
        for point, xyz in zip(line.points, points):
            point.co = (*xyz, 1)
    space.objects.link(bpy.data.objects.new(name, curve))

hero_data = bpy.data.cameras.new("Compute-space review lens")
hero_data.lens = 34
hero = bpy.data.objects.new("Compute-space review angle", hero_data)
space.objects.link(hero)
scene.frame_set(1)
wall = bpy.data.objects["ILLUSTRATIVE CONTINUOUS WALL v009"]
start_z = min((wall.matrix_world @ Vector(corner)).z for corner in wall.bound_box)
hero.location = (0.72, -0.42, start_z - 0.95)
target = Vector((0.0, 0.0, start_z + 0.75))
hero.rotation_mode = "QUATERNION"
hero.rotation_quaternion = (target - hero.location).to_track_quat("-Z", "Y") @ Quaternion((0, 0, 1), 0.70)

# The environment reads as one broad plane with a distant rectangular back wall.
# The bore wall and its own rings remain separate from the room.
bpy.data.collections["v018 minimal scientific coordinate field"].hide_render = True
up = hero.rotation_quaternion @ Vector((0, 1, 0))
up.z = 0
up.normalize()
across = Vector((up.y, -up.x, 0))
floor = -1.1 * up

def room_point(x, z, height=0):
    return floor + x * across + Vector((0, 0, z)) + height * up

grid = emission("Room grid | low blue", (0.008, 0.065, 0.14), 0.28)
major = emission("Room tracks | cyan", (0.012, 0.12, 0.22), 0.40)
minor_lines, major_lines = [], []
for step in range(-32, 33):
    p = step * 0.75
    layer = major_lines if step % 4 == 0 else minor_lines
    layer.extend([(room_point(p, -18), room_point(p, 36)),
                  (room_point(-24, p + 12), room_point(24, p + 12))])
traces("Wide rectangular floor grid", minor_lines, 0.002, grid)
traces("Long horizon and floor tracks",
       major_lines + [(room_point(-24, 36), room_point(24, 36))], 0.003, major)

wall_dots = []
for row in range(1, 12):
    for column in range(-24, 25):
        point = room_point(column * 0.95, 36, row * 0.75)
        wall_dots.append((point, point + across * 0.045))
traces("Distant rectangular wall sample lights", wall_dots, 0.009, grid)

scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.render.resolution_percentage = 100
scene.eevee.taa_render_samples = 8
scene.render.image_settings.file_format = "PNG"
scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(candidate), relative_remap=True)
bpy.ops.wm.open_mainfile(filepath=str(candidate))
assert not bpy.data.libraries
scene = bpy.context.scene
for frame, suffix in ((1, "opening"), (1, "angle")):
    if suffix == "angle":
        scene.camera = bpy.data.objects["Compute-space review angle"]
    scene.frame_set(frame)
    scene.camera.data.update_tag()
    bpy.context.view_layer.update()
    scene.render.filepath = str(shot / f"Previews/S03_compute-box_v007_{suffix}.png")
    start = perf_counter()
    bpy.ops.render.render(write_still=True)
    print("PROOF", frame, round(perf_counter() - start, 3), flush=True)
