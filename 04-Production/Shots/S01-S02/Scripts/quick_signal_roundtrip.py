"""Fast finite pulse-train proof: complete cyan send, then violet return."""
import bpy,math,time,json,numpy as np
from pathlib import Path
from mathutils import Vector
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');Q=R/'04-Production/Shots/S01-S02';P=Q/'Previews/Waveform-direction-v005';P.mkdir(exist_ok=True);s=bpy.context.scene
if bpy.data.is_dirty:bpy.ops.wm.save_as_mainfile(filepath=str(Q/f'Scenes/Pulse_session_before_roundtrip_{int(time.time())}.blend'),copy=True,compress=True)
spacing=bpy.data.node_groups['QUICK pulse strand separation'];camera=s.camera
for layer in s.view_layers[0].layer_collection.children:layer.exclude=True
for ob in list(s.collection.objects):
 if not ob.library:ob.hide_render=True;ob.hide_set(True)
col=bpy.data.collections.new('QUICK complete send and reflected train');s.collection.children.link(col)
axis=Vector((.3583680987,-.9335803986,0));side=Vector((-.9335803986,-.3583680987,0));up=Vector((0,0,1));gap=.0245758537;strands=5;samples=145
def mat(name,color):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);return m
g=bpy.data.node_groups.new('QUICK finite packet head and tail','GeometryNodeTree');g.is_modifier=True
for name,io,typ,value in [('Geometry','INPUT','NodeSocketGeometry',None),('Geometry','OUTPUT','NodeSocketGeometry',None),('Start frame','INPUT','NodeSocketFloat',5.),('Travel frames','INPUT','NodeSocketFloat',16.),('Train frames','INPUT','NodeSocketFloat',20.),('Reverse','INPUT','NodeSocketBool',False)]:
 x=g.interface.new_socket(name=name,in_out=io,socket_type=typ)
 if value is not None:x.default_value=value
n=g.nodes;l=g.links;i=n.new('NodeGroupInput');out=n.new('NodeGroupOutput');tm=n.new('GeometryNodeInputSceneTime');u=n.new('GeometryNodeInputNamedAttribute');u.data_type='FLOAT';u.inputs['Name'].default_value='pulse_route_u'
def op(kind,a,b):
 node=n.new('ShaderNodeMath');node.operation=kind
 for j,v in enumerate([a,b]):
  if isinstance(v,(int,float)):node.inputs[j].default_value=v
  else:l.new(v,node.inputs[j])
 return node.outputs[0]
sw=n.new('GeometryNodeSwitch');sw.input_type='FLOAT';l.new(i.outputs['Reverse'],sw.inputs['Switch']);l.new(op('SUBTRACT',1,u.outputs['Attribute']),sw.inputs['True']);l.new(u.outputs['Attribute'],sw.inputs['False'])
age=op('SUBTRACT',op('SUBTRACT',tm.outputs['Frame'],i.outputs['Start frame']),op('MULTIPLY',sw.outputs[0],i.outputs['Travel frames']));active=op('MULTIPLY',op('GREATER_THAN',age,0),op('LESS_THAN',age,i.outputs['Train frames']));delete=n.new('GeometryNodeDeleteGeometry');delete.domain='POINT';delete.mode='ALL';l.new(i.outputs['Geometry'],delete.inputs['Geometry']);l.new(op('SUBTRACT',1,active),delete.inputs['Selection']);l.new(delete.outputs['Geometry'],out.inputs[0])
def value(mod,name,v):
 x=next(x for x in mod.node_group.interface.items_tree if getattr(x,'in_out','')=='INPUT' and x.name==name);getattr(mod.properties.inputs,x.identifier).value=v
faces=[]
for strand in range(strands):
 for k in range(samples-1):
  a=(strand*samples+k)*4
  for ring in range(4):faces.append((a+ring,a+(ring+1)%4,a+4+(ring+1)%4,a+4+ring))
