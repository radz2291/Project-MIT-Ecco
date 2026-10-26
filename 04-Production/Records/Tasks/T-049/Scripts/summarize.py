import json, pathlib, hashlib, collections, re
R=pathlib.Path(__file__).resolve().parents[5]; T=R/'04-Production/Records/Tasks/T-049'
sources=json.loads((T/'sources.json').read_text())
all_data={s['id']:json.loads((T/'Evidence'/f"{s['id']}_native.json").read_text()) for s in sources if (T/'Evidence'/f"{s['id']}_native.json").exists()}
groups={'ECCO':r'ECCO|ENP3|housing|sensor|cap_|plug','BHA-bit-connection':r'BHA|bit|collar|adapter|joint|extension|drill|string','environment':r'rock|formation|bore|well|ground|surface|ocean|rig|water|terrain|casing|cement|channel|wear|steel','sensing-data-graphics':r'acoustic|pulse|echo|contact|return|send|wave|record|sample|nominal|wall|profile|map|grid|HUD|label|title|text|amplitude|measur','flow':r'flow|cutting|tracer|hydraul|fluid|mud'}
compact=[]; members=[]
for id,d in all_data.items():
    match=collections.defaultdict(list)
    for o in d['objects']:
        names=' '.join([o['name'],o['data'] or '',*o['collections']])
        cats=[k for k,v in groups.items() if re.search(v,names,re.I)]
        if not cats and o['type'] in ('LIGHT','CAMERA'): cats=[o['type'].lower()]
        for k in cats: match[k].append(o['name'])
        members.append({'source':id,'name':o['name'],'type':o['type'],'categories':cats,'ownership':'linked' if o['library'] else 'local (append versus authored requires provenance)','library':o['library'],'data_library':o['data_library'],'collections':o['collections'],'instance':o['instance'],'instance_library':o['instance_library'],'data':o['data'],'geometry_sha256':d['meshes'].get(o['data'],{}).get('geometry_sha256'),'materials':o['materials']})
    c={'id':id,'native':d['native'],'sha256':d['native_sha256'],'unchanged':d['source_unchanged'],'scenes':d['scenes'],'libraries':d['libraries'],'cameras':[{'name':c['name'],'lens':c['lens'],'camera_animation_sha256':hashlib.sha256(json.dumps(c['animation'],sort_keys=True).encode()).hexdigest(),'lens_animation_sha256':hashlib.sha256(json.dumps(c['data_animation'],sort_keys=True).encode()).hexdigest()} for c in d['cameras']],'images':d['images'],'fonts':d['fonts'],'counts':{'objects':len(d['objects']),'local_objects':sum(not o['library'] for o in d['objects']),'linked_objects':sum(bool(o['library']) for o in d['objects']),'materials':len(d['materials']),'meshes':len(d['meshes'])},'categories':{k:len(v) for k,v in match.items()},'object_state_sha256':hashlib.sha256(json.dumps(d['objects'],sort_keys=True).encode()).hexdigest(),'materials_sha256':hashlib.sha256(json.dumps(d['materials'],sort_keys=True).encode()).hexdigest(),'raw_evidence_sha256':hashlib.sha256((T/'Evidence'/f'{id}_native.json').read_bytes()).hexdigest()}
    compact.append(c)
    if id.startswith('S0'):
        print(id,c['counts'],d['scenes'])
        print('LIBRARIES',[pathlib.Path(l['resolved']).name for l in d['libraries']])
        print('LOCAL SAMPLE',[o['name'] for o in d['objects'] if not o['library']][:38])
        print('MATERIALS',[m['name'] for m in d['materials']][:30])
by_hash=collections.defaultdict(list)
for m in members:
    if m['geometry_sha256']: by_hash[m['geometry_sha256']].append({'source':m['source'],'name':m['name'],'data':m['data']})
dupes=[{'geometry_sha256':h,'objects':a} for h,a in by_hash.items() if len({o['source'] for o in a})>1]
(T/'Evidence/source-audit.json').write_text(json.dumps(compact,indent=2))
(T/'Evidence/component-members.json').write_text(json.dumps(members,separators=(',',':')))
(T/'Evidence/geometry-matches.json').write_text(json.dumps(dupes,indent=2))
(T/'Evidence/native-summary.json').write_text(json.dumps([{'id':d['id'],'native':d['native'],'sha256':d['sha256'],'unchanged':d['unchanged'],'objects':d['counts']['objects'],'libraries':len(d['libraries']),'missing_libraries':[l for l in d['libraries'] if not l['exists']]} for d in compact],indent=2))
print('SOURCES',len(compact),'MEMBERS',len(members),'CROSS-SOURCE MESH MATCHES',len(dupes))
