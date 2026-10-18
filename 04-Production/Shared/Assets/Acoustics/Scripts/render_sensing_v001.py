"""Run only with an explicit T45 render-queue grant."""
import bpy,sys,json,time,platform
from pathlib import Path
import gpu
ROOT=Path(__file__).resolve().parents[5];T=ROOT/'04-Production/Records/Tasks/T-046';E=T/'Evidence';P=T/'Previews'
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
mode=args[0];kind=args[1] if len(args)>1 else 'A'
path=T/f'Scenes/Sensing_reuse_{kind}_v008.blend';bpy.ops.wm.open_mainfile(filepath=str(path),load_ui=False,use_scripts=False);s=bpy.context.scene
frames=[1,17,23,31,40,96] if mode=='benchmark' and kind=='A' else [23,29,38,108] if mode=='benchmark' else list(range(1,s.frame_end+1))
if mode=='sample':frames=[17,23,31]
folder=P/('Benchmark_v008_'+kind if mode=='benchmark' else 'Sample_v008_'+kind if mode=='sample' else 'Frames_'+kind);folder.mkdir(parents=True,exist_ok=True)
log=dict(scene=str(path.relative_to(ROOT)).replace('\\','/'),kind=mode,backend='VULKAN requested by command',hardware=[platform.platform()],engine=s.render.engine,resolution=[s.render.resolution_x,s.render.resolution_y],fps=s.render.fps,samples=s.eevee.taa_render_samples,color_management=[s.view_settings.view_transform,s.view_settings.look],compositor=s.render.use_compositing,cache='Normal pre-existing GPU driver disk caches; no warmup render, first render in this process labelled first_process. Empty-cache 12.55–25.13s T44 limitation unresolved.',measurement='wall clock complete bpy.ops.render.render(write_still=True), initialization/write included, process/file loading excluded',frames=[])
logpath=E/f'{mode}_{kind}_v008.json'
if mode=='batch':
 prev=json.loads((E/f'benchmark_{kind}_v008.json').read_text());assert prev['all_under_5'],'Benchmark must pass before batch'
for i,f in enumerate(frames):
 s.frame_set(f);s.render.filepath=str(folder/f'f{f:04d}.png');start=time.perf_counter();bpy.ops.render.render(write_still=True);elapsed=time.perf_counter()-start
 log['backend']=gpu.platform.backend_type_get();log['hardware']=[platform.platform(),gpu.platform.vendor_get(),gpu.platform.renderer_get(),gpu.platform.version_get()]
 row=dict(frame=f,seconds=elapsed,under_5=elapsed<5,first_process=i==0,path=str(Path(s.render.filepath).relative_to(ROOT)).replace('\\','/'));log['frames'].append(row);log['all_under_5']=all(r['under_5'] for r in log['frames']);logpath.write_text(json.dumps(log,indent=2));print('SENSING_RENDER',kind,f,elapsed,elapsed<5,flush=True)
 if elapsed>=5:raise RuntimeError('Strict 5s cap failed; stop before batch/remaining frames and retain evidence')


