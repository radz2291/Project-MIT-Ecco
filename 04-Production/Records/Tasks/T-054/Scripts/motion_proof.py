import bpy,json,time,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[5];T=R/'04-Production/Records/Tasks/T-054';P=T/'Previews';F=P/'Frames';F.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(T/'Consumers/S02_shared-reveal_v001.blend'),load_ui=False);s=bpy.context.scene;s.render.engine='BLENDER_WORKBENCH';s.render.resolution_x=640;s.render.resolution_y=360;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.use_compositing=False
times=[]
def render(f,path):
 s.frame_set(f);s.render.filepath=str(path);t=time.perf_counter();bpy.ops.render.render(write_still=True);elapsed=time.perf_counter()-t;times.append({'frame':f,'seconds':elapsed,'pass':elapsed<5});(T/'Evidence/motion-timings.json').write_text(json.dumps(times,indent=2));return elapsed<5
if not render(528,P/'S02_shared-reveal_f528_benchmark.png'):raise RuntimeError('Cap failed; no batch')
frames=list(range(440,529,4))
for i,f in enumerate(frames):
 if not render(f,F/f'{i:04d}.png'):raise RuntimeError('Cap failure; stopped batch')
ff=R/'04-Production/Mechanisms/B201/Cache/python/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
subprocess.run([str(ff),'-y','-framerate','6','-i',str(F/'%04d.png'),'-c:v','libx264','-pix_fmt','yuv420p','-crf','20',str(P/'S02_shared-reveal_motion_v001.mp4')],check=True)
print('MOTION_DONE',len(frames),max(x['seconds'] for x in times))
