import bpy,math,json,time,hashlib,sys,bmesh
from pathlib import Path
from mathutils import Vector,Matrix
B=Path(__file__).resolve().parents[1];ROOT=B.parents[4];P=ROOT/'05-Previs/Section-04_Cement-Casing-Integrity'
SRC=P/'Cinematic-Previs_v022/Scenes/S04_complete_v022.blend';DREF=P/'CD-Arc-Test_v032/Scenes/S04_CD_arc-test_v032.blend';OUT=B/'Scenes/S04_continuous_ABCD_v033.blend'
CACHE=Path(json.loads((B/'Records/storage.json').read_text())['cache_work_root']) if (B/'Records/storage.json').exists() else B/'Work'
OFFSET=1.55;ARC0=261;ARC1=336;SCAN0=337;SCAN1=419
def sm(t):
 t=max(0,min(1,t));return t*t*t*(t*(6*t-15)+10)
def dump(n,v):(B/'Records'/n).write_text(json.dumps(v,indent=2),encoding='utf-8')
def digest(m):return hashlib.sha256(repr(([tuple(v.co) for v in m.vertices],[tuple(p.vertices) for p in m.polygons])).encode()).hexdigest()
def fcurves(a):
 for l in a.layers:
  for st in l.strips:
   for bag in st.channelbags:yield from bag.fcurves
def qlook(pos,target,up):
 f=(target-pos).normalized();u=(up-f*up.dot(f)).normalized();r=f.cross(u).normalized();return Matrix((r,u,-f)).transposed().to_quaternion()
