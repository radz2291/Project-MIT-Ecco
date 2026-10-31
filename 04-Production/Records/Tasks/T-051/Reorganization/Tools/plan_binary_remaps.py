"""Read-only plan and full-original backup budget from the finished inventory."""
import pathlib,json,ntpath
R=pathlib.Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');T=R/'04-Production/Records/Tasks/T-051/Reorganization'
def norm(p):return ntpath.normcase(ntpath.normpath(str(p)))
inv=json.loads((T/'all-blend-paths-before.json').read_text());assert inv['complete'],'Wait for complete scan';assert all(x['ok'] for x in inv['files']),'Parser errors need review'
moves=json.loads((T/'move-plan.json').read_text());mapping={norm(R/x['old']):str(R/x['new']) for x in moves};plans=[];review=[];allowed={x['old'] for x in moves if x['kind'] in ('active','demo') and x['old'].endswith('.blend')}
for f in inv['files']:
 if f['path'] not in allowed:continue
 old_owner=str(R/f['path']);new_owner=mapping.get(norm(old_owner),old_owner);edits=[]
 if norm(new_owner).startswith(norm(R/'04-Production/Shared/Sources')+'\\'):continue
 for x in f['paths']:
  if x['value'].startswith('<') or x['value'] in ('Bfont','Bfont Regular'):continue
  resolved=x['resolved_from_owning_blend'];target=mapping.get(norm(resolved),resolved);value=x['value'];mapped=norm(resolved) in mapping;relative=value.startswith('//') or not ntpath.isabs(value)
  # Real dependencies/provenance; exclude UI/render destinations from implicit owner-rebasing.
  dependency=x['library'] or x['struct']=='LibraryWeakReference' or x.get('external_candidate',False)
  if not mapped and not (dependency and relative and norm(new_owner)!=norm(old_owner)):continue
  if relative:new='//'+ntpath.relpath(target,ntpath.dirname(new_owner)).replace('\\','/')
  else:new=ntpath.normpath(target)
  if new==value:continue
  if len(new.encode('utf8'))>=x['capacity']:review.append({'owner':f['path'],'reason':'capacity overflow','field':x,'new':new});continue
  if not x['exists'] and not mapped:review.append({'owner':f['path'],'reason':'pre-existing missing target; rebasing only preserves prior meaning','field':x,'new':new})
  edits.append({'offset':x['offset'],'capacity':x['capacity'],'struct':x['struct'],'field':x['field'],'old':value,'new':new,'resolved_before':resolved,'resolved_after':target,'target_explicitly_moved':mapped})
 if edits:plans.append({'old_owner':f['path'],'new_owner':ntpath.relpath(new_owner,str(R)).replace('\\','/'),'sha256_before':f['sha256'],'bytes_before':f['bytes'],'container':f['container'],'edits':edits})
result={'read_only':True,'scanned':len(inv['files']),'changed_files':len(plans),'changed_fields':sum(len(x['edits']) for x in plans),'full_original_backup_bytes':sum(x['bytes_before'] for x in plans),'full_original_backup_GiB':sum(x['bytes_before'] for x in plans)/2**30,'largest_changed_bytes':max((x['bytes_before'] for x in plans),default=0),'plans':plans,'review':review,'policy':'Exact target move map; relative dependency paths rebased from each owning file after owner move. Includes Library.name, weakrefs and recognized resource arrays; UI/render outputs excluded from implicit rebasing. No actual writes.'}
(T/'binary-remap-plan.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k not in ('plans','review')},indent=2));print('REVIEW_ITEMS',len(review))
