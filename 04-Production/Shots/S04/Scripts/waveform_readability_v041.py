"""Improve waveform legibility while preserving the original impact tiles."""
import json
from pathlib import Path
import sys
import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

wave, output, record = [Path(p).resolve() for p in sys.argv[sys.argv.index("--")+1:]]
sys.path.insert(0, str(wave / "Scripts"))
from pulse_asset_api import arrival_readouts, get_input, set_input
s = bpy.context.scene
events = []
for name, frame, return_scale in (
    ("Supported", 82, 1.0), ("Reduced support", 194, 1.65),
):
    s.frame_set(frame)
    field = s.objects[name + " | shared v021 waveform"]
    mod = field.modifiers[0]
    axis = Vector(get_input(mod, "Route axis")).normalized()
    origin = field.location.copy()
    midpoint = origin + axis * get_input(mod, "Gap length m") / 2
    toward_camera = (s.camera.matrix_world.translation - midpoint).normalized()
    amplitude = axis.cross(toward_camera).normalized()
    right = s.camera.matrix_world.to_quaternion() @ Vector((1, 0, 0))
    if amplitude.dot(right) < 0:
        amplitude.negate()
    previous_up = Vector(get_input(mod, "Up axis"))
    previous_span = abs(previous_up.dot(amplitude))
    for key, value in {
        "Up axis": tuple(amplitude), "Transverse axis": tuple(axis.cross(amplitude)),
        "Strength multiplier": 2.1, "Radius multiplier": 1.45,
        "Return train scale": return_scale,
    }.items():
        set_input(mod, key, value)
    s.frame_set(frame)
    actual = arrival_readouts(field, s)
    assert abs(actual["Send head arrival"] - frame) < 0.001
    assert actual["Return tail arrival"] < (141 if frame == 82 else 261)
    events.append({"case": name, "impact_frame": frame, "readouts": actual,
                   "previous_amplitude_projection_factor": previous_span,
                   "amplitude_multiplier": 2.1, "line_radius_multiplier": 1.45,
                   "return_train_scale": return_scale})
tails = [obj for obj in s.objects if obj.name.startswith("Casing response tail")]
assert len(tails) == 5
for obj in tails:
    obj.animation_data_clear()
    obj.hide_render = obj.hide_viewport = True
s.frame_set(82)
s.render.filepath = "//../Cache/v041/S04_"
bpy.context.preferences.filepaths.save_version = 0
bpy.ops.wm.save_as_mainfile(filepath=str(output), compress=True)
bpy.ops.wm.open_mainfile(filepath=str(output), use_scripts=False)
assert all(Path(bpy.path.abspath(l.filepath)).is_file() for l in bpy.data.libraries)
assert all(o.hide_render for o in bpy.context.scene.objects if o.name.startswith("Casing response tail"))
record.write_text(json.dumps({"events": events, "legacy_tail_curves_hidden": 5,
 "intent": "Longer illustrative reduced-support ring-down in the same violet return. Existing steel impact and tiles retain their animation."}, indent=2)+"\n")
print("V041_READY", events, flush=True)
