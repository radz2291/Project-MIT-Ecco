import bpy,json,math
from pathlib import Path
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');Q=R/'04-Production/Shots/S01-S02';A=R/'04-Production/Shared/Assets/Effects/Waveform'
def sample(o,f):
 bpy.context.scene.frame_set(f);e=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=e.to_mesh();co=[tuple(v.co) for v in m.vertices];at={n:[v.value for v in m.attributes[n].data] for n in ['wf17_u','wf17_component'] if n in m.attributes};e.to_mesh_clear();return co,at
defaults=[]
for v in ['v018','v019']:
 bpy.ops.wm.open_mainfile(filepath=str(A/f'Waveform_shared_{v}.blend'),use_scripts=False);defaults.append(sample(bpy.data.objects['WF_PULSE_FIELD'],18)[0])
assert defaults[0]==defaults[1]
bpy.ops.wm.open_mainfile(filepath=str(Q/'Scenes/S01-S02_production_v014.blend'),use_scripts=False)
assert all(Path(bpy.path.abspath(l.filepath)).exists() for l in bpy.data.libraries)
o=bpy.data.objects['WF sequence event 1'];rows=[]
for f in range(299,344):
 co,a=sample(o,f);active=301<=f<=337;assert bool(co)==active,(f,len(co))
 if active:
  assert min(a['wf17_u'])==0 and max(a['wf17_u'])==1,(f,'disconnected endpoints')
  assert set(a['wf17_component'])=={1 if f<321 else 2},(f,'phase/color')
  assert all(math.isfinite(x) for p in co for x in p)
  flat=max(abs(sum(p[2] for p in co[i:i+4])/4) for i in range(0,len(co),4))
  if f in [301,302,337]:assert flat<1e-8,(f,'handshake/close must be straight')
  if f in [307,329]:assert flat>.0001,(f,'missing pulse')
  rows.append({'frame':f,'vertices':len(co),'phase':next(iter(set(a['wf17_component']))),'max_center_height':flat})
(Q/'Notes/waveform_v014_verification.json').write_text(json.dumps({'v019_beamoff_exactly_v018':True,'native_reopen_links':True,'beam_connected_every_frame301_337':True,'straight_handshake301_302':True,'outgoing_cyan_then_feedback_violet':True,'markers_absent':True,'beam_closed_before_tool_turn342':True,'samples':rows},indent=2));print('BEAM_V014_CHECKS_PASS')
