import json,csv,hashlib,shutil,datetime
from pathlib import Path
from PIL import Image,ImageChops
R=Path(__file__).resolve().parents[2];C=R/'Closure'
keep={'v009':'Approved restrained illustrative geometry and engineering comparison', 'v014':'Approved generated amplitude direction, original texture, seamless derivative and seam proof', 'v023':'Computed organic radius surface and geometry-derived colour milestone', 'v028':'Full irregular surrounding ground and scientific HUD environment milestone', 'v033':'Smooth continuous camera and drone ending before spatial-label revision', 'v036':'FINAL — approved complete sequence, single spatial label at second-last circle'}
versions=sorted(p for p in R.iterdir() if p.is_dir() and p.name[0:1]=='v' and p.name[1:].isdigit())
inventory=[];archive=[]
for v in versions:
 files=[p for p in v.rglob('*') if p.is_file()];size=sum(p.stat().st_size for p in files)
 inventory.append({'version':v.name,'decision':'KEEP' if v.name in keep else 'REMOVE AFTER REVIEW','bytes':size,'reason':keep.get(v.name,'Superseded experiment or intermediate adjustment; provenance archived in Closure/Iteration-History'),'absolute_path':str(v)})
 for p in files:
  rel=p.relative_to(v)
  if any(x.lower() in ['work','dependencies','__pycache__'] for x in rel.parts):continue
  if p.suffix.lower() not in ['.md','.txt','.json','.csv','.py']:continue
  if p.stat().st_size>3*1024*1024:continue
  dst=C/'Iteration-History'/v.name/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dst)
  archive.append({'source':str(p.relative_to(R)),'archive':str(dst.relative_to(R)),'sha256':hashlib.sha256(dst.read_bytes()).hexdigest()})
(C/'Version-inventory.json').write_text(json.dumps(inventory,indent=2))
(C/'Archived-provenance-manifest.json').write_text(json.dumps(archive,indent=2))
with (C/'KEEP-REMOVE.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=inventory[0].keys());w.writeheader();w.writerows(inventory)
drop=[x for x in inventory if x['decision']!='KEEP'];caches=[]
for version in keep:
 for p in (R/version).rglob('Work'):
  if p.is_dir():caches.append({'path':str(p),'bytes':sum(x.stat().st_size for x in p.rglob('*') if x.is_file()),'reason':'Regenerable rendering cache; not required to open saved native scene or play delivered MP4'})
(C/'Optional-cache-removal.json').write_text(json.dumps(caches,indent=2))
a=Image.open(R/'v036/Previews/S03_v036_nominal-label_frame0060.png').convert('RGB');b=Image.open(C/'Final-label-verification.png').convert('RGB');assert a.size==b.size
proof={'frame':60,'pixel_identical_after_dependency_localization':ImageChops.difference(a,b).getbbox() is None}
assert proof['pixel_identical_after_dependency_localization']
(C/'Final-visual-verification.json').write_text(json.dumps(proof,indent=2))
manifest=[]
for version in keep:
 for p in sorted((R/version).rglob('*')):
  if not p.is_file() or 'Work' in p.relative_to(R/version).parts or p.suffix=='.blend1':continue
  manifest.append({'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(C/'Retained-file-manifest.json').write_text(json.dumps(manifest,indent=2))
summary={'approved_date':'2026-10-20','authority':'Radzi: Good, this project is approved. Current request authorizes closure and cleanup recommendations. No deletion performed.','scope':'Section 3 only; Sections 1 and 2, canonical shared assets and project-level source image excluded','keep_versions':list(keep),'remove_versions':[x['version'] for x in drop],'remove_logical_bytes':sum(x['bytes'] for x in drop),'optional_cache_bytes':sum(x['bytes'] for x in caches),'archive_files':len(archive),'retained_files':len(manifest),'visual_check':proof}
(C/'Closure-summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
