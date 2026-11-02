"""Camera-only successor: restore original widening during scans four to six."""
import bpy,json,math,hashlib
from pathlib import Path
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');Q=R/'04-Production/Shots/S01-S02'
source=R/'05-Previs/Section-02_Measurement-History/v011/Continuation/Scenes/S01-S02_continuous_v011.blend'
out=Q/'Scenes/S01-S02_production_v017.blend';assert not out.exists()
bpy.ops.wm.open_mainfile(filepath=str(source),use_scripts=False)
s=bpy.context.scene;original=[]
for f in range(408,529):
 s.frame_set(f);original.append((s.camera.matrix_world.copy(),s.camera.data.lens))
bpy.ops.wm.open_mainfile(filepath=str(Q/'Scenes/S01-S02_production_v016.blend'),use_scripts=False)
s=bpy.context.scene;cam=s.camera;first,last=474,720
def snapshot():
 rows=[]
 for f in [1,94,95,120,180,299,300,360,420,474]:
  s.frame_set(f);rows.append((f,[list(r) for r in cam.matrix_world],cam.data.lens))
 return rows
before=snapshot();s.frame_set(first);anchor=cam.matrix_world.copy();lens_offset=cam.data.lens-original[0][1];alignment=anchor@original[0][0].inverted()
def action_signature(obj):
 if not obj.animation_data or not obj.animation_data.action:return None
 return [(fc.data_path,fc.array_index,[(tuple(k.co),k.interpolation) for k in fc.keyframe_points]) for l in obj.animation_data.action.layers for st in l.strips for bag in st.channelbags for fc in bag.fcurves]
bha=bpy.data.objects['BHA sequence assembly'];bha_before=action_signature(bha)
field_groups={o.name:o.modifiers[0].node_group.name for o in bpy.data.objects if o.name.startswith('WF sequence event ')}
for obj in [cam,cam.data]:
 obj.animation_data.action=obj.animation_data.action.copy()
 for l in obj.animation_data.action.layers:
  for st in l.strips:
   for bag in st.channelbags:
    for fc in bag.fcurves:
     for i in range(len(fc.keyframe_points)-1,-1,-1):
      if fc.keyframe_points[i].co.x>first:fc.keyframe_points.remove(fc.keyframe_points[i],fast=True)
for f in range(first+1,s.frame_end+1):
 t=min(120.,(f-first)*120/(last-first));i=min(119,int(t));a=t-i;m0,l0=original[i];m1,l1=original[i+1]
 loc=m0.translation.lerp(m1.translation,a);rot=m0.to_quaternion().slerp(m1.to_quaternion(),a)
 m=rot.to_matrix().to_4x4();m.translation=loc;cam.matrix_world=alignment@m
 for p in ['location','rotation_quaternion','scale']:cam.keyframe_insert(p,frame=f)
 cam.data.lens=l0+(l1-l0)*a+lens_offset*(1-t/120);cam.data.keyframe_insert('lens',frame=f)
for obj in [cam,cam.data]:
 for l in obj.animation_data.action.layers:
  for st in l.strips:
   for bag in st.channelbags:
    for fc in bag.fcurves:
     for k in fc.keyframe_points:
      if k.co.x>=first:k.interpolation='LINEAR'
after=snapshot();errors=[]
for (_,bm,bl),(_,am,al) in zip(before,after):
 errors.extend(abs(x-y) for br,ar in zip(bm,am) for x,y in zip(br,ar));errors.append(abs(bl-al))
assert max(errors)<1e-5,max(errors)
assert bha_before==action_signature(bha)
assert field_groups=={o.name:o.modifiers[0].node_group.name for o in bpy.data.objects if o.name.startswith('WF sequence event ')}
# The moving inspection cutaway must never delete an authored scan target.
wall=bpy.data.objects['ONE WALL - old history and current cells share topology']
g=wall.modifiers['Shot camera viewing wedge — inspection cutaway'].node_group
delete=next(n for n in g.nodes if n.type=='DELETE_GEOMETRY');selection=delete.inputs['Selection'].links[0].from_socket
attr=g.nodes.new('GeometryNodeInputNamedAttribute');attr.data_type='FLOAT';attr.inputs['Name'].default_value='ecco_receipt_frame'
def op(kind,a,b):
 n=g.nodes.new('ShaderNodeMath');n.operation=kind
 for socket,value in zip(n.inputs,[a,b]):
  if isinstance(value,(int,float)):socket.default_value=value
  else:g.links.new(value,socket)
 return n.outputs[0]
target=op('MULTIPLY',op('GREATER_THAN',attr.outputs['Attribute'],299),op('LESS_THAN',attr.outputs['Attribute'],1000))
g.links.new(op('MULTIPLY',selection,op('SUBTRACT',1,target)),delete.inputs['Selection'])
s.frame_set(600);bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True)
bpy.ops.wm.open_mainfile(filepath=str(out),use_scripts=False)
s=bpy.context.scene
assert all(Path(bpy.path.abspath(l.filepath)).exists() for l in bpy.data.libraries)
samples=[]
for f in [474,480,528,540,600,654,660,720,756]:
 s.frame_set(f);samples.append({'frame':f,'camera':list(s.camera.matrix_world.translation),'lens':s.camera.data.lens})
(Q/'Notes/camera_v017_restore.json').write_text(json.dumps({'scene':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'source':str(source),'source_pull':[408,528],'retimed_pull':[first,last],'final_hold':[last,756],'sequence_frames':756,'fps':24,'scan_starts':[300,360,420,480,540,600],'third_scan_return_complete':469,'third_beam_closed':472,'third_hold_ends':474,'reason':'Restore close-up to wide discovery during scans four to six, rather than after all six. Actual previs arc/lens aligned rigidly to current third-scan camera, retimed to approved longer exchanges.','camera_before_and_at_start_max_error':max(errors),'hardware_action_unchanged':True,'shared_waveform_groups_unchanged':True,'relative_links_resolve_on_reopen':True,'samples':samples,'scope':'Camera/lens correction plus shot viewing-mask target protection; shared masters, scan events, hardware and signal/reveal animation unchanged.','target_protection':'Shot camera viewing wedge excludes all six current scan target patches using receipt-frame attributes.'},indent=2))
print('PREVIS_CAMERA_RESTORED_V017')
