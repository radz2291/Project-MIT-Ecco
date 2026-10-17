"""B201 pre-client consumer. Frozen v005 is input, never overwritten."""
import bpy, json, math, hashlib, sys, time
from pathlib import Path
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree
P=Path(__file__).resolve().parents[3]; M=P/'Mechanisms/B201'; E=P/'Records/Tasks/T-007/Evidence/Motion_v006'; E.mkdir(parents=True,exist_ok=True)
OUT=M/'Scenes/B201_pulse-echo_refinement_v006.blend'
assert not OUT.exists(), 'Version before rebuilding'
old=json.loads((P/'Records/Tasks/T-007/Evidence/Motion_v005/build.json').read_text())
src=P/old['scene']; assert hashlib.sha256(src.read_bytes()).hexdigest()==old['scene_sha256']
bpy.ops.wm.open_mainfile(filepath=str(src)); s=bpy.context.scene
bpy.context.window.view_layer=s.view_layers['FAST model and mechanism']; s.frame_set(1)
root=bpy.data.objects['FAST_PREVIEW_TOOL_ROTATION']; control=bpy.data.objects['B201_MOTION_CONTROL']; contact=bpy.data.objects['ACOUSTIC_CONTACT_CONTROLLER']
wallob=bpy.data.objects['T6_WALL_CONTACT_SECTION']; product=bpy.data.materials['FAST_PREVIEW_LOCAL_PRODUCT_LOOK']
receiver0=Vector(old['events'][0]['receiver']); wall0=Vector(old['events'][0]['wall']); normal0=(wall0-receiver0).normalized()
tree=BVHTree.FromPolygons([wallob.matrix_world@v.co for v in wallob.data.vertices],[list(p.vertices) for p in wallob.data.polygons])
tx=sorted([o for o in s.objects if o.name.startswith('OUTGOING_WAVEFRONT_ILLUSTRATION_')],key=lambda o:o.name)
tx_base=[o['radius_m'] for o in tx]; tx_lags=[max(tx_base)-r for r in tx_base]
echo=[bpy.data.objects['RETURNING_ECHO_FIRST_RECEPTION']]+sorted([o for o in s.objects if o.name.startswith('RETURNING_ECHO_FOLLOWER_')],key=lambda o:o.name)
echo_base=[o['radius_m'] for o in echo]; echo_lags=[max(echo_base)-r for r in echo_base]
def driven_socket(socket,prop):
 d=socket.driver_add('default_value').driver; v=d.variables.new(); v.name='v'; v.targets[0].id=control; v.targets[0].data_path='["'+prop+'"]'; d.expression='v'
def multiply_opacity(mat,prop):
 n=mat.node_tree.nodes; l=mat.node_tree.links; mix=next(x for x in n if x.bl_idname=='ShaderNodeMixShader'); oldsock=mix.inputs[0].links[0].from_socket
 val=n.new('ShaderNodeValue'); val.label=prop; driven_socket(val.outputs[0],prop)
 mul=n.new('ShaderNodeMath'); mul.operation='MULTIPLY'; l.new(oldsock,mul.inputs[0]); l.new(val.outputs[0],mul.inputs[1]); l.new(mul.outputs[0],mix.inputs[0])
for i,o in enumerate(tx): multiply_opacity(o.data.materials[0],f'wall_stop_{i}')
sensor_dist=next(n for n in product.node_tree.nodes if n.bl_idname=='ShaderNodeVectorMath' and n.operation=='DISTANCE')
patch_dist=[n for n in wallob.data.materials[0].node_tree.nodes if n.bl_idname=='ShaderNodeVectorMath' and n.operation=='DISTANCE'][-1]
patch_before={k:contact[k] for k in ('scan_radius_x_m','scan_radius_y_m','scan_opacity')}
contact['scan_radius_x_m']*=.42; contact['scan_radius_y_m']*=.42; contact['scan_opacity']*=.48
events=[]
for i,(degrees,start,emit,leg,end,rotate) in enumerate(((0,1,12,24,143,120),(6,144,150,13,191,180),(12,192,198,12,240,240))):
 rot=Matrix.Rotation(math.radians(degrees),4,'X'); receiver=rot@receiver0; direction=rot.to_3x3()@normal0; wall=tree.ray_cast(receiver,direction)[0]; assert wall is not None
 events.append(dict(cycle=i+1,start=start,end=end,rotate_start=rotate,rotation_degrees=degrees,emit_frame=emit,contact_frame=emit+leg,receive_frame=emit+2*leg,leg_frames=leg,receiver=list(receiver),wall=list(wall),standoff_m=(wall-receiver).length))
