"""Stage nominal rings first, then draw the three labeled measurement profiles."""
import bpy
import json
from math import hypot
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from pathlib import Path
from time import perf_counter

shot = Path(__file__).resolve().parents[1]
candidate = shot / "Scenes/S03_label-synced-rings_v028.blend"
assert not candidate.exists()
scene = bpy.context.scene

def mix_socket(material):
    node = next(n for n in material.node_tree.nodes if n.type == "MIX_SHADER")
    assert node.inputs[1].links[0].from_node.type == "BSDF_TRANSPARENT"
    return node.inputs[0]

names = ("Near Nominal", "Enlarged", "Tight")
label_factors = [mix_socket(bpy.data.objects["v018 " + name].data.materials[0]) for name in names]
visibility = {i: [] for i in range(3)}
nominal_sockets = [mix_socket(bpy.data.materials[f"Nominal ring station {i}"]) for i in range(8)]
nominal_values = []
for frame in range(1, 242):
    scene.frame_set(frame)
    nominal_values.append([socket.default_value for socket in nominal_sockets])
    for i,socket in enumerate(label_factors):
        visibility[i].append(socket.default_value)

def set_override(socket, key, values):
    scene[key] = 0.0
    path = '["' + key + '"]'
    for f, value in enumerate(values, 1):
        scene[key] = value
        scene.keyframe_insert(path, frame=f)
    driver_path = socket.path_from_id("default_value")
    driver = next(c.driver for c in socket.id_data.animation_data.drivers if c.data_path == driver_path)
    var = driver.variables.new()
    var.name = "label_reveal"
    var.type = "SINGLE_PROP"
    var.targets[0].id_type = "SCENE"
    var.targets[0].id = scene
    var.targets[0].data_path = path
    driver.type = "SCRIPTED"
    driver.expression = "label_reveal if frame <= 240 else channel"

for i in range(8):
    measured_material = bpy.data.materials[f"Measured ring station {i}"]
    measured = mix_socket(measured_material)
    nominal = mix_socket(bpy.data.materials[f"Nominal ring station {i}"])
    scene.frame_set(241)

    if i < 3:
        onset = next(f for f,v in enumerate(visibility[i], 1) if v > .001)
        for sign in (-1,1):
            for prefix in ("NOMINAL","MEASURED"):
                ring = bpy.data.objects[f"{prefix} {i:02d} arm {sign}"]
                scene.frame_set(241)
                resume = ring.hide_render
                for f in range(1,241):
                    ring.hide_render = False
                    ring.keyframe_insert("hide_render",frame=f)
                ring.hide_render = resume
                ring.keyframe_insert("hide_render",frame=241)
                if prefix == "MEASURED":
                    for f in range(onset-1, onset+12):
                        ring.data.bevel_factor_end = max(0,min(1,(f-onset+1)/10))
                        ring.data.keyframe_insert("bevel_factor_end",frame=f)
        glow = next(n for n in measured_material.node_tree.nodes if n.type == "EMISSION")
        glow.inputs["Strength"].default_value *= 1.28
    set_override(measured, f"S03 measured reveal {i}", visibility[i][:240] if i < 3 else [0.0]*240)
    if i < 3:
        values = [max(row[i], .72*visibility[i][f]) if f >= 99 else row[i]
                  for f,row in enumerate(nominal_values[:240])]
        for f,value in enumerate(values + [nominal_values[240][i]], 1):
            nominal.default_value = value
            nominal.keyframe_insert("default_value", frame=f)

# The overview contours and independent classified fragments would reveal
# measured geometry ahead of the text. Keep them for the outgoing view.
scene.frame_set(241)
for obj in scene.objects:
    if obj.name == "360 DEGREE actual irregular wall contours" or obj.name.startswith(("CLASSIFIED ","Radial witness station")):
        exit_state = obj.hide_render
        for f, hidden in ((1,True),(240,True),(241,exit_state)):
            obj.hide_render = hidden
            obj.keyframe_insert("hide_render",frame=f)

# Conform the Tight line to the visible wall, with a small drawing offset inward.
scene.frame_set(222)
wall = bpy.data.objects["ILLUSTRATIVE CONTINUOUS WALL v009"]
wall.data.calc_loop_triangles()
surface = BVHTree.FromPolygons([wall.matrix_world @ v.co for v in wall.data.vertices],
                               [tuple(t.vertices) for t in wall.data.loop_triangles],
                               all_triangles=True)
adjusted = 0
for sign in (-1, 1):
    ring = bpy.data.objects[f"MEASURED 02 arm {sign}"]
    inverse = ring.matrix_world.inverted()
    for spline in ring.data.splines:
        for point in spline.points:
            p = ring.matrix_world @ point.co.to_3d()
            r = hypot(p.x, p.y)
            if r < 0.001:
                continue
            direction = Vector((p.x/r,p.y/r,0))
            hit, _, _, distance = surface.ray_cast(Vector((0,0,p.z)),direction,1)
            if hit is not None and r > distance - 0.0014:
                p.x, p.y = direction.x*(distance-0.0014), direction.y*(distance-0.0014)
                point.co = (*(inverse @ p), point.co.w)
                adjusted += 1
    ring.data.bevel_depth = 0.00085
print("TIGHT LINE DRAWING OFFSET", adjusted, flush=True)

scene.frame_set(122)
bpy.ops.wm.save_as_mainfile(filepath=str(candidate),relative_remap=True)
bpy.ops.wm.open_mainfile(filepath=str(candidate))
scene = bpy.context.scene
checks = {}
for frame in (1,72,122,172,222):
    scene.frame_set(frame)
    factors = [mix_socket(bpy.data.materials[f"Measured ring station {i}"]).default_value for i in range(8)]
    assert [i for i,v in enumerate(factors) if v > .05] == {1:[],72:[],122:[0],172:[1],222:[2]}[frame]
    assert bpy.data.objects["360 DEGREE actual irregular wall contours"].hide_render
    checks[frame] = factors
(shot/"Notes/label-synced-rings_v028.json").write_text(json.dumps(checks,indent=2)+"\n")
scene.render.resolution_x = 480
scene.render.resolution_y = 270
scene.render.resolution_percentage = 100
scene.eevee.taa_render_samples = 4
scene.eevee.use_raytracing = False
scene.render.use_compositing = False
for frame in (1,122,172,222):
    scene.frame_set(frame)
    scene.camera.data.update_tag()
    bpy.context.view_layer.update()
    scene.render.filepath = str(shot/f"Previews/S03_label-synced-rings_v028_f{frame:04d}.png")
    start = perf_counter()
    bpy.ops.render.render(write_still=True)
    print("STILL",frame,round(perf_counter()-start,3),flush=True)
