"""Read originals, prepare sparse rollback JSON and exact-byte proof. NO native writes."""
import pathlib,json,hashlib,os,time
from blend_path_bytes import Blend,patch_bytes
from blend_rollback_delta import create_delta,restore
R=pathlib.Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');T=R/'04-Production/Records/Tasks/T-051/Reorganization';B=T/'Backup/deltas';B.mkdir(parents=True,exist_ok=True);plan=json.loads((T/'binary-remap-plan.json').read_text());records=[];started=time.time();prior=T/'sparse-remap-prepared.json';existing={x['old_owner']:x for x in json.loads(prior.read_text())['records']} if prior.exists() else {};reused=0
for i,x in enumerate(plan['plans']):
 assert not x['new_owner'].startswith('04-Production/Shared/Sources/'),'Supplied source must stay byte exact'
 data=(R/x['old_owner']).read_bytes();assert hashlib.sha256(data).hexdigest()==x['sha256_before'],'Source drift'
 old=existing.get(x['old_owner'])
 if old and old['original_sha256']==x['sha256_before'] and old['new_owner']==x['new_owner']:
  blob=(R/old['delta']).read_bytes();assert hashlib.sha256(blob).hexdigest()==old['delta_sha256'];delta=json.loads(blob);assert delta['original_sha256']==x['sha256_before'];record=old;reused+=1
 else:
  b=Blend(data);fields={p['offset']:p for p in b.paths()}
  for e in x['edits']:assert fields[e['offset']]['value']==e['old'] and fields[e['offset']]['capacity']==e['capacity'],'Field drift'
  patched,proof=patch_bytes(data,{e['offset']:e['new'] for e in x['edits']});delta=create_delta(data,patched,proof);assert restore(patched,delta)==data
  filename=x['sha256_before'][:16]+'_'+hashlib.sha256(x['old_owner'].encode()).hexdigest()[:12]+'.json';target=B/filename;blob=json.dumps(delta,separators=(',',':')).encode();tmp=target.with_suffix('.tmp');tmp.write_bytes(blob);os.replace(tmp,target)
  record={'old_owner':x['old_owner'],'new_owner':x['new_owner'],'original_sha256':delta['original_sha256'],'patched_sha256':delta['patched_sha256'],'delta':target.relative_to(R).as_posix(),'delta_sha256':hashlib.sha256(blob).hexdigest(),'delta_bytes':len(blob),'proof':proof,'exact_original_restored_in_memory':True}
 record['original_bytes']=delta['original_bytes'];record['patched_bytes']=delta['patched_bytes'];record['growth_bytes']=delta['patched_bytes']-delta['original_bytes'];records.append(record)
 result={'complete':len(records)==len(plan['plans']),'files':len(records),'expected':len(plan['plans']),'reused_prior_proofs':reused,'delta_total_bytes':sum(v['delta_bytes'] for v in records),'total_native_growth_bytes':sum(v['growth_bytes'] for v in records),'maximum_patched_file_bytes':max(v['patched_bytes'] for v in records),'elapsed_seconds':time.time()-started,'native_files_written':0,'records':records};j=T/'sparse-remap-prepared.json';tmp=j.with_suffix('.json.tmp');tmp.write_text(json.dumps(result,indent=2));os.replace(tmp,j)
 if (i+1)%20==0:print('PREPARED',i+1,'/',len(plan['plans']),flush=True)
print('ALL_PREPARED',len(records),result['delta_total_bytes'],flush=True)
