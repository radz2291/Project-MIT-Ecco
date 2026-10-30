"""Bounded local signal-data inventory; no client sample values/images are copied."""
from pathlib import Path
import json,gzip,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parents[4];TASK=Path(__file__).resolve().parent
extensions={'.csv','.npz','.npy','.mat','.h5','.hdf5','.bin','.las','.dlis','.dat','.xlsx','.exe'}
excluded={'Cache','Scratch','node_modules','.git','__pycache__'}
candidates=[]
for folder in ['01-Brief','02-Reference','03-Context','04-Production','05-Previs']:
 for p in (ROOT/folder).rglob('*'):
  if p.is_file() and p.suffix.lower() in extensions and not any(x in excluded for x in p.parts):
   candidates.append({'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size})
npz=[]
for row in candidates:
 p=ROOT/row['path']
 if p.suffix=='.npz':
  with np.load(p,allow_pickle=False) as z:
   fields={}
   for key in z.files:
    try:a=z[key];fields[key]={'shape':list(a.shape),'dtype':str(a.dtype)}
    except ValueError:fields[key]={'status':'object array not loaded'}
   npz.append({'path':row['path'],'fields':fields})
events=ROOT/'04-Production/Mechanisms/B202/Data/v009/irregular_layers_events_v009.json.gz'
data=json.loads(gzip.decompress(events.read_bytes()));first=data[0] if isinstance(data,list) else data
out={'search_roots':['01-Brief','02-Reference','03-Context','04-Production','05-Previs'],'excluded_directory_names':sorted(excluded),'extensions':sorted(extensions),'candidate_files':candidates,'npz_headers':npz,'B202_event_example':{'path':events.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(events.read_bytes()).hexdigest(),'top_type':type(data).__name__,'event_keys':list(first),'source_kind':first.get('source_kind') if isinstance(first,dict) else None},'conclusion':'No identified recorded RF time-amplitude series in bounded local candidates. B202 supplies authored scalar TOF/strength; NPZ candidates require their existing synthetic/derived provenance. File-extension search cannot prove absence in unexamined files or external machines.'}
(TASK/'local-signal-data-audit.json').write_text(json.dumps(out,indent=2))
print(json.dumps({'candidate_count':len(candidates),'npz_count':len(npz),'B202_event_keys':out['B202_event_example']['event_keys']}))
