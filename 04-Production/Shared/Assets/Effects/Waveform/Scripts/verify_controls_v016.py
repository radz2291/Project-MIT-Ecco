import bpy,json,hashlib,numpy as np
from pathlib import Path
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');B=R/'04-Production/Shared/Assets/Effects/Waveform';Q=R/'04-Production/Shots/S01-S02';p=B/'Waveform_shared_v016.blend';before=hashlib.sha256(p.read_bytes()).hexdigest();bpy.ops.wm.open_mainfile(filepath=str(p));live=bpy.data.objects['WF_LIVE_FIELD'];ctrl=bpy.data.objects['WF_MASTER_CONTROLS'];mod=live.modifiers[0];cm=ctrl.modifiers[0]
def param(m,name):return getattr(m.properties.inputs,next(x.identifier for x in m.node_group.interface.items_tree if getattr(x,'in_out','')=='INPUT' and x.name==name))
def update():ctrl.update_tag(refresh={'OBJECT','DATA','TIME'});live.update_tag(refresh={'OBJECT','DATA','TIME'});bpy.context.view_layer.update()
def coords(f):
 bpy.context.scene.frame_set(f);update();ev=live.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();a=np.array([v.co[:] for v in me.vertices]);ev.to_mesh_clear();return a
organic=coords(30);v=param(cm,'Short Crests').value;param(cm,'Short Crests').value=3.;assert np.array_equal(organic,coords(30));param(cm,'Short Crests').value=v
for name,value in {'Motion Preset 0 Organic 1 Short':1,'Start Frame':300.,'Contact Frame':309.,'Receipt Frame':318.,'Echo Delay Frames':1.,'Travel Override':9.,'Return Travel Override':8.,'Lock Event Timing':1.,'Route Axis':(1,0,0),'Transverse Axis':(0,1,0),'Up Axis':(0,0,1)}.items():param(mod,name).value=value
base=coords(311);changes=[]
for name,value in [('Short Crests',3.),('Short Packet Fraction',.7),('Short Contact Blend Frames',0.),('Short Return Fade Frames',2.),('Short Stroke Factor',1.),('Short Taper Power',1.),('Short Height Fraction',.5)]:
 old=param(cm,name).value;param(cm,name).value=value;test=coords(316 if name=='Short Return Fade Frames' else 311);param(cm,name).value=old;restore=coords(316 if name=='Short Return Fade Frames' else 311);assert test.shape!=restore.shape or not np.array_equal(test,restore);assert np.array_equal(base,coords(311));changes.append(name)
old=param(cm,'Playback Speed').value;param(cm,'Playback Speed').value=2.;assert np.array_equal(base,coords(311));assert len(coords(318))==0;param(cm,'Playback Speed').value=old
# Recorded S04 basis is a rotation of the canonical fixture, with no route drift.
canonical=coords(311);basis=np.array([[0.,.7771459818,.6293203235],[0.,.6293203235,-.7771459818],[1.,0.,0.]])
for name,value in zip(['Route Axis','Transverse Axis','Up Axis'],basis):param(mod,name).value=tuple(value)
actual=coords(311);error=float(np.max(np.abs(actual-canonical@basis)));assert error<1e-7
assert hashlib.sha256(p.read_bytes()).hexdigest()==before
report={'pass':True,'organic_unaffected_by_short_style':True,'seven_shared_controls_change_and_restore_geometry':changes,'locked_playback_does_not_move_or_change_event':True,'s04_rotated_basis_max_error_m':error,'master_file_unchanged':True,'no_native_save':True}
(Q/'Notes/waveform_v016_control_verification.json').write_text(json.dumps(report,indent=2));print('SHARED_CONTROLS_PASS',report)
