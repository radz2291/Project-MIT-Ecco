import bpy,sys,json,time,math,hashlib
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
B=Path(__file__).resolve().parents[1];P=B.parent
SOURCES={'A':P/'Cinematic-Previs_v006/Scenes/S04_cinematic-previs_v006.blend','B':P/'Communication-Test_v009/Scenes/S04_B_formation-acquisition_v009.blend','C':P/'Communication-Test_v009/Scenes/S04_C_formation-acquisition_v009.blend','D':P/'D-Physical-Wear_v017/Scenes/S04_D_cool-wear-depth_v017.blend'}
def dump(name,data):(B/'Records'/name).write_text(json.dumps(data,indent=2))
def smooth(t):
 t=max(0,min(1,t));return t*t*t*(t*(6*t-15)+10)
def geometry(s):return {o.name:hashlib.sha256(repr(([tuple(v.co) for v in o.data.vertices],[tuple(p.vertices) for p in o.data.polygons])).encode()).hexdigest() for o in s.objects if o.type=='MESH'}
def scalar(socket,values):
 for f,v in enumerate(values,1):socket.default_value=v;socket.keyframe_insert('default_value',frame=f)
def linear_actions():
 for act in bpy.data.actions:
  if act.library:continue
  for layer in act.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for fc in bag.fcurves:
      for k in fc.keyframe_points:k.interpolation='CONSTANT' if fc.data_path.startswith('hide') else 'LINEAR'
def build(case):
 src=SOURCES[case];bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False,use_scripts=False)
 s=bpy.data.scenes['D computed wear depth - cool palette v017'] if case=='D' else bpy.context.scene
 for w in bpy.context.window_manager.windows:w.scene=s
 s.frame_set(1);before=geometry(s);metadata={'source':str(src),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'case':case}
 if case=='A':
  s.frame_end=96;s.name='S04-A approved upward entry v018';metadata['source_animation_unchanged']=True;metadata['frame_range']=[1,96]
 elif case in 'BC':
  s.name='S04-'+case+' matched 50-percent panel v018';s.frame_end=120
  cam=s.camera;cam.data=cam.data.copy();metadata['source_camera_lens']=cam.data.lens;metadata['source_sensor_fit']=cam.data.sensor_fit
  cam.data.sensor_fit='HORIZONTAL';cam.data.lens*=1.65
  s.render.resolution_x=640;s.render.resolution_y=720;s.render.resolution_percentage=100
  event=json.loads((P/'Communication-Test_v009/Records'/('build-'+case+'.json')).read_text())['event']
  metadata.update(frame_range=[1,120],panel_resolution=[640,720],camera_lens=cam.data.lens,camera_sensor_fit=cam.data.sensor_fit,event=event,signal_animation_unchanged=True,camera_transform_unchanged=True)
  metadata['projection']={k:list(world_to_camera_view(s,cam,Vector(event[v]))) for k,v in [('sensor','emitter_world_m'),('steel_contact','hit_world_m')]}
  assert all(0<metadata['projection'][k][0]<1 and 0<metadata['projection'][k][1]<1 for k in metadata['projection'])
 else:
  s.name='S04-D physical wear then computed data v018';s.frame_start=1;s.frame_end=168
  cam=s.camera;cam.animation_data_clear();cam.data=cam.data.copy();cam.data.animation_data_clear();final=cam.location.copy();target=Vector((-1.66,.145,0));rot=cam.rotation_euler.copy()
  for f in range(1,169):
   amount=1+.07*(1-smooth((f-1)/52));cam.location=target+(final-target)*amount;cam.keyframe_insert('location',frame=f)
  visible=[o for o in s.objects if o.type=='CURVE' and not o.hide_render]
  schedule=[]
  for ob in visible:
   words=ob.name.split();station=int(words[1]);is_blue='blue actual' in ob.name
   start=18 if station<=2 else 28+(station-3)*10+(10 if is_blue else 0);end=start+15
   ob.data=ob.data.copy();m=ob.data.materials[0].copy();m.name='D reveal '+ob.name;ob.data.materials[0]=m;nt=m.node_tree
   output=next(n for n in nt.nodes if n.type=='OUTPUT_MATERIAL');original=output.inputs['Surface'].links[0].from_socket
   tr=nt.nodes.new('ShaderNodeBsdfTransparent');mix=nt.nodes.new('ShaderNodeMixShader');nt.links.new(tr.outputs[0],mix.inputs[1]);nt.links.new(original,mix.inputs[2]);nt.links.new(mix.outputs[0],output.inputs['Surface']);m.surface_render_method='BLENDED'
   values=[smooth((f-start)/(end-start)) for f in range(1,169)];scalar(mix.inputs[0],values)
   for f,a in enumerate(values,1):
    ob.hide_render=a<.0001;ob.hide_viewport=ob.hide_render;ob.keyframe_insert('hide_render',frame=f);ob.keyframe_insert('hide_viewport',frame=f)
   schedule.append({'object':ob.name,'fade_start':start,'fade_end':end})
  steel=next(o for o in s.objects if o.name.startswith('Actual registered worn steel'));m=steel.data.materials[0].copy();m.name='D fixed computed depth - exposure reveal';steel.data.materials[0]=m;nt=m.node_tree
  output=next(n for n in nt.nodes if n.type=='OUTPUT_MATERIAL');heatmix=output.inputs['Surface'].links[0].from_node;original=heatmix.inputs[0].links[0].from_socket
  gain=nt.nodes.new('ShaderNodeValue');gain.name='Recorded depth display reveal';gain.label='Exposes fixed computed loss values only'
  mul=nt.nodes.new('ShaderNodeMath');mul.operation='MULTIPLY';nt.links.new(original,mul.inputs[0]);nt.links.new(gain.outputs[0],mul.inputs[1]);nt.links.new(mul.outputs[0],heatmix.inputs[0]);scalar(gain.outputs[0],[smooth((f-78)/54) for f in range(1,169)])
  linear_actions();metadata.update(frame_range=[1,168],camera_start_factor=1.07,camera_settled_frame=53,approved_final_camera=list(final),line_schedule=schedule,depth_map_reveal=[78,132],depth_attribute_unchanged=True,geometry_static=True)
 s.render.fps=24;s['scope']='Owner released full18s cinematic previs: A then synchronized50/50 B+C then D. No final finishing or engineering approval.'
 assert before==geometry(s);metadata['geometry_unchanged']=True
 out=B/'Scenes'/('S04_'+case+'_v018.blend')
 for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(out.parent))
 s.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(out),relative_remap=False);dump('build-'+case+'.json',metadata);return s
