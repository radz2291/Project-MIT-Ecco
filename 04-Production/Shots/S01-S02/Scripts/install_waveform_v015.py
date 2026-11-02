"""Six-second exchanges; staged reveal, breathing amplitude and close camera."""
import bpy,json,sys,hashlib,re,math
from pathlib import Path
from mathutils import Matrix,Vector
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');Q=R/'04-Production/Shots/S01-S02';sys.path.insert(0,str(R/'04-Production/Shared/Assets/Effects/Waveform/Scripts'))
from pulse_asset_api import get_input,set_input,arrival_readouts
from pulse_graph import Graph
out=Q/'Scenes/S01-S02_production_v015.blend';assert not out.exists() or '--candidate-rebuild' in sys.argv;s=bpy.context.scene;assert 'v014' in bpy.data.filepath
bha=bpy.data.objects['BHA sequence assembly'];cam=s.camera;poses=[]
for f in [300+48*i for i in range(6)]:s.frame_set(f);poses.append(bha.matrix_world.copy())
s.frame_set(300);basecam=cam.matrix_world.copy();relative=poses[0].inverted()@basecam;original_lens=cam.data.lens;pull=[]
routes=json.loads((Q/'Notes/waveform_v013_install.json').read_text())['events'];mids=[(Vector(r['surface_hit'])+Vector(r['wall']))/2 for r in routes];deltas=[m-mids[0] for m in mids]
for f in range(97):
 old=300+228*f/96;s.frame_set(int(old),subframe=old-int(old));pull.append((1152+f,cam.matrix_world.copy(),cam.data.lens))
def trim(obj):
 if obj.animation_data and obj.animation_data.action:
  obj.animation_data.action=obj.animation_data.action.copy()
  for l in obj.animation_data.action.layers:
   for st in l.strips:
    for bag in st.channelbags:
     for fc in bag.fcurves:
      for i in range(len(fc.keyframe_points)-1,-1,-1):
       if fc.keyframe_points[i].co.x>=300:fc.keyframe_points.remove(fc.keyframe_points[i],fast=True)
def posekey(obj,f,m):
 obj.matrix_world=m
 for p in ['location','rotation_quaternion','scale']:obj.keyframe_insert(p,frame=f)
def linear(obj):
 for l in obj.animation_data.action.layers:
  for st in l.strips:
   for b in st.channelbags:
    for fc in b.fcurves:
     for k in fc.keyframe_points:
      if k.co.x>=300:k.interpolation='LINEAR'
for obj in [bha,cam,cam.data]:trim(obj)
for i,m in enumerate(poses):
 start=300+144*i
 for f in [start,start+132]:posekey(bha,f,m);posekey(cam,f,m@relative);cam.data.lens=original_lens;cam.data.keyframe_insert('lens',frame=f)
posekey(bha,1248,poses[-1]);offset=poses[-1]@poses[0].inverted()
for f,m,lens in pull:posekey(cam,f,offset@m);cam.data.lens=lens;cam.data.keyframe_insert('lens',frame=f)
linear(bha);linear(cam);linear(cam.data);s.frame_end=1248
# Material color transitions must agree with the new geometry reveal cues.
oldreceipts=[318,360,402,450,498,524];colors={}
for i,old in enumerate(oldreceipts,1):
 mats=[m for m in bpy.data.materials if re.match(r'Unified cell '+str(i)+r'(\s|$)',m.name)]
 for t in [0,6,15]:
  s.frame_set(old+t)
  for m in mats:colors[(m.name,t)]=tuple(m.diffuse_color)
with bpy.data.libraries.load(str(R/'04-Production/Shared/Assets/Effects/Waveform/Waveform_shared_v020.blend'),link=True) as (a,b):b.objects=['WF_MASTER_CONTROLS','WF_PULSE_FIELD']
ctrl,template=b.objects;s.collection.objects.link(ctrl);wall=bpy.data.objects['ONE WALL - old history and current cells share topology'];rows=[]
for n in wall.modifiers[0].node_group.nodes:
 if n.type=='GROUP' and 'Settle frames' in n.inputs:n.inputs['Settle frames'].default_value=12
