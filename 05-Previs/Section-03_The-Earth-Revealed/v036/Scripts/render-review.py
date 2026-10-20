import subprocess,json,time,statistics,shutil
from pathlib import Path
R=Path(__file__).resolve().parents[1];blender=Path(r'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe');ff=R.parents[2]/'04-Production/Mechanisms/B201/Cache/python/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe';begin=time.perf_counter();rows=[];chunks=[]
previous_elapsed=json.loads((R/'Records/Render-progress.json').read_text())['elapsed_seconds'] if (R/'Records/Render-progress.json').exists() else 0
for start,end in [(1,120),(121,240),(241,336),(337,432)]:
 chunk=R/f'Work/chunk_{start:04d}_{end:04d}.mp4';record=R/f'Records/timings_{start:04d}.json';valid=chunk.exists() and record.exists() and len(json.loads(record.read_text()))==end-start+1
 if valid:
  probe=subprocess.run([str(ff),'-v','error','-i',str(chunk),'-progress','pipe:1','-f','null','-'],capture_output=True,text=True);valid=probe.returncode==0 and ('frame=%d'%(end-start+1)) in probe.stdout
 if not valid:
  log=(R/f'Records/render_{start:04d}.log').open('w');p=subprocess.run([str(blender),'-b',str(R/'Scenes/S03_second-last-nominal-label_v036.blend'),'-t','4','--python-exit-code','1','--python',str(R/'Scripts/render-chunk.py'),'--',str(start),str(end)],stdout=log,stderr=subprocess.STDOUT);log.close();assert p.returncode==0,('Render block failed',start)
 chunk=R/f'Work/chunk_{start:04d}_{end:04d}.mp4';chunks.append(chunk);current=json.loads((R/f'Records/timings_{start:04d}.json').read_text());rows.extend(current)
 if start==1:shutil.copy2(chunk,R/'Previews/S03_v036_opening-test_5s.mp4')
 (R/'Records/Render-progress.json').write_text(json.dumps({'frames':end,'total':432,'elapsed_seconds':previous_elapsed+time.perf_counter()-begin,'opening_ready':True},indent=2));print('FINISHED_BLOCK',start,end,flush=True)
manifest=R/'Work/concat.txt';manifest.write_text(''.join("file '%s'\n"%p.name for p in chunks));video=R/'Previews/S03_v036_final_24fps.mp4'
p=subprocess.run([str(ff),'-y','-f','concat','-safe','0','-i',str(manifest),'-c','copy','-movflags','+faststart',str(video)],capture_output=True,text=True);(R/'Records/Concat.log').write_text(p.stderr);assert p.returncode==0
p=subprocess.run([str(ff),'-v','error','-i',str(video),'-progress','pipe:1','-f','null','-'],capture_output=True,text=True);(R/'Records/Decode.log').write_text(p.stdout+p.stderr);assert p.returncode==0 and 'frame=432' in p.stdout
report={'frames':432,'fps':24,'duration_seconds':18,'resolution':[960,540],'samples':4,'total_wall_seconds':previous_elapsed+time.perf_counter()-begin,'render_seconds':sum(x['seconds'] for x in rows),'mean_seconds_per_frame':statistics.mean(x['seconds'] for x in rows),'maximum_seconds_per_frame':max(x['seconds'] for x in rows),'all_frames_below5_seconds':all(x['seconds']<5 for x in rows),'video_decode_verified':True}
(R/'Records/Render-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
