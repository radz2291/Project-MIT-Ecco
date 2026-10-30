"""Independent read-only saved master inspection and in-memory control exercise."""
import bpy, pathlib, hashlib, json, numpy as np
R=pathlib.Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco')
old=R/'04-Production/Shared/Assets/Acoustics/RibbonWaveform_v013/S02_rolling-wave-field_v013.blend'
new=R/'04-Production/Shared/Assets/Acoustics/Waveform_shared_v014/Waveform_shared_v014.blend'
hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [old,new]}
frames=[1,12,18,26,30,38,54,62,68,96]; refs={}; samples=[]
def snapshot(ob):
 ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get()); me=ev.to_mesh()
 co=np.empty(len(me.vertices)*3);me.vertices.foreach_get('co',co)
 ids=np.array([x.value for x in me.attributes['wf_index'].data],dtype=int) if me.attributes.get('wf_index') else None
 ev.to_mesh_clear();return co.reshape(-1,3),ids
bpy.ops.wm.open_mainfile(filepath=str(old),load_ui=False)
for f in frames:
 bpy.context.scene.frame_set(f);refs[f]=snapshot(bpy.data.objects['COHERENT_EVOLVING_FIELD_v013'])[0]
bpy.ops.wm.open_mainfile(filepath=str(new),load_ui=False)
s=bpy.context.scene; ob=bpy.data.objects['WF_LIVE_FIELD']; ctrl=bpy.data.objects['WF_MASTER_CONTROLS']
for f in frames:
 s.frame_set(f);co,ids=snapshot(ob)
 samples.append({'frame':f,'vertices':len(co),'max_default_error_m':float(np.max(np.abs(co-refs[f][ids]))) if len(co) else 0})
def set_control(mod,name,val):
 item=next(x for x in mod.node_group.interface.items_tree if getattr(x,'in_out','')=='INPUT' and x.name==name)
 getattr(mod.properties.inputs,item.identifier).value=val
 mod.id_data.update_tag(refresh={'OBJECT','DATA','TIME'});ctrl.update_tag();ob.update_tag();bpy.context.view_layer.update()
s.frame_set(30); baseline,ids=snapshot(ob); cm=next(m for m in ctrl.modifiers if m.type=='NODES'); lm=next(m for m in ob.modifiers if m.type=='NODES')
set_control(cm,'Strength',.5);half,_=snapshot(ob)
set_control(cm,'Strength',1.);restored,_=snapshot(ob)
set_control(lm,'Preset 0 Open 1 Cased',1);cased,_=snapshot(ob)
set_control(lm,'Preset 0 Open 1 Cased',0)
checks={
 'native_live_matches_selected_v013':all(x['max_default_error_m']<2e-6 for x in samples),
 'quiet_start_and_end_empty':all(x['vertices']==0 for x in samples if x['frame'] in [1,68,96]),
 'shared_strength_changes_geometry':half.shape==baseline.shape and np.max(np.abs(half-baseline))>.001,
 'shared_strength_restores_geometry':restored.shape==baseline.shape and np.allclose(restored,baseline,atol=1e-7,rtol=0),
 'cased_preset_changes_geometry':cased.shape!=baseline.shape or np.max(np.abs(cased-baseline))>.0001,
 'relative_libraries_resolve':all(x.filepath.startswith('//') and pathlib.Path(bpy.path.abspath(x.filepath)).is_file() for x in bpy.data.libraries),
 'source_files_unchanged':all(hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()==h for p,h in hashes.items()),
}
checks={key:bool(value) for key,value in checks.items()}
result={'checks':checks,'pass':all(checks.values()),'samples':samples,'hashes':hashes,'scope':'No native saves. Blender launched with autoexec disabled. These checks do not replace owner native review.'}
(R/'04-Production/Records/Tasks/T-051/Evidence/live-waveform-v014-independent.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result))
if not result['pass']:raise SystemExit(1)
