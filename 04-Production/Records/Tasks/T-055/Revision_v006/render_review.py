"""Budgeted review only: benchmark before a short source-speed sampled motion proof."""
import bpy, time, json, sys
from pathlib import Path
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco')
T=R/'04-Production/Records/Tasks/T-055/Revision_v006';P=T/'Previews';P.mkdir(exist_ok=True)
src=R/'04-Production/Shared/Demos/Surface_descent_demo_v002.blend'
bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False)
mode=sys.argv[-1];rows=[]
if mode=='benchmark':
    jobs=[('Descent — connected S01-S02',f,f'benchmark_{f:03d}.png') for f in [1,60,94,110,112,120,180,220,240,241,264]]
    jobs += [(n,1,n.split(' — ')[1].replace(' ','_')+'.png') for n in ['Surface — waterline','Surface — water column','World — layered descent']]
else:
    jobs=[('Descent — connected S01-S02',f,f'Frames/{i:04d}.png') for i,f in enumerate(range(1,289))]
    assert json.loads((T/'benchmark.json').read_text())['pass'], 'Benchmark first'
for scene,f,name in jobs:
    s=bpy.data.scenes[scene];bpy.context.window.scene=s;s.frame_set(f)
    s.render.image_settings.file_format='PNG';out=P/name;out.parent.mkdir(parents=True,exist_ok=True)
    s.render.filepath=str(out);start=time.perf_counter();bpy.ops.render.render(write_still=True)
    elapsed=time.perf_counter()-start
    rows.append({'scene':scene,'frame':f,'seconds':elapsed,'path':str(out.relative_to(R)),'pass':elapsed<5})
    (T/(mode+'.json')).write_text(json.dumps({'pass':all(r['pass'] for r in rows),'engine':s.render.engine,'resolution':[s.render.resolution_x,s.render.resolution_y],'aa':s.display.render_aa,'rows':rows},indent=2))
    print('BUDGET',scene,f,round(elapsed,3),flush=True)
    if elapsed>=5:raise RuntimeError('Frame exceeds strict <5 second budget; stop')
