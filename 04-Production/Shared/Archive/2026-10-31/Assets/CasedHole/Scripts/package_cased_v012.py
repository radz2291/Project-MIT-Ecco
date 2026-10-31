"""Package exact T47 selected media/hashes. No Blender/Git/network operations."""
import json,hashlib,subprocess,sys
from pathlib import Path
from PIL import Image,ImageStat
ROOT=Path(__file__).resolve().parents[5];A=ROOT/'04-Production/Shared/Assets/CasedHole';T=ROOT/'04-Production/Records/Tasks/T-047';E=T/'Evidence'
selection=json.loads((T/'release-selection_v012.json').read_text());P=ROOT/selection['preview_folder']
FF=ROOT/'04-Production/Mechanisms/B201/Cache/python/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
def rel(p):return p.relative_to(ROOT).as_posix()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,indent=2),encoding='utf8')
STILLS=[T/'Previews/v010'/n for n in ['CasedHardware_f001_v010.png','CasedChannel_f001_v010.png','CasedWearGraze_f001_v010.png','CasedRetrieval_f048_v010.png','CasedRetrieval_f096_v010.png']]+[P/n for n in ['CasedWearSection_f001_v012.png','CasedLayerSection_f001_v012.png','CasedSupport_f012_v012.png','CasedSupport_f018_v012.png','CasedSupport_f056_v012.png','CasedSupport_f076_v012.png']]
def encode():
 log=json.loads((E/'demo_v012.json').read_text());assert log['all_under_5'] and len(log['samples'])==192;out=[]
 for name in ['Retrieval','Support']:
  native=ROOT/selection['inspection'][name];frames=P/'Frames'/name;files=sorted(frames.glob('*.png'));assert len(files)==96
  samples=[r for r in log['samples'] if r['scene']==rel(native)];assert len(samples)==96 and all(r['native_sha256']==sha(native) for r in samples)
  video=P/('Cased'+name+'_v012.mp4');assert not video.exists(),video
  subprocess.run([str(FF),'-framerate','24','-i',str(frames/('Cased'+name+'_f%03d_v012.png')),'-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
  decoded=P/'Cache'/(name+'_Decoded');decoded.mkdir(parents=True,exist_ok=True)
  assert not list(decoded.glob('*.png')),'Do not replace retained media evidence'
  subprocess.run([str(FF),'-i',str(video),'-vsync','0',str(decoded/'frame_%03d.png')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
  decoded_files=sorted(decoded.glob('*.png'));assert len(decoded_files)==96
  for p in decoded_files:
   with Image.open(p) as im:assert im.size==(1280,720) and max(ImageStat.Stat(im).stddev)>1
  distinct=len({sha(p) for p in decoded_files});assert distinct>1
  out.append(dict(video=rel(video),sha256=sha(video),bytes=video.stat().st_size,source_native=rel(native),source_sha256=sha(native),fps=24,frames=96,duration_s=4,decoded_nonblank=True,distinct_decoded_frames=distinct,review='Decoded all frames; chronological selected decoded images require executor inspection. Human motion comprehension remains review.'))
 dump(E/'media-verification_v012.json',out)
def package():
 current=[ROOT/selection['master']]+[ROOT/p for p in selection['reuse']]+[ROOT/p for p in selection['inspection'].values()]
 inputs=['04-Production/Shared/Assets/BHA/BHA_film_v007.blend','04-Production/Shared/Assets/BHA/BHA_film_v006.blend','04-Production/Shared/Assets/ECCO/ECCO_film_v002.blend','04-Production/Shared/Assets/WellAssembly/World_environment_v009.blend','04-Production/Shared/Assets/Acoustics/Acoustics_v003.blend','04-Production/Shared/Assets/Acoustics/Scripts/acoustic_event_v002.py','04-Production/Shared/Assets/Acoustics/Scripts/acoustic_binding_v001.py','04-Production/Shared/Assets/Acoustics/Scripts/acoustic_verify_v002.py','04-Production/Shared/Assets/World/Scripts/continuation_controls_v001.py','04-Production/Records/Tasks/T-045/event-contract_v001.json']
 stills=[]
 for p in STILLS:
  assert p.exists(),p
  with Image.open(p) as im:assert im.size==(1280,720)
  stills.append(dict(path=rel(p),sha256=sha(p),bytes=p.stat().st_size))
 d=dict(task='T47',task_id='de4e8339-fbdd-4c40-9f30-bf61302ed04e',base_commit=selection['base_commit'],status='candidate_for_master_checks_integration_and_Radzi_review',units='metres',axis='common T44 +X downhole; retrieval toward negativeX',master=selection['master'],current_native_candidates=[dict(path=rel(p),sha256=sha(p),bytes=p.stat().st_size) for p in current],inputs=[dict(path=p,sha256=sha(ROOT/p)) for p in inputs],event_export=dict(path=selection['events'],sha256=sha(ROOT/selection['events'])),consumer_map={'S04-A':'Later upward retrieval/context','S04-B':'Qualitative support and actual cap/steel acoustic response','S04-C':'Static localized exterior channel','S04-D':'Pre-existing inner wear/registered nominal contour'},controls=['cutaway','show_steel','show_cement','show_channel','show_reference','wear','channel'],layer_truth_table_states=128,bounds_control_policy='Linked geometry bounds/4mm authored wear are master-owned; local numeric bounds metadata is informational. Republish versioned master for dimension edits.',geometry=dict(casing_interval_x_m=[-5.5,0],nominal_inner_radius_m=.1589405,outer_radius_m=.1698625,cement_outer_radius_m=.22225,channel_interval_x_m=[-2.5,-.4],channel_azimuth_rad=[.3,.8],authored_preexisting_wear_max_m=.004),selected_review_stills=stills,response=dict(short_lifetime_s=.45,long_lifetime_s=1.20,representation='Compact screen lanes only; legacy24worldbars removed; contactcup/patch consumer0.35; shared acoustic fronts unchanged'),limits=['No calibrated acoustics, quantified bond/thickness result or chemistry classification','No actual V3 movie shots, narration or film assembly','Native/video/raw/cache local ignored, no remote upload or off-machine backup claimed','Normal GPU-cache tests do not establish empty-cache compliance; prior T44 12.55â€“25.13s initialization unresolved','Generic full-BVH nearest3.4035mm discrepancy retained alongside passing actual ray/native face plane+bounds','Human appearance/comprehension, engineering/client interpretation and final acceptance pending'])
 media=E/'media-verification_v012.json';assert media.exists(),'Playable demo package required';d['playable_media']=json.loads(media.read_text())
 for name in ['benchmark-all_v010.json','benchmark-repaired_v012.json','demo_v012.json']:
  p=E/name;assert p.exists();d.setdefault('render_evidence',[]).append(dict(path=rel(p),sha256=sha(p)))
 dump(A/'manifest_v002.json',d)
 all_native=list(A.glob('*.blend'))+list((T/'Scenes').glob('*.blend'))
 dump(E/'retained-native-hashes_v012.json',[dict(path=rel(p),sha256=sha(p),bytes=p.stat().st_size) for p in sorted(all_native)])
 allowed=[p for root in [A,T] for p in root.rglob('*') if p.is_file() and p.suffix in ['.py','.md','.json'] and '__pycache__' not in str(p) and '/Cache/' not in p.as_posix() and '/Frames/' not in p.as_posix()]+STILLS+[T/'Previews/v001/CasedReuse_B_f001_v002.png']
 paths=sorted({rel(p) for p in allowed}|{rel(E/'tracked-files_v012.json')})
 dump(E/'tracked-files_v012.json',dict(integrator='T45 only',paths=paths,excluded='All native/video/raw/cache and unrelated/global files. No force-add. Historical scripts/evidence remain explicitly versioned.'))
if len(sys.argv)>1 and sys.argv[1]=='encode':encode()
package();print('T47_PACKAGE12_COMPLETE')
