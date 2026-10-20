import bpy,sys,json,time,subprocess,shutil
from pathlib import Path
R=Path(__file__).resolve().parents[1];s=bpy.context.scene;bpy.context.window.scene=s;args=sys.argv[sys.argv.index('--')+1:];start,end=map(int,args);ff=R.parents[2]/'04-Production/Mechanisms/B201/Cache/python/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe';chunk=R/f'Work/chunk_{start:04d}_{end:04d}.mp4';tmp=R/'Work/current-frame.png';rows=[]
(R/'Previews/Stills').mkdir(parents=True,exist_ok=True)
assert shutil.disk_usage(R).free>20*1024*1024,'Insufficient space for safe chunk rendering'
log=(R/f'Records/encoder_{start:04d}.log').open('w');proc=subprocess.Popen([str(ff),'-y','-f','image2pipe','-vcodec','png','-r','24','-i','pipe:0','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(chunk)],stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=log)
try:
 for f in range(start,end+1):
  s.frame_set(f);s.camera.data.update_tag();bpy.context.view_layer.update();bpy.context.evaluated_depsgraph_get().update();s.render.filepath=str(tmp);t=time.perf_counter();bpy.ops.render.render(scene=s.name,write_still=True);dt=time.perf_counter()-t;assert dt<5,(f,dt);data=tmp.read_bytes();assert data[:8]==b'\x89PNG\r\n\x1a\n';proc.stdin.write(data);proc.stdin.flush();rows.append({'frame':f,'seconds':dt})
  if f in [72,132,172,216,228,240,241,264,288,336,384,432]:shutil.copy2(tmp,R/f'Previews/Stills/S03_v036_{f:04d}.png')
  (R/f'Records/timings_{start:04d}.json').write_text(json.dumps(rows,indent=2))
 proc.stdin.close();assert proc.wait(timeout=90)==0
except:
 proc.kill();proc.wait();raise
finally:log.close()