def smooth(x): x=max(0,min(1,x)); return x*x*(3-2*x)
def key(obj,prop,value,f): obj[prop]=value; obj.keyframe_insert(data_path='["'+prop+'"]',frame=f)
# Native camera-facing editorial layer, deliberately simple and editable.
coll=bpy.data.collections.new('B201_ECHO_TIMING_v006'); s.collection.children.link(coll)
bpy.context.view_layer.update()
cam=s.camera; corners=cam.data.view_frame(scene=s); depth=cam.data.clip_start*2.5
hw=max(abs(v.x/v.z*depth) for v in corners); hh=max(abs(v.y/v.z*depth) for v in corners)
def point(x,y,z=0): return ((x-.5)*2*hw,(y-.5)*2*hh,-depth+z*depth)
def material(name,color,prop):
 mat=bpy.data.materials.new(name); mat.use_nodes=True; n=mat.node_tree.nodes; n.clear(); l=mat.node_tree.links
 out=n.new('ShaderNodeOutputMaterial'); mix=n.new('ShaderNodeMixShader'); tr=n.new('ShaderNodeBsdfTransparent'); em=n.new('ShaderNodeEmission'); em.inputs['Color'].default_value=(*color,1); em.inputs['Strength'].default_value=1
 val=n.new('ShaderNodeValue'); driven_socket(val.outputs[0],prop); l.new(val.outputs[0],mix.inputs[0]); l.new(tr.outputs[0],mix.inputs[1]); l.new(em.outputs[0],mix.inputs[2]); l.new(mix.outputs[0],out.inputs[0]); mat.surface_render_method='BLENDED'; return mat
white=material('TIMING editorial white',(.8,.85,.88),'graphic'); cyan=material('TIMING transmitted cyan',(.12,.55,1),'sent_graphic'); green=material('TIMING returned emerald',(.08,.65,.32),'echo_graphic'); gray=material('TIMING quiet interval',(.36,.43,.47),'interval_graphic'); black=material('TIMING quiet backing',(.002,.004,.006),'panel')
def link(ob,mat):
 coll.objects.link(ob); ob.parent=cam; ob.data.materials.append(mat); ob.visible_shadow=False; return ob
me=bpy.data.meshes.new('Timing backing'); me.from_pydata([point(.03,.018,-.0005),point(.97,.018,-.0005),point(.97,.285,-.0005),point(.03,.285,-.0005)],[],[(0,1,2,3)]); link(bpy.data.objects.new('Timing quiet backing',me),black)
font_path=Path('C:/Windows/Fonts/segoeui.ttf'); font=bpy.data.fonts.load(str(font_path)) if font_path.exists() else None
def text(name,body,x,y,pixels,mat):
 c=bpy.data.curves.new(name,'FONT'); c.body=body; c.align_x='CENTER'; c.size=2*hh*pixels*1.65/540; c.space_character=1.04
 if font: c.font=font
 ob=link(bpy.data.objects.new(name,c),mat); ob.location=point(x,y,.0003); return ob
