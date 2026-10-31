"""T44 individual image evidence, review index, hashes and consumer manifest."""
from pathlib import Path
import json,hashlib,re,math
from PIL import Image,ImageDraw,ImageFont,ImageStat
ROOT=Path(__file__).resolve().parents[5];PROD=ROOT/'04-Production';ASSET=PROD/'Shared/Assets';WORLD=ASSET/'World';TASK=PROD/'Records/Tasks/T-044';REV=TASK/'Revision_v005';E=REV/'Evidence';P=TASK/'Previews/Revision_v005'
def rel(p):return p.relative_to(ROOT).as_posix()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,indent=2),encoding='utf-8')
def font(n):return ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',n)
views=[
 ('wide_context','v007','01  Rig and surrounding earth / intentional section'),
 ('downhole_A','v006','02  Downhole A / source scale, surrounding rock and fluid'),
 ('downhole_B','v006','03  Nearby downhole B / same shared environment'),
 ('layers','v010','04  Steel, cement, formation / hardware hidden for inspection'),
 ('BHA_detail','v006','05  BHA, bit and adapters / simplified geometry')]
images=[]
for name,version,label in views:
 p=P/(name+'_working_'+version+'.png');im=Image.open(p);im.load();assert im.size==(1280,720)
 data=dict(name=name,label=label,path=rel(p),scene=rel(REV/'Scenes'/(name+'_'+version+'.blend')),sha256=sha(p),bytes=p.stat().st_size,dimensions=list(im.size),benchmark=rel(E/(name+'_working_benchmark_'+version+'.json')))
 data['alpha_extrema']=list(im.getchannel('A').getextrema()) if im.mode=='RGBA' else None
 data['bright_pixels_percent']=100*sum(1 for px in im.convert('RGB').getdata() if min(px)>=250)/(1280*720)
 images.append(data)
