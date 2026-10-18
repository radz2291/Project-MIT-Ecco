"""Selected T44 continuity images, native hashes and sole-integrator allow-list."""
from pathlib import Path
import json,hashlib,re
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[6];ASSET=ROOT/'04-Production/Shared/Assets';WORLD=ASSET/'World';TASK=ROOT/'04-Production/Records/Tasks/T-044';REV=TASK/'Revision_v007';E=REV/'Evidence';P=TASK/'Previews/Revision_v007'
def rel(p):return p.relative_to(ROOT).as_posix()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,indent=2),encoding='utf-8')
views=[('connection_wide','v003','Wider connected assembly'),('furthest_uphole','v002','Second / furthest intended view'),('Reuse_A','v002','Consumer A / preserved camera and timing'),('Reuse_B','v002','Consumer B / preserved camera and timing')]
images=[]
for name,version,label in views:
 p=P/(name+'_'+version+'.png');im=Image.open(p);im.load();assert im.size==(1280,720)
 scene=REV/'Scenes'/((name+'_continuity_' if name.startswith('Reuse') else name+'_')+version+'.blend')
 images.append(dict(name=name,path=rel(p),scene=rel(scene),label=label,sha256=sha(p),dimensions=list(im.size),bytes=p.stat().st_size,benchmark=rel(E/(name+'_'+version+'_benchmark_v007.json'))))
items=[]
for k in ['A','B']:
 items.extend([(f'Consumer {k} / preserved v006 baseline',TASK/'Previews/Revision_v006'/f'Reuse_{k}_working_v010.png'),(f'Consumer {k} / shared continuation, unchanged camera',P/f'Reuse_{k}_v002.png')])
canvas=Image.new('RGB',(1344,960),(16,23,30));d=ImageDraw.Draw(canvas);font=lambda n:ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',n)
d.text((24,20),'T44 / uphole continuity / two unchanged consumers',font=font(25),fill=(232,241,245))
for i,(label,p) in enumerate(items):
 x=24+(i%2)*656;y=75+(i//2)*420;im=Image.open(p).convert('RGB');canvas.paste(im.resize((640,360),Image.Resampling.LANCZOS),(x,y));d.text((x,y+370),label,font=font(17),fill=(199,217,227))
d.text((24,925),'Native source preserved. Length/show are new local controls; exact client connection and visual approval remain pending.',font=font(16),fill=(160,183,195));canvas.save(P/'propagation_v007.jpg',quality=92)
native_paths=[ASSET/'BHA/BHA_film_v007.blend']+[ROOT/i['scene'] for i in images]
native=json.loads((E/'native-verification_canonical_v007.json').read_text())
manifest=dict(version='v007',task='T44',status='canonical_continuity_successor_for_Radzi_review',baseline_commit='df1bc5626e820dc3a0b9af286bfcca4ce498d8c0',local_root=str(ROOT),native_backup='All .blend files local Git-ignored; no upload or off-machine backup claimed',artifacts=[dict(path=rel(p),sha256=sha(p),bytes=p.stat().st_size,storage='local-native') for p in native_paths],approval_images=images,source_preservation='Accepted BHAv006, ECCO filmv002 and environmentv009 unchanged; v007 nests v006',api=['World/Scripts/formation_controls_v004.py','World/Scripts/continuation_controls_v001.py'],continuation=dict(default_length_m=12,range_m=[.25,40],join_x_m=-1.5,source_far_x_m=-13.5,outer_radius_m=.104775,inner_radius_m=.03571875,connection_outer_radius_m=.107,coordinates='metres; +X selected downhole; parented to existing hardware placement/travel/rotation'),limits='Simplified collar continuation and raised transition; no exact client BHA/thread fit, full string-to-rig or engineering acceptance. Coverage checked for these cameras/default12m only.',human_gate='Appearance approval pending; technical release does not bypass Work dependency gate',integrator='T45 sole Git integrator; T44 makes no Git mutation')
dump(WORLD/'manifest_v007.json',manifest)
prior=json.loads((TASK/'Revision_v006/component-consumers_v006.json').read_text());prior['version']='v007';prior['master']='BHA_film_v007.blend';prior['actual_continuity_consumers']=[rel(p) for p in native_paths[1:]];prior['future_shot_status']='No actual shots built; connected S01-B/C and other wide/travelling consumers require migration/coverage check; isolated heroes may hide continuation';prior['external_consumers_pending']='T45 owns T46/T47/T48 migration/rechecks against this exact successor; not claimed completed by T44'
dump(REV/'component-consumers_v007.json',prior)
explicit=[TASK/'.gitignore',TASK/'report.md',TASK/'report_v006.md',WORLD/'README.md',WORLD/'README_v004.md',WORLD/'manifest_v007.json',WORLD/'Scripts/formation_controls_v004.py',WORLD/'Scripts/continuation_controls_v001.py']
records=[p for p in REV.rglob('*') if p.is_file() and p.suffix in ['.py','.json','.md'] and p.name!='sync-verification_v007.json']
files=sorted(set(rel(p) for p in explicit+records+[ROOT/i['path'] for i in images]+[P/'propagation_v007.jpg']))
allow=rel(REV/'allowed-tracked_v007.json');files=sorted(set(files+[allow,rel(E/'package-verification_v007.json')]))
dump(REV/'allowed-tracked_v007.json',dict(task='T44',integrator='T45 only',files=files,exclusions='No .blend/logs/raw samples/T45-T48 roots/global asset register/unrelated generated image'))
bench=[json.loads(p.read_text()) for p in E.glob('*benchmark_v007.json')]
preserved=[]
for mf in ['manifest_v004.json','manifest_v005.json','manifest_v006.json']:
 data=json.loads((WORLD/mf).read_text())
 for i in data.get('sources',[])+data['artifacts']:preserved.append(dict(path=i['path'],unchanged=sha(ROOT/i['path'])==i['sha256']))
dump(E/'package-verification_v007.json',dict(all_pass=False,status='Package link validation in progress'))
links=[]
for p in [TASK/'report.md',REV/'review-guide.md',REV/'handoff_v007.md',WORLD/'README_v004.md',WORLD/'README.md']:
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
  if '://' not in target:links.append(dict(source=rel(p),target=target,exists=(p.parent/target.split('#')[0]).exists()))
checks=[dict(name='389 canonical native checks pass',passed=native['all_pass']),dict(name='all prior native/source hashes unchanged',passed=all(x['unchanged'] for x in preserved)),dict(name='all five full render-to-file samples below5s',passed=len(bench)==5 and all(x['under_5'] for x in bench)),dict(name='all current review/report/API links resolve',passed=all(x['exists'] for x in links)),dict(name='allow-list excludes private/heavy/other-worker roots',passed=all(not re.search(r'\.(blend|log)$|/T-04[5-8]/|^02-Reference/',p) for p in files))]
out=dict(all_pass=all(c['passed'] for c in checks),checks=checks,native_check_count=len(native['checks']),approval_images=images,benchmarks=bench,preserved_sources=preserved,links=links,performance_limit='Normal existing disk GPU caches only. Prior empty-cache startup12.55-25.13s unresolved.',gate='Human appearance acceptance pending; T45 sole integrator and downstream Work dependency gate remain explicit')
dump(E/'package-verification_v007.json',out);print(json.dumps(dict(all_pass=out['all_pass'],checks=checks,allowed_file_count=len(files),missing_links=[x for x in links if not x['exists']]),indent=2))
