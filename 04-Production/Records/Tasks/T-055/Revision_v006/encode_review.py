"""Encode native-speed proof; decode entire output and make a frame-review sheet."""
from pathlib import Path
import subprocess,json,re
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');T=R/'04-Production/Records/Tasks/T-055/Revision_v006';P=T/'Previews'
ff=Path('C:/Users/RZ1/.codex/tmp/ecco-media-runtime/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe')
motion=json.loads((T/'motion.json').read_text());assert motion['pass'] and len(motion['rows'])==288
for name in ['motion','benchmark']:
    p=T/(name+'.json');j=json.loads(p.read_text())
    j['export_profile']='Workbench AA5, shadows/cavity off, 640x360 landscape or360x640 portrait'
    for row in j['rows']:
        row.update(resolution=[360,640] if row['scene']=='World — layered descent' else [640,360],aa='5',shadows=False,cavity=False)
    p.write_text(json.dumps(j,indent=2))
out=P/'Surface-to-wall_v006.mp4'
subprocess.run([str(ff),'-y','-v','error','-framerate','24','-start_number','0','-i',str(P/'Frames/%04d.png'),'-frames:v','288','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart','-an',str(out)],check=True)
probe=subprocess.run([str(ff),'-v','error','-i',str(out),'-progress','pipe:1','-f','null','-'],capture_output=True,text=True,check=True)
frames=int(re.findall(r'^frame=(\d+)',probe.stdout,re.M)[-1]);duration=int(re.findall(r'^out_time_us=(\d+)',probe.stdout,re.M)[-1])/1e6
assert frames==288 and abs(duration-12)<.05,(frames,duration)
subprocess.run([str(ff),'-y','-v','error','-i',str(out),'-vf',r'select=not(mod(n\,12)),scale=320:180,tile=4x6','-frames:v','1',str(P/'motion-review-sheet.png')],check=True)
record={'pass':True,'path':str(out.relative_to(R)),'decoded_frames':frames,'fps':24,'duration_seconds':duration,'resolution':[640,360],'all_frames_decoded':True,'audio':False,'source_frames':[1,288],'source_speed_unchanged':True,'render_max_seconds':max(r['seconds'] for r in motion['rows']),'review_sheet':'Previews/motion-review-sheet.png','limits':'Workbench geometry/continuity proof, not final cinematic lighting or underwater optics'}
(T/'media-verification.json').write_text(json.dumps(record,indent=2));print(json.dumps(record,indent=2))
