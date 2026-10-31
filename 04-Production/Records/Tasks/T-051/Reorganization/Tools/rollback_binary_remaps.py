"""Sole-integrator opt-in rollback of path-byte patches only; does not undo moves."""
import pathlib,json,hashlib,os,argparse
R=pathlib.Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco').resolve();T=R/'04-Production/Records/Tasks/T-051/Reorganization';ap=argparse.ArgumentParser();ap.add_argument('--apply',action='store_true');args=ap.parse_args();rows=json.loads((T/'binary-remap-applied.json').read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
for x in reversed(rows):
 if not x.get('prepared',x['applied']):continue
 p=(R/x['path']).resolve();backup=(R/x['backup']).resolve();assert p.is_relative_to(R) and backup.is_relative_to(T/'Backup');original=backup.read_bytes();assert sha(original)==x['sha256_before'];current=sha(p.read_bytes());assert current in (x['sha256_before'],x['sha256_after']),'Unexpected newer changes: stop rollback'
 if args.apply and current!=x['sha256_before']:
  tmp=p.with_name(p.name+'.ecco-rollback.tmp');assert not tmp.exists()
  with tmp.open('xb') as f:f.write(original);f.flush();os.fsync(f.fileno())
  os.replace(tmp,p);assert sha(p.read_bytes())==x['sha256_before']
print('RESTORED' if args.apply else 'ROLLBACK_CHECK_PASS',len(rows))
