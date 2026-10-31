"""Root opt-in byte-exact restoration at post-move paths; DOES NOT undo filesystem moves."""
import pathlib,json,hashlib,os,argparse
from blend_rollback_delta import restore
R=pathlib.Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco').resolve();T=R/'04-Production/Records/Tasks/T-051/Reorganization';ap=argparse.ArgumentParser();ap.add_argument('--apply',action='store_true');args=ap.parse_args();records=json.loads((T/'sparse-remap-applied.json').read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
for x in reversed(records):
 p=(R/x['new_owner']).resolve();dp=(R/x['delta']).resolve();assert p.is_relative_to(R) and dp.is_relative_to((T/'Backup').resolve());data=p.read_bytes();current=sha(data)
 if current==x['original_sha256']:continue
 assert current==x['patched_sha256'],'File changed after patch: stop, never overwrite newer work';blob=dp.read_bytes();assert sha(blob)==x['delta_sha256'];restored=restore(data,json.loads(blob));assert sha(restored)==x['original_sha256']
 if args.apply:
  tmp=p.with_name(p.name+'.ecco-sparse-rollback.tmp');assert not tmp.exists()
  with tmp.open('xb') as f:f.write(restored);f.flush();os.fsync(f.fileno())
  os.replace(tmp,p);assert sha(p.read_bytes())==x['original_sha256']
print('RESTORED' if args.apply else 'ROLLBACK_CHECKED',len(records))