def render(case,benchmark):
 file=B/'Scenes'/('S04_'+case+'_v018.blend');bpy.ops.wm.open_mainfile(filepath=str(file),load_ui=False,use_scripts=False)
 s=bpy.data.scenes[{'A':'S04-A approved upward entry v018','B':'S04-B matched 50-percent panel v018','C':'S04-C matched 50-percent panel v018','D':'S04-D physical wear then computed data v018'}[case]]
 for w in bpy.context.window_manager.windows:w.scene=s
 rows=[];frames=([1,35,78] if case in 'BC' else [1,72,132]) if benchmark else range(1,121 if case in 'BC' else 169)
 for f in frames:
  s.frame_set(f);s.render.filepath=str(B/('Previews' if benchmark else 'Work/'+case)/(('Bench_'+case+'_') if benchmark else (case+'_')))+f'{f:04d}.png'
  t=time.perf_counter();bpy.ops.render.render(scene=s.name,write_still=True);elapsed=time.perf_counter()-t;rows.append({'frame':f,'seconds':elapsed});dump(('benchmark-' if benchmark else 'timings-')+case+'.json',rows);print('FRAME',case,f,round(elapsed,4),flush=True)
  if elapsed>=5:raise RuntimeError('Frame cap exceeded; stop and reduce cost')
mode,case=sys.argv[sys.argv.index('--')+1:][:2]
if mode=='build':build(case)
elif mode=='bench':build(case);render(case,True)
else:
 checks=json.loads((B/'Records'/('benchmark-'+case+'.json')).read_text());assert len(checks)==3 and max(r['seconds'] for r in checks)<5;render(case,False)