def build():
 # Read accepted D view and lights, then work only in a source-scene successor.
 bpy.ops.wm.open_mainfile(filepath=str(DREF),load_ui=False,use_scripts=False);s=bpy.context.scene;s.frame_set(48);bpy.context.view_layer.update();dcam=s.camera.matrix_world.copy();dcam.translation.x-=OFFSET-.65;dlens=s.camera.data.lens;dshift=s.camera.data.shift_x
 dbg=next(n for n in s.world.node_tree.nodes if n.type=='BACKGROUND');dworld=(tuple(dbg.inputs['Color'].default_value),dbg.inputs['Strength'].default_value)
 stage=[]
 for o in s.objects:
  if o.type=='LIGHT' and o.name.startswith('Stage - '):
   mx=o.matrix_world.copy();mx.translation.x-=OFFSET-.65
   stage.append({'name':o.name,'type':o.data.type,'color':tuple(o.data.color),'energy':o.data.energy,'matrix':mx,'size':getattr(o.data,'size',1),'size_y':getattr(o.data,'size_y',1),'shape':getattr(o.data,'shape','DISK')})
 bpy.ops.wm.open_mainfile(filepath=str(SRC),load_ui=False,use_scripts=False);s=bpy.context.scene;s.name='S04 continuous A B C D - high crossing v033';cam=s.camera;world=bpy.data.objects['WORLD_CONTROL'];steel=bpy.data.objects['STEEL - capped true source section'];before={o.name:digest(o.data) for o in s.objects if o.type=='MESH'};depth=[d.value for d in steel.data.attributes['ComputedWearDepth_m'].data]
 abc=[]
 for f in range(1,262):
  s.frame_set(f);bpy.context.view_layer.update();abc.append({'matrix':cam.matrix_world.copy(),'lens':cam.data.lens,'shift':cam.data.shift_x,'travel':world['travel_m'],'rotation':world['rotation_rad'],'lights':{o.name:o.data.energy for o in s.objects if o.type=='LIGHT'}})
 # Relocate the wear intact within one fixed tube. The ends and all radii stay put.
 # The zero-wear cylindrical spans can be reparameterized axially without changing their surface.
 lo=-2.3375;hi=-.6875;xmin=-5.5;xmax=0;wear_vertices=0;max_radial_error=0
 for v in steel.data.vertices:
  x=v.co.x;r=math.hypot(v.co.y,v.co.z)
  if lo<=x<=hi:v.co.x=x-OFFSET;wear_vertices+=1
  elif x<lo:v.co.x=xmin+(x-xmin)*(lo-OFFSET-xmin)/(lo-xmin)
  else:v.co.x=hi-OFFSET+(x-hi)*(xmax-hi+OFFSET)/(xmax-hi)
  max_radial_error=max(max_radial_error,abs(math.hypot(v.co.y,v.co.z)-r))
 steel.data.update();steel.animation_data_clear();nt=steel.data.materials[0].node_tree;nt.animation_data_clear();expose=nt.nodes['Expose fixed recorded depth'];front=nt.nodes['ECCO axial acquisition front'];nt.nodes['Math.005'].inputs[1].default_value=-1.499-OFFSET
 s.frame_set(400);bpy.context.view_layer.update()
 profiles=[o for o in s.objects if o.type=='CURVE' and o.name.startswith('Station ')]
 for o in profiles:
  o.animation_data_clear();o.data.animation_data_clear();o.location.x-=OFFSET
  for m in o.data.materials:
   color=tuple(m.diffuse_color);m.animation_data_clear();m.diffuse_color=color
   if m.node_tree:m.node_tree.animation_data_clear()
 # Use approved CAD feature-edge display on local copies; source surfaces remain for A/B/C.
 display_materials={};body_sockets=[];wireobjects=[];memo={};source_housing=bpy.data.objects.get('ECCO unchanged source housing - D technical transparency')
 def local_material(m):
  if m in display_materials:return display_materials[m]
  cp=m.copy();cp.name=m.name+' v033 presentation';cp.animation_data_clear()
  if cp.use_nodes:
   n=cp.node_tree;n.animation_data_clear()
   old=n.nodes.get('Housing opacity - sensor remains solid')
   if old:old.outputs[0].default_value=1
   out=next(x for x in n.nodes if x.type=='OUTPUT_MATERIAL');src=out.inputs['Surface'].links[0].from_socket;tr=n.nodes.new('ShaderNodeBsdfTransparent');mix=n.nodes.new('ShaderNodeMixShader');mix.name='v033 source surface opacity';mix.inputs[0].default_value=1;n.links.new(tr.outputs[0],mix.inputs[1]);n.links.new(src,mix.inputs[2]);n.links.new(mix.outputs[0],out.inputs['Surface']);body_sockets.append(mix.inputs[0]);cp.surface_render_method='BLENDED';cp.use_transparency_overlap=False
  display_materials[m]=cp;return cp
 def clone(col):
  if col in memo:return memo[col]
  new=bpy.data.collections.new(col.name+' v033 local display');memo[col]=new
  for ob in col.objects:
   if ob.type=='MESH':
    cp=ob.copy();cp.data=ob.data.copy();new.objects.link(cp)
    for i,m in enumerate(cp.data.materials):
     if m:cp.data.materials[i]=local_material(m)
    bm=bmesh.new();bm.from_mesh(cp.data);bm.normal_update();edges=[e for e in bm.edges if e.is_boundary or e.is_manifold and e.calc_face_angle(0)>math.radians(40)]
    if edges:
     cu=bpy.data.curves.new(cp.name+' design edges v033','CURVE');cu.dimensions='3D';sc=max(1e-6,cp.matrix_world.to_scale().length/math.sqrt(3));cu.bevel_depth=.0001/sc;cu.bevel_resolution=0;cu.resolution_u=1
     for e in edges:
      sp=cu.splines.new('POLY');sp.points.add(1)
      for p,v in zip(sp.points,e.verts):p.co=(*v.co,1)
     wo=bpy.data.objects.new(cu.name,cu);new.objects.link(wo);wo.parent=cp;wireobjects.append(wo)
    bm.free()
   elif ob.instance_collection:
    cp=ob.copy();cp.instance_collection=clone(ob.instance_collection);new.objects.link(cp)
   else:new.objects.link(ob)
  for ch in col.children:new.children.link(clone(ch))
  return new
 inst=bpy.data.objects['WORLD_HARDWARE_INSTANCE'];inst.instance_collection=clone(inst.instance_collection)
 wm=bpy.data.materials.new('v033 accepted CAD edges');wm.use_nodes=True;wm.surface_render_method='BLENDED';n=wm.node_tree;n.nodes.clear();out=n.nodes.new('ShaderNodeOutputMaterial');tr=n.nodes.new('ShaderNodeBsdfTransparent');em=n.nodes.new('ShaderNodeEmission');em.inputs[0].default_value=(.1,.32,.4,1);em.inputs[1].default_value=.6;mix=n.nodes.new('ShaderNodeMixShader');n.links.new(tr.outputs[0],mix.inputs[1]);n.links.new(em.outputs[0],mix.inputs[2]);n.links.new(mix.outputs[0],out.inputs['Surface']);wirealpha=mix.inputs[0]
 for o in wireobjects:o.data.materials.append(wm)
 # Fixed section; global context fade changes presentation during travel only.
 s.frame_set(261);context=[]
 for o in s.objects:
  if o.type=='MESH' and not o.hide_render and o!=steel and not o.name.startswith(('STEEL-','STEEL THICKNESS','S02 sourced','Casing response','s04-v005')):context.append(o)
 cm=bpy.data.materials.new('v033 fast environmental presentation');cm.use_nodes=True;cm.surface_render_method='BLENDED';cm.use_transparency_overlap=False;n=cm.node_tree;n.nodes.clear();out=n.nodes.new('ShaderNodeOutputMaterial');info=n.nodes.new('ShaderNodeObjectInfo');bs=n.nodes.new('ShaderNodeBsdfDiffuse');bs.inputs['Roughness'].default_value=.7;n.links.new(info.outputs['Color'],bs.inputs[0]);tr=n.nodes.new('ShaderNodeBsdfTransparent');mix=n.nodes.new('ShaderNodeMixShader');n.links.new(tr.outputs[0],mix.inputs[1]);n.links.new(bs.outputs[0],mix.inputs[2]);n.links.new(mix.outputs[0],out.inputs['Surface']);envopacity=n.nodes.new('ShaderNodeValue').outputs[0];mul=n.nodes.new('ShaderNodeMath');mul.operation='MULTIPLY';n.links.new(envopacity,mul.inputs[0]);n.links.new(info.outputs['Alpha'],mul.inputs[1]);n.links.new(mul.outputs[0],mix.inputs[0])
 for o in context:
  o.animation_data_clear()
  if o.data.materials and o.data.materials[0]:o.color=o.data.materials[0].diffuse_color
  if 'Internal fluid visibility' in o.name:o.color=(*o.color[:3],.045)
  for i in range(len(o.data.materials)):o.data.materials[i]=cm
 # Clear earlier D-only pulse display; B/C signal actions remain exactly as supplied.
 effects=[o for o in s.objects if o.name.startswith(('STEEL-ATTACHED resonance band','STEEL THICKNESS response','STEEL-BOUND acquisition segment','S02 sourced','Casing response tail'))]
 effect_states={o.name:(o.hide_render,o.hide_viewport) for o in effects}
 for o in s.objects:
  if o.name.startswith('D sensor '):o.animation_data_clear();o.hide_render=True;o.hide_viewport=True
 for o in effects:
  o.keyframe_insert('hide_render',frame=261);o.keyframe_insert('hide_viewport',frame=261);o.hide_render=True;o.hide_viewport=True;o.keyframe_insert('hide_render',frame=262);o.keyframe_insert('hide_viewport',frame=262)
 s.world=s.world.copy();s.world.animation_data_clear();s.world.node_tree.animation_data_clear();bg=next(n for n in s.world.node_tree.nodes if n.type=='BACKGROUND');cworld=(tuple(bg.inputs['Color'].default_value),bg.inputs['Strength'].default_value)
 lights=[]
 for o in s.objects:
  if o.type=='LIGHT':
   o.data.animation_data_clear();o.data.use_shadow=False;lights.append(o)
 stage_lights=[]
 for r in stage:
  d=bpy.data.lights.new(r['name']+' v033',r['type']);d.color=r['color'];d.energy=0;d.use_shadow=False
  if r['type']=='AREA':d.shape=r['shape'];d.size=r['size'];d.size_y=r['size_y']
  ob=bpy.data.objects.new(d.name,d);s.collection.objects.link(ob);ob.matrix_world=r['matrix'];stage_lights.append((ob,r['energy']))
 # Camera and hardware are baked into one uncut 432-frame journey.
 cam.animation_data_clear();cam.data.animation_data_clear();cam.rotation_mode='QUATERNION';world.animation_data_clear();c=abc[-1];cpos=c['matrix'].translation;cq=c['matrix'].to_quaternion();ctar=cpos+cq@Vector((0,0,-.55));dpos=dcam.translation;dq=dcam.to_quaternion();dtar=dpos+dq@Vector((0,0,-.75));p1=Vector((-1.85,-.01,3.20));p2=Vector((-3.80,-.12,2.80));prev=None;rows=[]
 for f in range(1,433):
  s.frame_set(f);u=sm((f-ARC0)/(ARC1-ARC0));scan=sm((f-SCAN0)/(SCAN1-SCAN0));drift=sm((f-ARC1)/(432-ARC1))
  if f<=261:
   a=abc[f-1];pos=a['matrix'].translation;q=a['matrix'].to_quaternion();lens=a['lens'];shift=a['shift'];travel=a['travel'];rot=a['rotation']
  else:
   pos=(1-u)**3*cpos+3*(1-u)**2*u*p1+3*(1-u)*u*u*p2+u**3*dpos+Vector((-.07,-.018,.012))*drift;tar=ctar.lerp(dtar,u)+Vector((-.025,0,0))*drift;q=qlook(pos,tar,cq.slerp(dq,u)@Vector((0,1,0)));lens=c['lens']+(dlens-c['lens'])*u;shift=dshift*u;travel=c['travel']-OFFSET*u-.45*scan;rot=c['rotation']+(-math.radians(39)-c['rotation'])*u
  if prev and prev.dot(q)<0:q.negate()
  prev=q.copy();cam.location=pos;cam.rotation_quaternion=q;cam.data.lens=lens;cam.data.shift_x=shift;cam.data.shift_y=0
  cam.keyframe_insert('location',frame=f);cam.keyframe_insert('rotation_quaternion',frame=f);cam.data.keyframe_insert('lens',frame=f);cam.data.keyframe_insert('shift_x',frame=f)
  world['travel_m']=travel;world['rotation_rad']=rot;world.keyframe_insert('["travel_m"]',frame=f);world.keyframe_insert('["rotation_rad"]',frame=f)
  bg.inputs['Color'].default_value=tuple(a+(b-a)*u for a,b in zip(cworld[0],dworld[0]));bg.inputs['Strength'].default_value=cworld[1]+(dworld[1]-cworld[1])*u;bg.inputs['Color'].keyframe_insert('default_value',frame=f);bg.inputs['Strength'].keyframe_insert('default_value',frame=f)
  for sock in body_sockets:sock.default_value=1-u;sock.keyframe_insert('default_value',frame=f)
  wirealpha.default_value=u;wirealpha.keyframe_insert('default_value',frame=f);envopacity.default_value=1-u;envopacity.keyframe_insert('default_value',frame=f)
  for o in context:o.hide_render=u>=1;o.hide_viewport=o.hide_render;o.keyframe_insert('hide_render',frame=f);o.keyframe_insert('hide_viewport',frame=f)
  for o in lights:o.data.energy=abc[min(f,261)-1]['lights'].get(o.name,0)*(1-u);o.data.keyframe_insert('energy',frame=f)
  for o,energy in stage_lights:o.data.energy=energy*u;o.data.keyframe_insert('energy',frame=f)
  sx=travel+.7300000190734863;front.outputs[0].default_value=sx;front.outputs[0].keyframe_insert('default_value',frame=f);expose.outputs[0].default_value=.35*sm((f-SCAN0)/10);expose.outputs[0].keyframe_insert('default_value',frame=f)
  for o in profiles:
   pts=[p.co.x for sp in o.data.splines for p in sp.points];px=sum(pts)/len(pts)+o.location.x;o.hide_render=f<SCAN0 or px<sx or px<-2-OFFSET;o.hide_viewport=o.hide_render;o.keyframe_insert('hide_render',frame=f);o.keyframe_insert('hide_viewport',frame=f)
  rows.append({'frame':f,'camera_m':list(pos),'lens_mm':lens,'shift_x':shift,'sensor_x_m':sx,'arc_progress':u,'wear_display':expose.outputs[0].default_value})
 ids=[cam,cam.data,world,nt,wm.node_tree,cm.node_tree,s.world.node_tree]+[o for o in context+profiles]+[o.data for o in lights]+[o.data for o,e in stage_lights]+[m.node_tree for m in display_materials.values() if m.use_nodes]
 for item in ids:
  if item.animation_data and item.animation_data.action:
   for fc in fcurves(item.animation_data.action):
    for k in fc.keyframe_points:k.interpolation='CONSTANT' if fc.data_path.startswith('hide') else 'LINEAR'
 assert depth==[d.value for d in steel.data.attributes['ComputedWearDepth_m'].data]
 assert all(digest(bpy.data.objects[n].data)==h for n,h in before.items() if n!=steel.name)
 assert abs(min(v.co.x for v in steel.data.vertices)+5.5)<1e-6 and abs(max(v.co.x for v in steel.data.vertices))<1e-6
 s.frame_start=1;s.frame_end=432;s.render.fps=24;s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.eevee.taa_render_samples=8;s.render.image_settings.file_format='PNG';s.render.image_settings.compression=10;s['scope']='Owner released full18s continuous ABCD integration: approved ABC, higher overhead crossing, wear further ahead, accepted close side-offset D with drift. Illustrative data, not field measurement.'
 for marker in list(s.timeline_markers):s.timeline_markers.remove(marker)
 for f,n in [(1,'A - casing entry'),(63,'B - supported backing'),(175,'C - reduced support'),(262,'High crossing and style transition'),(337,'D - sensor passes wear')]:s.timeline_markers.new(n,frame=f)
 for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(OUT.parent))
 s.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(OUT),relative_remap=False)
 dump('camera-score.json',rows);dump('build.json',{'native':str(OUT),'source':str(SRC),'source_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),'D_reference':str(DREF),'D_reference_sha256':hashlib.sha256(DREF.read_bytes()).hexdigest(),'ABC_camera_tool_samples_preserved_frames':[1,261],'wear_offset_from_original_m':OFFSET,'additional_offset_from_v032_m':OFFSET-.65,'steel_fixed_endpoints_m':[-5.5,0],'wear_region_translation_support_m':[lo,hi],'steel_radial_error_m':max_radial_error,'computed_depth_values_unchanged':True,'max_authored_depth_mm':1000*max(depth),'all_other_meshes_unchanged':True,'arc_frames':[262,336],'D_acquisition_frames':[337,419],'camera_peak_z_m':max(x['camera_m'][2] for x in rows),'context_materials':'Simple diffuse source colors for inexpensive previs; source ABC signal actions retained.','one_camera':True,'duration_seconds':18,'frames':432,'human_approval':'pending'})
def render(mode):
 bpy.ops.wm.open_mainfile(filepath=str(OUT),load_ui=False,use_scripts=False);s=bpy.context.scene;rows=[];frames=[1,40,85,94,104,190,206,216,261,280,300,318,336,365,400,432] if mode=='bench' else range(1,433)
 if mode=='resume':
  rows=json.loads((B/'Records/timings-render.json').read_text());frames=range(rows[-1]['frame']+1,433)
 if mode!='bench':assert max(r['seconds'] for r in json.loads((B/'Records/timings-bench.json').read_text()))<5
 for f in frames:
  s.frame_set(f);s.render.filepath=str((B/'Previews' if mode=='bench' else CACHE/'Frames')/f'S04_{f:04d}.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t;rows.append({'frame':f,'seconds':dt});dump('timings-'+('render' if mode=='resume' else mode)+'.json',rows);print('FRAME',f,dt,flush=True)
  if dt>=5:raise RuntimeError('Frame budget exceeded; stop before proceeding')
if __name__=='__main__':
 mode=sys.argv[sys.argv.index('--')+1]
 if mode=='build':build()
 else:render(mode)
