"""Add two illustrative tight spots at the marked close-up locations."""
import bpy
import json
import math
from mathutils.bvhtree import BVHTree
from mathutils import Vector, noise
from pathlib import Path
from time import perf_counter

shot = Path(__file__).resolve().parents[1]
candidate = shot / "Scenes/S03_tight-accents_v026.blend"
assert not candidate.exists()
scene = bpy.context.scene
scene.frame_set(216)
camera = scene.camera
wall = bpy.data.objects["ILLUSTRATIVE CONTINUOUS WALL v009"]
mesh = wall.data
mesh.calc_loop_triangles()
vertices = [wall.matrix_world @ v.co for v in mesh.vertices]
surface = BVHTree.FromPolygons(vertices, [tuple(t.vertices) for t in mesh.loop_triangles],
                              all_triangles=True)
corners = camera.data.view_frame(scene=scene)
left, right = min(v.x for v in corners), max(v.x for v in corners)
bottom, top = min(v.y for v in corners), max(v.y for v in corners)
ray = corners[0].copy()
eye = camera.matrix_world.translation
marks = [(0.181, 0.490, 0.034, 0.165), (0.435, 0.630, 0.030, 0.135)]
hits = []
for u, v, width, depth in marks:
    ray.x, ray.y = left + (right-left)*u, bottom + (top-bottom)*v
    direction = (camera.matrix_world.to_3x3() @ ray).normalized()
    hit, _, _, _ = surface.ray_cast(eye, direction, 10)
    assert hit is not None, (u,v)
    hits.append((hit, width, depth))

inverse = wall.matrix_world.inverted()
count = 0
max_change = 0.0
for vertex, pos in zip(mesh.vertices, vertices):
    change = 0.0
    for hit, width, depth in hits:
        dx, dy, dz = pos-hit
        distance = (dx*dx+dy*dy)/width**2 + dz*dz/depth**2
        if distance < 1:
            radius = math.hypot(pos.x,pos.y)
            # Fade to the untouched wall at the edge and cap the local pull-in.
            sample = Vector((pos.x * 740, pos.y * 740, pos.z * 105))
            grain = 0.58 * noise.noise(sample) + 0.42 * noise.noise(sample * 0.51)
            strength = max(0, min(1, 0.48 + 1.6 * grain))
            change = max(change, min(0.026,max(0,radius-0.145)) * (1-distance)**1.65 * strength)
    if change > 0:
        radius = math.hypot(pos.x,pos.y)
        pos.x *= 1-change/radius
        pos.y *= 1-change/radius
        vertex.co = inverse @ pos
        max_change = max(max_change,change)
        count += 1
assert count > 100 and max_change > 0.002, (count,max_change)
mesh.update()
scene.frame_set(216)
bpy.ops.wm.save_as_mainfile(filepath=str(candidate), relative_remap=True)
bpy.ops.wm.open_mainfile(filepath=str(candidate))
scene = bpy.context.scene
assert scene.frame_end == 552
evidence = {"frame":216, "hits":[list(p) for p,_,_ in hits],
            "changed_vertices":count, "max_radial_change":max_change}
print("VERIFIED",evidence,flush=True)
(shot/"Notes/tight-accents_v026.json").write_text(json.dumps(evidence,indent=2)+"\n")
scene.render.resolution_x = 480
scene.render.resolution_y = 270
scene.render.resolution_percentage = 100
scene.eevee.taa_render_samples = 4
scene.eevee.use_raytracing = False
scene.render.use_compositing = False
scene.render.filepath = str(shot/"Previews/S03_tight-accents_v026_f0216.png")
scene.camera.data.update_tag()
bpy.context.view_layer.update()
start = perf_counter()
bpy.ops.render.render(write_still=True)
print("STILL",round(perf_counter()-start,3),flush=True)
