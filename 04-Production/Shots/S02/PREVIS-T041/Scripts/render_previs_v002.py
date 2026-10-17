"""Reopen saved T41 candidate; render selected QA frames or all 288 cheap frames."""
import bpy,json,time,sys
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];E=BASE.parents[2]/'Records/Tasks/T-041/Evidence'
scene=BASE/'Scenes/S02_previs_T041_v002.blend'
bpy.ops.wm.open_mainfile(filepath=str(scene));s=bpy.context.scene
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
frames=range(1,289) if 'all' in args else [1,22,32,92,103,130,157,169,210,242,266,288]
folder=BASE/'Previews/v002/Frames';folder.mkdir(parents=True,exist_ok=True)
times=[]
for f in frames:
    path=folder/f'frame_{f:04d}.png'
    if path.exists():continue
    s.frame_set(f);s.render.filepath=str(path);t=time.perf_counter();bpy.ops.render.render(write_still=True)
    times.append(dict(frame=f,seconds=round(time.perf_counter()-t,3)))
    (E/('render_all_v002.json' if 'all' in args else 'render_selected_v002.json')).write_text(json.dumps(times,indent=2))
print('T41_RENDER_DONE',len(times))