for i in range(1,7):
 o=bpy.data.objects[f'WF sequence event {i}'];mod=o.modifiers[0];before={}
 for x in mod.node_group.interface.items_tree:
  if getattr(x,'in_out','')=='INPUT' and x.socket_type!='NodeSocketGeometry':
   v=get_input(mod,x.name);before[x.name]=tuple(v) if x.socket_type in ['NodeSocketVector','NodeSocketColor'] else v
 o.data=template.data;mod.node_group=template.modifiers[0].node_group
 for k,v in before.items():set_input(mod,k,v)
 start=300+144*(i-1);impact=start+41
 settings={'Start frame':float(start),'Beam opening frames':5.,'Beam setup frames':8.,'Beam closing frames':5.,'Travel frames':30.,'Return travel override':30.,'Reflection delay':10.,'Tail allowance':20.,'Lead rest frames':0.,'Pulse width':1.,'Head fade':2.,'Tail fade':3.,'Amplitude breath':.32,'Breath period frames':48.}
 for k,v in settings.items():set_input(mod,k,v)
 for p in wall.data.polygons:
  if re.match(r'Unified cell '+str(i)+r'(\s|$)',wall.data.materials[p.material_index].name):wall.data.attributes['ecco_receipt_frame'].data[p.index].value=impact-1
 for m in bpy.data.materials:
  if (m.name,0) in colors and re.match(r'Unified cell '+str(i)+r'(\s|$)',m.name):
   m.animation_data_clear()
   for f,t in [(impact-1,0),(impact+4,6),(impact+12,15)]:m.diffuse_color=colors[(m.name,t)];m.keyframe_insert('diffuse_color',frame=f)
 s.frame_set(start+40);rows.append({'event':i,'start':start,'connected':start+5,'pulse_launch':start+8,'tile_impact':impact,'tile_settled':impact+12,'feedback_launch':start+68,'feedback_peak_arrives':start+101,'exchange_complete':start+118,'beam_closed':start+123,'turn_start':start+132,'next_target':start+144,'settings':settings,'readouts':arrival_readouts(o)})
g=Graph('S15 shot camera viewing wedge');angle=g.input('Viewing half angle degrees','NodeSocketFloat',30.,5.,45.);on=g.input('Enabled','NodeSocketBool',True);pos=g.node('GeometryNodeInputPosition');info=g.node('GeometryNodeObjectInfo');info.transform_space='RELATIVE';info.inputs['Object'].default_value=cam
rad=g.vop('NORMALIZE',g.vop('MULTIPLY',pos.outputs['Position'],(1,1,0)));view=g.vop('NORMALIZE',g.vop('MULTIPLY',info.outputs['Location'],(1,1,0)));sel=g.op('GREATER_THAN',g.vop('DOT_PRODUCT',rad,view),g.op('COSINE',g.op('MULTIPLY',angle,math.pi/180)));tm=g.node('GeometryNodeInputSceneTime');sel=g.op('MULTIPLY',sel,g.op('MULTIPLY',on,g.op('GREATER_THAN',tm.outputs['Frame'],299.9)));d=g.node('GeometryNodeDeleteGeometry');d.domain='FACE';g.link(g.i.outputs['Geometry'],d.inputs['Geometry']);g.link(sel,d.inputs['Selection']);g.link(d.outputs['Geometry'],g.o.inputs['Geometry']);wall.modifiers.new('Shot camera viewing wedge — inspection cutaway','NODES').node_group=g.g
s.frame_set(305);bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True)
(Q/'Notes/waveform_v015_install.json').write_text(json.dumps({'scene':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'fps':24,'cycle_frames':144,'scene_frames':1248,'scene_seconds':52,'events':rows,'camera':'entry1..299 retained; follows held hardware during exchanges300..1152; final original pullback path applied relative to final pose1152..1248','material_reveal':'all six cell color transitions and geometry retimed together;12frame settle completes before feedback','motion':'amplitude .32 native sinusoidal breathing,48frame period; width remains1'},indent=2));print('V015_SAVED')
