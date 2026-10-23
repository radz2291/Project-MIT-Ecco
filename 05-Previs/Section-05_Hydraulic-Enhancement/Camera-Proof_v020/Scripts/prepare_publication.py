import subprocess,shutil,json
from pathlib import Path
B=Path(__file__).resolve().parents[1];ROOT=B.parents[2];D=Path('D:/MIT-ECCO-Render-Recovery/Source-Control_v034');backup=Path('D:/MIT-ECCO-Render-Recovery/S05-v020-Previs')
git=['git','-c',f'safe.directory={D.as_posix()}','-C',str(D)]
def run(*args):return subprocess.check_output(git+list(args),text=True).strip()
assert run('rev-parse','HEAD')=='53dbf55361a6453b6feb08df3d312936a1868506'
assert not run('diff','--cached','--name-only')
paths=[B/'README.md',*sorted((B/'Scripts').glob('*.py')),*sorted((B/'Records').glob('*.json')),*sorted((B/'Records').glob('*.md'))]
paths=[p for p in paths if p.name!='sync-verification.json']
paths.extend(B/'Previews'/name for name in ['A_entry.png','A_arrival.png','transition-study.jpg','continuous-camera-contact-sheet.jpg'])
paths.extend(ROOT/f'04-Production/Shots/S05/S05-{part}/direction.md' for part in 'ABC')
rels=[]
for p in paths:
 rel=p.relative_to(ROOT);rels.append(rel.as_posix())
 for dest in [D,backup]:
  q=dest/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
subprocess.run(git+['add','--']+rels,check=True)
staged=set(run('diff','--cached','--name-only').splitlines());assert staged.issubset(set(rels))
# Keep the exact user's Markdown hard breaks in the copied handoff.
subprocess.run(git+['diff','--cached','--check','--','.',':(exclude)**/owner-direction.txt'],check=True)
print(run('diff','--cached','--stat'))
