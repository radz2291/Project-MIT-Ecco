"""Portable review package, native hashes, consumer impact and image QA."""
from pathlib import Path
import json,hashlib,re
from PIL import Image,ImageDraw,ImageFont,ImageChops,ImageStat
ROOT=Path(__file__).resolve().parents[5];PROD=ROOT/'04-Production';ASSET=PROD/'Shared/Assets';WORLD=ASSET/'World';TASK=PROD/'Records/Tasks/T-044';E=TASK/'Evidence';P=TASK/'Previews'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,indent=2),encoding='utf-8')
def font(n):return ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',n)
def sheet(items,out,title,cols=2):
 w=700;h=394;bar=44;pad=24;head=75;rows=(len(items)+cols-1)//cols
 canvas=Image.new('RGB',(pad+(w+pad)*cols,head+(h+bar+pad)*rows+45),(16,23,30));draw=ImageDraw.Draw(canvas)
 draw.text((pad,20),title,font=font(28),fill=(235,240,245))
 for i,(label,name) in enumerate(items):
  im=Image.open(P/name).convert('RGB');im.load();assert im.size==(1280,720)
  x=pad+(i%cols)*(w+pad);y=head+(i//cols)*(h+bar+pad)
  canvas.paste(im.resize((w,h),Image.Resampling.LANCZOS),(x,y));draw.text((x,y+h+8),label,font=font(19),fill=(197,214,225))
 draw.text((pad,canvas.height-35),'T44 / shared asset tests · editable libraries stay local · Radzi review pending',font=font(18),fill=(150,172,188))
 canvas.save(out,quality=91)
sheet([
 ('Reused owner-designated offshore rig / material polish','Reuse_surface_before_v003_vulkan-working_f001.png'),
 ('Shared BHA, ECCO, casing / cement / rock / shoe','Reuse_B_after_v004_vulkan-cold-retest_f048.png'),
 ('Exact T5 shape / satin shading / preserved sensor plane','Reuse_A_after_v004_vulkan-working_f001.png'),
 ('Full assembly / simplified adapters and generic bit','Hardware_overview_v001_vulkan-working_f001.png')],P/'review-sheet_v004.jpg','A-WORLD · Shared libraries and reusable interfaces')
sheet([
 ('Consumer A / environment v003 / frame1','Reuse_A_before_v003_vulkan-working_f001.png'),
 ('Consumer A / environment v004 / same camera and timing','Reuse_A_after_v004_vulkan-working_f001.png'),
 ('Consumer B / environment v003 / frame1','Reuse_B_before_v003_vulkan-working_f001.png'),
 ('Consumer B / environment v004 / same camera and timing','Reuse_B_after_v004_vulkan-cold-retest_f001.png')],P/'revision-comparison_v004.jpg','One shared mineral revision · both consumers adopt it')
changes=[]
for kind,after in [('A','vulkan-working'),('B','vulkan-cold-retest')]:
 a=Image.open(P/f'Reuse_{kind}_before_v003_vulkan-working_f001.png').convert('RGB');b=Image.open(P/f'Reuse_{kind}_after_v004_{after}_f001.png').convert('RGB')
 diff=ImageChops.difference(a,b);count=sum(1 for p in diff.getdata() if max(p)>2)
 changes.append(dict(consumer=kind,changed_pixels_gt2=count,percent=count/(a.width*a.height)*100,mean_abs_difference=ImageStat.Stat(diff).mean,camera_timing_controls_preserved=json.loads((E/f'migration_{kind}_v004.json').read_text())['camera_timing_controls_preserved']))
dump(E/'pixel-change_v004.json',dict(comparisons=changes,note='Before/after first frames rendered with Vulkan. Material-grain/roughness revision; no intended geometry/camera/timing change. Pixel differences are supporting visual evidence, not independent proof of appearance approval.'))
paths=['ECCO/ECCO_film_v002.blend','BHA/BHA_film_v002.blend','WellAssembly/World_environment_v003.blend','WellAssembly/World_environment_v004.blend','Surface/Surface_context_v002.blend','Surface/Originals/IntoTheInvisible_Shot01.blend']
native=[ASSET/p for p in paths]+[TASK/'ReuseTests'/n for n in ['Reuse_A_before_v003.blend','Reuse_A_after_v004.blend','Reuse_B_before_v003.blend','Reuse_B_after_v004.blend','Reuse_surface_before_v003.blend','Controls_stress_v001.blend','Hardware_overview_v001.blend']]
sources=[ASSET/'ECCO/ECCO_master_temporary-plugs_v002.blend',ASSET/'WellAssembly/WellAssembly_variants_v003.blend']
manifest=dict(version='v004',task='T44',status='candidate_for_Radzi_review',local_root=str(ROOT),native_media_remote_backup='none claimed; ignored local files',sources=[dict(path=str(p.relative_to(ROOT)).replace('\\','/'),sha256=sha(p)) for p in sources],artifacts=[dict(path=str(p.relative_to(ROOT)).replace('\\','/'),bytes=p.stat().st_size,sha256=sha(p),storage='local Git-ignored native') for p in native],interfaces=dict(hardware='WORLD_HARDWARE',environment='WORLD_* named collections',product='ECCO_FILM',surface='WORLD_SURFACE',controls='world_controls.py v001'),source_truth='T5/T6 originals unchanged; geometry identity verified separately. Versions are immutable candidates; no human/engineering approval inferred.')
dump(WORLD/'manifest_v004.json',manifest)
shotmap=json.loads((PROD/'Records/Tasks/T-042/shot-map_v001.json').read_text())
ids=['ECCO','BHA','WELL','MUD','SURFACE','CASING'];comps={k:dict(shots=[s['id'] for s in shotmap['shots'] if k in s['components']],actual_consumers=['T44 Reuse_A','T44 Reuse_B','T44 Controls_stress'] if k!='SURFACE' else ['T44 Reuse_surface'],future_shots_state='not-built; identify and verify actual files when created') for k in ids}
dump(TASK/'component-consumers_v004.json',dict(version='v004',source='T42 shot-map_v001.json',components=comps,migrations=[dict(consumer=k,from_version='environment_v003',to_version='environment_v004',status='saved and fresh-open verified',camera_timing_controls='preserved',local_material_override=False,rollback=f'ReuseTests/Reuse_{k}_before_v003.blend') for k in ['A','B']],future_revision_procedure='See Shared/Assets/World/README_v001.md; identify consumers, relink/reload, check source/overrides/continuity, cold benchmark, rerender affected frames, record status; rollback to preserved immutable library.'))
bench=[]
for pattern in ['*vulkan-working_benchmark.json','*vulkan-cold-retest_benchmark.json']:
 for p in sorted(E.glob(pattern)):
  d=json.loads(p.read_text());bench.append(dict(path=p.name,all_under_5=d['all_under_5'],cold=[x['seconds'] for x in d['renders'] if x['cold']],seconds=[x['seconds'] for x in d['renders']]))
geometry=json.loads((E/'geometry-verification_v004.json').read_text());controls=json.loads((E/'controls-verification_v001.json').read_text())
checks=[dict(name='all native artifacts exist',passed=all(p.exists() for p in native)),dict(name='60 geometry/source checks',passed=geometry['all_pass']),dict(name='13 stable control checks',passed=controls['all_pass']),dict(name='every current profile render including fresh-process first frame below5',passed=bool(bench) and all(x['all_under_5'] for x in bench)),dict(name='both consumers visibly adopt revision',passed=all(x['changed_pixels_gt2']>0 and x['camera_timing_controls_preserved'] for x in changes))]
links=[]
for p in [TASK/'report.md',WORLD/'README_v001.md']:
 for match in re.finditer(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
  target=match.group(1)
  if '://' not in target:links.append(dict(source=str(p.relative_to(ROOT)),target=target,exists=(p.parent/target).exists()))
checks.append(dict(name='all report/guide relative links resolve',passed=all(x['exists'] for x in links)))
dump(E/'package-verification_v004.json',dict(checks=checks,all_pass=all(x['passed'] for x in checks),benchmarks=bench,geometry_checks=len(geometry['checks']),control_checks=len(controls['checks']),links=links,pixel_changes=changes,performance_limit='Fresh process with normal existing driver caches, no in-process warmup. First uncached initialization failed12.55–25.13s and is not covered by current performance release; benchmark after cache/backend/driver/machine/shot changes.',review='Executor checks only; Radzi acceptance pending'))
print(json.dumps(dict(checks=checks,benchmarks=bench,pixels=changes),indent=2))
