"""Restore explicit pre-exit visibility for the three borehole labels."""
import bpy
import json
from pathlib import Path
from time import perf_counter

shot = Path(__file__).resolve().parents[1]
candidate = shot / "Scenes/S03_restored-interior-labels_v040.blend"
assert not candidate.exists()
scene = bpy.context.scene
names = ("v018 Near Nominal","v018 Enlarged","v018 Tight")
for name in names:
    label = bpy.data.objects[name]
    for frame,hidden in ((1,False),(253,False),(254,True)):
        label.hide_render = label.hide_viewport = hidden
        label.keyframe_insert("hide_render",frame=frame)
        label.keyframe_insert("hide_viewport",frame=frame)
scene.frame_set(122)
bpy.ops.wm.save_as_mainfile(filepath=str(candidate),relative_remap=True)
bpy.ops.wm.open_mainfile(filepath=str(candidate))
scene = bpy.context.scene
checks = {}
for frame,i in ((122,0),(172,1),(222,2)):
    scene.frame_set(frame)
    label = bpy.data.objects[names[i]]
    opacity = label.data.materials[0].node_tree.nodes["Mix Shader"].inputs[0].default_value
    assert not label.hide_render and not label.hide_viewport and opacity > .95
    for sign in (-1,1):
        assert not bpy.data.objects[f"MEASURED {i:02d} arm {sign}"].hide_render
    checks[frame] = {"label":names[i],"opacity":opacity}
scene.frame_set(254)
assert all(bpy.data.objects[n].hide_render for n in names)
(shot/"Notes/restored-interior-labels_v040.json").write_text(json.dumps(checks,indent=2)+"\n")
scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.render.resolution_percentage = 100
scene.eevee.taa_render_samples = 8
scene.eevee.use_raytracing = False
scene.render.use_compositing = False
for frame in (122,172,222):
    scene.frame_set(frame)
    scene.camera.data.update_tag()
    bpy.context.view_layer.update()
    scene.render.filepath = str(shot/f"Previews/S03_restored-interior-labels_v040_f{frame:04d}.png")
    start = perf_counter()
    bpy.ops.render.render(write_still=True)
    print("STILL",frame,round(perf_counter()-start,3),flush=True)
