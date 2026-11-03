"""Build an editable S03 compute-space look proof on the v001 shot."""
import bpy
from pathlib import Path
from mathutils import Vector, Quaternion
from time import perf_counter

shot = Path(__file__).resolve().parents[1]
scene = bpy.context.scene
candidate = shot / "Scenes/S03_compute-room-proof_v010.blend"
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

bpy.data.collections["v018 minimal scientific coordinate field"].hide_render = True
up = hero.rotation_quaternion @ Vector((0, 1, 0))
up.z = 0
up.normalize()
across = Vector((up.y, -up.x, 0))

def room_point(x, z, height=0):
    return (height - 1.16) * up + x * across + Vector((0, 0, z))

def panel(name, corners, material):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(corners, [], [(0, 1, 2, 3)])
    mesh.materials.append(material)
    space.objects.link(bpy.data.objects.new(name, mesh))

left, right = -4.35, 4.35
near, far = start_z - 3.0, start_z + 9.0
height = 4.4
floor = emission("Room floor | navy", (0.007, 0.017, 0.034), 0.7)
side = emission("Side walls | dark blue", (0.011, 0.027, 0.052), 0.75)
back = emission("Back wall | blue", (0.014, 0.041, 0.074), 0.85)
grid = emission("Room grid | blue", (0.016, 0.084, 0.14), 0.48)
edge = emission("Room corner | cyan", (0.018, 0.15, 0.26), 0.68)

panel("Flat room floor", [room_point(left, near), room_point(right, near),
                         room_point(right, far), room_point(left, far)], floor)
panel("Visible back wall", [room_point(left, far), room_point(right, far),
                            room_point(right, far, height), room_point(left, far, height)], back)
segments, corners = [], []
for x in (left, right):
    panel("Flat side wall", [room_point(x, near), room_point(x, far),
                            room_point(x, far, height), room_point(x, near, height)], side)
    corners.extend([(room_point(x, near, 0.006), room_point(x, far, 0.006)),
                    (room_point(x, far - 0.008), room_point(x, far - 0.008, height))])
    inset = x * 0.997
    for row in range(1, 10):
        h = row * 0.44
        segments.append((room_point(inset, near, h), room_point(inset, far, h)))
    for col in range(1, 22):
        z = near + (far - near) * col / 22
        segments.append((room_point(inset, z), room_point(inset, z, height)))

for col in range(1, 24):
    x = left + (right - left) * col / 24
    segments.extend([(room_point(x, near, 0.006), room_point(x, far, 0.006)),
                     (room_point(x, far - 0.008), room_point(x, far - 0.008, height))])
for col in range(1, 22):
    z = near + (far - near) * col / 22
    segments.append((room_point(left, z, 0.006), room_point(right, z, 0.006)))
for row in range(1, 10):
    h = row * 0.44
    segments.append((room_point(left, far - 0.008, h), room_point(right, far - 0.008, h)))
corners.append((room_point(left, far - 0.008, 0.006), room_point(right, far - 0.008, 0.006)))
traces("Rectangular room panel grid", segments, 0.002, grid)
traces("Floor and back-wall corner seams", corners, 0.004, edge)

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
    scene.render.filepath = str(shot / f"Previews/S03_compute-room_v010_{suffix}.png")
    start = perf_counter()
    bpy.ops.render.render(write_still=True)
    print("PROOF", frame, round(perf_counter() - start, 3), flush=True)
