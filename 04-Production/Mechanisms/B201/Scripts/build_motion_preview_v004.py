"""Reusable keyed pulse/contact/echo proof. Explicitly excludes KIV Still05."""
import bpy,math,json,hashlib,time,sys
from pathlib import Path
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
sys.path.insert(0,str(Path(__file__).resolve().parent))
from fast_preview import configure
P=Path(__file__).resolve().parents[3];M=P/'Mechanisms/B201';E=P/'Records/Tasks/T-007/Evidence/Motion_v004';E.mkdir(parents=True,exist_ok=True)
OUT=M/'Scenes/B201_pulse-echo_fast-preview_v004.blend';FR=M/'Previews/Motion_v004/Frames';FR.mkdir(parents=True,exist_ok=True)
assert not OUT.exists(),'Preserve existing scene; version before rebuilding'
r=json.loads((P/'Records/Tasks/T-007/Evidence/Still_04/build-render_still04_v003.json').read_text());src=P/r['parent_scene']
source=M/'Scenes/B201_returning-echo_still04_v003.blend';assert hashlib.sha256(source.read_bytes()).hexdigest()==r['scene_sha256']
bpy.ops.wm.open_mainfile(filepath=str(source));s=bpy.context.scene
camera={'location':list(s.camera.location),'rotation':list(s.camera.rotation_euler),'lens_mm':s.camera.data.lens}
origin0=Vector(r['emitter_reference']);receiver0=Vector(r['receiver_surface']);wall0=Vector(r['wall_origin']);normal0=(wall0-receiver0).normalized()
root,product_mat,instances=configure(s,32)
control=bpy.data.objects.new('B201_MOTION_CONTROL',None);bpy.data.collections['FAST_PREVIEW_PRODUCT'].objects.link(control)
for name in ('transmit','receive','outgoing_fade','return_fade'):control[name]=0.
control['timing']='Slowed illustrative preview frames, not physical acoustic time or calibrated RPM'
control['excluded']='Still05, waveform, distance line, formulas, labels and numbers'
contact=bpy.data.objects['ACOUSTIC_CONTACT_CONTROLLER']
wallob=bpy.data.objects['T6_WALL_CONTACT_SECTION'];tree=BVHTree.FromPolygons([wallob.matrix_world@v.co for v in wallob.data.vertices],[list(p.vertices) for p in wallob.data.polygons])
events=[];step=(wall0-receiver0).length/20
for i,degrees in enumerate((0,6,12)):
 rot=Matrix.Rotation(math.radians(degrees),4,'X');receiver=rot@receiver0;direction=(rot.to_3x3()@normal0).normalized()
 hit=tree.ray_cast(receiver,direction);assert hit[0] is not None
 wall=hit[0];distance=(wall-receiver).length;leg=round(distance/step);start=1+i*80;emit=start+7;arrival=emit+leg;receive=arrival+leg
 assert receive<start+64
 events.append({'cycle':i+1,'start':start,'end':start+79,'rotation_degrees':degrees,'emit_frame':emit,'contact_frame':arrival,'receive_frame':receive,'leg_frames':leg,'receiver':list(receiver),'wall':list(wall),'standoff_m':distance,'ray_error_m':tree.find_nearest(wall)[3]})
def socket_driver(socket,prop):
 fc=socket.driver_add('default_value');d=fc.driver;v=d.variables.new();v.name='v';v.targets[0].id=control;v.targets[0].data_path='["'+prop+'"]';d.expression='v'
def gain(mat,prop):
 n=mat.node_tree.nodes;l=mat.node_tree.links;mix=next(x for x in n if x.bl_idname=='ShaderNodeMixShader');old=mix.inputs[0].links[0].from_socket
 val=n.new('ShaderNodeValue');val.label=prop;socket_driver(val.outputs[0],prop);node=n.new('ShaderNodeMath');node.operation='MULTIPLY';l.new(old,node.inputs[0]);l.new(val.outputs[0],node.inputs[1]);l.new(node.outputs[0],mix.inputs[0])
tx=sorted([o for o in s.objects if o.name.startswith('OUTGOING_WAVEFRONT_ILLUSTRATION_')],key=lambda o:o.name)
tx_radius=[o['radius_m'] for o in tx];tx_lags=[max(tx_radius)-v for v in tx_radius]
for o in tx:
 for v in o.data.vertices:v.co-=origin0
 gain(o.data.materials[0],'outgoing_fade')
