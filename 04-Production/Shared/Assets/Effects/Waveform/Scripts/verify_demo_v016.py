"""Read-only geometry/cue checks plus cheap fixture renders. Candidate demo only."""
import bpy,json,math,time,hashlib,numpy as np
from pathlib import Path
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');B=R/'04-Production/Shared/Assets/Effects/Waveform';Q=R/'04-Production/Shots/S01-S02';P=R/'04-Production/Shared/Demos/Previews/Waveform_v016';P.mkdir(parents=True,exist_ok=True)
demo=R/'04-Production/Shared/Demos/Waveform_demo_v016.blend';master=B/'Waveform_shared_v016.blend';master_hash=hashlib.sha256(master.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(demo));bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(demo),compress=True)
def parameter(mod,name):
 x=next(x for x in mod.node_group.interface.items_tree if getattr(x,'in_out','')=='INPUT' and x.name==name);return getattr(mod.properties.inputs,x.identifier)
def sample(ob,f):
 bpy.context.scene.frame_set(math.floor(f),subframe=f-math.floor(f));bpy.context.view_layer.update();ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();a=np.empty(len(me.vertices)*3);me.vertices.foreach_get('co',a);co=a.reshape(-1,3);out={'vertices':len(co),'height':float(np.ptp(co[:,2])) if len(co) else 0.,'width':float(np.ptp(co[:,1])) if len(co) else 0.,'hash':hashlib.sha256(a.tobytes()).hexdigest()}
 for attr,key in [('wf_out_envelope','out'),('wf_return_envelope','ret')]:
  data=me.attributes.get(attr);out[key]=max((x.value for x in data.data),default=0.) if data else 0.
 if len(co) and len(co)%4==0:
  rings=co.reshape(-1,4,3);r=np.linalg.norm(rings-rings.mean(axis=1)[:,None,:],axis=2);out['radius_min']=float(r.min());out['radius_max']=float(r.max())
 ev.to_mesh_clear();return out
report={'cases':[],'benchmarks':[],'batch':[],'master_unchanged':None}
for scene in bpy.data.scenes:
 bpy.context.window.scene=scene;case=json.loads(scene['waveform_case']);ob=next(o for o in scene.objects if o.name.endswith(' field'));mod=ob.modifiers[0];row={'case':case,'samples':{}}
 if case['preset']==1:
  for label,f in [('before',case['start']-1),('onset',case['start']+1),('precontact',case['contact']-.05),('blend',case['contact']+2),('return',case['receipt']-2),('receipt',math.ceil(case['receipt'])),('after',math.ceil(case['receipt'])+2)]:row['samples'][label]=sample(ob,f)
  assert row['samples']['before']['vertices']==0 and row['samples']['receipt']['vertices']==0 and row['samples']['after']['vertices']==0
  assert row['samples']['onset']['vertices']>0 and row['samples']['precontact']['ret']==0
  assert row['samples']['blend']['out']>0 and row['samples']['blend']['ret']>0
  assert max(x['height'] for x in row['samples'].values())<.0401 and max(x['width'] for x in row['samples'].values())<.0401
  assert row['samples']['blend']['radius_min']<row['samples']['blend']['radius_max']*.5
  parameter(mod,'Enabled').value=0;ob.update_tag();assert sample(ob,case['contact']+2)['vertices']==0;parameter(mod,'Enabled').value=1;ob.update_tag()
  # Source fixture timing remains unchanged when the open/cased display changes.
  old=parameter(mod,'Preset 0 Open 1 Cased').value;baseline=sample(ob,case['contact']+3);parameter(mod,'Preset 0 Open 1 Cased').value=1-old;ob.update_tag();alternate=sample(ob,case['contact']+3);assert baseline['hash']!=alternate['hash'];parameter(mod,'Preset 0 Open 1 Cased').value=old;ob.update_tag();assert sample(ob,case['contact']+3)['hash']==baseline['hash'];row['context_switch_restores']=True
  cue=next(o for o in scene.objects if o.name.endswith('measurement AFTER receipt'));scene.frame_set(math.floor(case['receipt']));assert cue.scale.length==0;scene.frame_set(math.ceil(case['measure']));assert cue.scale.length>0
 else:
  row['samples']={str(f):sample(ob,f) for f in [1,12,30,54,62,96]};assert row['samples']['1']['vertices']==0 and row['samples']['96']['vertices']==0
 report['cases'].append(row)
 scene.frame_set(30 if case['preset']==0 else round(case['contact']+2));scene.render.filepath=str(P/(scene.name[:2]+'_benchmark.png'));t=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t;report['benchmarks'].append({'scene':scene.name,'seconds':dt,'size':[1280,720]});(Q/'Notes/waveform_v016_fixture_verification.json').write_text(json.dumps(report,indent=2));assert dt<5
for name,prefix in [('01 Organic reference','organic'),('03 Short S04 open','open'),('04 Short S04 cased','cased')]:
 scene=bpy.data.scenes[name];bpy.context.window.scene=scene;scene.render.resolution_x=640;scene.render.resolution_y=360
 for f in range(scene.frame_start,scene.frame_end+1):
  t=time.perf_counter();scene.frame_set(f);scene.render.filepath=str(P/f'{prefix}_{f:04}.png');bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t;report['batch'].append({'scene':name,'frame':f,'seconds':dt});(Q/'Notes/waveform_v016_fixture_verification.json').write_text(json.dumps(report,indent=2));assert dt<5
assert hashlib.sha256(master.read_bytes()).hexdigest()==master_hash
report['master_unchanged']=True;report['libraries']=[{'path':l.filepath,'exists':Path(bpy.path.abspath(l.filepath)).exists()} for l in bpy.data.libraries];report['pass']=True
(Q/'Notes/waveform_v016_fixture_verification.json').write_text(json.dumps(report,indent=2));print('WAVEFORM_FIXTURES_PASS')
