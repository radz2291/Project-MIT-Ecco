import bpy,math,json,time,hashlib,sys
from pathlib import Path
from mathutils import Vector,Matrix,Quaternion
from bpy_extras.object_utils import world_to_camera_view
B=Path(__file__).resolve().parents[1];PREV=Path(r'C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/Shots/S04/S04-A/Previs_v033');SRC=PREV/'Scenes/S04_continuous_ABCD_v033.blend';OUT=B/'Scenes/S04_continuous_ABCD_v034.blend';CACHE=Path(r'D:/MIT-ECCO-Render-Recovery/261013-MIT-Ecco/04-Production/Shots/S04/S04-A/Previs_v034/Work')
def sm(t):
 t=max(0,min(1,t));return t*t*t*(t*(6*t-15)+10)
def dump(n,x):(B/'Records'/n).write_text(json.dumps(x,indent=2),encoding='utf-8')
def digest(o):return hashlib.sha256(repr(([tuple(v.co) for v in o.data.vertices],[tuple(p.vertices) for p in o.data.polygons])).encode()).hexdigest()
def curves(a):
 for l in a.layers:
  for st in l.strips:
   for bag in st.channelbags:yield from bag.fcurves
def look(pos,target):return (target-pos).to_track_quat('-Z','Y')
def build():
 bpy.ops.wm.open_mainfile(filepath=str(SRC),load_ui=False,use_scripts=False);s=bpy.context.scene;s.name='S04 continuous ABCD - clear product and smooth steel v034';cam=s.camera;world=bpy.data.objects['WORLD_CONTROL'];steel=bpy.data.objects['STEEL - capped true source section'];geo={o.name:digest(o) for o in s.objects if o.type=='MESH'};depth=[d.value for d in steel.data.attributes['ComputedWearDepth_m'].data]
 key=bpy.data.objects['Wide sectional softbox'];ld=key.data
 old=[]
 for f in range(1,64):
  s.frame_set(f);bpy.context.view_layer.update();old.append({'matrix':cam.matrix_world.copy(),'lens':cam.data.lens,'shift':cam.data.shift_x,'travel':world['travel_m'],'key_matrix':key.matrix_world.copy(),'key_energy':key.data.energy})
 # Remove only presentation curves generated from a non-rendering Boolean helper.
 hidden=[]
 for col in bpy.data.collections:
  for o in col.objects:
   if o.type=='CURVE' and 'design edges' in o.name and ('CUTTER' in o.name or 'PREVIEW_ONLY' in o.name):o.hide_render=True;o.hide_viewport=True;hidden.append(o.name)
 # No physical pit exists at sampled points. Soften the specular/roughness response in D.
 nt=steel.data.materials[0].node_tree;bs=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED');rough=bs.inputs['Roughness'];oldrough=rough.links[0].from_socket if rough.links else None;mul=nt.nodes.new('ShaderNodeMath');mul.name='v034 retain source roughness';mul.operation='MULTIPLY';add=nt.nodes.new('ShaderNodeMath');add.name='v034 broad satin finish';add.operation='ADD'
 if oldrough:nt.links.new(oldrough,mul.inputs[0])
 else:mul.inputs[0].default_value=rough.default_value
 nt.links.new(mul.outputs[0],add.inputs[0]);nt.links.new(add.outputs[0],rough);metal=bs.inputs['Metallic'].default_value;spec=bs.inputs['Specular IOR Level'].default_value
 fill=next(o for o in s.objects if o.type=='LIGHT' and o.name.startswith('Stage - Low soft inspection fill'));fd=fill.data;fill.location=(-3.2,-.05,.45);fill.rotation_euler=look(fill.location,Vector((-3.2,.03,-.159))).to_euler()
 body_objects=[o for o in bpy.data.objects if o.type=='MESH' and o.library is None and not o.hide_render and any(m and 'v033 presentation' in m.name for m in o.data.materials)]
 projected=[];previous=None
 for f in range(1,433):
  s.frame_set(f);u=sm((f-261)/75);cam.data.shift_y=.14*u;cam.data.keyframe_insert('shift_y',frame=f)
  for o in body_objects:o.hide_render=u>=1;o.keyframe_insert('hide_render',frame=f)
  mul.inputs[1].default_value=1-u;add.inputs[1].default_value=.64*u;mul.inputs[1].keyframe_insert('default_value',frame=f);add.inputs[1].keyframe_insert('default_value',frame=f);bs.inputs['Metallic'].default_value=metal+(.30-metal)*u;bs.inputs['Specular IOR Level'].default_value=spec+(.25-spec)*u;bs.inputs['Metallic'].keyframe_insert('default_value',frame=f);bs.inputs['Specular IOR Level'].keyframe_insert('default_value',frame=f);fd.energy=1.5*u;fd.keyframe_insert('energy',frame=f)
  opening=sm((f-12)/51)
  if f<=63:
   a=old[f-1];delta=a['travel']-old[0]['travel'];pos=Vector((1.8,1.9,2.4))+Vector((delta,0,0));target=Vector((1.45,0,0))+Vector((delta,0,0));q=look(pos,target)@Quaternion((0,0,1),math.radians(-6));pos=pos.lerp(a['matrix'].translation,opening);q=q.slerp(a['matrix'].to_quaternion(),opening)
   if previous and previous.dot(q)<0:q.negate()
   previous=q.copy();cam.location=pos;cam.rotation_quaternion=q;cam.data.lens=32+(a['lens']-32)*opening;cam.data.shift_x=a['shift']*opening;cam.keyframe_insert('location',frame=f);cam.keyframe_insert('rotation_quaternion',frame=f);cam.data.keyframe_insert('lens',frame=f);cam.data.keyframe_insert('shift_x',frame=f);key.location=(Vector((1.5,1.0,1.3))+Vector((delta,0,0))).lerp(a['key_matrix'].translation,opening);key.rotation_mode='QUATERNION';key.rotation_quaternion=look(key.location,Vector((1.35+delta,0,0))).slerp(a['key_matrix'].to_quaternion(),opening);ld.energy=18+(a['key_energy']-18)*opening;ld.keyframe_insert('energy',frame=f);key.keyframe_insert('location',frame=f);key.keyframe_insert('rotation_quaternion',frame=f)
  if f>63:
   q=cam.rotation_quaternion.copy()
   if previous and previous.dot(q)<0:q.negate()
   previous=q.copy();cam.rotation_quaternion=q;cam.keyframe_insert('rotation_quaternion',frame=f)
  if f in [1,12,24,40,63]:
   bpy.context.view_layer.update();port=next(i.matrix_world.translation.copy() for i in bpy.context.evaluated_depsgraph_get().object_instances if i.object.name=='ECCO_SENSOR_REF_01');uv=world_to_camera_view(s,cam,port);projected.append({'frame':f,'sensor_screen':[uv.x,uv.y],'camera':list(cam.location)})
 for item in [cam,cam.data,nt,ld,fd,key]+body_objects:
  if item.animation_data and item.animation_data.action:
   for fc in curves(item.animation_data.action):
    for k in fc.keyframe_points:k.interpolation='CONSTANT' if fc.data_path.startswith('hide') else 'LINEAR'
 assert geo=={o.name:digest(o) for o in s.objects if o.type=='MESH'};assert depth==[d.value for d in steel.data.attributes['ComputedWearDepth_m'].data]
 s.eevee.taa_render_samples=4
 s['scope']='Owner revision: clear product establishment and eliminate false pit appearance. Same physical steel/wear and continuous18second journey; revise A camera, D satin response/fill and hide Boolean-helper wire.';s.frame_set(1);s.render.filepath=str(CACHE/'Frames/S04_')
 for d in ['Frames','Assembly']:(CACHE/d).mkdir(parents=True,exist_ok=True)
 bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
 dump('storage.json',{'cache_work_root':str(CACHE),'reuse_work_root':str(Path(json.loads((PREV/'Records/storage.json').read_text())['cache_work_root']))});dump('build.json',{'source':str(SRC),'source_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),'native':str(OUT),'all_physical_meshes_unchanged':True,'computed_depth_values_unchanged':True,'max_authored_depth_mm':1000*max(depth),'hidden_helper_curves':hidden,'opening_projected_sensor':projected,'B_C_and_crossing_camera_preserved_from_frame':63,'D_changes':'Satin metallic/roughness and broad fill; zero geometry edits','marked_region_inspection':'v033 frame432 samples x=.60-.75,y=.18-.35 hit the inner steel at authored depth0mm. Shading/reflection is the likely false-pit cause, not a cement void.','duration_seconds':18,'frames':432,'human_approval':'pending'})
def render(mode):
 import shutil
 bpy.ops.wm.open_mainfile(filepath=str(OUT),load_ui=False,use_scripts=False);s=bpy.context.scene
 if mode=='bench':frames=[432,1,12,24,40,63,85,206,280,300,336,400];rows=[]
 else:
  prior=json.loads((PREV/'Records/timings-render.json').read_text());oldcache=Path(json.loads((PREV/'Records/storage.json').read_text())['cache_work_root']);rows=[]
  for f in range(63,262):
   shutil.copy2(oldcache/'Frames'/f'S04_{f:04d}.png',CACHE/'Frames'/f'S04_{f:04d}.png');r=dict(prior[f-1]);r['inherited_from']='v033 unchanged B/C';rows.append(r)
  frames=[432]+list(range(1,63))+list(range(262,432));assert max(x['seconds'] for x in json.loads((B/'Records/timings-bench.json').read_text()))<5
 for f in frames:
  s.frame_set(f);(CACHE/'Benchmark').mkdir(parents=True,exist_ok=True);s.render.filepath=str((CACHE/'Benchmark' if mode=='bench' else CACHE/'Frames')/f'S04_{f:04d}.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t;rows.append({'frame':f,'seconds':dt});dump('timings-'+mode+'.json',sorted(rows,key=lambda x:x['frame']));print('FRAME',f,dt,flush=True)
  if dt>=5:raise RuntimeError('Frame budget exceeded')
if __name__=='__main__':
 mode=sys.argv[sys.argv.index('--')+1]
 if mode=='build':build()
 else:render(mode)
