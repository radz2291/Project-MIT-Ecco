"""Express reduced support as multiple diminishing returns on the shared route."""
import json
from pathlib import Path
import sys
import bpy

wave, out, notes = [Path(x).resolve() for x in sys.argv[sys.argv.index("--")+1:]]
sys.path.insert(0,str(wave/"Scripts"))
from pulse_asset_api import duplicate_instance, set_input, get_input, arrival_readouts
s=bpy.context.scene
field=s.objects["Reduced support | shared v021 waveform"]
base=field.modifiers[0]
set_input(base,"Return train scale",1.0)
collection=field.users_collection[0]
results=[]
for i,(start,ratio) in enumerate(((213,.65),(224,.43),(235,.28)),1):
    tail=duplicate_instance(field,collection,f"Reduced support | fading echo {i}",{
        "Start frame":float(start), "Mode 0 Both 1 Send 2 Return":2,
        "Beam mode":False, "Return train scale":.67,
        "Strength multiplier":get_input(base,"Strength multiplier")*ratio,
    })
    s.frame_set(start+5)
    values=arrival_readouts(tail,s)
    assert values and values["Return tail arrival"]<261,(tail.name,values)
    assert abs(values["Return start"]-start)<.001,values
    e=tail.evaluated_get(bpy.context.evaluated_depsgraph_get())
    mesh=e.to_mesh()
    try:
        components={x.value for x in mesh.attributes["wf17_component"].data}
        assert components=={2},components
    finally:
        e.to_mesh_clear()
    results.append({"echo":i,"relative_amplitude":ratio,**values})
s.frame_set(194)
s.render.filepath="//../Cache/v044/S04_"
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True)
bpy.ops.wm.open_mainfile(filepath=str(out),use_scripts=False)
assert all(Path(bpy.path.abspath(l.filepath)).is_file() for l in bpy.data.libraries)
notes.write_text(json.dumps({"extra_returns":results,"unchanged_glitch_frames":[82,194],
 "interpretation":"Progressively weaker return packets illustrate longer casing ring-down."},indent=2)+"\n")
print("V044_READY",results,flush=True)
