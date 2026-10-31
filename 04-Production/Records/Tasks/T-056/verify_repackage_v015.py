import bpy,pathlib,json,hashlib,numpy as np
R=pathlib.Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');T=R/'04-Production/Records/Tasks/T-056';shared=R/'04-Production/Shared/Assets/Acoustics/Waveform_shared_v015/Waveform_shared_v015.blend';demo=T/'Demos/Waveform_demo_v015.blend';original=shared.read_bytes()
def snap(path):
 bpy.ops.wm.open_mainfile(filepath=str(path));bpy.context.scene.frame_set(30);ev=bpy.data.objects['WF_LIVE_FIELD'].evaluated_get(bpy.context.evaluated_depsgraph_get());a=np.array([v.co[:] for v in ev.data.vertices],dtype=np.float32);return hashlib.sha256(a.tobytes()).hexdigest()
base=snap(demo);links=[{'path':x.filepath,'exists':pathlib.Path(bpy.path.abspath(x.filepath)).exists()} for x in bpy.data.libraries];names=[o.name for o in bpy.data.objects];counts={'objects':len(names),'cameras':len(bpy.data.cameras),'lights':len(bpy.data.lights),'libraries':links};cue_targets=[]
for g in bpy.data.node_groups:
 if g.name.startswith('WF_NATIVE_CUE_'):
  cue_targets += [n.inputs['Object'].default_value.library.filepath for n in g.nodes if n.bl_idname=='GeometryNodeObjectInfo']
try:
 bpy.ops.wm.open_mainfile(filepath=str(shared));m=bpy.data.objects['WF_MASTER_CONTROLS'].modifiers[0];ident=next(x.identifier for x in m.node_group.interface.items_tree if getattr(x,'in_out','')=='INPUT' and x.name=='Strength');getattr(m.properties.inputs,ident).value=.8;m.id_data.update_tag(refresh={'OBJECT','DATA','TIME'});bpy.ops.wm.save_as_mainfile(filepath=str(shared));changed=snap(demo)
finally:shared.write_bytes(original)
restored=snap(demo);result={'demo_counts':counts,'demo_objects':names,'cue_linked_control_libraries':cue_targets,'shared_edit_changes_demo':base!=changed,'restored_exactly':base==restored,'only_v015_library':len(links)==1 and 'v015' in links[0]['path'],'links_exist':all(x['exists'] for x in links),'shared_sha256':hashlib.sha256(shared.read_bytes()).hexdigest(),'demo_sha256':hashlib.sha256(demo.read_bytes()).hexdigest(),'autoexec':'disabled; native GN, no handlers'};result['pass']=all(result[k] for k in ['shared_edit_changes_demo','restored_exactly','only_v015_library','links_exist']);(T/'repackage-verification_v015.json').write_text(json.dumps(result,indent=2));print('VERIFY',json.dumps(result))
