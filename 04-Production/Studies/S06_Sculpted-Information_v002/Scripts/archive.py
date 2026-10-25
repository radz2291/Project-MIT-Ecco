import json,shutil,hashlib
from pathlib import Path
B=Path(__file__).resolve().parents[1];OLD=B.with_name('S06_Sculpted-Information_v001')
backup=Path('D:/MIT-ECCO-Render-Recovery/S06-Sculpted-Information_v002')
pub=Path('D:/MIT-ECCO-Render-Recovery/Source-Control_v034/04-Production/Studies/S06_Sculpted-Information_v002')
hashof=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
old_manifest=json.loads((OLD/'Records/asset-manifest.json').read_text(encoding='utf-8'))
old_checks=[]
for a in old_manifest['artifacts']:
    p=OLD/a['path'];same=hashof(p)==a['sha256'];old_checks.append({'path':a['path'],'unchanged':same});assert same
files=[]
for p in B.rglob('*'):
    if not p.is_file():continue
    rel=p.relative_to(B)
    if 'Cache' in rel.parts or rel.name in ('asset-manifest.json','sync-verification.json'):continue
    if rel.parts[0]=='Scenes' and p.name.startswith('Arrival_'):continue
    target=backup/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
    assert hashof(p)==hashof(target)
    if p.suffix in ('.blend','.mp4','.npz') or p.name.startswith('S06_arrival_'):
        files.append({'path':str(rel).replace('\\','/'),'bytes':p.stat().st_size,'sha256':hashof(p),'backup':str(target)})
manifest={'status':'v002 owner review candidate; v001 unfolding foundation accepted','date':'2026-10-25','backup_root':str(backup),'same_machine_backup_only':True,'artifacts':files,'v001_artifacts_unchanged':old_checks,'media_remote':False}
(B/'Records/asset-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8');shutil.copy2(B/'Records/asset-manifest.json',backup/'Records/asset-manifest.json')
for p in B.rglob('*'):
    if not p.is_file():continue
    rel=p.relative_to(B)
    if any(x in rel.parts for x in ('Cache','Scenes')) or p.suffix in ('.mp4','.log') or p.name in ('owner-handoff.txt','sync-verification.json'):continue
    dest=pub/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
print('BACKUP HASH VERIFIED',len(files),'retained media/data artifacts; v001 unchanged; publishing files staged for Git inspection')