def contact(items,target,title,footer,legend=False):
 w=700;h=394;pad=24;bar=50;rows=math.ceil((len(items)+(1 if legend else 0))/2);canvas=Image.new('RGB',(1472,80+rows*(h+bar+pad)+48),(16,23,30));d=ImageDraw.Draw(canvas);d.text((24,21),title,font=font(27),fill=(238,244,247))
 for i,(label,path) in enumerate(items):
  im=Image.open(path).convert('RGB');x=24+(i%2)*724;y=80+(i//2)*(h+bar+pad);canvas.paste(im.resize((w,h),Image.Resampling.LANCZOS),(x,y));d.text((x,y+h+9),label,font=font(18),fill=(203,220,229))
 if legend:
  x=748;y=80+2*(h+bar+pad)
  lines=['Read the five individual full-size images.','Brown: illustrative formation','Slate-blue: steel / pale grey: cement','Muted olive: static optical fluid section','Two nearby cameras; same linked mass.','Source bore and product scale preserved.','Radzi image approval remains pending.']
  for i,line in enumerate(lines):d.text((x+15,y+30+i*42),line,font=font(22 if i==0 else 19),fill=(202,219,228))
 d.text((24,canvas.height-35),footer,font=font(18),fill=(150,175,189));canvas.save(target,quality=92)
contact([(v['label'],ROOT/v['path']) for v in images],P/'approval-overview_v005.jpg','T44 / shared surrounding formation / approval image index','Five native-rendered individual PNGs are primary evidence; this sheet is an index.',True)
contact([
 ('Consumer A / preserved v004 camera',TASK/'Previews/Reuse_A_after_v004_vulkan-working_f001.png'),
 ('Consumer A / formation v005 / same camera and timing',P/'Reuse_A_formation_working_v005.png'),
 ('Consumer B / preserved v004 camera',TASK/'Previews/Reuse_B_after_v004_vulkan-cold-retest_f001.png'),
 ('Consumer B / formation v005 / same camera and timing',P/'Reuse_B_formation_working_v005.png')],P/'propagation_v005.jpg','One shared environment update / two unchanged consumer cameras','Inspection cameras/timing/local controls preserved; these are reuse tests, not film shots.')
master_paths=[ASSET/'WellAssembly/World_environment_v005.blend',ASSET/'Formation/Formation_context_v002.blend',ASSET/'Formation/Formation_cased-section_v002.blend',ASSET/'Surface/Surface_context_v003.blend']
scene_paths=[ROOT/i['scene'] for i in images]+[REV/'Scenes'/f'Reuse_{k}_formation_v005.blend' for k in ['A','B']]
manifest=dict(version='v005',task='T44',status='revised_candidate_for_Radzi_image_review',local_root=str(ROOT),native_backup='Local Git-ignored files; no remote native media/off-machine backup claimed',baseline_manifest='manifest_v004.json',artifacts=[dict(path=rel(p),sha256=sha(p),bytes=p.stat().st_size,storage='local-native') for p in master_paths+scene_paths],reused_unchanged=['BHA/BHA_film_v002.blend','ECCO/ECCO_film_v002.blend'],approval_images=images,downhole_extent=dict(axial_m=[-8,10],transverse_half_width_m=2.4,construction='surrounding boundary mass; cut-face relief outside unchanged registered bore'),controls='formation_controls_v002.py',source_truth='Illustrative geology/rig context and simplified hardware, not engineering certification or actual deployment',performance='720p EEVEE16 Vulkan; first render in fresh process with normal driver caches; known empty-cache initialization limitation retained')
dump(WORLD/'manifest_v005.json',manifest)
oldmap=json.loads((TASK/'component-consumers_v004.json').read_text());comps=oldmap['components']
for key,rec in comps.items():rec['future_shots_state']='not built; old V3 map retained, no automatic migration/approval'
comps['FORMATION']=dict(parent_components=['WELL','SURFACE'],shots=sorted(set(comps['WELL']['shots']+comps['SURFACE']['shots'])),actual_consumers=['Reuse_A_formation_v005','Reuse_B_formation_v005','downhole_A_v006','downhole_B_v006','layers_v010','wide_context_v007'],future_shots_state='not built; verify exact view/coverage when authorized')
dump(REV/'component-consumers_v005.json',dict(version='v005',components=comps,migrations=[dict(consumer=k,from_master='World_environment_v004.blend',to_master='World_environment_v005.blend',saved=rel(REV/'Scenes'/f'Reuse_{k}_formation_v005.blend'),camera_timing_controls_preserved=True,rollback=rel(TASK/'ReuseTests'/f'Reuse_{k}_after_v004.blend')) for k in ['A','B']],procedure='Read World/README_v002.md; identify consumers, relink/reload, verify source/controls/overrides/coverage, benchmark and rerender. Preserve prior immutable candidate for rollback.'))
native=json.loads((E/'native-verification_v005.json').read_text());benchmarks=[dict(path=rel(p),**json.loads(p.read_text())) for p in sorted(E.glob('*benchmark*.json'))]
finalbench=[json.loads((ROOT/i['benchmark']).read_text()) for i in images]
checks=[dict(name='62 native/source/control checks',passed=native['all_pass']),dict(name='all five final approval views below5s',passed=all(x['under_5'] for x in finalbench)),dict(name='all retained revision benchmark samples below5s',passed=all(x['under_5'] for x in benchmarks)),dict(name='both nearby downhole images have complete alpha coverage',passed=all(i['alpha_extrema']==[255,255] for i in images if i['name'].startswith('downhole'))),dict(name='five separate full-size native images',passed=len(images)==5 and all(i['dimensions']==[1280,720] for i in images))]
out=E/'package-verification_v005.json';dump(out,dict(checks=checks))
links=[]
for p in [TASK/'report.md',REV/'review-guide.md',WORLD/'README_v002.md',WORLD/'README.md']:
 for m in re.finditer(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
  target=m.group(1)
  if '://' not in target:links.append(dict(source=rel(p),target=target,exists=(p.parent/target).exists()))
checks.append(dict(name='all current review/usage links resolve',passed=all(l['exists'] for l in links)))
data=dict(checks=checks,all_pass=all(c['passed'] for c in checks),native_check_count=len(native['checks']),approval_images=images,final_timings_s=[x['seconds'] for x in finalbench],all_benchmarks=benchmarks,links=links,visual_review='Executor inspected individual renders; Radzi image approval pending. Alpha/checklists do not establish visual or engineering acceptance.',normal_cache_limit='Fresh process, normal existing GPU caches, no excluded warmup. Original empty-cache initialization12.55–25.13s remains a known limit; retest on cache/backend/driver/machine/material/heavy-state changes.')
dump(out,data);print(json.dumps(dict(all_pass=data['all_pass'],checks=checks,timings=data['final_timings_s'],missing_links=[l for l in links if not l['exists']]),indent=2))
