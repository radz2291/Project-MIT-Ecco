import bpy,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[5];D=Path(__file__).resolve().parent
p=D/'Hardware_demo_v001.blend';bpy.ops.wm.open_mainfile(filepath=str(p));s=bpy.context.scene
c=next(o for o in bpy.data.objects if o.name=='UPHOLE_CONTINUATION_CONTROL' and o.override_library);states=[]
for show in [0,1]:
    c['show']=show;c.update_tag();s.frame_set(1);bpy.context.view_layer.update()
    states.append({'show':show,'length_m':c['length_m'],'objects':[{'name':o.name,'hide_render':o.hide_render,'scale':list(o.scale)} for o in bpy.data.objects if o.override_library and o.name in ['WORLD_UPHOLE_EXTENSION_INSTANCE','WORLD_UPHOLE_JOINT_INSTANCE']]})
g=bpy.data.node_groups['ECCO | Satin finish v001']
libs=[{'path':l.filepath,'exists':Path(bpy.path.abspath(l.filepath)).exists()} for l in bpy.data.libraries]
result={'native':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'libraries':libs,'all_relative':all(l['path'].startswith('//') for l in libs),'all_resolve':all(l['exists'] for l in libs),'control_is_override':bool(c.override_library),'control_states':states,'finish':{'linked':bool(g.library),'revision':g.get('revision'),'roughness_base':g.nodes['Math.001'].inputs[1].default_value},'scene_objects':[o.name for o in s.objects],'no_section_scene':len(bpy.data.scenes)==1,'source_masters_unchanged':'checked separately against prior manifest'}
(D/'verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
