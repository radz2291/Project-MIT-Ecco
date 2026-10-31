import pathlib,json,hashlib,gzip,time
from blend_path_bytes import Blend,patch_bytes,decode
R=pathlib.Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');T=R/'04-Production/Records/Tasks/T-051/Reorganization';sample=R/'04-Production/Records/Tasks/T-056/Demos/Waveform_demo_v015.blend';data=sample.read_bytes();original=hashlib.sha256(data).hexdigest();raw,_=decode(data);out=[]
for kind,encoded in [('actual_zstd',data),('raw',raw),('gzip',gzip.compress(raw,mtime=0))]:
 b=Blend(encoded);item=next(x for x in b.paths() if x['library']);new='//TEST_ONLY/longer/path/Waveform_shared_v015.blend';patched,proof=patch_bytes(encoded,{item['offset']:new});r=Blend(patched);assert next(x for x in r.paths() if x['offset']==item['offset'])['value']==new;out.append({'test':kind,'pass':True,**proof})
try:patch_bytes(data,{item['offset']:'X'*1024})
except AssertionError:out.append({'test':'overflow rejected','pass':True})
else:raise AssertionError('overflow accepted')
assert hashlib.sha256(sample.read_bytes()).hexdigest()==original
scan=[]
for rel in ['04-Production/Shared/Assets/Acoustics/Waveform_shared_v014/Waveform_shared_v014.blend','04-Production/Shared/Assets/Acoustics/Waveform_shared_v015/Waveform_shared_v015.blend','04-Production/Shared/Assets/BHA/BHA_film_v007.blend','05-Previs/Section-02_Measurement-History/v011/Continuation/Scenes/S01-S02_continuous_v011.blend','04-Production/Shots/S04/S04-A/Previs_v033/Scenes/S04_continuous_ABCD_v033.blend']:
 p=R/rel;t=time.perf_counter()
 try:b=Blend(p.read_bytes());paths=b.paths();scan.append({'path':rel,'seconds':time.perf_counter()-t,'container':b.container[0],'header_format':b.header.file_format_version,'library_paths':[x['value'] for x in paths if x['library']],'all_path_candidates':len(paths),'pass':True})
 except Exception as e:scan.append({'path':rel,'pass':False,'error':str(e)})
(T/'binary-parser-readonly-tests.json').write_text(json.dumps({'roundtrips':out,'samples':scan,'sample_source_unchanged':True,'blend_files_written':0},indent=2));print(json.dumps({'roundtrips_pass':all(x['pass'] for x in out),'samples':scan},indent=2))
