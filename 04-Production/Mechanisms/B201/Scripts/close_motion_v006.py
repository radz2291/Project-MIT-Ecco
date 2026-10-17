"""Verify retained local files and Markdown links before explicit-path sync."""
import json,re,hashlib
from pathlib import Path
P=Path(__file__).resolve().parents[3]; root=P.parent; task=P/'Records/Tasks/T-007'; E=task/'Evidence/Motion_v006'
files=json.loads((task/'sync-files_motion_v006.json').read_text()); missing=[]; links=[]
for rel in files:
 p=root/rel
 if p.name=='closure.json': continue
 if not p.is_file(): missing.append(rel)
 if p.suffix=='.md':
  for target in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8-sig')):
   target=target.split('#')[0]
   if not target or '://' in target: continue
   dest=(p.parent/target).resolve(); links.append(dict(source=rel,target=target,exists=dest.is_file()))
manifest=json.loads((E/'output-manifest.json').read_text()); hashes={rel:hashlib.sha256((P/rel).read_bytes()).hexdigest()==h for rel,h in manifest.items()}
result=dict(passed=not missing and all(x['exists'] for x in links) and all(hashes.values()),missing=missing,local_markdown_links=links,output_hashes_match=hashes,heavy_media_remote_backup=False,executor_self_check=True)
(E/'closure.json').write_text(json.dumps(result,indent=2)); print('CLOSURE',result['passed'],'links',len(links),'outputs',len(hashes)); assert result['passed'],result
