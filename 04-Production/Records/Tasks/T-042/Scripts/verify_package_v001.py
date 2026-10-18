"""Validate P01 coverage, local references, source preservation and review file hashes."""
import json, pathlib, re, hashlib, struct
ROOT=pathlib.Path(__file__).resolve().parents[5]
TASK=ROOT/'04-Production/Records/Tasks/T-042'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
 return h.hexdigest()
checks=[]
def check(name,result):checks.append({'check':name,'pass':bool(result)})
m=json.loads((TASK/'shot-map_v001.json').read_text(encoding='utf-8'))
shots=m['shots']; ids=[s['id'] for s in shots]
expected=[f'S0{s}-{letter}' for s in range(1,8) for letter in ('ABCD' if s==4 else 'ABC')]
check('Exactly the 22 V3 IDs in order',ids==expected)
check('Contiguous 0–90 second coverage',shots[0]['start_s']==0 and shots[-1]['end_s']==90 and all(a['end_s']==b['start_s'] for a,b in zip(shots,shots[1:])))
check('Positive durations total 90 seconds',all(s['end_s']>s['start_s'] for s in shots) and sum(s['end_s']-s['start_s'] for s in shots)==90)
components={'ECCO','BHA','WELL','SURFACE','MUD','ACOUSTICS','DATA','CASING','FLOW','GRAPHICS','OUTPUT','BRAND'}
check('All 12 components have consumers and no unknown IDs',set(c for s in shots for c in s['components'])==components)
for s in shots:
 check(s['id']+' source exists',(ROOT/s['source']).is_file())
 check(s['id']+' direction remains unfilled',all(s[k] is None for k in ['camera','look','event_frames','approved_by']))
b=json.loads((TASK/'Evidence/source-index_v001.json').read_text(encoding='utf-8'))
check('Live board index includes 22 shot cards',len([c for c in b['cards'] if re.match(r'S0[1-7]-[A-D]',c['title'])])==22)
check('Start guide and seven sequence guides indexed',len(b['cards'])==30)
a=json.loads((TASK/'Evidence/asset-inspection_v001.json').read_text(encoding='utf-8'))
for rec in a['assets']:
 check(rec['path']+' opens and preserved',rec.get('opened') and rec.get('source_unchanged') and sha(ROOT/rec['path'])==rec['sha256'])
 check(rec['path']+' image and library dependencies',not rec.get('missing_images') and all(l['exists'] for l in rec.get('libraries',[])))
idxpath=ROOT/'04-Production/Mechanisms/B202/Data/v009/index_v009.json'
idx=json.loads(idxpath.read_text(encoding='utf-8'))
check('B202 registered source hashes match current files',all(sha(ROOT/p)==h for p,h in idx['source_hashes'].items()))
check('All indexed B202 case files exist',all((idxpath.parent/p).is_file() for c in idx['cases'].values() for p in c['files'].values()))
for p in TASK.glob('*.md'):
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
  if '://' in target:continue
  target=target.split('#')[0]
  check(p.name+' link '+target,(p.parent/target).exists())
logo=ROOT/'03-Context/02_Storyboard/V3/ECCO_Section_07_Cinematic_Rich_Direction_Separated/S07_C_MIT_Brand_Closing/MIT_Official_Logo_Supplied_Unaltered.png'
check('Supplied original logo exists',logo.is_file())
raw=logo.read_bytes();check('Supplied logo PNG header',raw[:8]==b'\x89PNG\r\n\x1a\n')
manifest=[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(TASK.rglob('*')) if p.is_file() and p.name!='package-verification_v001.json']
out={'checks':checks,'passed':sum(c['pass'] for c in checks),'failed':[c for c in checks if not c['pass']],
 'logo':{'path':logo.relative_to(ROOT).as_posix(),'sha256':sha(logo),'dimensions_px':struct.unpack('>II',raw[16:24])},
 'data_index':{'path':idxpath.relative_to(ROOT).as_posix(),'sha256':sha(idxpath),'case_count':len(idx['cases'])},
 'outputs':manifest,'limits':'Self-checks of planning coverage and saved-file availability. No render, visual acceptance or engineering certification.'}
(TASK/'Evidence/package-verification_v001.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps({'passed':out['passed'],'failed':out['failed'],'outputs':len(manifest),'logo':out['logo']}))
raise SystemExit(bool(out['failed']))
