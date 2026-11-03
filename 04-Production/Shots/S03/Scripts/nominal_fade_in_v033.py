"""Ease the entrance title in while preserving its existing exit timing."""
import bpy
from pathlib import Path

shot = Path(__file__).resolve().parents[1]
candidate = shot / "Scenes/S03_nominal-fade-in_v033.blend"
assert not candidate.exists()
name = "Nominal Reference | upper-left third"

def opacity():
    tree = bpy.data.objects[name].data.materials[0].node_tree
    return next(n for n in tree.nodes if n.type == "MIX_SHADER").inputs[0]

factor = opacity()
for frame, value in ((1, 0), (15, 1)):
    factor.default_value = value
    factor.keyframe_insert("default_value", frame=frame)
bpy.context.scene.frame_set(15)
bpy.ops.wm.save_as_mainfile(filepath=str(candidate), relative_remap=True)
bpy.ops.wm.open_mainfile(filepath=str(candidate))
scene = bpy.context.scene
factor = opacity()
for frame, value in ((1, 0), (15, 1), (49, 1), (78, 0), (172, 0)):
    scene.frame_set(frame)
    assert abs(factor.default_value - value) < 1e-6
for frame in (8, 64):
    scene.frame_set(frame)
    assert 0 < factor.default_value < 1
print("VERIFIED nominal title fade in and out")
