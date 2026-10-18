"""Hash exact released child records and verify manifest-listed local artifacts.

Ordinary Python. Run only after builders freeze their final manifests. This is
integrator verification, separate from fresh-context candidate review.
"""
import argparse,hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def rel(path):return path.relative_to(ROOT).as_posix()

def records(value):
    if isinstance(value,dict):
        if isinstance(value.get('path'),str) and isinstance(value.get('sha256'),str):yield value
        for item in value.values():yield from records(item)
    elif isinstance(value,list):
        for item in value:yield from records(item)

def main():
    p=argparse.ArgumentParser();p.add_argument('manifests',nargs='+',type=Path)
    a=p.parse_args();rows=[];inputs=[]
    for manifest in a.manifests:
        manifest=manifest.resolve();data=json.loads(manifest.read_text(encoding='utf-8-sig'))
        inputs.append({'path':rel(manifest),'sha256':sha(manifest)})
        seen=set()
        for record in records(data):
            path=Path(record['path'])
            if not path.is_absolute():path=ROOT/path
            path=path.resolve()
            if path in seen:continue
            seen.add(path)
            actual=sha(path) if path.is_file() else None
            rows.append({'manifest':rel(manifest),'path':rel(path),'expected_sha256':record['sha256'],
                         'actual_sha256':actual,'bytes':path.stat().st_size if path.is_file() else None,
                         'pass':actual==record['sha256'],'storage':'local Git-ignored' if path.suffix.lower() in ['.blend','.mp4'] else 'tracked review record or selected image'})
    result={'task':'T45','upstream':'a08d0ecfbd6f3241298f506b3ea42613388b3baf','manifests':inputs,
            'artifacts':rows,'all_pass':all(r['pass'] for r in rows),'scope':'Exact local artifact integrity; native behavior and human acceptance require separate evidence',
            'backup':'Heavy native/video/raw/cache files remain local. No off-machine backup established.'}
    out=HERE/'Evidence/package-integrity_v001.json';out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'manifest_count':len(inputs),'artifacts':len(rows),'all_pass':result['all_pass'],'output':str(out)}))
    if not rows or not result['all_pass']:raise SystemExit(1)
if __name__=='__main__':main()
