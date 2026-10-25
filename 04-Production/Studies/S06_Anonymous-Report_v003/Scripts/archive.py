import json,hashlib,shutil
from pathlib import Path
B=Path(__file__).resolve().parents[1];BASE=B.with_name('S06_Sculpted-Information_v002')
recovery=Path('D:/MIT-ECCO-Render-Recovery/S06-Anonymous-Report_v003')
pub=Path('D:/MIT-ECCO-Render-Recovery/Source-Control_v034/04-Production/Studies/S06_Anonymous-Report_v003')
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
old=json.loads((BASE/'Records/asset-manifest.json').read_text(encoding='utf-8'))
for a in old['artifacts']:assert h(BASE/a['path'])==a['sha256']
assets=[]
for p in B.rglob('*'):
    if not p.is_file():continue
    rel=p.relative_to(B)
    if 'Cache' in rel.parts or rel.name in ('asset-manifest.json','sync-verification.json'):continue
    dest=recovery/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest);assert h(p)==h(dest)
    if rel.parts[0] in ('Scenes','Media') or (rel.parts[0]=='Previews' and not p.name.startswith('check_')):assets.append({'path':str(rel).replace('\\','/'),'sha256':h(p),'bytes':p.stat().st_size,'backup':str(dest)})
manifest={'status':'owner review candidate','scope':'Option C final three seconds only','previous_v002_hashes_unchanged':True,'same_machine_backup_only':True,'source_and_derived_media_remote':False,'assets':assets}
(B/'Records/asset-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8');shutil.copy2(B/'Records/asset-manifest.json',recovery/'Records/asset-manifest.json')
for p in B.rglob('*'):
    if not p.is_file():continue
    rel=p.relative_to(B)
    if rel.parts[0] in ('Cache','Scenes','Media','Previews') or p.suffix=='.log' or rel.name in ('source-private.json','sync-verification.json'):continue
    dest=pub/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
print('Local media backup verified; v002 unchanged; only generic scripts and records copied to publishing checkout.')
