import pathlib,json,gzip
from blend_path_bytes import Blend,patch_bytes,decode
from blend_rollback_delta import create_delta,restore
T=pathlib.Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/Records/Tasks/T-051/Reorganization');R=T.parents[3];sample=pathlib.Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/Records/Tasks/T-056/Demos/Waveform_demo_v015.blend').read_bytes();raw,_=decode(sample);out=[]
for name,data in [('actual_zstd',sample),('raw',raw),('gzip',gzip.compress(raw,mtime=0))]:
 b=Blend(data);p=next(x for x in b.paths() if x['library']);new,proof=patch_bytes(data,{p['offset']:'//Effects/Acoustics/longer-new-path.blend'});delta=create_delta(data,new,proof);assert restore(new,delta)==data
 try:restore(new+b'X',delta)
 except AssertionError:stale_rejected=True
 else:stale_rejected=False
 assert stale_rejected;out.append({'container':name,'original_bytes':len(data),'delta_json_bytes':len(json.dumps(delta).encode()),'exact_original_SHA_restored':True,'stale_postimage_rejected':True,'changes':len(delta['changes'])})
(T/'rollback-delta-tests.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