echo=[bpy.data.objects['RETURNING_ECHO_FIRST_RECEPTION']]+sorted([o for o in s.objects if o.name.startswith('RETURNING_ECHO_FOLLOWER_')],key=lambda o:o.name)
echo_radius=[o['radius_m'] for o in echo];echo_lags=[r['return_radius_m']-v for v in echo_radius]
for o in echo:
 for v in o.data.vertices:v.co-=wall0
 gain(o.data.materials[0],'return_fade')
# Actual sensor response: cyan transmit then emerald reception, no new surface objects.
n=product_mat.node_tree.nodes;l=product_mat.node_tree.links;shader=next(x for x in n if x.bl_idname=='ShaderNodeBsdfPrincipled');strength=shader.inputs['Emission Strength'].links[0].from_node;weight=strength.inputs[0].links[0].from_socket
def mathnode(kind,a,b):
 node=n.new('ShaderNodeMath');node.operation=kind
 for i,v in enumerate((a,b)):
  if isinstance(v,(int,float)):node.inputs[i].default_value=v
  else:l.new(v,node.inputs[i])
 return node.outputs[0]
txval=n.new('ShaderNodeValue');rxval=n.new('ShaderNodeValue');socket_driver(txval.outputs[0],'transmit');socket_driver(rxval.outputs[0],'receive')
energy=mathnode('ADD',mathnode('MULTIPLY',txval.outputs[0],.8),mathnode('MULTIPLY',rxval.outputs[0],1.1));l.new(mathnode('MULTIPLY',weight,energy),shader.inputs['Emission Strength'])
color=n.new('ShaderNodeMixRGB');color.inputs[1].default_value=(.18,.55,1,1);color.inputs[2].default_value=(.035,.60,.26,1);l.new(rxval.outputs[0],color.inputs[0]);l.new(color.outputs[0],shader.inputs['Emission Color'])
tint=shader.inputs['Base Color'].links[0].from_node;old=tint.inputs[0].links[0].from_socket;l.new(mathnode('MULTIPLY',old,rxval.outputs[0]),tint.inputs[0])
sensor_dist=next(x for x in n if x.bl_idname=='ShaderNodeVectorMath' and x.operation=='DISTANCE')
from wall_contact_flow import build_contact_flow
patch_dist=build_contact_flow(wallob,contact,origin0,wall0,normal0,step)
def clamp(x):return max(0.,min(1.,x))
def smooth(x):x=clamp(x);return x*x*(3-2*x)
def keyed_prop(obj,name,value,frame):obj[name]=value;obj.keyframe_insert(data_path='["'+name+'"]',frame=frame)
states=[]
for f in range(1,241):
 i=min((f-1)//80,2);e=events[i];next_e=events[min(i+1,2)]
 blend=smooth((f-(e['start']+70))/9);angle=math.radians(e['rotation_degrees']+(next_e['rotation_degrees']-e['rotation_degrees'])*blend)
 rot=Matrix.Rotation(angle,4,'X');root.rotation_euler=(angle,0,0);root.keyframe_insert(data_path='rotation_euler',frame=f)
 receiver=rot@receiver0;direction=(rot.to_3x3()@normal0).normalized();wall=tree.ray_cast(receiver,direction)[0];distance=(wall-receiver).length
 leg=e['leg_frames']
 # Smooth the approach into the readable surface sweep, with continuous velocity at contact.
 t=clamp((f-e['emit_frame'])/leg);end_slope=.0005*leg/distance
 out_radius=distance*((2-end_slope)*t+(end_slope-1)*t*t) if f<=e['contact_frame'] else distance+(f-e['contact_frame'])*.0005
 in_radius=max(0,(f-e['contact_frame'])/leg*distance)
 out_fade=smooth((f-e['emit_frame'])/3)*(1-smooth((f-e['contact_frame']-2)/12))
 in_fade=smooth((f-e['contact_frame'])/3)*(1-smooth((f-e['receive_frame']-2)/9))
 transmit=smooth((f-e['emit_frame']+2)/2)*(1-smooth((f-e['emit_frame']-2)/6))
 receive=smooth((f-e['receive_frame']+1)/2)*(1-smooth((f-e['receive_frame']-12)/9))
 for name,value in (('transmit',transmit),('receive',receive),('outgoing_fade',out_fade),('return_fade',in_fade)):keyed_prop(control,name,value,f)
 for o,base,lag in zip(tx,tx_radius,tx_lags):
  rad=max(0,out_radius-lag);o.location=receiver;o.rotation_euler=(angle,0,0);o.scale=(max(rad,.00001)/base,)*3;o.hide_render=out_fade<.001 or rad<=.0005
  for path in ('location','rotation_euler','scale','hide_render'):o.keyframe_insert(data_path=path,frame=f)
 for o,base,lag in zip(echo,echo_radius,echo_lags):
  rad=max(0,in_radius-lag);o.location=wall;o.rotation_euler=(angle,0,0);o.scale=(max(rad,.00001)/base,)*3;o.hide_render=in_fade<.001 or rad<=.0005
  for path in ('location','rotation_euler','scale','hide_render'):o.keyframe_insert(data_path=path,frame=f)
 contact.location=wall;contact.keyframe_insert(data_path='location',frame=f)
 contact_radius=out_radius
 patch=1-smooth((f-(e['start']+66))/5)
 keyed_prop(contact,'leading_radius_m',contact_radius,f);keyed_prop(contact,'scan_fade',patch,f)
 for socket in (sensor_dist.inputs[1],patch_dist.inputs[1]):socket.default_value=receiver;socket.keyframe_insert(data_path='default_value',frame=f)
 states.append({'frame':f,'cycle':i+1,'outgoing_radius_m':out_radius,'return_radius_m':in_radius,'transmit':transmit,'receive':receive,'patch_fade':patch})
# Native keyframes make the saved scene independently playable/renderable, no handlers.
for action in bpy.data.actions:
 if action.library:continue
 for layer in action.layers:
  for strip in layer.strips:
   if not hasattr(strip,'channelbags'):continue
   for bag in strip.channelbags:
    for fc in bag.fcurves:
     for k in fc.keyframe_points:k.interpolation='CONSTANT' if fc.data_path=='hide_render' else 'LINEAR'
for e in events:
 for kind in ('emit','contact','receive'):s.timeline_markers.new(f'Ping {e["cycle"]}: {kind}',frame=e[kind+'_frame'])
s.render.fps=24;s.frame_start=1;s.frame_end=240;s.render.image_settings.file_format='PNG';s.render.filepath='//../Previews/Motion_v004/Frames/frame_'
s['preview_scope']='Three slowed pulse/contact/same-sensor echo cycles. Still05 excluded. No waveform, distance graphic, labels or numbers.'
bpy.context.window.view_layer=s.view_layers['FAST model and mechanism'];s.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(OUT),relative_remap=False)
record={'scene':str(OUT.relative_to(P)),'scene_sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'source_still04_sha256':r['scene_sha256'],'inputs':r['inputs'],'product_instances':instances,'events':events,'camera':camera,'fps':24,'frames':240,'duration_seconds':10,'resolution':[960,540],'engine':'BLENDER_EEVEE','samples':32,'Still05_included':False,'waveform_included':False,'physical_time_claim':False,'frozen_geometry_consumer':True,'preview_quality_changes':'EEVEE blended transparency, reduced metal/shadows for readable fast preview; original stills/masters untouched','authoring_states':states,'contact_model':'Local sphere-rock signed intersection drives cell maturation and age decay; no global patch appearance envelope','surface_sweep_m_per_frame':.0005,'continuous_contact_velocity':True,'illustrative_contact_timing':True}
(E/'build.json').write_text(json.dumps(record,indent=2));print('ANIMATION_BUILD_PASS',events,flush=True)
bpy.ops.wm.open_mainfile(filepath=str(OUT));s=bpy.context.scene
checks=sorted(set([1,240]+[e[k] for e in events for k in ('emit_frame','contact_frame','receive_frame')]+[18,27,29,31,34,38,42,50]))
times=[]
for frame in checks:
 s.frame_set(frame);s.render.filepath=str(M/f'Previews/Motion_v004/B201_inspect_f{frame:03d}_v004.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);times.append({'frame':frame,'seconds':time.perf_counter()-t});(E/'inspection-render-times.json').write_text(json.dumps(times,indent=2));print('INSPECTION',times[-1],flush=True)
