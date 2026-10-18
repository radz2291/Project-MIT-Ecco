"""Package selected native renders and honest timing/native evidence for review."""
from pathlib import Path
import json,hashlib,math,re
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[5];ASSET=ROOT/'04-Production/Shared/Assets';TASK=ROOT/'04-Production/Records/Tasks/T-044';REV=TASK/'Revision_v006';E=REV/'Evidence';P=TASK/'Previews/Revision_v006'
def rel(p):return p.relative_to(ROOT).as_posix()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,indent=2),encoding='utf-8')
def font(n):return ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',n)
views=[('BHA_detail','Bit / adapter side view; original camera'),('BHA_face','Additional bit-face inspection'),('layers','Smooth steel / cement / formation section'),('downhole_A','Downhole A / curved static fluid and controlled highlights'),('downhole_B','Nearby downhole B / same shared masters')]
images=[]
for name,label in views:
 p=P/(name+'_working_v010.png');im=Image.open(p);im.load();assert im.size==(1280,720)
 images.append(dict(name=name,label=label,path=rel(p),scene=rel(REV/'Scenes'/(name+'_cleanup_v010.blend')),sha256=sha(p),bytes=p.stat().st_size,dimensions=list(im.size),alpha_extrema=list(im.getchannel('A').getextrema()) if im.mode=='RGBA' else None,bright_pixels_percent=100*sum(min(px)>=250 for px in im.convert('RGB').getdata())/(1280*720),benchmark=rel(E/(name+'_working_benchmark_v010.json'))))
