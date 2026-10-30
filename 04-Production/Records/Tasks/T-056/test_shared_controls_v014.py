import bpy,pathlib,json,numpy as np,hashlib
R=pathlib.Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');T=R/'04-Production/Records/Tasks/T-056';master=R/'04-Production/Shared/Assets/Acoustics/Waveform_shared_v014/Waveform_shared_v014.blend';mapping=json.loads((T/'consumer-mapping_v014.json').read_text());original=master.read_bytes();localpath=pathlib.Path(mapping[0]['candidate']);localbytes=localpath.read_bytes();checks=[]
def val(mod,name,value):
 ident=next(x.identifier for x in mod.node_group.interface.items_tree if getattr(x,'in_out','')=='INPUT' and x.name==name);getattr(mod.properties.inputs,ident).value=value;mod.id_data.update_tag(refresh={'OBJECT','DATA','TIME'});bpy.context.view_layer.update()
def snapshot(name,frame):
 bpy.context.scene.frame_set(frame);bpy.context.view_layer.update();ob=bpy.data.objects[name];ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());a=np.array([v.co[:] for v in ev.data.vertices],dtype=np.float32);return {'vertices':len(a),'hash':hashlib.sha256(a.tobytes()).hexdigest(),'extent':np.ptp(a,axis=0).tolist() if len(a) else []}
def consumers():
 result={}
 for m in mapping:
  bpy.ops.wm.open_mainfile(filepath=m['candidate']);result[m['name']]=snapshot(m['instances'][0]['object'],305 if m['name']=='S02' else 77)
 return result
try:
 baseline=consumers();bpy.ops.wm.open_mainfile(filepath=str(master));ctrl=bpy.data.objects['WF_MASTER_CONTROLS'].modifiers[0];base=snapshot('WF_LIVE_FIELD',30)
 for name,default,changed in [('Playback Speed',1,1.2),('Frequency Multiplier',1,1.3),('Strength',1,.8),('Echo Strength',.5,.3),('Decay Tightness',1,1.4),('Source Duration Frames',30,24),('One Way Frames',12,10),('Reference Height m',.0400390625,.03),('Width m',.0400000084,.03),('Strand Radius m',.000018,.00003)]:
  val(ctrl,name,changed);test=snapshot('WF_LIVE_FIELD',30);checks.append({'control':name,'geometry_changed':test['hash']!=base['hash']});val(ctrl,name,default)
 for name,changed,attr in [('Emission',5,'wf_emission'),('Opacity Power',1,'wf_alpha')]:
  ev=bpy.data.objects['WF_LIVE_FIELD'].evaluated_get(bpy.context.evaluated_depsgraph_get());before=[d.value for d in ev.data.attributes[attr].data];val(ctrl,name,changed);ev=bpy.data.objects['WF_LIVE_FIELD'].evaluated_get(bpy.context.evaluated_depsgraph_get());after=[d.value for d in ev.data.attributes[attr].data];checks.append({'control':name,'attribute_changed':before!=after});val(ctrl,name,3.5 if name=='Emission' else .65)
 val(ctrl,'Strength',.8);bpy.ops.wm.save_as_mainfile(filepath=str(master));changed=consumers();checks.append({'test':'saved shared Strength=.8 reaches both reopened consumers','pass':all(changed[k]['hash']!=baseline[k]['hash'] for k in baseline),'baseline':baseline,'changed':changed})
 master.write_bytes(original);restored=consumers();checks.append({'test':'restored shared source returns both consumers exactly','pass':all(restored[k]['hash']==baseline[k]['hash'] for k in baseline)})
 bpy.ops.wm.open_mainfile(filepath=str(localpath));mod=bpy.data.objects['WF_S02_EVENT_1'].modifiers[0];val(mod,'Strength Override',.7);bpy.ops.wm.save_as_mainfile(filepath=str(localpath));isolated=consumers();checks.append({'test':'saved local override changes S02 only','pass':isolated['S02']['hash']!=baseline['S02']['hash'] and isolated['S04']['hash']==baseline['S04']['hash']})
 localpath.write_bytes(localbytes);bpy.ops.wm.open_mainfile(filepath=str(master));mod=bpy.data.objects['WF_LIVE_FIELD'].modifiers[0];a=snapshot('WF_LIVE_FIELD',30);val(mod,'Preset 0 Open 1 Cased',1);b=snapshot('WF_LIVE_FIELD',30);checks.append({'test':'native cased preset changes field','pass':a['hash']!=b['hash']})
finally:
 master.write_bytes(original);localpath.write_bytes(localbytes)
passed=all(x.get('pass',x.get('geometry_changed',x.get('attribute_changed',False))) for x in checks);(T/'shared-control-tests_v014.json').write_text(json.dumps({'pass':passed,'checks':checks,'master_restored_sha256':hashlib.sha256(master.read_bytes()).hexdigest(),'execution':'Blender --disable-autoexec; saved file edits and reopens; no handlers'},indent=2));print('CONTROL_TESTS_PASS',passed)
