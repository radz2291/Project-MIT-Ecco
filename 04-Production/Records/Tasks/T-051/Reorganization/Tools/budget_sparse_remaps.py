import pathlib,json,hashlib,time
from blend_rollback_delta import budget
R=pathlib.Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');T=R/'04-Production/Records/Tasks/T-051/Reorganization';p=json.loads((T/'binary-remap-plan.json').read_text());out=[]
for i,x in enumerate(p['plans']):
 data=(R/x['old_owner']).read_bytes();assert hashlib.sha256(data).hexdigest()==x['sha256_before'],'source drift';b=budget(data,x['container'],[(e['offset'],e['offset']+e['capacity']) for e in x['edits']]);out.append({'path':x['old_owner'],**b})
 if (i+1)%100==0:print('BUDGET',i+1,flush=True)
result={'files':len(out),'all_source_hashes_match':True,'payload_upper_bytes':sum(x['original_payload_bytes_upper'] for x in out),'json_upper_bytes':sum(x['delta_json_bytes_upper'] for x in out),'largest_native_bytes':p['largest_changed_bytes'],'items':out};result['recommended_free_bytes']=result['json_upper_bytes']+2*result['largest_native_bytes']+256*1024**2;(T/'sparse-backup-budget.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='items'}))
