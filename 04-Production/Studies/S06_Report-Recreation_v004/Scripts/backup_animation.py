from pathlib import Path
import json,hashlib,shutil
B=Path(__file__).resolve().parents[1]
backup=Path('D:/MIT-ECCO-Render-Recovery/S06-Report-Recreation_v004')
files=[p for p in B.rglob('*') if p.is_file() and 'Cache' not in p.relative_to(B).parts and p.suffix!='.log' and p.name not in ('asset-manifest.json','sync-verification.json','recovery-verification.json')]
manifest=[]
for p in files:
    rel=p.relative_to(B);dst=backup/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dst)
    sha=hashlib.sha256(p.read_bytes()).hexdigest();assert sha==hashlib.sha256(dst.read_bytes()).hexdigest()
    manifest.append({'path':rel.as_posix(),'bytes':p.stat().st_size,'sha256':sha})
(B/'Records/asset-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
record={'recovery_root':str(backup),'hash_verified_files':len(manifest),'same_machine_only':True,'cache_included':False,'movie_and_editable_native_included':True,'prior_still_native_retained':True}
(B/'Records/recovery-verification.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
for name in ('asset-manifest.json','recovery-verification.json'):shutil.copy2(B/'Records'/name,backup/'Records'/name)
print(json.dumps(record))
