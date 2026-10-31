import bpy,pathlib,json,hashlib,numpy as np
R=pathlib.Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');T=R/'04-Production/Records/Tasks/T-051'
paths=['04-Production/Shared/Assets/Acoustics/Waveform_shared_v015/Waveform_shared_v015.blend','04-Production/Records/Tasks/T-056/Demos/Waveform_demo_v015.blend','04-Production/Records/Tasks/T-052/Demos/Hardware_demo_v001.blend','04-Production/Records/Tasks/T-054/Demos/Digital_environment_demo_v005.blend','04-Production/Records/Tasks/T-054/Demos/Measurement_reveal_demo_v002.blend','04-Production/Records/Tasks/T-051/Demos/World_demo_v001.blend','04-Production/Records/Tasks/T-051/Demos/Surface_demo_v001.blend']
rows=[]
for rel in paths:
 p=R/rel;h=hashlib.sha256(p.read_bytes()).hexdigest();bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False)
 libs=[{'path':l.filepath,'exists':pathlib.Path(bpy.path.abspath(l.filepath)).exists()} for l in bpy.data.libraries]
 checks={'libraries_relative_resolve':all(x['path'].startswith('//') and x['exists'] for x in libs),'no_shot_libraries':all(not any(k in x['path'] for k in ['Previs','Consumers','Shots']) for x in libs),'file_unchanged':hashlib.sha256(p.read_bytes()).hexdigest()==h}
 if 'Waveform_shared_v015.blend' in rel:checks.update({'only_two_objects':len(bpy.data.objects)==2,'no_external_libraries':not libs,'no_camera_lights':all(o.type not in ['CAMERA','LIGHT'] for o in bpy.data.objects),'near_origin':all(o.location.length<.1 for o in bpy.context.scene.objects)})
 rows.append({'path':rel,'sha256':h,'objects':len(bpy.data.objects),'local_objects':sum(o.library is None for o in bpy.data.objects),'texts':[x.name for x in bpy.data.texts],'scenes':[{'name':s.name,'camera':s.camera.name if s.camera else None} for s in bpy.data.scenes],'libraries':libs,'checks':checks,'pass':all(checks.values())})
# Compare v014 and v015 local live geometry at the approved frame samples.
samples={};frames=[1,12,18,26,30,38,54,62,68,96]
for version in ['014','015']:
 p=R/f'04-Production/Shared/Assets/Acoustics/Waveform_shared_v{version}/Waveform_shared_v{version}.blend';bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False);a={}
 for f in frames:
  bpy.context.scene.frame_set(f);o=bpy.data.objects['WF_LIVE_FIELD'].evaluated_get(bpy.context.evaluated_depsgraph_get());me=o.to_mesh();co=np.empty(len(me.vertices)*3);me.vertices.foreach_get('co',co);o.to_mesh_clear();a[f]=co
 samples[version]=a
errors={f:float(np.max(np.abs(samples['014'][f]-samples['015'][f]))) if len(samples['014'][f]) else 0 for f in frames};passed=all(x['pass'] for x in rows) and max(errors.values())<1e-7
(T/'Evidence/shared-demo-independent.json').write_text(json.dumps({'files':rows,'waveform_default_errors_m':errors,'pass':passed},indent=2));print(json.dumps({'files':[{k:x[k] for k in ['path','objects','checks','pass']} for x in rows],'errors':errors,'pass':passed}))
if not passed:raise SystemExit(1)
