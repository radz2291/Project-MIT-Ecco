"""Shape the single connected shared return into a smoothly decaying ring-down."""
import json,sys
from pathlib import Path
from mathutils import Vector
import bpy
wave,out,record=[Path(x).resolve() for x in sys.argv[sys.argv.index("--")+1:]]
sys.path.insert(0,str(wave/"Scripts"))
from pulse_asset_api import set_input,get_input,arrival_readouts
s=bpy.context.scene
o=s.objects["Reduced support | shared v021 waveform"]
m=o.modifiers[0]
def sample(frame):
    s.frame_set(frame)
    e=o.evaluated_get(bpy.context.evaluated_depsgraph_get())
    mesh=e.to_mesh()
    try:
        return [(tuple(v.co),mesh.attributes["wf17_component"].data[v.index].value)
                for v in mesh.vertices] if mesh.vertices else []
    finally:e.to_mesh_clear()
before={f:sample(f) for f in (188,191,194,197,201)}
style=json.loads((wave/"Approved_beam_exchange_v001.json").read_text())["style"]
for key,value in style.items():
    set_input(m,key,value)
set_input(m,"Use master style",False)
set_input(m,"Return train scale",3.2)
for name,value in {"Flat after age":0.0,"Pulse width":.78,"Ringing":.45,
                   "Ring period":1.8,"Ring decay":3.2}.items():
    socket=next(x for x in m.node_group.interface.items_tree if x.name==name and x.in_out=="INPUT")
    prop=getattr(m.properties.inputs,socket.identifier)
    path=prop.path_from_id("value")
    driver=o.driver_add(path).driver
    driver.expression=f"{value} if frame >= 201.5 else {style[name]}"
    s.frame_set(202)
    assert abs(get_input(m,name)-value)<1e-6,(name,path,get_input(m,name))
for f,pts in before.items():
    after=sample(f)
    assert len(pts)==len(after) and all(a[1]==b[1] and (Vector(a[0])-Vector(b[0])).length<1e-6 for a,b in zip(pts,after)),f
s.frame_set(220)
readout=arrival_readouts(o,s)
assert abs(readout["Return start"]-201.5)<1e-4 and readout["Return tail arrival"]<261
assert abs(readout["Send head arrival"]-191.25)<1e-4
assert all(set(c for _,c in sample(f))=={2} for f in (207,214,220,225))
s.frame_set(220)
s.render.filepath="//../Cache/v045/S04_"
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True)
bpy.ops.wm.open_mainfile(filepath=str(out),use_scripts=False)
assert all(Path(bpy.path.abspath(l.filepath)).is_file() for l in bpy.data.libraries)
record.write_text(json.dumps({"return":readout,"unchanged_send_samples":list(before),
 "impact_frames":[82,194],"ring_amplitude":.45,"ring_period":1.8,"ring_decay":3.2,
 "source":"v043 single linked waveform with shot-local reduced-support return shape"},indent=2)+"\n")
print("V045_READY",readout,flush=True)
