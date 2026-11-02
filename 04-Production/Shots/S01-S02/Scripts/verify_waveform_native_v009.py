import bpy,json,hashlib,numpy as np
from pathlib import Path
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');Q=R/'04-Production/Shots/S01-S02';records=[]
def action_hash(ad):
 data=[]
 for l in ad.action.layers:
  for st in l.strips:
   for bag in st.channelbags:
    if bag.slot_handle!=ad.action_slot.handle:continue
    for fc in bag.fcurves:data.append([fc.data_path,fc.array_index,[[float(k.co.x),float(k.co.y),k.interpolation] for k in fc.keyframe_points]])
 return hashlib.sha256(json.dumps(data).encode()).hexdigest()
for version in ['007','009']:
 p=Q/f'Scenes/S01-S02_production_v{version}.blend';bpy.ops.wm.open_mainfile(filepath=str(p));s=bpy.context.scene;c=s.camera;row={'version':version,'camera':action_hash(c.animation_data),'lens':action_hash(c.data.animation_data),'wall':{},'field':{}}
 for f in [299,309,311,318,328,336]:
  s.frame_set(f);bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();wall=bpy.data.objects['ONE WALL - old history and current cells share topology'];ev=wall.evaluated_get(dg);me=ev.to_mesh();co=np.array([v.co[:] for v in me.vertices]);row['wall'][str(f)]=hashlib.sha256(co.tobytes()+str(len(me.polygons)).encode()).hexdigest();ev.to_mesh_clear()
  ob=bpy.data.objects['WF sequence event 1'];ev=ob.evaluated_get(dg);me=ev.to_mesh();counts={'vertices':len(me.vertices)}
  for attr,key in [('wf_out_envelope','out'),('wf_return_envelope','ret')]:
   a=me.attributes.get(attr);counts[key]=max((x.value for x in a.data),default=0.) if a else None
  row['field'][str(f)]=counts;ev.to_mesh_clear()
 row['wave_groups']={o.name:[m.node_group.name for m in o.modifiers if m.type=='NODES'] for o in s.objects if o.name.startswith('WF sequence event')};row['libraries']=[{'path':l.filepath,'exists':Path(bpy.path.abspath(l.filepath)).exists()} for l in bpy.data.libraries];records.append(row)
assert records[0]['camera']==records[1]['camera'] and records[0]['lens']==records[1]['lens']
assert records[0]['wall']==records[1]['wall']
assert records[1]['field']['299']['vertices']==0 and records[1]['field']['318']['vertices']==0 and records[1]['field']['328']['vertices']==0
assert records[1]['field']['311']['out']>0 and records[1]['field']['311']['ret']>0
assert all(x['exists'] for x in records[1]['libraries'])
for i in range(2,7):assert records[0]['wave_groups'][f'WF sequence event {i}']==records[1]['wave_groups'][f'WF sequence event {i}']
(Q/'Notes/waveform_v009_native_verification.json').write_text(json.dumps({'pass':True,'records':records,'no_native_save':True},indent=2));print('NATIVE_V009_PASS')