def sheet(items,path,title,footer):
 w,h=640,360;rows=math.ceil(len(items)/2);im=Image.new('RGB',(1344,85+rows*424+45),(15,22,28));d=ImageDraw.Draw(im);d.text((24,22),title,fill=(230,240,245),font=font(26))
 for i,(label,p) in enumerate(items):
  x=24+(i%2)*656;y=85+(i//2)*424;img=Image.open(p).convert('RGB');im.paste(img.resize((w,h),Image.Resampling.LANCZOS),(x,y));d.text((x,y+h+12),label,fill=(199,217,226),font=font(17))
 d.text((24,im.height-32),footer,fill=(156,180,192),font=font(17));im.save(path,quality=92)
sheet([(i['label'],ROOT/i['path']) for i in images],P/'approval-overview_v006.jpg','T44 / bounded bit, steel and static-fluid cleanup','Individual full-size PNGs are the review evidence. Appearance approval remains with Radzi.')
sheet([('Consumer A / prior formation candidate',TASK/'Previews/Revision_v005/Reuse_A_formation_working_v005.png'),('Consumer A / shared cleanup; camera/timing retained',P/'Reuse_A_working_v010.png'),('Consumer B / prior formation candidate',TASK/'Previews/Revision_v005/Reuse_B_formation_working_v005.png'),('Consumer B / shared cleanup; camera/timing retained',P/'Reuse_B_working_v010.png')],P/'propagation_v006.jpg','Two unchanged consumer cameras / one shared library revision','Both consumers link environmentv009 / BHAv006 / unchanged ECCO filmv002. Full native checks accompany this image.')
paths=[ASSET/'BHA/BHA_film_v006.blend',ASSET/'WellAssembly/World_environment_v009.blend']+[REV/'Scenes'/(n+'_cleanup_v010.blend') for n in [i[0] for i in views]+['Reuse_A','Reuse_B']]
manifest=dict(version='v006',task='T44',status='bounded_cleanup_candidate_for_Radzi_image_review',local_root=str(ROOT),baseline_manifest='manifest_v005.json',native_backup='All .blend originals/candidates local Git-ignored; no native upload or off-machine backup claimed',artifacts=[dict(path=rel(p),sha256=sha(p),bytes=p.stat().st_size,storage='local-native') for p in paths],approval_images=images,reused_unchanged=['ECCO/ECCO_film_v002.blend','Formation/Formation_context_v002.blend','Formation/Formation_cased-section_v002.blend','Surface/Surface_context_v003.blend'],controls='formation_controls_v003.py',accepted_coverage='Exact v005 formation mesh retained; X[-8,10]m / transverse half-width2.4m',bit_reference='https://www.slb.com/resource-library/oilfield-review/defining-series/defining-bits',bit_limit='Authored six-blade fixed-cutter visual study; no exact MIT/client bit, thread fit, selected alloy or hydraulic qualification',fluid_limit='Static curved continuously blended optical cut, not a free liquid surface, volumetric fluid domain or flow simulation',shoe_limit='Prior redundant coplanar illustrative rim retained hidden; flush source casing end represents boundary context. Exact shoe assembly remains unverified.')
dump(ASSET/'World/manifest_v006.json',manifest)
mapping=json.loads((TASK/'Revision_v005/component-consumers_v005.json').read_text())
mapping['version']='v006';mapping['masters']=['BHA_film_v006.blend','World_environment_v009.blend','ECCO_film_v002.blend'];mapping['actual_cleanup_consumers']=[rel(p) for p in paths[2:]];mapping['future_shot_status']='V3 component mapping inherited; actual film shots not built or authorized by this cleanup'
mapping['migrations']=[dict(consumer=k,from_master=['World_environment_v005.blend','BHA_film_v002.blend'],to_master=['World_environment_v009.blend','BHA_film_v006.blend'],saved=rel(REV/'Scenes'/f'Reuse_{k}_cleanup_v010.blend'),camera_timing_controls_preserved=True,rollback=rel(TASK/'Revision_v005/Scenes'/f'Reuse_{k}_formation_v005.blend')) for k in ['A','B']]
dump(REV/'component-consumers_v006.json',mapping)
native=json.loads((E/'native-verification_v006.json').read_text());bench=[dict(path=rel(p),**json.loads(p.read_text())) for p in sorted(E.glob('*benchmark*.json'))];final=[json.loads((E/(n+'_working_benchmark_v010.json')).read_text()) for n in [i[0] for i in views]+['Reuse_A','Reuse_B']]
checks=[dict(name='native source/geometry/link/control checks',passed=native['all_pass']),dict(name='all seven final full renders below5s',passed=all(x['under_5'] for x in final)),dict(name='five separately viewable720p approval images',passed=len(images)==5 and all(i['dimensions']==[1280,720] for i in images)),dict(name='accepted full-frame downhole coverage retained',passed=all(i['alpha_extrema']==[255,255] for i in images if i['name'].startswith('downhole')))]
dump(E/'package-verification_v006.json',dict(all_pass=False,checks=checks,status='Packaging/link validation in progress'))
links=[]
for p in [TASK/'report.md',REV/'review-guide.md',ASSET/'World/README_v003.md',ASSET/'World/README.md']:
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
  if '://' not in target:links.append(dict(source=rel(p),target=target,exists=(p.parent/target.split('#')[0]).exists()))
checks.append(dict(name='current report/review/usage links resolve',passed=all(i['exists'] for i in links)))
data=dict(all_pass=all(i['passed'] for i in checks),checks=checks,native_check_count=len(native['checks']),approval_images=images,final_timings=final,retained_benchmarks=bench,retained_failed_attempts=[b for b in bench if not b['under_5']],links=links,performance_limit='Normal-cache fresh-process first full render-to-file only. v008 new blended shader6.45s failure prompted simplification before final tests; prior empty-cache12.55-25.13s initialization remains unresolved. No universal cold-machine compliance claim.',visual_review='Executor inspected full-size saved-candidate renders; this does not establish human appearance acceptance or engineering approval.')
dump(E/'package-verification_v006.json',data);print(json.dumps(dict(all_pass=data['all_pass'],checks=checks,timings={Path(i['scene']).stem:i['seconds'] for i in final},retained_failure_count=len(data['retained_failed_attempts']),missing_links=[i for i in links if not i['exists']]),indent=2))
