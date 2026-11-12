from pathlib import Path
import hashlib,json,os,re,sys
from time import perf_counter
import bpy
native=Path(bpy.data.filepath)
base=native.parent.parent
cache=base/"Cache"
old=cache/"v040/full-vulkan-75"
proof=cache/"v042"
out=proof/"Full"
out.mkdir(exist_ok=True)
state=json.loads((old/"timings.json").read_text())
state["settings"]["native_sha256"]=hashlib.sha256(native.read_bytes()).hexdigest()
state["reused_from"]="v040"
if "--finish-tail" in sys.argv:state=json.loads((out/"timings.json").read_text())
log=Path(sys.argv[-1]).read_text(encoding="utf-8-sig",errors="replace")
times={int(f):float(t) for f,t in re.findall(r"(?m)^FRAME (\d+) ([\d.]+)",log)}
assert len(times)==69
s=bpy.context.scene
s.render.resolution_percentage=75
assert (s.frame_start,s.frame_end,s.render.fps)==(1,432,24)
s.frame_set(82)
t=perf_counter()
bpy.ops.render.render()
state["setup_attempts"].append({"82_v042":perf_counter()-t})
for f in (229,230) if "--finish-tail" in sys.argv else range(1,433):
    name=f"S04_{f:04d}.png"
    dest=out/name
    if 64<=f<=112 or 176<=f<=230:
        if f in times:
            if not dest.exists():os.link(proof/name,dest)
            dt=times[f]
        else:
            if dest.exists() and os.path.samefile(old/name,dest):
                dest.unlink()
            s.frame_set(f)
            s.render.filepath=str(dest)
            t=perf_counter()
            bpy.ops.render.render(write_still=True)
            dt=perf_counter()-t
        assert dt<5,(f,dt)
        state["frames"][str(f)]=dt
    elif not dest.exists():os.link(old/name,dest)
assert len(list(out.glob("S04_*.png")))==432
(out/"timings.json").write_text(json.dumps(state,indent=2)+"\n")
