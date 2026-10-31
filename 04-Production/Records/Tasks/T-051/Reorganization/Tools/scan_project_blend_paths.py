"""Read-only complete project .blend/.blendN inventory. JSON progress after each file."""
import pathlib,json,time,hashlib,os,re,ntpath
from blend_path_bytes import Blend
R=pathlib.Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');T=R/'04-Production/Records/Tasks/T-051/Reorganization';files=sorted(p for p in R.rglob('*') if p.is_file() and re.search(r'\.blend\d*$',p.name,re.I));out=[];started=time.time()
for i,p in enumerate(files):
 t=time.perf_counter();row={'path':p.relative_to(R).as_posix(),'bytes':p.stat().st_size}
 try:
  data=p.read_bytes();row['sha256']=hashlib.sha256(data).hexdigest();b=Blend(data);paths=b.paths()
  for x in paths:
   value=x['value']
   if value.startswith('//'):resolved=ntpath.normpath(ntpath.join(str(p.parent),value[2:]))
   elif ntpath.isabs(value):resolved=ntpath.normpath(value)
   else:resolved=ntpath.normpath(ntpath.join(str(p.parent),value))
   x['resolved_from_owning_blend']=resolved;x['exists']=os.path.exists(resolved);x['resolution_note']='Relative to this on-disk owning blend; transitive libraries are independently scanned, not recursively rebased from another main file.'
  row.update({'container':b.container[0],'format':b.header.file_format_version,'version':b.header.version,'paths':paths,'ok':True})
 except Exception as e:row.update({'ok':False,'error':repr(e)})
 row['seconds']=time.perf_counter()-t;out.append(row)
 (T/'all-blend-paths-before.json').write_text(json.dumps({'root':str(R),'expected_count':len(files),'scanned':len(out),'complete':len(out)==len(files),'elapsed_seconds':time.time()-started,'files':out},indent=2))
 if (i+1)%20==0 or not row['ok']:print('SCAN',i+1,'/',len(files),'ok',sum(x['ok'] for x in out),flush=True)
print('SCAN_COMPLETE',len(files),'errors',sum(not x['ok'] for x in out),flush=True)
