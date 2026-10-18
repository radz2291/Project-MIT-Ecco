"""Explicit T45 render slot required. Complete render-to-written-frame timing."""
import bpy,sys,json,time,platform
from pathlib import Path
import gpu
ROOT=Path(__file__).resolve().parents[5];T=ROOT/'04-Production/Records/Tasks/T-046';E=T/'Evidence';P=T/'Previews'
args=sys.argv[sys.argv.index('--')+1:];mode=args[0];kind=args[1];version=args[2] if len(args)>2 else 'v009';scene=T/f'Scenes/Sensing_reuse_{kind}_{version}.blend'
bpy.ops.wm.open_mainfile(filepath=str(scene),load_ui=False,use_scripts=False);s=bpy.context.scene
frames=[17,23,31] if mode=='sample' else [1,25,40,65,96] if mode=='benchmark' and kind=='A' else [23,29,31,73,108] if mode=='benchmark' else list(range(s.frame_start,s.frame_end+1))
folder=P/'Frames'/f'{mode}_{kind}_{version}';folder.mkdir(parents=True,exist_ok=True)
if mode=='batch':assert json.loads((E/f'benchmark_{kind}_{version}.json').read_text())['all_under_5']
log=dict(scene=scene.relative_to(ROOT).as_posix(),scene_sha256=__import__('hashlib').sha256(scene.read_bytes()).hexdigest(),mode=mode,resolution=[s.render.resolution_x,s.render.resolution_y],fps=s.render.fps,engine=s.render.engine,samples=s.eevee.taa_render_samples,color_management=[s.view_settings.view_transform,s.view_settings.look],compositor=s.render.use_compositing,cache='Normal existing GPU disk caches; no warmup render. First-process is first full render-to-file in fresh process, not empty-cache machine. T44 empty-cache12.55–25.13s remains unresolved.',measurement='wall-clock around complete bpy.ops.render.render(write_still=True); includes initialization/compositor if enabled/write, excludes process/file loading',frames=[])
for i,f in enumerate(frames):
 s.frame_set(f);s.render.filepath=str(folder/f'f{f:04d}.png');start=time.perf_counter();bpy.ops.render.render(write_still=True);seconds=time.perf_counter()-start
 log['backend']=gpu.platform.backend_type_get();log['hardware']=[platform.platform(),gpu.platform.vendor_get(),gpu.platform.renderer_get(),gpu.platform.version_get()];log['frames'].append(dict(frame=f,seconds=seconds,under_5=seconds<5,first_process=i==0,path=Path(s.render.filepath).relative_to(ROOT).as_posix()));log['all_under_5']=all(r['under_5'] for r in log['frames']);(E/f'{mode}_{kind}_{version}.json').write_text(json.dumps(log,indent=2));print('SENSING_RENDER',version,kind,f,round(seconds,4),seconds<5,flush=True)
 if seconds>=5:raise RuntimeError('Strict5s cap failed; retain evidence and stop')
