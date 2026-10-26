from pathlib import Path
from PIL import Image, ImageStat
from html.parser import HTMLParser
import json, hashlib, re, ast
R=Path(__file__).resolve().parents[5];T=R/'04-Production/Records/Tasks/T-049'
def j(p):return json.loads((T/p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def ck(name,ok,detail=None):checks.append({'check':name,'pass':bool(ok),'detail':detail})
sources=j('sources.json');audit=j('Evidence/source-audit.json');ims=j('Evidence/image-manifest.json');media=j('Evidence/media-audit.json')
for s in sources:
    a=next(x for x in audit if x['id']==s['id']);p=R/s['native'];ck('native-'+s['id'],p.exists() and sha(p)==a['sha256'])
    for l in a['libraries']:
        p=Path(l['resolved']);ck('library-'+s['id']+'-'+p.name,p.exists() and sha(p)==l['sha256'])
    for i in a['images']:
        if i['path'] and i['source']!='GENERATED':ck('image-dependency-'+s['id']+'-'+i['name'],i['packed'] or Path(i['resolved']).exists())
    for f in a['fonts']:
        if f['path'] and f['path']!='<builtin>':ck('font-'+s['id']+'-'+f['name'],f['packed'] or Path(f['path']).exists(),f['path'])
    ck('raw-inspection-'+s['id'],sha(T/'Evidence'/f"{s['id']}_native.json")==a['raw_evidence_sha256'])
for m in media:
    ck('movie-'+m['id'],sha(R/m['video'])==m['sha256'] and m['decoded_frames']>0 and m['decode_errors']==0)
for x in ims:
    p=T/x['image'];src=R/x['source'];ck('image-source-'+x['id'],src.exists() and sha(src)==x['source_sha256'])
    ck('image-native-'+x['id'],(R/x['native']).exists())
    ck('image-derivative-'+x['id'],sha(p)==x['sha256'])
    with Image.open(p) as im:
        ck('image-size-'+x['id'],list(im.size)==x['dimensions']);ck('image-nonblank-'+x['id'],max(ImageStat.Stat(im.convert('RGB')).stddev)>1)
    ck('no-restricted-source-'+x['id'],not re.search('PRIVATE_REFERENCE|BoreholeLog_Report|Originals/Private',x['source'],re.I))
def link(target,origin):
    if target.startswith(('http:','https:','#','mailto:')):return
    p=origin.parent/target.split('#')[0];ck('link-'+origin.name+'-'+target,p.exists())
for p in T.glob('*.md'):
    for target in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):link(target,p)
class Parser(HTMLParser):
    def handle_starttag(self,tag,attrs):
        for k,v in attrs:
            if k in ('src','href'):link(v,T/'review.html')
Parser().feed((T/'review.html').read_text(encoding='utf-8'))
for p in (T/'Scripts').glob('*.py'):
    ast.parse(p.read_text(encoding='utf-8'));ck('python-syntax-'+p.name,True)
ck('25-native-sources',len(audit)==25);ck('30-source-images',len(ims)==30);ck('2376-decoded-frames',sum(m['decoded_frames'] for m in media)==2376)
for name in ['01-seven-section-baseline.jpg','02-hardware-and-world.jpg','03-sensing-and-casing.jpg','04-flow-and-data.jpg']:
    with Image.open(T/'Images'/name) as im:im.verify()
    ck('sheet-'+name,True)
result={'status':'PASS' if all(c['pass'] for c in checks) else 'FAIL','checks':len(checks),'failed':[c for c in checks if not c['pass']],'results':checks,'limits':'Executor inspection. No new render or independent technical/creative acceptance. Raw native evidence remains local.'}
(T/'Evidence/verification.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='results'},indent=2))
raise SystemExit(0 if result['status']=='PASS' else 1)
