import bpy,bmesh,math,json,sys,time,hashlib
from pathlib import Path
from mathutils import Vector,Quaternion,Matrix
from mathutils.bvhtree import BVHTree
from bpy_extras.object_utils import world_to_camera_view
B=Path(__file__).resolve().parents[1];P=B.parent;ROOT=B.parents[2]
SRC=P/'Communication-Test_v009/Scenes/S04_B_formation-acquisition_v009.blend'
D=P/'D-Physical-Wear_v017/Scenes/S04_D_cool-wear-depth_v017.blend'
OUT=B/'Scenes/S04_continuous-camera_v019.blend'
PHI=math.radians(39);N=Vector((0,-math.sin(PHI),math.cos(PHI)));CUT=.00005
def sm(t):
 t=min(1,max(0,t));return t*t*t*(t*(6*t-15)+10)
def dump(n,v):(B/'Records'/n).write_text(json.dumps(v,indent=2))
def fcurves(action):
 for layer in action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    yield from bag.fcurves
def shift_actions(delta):
 for act in bpy.data.actions:
  if act.library:continue
  for fc in fcurves(act):
   for k in fc.keyframe_points:k.co.x+=delta;k.handle_left.x+=delta;k.handle_right.x+=delta
def section(o):
 bm=bmesh.new();bm.from_mesh(o.data)
 bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-7,plane_co=N*CUT,plane_no=N,clear_outer=True,clear_inner=False)
 edges=[e for e in bm.edges if e.is_boundary and all(abs(v.co.dot(N)-CUT)<2e-6 for v in e.verts)]
 caps=bmesh.ops.holes_fill(bm,edges=edges,sides=0)['faces'] if edges else []
 if caps:bmesh.ops.triangulate(bm,faces=caps)
 bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();o.data.update()
def driver(socket,index,mat,prop):
 fc=socket.driver_add('default_value',index) if index is not None else socket.driver_add('default_value');v=fc.driver.variables.new();v.name='c';v.targets[0].id_type='MATERIAL';v.targets[0].id=mat;v.targets[0].data_path=prop;fc.driver.expression='c'
def convert(mat):
 if mat.library:return
 mat.use_nodes=True;nt=mat.node_tree;nt.nodes.clear();ns=nt.nodes;li=nt.links;out=ns.new('ShaderNodeOutputMaterial')
 graphic=any(x in mat.name for x in ['response','Acquisition','front','return','wave','Echo','Signal','S02'])
 sh=ns.new('ShaderNodeEmission' if graphic else 'ShaderNodeBsdfDiffuse');color=sh.inputs['Color']
 for i in range(4):driver(color,i,mat,f'diffuse_color[{i}]')
 if graphic:sh.inputs['Strength'].default_value=.85
 tr=ns.new('ShaderNodeBsdfTransparent');mix=ns.new('ShaderNodeMixShader');driver(mix.inputs[0],None,mat,'diffuse_color[3]');li.new(tr.outputs[0],mix.inputs[1]);li.new(sh.outputs[0],mix.inputs[2]);li.new(mix.outputs[0],out.inputs['Surface']);mat.surface_render_method='BLENDED'
def light(name,pos,target,power,size):
 d=bpy.data.lights.new(name,'AREA');d.energy=power;d.shape='DISK';d.size=size;d.use_shadow=False;o=bpy.data.objects.new(name,d);bpy.context.scene.collection.objects.link(o);o.location=pos;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
