from pathlib import Path
import subprocess,shutil,json,datetime
B=Path(__file__).resolve().parents[1];R=B.parents[3]
P=Path('D:/MIT-ECCO-Render-Recovery/Source-Control_v034');remote='https://github.com/radz2291/Project-MIT-Ecco.git'
def git(*args):
 r=subprocess.run(['git','-c','safe.directory='+P.as_posix(),'-c','user.name=radz2291','-c','user.email=radz2291@users.noreply.github.com','-C',str(P),*args],capture_output=True,text=True)
 assert r.returncode==0,r.stderr;return r.stdout.strip()
assert not git('status','--porcelain','--untracked-files=no'),'Unrelated tracked edits in publishing checkout'
head=git('rev-parse','HEAD');assert git('ls-remote',remote,'refs/heads/main').split()[0]==head,'Remote advanced; reconcile first'
paths=[]
for root in [B,R/'04-Production/Records/Tasks/S07-v003-Revision']:
 for p in root.rglob('*'):
  if not p.is_file():continue
  rel=p.relative_to(root)
  if any(x in rel.parts for x in ['Cache','Scenes','Previews']):continue
  if p.name=='sync-verification.json' or p.suffix=='.log':continue
  dest=P/p.relative_to(R);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
  paths.append(p.relative_to(R).as_posix())
git('add','--',*paths)
git('commit','-m','S07 v003: continuous beauty camera, centered hero and fade to black')
sha=git('rev-parse','HEAD');git('push',remote,'HEAD:main');online=git('ls-remote',remote,'refs/heads/main').split()[0];assert sha==online
assert not git('status','--porcelain','--untracked-files=no')
record={'commit':sha,'remote_main':online,'exact_remote_parity':True,'tracked_checkout_clean':True,'unrelated_untracked_files_preserved':True,'media_local_only':True,'recovery':'D:/MIT-ECCO-Render-Recovery/S07-Monumental-Precision_v003','report_url':f'https://github.com/radz2291/Project-MIT-Ecco/blob/{sha}/04-Production/Shots/S07/Sequence_v003/Records/production-report.md','verified_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
for root in [B,P/B.relative_to(R),Path(record['recovery'])]:
 (root/'Records/sync-verification.json').write_text(json.dumps(record,indent=2))
print(json.dumps(record,indent=2))
