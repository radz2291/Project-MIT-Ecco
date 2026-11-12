import bpy,sys,json
from pathlib import Path
from mathutils import Vector
wave,out,notes=map(Path,sys.argv[sys.argv.index("--")+1:])
sys.path.insert(0,str(wave.resolve()/"Scripts"))
from pulse_asset_api import get_input,set_input,arrival_readouts
s=bpy.context.scene
results=[]
for name,f in (("Supported",82),("Reduced support",194)):
    o=s.objects[name+" | shared v021 waveform"]
    m=o.modifiers[0]
    axis=Vector(get_input(m,"Route axis"))
    up=Vector(get_input(m,"Up axis"))
    gap=get_input(m,"Gap length m")
    start=get_input(m,"Start frame")
    def peak(advance):
        set_input(m,"Start frame",start-advance)
        s.frame_set(f)
        e=o.evaluated_get(bpy.context.evaluated_depsgraph_get())
        mesh=e.to_mesh()
        try:
            c=mesh.attributes["wf17_component"].data
            send=[v.co.copy() for v in mesh.vertices if c[v.index].value==1]
            if not send:return 0.,0.
            p=max(send,key=lambda p:abs(p.dot(up)))
            return p.dot(axis)/gap,abs(p.dot(up))
        finally:e.to_mesh_clear()
    before=peak(0)
    trials=[(i/4,*peak(i/4)) for i in range(1,25)]
    valid=[t for t in trials if t[1]>=.975 and t[2]>=before[1]*.34]
    assert valid,(name,before,trials)
    advance,u,amp=valid[0]
    peak(advance)
    set_input(m,"Reflection delay",get_input(m,"Reflection delay")+advance*get_input(m,"Speed"))
    s.frame_set(f)
    results.append(dict(case=name,glitch=f,advance_frames=advance,old_crest_fraction=before[0],new_crest_fraction=u,crest_height_m=amp,readouts=arrival_readouts(o,s)))
s.frame_set(82)
s.render.filepath="//../Cache/v042/S04_"
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(out.resolve()),compress=True)
notes.write_text(json.dumps(results,indent=2)+"\n")
print("CREST_SYNC",results,flush=True)
