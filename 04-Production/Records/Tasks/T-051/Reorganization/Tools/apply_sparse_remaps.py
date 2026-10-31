"""Root sole-writer opt-in. Run AFTER moves; default verifies all inputs only.
Requires complete dry-run prepared manifest and already stored sparse rollback records.
"""
import pathlib,json,hashlib,os,argparse,shutil
from blend_path_bytes import patch_bytes
from blend_rollback_delta import restore
R=pathlib.Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco').resolve();T=R/'04-Production/Records/Tasks/T-051/Reorganization';ap=argparse.ArgumentParser();ap.add_argument('--apply',action='store_true');args=ap.parse_args();prepared=json.loads((T/'sparse-remap-prepared.json').read_text());assert prepared['complete'];plan=json.loads((T/'binary-remap-plan.json').read_text());byold={x['old_owner']:x for x in plan['plans']};records=prepared['records'];assert len(records)==len(byold)
def sha(b):return hashlib.sha256(b).hexdigest()
def inside(p,base=R):
 p=p.resolve();assert p.is_relative_to(base.resolve()),str(p);return p
def journal(rows):
 p=T/'sparse-remap-applied.json';tmp=p.with_suffix('.json.tmp');tmp.write_text(json.dumps(rows,indent=2));os.replace(tmp,p)
# Whole-transaction preflight before writing even one native.
for x in records:
 p=inside(R/x['new_owner']);assert sha(p.read_bytes())==x['original_sha256'],f'Input drift {p}';d=inside(R/x['delta'],T/'Backup');assert sha(d.read_bytes())==x['delta_sha256'],'Rollback record drift';assert byold[x['old_owner']]['new_owner']==x['new_owner']
if not args.apply:print('ALL_INPUTS_AND_DELTAS_VERIFIED',len(records));raise SystemExit(0)
growth=sum(max(0,x['patched_bytes']-x['original_bytes']) for x in records);temporary=max(x['patched_bytes'] for x in records);assert shutil.disk_usage(R).free>growth+temporary+256*1024**2,'Insufficient growth plus atomic-write margin';log=[]
for i,x in enumerate(records):
 p=inside(R/x['new_owner']);original=p.read_bytes();assert sha(original)==x['original_sha256'];entry=byold[x['old_owner']];patched,proof=patch_bytes(original,{e['offset']:e['new'] for e in entry['edits']});assert sha(patched)==x['patched_sha256'],'Dry-run output mismatch';delta=json.loads((R/x['delta']).read_text());assert restore(patched,delta)==original,'Independent exact rollback failed';item={**x,'prepared':True,'applied':False};log.append(item);journal(log)
 temp=p.with_name(p.name+'.ecco-sparse-remap.tmp');assert not temp.exists()
 with temp.open('xb') as f:f.write(patched);f.flush();os.fsync(f.fileno())
 assert sha(temp.read_bytes())==x['patched_sha256'];os.replace(temp,p);item['applied']=True;journal(log)
 if (i+1)%20==0:print('APPLIED',i+1,'/',len(records),flush=True)
print('ALL_APPLIED',len(records))