text('Timing purpose','Echo timing reveals distance',.5,.233,23,white)
text('Transmit label','Pulse sent',.27,.13,16,cyan); text('Echo label','Echo received',.73,.13,16,green)
text('Round trip label','Round-trip delay',.5,.047,16,gray)
def line(name,pts,mat,width=1.25):
 c=bpy.data.curves.new(name,'CURVE'); c.dimensions='3D'; c.bevel_depth=2*hh*width/540/2; c.bevel_resolution=2; sp=c.splines.new('POLY'); sp.points.add(len(pts)-1)
 for v,(x,y) in zip(sp.points,pts): v.co=(*point(x,y,.0002),1)
 return link(bpy.data.objects.new(name,c),mat)
line('Timing baseline',[(.18,.19),(.82,.19)],gray,.7)
line('Transmit peak',[(.25,.19),(.26,.19),(.27,.224),(.28,.172),(.29,.19),(.30,.19)],cyan,1.5)
line('Echo peak',[(.70,.19),(.71,.19),(.73,.216),(.75,.178),(.76,.19)],green,1.5)
line('Round-trip interval',[(.27,.10),(.27,.085),(.73,.085),(.73,.10)],gray,1)
# Render editorial type in its own transparent layer so near geometry cannot occlude it.
coll.objects.link(control)
s.view_layers['FAST model and mechanism'].layer_collection.children[coll.name].exclude=True
overlay=s.view_layers.new('B201 timing editorial'); overlay.use=True
for child in overlay.layer_collection.children: child.exclude=child.name not in (coll.name,'B201_REVIEW_CAMERA')
g=s.compositing_node_group; n=g.nodes; l=g.links; outnode=next(x for x in n if x.bl_idname=='NodeGroupOutput'); prior=outnode.inputs['Image'].links[0].from_socket
rl=n.new('CompositorNodeRLayers'); rl.scene=s; rl.layer=overlay.name
over=n.new('CompositorNodeAlphaOver'); l.new(prior,over.inputs['Background']); l.new(rl.outputs['Image'],over.inputs['Foreground']); l.new(over.outputs[0],outnode.inputs['Image'])
states=[]
for f in range(1,241):
 e=events[0 if f<144 else 1 if f<192 else 2]; next_e=events[min(e['cycle'],2)]
 blend=smooth((f-e['rotate_start'])/max(1,e['end']-e['rotate_start'])); angle=math.radians(e['rotation_degrees']+(next_e['rotation_degrees']-e['rotation_degrees'])*blend)
 rot=Matrix.Rotation(angle,4,'X'); root.rotation_euler=(angle,0,0); root.keyframe_insert(data_path='rotation_euler',frame=f)
 receiver=rot@receiver0; wall=tree.ray_cast(receiver,rot.to_3x3()@normal0)[0]; distance=(wall-receiver).length; speed=distance/e['leg_frames']
 out_rad=max(0,(f-e['emit_frame'])*speed); in_rad=max(0,(f-e['contact_frame'])*speed)
 out_fade=smooth((f-e['emit_frame'])/3); in_fade=smooth((f-e['contact_frame'])/2)*(1-smooth((f-e['receive_frame']-2)/7))
 transmit=smooth((f-e['emit_frame']+2)/2)*(1-smooth((f-e['emit_frame']-2)/5)); receive=smooth((f-e['receive_frame'])/2)*(1-smooth((f-e['receive_frame']-8)/7))
 for name,val in (('transmit',transmit),('receive',receive),('outgoing_fade',out_fade),('return_fade',in_fade)): key(control,name,val,f)
 front_gains=[]
 for i,(ob,base,lag) in enumerate(zip(tx,tx_base,tx_lags)):
  rad=max(0,out_rad-lag); arrival=e['contact_frame']+lag/speed; stop=1-smooth((f-arrival)/2); front_gains.append(stop); key(control,f'wall_stop_{i}',stop,f)
  ob.location=receiver; ob.rotation_euler=(angle,0,0); ob.scale=(max(rad,.00001)/base,)*3; ob.hide_render=out_fade*stop<.001 or rad<=.0005
  for path in ('location','rotation_euler','scale','hide_render'): ob.keyframe_insert(data_path=path,frame=f)
 for ob,base,lag in zip(echo,echo_base,echo_lags):
  rad=max(0,in_rad-lag); ob.location=wall; ob.rotation_euler=(angle,0,0); ob.scale=(max(rad,.00001)/base,)*3; ob.hide_render=in_fade<.001 or rad<=.0005
  for path in ('location','rotation_euler','scale','hide_render'): ob.keyframe_insert(data_path=path,frame=f)
 contact.location=wall; contact.keyframe_insert(data_path='location',frame=f)
 patch=1-smooth((f-e['contact_frame']-3)/7)
 key(contact,'leading_radius_m',out_rad,f); key(contact,'propagation_m_per_frame',speed,f); key(contact,'scan_fade',patch,f)
 for sock in (sensor_dist.inputs[1],patch_dist.inputs[1]): sock.default_value=receiver; sock.keyframe_insert(data_path='default_value',frame=f)
 # Only first event is explained. Peaks appear with the actual observed event.
 appear=smooth((f-8)/4)*(1-smooth((f-116)/8))
 sent=appear if f>=12 else 0; returned=appear*smooth((f-60)/3); interval=appear*smooth((f-60)/6)
 for name,val in (('panel',appear*.94),('graphic',returned),('sent_graphic',sent),('echo_graphic',returned),('interval_graphic',interval)): key(control,name,val,f)
 states.append(dict(frame=f,cycle=e['cycle'],outgoing_radius_m=out_rad,return_radius_m=in_rad,front_gains=front_gains,patch_fade=patch,graphic=returned))
