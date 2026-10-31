"""Package completed queued renders and preserved exact native/source evidence."""
import json,hashlib,subprocess,re,shutil
from pathlib import Path
from PIL import Image,ImageStat,ImageChops,ImageDraw
ROOT=Path(__file__).resolve().parents[5];A=ROOT/'04-Production/Shared/Assets/Acoustics';T=ROOT/'04-Production/Records/Tasks/T-046';E=T/'Evidence';P=T/'Previews'
FF=ROOT/'04-Production/Mechanisms/B201/Cache/python/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.relative_to(ROOT).as_posix()
def item(p,kind):return dict(path=rel(p),sha256=sha(p),bytes=p.stat().st_size,storage=kind)
def dump(p,d):p.write_text(json.dumps(d,indent=2),encoding='utf-8')
assert (P/'Frames/batch_A_v009/f0096.png').exists()
video=P/'Sensing_behavior_v002.mp4'
if not video.exists():subprocess.run([str(FF),'-v','error','-framerate','24','-i',str(P/'Frames/batch_A_v009/f%04d.png'),'-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],check=True)
decoded=P/'Frames/Decoded_v002';decoded.mkdir(parents=True,exist_ok=True);subprocess.run([str(FF),'-v','error','-y','-i',str(video),str(decoded/'f%04d.png')],check=True)
subprocess.run([str(FF),'-v','error','-i',str(video),'-f','null','-'],check=True)
images=sorted(decoded.glob('f*.png'));distinct=[];deltas=[];valid=[]
for i,p in enumerate(images):
 im=Image.open(p).convert('RGB');valid.append(im.size==(1280,720) and max(ImageStat.Stat(im).stddev)>3);distinct.append(sha(p))
 if i:deltas.append(sum(ImageStat.Stat(ImageChops.difference(Image.open(images[i-1]).convert('RGB'),im)).mean))
selected={"send":P/'Frames/batch_A_v009/f0017.png',"contact":P/'Frames/batch_A_v009/f0023.png',"return":P/'Frames/batch_A_v009/f0031.png',"arrival_cue":P/'Frames/batch_A_v009/f0040.png',"reuse_B":P/'Frames/benchmark_B_v010/f0029.png'}
for label,p in selected.items():shutil.copyfile(p,P/f'Review_{label}_v002.png')
frames=[1,10,14,17,21,23,25,28,31,35,40,47,53,57,61,65,69,73,77,81,88,92,95,96];sheet=Image.new('RGB',(1280,1200),(14,18,21));draw=ImageDraw.Draw(sheet)
for i,f in enumerate(frames):
 im=Image.open(decoded/f'f{f:04d}.png');im.thumbnail((320,180));x=i%4*320;y=i//4*200;sheet.paste(im,(x,y));draw.text((x+4,y+181),f'{f} / {(f-1)/24:.2f}s',fill='white')
sheet.save(P/'Frames/motion-inspection_v002.jpg',quality=92)
media=dict(video=item(video,'local-video'),decoded_frames=len(images),fps=24,duration_s=len(images)/24,resolution=[1280,720],decode_without_errors=True,all_frames_nonblank_size=all(valid),distinct_decoded_frame_hashes=len(set(distinct)),successive_frame_rgb_delta=dict(min=min(deltas),max=max(deltas),moving_transitions=sum(d>.05 for d in deltas)),inspection_sheet=rel(P/'Frames/motion-inspection_v002.jpg'),scope='Decoded full local MP4 and selected chronological image inspection. Human narrated comprehension/engineering acceptance not inferred.')
dump(E/'media-verification_v002.json',media)
native=[A/'Acoustics_v003.blend',T/'Scenes/Sensing_reuse_A_v009.blend',T/'Scenes/Sensing_reuse_B_v010.blend'];sources=[ROOT/'04-Production/Shared/Assets/BHA/BHA_film_v007.blend',ROOT/'04-Production/Shared/Assets/BHA/BHA_film_v006.blend',ROOT/'04-Production/Shared/Assets/ECCO/ECCO_film_v002.blend',ROOT/'04-Production/Shared/Assets/WellAssembly/World_environment_v009.blend']
manifest=dict(task='T46',ticket_id='41cb52bd-780a-4fc2-9b2f-df2728b3aba4',version='v002',status='candidate_waiting_master_remote_integration_and_independent_verdict',accepted_upstream_commit='a08d0ecfbd6f3241298f506b3ea42613388b3baf',current_master=rel(native[0]),current_consumers=[rel(p) for p in native[1:]],top_collection='ACOUSTICS_MASTER',units='metres_seconds',axes='T44 unscaled world+X longitudinal; acoustic local+Z propagation/normal',artifacts=[*[item(p,'local-native') for p in native],item(video,'local-video'),*[item(P/f'Review_{label}_v002.png','selected-tracked-still') for label in selected]],sources=[item(p,'unchanged-accepted-native-source') for p in sources],event_exports=[item(E/f'events_{kind}_v003.json','portable-event-json') for kind in ['A','B']],event_interface=rel(A/'event-interface_v002.json'),consumer_ids=['S02-A','S02-B','S02-C','S04-B','S04-D'],native_verification=rel(E/'native-verification_v010.json'),finite_continuation_visibility=rel(E/'extension-visibility_v010.json'),media_verification=rel(E/'media-verification_v002.json'),benchmarks=[rel(E/'benchmark_A_v009.json'),rel(E/'benchmark_B_v010.json'),rel(E/'batch_A_v009.json')],timing='Leading-front common times;3fronts lag0/.07/.14s; hold actual cap throughreceive_s+.14; all per-front intervals exported.',native_backup='All .blend/video/raw frames/cache local Git-ignored; no media upload or off-machine backup claimed.',limits=['Illustrative acoustic timing/graphics; no calibrated speed/firing cadence or field measurements','Native temporary-cap emission exit is source-derived but provisional, not certified transducer datum','Source2.400m geometry/reference plane/120degrees retained; no mud-sensor coordinate invented','No reconstruction/A-OUTPUT/actual film shot/narration/editing/client contact','Normal-cache render cap only; T44 empty-cache initialization12.55–25.13s remains unresolved','Executor checks/visual inspection do not establish human comprehension, engineering approval or client acceptance'])
dump(A/'manifest_v002.json',manifest);print(json.dumps(dict(media=media,native=[item(p,'local-native') for p in native]),indent=2))
