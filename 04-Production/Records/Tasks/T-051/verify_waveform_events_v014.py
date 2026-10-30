import bpy,json,pathlib,math,numpy as np
R=pathlib.Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');T=R/'04-Production/Records/Tasks/T-056'
mapping=json.loads((T/'consumer-mapping_v014.json').read_text());results=[]
for m in mapping:
 bpy.ops.wm.open_mainfile(filepath=m['candidate'],load_ui=False);s=bpy.context.scene
 for inst in m['instances']:
  vals=inst['settings'];start=vals['Start Frame'];end=vals['Return End Frame'];ob=bpy.data.objects[inst['object']];a=np.array(inst['start']);b=np.array(inst['wall']);axis=b-a;gap=np.linalg.norm(axis);axis/=gap
  samples=[]
  for f in sorted(set([math.floor(start)-1,math.ceil(start)+2,math.floor(start+vals['Travel Override']/2),math.floor(end)-3,math.ceil(end)+1,math.ceil(end)+4])):
   s.frame_set(f);ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();n=len(me.vertices);co=np.empty(n*3);me.vertices.foreach_get('co',co);co=co.reshape(-1,3);ev.to_mesh_clear()
   samples.append({'frame':f,'vertices':n,'axial_min_max': [float((co@axis).min()),float((co@axis).max())] if n else None})
  checks={'nonzero_gap':gap>.001,'gap_matches_endpoint_distance':abs(gap-vals['Gap Length m'])<1e-7,'quiet_before_start':all(x['vertices']==0 for x in samples if x['frame']<start),'quiet_after_end':all(x['vertices']==0 for x in samples if x['frame']>end),'active_during_event':any(x['vertices']>0 for x in samples if start<x['frame']<end)}
  checks={k:bool(v) for k,v in checks.items()}
  results.append({'consumer':m['name'],'instance':inst['object'],'samples':samples,'checks':checks,'pass':all(checks.values())})
(R/'04-Production/Records/Tasks/T-051/Evidence/waveform-events-v014-independent.json').write_text(json.dumps(results,indent=2));print(json.dumps(results))
if not all(x['pass'] for x in results):raise SystemExit(1)
