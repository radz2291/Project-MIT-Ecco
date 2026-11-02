"""Apply owner-approved shared exchange to all six actual production targets."""
import bpy,json,sys,re,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');Q=R/'04-Production/Shots/S01-S02';B=R/'04-Production/Shared/Assets/Effects/Waveform';sys.path.insert(0,str(B/'Scripts'))
from pulse_asset_api import get_input,set_input
from approved_exchange_api import apply_approved_preset,create_contact_patch,configure_surface_patch
out=Q/'Scenes/S01-S02_production_v016.blend';assert not out.exists();bpy.ops.wm.open_mainfile(filepath=str(Q/'Scenes/S01-S02_production_v015.blend'),use_scripts=False);s=bpy.context.scene;bha=bpy.data.objects['BHA sequence assembly'];cam=s.camera;poses=[];camposes=[]
for f in [300+144*i for i in range(6)]:s.frame_set(f);poses.append(bha.matrix_world.copy());camposes.append((cam.matrix_world.copy(),cam.data.lens))
pull=[]
for i in range(97):s.frame_set(1152+i);pull.append((660+i,cam.matrix_world.copy(),cam.data.lens))
def trim(obj):
 if obj.animation_data and obj.animation_data.action:
  obj.animation_data.action=obj.animation_data.action.copy()
  for l in obj.animation_data.action.layers:
   for st in l.strips:
    for bag in st.channelbags:
     for fc in bag.fcurves:
      for idx in range(len(fc.keyframe_points)-1,-1,-1):
       if fc.keyframe_points[idx].co.x>=300:fc.keyframe_points.remove(fc.keyframe_points[idx],fast=True)
def key(obj,f,m):
 obj.matrix_world=m
 for p in ['location','rotation_quaternion','scale']:obj.keyframe_insert(p,frame=f)
for obj in [bha,cam,cam.data]:trim(obj)
for i,(pose,(c,lens)) in enumerate(zip(poses,camposes)):
 start=300+60*i
 for f in [start,start+54]:key(bha,f,pose);key(cam,f,c);cam.data.lens=lens;cam.data.keyframe_insert('lens',frame=f)
key(bha,756,poses[-1])
for f,m,lens in pull:key(cam,f,m);cam.data.lens=lens;cam.data.keyframe_insert('lens',frame=f)
for obj in [bha,cam,cam.data]:
 for l in obj.animation_data.action.layers:
  for st in l.strips:
   for bag in st.channelbags:
    for fc in bag.fcurves:
     for k in fc.keyframe_points:
      if k.co.x>=300:k.interpolation='LINEAR'
s.frame_end=756
with bpy.data.libraries.load(str(B/'Waveform_shared_v021.blend'),link=True) as (a,b):b.objects=['WF_MASTER_CONTROLS','WF_PULSE_FIELD']
ctrl,template=b.objects;s.collection.objects.link(ctrl);wall=bpy.data.objects['ONE WALL - old history and current cells share topology'];records=[]
for node in wall.modifiers[0].node_group.nodes:
 if node.type=='GROUP' and 'Settle frames' in node.inputs:node.inputs['Settle frames'].default_value=4
for i in range(1,7):
 start=300+60*(i-1);s.frame_set(start);ob=bpy.data.objects[f'WF sequence event {i}'];A=ob.matrix_world.translation.copy();faces=[p for p in wall.data.polygons if re.match(r'Unified cell '+str(i)+r'(\s|$)',wall.data.materials[p.material_index].name)];assert len(faces)==16
 verts=[wall.matrix_world@wall.data.vertices[n].co for n in sorted({n for p in faces for n in p.vertices})];avg=sum(verts,Vector())/len(verts);center=min(verts,key=lambda v:(v-avg).length);bvh=BVHTree.FromPolygons([wall.matrix_world@v.co-A for v in wall.data.vertices],[tuple(p.vertices) for p in faces]);hit=bvh.ray_cast(Vector(),(center-A).normalized(),.15);assert hit[0] is not None;target=A+hit[0]
 axis=(target-A).normalized();side=axis.cross(Vector((0,0,1))).normalized();up=side.cross(axis).normalized();ob.data=template.data;ob.modifiers.clear();mod=ob.modifiers.new('Approved shared exchange — shot placement/timing','NODES');mod.node_group=template.modifiers[0].node_group;marks=apply_approved_preset(mod,start)
 for n,v in {'Gap length m':(target-A).length,'Route axis':tuple(axis),'Transverse axis':tuple(side),'Up axis':tuple(up)}.items():set_input(mod,n,v)
 configure_surface_patch(wall,faces,target,start);patch=create_contact_patch(s.collection,target,Vector((target.x,target.y,0)),start_frame=start);patch.name=f'Contact patch event {i}'
 records.append({'event':i,'start':start,'source':list(A),'target':list(target),'center_error_mm':(target-center).length*1000,'landmarks':marks,'tool_hold_until':start+54,'next_event':start+60,'faces':[p.index for p in faces]})
s.frame_set(315);bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True)
(Q/'Notes/approved_v016_integration.json').write_text(json.dumps({'native':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'shared':'Waveform_shared_v021.blend','preset':'Approved_beam_exchange_v001.json','approved_review':'Waveform_active_patch_fast_v022.blend','frames':756,'fps':24,'seconds':31.5,'events':records,'timing':'54frame approved exchange/hold +6frame target turn, last event then finishing pullback660..756','approval':'Owner approved component appearance; whole-shot review remains open'},indent=2));print('APPROVED_PRODUCTION_READY')
