import bpy,json,time,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[5];T=R/'04-Production/Records/Tasks/T-054';P=T/'Previews';F=P/'Frames-v004';F.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(T/'Consumers/S03_shared-digital_v004.blend'),load_ui=False);s=bpy.context.scene;s.render.engine='BLENDER_EEVEE';s.render.resolution_x=640;s.render.resolution_y=360;s.render.resolution_percentage=100;s.eevee.taa_render_samples=8;s.eevee.use_raytracing=False;s.render.use_compositing=False;s.render.image_settings.file_format='PNG';times=[]
def render(f,path):
 s.frame_set(f);s.render.filepath=str(path);start=time.perf_counter();bpy.ops.render.render(write_still=True);elapsed=time.perf_counter()-start;times.append({'frame':f,'seconds':elapsed});(T/'Evidence/motion-v004.json').write_text(json.dumps({'settings':'640x360 Eevee8 no raytrace/compositor; source step12 at2fps','records':times},indent=2));assert elapsed<5,'Frame cap failed'
for f in [1,120,220,288]:render(f,P/f'S03_linked-context-v004_f{f:03}.png')
frames=list(range(1,289,12))
for i,f in enumerate(frames):render(f,F/f'{i:04d}.png')
ff=R/'04-Production/Mechanisms/B201/Cache/python/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
subprocess.run([str(ff),'-y','-framerate','2','-i',str(F/'%04d.png'),'-c:v','libx264','-pix_fmt','yuv420p','-crf','20',str(P/'S03_shared-context_v004.mp4')],check=True)
print('MOTION_DONE',len(frames),max(x['seconds'] for x in times))