def build():
 bpy.ops.wm.open_mainfile(filepath=str(SRC),load_ui=False,use_scripts=False);s=bpy.context.scene;s.name='S04 one continuous physical scene v019';s.frame_set(1)
 shift_actions(120)
 # Restore the complete source circumference BEFORE making one permanent 180-degree section.
 steel=bpy.data.objects['STEEL - capped true source section'];steel.data=bpy.data.objects['CASED_STEEL_WEAR_FULL'].data.copy();section(steel)
 for p in steel.data.polygons:p.material_index=0;p.use_smooth=abs(p.normal.dot(N))<.99
 # Existing cement, stationary channel and steel are fixed at this same section for all432 frames.
 static=[o for o in s.objects if o.type=='MESH' and not o.hide_render and (o.name.startswith('Cement ') or 'organic fluid-filled' in o.name or o==steel)]
 for o in static:o.animation_data_clear()
 rock=bpy.data.objects['FORMATION - closed source-guided continuation to frame edge'];rock.data=rock.data.copy()
 for v in rock.data.vertices:
  x,y,z=v.co;v.co.x=-5.5+(x+1.51999998)/2.4*8.0
  r=math.hypot(y,z)
  if r>.9:v.co.y*=3.5/r;v.co.z*=3.5/r
 rock['scope']='Static illustrative formation continuation to screen edge; existing inner geological cross-section reused, no borehole radial geometry altered.'
 w=bpy.data.objects['WORLD_CONTROL'];w.animation_data_clear()
 for f,val in [(1,1.1),(85,-1.05),(432,-1.05)]:w['travel_m']=val;w.keyframe_insert(data_path='["travel_m"]',frame=f)
 if w.animation_data:
  for fc in fcurves(w.animation_data.action):
   for k in fc.keyframe_points:k.interpolation='BEZIER';k.handle_left_type='AUTO_CLAMPED';k.handle_right_type='AUTO_CLAMPED'
 # Import only approved display curves and palette; use the continuous steel, not D's cropped specimen.
 with bpy.data.libraries.load(str(D),link=False) as (a,b):
  b.objects=[n for n in a.objects if n.startswith('Station ')];b.materials=['Satin steel plus computed wear depth - cool blue cyan']
 heat=b.materials[0];heat=heat.copy();heat.name='Continuous steel - fixed computed wear values v019'
 retained={m for ob in b.objects if ob for m in ob.data.materials if m};retained.add(heat);retained.add(b.materials[0])
 for m in list(bpy.data.materials):
  if m not in retained and not m.library:convert(m)
 # Compute recorded radial loss on the unchanged whole-length registered wear mesh.
 nom=bpy.data.objects['CASED_STEEL_NOMINAL_FULL'];tree=BVHTree.FromPolygons([v.co.copy() for v in nom.data.vertices],[tuple(p.vertices) for p in nom.data.polygons])
 attr=steel.data.attributes.get('ComputedWearDepth_m') or steel.data.attributes.new('ComputedWearDepth_m','FLOAT','POINT');rows=[]
 for v,a in zip(steel.data.vertices,attr.data):
  x,y,z=v.co;r=math.hypot(y,z);loss=0
  if r<.164:
   di=Vector((0,y,z)).normalized();p=tree.ray_cast(Vector((x,0,0)),di,1)[0]
   if p is not None:loss=max(0,r-math.hypot(p.y,p.z))
   if loss<1e-7:loss=0
  a.value=loss;rows.append([v.index,float(x),float(loss)])
 assert .0038<max(r[2] for r in rows)<.004001
 steel.data.materials.clear();steel.data.materials.append(heat)
 nt=heat.node_tree;out=next(n for n in nt.nodes if n.type=='OUTPUT_MATERIAL');hm=out.inputs['Surface'].links[0].from_node;old=hm.inputs[0].links[0].from_socket;gain=nt.nodes.new('ShaderNodeValue');gain.name='Expose fixed recorded depth';mul=nt.nodes.new('ShaderNodeMath');mul.operation='MULTIPLY';nt.links.new(old,mul.inputs[0]);nt.links.new(gain.outputs[0],mul.inputs[1]);nt.links.new(mul.outputs[0],hm.inputs[0])
 for f in range(1,433):gain.outputs[0].default_value=sm((f-361)/43);gain.outputs[0].keyframe_insert('default_value',frame=f)
 curves=[]
 for ob in b.objects:
  if ob is None:continue
  # Retain only curves that were active in the approved station scheme.
  if not any(t in ob.name for t in ['normal-sector solid','fine dashed nominal worn-sector','blue actual worn-sector only']):continue
  s.collection.objects.link(ob);ob.animation_data_clear();ob.data=ob.data.copy()
  # Fixed angular clipping matches the single physical section; never opens during motion.
  pieces=[]
  for sp in ob.data.splines:
   current=[]
   for pp in sp.points:
    p=Vector(pp.co[:3])
    if p.dot(N)<=CUT+.0001:current.append(p)
    else:
     if len(current)>1:pieces.append(current)
     current=[]
   if len(current)>1:pieces.append(current)
  ob.data.splines.clear()
  for pts in pieces:
   sp=ob.data.splines.new('POLY');sp.points.add(len(pts)-1)
   for pp,p in zip(sp.points,pts):pp.co=(*p,1)
  station=int(ob.name.split()[1]);blue='blue actual' in ob.name;start=316+max(0,station-2)*6+(8 if blue else 0)
  m=ob.data.materials[0].copy();ob.data.materials[0]=m
  m.node_tree.animation_data_clear() if m.node_tree.animation_data else None
  output=next(n for n in m.node_tree.nodes if n.type=='OUTPUT_MATERIAL');old=output.inputs['Surface'].links[0].from_socket;tr=m.node_tree.nodes.new('ShaderNodeBsdfTransparent');mix=m.node_tree.nodes.new('ShaderNodeMixShader');m.node_tree.links.new(tr.outputs[0],mix.inputs[1]);m.node_tree.links.new(old,mix.inputs[2]);m.node_tree.links.new(mix.outputs[0],output.inputs['Surface']);m.surface_render_method='BLENDED'
  for f in range(1,433):
   value=sm((f-start)/12);mix.inputs[0].default_value=value;mix.inputs[0].keyframe_insert('default_value',frame=f);ob.hide_render=value<.001;ob.hide_viewport=ob.hide_render;ob.keyframe_insert('hide_render',frame=f);ob.keyframe_insert('hide_viewport',frame=f)
  curves.append(ob.name)
 # Same camera datablock for every main-view frame, with independently smooth position/gaze/lens.
 cam=s.camera;cam.animation_data_clear();cam.data=cam.data.copy();cam.data.animation_data_clear();cam.rotation_mode='QUATERNION';cam.data.sensor_fit='HORIZONTAL';cam.data.clip_start=.001;cam.data.clip_end=60
 poses=[(1,(2.4,-2.5,2.6),(-.15,0,0),35,0),(55,(.45,-.42,.90),(-.30,.08,.03),37,0),(97,(-.46999994,-.00599794,.4841116),(-.32,.115,.093),37.95,.25),(253,(-.46999994,-.00599794,.4841116),(-.32,.115,.093),37.95,.25),(318,(-1.12,.12,.07),(-1.86,.158,-.015),45,0),(432,(-1.12,.12,.07),(-1.86,.158,-.015),45,0)]
 score=[];prev=None
 for f in range(1,433):
  left,right=next(((a,b) for a,b in zip(poses,poses[1:]) if a[0]<=f<=b[0]),(poses[-2],poses[-1]));u=sm((f-left[0])/(right[0]-left[0]));pos=Vector(left[1]).lerp(Vector(right[1]),u);target=Vector(left[2]).lerp(Vector(right[2]),u)
  direction=(target-pos).normalized();rad=Vector((0,math.cos(PHI),math.sin(PHI)));screen_right=-(rad-direction*rad.dot(direction)).normalized();up=(-direction).cross(screen_right).normalized();q=Matrix((screen_right,up,-direction)).transposed().to_quaternion()
  if prev and prev.dot(q)<0:q.negate()
  prev=q.copy();cam.location=pos;cam.rotation_quaternion=q;cam.data.lens=(1-u)*left[3]+u*right[3];cam.data.shift_x=(1-u)*left[4]+u*right[4]
  cam.keyframe_insert('location',frame=f);cam.keyframe_insert('rotation_quaternion',frame=f);cam.data.keyframe_insert('lens',frame=f);cam.data.keyframe_insert('shift_x',frame=f)
  score.append({'frame':f,'position':list(pos),'target':list(target),'lens':cam.data.lens,'shift_x':cam.data.shift_x})
 for act in bpy.data.actions:
  if act.library:continue
  for fc in fcurves(act):
   for k in fc.keyframe_points:
    if fc.data_path.startswith('hide'):k.interpolation='CONSTANT'
    elif act not in [w.animation_data.action]:k.interpolation='LINEAR'
 # Economical unified preview illumination, no animated physical masks.
 for o in s.objects:
  if o.type=='LIGHT':o.hide_render=True
 light('Wide sectional softbox',(0,-.6,1.4),(-1,.10,0),22,1.5)
 light('Uphole fill',(-2.3,-.2,.7),(-1.7,.15,0),8,.7)
 light('Wear grazing softbox',(-1.45,-.07,.27),(-1.8,.15,-.03),1.3,.25)
 s.world=s.world.copy();s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.22,.27,.32,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.65
 s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=4;s.eevee.use_raytracing=False;s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.fps=24;s.frame_start=1;s.frame_end=432;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.image_settings.compression=10;s.render.use_compositing=False;s.view_settings.view_transform='AgX';s.view_settings.look='AgX - Medium High Contrast';s.view_settings.exposure=-.4
 s['scope']='Owner released continuous main camera A-B-D, temporary entering/exiting C comparison, permanent half-section from frame1. No cutaway animation. Inexpensive previs only.'
 for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(OUT.parent))
 s.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(OUT),relative_remap=False)
 dump('build.json',{'source_B':str(SRC),'approved_D':str(D),'single_main_camera':cam.name,'permanent_section_plane_normal':list(N),'section_offset_m':CUT,'main_geometry_static':True,'full_source_steel_statically_sectioned':True,'wear_max_m':max(r[2] for r in rows),'depth_samples':rows,'visible_station_objects':curves,'C_overlay':'Uses v018 C frames in temporary sliding panel; fixed separate physical location, not a moving well or cement change.'});dump('camera-score.json',score)
def render(mode):
 bpy.ops.wm.open_mainfile(filepath=str(OUT),load_ui=False,use_scripts=False);s=bpy.context.scene;rows=[]
 frames=[1,55,97,151,260,290,318,400] if mode=='bench' else range(1,433)
 for f in frames:
  s.frame_set(f);s.render.filepath=str(B/('Previews' if mode=='bench' else 'Work/Main')/f'S04_{f:04d}.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t;rows.append({'frame':f,'seconds':dt});dump('timings-'+mode+'.json',rows);print('FRAME',f,dt,flush=True)
  if dt>=5:raise RuntimeError('Render cap reached')
if __name__=='__main__':
 mode=sys.argv[sys.argv.index('--')+1]
 if mode=='build':build()
 else:render(mode)
