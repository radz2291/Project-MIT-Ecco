"""Reopen v013 and inspect evaluated geometry, causal controls and dependencies."""
import bpy, pathlib, json, hashlib, numpy as np
R=pathlib.Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco')
P=R/'04-Production/Shared/Assets/Acoustics/RibbonWaveform_v013/S02_rolling-wave-field_v013.blend'
digest=hashlib.sha256(P.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(P),load_ui=False)
s=bpy.context.scene; ob=bpy.data.objects['COHERENT_EVOLVING_FIELD_v013']; n=len(ob.data.vertices)
records={}; arrays={}; mats=[]
for f in range(1,97):
 s.frame_set(f); ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get()); me=ev.to_mesh()
 co=np.empty(n*3); me.vertices.foreach_get('co',co); ev.to_mesh_clear(); co=co.reshape(-1,3)
 arrays[f]=co; mats.append(np.array(ob.matrix_world)); cues={}
 for name in ['FIELD_EMISSION','FIELD_WALL_CONTACT','FIELD_SENSOR_RECEIPT','FIELD_MEASUREMENT_AFTER_RECEIPT']:
  cue=bpy.data.objects[name]; em=next(x for x in cue.data.materials[0].node_tree.nodes if x.type=='EMISSION')
  cues[name]=bool(not cue.hide_render and em.inputs[1].default_value>1e-5)
 records[f]={'height_m':float(np.ptp(co[:,2])),'cues':cues}
model=json.loads((R/'04-Production/Records/Tasks/T-056/field-model_v013.json').read_text())
axis=np.array(model['wall_world'])-np.array(model['sensor_world']); axis/=np.linalg.norm(axis)
libs=[{'path':x.filepath,'exists':pathlib.Path(bpy.path.abspath(x.filepath)).exists()} for x in bpy.data.libraries]
cue=lambda f,name:records[f]['cues'][name]
checks={
 'object_transform_stationary':all(np.allclose(m,mats[0],atol=1e-8,rtol=0) for m in mats),
 'axial_sampling_stationary':all(np.allclose(x@axis,arrays[1]@axis,atol=1e-7,rtol=0) for x in arrays.values()),
 'geometry_evolves_at_fixed_locations':all(np.max(np.abs(arrays[f+1][:,2]-arrays[f][:,2]))>.001 for f in [22,26,30,38]),
 'full_height_matches_sensor':abs(max(r['height_m'] for r in records.values())/.0400390625-1)<.02,
 'quiet_geometry_returns_to_start':np.allclose(arrays[1],arrays[96],atol=1e-8,rtol=0),
 'no_early_wall_response':all(not cue(f,'FIELD_WALL_CONTACT') for f in range(1,21)),
 'wall_response_present':cue(26,'FIELD_WALL_CONTACT'),
 'no_early_receipt':all(not cue(f,'FIELD_SENSOR_RECEIPT') for f in range(1,33)),
 'receipt_present':cue(38,'FIELD_SENSOR_RECEIPT'),
 'measurement_after_return_tail':all(not cue(f,'FIELD_MEASUREMENT_AFTER_RECEIPT') for f in range(1,68)) and cue(68,'FIELD_MEASUREMENT_AFTER_RECEIPT'),
 'same_sensor_emits_receives':np.allclose(bpy.data.objects['FIELD_EMISSION'].location,bpy.data.objects['FIELD_SENSOR_RECEIPT'].location),
 'relative_libraries_resolve':all(x['path'].startswith('//') and x['exists'] for x in libs),
 'four_seconds':s.frame_end==96 and s.render.fps==24,
 'native_preserved':hashlib.sha256(P.read_bytes()).hexdigest()==digest,
}
result={'candidate':str(P),'sha256':digest,'checks':checks,'all_pass':all(checks.values()),'frame_samples':records,'libraries':libs,'limit':'Technical checks complement rendered sequence review; not physical calibration or owner acceptance.'}
(R/'04-Production/Records/Tasks/T-051/Evidence/rolling-field-v013-independent.json').write_text(json.dumps(result,indent=2))
print(json.dumps({'checks':checks,'all_pass':result['all_pass']}))
if not result['all_pass']:raise SystemExit(1)
