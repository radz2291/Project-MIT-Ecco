from pathlib import Path
import json,hashlib,re
here=Path(__file__).parent
root=here.parents[3]
files=list(here.glob('*.md'))+[root/'04-Production/Records/asset-manifest_v001.md']+[root/'03-Context/01_Foundation'/f for f in ['02-ENGINEERING_BASELINE.md','05-PRODUCTION_WORKFLOW.md','06-DECISIONS_AND_READINESS.md']]
links=[];bad=[]
for p in files:
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
  if '://' in target or target.startswith('#'):continue
  target=target.split('#')[0]
  if not target:continue
  q=p.parent/target;links.append(str(q))
  if not q.exists():bad.append(str(q))
records=[]
for n in ['local-input-inventory_v001.json','external-inputs_v001.json']:
 for r in json.loads((here/'Evidence'/n).read_text()):
  p=Path(r['path']); records.append(dict(path=str(p),exists=p.exists(),hash_matches=p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256']))
assert not bad,bad
assert all(r['hash_matches'] for r in records)
result=dict(markdown_files=len(files),relative_links=len(links),broken_links=bad,source_hash_checks=len(records),all_hashes_match=True,all_retained_files_nonempty=all(p.stat().st_size>0 for p in here.rglob('*') if p.is_file()))
(here/'Evidence/closure-check_v001.json').write_text(json.dumps(result,indent=2))
print(result)