def field(name,start,reverse,color,amp):
 def coords(f):
  vs=[]
  for strand in range(strands):
   v=2*strand/(strands-1)-1
   for k in range(samples):
    u=k/(samples-1);distance=1-u if reverse else u;age=f-start-16*distance;edge=max(0,min(1,age/.8))*max(0,min(1,(20-age)/1.2));signal=0
    for onset,gain,width in [(0,1.,1.),(6.2,.75,1.12),(12.8,.9,.87)]:
     t=(age-onset)/((1+.12*distance)*width)+.10*v
     pulse=-.16*math.exp(-((t-1.3)/.45)**2)+math.exp(-((t-2.1)/.27)**2)-.45*math.exp(-((t-2.7)/.4)**2)+.18*math.exp(-((t-4.3)/.9)**2)
     tail=.08*math.sin(math.tau*(t-5)/2.4)*math.exp(-(t-5)/2.4) if 5<t<12 else 0;signal+=gain*(pulse+tail)
    z=.011*(.35+.65*math.sin(math.pi*u)**2)*edge*signal*amp/(1+.25*distance);y=.0015*v*edge;radius=.00008*edge
    for ring in range(4):
     a=ring*math.tau/4;vs.append(axis*(gap*u)+side*(y+radius*math.cos(a))+up*(z+radius*math.sin(a)))
  return vs
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(coords(1),[],faces);mesh.update();ob=bpy.data.objects.new(name,mesh);col.objects.link(ob)
 for j in range(strands):mesh.materials.append(mat(name+' strand '+str(j),tuple(c*(.65+.35*j/(strands-1)) for c in color)))
 for p in mesh.polygons:p.material_index=p.index//((samples-1)*4)
 for attr,values in [('pulse_route_u',[(j//4%samples)/(samples-1) for j in range(len(mesh.vertices))]),('pulse_strand_weight',[2*(j//(samples*4))/(strands-1)-1 for j in range(len(mesh.vertices))])]:a=mesh.attributes.new(attr,'FLOAT','POINT');a.data.foreach_set('value',values)
 ob.shape_key_add(name='Basis');mesh.shape_keys.use_relative=False
 for f in range(2,98):key=ob.shape_key_add(name=f'Frame {f}');key.interpolation='KEY_LINEAR';key.data.foreach_set('co',np.array(coords(f),dtype=np.float32).reshape(-1))
 keys=mesh.shape_keys;keys.eval_time=0;keys.keyframe_insert(data_path='eval_time',frame=1);keys.eval_time=keys.key_blocks[-1].frame;keys.keyframe_insert(data_path='eval_time',frame=97)
 for layer in keys.animation_data.action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for fc in bag.fcurves:
     for k in fc.keyframe_points:k.interpolation='LINEAR'
 mod=ob.modifiers.new('Adjustable strand separation','NODES');mod.node_group=spacing;value(mod,'Strand separation',.65)
 mod=ob.modifiers.new('Finite head / tail window','NODES');mod.node_group=g;value(mod,'Start frame',start);value(mod,'Reverse',reverse)
 return ob
send=field('CYAN outgoing packet',5,False,(.02,.85,1),1.);ret=field('VIOLET reflected packet',43,True,(.75,.22,1),.75)
for end in [0,1]:
 bpy.ops.mesh.primitive_torus_add(major_radius=.011,minor_radius=.00015,major_segments=48,minor_segments=6,location=axis*(end*gap));ob=bpy.context.object;ob.name='Fixed endpoint '+str(end);ob.rotation_mode='QUATERNION';ob.rotation_quaternion=Vector((0,0,1)).rotation_difference(axis)
 for prev in list(ob.users_collection):prev.objects.unlink(ob)
 col.objects.link(ob);ob.data.materials.append(mat('Neutral anchor '+str(end),(.32,.38,.42)))
for label,start,reverse,color in [('SEND',5,False,(.25,.95,1)),('RETURN',43,True,(.9,.4,1))]:
 for part,delay,radius in [('HEAD',0,.00035),('TAIL',20,.0002)]:
  bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=6,radius=radius);ob=bpy.context.object;ob.name=label+' '+part
  for prev in list(ob.users_collection):prev.objects.unlink(ob)
  col.objects.link(ob);ob.data.materials.append(mat(ob.name+' color',color))
  for f in range(1,98):
   u=max(0,min(1,(f-start-delay)/16));u=1-u if reverse else u;ob.location=axis*(gap*u);ob.scale=(1,1,1) if start<=f<=start+36 else (0,0,0);ob.keyframe_insert(data_path='location',frame=f);ob.keyframe_insert(data_path='scale',frame=f)
col.objects.link(camera);camera.hide_render=False;camera.hide_set(False);s.camera=camera;camera.data.ortho_scale=.08;s.frame_start=1;s.frame_end=96;s.render.fps=24;s.render.resolution_x=640;s.render.resolution_y=360;s.frame_set(18)
for label,f in [('Cyan head starts',5),('Cyan head reaches far end',21),('Cyan tail reaches far end',41),('Violet head starts',43),('Violet head reaches source',59),('Violet tail reaches source',79)]:s.timeline_markers.new(label,frame=f)
bpy.ops.wm.save_as_mainfile(filepath=str(Q/'Scenes/Waveform_direction_quick_v005.blend'),compress=True);rows=[]
for f in range(1,97):
 t=time.perf_counter();s.frame_set(f);s.render.filepath=str(P/f'frame_{f:04}.png');bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t;rows.append({'frame':f,'seconds':dt})
 if dt>=5:raise RuntimeError('Render cap failed')
s.frame_set(18);(Q/'Notes/wave_direction_quick_v005.json').write_text(json.dumps({'proof':'Finite three-pulse train. Cyan head/tail completes outgoing journey before violet head/tail returns; larger dot=head, smaller dot=tail. Adjustable separation retained. No shared asset or shot migration.','landmarks':{'send_start':5,'send_head_far':21,'send_tail_far':41,'return_start':43,'return_head_source':59,'return_tail_source':79},'frames':96,'fps':24,'rows':rows},indent=2));result={'native':bpy.data.filepath,'frames':96,'max_seconds':max(r['seconds'] for r in rows)}