for action in bpy.data.actions:
 if action.library: continue
 for layer in action.layers:
  for strip in layer.strips:
   for bag in getattr(strip,'channelbags',[]):
    for fc in bag.fcurves:
     for k in fc.keyframe_points: k.interpolation='CONSTANT' if fc.data_path=='hide_render' else 'LINEAR'
s.timeline_markers.clear()
for e in events:
 for kind in ('emit','contact','receive'): s.timeline_markers.new(f'Ping {e["cycle"]}: {kind}',frame=e[kind+'_frame'])
control['excluded']='B202 accumulation, reconstruction, equations, numerical calibration'; control['timing']='Illustrative and time-compressed; not physical TOF or RPM'
s['preview_scope']='B201 client refinement: full explained echo measurement then two shorter acquisitions. Native timing graphics are conceptual.'
s.render.fps=24; s.frame_start=1; s.frame_end=240; s.render.filepath='//../Previews/Motion_v006/Frames/frame_'; s.frame_set(1)
bpy.ops.file.pack_all(); bpy.ops.wm.save_as_mainfile(filepath=str(OUT),relative_remap=False)
record={**{k:old[k] for k in ('inputs','product_instances','camera')},'scene':str(OUT.relative_to(P)),'scene_sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'baseline_scene':str(src.relative_to(P)),'baseline_sha256':old['scene_sha256'],'events':events,'authoring_states':states,'patch_before':patch_before,'patch_after':{k:contact[k] for k in patch_before},'font':str(font_path),'fps':24,'frames':240,'duration_seconds':10,'resolution':[960,540],'physical_time_claim':False,'waveform_kind':'Conceptual two-event timing cue, no sampled data or numeric calibration','wall_stop':'Each front loses opacity over two frames after its own ray-axis wall arrival; no intact continuing cyan packet','executor_self_check':True}
(E/'build.json').write_text(json.dumps(record,indent=2)); print('BUILD_PASS',flush=True)
if '--inspect' in sys.argv:
 times=[]
 for f in (24,36,39,44,54,60,72,100,163,176,210,222):
  s.frame_set(f); path=M/f'Previews/Motion_v006/Inspect/f{f:03d}.png'; path.parent.mkdir(parents=True,exist_ok=True); s.render.filepath=str(path); t=time.perf_counter(); bpy.ops.render.render(write_still=True); times.append(dict(frame=f,seconds=time.perf_counter()-t))
 (E/'inspection-render-times.json').write_text(json.dumps(times,indent=2))
