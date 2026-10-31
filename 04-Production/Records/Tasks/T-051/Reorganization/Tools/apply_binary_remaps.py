"""Sole-integrator opt-in writer. Default checks/estimates ONLY; never run --apply by worker.
Run after filesystem moves: all plan new_owner paths must exist with original hashes.
Full original backups + atomic replacement. Refuses insufficient free space.
"""
import pathlib,json,hashlib,shutil,os,argparse
from blend_path_bytes import Blend,patch_bytes
R=pathlib.Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco').resolve();T=R/'04-Production/Records/Tasks/T-051/Reorganization';B=T/'Backup';ap=argparse.ArgumentParser();ap.add_argument('--apply',action='store_true');args=ap.parse_args();plan=json.loads((T/'binary-remap-plan.json').read_text());log=[]
def sha(data):return hashlib.sha256(data).hexdigest()
def inside(p):
 p=p.resolve();assert p.is_relative_to(R),str(p);return p
if args.apply:
 required=plan['full_original_backup_bytes']+plan['largest_changed_bytes']*2+256*1024**2
 assert shutil.disk_usage(R).free>required,'Insufficient space for full originals plus working margin; no changes started'
for entry in plan['plans']:
 p=inside(R/entry['new_owner']);original=p.read_bytes();assert sha(original)==entry['sha256_before'],f'Stale input: {p}';b=Blend(original);paths={x['offset']:x for x in b.paths()}
 for e in entry['edits']:assert paths[e['offset']]['value']==e['old'] and paths[e['offset']]['capacity']==e['capacity'],'Stale field'
 patched,proof=patch_bytes(original,{e['offset']:e['new'] for e in entry['edits']});record={'path':entry['new_owner'],'original_path':entry['old_owner'],'sha256_before':sha(original),'sha256_after':sha(patched),'proof':proof,'applied':False}
 if args.apply:
  backup=inside(B/entry['old_owner']);backup.parent.mkdir(parents=True,exist_ok=True)
  if backup.exists():assert sha(backup.read_bytes())==sha(original),'Backup conflict'
  else:
   with backup.open('xb') as f:f.write(original);f.flush();os.fsync(f.fileno())
  record['backup']=backup.relative_to(R).as_posix();record['prepared']=True;log.append(record);target=T/'binary-remap-applied.json';journal=target.with_suffix('.json.tmp');journal.write_text(json.dumps(log,indent=2));os.replace(journal,target)
  temp=p.with_name(p.name+'.ecco-remap.tmp');assert not temp.exists(),'Unexpected temp file'
  with temp.open('xb') as f:f.write(patched);f.flush();os.fsync(f.fileno())
  assert sha(temp.read_bytes())==sha(patched);os.replace(temp,p);record['applied']=True;record['backup']=backup.relative_to(R).as_posix()
 if not args.apply:log.append(record)
 target=T/('binary-remap-applied.json' if args.apply else 'binary-remap-dryrun.json');tmp=target.with_suffix('.json.tmp');tmp.write_text(json.dumps(log,indent=2));os.replace(tmp,target)
print('APPLIED' if args.apply else 'DRYRUN',len(log),'files')
