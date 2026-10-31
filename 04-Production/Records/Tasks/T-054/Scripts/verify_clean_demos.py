import bpy,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[5];T=R/'04-Production/Records/Tasks/T-054';out=[]
def counts():
 bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();return {o.name:len(o.evaluated_get(dg).data.polygons) for o in bpy.context.scene.objects if o.type=='MESH'}
for filename in ['Digital_environment_demo_v005.blend','Measurement_reveal_demo_v002.blend']:
 bpy.ops.wm.open_mainfile(filepath=str(T/'Demos'/filename),load_ui=False);s=bpy.context.scene;ctl=next(o for o in s.objects if o.type=='EMPTY');libs=[{'path':l.filepath,'exists':Path(bpy.path.abspath(l.filepath)).is_file()} for l in bpy.data.libraries];assert all(l['exists'] for l in libs);assert len(s.objects)==5
 record={'demo':filename,'scene_objects':[o.name for o in s.objects],'local_objects':[o.name for o in bpy.data.objects if not o.library],'libraries':libs,'default_counts':counts(),'raw_local_mesh_vertices':{o.name:len(o.data.vertices) for o in s.objects if o.type=='MESH'},'control_names':list(ctl.keys()),'readme':bool(bpy.data.texts.get('README — SHARED ASSET DEMO'))}
 if filename.startswith('Digital'):
  before=counts();ctl['Show soil']=False;ctl.update_tag();s.frame_set(1);off=counts();assert off['DEMO linked soil']==0
  ctl['Show soil']=True;ctl['Axial half window m']=2.;ctl.update_tag();s.frame_set(1);small=counts();assert small['DEMO linked soil']<before['DEMO linked soil'];record['control_effects']={'normal':before,'soil_off':off,'window2m':small}
 else:
  samples={}
  for f in [1,20,34,60]:s.frame_set(f);samples[f]=counts()
  assert all(v==0 for v in samples[1].values());assert all(samples[60][k]>samples[20][k]>0 for k in samples[60]);s.frame_set(34);ctl['Start frame']=70.;ctl.update_tag();s.frame_set(35);late=counts();assert all(v==0 for v in late.values());record['frame_counts']=samples;record['late_start_at35']=late
 out.append(record)
(T/'Evidence/demo-validation.json').write_text(json.dumps(out,indent=2));print('DEMO_NATIVE_CHECKS_PASS')
