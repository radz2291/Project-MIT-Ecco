"""Align the floor and wall grids at the S03 room corners."""
import bpy
import json
from pathlib import Path
from time import perf_counter

shot = Path(__file__).resolve().parents[1]
candidate = shot / "Scenes/S03_unified-room-grid_v035.blend"
assert not candidate.exists()
scene = bpy.context.scene
room = bpy.data.collections["S03 RECTANGULAR COMPUTE ROOM"]
floor = room.objects["Flat room floor"]
side = room.objects["Flat side wall"]
a, b, c, d = [floor.matrix_world @ v.co for v in floor.data.vertices]
rise = side.matrix_world @ side.data.vertices[3].co - a
center = (a+b+c+d)/4 + rise/2
spacing = 0.72
cross_count = round(((b-a).length + (c-d).length) / (2*spacing))
depth_count = round(((d-a).length + (c-b).length) / (2*spacing))
height_count = round(rise.length/spacing)

def traces(name, segments, color, strength, width):
    curve = bpy.data.curves.new(name,"CURVE")
    curve.dimensions = "3D"
    curve.bevel_depth = width
    curve.bevel_resolution = 0
    material = bpy.data.materials.new(name)
    material.diffuse_color = (*color,1)
    material.use_nodes = True
    tree = material.node_tree
    tree.nodes.clear()
    emission = tree.nodes.new("ShaderNodeEmission")
    emission.inputs["Color"].default_value = (*color,1)
    emission.inputs["Strength"].default_value = strength
    output = tree.nodes.new("ShaderNodeOutputMaterial")
    tree.links.new(emission.outputs[0],output.inputs["Surface"])
    curve.materials.append(material)
    for start,end in segments:
        spline = curve.splines.new("POLY")
        spline.points.add(1)
        spline.points[0].co = (*start,1)
        spline.points[1].co = (*end,1)
    room.objects.link(bpy.data.objects.new(name,curve))

floor_segments, wall_segments = [], []
# Apply an identical tiny inset at each shared endpoint to avoid z-fighting.
def inset(p):
    return p.lerp(center,0.0008)

for i in range(1,cross_count):
    t = i/cross_count
    near,far = inset(a.lerp(b,t)),inset(d.lerp(c,t))
    floor_segments.append((near,far))
    wall_segments.extend(((near,inset(a.lerp(b,t)+rise)),(far,inset(d.lerp(c,t)+rise))))
for i in range(1,depth_count):
    t = i/depth_count
    left,right = inset(a.lerp(d,t)),inset(b.lerp(c,t))
    floor_segments.append((left,right))
    wall_segments.extend(((left,inset(a.lerp(d,t)+rise)),(right,inset(b.lerp(c,t)+rise))))
for i in range(1,height_count):
    height = rise*(i/height_count)
    corners = [inset(p+height) for p in (a,b,c,d)]
    wall_segments.extend(zip(corners,corners[1:]+corners[:1]))

bpy.data.objects.remove(room.objects["Rectangular room panel grid"],do_unlink=True)
color = (0.016,0.084,0.14)
traces("Unified room grid | floor",floor_segments,color,0.54,0.0022)
traces("Unified room grid | walls",wall_segments,color,0.34,0.00185)
scene.frame_set(300)
bpy.ops.wm.save_as_mainfile(filepath=str(candidate),relative_remap=True)
bpy.ops.wm.open_mainfile(filepath=str(candidate))
scene = bpy.context.scene
assert bpy.data.objects.get("Rectangular room panel grid") is None
assert len(bpy.data.objects["Unified room grid | floor"].data.splines) == len(floor_segments)
assert len(bpy.data.objects["Unified room grid | walls"].data.splines) == len(wall_segments)
(shot/"Notes/unified-room-grid_v035.json").write_text(json.dumps(
    {"target_spacing":spacing,"divisions":[cross_count,depth_count,height_count],
     "floor_strokes":len(floor_segments),"wall_strokes":len(wall_segments)},indent=2)+"\n")
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
    scene.render.filepath = str(shot/f"Previews/S03_unified-room-grid_v035_f{frame:04d}.png")
    start = perf_counter()
    bpy.ops.render.render(write_still=True)
    print("STILL",frame,round(perf_counter()-start,3),flush=True)
