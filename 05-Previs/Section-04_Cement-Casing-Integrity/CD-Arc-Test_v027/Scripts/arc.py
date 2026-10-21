import bpy,json,math,time,hashlib,sys
from pathlib import Path
from mathutils import Vector,Matrix
B=Path(__file__).resolve().parents[1];P=B.parent;SRC=P/'Cinematic-Previs_v022/Scenes/S04_complete_v022.blend';STAGE=P/'D-Scientific-Stage_v026/Scenes/S04_D_B_v026.blend';OUT=B/'Scenes/S04_CD_arc-test_v027.blend'
def sm(t):
 t=max(0,min(1,t));return t*t*t*(t*(6*t-15)+10)
def dump(n,v):(B/'Records'/n).write_text(json.dumps(v,indent=2))
def geo(s):return {o.name:hashlib.sha256(repr(([tuple(v.co) for v in o.data.vertices],[tuple(p.vertices) for p in o.data.polygons])).encode()).hexdigest() for o in s.objects if o.type=='MESH'}
def fc(a):
 for l in a.layers:
  for st in l.strips:
   for bag in st.channelbags:yield from bag.fcurves
def build():
 bpy.ops.wm.open_mainfile(filepath=str(SRC),load_ui=False,use_scripts=False);s=bpy.context.scene;s.frame_set(250);bpy.context.view_layer.update();cm=s.camera.matrix_world.copy();clens=s.camera.data.lens
 contexts=[o.name for o in s.objects if o.type=='MESH' and not o.hide_render and o.name!='STEEL - capped true source section' and not o.name.startswith(('STEEL-','STEEL THICKNESS','S02 sourced','Casing response','s04-v005'))]
 lightstate={o.name:o.data.energy for o in s.objects if o.type=='LIGHT' and not o.hide_render and o.data.energy>0}
 bpy.ops.wm.open_mainfile(filepath=str(STAGE),load_ui=False,use_scripts=False);s=bpy.context.scene;s.name='S04 C to D arc - bounded v027';before=geo(s);cam=s.camera;dm=cam.matrix_world.copy();dlens=cam.data.lens;cam.animation_data_clear();cam.data.animation_data_clear();cam.rotation_mode='QUATERNION';cam.data.shift_x=0;cam.data.shift_y=0
 world=bpy.data.objects['WORLD_CONTROL'];world.animation_data_clear();world['show_hardware']=1
 steel=bpy.data.objects['STEEL - capped true source section'];depth=[v.value for v in steel.data.attributes['ComputedWearDepth_m'].data];nt=steel.data.materials[0].node_tree;nt.animation_data_clear();expose=nt.nodes['Expose fixed recorded depth'];front=nt.nodes['ECCO axial acquisition front']
 profiles=[o for o in s.objects if o.type=='CURVE' and o.name.startswith('Station ')]
 for o in profiles:
  o.animation_data_clear();o.data.animation_data_clear()
  for m in o.data.materials:
   color=tuple(m.diffuse_color);m.animation_data_clear();m.diffuse_color=color
   if m.node_tree and m.node_tree.animation_data and m.node_tree.animation_data.action:m.node_tree.animation_data.action=None
 # Fade the full environmental presentation together, never animate a cut.
 env=[];opacity=[];cache={}
 simple=bpy.data.materials.new('Fast context fade - material colors retained');simple.use_nodes=True;simple.surface_render_method='BLENDED';simple.use_transparency_overlap=False;n=simple.node_tree;n.nodes.clear();out=n.nodes.new('ShaderNodeOutputMaterial');info=n.nodes.new('ShaderNodeObjectInfo');bs=n.nodes.new('ShaderNodeBsdfDiffuse');bs.inputs['Roughness'].default_value=.7;n.links.new(info.outputs['Color'],bs.inputs['Color']);tr=n.nodes.new('ShaderNodeBsdfTransparent');mix=n.nodes.new('ShaderNodeMixShader');n.links.new(tr.outputs[0],mix.inputs[1]);n.links.new(bs.outputs[0],mix.inputs[2]);n.links.new(mix.outputs[0],out.inputs['Surface']);opacity.append(mix.inputs[0]);cache['simple']=simple
 for name in contexts:
  o=bpy.data.objects.get(name)
  if not o:continue
  o.animation_data_clear();o.hide_render=False;o.hide_viewport=False;env.append(o)
  if o.data.materials and o.data.materials[0]:o.color=o.data.materials[0].diffuse_color
  for i in range(len(o.data.materials)):o.data.materials[i]=simple
 toolmat=bpy.data.materials['D Contour wireframe look'];toolnt=toolmat.node_tree;body=next(n for n in toolnt.nodes if n.type=='MATH' and n.operation=='ADD').inputs[1]
 wire=bpy.data.materials['Desaturated cyan CAD design-edge display'].node_tree;wirealpha=next(n for n in wire.nodes if n.type=='MIX_SHADER').inputs[0]
 # Two existing light rigs crossfade with the same presentation change.
 rigs=[]
 for o in s.objects:
  if o.type!='LIGHT':continue
  o.data.animation_data_clear();o.hide_render=False;o.data.use_shadow=False
  if o.name.startswith('Stage - '):rigs.append((o.data,0,o.data.energy))
  else:rigs.append((o.data,lightstate.get(o.name,0),0))
 cpos=cm.translation;dpos=dm.translation;cq=cm.to_quaternion();dq=dm.to_quaternion();ctarget=cpos+cq@Vector((0,0,-.55));dtarget=dpos+dq@Vector((0,0,-.75));p1=Vector((-1.58,-.34,.72));p2=Vector((-1.28,-.23,.28));score=[];prev=None;N=Vector((0,-math.sin(math.radians(39)),math.cos(math.radians(39))))
 for f in range(1,121):
  s.frame_set(f);u=sm((f-17)/31);scan=sm((f-49)/59);world['travel_m']=-2.23-.45*scan;world['rotation_rad']=-math.radians(39)*u
  world.keyframe_insert(data_path='["travel_m"]',frame=f);world.keyframe_insert(data_path='["rotation_rad"]',frame=f)
  pos=(1-u)**3*cpos+3*(1-u)**2*u*p1+3*(1-u)*u*u*p2+u**3*dpos;target=ctarget.lerp(dtarget,u);forward=(target-pos).normalized();hint=cq.slerp(dq,u)@Vector((0,1,0));up=(hint-forward*hint.dot(forward)).normalized();right=forward.cross(up).normalized();q=Matrix((right,up,-forward)).transposed().to_quaternion()
  if prev and prev.dot(q)<0:q.negate()
  prev=q.copy();cam.location=pos;cam.rotation_quaternion=q;cam.data.lens=clens+(dlens-clens)*u;cam.keyframe_insert('location',frame=f);cam.keyframe_insert('rotation_quaternion',frame=f);cam.data.keyframe_insert('lens',frame=f)
  for sock in opacity:sock.default_value=1-u;sock.keyframe_insert('default_value',frame=f)
  for o in env:o.hide_render=u>=1;o.hide_viewport=o.hide_render;o.keyframe_insert('hide_render',frame=f);o.keyframe_insert('hide_viewport',frame=f)
  body.default_value=1-u;body.keyframe_insert('default_value',frame=f);wirealpha.default_value=u;wirealpha.keyframe_insert('default_value',frame=f)
  for light,a,b in rigs:light.energy=a+(b-a)*u;light.keyframe_insert('energy',frame=f)
  sx=world['travel_m']+.7300000190734863;front.outputs[0].default_value=sx;front.outputs[0].keyframe_insert('default_value',frame=f);expose.outputs[0].default_value=.35*sm((f-49)/8);expose.outputs[0].keyframe_insert('default_value',frame=f)
  for o in profiles:
   pts=[p.co.x for sp in o.data.splines for p in sp.points];px=sum(pts)/len(pts);o.hide_render=f<49 or px<sx or px<-2;o.hide_viewport=o.hide_render;o.keyframe_insert('hide_render',frame=f);o.keyframe_insert('hide_viewport',frame=f)
  score.append({'frame':f,'arc_and_style_progress':u,'camera_m':list(pos),'lens_mm':cam.data.lens,'sensor_x_m':sx,'opening_plane_clearance_m':pos.dot(N),'tool_body_opacity':1-u,'wire_opacity':u,'context_opacity':1-u})
 assert before==geo(s) and depth==[v.value for v in steel.data.attributes['ComputedWearDepth_m'].data]
 assert min(r['opening_plane_clearance_m'] for r in score)>0
 # Keep all exact baked per-frame poses smooth; visibility remains discrete only at zero opacity.
 ids=[cam,cam.data,world,nt,toolnt,wire]+[o for o in env+profiles]+[l for l,a,b in rigs]+[m.node_tree for m in cache.values()]
 for item in ids:
  if item.animation_data and item.animation_data.action:
   for curve in fc(item.animation_data.action):
    for k in curve.keyframe_points:k.interpolation='CONSTANT' if curve.data_path.startswith('hide') else 'LINEAR'
 s.frame_start=1;s.frame_end=120;s.render.fps=24;s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.eevee.taa_render_samples=8;s['scope']='Only a5second C-to-D arc/styling proof; no full-section integration. Full surrounding context fades while camera arcs; steel/physical wear remain fixed. Sensor-tied acquisition follows arrival.'
 s.frame_set(80)
 for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(OUT.parent))
 bpy.ops.wm.save_as_mainfile(filepath=str(OUT),relative_remap=False)
 dump('camera-score.json',score);dump('build.json',{'source':str(SRC),'source_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),'stage':str(STAGE),'stage_sha256':hashlib.sha256(STAGE.read_bytes()).hexdigest(),'physical_meshes_unchanged':True,'computed_depth_unchanged':True,'max_authored_wear_mm':1000*max(depth),'context_objects':contexts,'arc_and_style_frames':[17,48],'D_scan_frames':[49,108],'duration_seconds':5,'single_camera':True,'full_section_integration':False})
def render(mode):
 bpy.ops.wm.open_mainfile(filepath=str(OUT),use_scripts=False,load_ui=False);s=bpy.context.scene;rows=[];frames=[1,17,25,33,41,48,65,90,120] if mode=='bench' else range(1,121)
 if mode=='resume':
  prior=json.loads((B/'Records/timings-render.json').read_text());rows=[r for r in prior if r['frame']<=48];frames=range(max(r['frame'] for r in rows)+1,121)
 if mode!='bench':assert max(r['seconds'] for r in json.loads((B/'Records/timings-bench.json').read_text()))<5
 for f in frames:
  s.frame_set(f);s.render.filepath=str(B/('Previews' if mode=='bench' else 'Work/Frames')/f'S04_CD_{f:04d}.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t;rows.append({'frame':f,'seconds':dt});dump('timings-'+('render' if mode=='resume' else mode)+'.json',rows);print('FRAME',f,dt,flush=True)
  if dt>=5:raise RuntimeError('Frame cap exceeded')
if __name__=='__main__':
 mode=sys.argv[sys.argv.index('--')+1]
 if mode=='build':build()
 else:render(mode)
