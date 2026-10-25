from pathlib import Path
import subprocess,shutil,json,hashlib
B=Path(__file__).resolve().parents[1];R=B.parents[3];P=Path('D:/MIT-ECCO-Render-Recovery/Source-Control_v034');backup=Path('D:/MIT-ECCO-Render-Recovery/S07-Monumental-Precision_v006')
def git(*args):
 r=subprocess.run(['git','-c','safe.directory='+P.as_posix(),'-C',str(P),*args],capture_output=True,text=True);assert r.returncode==0,r.stderr;return r.stdout.strip()
assert not git('status','--porcelain','--untracked-files=no')
assert git('ls-remote','https://github.com/radz2291/Project-MIT-Ecco.git','refs/heads/main').split()[0]==git('rev-parse','HEAD')
me=Path(__file__);dst=backup/me.relative_to(B);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(me,dst)
manifest=json.loads((B/'Records/asset-manifest.json').read_text());manifest=[x for x in manifest if x['path']!=me.relative_to(B).as_posix()];manifest.append({'path':me.relative_to(B).as_posix(),'sha256':hashlib.sha256(me.read_bytes()).hexdigest(),'bytes':me.stat().st_size})
(B/'Records/asset-manifest.json').write_text(json.dumps(manifest,indent=2));shutil.copy2(B/'Records/asset-manifest.json',backup/'Records/asset-manifest.json')
rv=json.loads((B/'Records/recovery-verification.json').read_text());rv['files_verified']=len(manifest);(B/'Records/recovery-verification.json').write_text(json.dumps(rv,indent=2));shutil.copy2(B/'Records/recovery-verification.json',backup/'Records/recovery-verification.json')
files=[B.parent/'README.md']
for root in [B,R/'04-Production/Records/Tasks/S07-v006-Revision',R/'04-Production/Records/Tasks/S07-Closure']:
 for p in root.rglob('*'):
  if not p.is_file() or any(x in p.relative_to(root).parts for x in ['Cache','Scenes','Previews']) or p.name=='sync-verification.json' or p.suffix=='.log':continue
  files.append(p)
paths=[]
for p in files:
 rel=p.relative_to(R);dest=P/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest);paths.append(rel.as_posix())
git('add','--',*paths);print(git('diff','--cached','--stat'));print('Staged for inspection; commit and remote verification remain.')
