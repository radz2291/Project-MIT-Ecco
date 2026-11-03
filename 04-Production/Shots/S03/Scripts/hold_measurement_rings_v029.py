"""Hold the established S03 comparisons as the camera passes them."""
import bpy
import json
from pathlib import Path
from time import perf_counter

shot = Path(__file__).resolve().parents[1]
candidate = shot / "Scenes/S03_held-measurements_v029.blend"
assert not candidate.exists()
scene = bpy.context.scene
camera = scene.camera

def opacity(material):
    return material.node_tree.nodes["Mix Shader"].inputs[0]

def key(socket, value, frame):
    socket.default_value = value
    socket.keyframe_insert("default_value", frame=frame)

names = ("Near Nominal","Enlarged","Tight")
for i,name in enumerate(names):
    prop = f"S03 measured reveal {i}"
    path = '["'+prop+'"]'
    # Capture the existing draw/fade-in and retain the maximum reached.
    peak = 0
    values = []
    for frame in range(1,241):
        scene.frame_set(frame)
        peak = max(peak, float(scene[prop]))
        values.append(peak)
    for frame,value in enumerate(values,1):
        scene[prop] = value
        scene.keyframe_insert(path,frame=frame)
    socket = opacity(bpy.data.materials[f"Measured ring station {i}"])
    driver = next(c.driver for c in socket.id_data.animation_data.drivers
                  if c.data_path == socket.path_from_id("default_value"))
    driver.expression = "label_reveal"
    label = bpy.data.objects["v018 " + name]
    factor = opacity(label.data.materials[0])
    for frame,value in enumerate(values,1):
        key(factor,value,frame)
    key(factor,peak,552)
    for sign in (-1,1):
        obj = bpy.data.objects[f"MEASURED {i:02d} arm {sign}"]
        for frame in (241,552):
            obj.hide_render = False
            obj.keyframe_insert("hide_render",frame=frame)

for i in range(8):
    mat = bpy.data.materials[f"Nominal ring station {i}"]
    factor = opacity(mat)
    scene.frame_set(261)
    resume = factor.default_value
    for frame in range(80,261):
        key(factor,0.82 if frame <= 247 else 0.82+(resume-0.82)*(frame-247)/14,frame)
    key(factor,resume,261)
    for sign in (-1,1):
        ring = bpy.data.objects[f"NOMINAL {i:02d} arm {sign}"]
        scene.frame_set(261)
        resume_hide = ring.hide_render
        for frame in range(80,261):
            ring.hide_render = False
            ring.keyframe_insert("hide_render",frame=frame)
        ring.hide_render = resume_hide
        ring.keyframe_insert("hide_render",frame=261)

font = bpy.data.curves.new("Nominal reference screen label","FONT")
font.body = "NOMINAL REFERENCE"
font.align_x = "CENTER"
font.align_y = "CENTER"
font.size = .020
title = bpy.data.objects.new("Nominal Reference | upper-left third",font)
scene.collection.objects.link(title)
title.parent = camera
title.location = (-.29,.178,-1)
mat = bpy.data.materials.new("Nominal reference | soft white")
mat.use_nodes = True
tree = mat.node_tree
tree.nodes.clear()
emission = tree.nodes.new("ShaderNodeEmission")
emission.inputs["Color"].default_value = (.68,.75,.82,1)
emission.inputs["Strength"].default_value = .8
transparent = tree.nodes.new("ShaderNodeBsdfTransparent")
mix = tree.nodes.new("ShaderNodeMixShader")
output = tree.nodes.new("ShaderNodeOutputMaterial")
tree.links.new(transparent.outputs[0],mix.inputs[1])
tree.links.new(emission.outputs[0],mix.inputs[2])
tree.links.new(mix.outputs[0],output.inputs["Surface"])
for frame,value in ((1,1),(244,1),(260,0),(552,0)):
    key(mix.inputs[0],value,frame)
font.materials.append(mat)
for prop,index,multiplier,shift in (("scale",0,1,""),("scale",1,1,""),
                                     ("location",0,-.29,"+36*shift/lens"),
                                     ("location",1,.178,"")):
    driver = title.driver_add(prop,index).driver
    for name,path in (("lens","lens"),("shift","shift_x")):
        var = driver.variables.new()
        var.name = name
        var.type = "SINGLE_PROP"
        var.targets[0].id_type = "CAMERA"
        var.targets[0].id = camera.data
        var.targets[0].data_path = path
    driver.expression = f"{multiplier}*32/lens{shift}"

scene.frame_set(172)
bpy.ops.wm.save_as_mainfile(filepath=str(candidate),relative_remap=True)
bpy.ops.wm.open_mainfile(filepath=str(candidate))
scene = bpy.context.scene
checks = {}
for frame in (1,72,122,172,222,241,337,432):
    scene.frame_set(frame)
    values = [opacity(bpy.data.materials[f"Measured ring station {i}"]).default_value
              for i in range(3)]
    expected = 0 if frame <= 72 else 1 if frame == 122 else 2 if frame == 172 else 3
    assert sum(v > .5 for v in values) == expected
    checks[frame] = values
(shot/"Notes/held-measurements_v029.json").write_text(json.dumps(checks,indent=2)+"\n")
scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.render.resolution_percentage = 100
scene.eevee.taa_render_samples = 8
scene.eevee.use_raytracing = False
scene.render.use_compositing = False
for frame in (1,122,172,222,337,432):
    scene.frame_set(frame)
    scene.camera.data.update_tag()
    bpy.context.view_layer.update()
    scene.render.filepath = str(shot/f"Previews/S03_held-measurements_v029_f{frame:04d}.png")
    start = perf_counter()
    bpy.ops.render.render(write_still=True)
    print("STILL",frame,round(perf_counter()-start,3),flush=True)
