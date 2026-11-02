"""Freeze approved quickv022 controls as a clean master and portable recipe."""
import bpy,json,sys,hashlib
from pathlib import Path
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');B=R/'04-Production/Shared/Assets/Effects/Waveform';Q=R/'04-Production/Shots/S01-S02';sys.path.insert(0,str(B/'Scripts'))
from pulse_asset_api import get_input,set_input
target=B/'Waveform_shared_v021.blend';assert not target.exists()
bpy.ops.wm.open_mainfile(filepath=str(Q/'Scenes/Waveform_active_patch_fast_v022.blend'),use_scripts=False)
mod=bpy.data.objects['WF sequence event 1'].modifiers[0];allvals={}
for x in mod.node_group.interface.items_tree:
 if getattr(x,'in_out','')=='INPUT' and x.socket_type not in ['NodeSocketGeometry','NodeSocketObject','NodeSocketMaterial']:
  v=get_input(mod,x.name);allvals[x.name]=list(v) if x.socket_type in ['NodeSocketVector','NodeSocketColor'] else v
color_profiles={}
for group in range(4):
 m=bpy.data.materials['Unified cell 1 edge0 reveal'+str(group)];profiles=[]
 curves=[fc for l in m.animation_data.action.layers for st in l.strips for bag in st.channelbags for fc in bag.fcurves if fc.data_path=='diffuse_color'];times=sorted({0.,54.}|{k.co.x-300 for fc in curves for k in fc.keyframe_points if 300<k.co.x<354})
 for t in times:profiles.append({'frame':t,'color':[next(fc for fc in curves if fc.array_index==ch).evaluate(300+t) for ch in range(4)]})
 color_profiles[str(group)]=profiles
timing_names=list(json.loads((B/'Waveform_interface_v020.json').read_text())['timing']);style_names=list(json.loads((B/'Waveform_interface_v020.json').read_text())['style'])
recipe={'name':'Approved connected bipolar exchange','approval':'Radzi approved quickv022 signal/center-out glitch/active held patch,2November2026','source_review':'Waveform_active_patch_fast_v022.blend','shared_master':'Waveform_shared_v021.blend','reference_fps':24,'style':{k:allvals[k] for k in style_names},'timing':{k:(1. if k=='Start frame' else allvals[k]) for k in timing_names},'quick':{k:allvals[k] for k in ['Strength multiplier','Width multiplier','Radius multiplier','Show markers']},'landmarks_relative':{'beam_contact':5,'pulse_launch':6,'surface_reveal':22,'feedback_start':28,'feedback_complete':49,'beam_closed':52,'review_end':54},'surface':{'rows':4,'columns':4,'order':'four central faces first, then distance-ranked groups outward toward rectangle edges/corners','group_offsets':[0,1.5,3,4.5],'settle_frames':4,'color_profiles':color_profiles},'contact_patch':{'size_m':.003,'surface_clearance_m':.00012,'color':[.17,.43,.46,1.],'min_scale':.78,'breath_period_frames':4,'arrival_after':5,'reveal_after':22,'handover_frames':1,'enabled':True},'shot_owned':['start frames','actual hardware and wall intersections','target patch face assignment and dimensions','camera/lighting','tool hold/turn choreography'],'native_media':'local only, no off-machine backup claimed'}
(B/'Approved_beam_exchange_v001.json').write_text(json.dumps(recipe,indent=2))
bpy.ops.wm.open_mainfile(filepath=str(B/'Waveform_shared_v020.blend'),use_scripts=False);field=bpy.data.objects['WF_PULSE_FIELD'];master=bpy.data.objects['WF_MASTER_CONTROLS'];fm=field.modifiers[0];cm=master.modifiers[0]
for k,v in recipe['style'].items():set_input(cm,k,v);set_input(fm,k,v)
for k,v in recipe['timing'].items():set_input(fm,k,v)
for k,v in recipe['quick'].items():set_input(fm,k,v)
set_input(fm,'Use master style',True);set_input(fm,'Pulse count override',0);set_input(fm,'Strand count override',0);set_input(fm,'Strand separation override',-1.)
for g in bpy.data.node_groups:g.name=g.name.replace('v020','v021')
field['Approved preset']='Approved_beam_exchange_v001.json';master['Approved preset']='Owner approved quickv022; master common defaults now match accepted style.'
bpy.context.scene.frame_start=1;bpy.context.scene.frame_end=54;bpy.context.scene.frame_set(16)
for screen in bpy.data.screens:
 for a in screen.areas:
  if a.type=='VIEW_3D':a.spaces.active.region_3d.view_location=(.012,0,0);a.spaces.active.region_3d.view_distance=.08
bpy.ops.wm.save_as_mainfile(filepath=str(target),compress=True)
(B/'Waveform_interface_v021.json').write_text(json.dumps({'native':str(target),'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'approved_preset':'Approved_beam_exchange_v001.json','style':recipe['style'],'timing':recipe['timing'],'objects':[field.name,master.name],'counts':{'objects':len(bpy.data.objects),'groups':len(bpy.data.node_groups),'libraries':len(bpy.data.libraries),'cameras':len(bpy.data.cameras)},'consumers':['approved exchange demo; production migration separately recorded']},indent=2));print('APPROVED_MASTER_READY')
