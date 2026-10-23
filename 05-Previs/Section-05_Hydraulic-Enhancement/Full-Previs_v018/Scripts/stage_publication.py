import shutil,subprocess,json
from pathlib import Path
B=Path(__file__).resolve().parents[1];ROOT=B.parents[2]
D=Path('D:/MIT-ECCO-Render-Recovery/Source-Control_v034')
recovery=Path('D:/MIT-ECCO-Render-Recovery/S05-v018-Previs')
git=['git','-c',f'safe.directory={D.as_posix()}','-C',str(D)]
def run(*args):return subprocess.check_output(git+list(args),text=True).strip()
assert run('rev-parse','HEAD')=='d362e7536523dd18a4972c10b9c4ab0212a96453'
assert not run('diff','--cached','--name-only')
paths=[B/'README.md',*sorted((B/'Scripts').glob('*.py')),*sorted((B/'Records').glob('*.json')),B/'Records/report.md',B/'Records/owner-production-handoff.txt']
paths=[p for p in paths if p.name!='sync-verification.json']
paths.extend(B/'Previews'/name for name in ['entry.png','interaction.png','diffuser.png','integrated.png','chronological-contact-sheet.jpg','review.html'])
paths.extend(ROOT/f'04-Production/Shots/S05/S05-{part}/direction.md' for part in 'ABC')
rels=[]
for p in paths:
 rel=p.relative_to(ROOT);q=D/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
 backup=recovery/rel;backup.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,backup)
 rels.append(rel.as_posix())
subprocess.run(git+['add','--']+rels,check=True)
actual=set(run('diff','--cached','--name-only').splitlines())
assert actual.issubset(set(rels)) and len(actual)>20
# Preserve exact owner handoff, including its five Markdown hard line breaks.
subprocess.run(git+['diff','--cached','--check','--','.',':(exclude)**/owner-production-handoff.txt'],check=True)
print(run('diff','--cached','--stat'))
print(json.dumps({'staged_paths':len(actual),'checkout':str(D)}))
