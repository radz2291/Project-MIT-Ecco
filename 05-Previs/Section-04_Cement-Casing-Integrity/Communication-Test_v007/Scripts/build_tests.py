import bpy,bmesh,math,json,time,sys,hashlib
from pathlib import Path
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
R=Path(r'C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');B=Path(__file__).resolve().parents[1];A=R/'04-Production/Shared/Assets'
BASE=R/'05-Previs/Section-04_Cement-Casing-Integrity/Cinematic-Previs_v006/Scenes/S04_cinematic-previs_v006.blend'
SHAPES=json.loads((B/'Records/Section2-front-shapes.json').read_text());RI=.1589405;RO=.1698625
sys.path.insert(0,str(A/'Acoustics/Scripts'))
from acoustic_event_v002 import sample_native_event,validate_native_event,native_instance
def smooth(t):
 t=max(0,min(1,t));return t*t*(3-2*t)
def dump(n,x):(B/'Records'/n).write_text(json.dumps(x,indent=2))
def folder(case):return B/('Test-2_Inner-Wear' if case=='D' else 'Test-1_Matched-Response')
def mat(n,c,a=1):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,a);return m
def addmesh(n,v,faces,m):
 d=bpy.data.meshes.new(n);d.from_pydata(v,[],faces);d.update();o=bpy.data.objects.new(n,d);bpy.context.scene.collection.objects.link(o);d.materials.append(m);return o
def curve(n,pts,m,w=.00012):
 d=bpy.data.curves.new(n,'CURVE');d.dimensions='3D';d.resolution_u=1;d.bevel_depth=w;d.bevel_resolution=0;sp=d.splines.new('POLY');sp.points.add(len(pts)-1)
 for p,co in zip(sp.points,pts):p.co=(*co,1)
 o=bpy.data.objects.new(n,d);bpy.context.scene.collection.objects.link(o);d.materials.append(m);return o
def cube(n,p,size,m):
 h=size/2;verts=[tuple(Vector(p)+Vector((x*h,y*h,z*h))) for x,y,z in [(-1,-1,-1),(-1,-1,1),(-1,1,-1),(-1,1,1),(1,-1,-1),(1,-1,1),(1,1,-1),(1,1,1)]]
 return addmesh(n,verts,[(0,4,6,2),(1,3,7,5),(0,1,5,4),(2,6,7,3),(0,2,3,1),(4,5,7,6)],m)
def visibility(o,alphas):
 m=o.data.materials[0];rgb=list(m.diffuse_color[:3])
 for f,a in enumerate(alphas,1):
  m.diffuse_color=(*rgb,a);m.keyframe_insert('diffuse_color',frame=f);o.hide_render=a<.005;o.hide_viewport=o.hide_render;o.keyframe_insert('hide_render',frame=f);o.keyframe_insert('hide_viewport',frame=f)
def fixed_section(o,xcenter,color):
 o.data=o.data.copy();bm=bmesh.new();bm.from_mesh(o.data)
 bad=[]
 for face in bm.faces:
  c=o.matrix_world@face.calc_center_median();a=math.atan2(c.z,c.y)
  if a>.72 or a<-.5*math.pi or abs(c.x-xcenter)>.8:bad.append(face)
 bmesh.ops.delete(bm,geom=bad,context='FACES');bm.to_mesh(o.data);bm.free();o.data.update();o.data.materials.clear();o.data.materials.append(mat('Fixed sectional '+o.name,color))
 for p in o.data.polygons:p.material_index=0;p.use_smooth=True
 for slot in o.material_slots:slot.link='DATA'
 o.animation_data_clear();o.hide_render=False;o.hide_viewport=False;o['display']='Fixed section only; retained source vertices unchanged; no opening animation'
def camera(eye,target,leftward=True,lens=45):
 cam=bpy.context.scene.camera;cam.animation_data_clear();cam.data.animation_data_clear();cam.data.lens=lens;cam.data.clip_start=.0005
 f=(Vector(target)-Vector(eye)).normalized();rad=Vector((0,1,0)) if not leftward else Vector((0,math.cos(math.radians(39)),math.sin(math.radians(39))))
 right=(rad-f*rad.dot(f)).normalized()*(-1 if leftward else 1);up=(-f).cross(right).normalized();q=Matrix((right,up,-f)).transposed().to_quaternion();cam.location=eye;cam.rotation_mode='QUATERNION';cam.rotation_quaternion=q;return cam
def prepare(case):
 bpy.ops.wm.open_mainfile(filepath=str(BASE),load_ui=False,use_scripts=False);s=bpy.context.scene;s.frame_start=1;s.frame_end=120;s.render.fps=24;s.render.engine='BLENDER_WORKBENCH';s.display.render_aa='FXAA';s.render.resolution_x=1280 if case=='D' else 960;s.render.resolution_y=720 if case=='D' else 540
 s.display.shading.light='STUDIO';s.display.shading.studio_light='paint.sl';s.display.shading.show_shadows=False;s.display.shading.color_type='MATERIAL';s.view_settings.view_transform='Standard';s.view_settings.look='None';s.view_settings.exposure=0;s.view_settings.gamma=1
 s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.resolution_percentage=100
 for o in list(s.objects):
  if o.type in ['CURVE','FONT'] or o.get('shared_package')=='Acoustics':o.animation_data_clear();o.hide_render=True;o.hide_viewport=True
  if o.name.startswith('MUD_'):o.animation_data_clear();o.hide_render=True;o.hide_viewport=True
 w=bpy.data.objects['WORLD_CONTROL'];w.animation_data_clear();w['travel_m']=-1.05 if case=='B' else -2.23;w['rotation_rad']=0.;w.update_tag();s.frame_set(1);bpy.context.view_layer.update()
 if case=='D':
  _,pose=native_instance('ECCO_SENSOR_REF_01');d=pose.to_3x3()@Vector((0,0,1));phi=math.atan2(d.z,d.y);w['rotation_rad']=-phi;w.update_tag();bpy.context.view_layer.update();_,pose=native_instance('ECCO_SENSOR_REF_01');d=pose.to_3x3()@Vector((0,0,1))
  if abs(math.atan2(d.z,d.y))>.01:w['rotation_rad']=phi;w.update_tag();bpy.context.view_layer.update()
 cc=bpy.data.objects['CASED_CONTROL'];cc.animation_data_clear();cc['cutaway']=1;cc['wear']=1;cc['show_steel']=1;cc.update_tag();bpy.context.view_layer.update()
 e=sample_native_event('ECCO_SENSOR_REF_01','CASED_STEEL_WEAR_CUTAWAY','s04-v007-'+case,.60,1.20,1.80);validate_native_event(e)
 cc['show_steel']=0;cc.update_tag();bpy.context.view_layer.update()
 source=bpy.data.objects['CASED_STEEL_WEAR_CUTAWAY'];old=bpy.data.objects['Steel - unchanged source with viewing window'];old.hide_render=True;old.hide_viewport=True
 steel=bpy.data.objects.new('ACTUAL STEEL INNER SURFACE - fixed source section',source.data);s.collection.objects.link(steel)
 xc=e['emitter_world_m'][0];fixed_section(steel,xc,(.29,.34,.38))
 for o in list(s.objects):
  if o.name.startswith('Cement ') and o.type=='MESH':fixed_section(o,xc,(.49,.39,.27))
  if o.name=='Section 2 geological surroundings - outside cement':fixed_section(o,xc,(.42,.28,.15))
  if 'Stationary organic fluid' in o.name:
   fixed_section(o,xc,(.05,.40,.53))
   m=mat('Static fluid illustration',(.05,.40,.53),.22)
   for slot in o.material_slots:slot.link='OBJECT';slot.material=m
 src=Vector(e['emitter_world_m']);hit=Vector(e['hit_world_m']);d=Vector(e['direction_world']);tree=BVHTree.FromPolygons([v.co.copy() for v in steel.data.vertices],[list(p.vertices) for p in steel.data.polygons]);return s,w,steel,e,tree
def reaction(e,tree,case):
 src=Vector(e['emitter_world_m']);hit=Vector(e['hit_world_m']);d=Vector(e['direction_world']);u=Vector((1,0,0));v=d.cross(u).normalized();color=(.13,.93,1.)
 # Contact cells are projected onto the actual visible steel, not a helper wall.
 for i in range(-3,4):
  for j in range(-3,4):
   origin=src+u*i*.0017+v*j*.0017;point,normal,face,dist=tree.ray_cast(origin,d,.2)
   if point is None:continue
   m=mat('Contact pixel '+str((i,j)),color,0);o=cube('Wall-fixed contact pixel '+str((i,j)),point-d*.00018,.00105,m)
   delay=((i*i+j*j)%4)*.018
   visibility(o,[max(0,.8*math.exp(-(5 if case=='B' else 1.4)*((f-1)/24-1.2-delay))) if 0<=(f-1)/24-1.2-delay<(.6 if case=='B' else 2.5) else 0 for f in range(1,121)])
 # Information cells occupy the exposed backing section; never a beam through steel.
 count=4 if case=='B' else 7
 for i in range(count):
  for j in range(3):
   for k in range(3):
    if case=='C' and (i*7+j*3+k)%4==0:continue
    radius=RO+.002+j*.004;a=.735+k*.012;pos=Vector((hit.x+(i-(count-1)/2)*.004,radius*math.cos(a),radius*math.sin(a)))
    m=mat('Backing information cell '+str((i,j,k)),color,0);o=cube('Illustrative backing reaction '+str((i,j,k)),pos,.00135,m);o['meaning']='Information visualization of casing response influenced by backing; not transmitted ray or material image'
    phase=(i*3+j*5+k*7)%11;alpha=[]
    for f in range(1,121):
     dt=(f-1)/24-1.2-(.02 if case=='B' else phase*.012)
     val=0
     if 0<=dt<(.65 if case=='B' else 2.7):val=.85*math.exp(-(5.5 if case=='B' else .8)*dt)*(1 if case=='B' else .65+.35*math.cos(4.5*dt+phase)**2)
     alpha.append(val)
    visibility(o,alpha)
def fronts(e,tree):
 src=Vector(e['emitter_world_m']);hit=Vector(e['hit_world_m']);d=Vector(e['direction_world']);u=Vector((1,0,0));v=d.cross(u).normalized();L=(hit-src).length;checks=[]
 for role in ['SEND','ECHO']:
  sh=SHAPES[role];returning=role=='ECHO';direction=-d if returning else d
  pts=[u*p[0]+v*p[1]+direction*p[2] for p in sh['shape']]
  for k in range(3):
   m=mat('S02 '+role+str(k),tuple(sh['source_color'][:3]),0);o=curve('S02 sourced '+role+' front '+str(k),pts,m,sh['bevel']);o['source']=sh['source_object'];alph=[]
   for f in range(1,121):
    t=(f-1)/24;start=(1.2 if returning else .6)+k*.07;end=(1.8 if returning else 1.2)+k*.07;q=(t-start)/(end-start);distance=L*max(0,min(1,q));taper=max(0,min(1,distance/.006,(L-distance)/.006));o.location=hit-d*distance if returning else src+d*distance;o.scale=(taper,)*3
    o.keyframe_insert('location',frame=f);o.keyframe_insert('scale',frame=f);alph.append((.85 if returning else 1.)*(1-k*.16) if 0<=q<1 else 0)
    if 0<=q<1:
     for p in pts:
      w=o.location+p*taper
      assert (w-src).dot(d)>=-.00003 and (hit-w).dot(d)>=-.00003,'Front crosses cap or wall plane'
   visibility(o,alph)
   # Small source-style digital samples move with each front, not with backing.
   for j in range(2,len(pts)-2,4):
    node=cube('Fine S02 front sample',pts[j],.00028,m);node.parent=o
def response(case):
 s,w,steel,e,tree=prepare(case);src=Vector(e['emitter_world_m']);hit=Vector(e['hit_world_m']);d=Vector(e['direction_world']);xc=src.x
 target=src+d*(.028/2+.012);eye=Vector((xc-.10,.25*math.cos(math.radians(80)),.25*math.sin(math.radians(80))))
 cam=camera(eye,target,True,45)
 rayhit,_,_,distance=tree.ray_cast(eye,(hit-eye).normalized(),2);visible=rayhit is not None and (rayhit-hit).length<.001
 dump('camera-'+case+'.json',dict(eye=list(eye),target=list(target),relative_eye=list(eye-src),relative_target=list(target-src),lens=cam.data.lens,actual_steel_contact_visible=visible,first_steel_view_hit=list(rayhit) if rayhit else None,contact=list(hit)))
 assert visible,'Actual steel contact occluded; adjust composition, not interaction plane'
 fronts(e,tree);reaction(e,tree,case);save(case,s,steel,e)
def wear():
 s,w,steel,e,tree=prepare('D');src=Vector(e['emitter_world_m']);hit=Vector(e['hit_world_m']);d=Vector(e['direction_world']);assert abs(d.z)<.01
 s.display.shading.studio_light='paint.sl';s.display.shading.show_shadows=False;s.display.shading.show_cavity=True;s.display.shading.cavity_type='BOTH';s.display.shading.show_specular_highlight=True
 cam=camera((hit.x-.10,.130,.055),(hit.x,.159,0),False,28);s.display.shading.curvature_valley_factor=.8;s.display.shading.curvature_ridge_factor=.25
 whites=(.86,.9,.92);cyans=(.08,.66,.79);amber=(.95,.68,.27)
 for kind in ['Reference','Current']:
  color=whites if kind=='Reference' else cyans;pts=[]
  for i in range(65):
   a=-.40+.8*i/64;di=Vector((0,math.cos(a),math.sin(a)));point=Vector((hit.x,0,0))+di*RI
   if kind=='Current':point=tree.ray_cast(Vector((hit.x,0,0)),di,1)[0]-di*.00010
   pts.append(point)
  for i in range(len(pts)-1):
   if kind=='Reference' and i%4>=2:continue
   o=curve(kind+' registered inner profile '+str(i),pts[i:i+2],mat(kind+' profile material '+str(i),color,0),.00010)
   visibility(o,[smooth(((f-1)/24-(1.3 if kind=='Reference' else 2.3))/.65) for f in range(1,121)])
 # Nominal intersection is a ghost reference, never a second measured wall.
 sy,sz=src.y,src.z;dy,dz=d.y,d.z;b=2*(sy*dy+sz*dz);c=sy*sy+sz*sz-RI*RI;tn=(-b+math.sqrt(b*b-4*c))/2;nominal=src+d*tn
 for name,pts,color in [('Sensor to actual inner wall',[src,hit],cyans),('Reference-current radial bracket',[nominal,hit],amber),('Reference bracket tick',[nominal+Vector((0,0,-.0016)),nominal+Vector((0,0,.0016))],amber),('Current bracket tick',[hit+Vector((0,0,-.0016)),hit+Vector((0,0,.0016))],amber)]:
  o=curve(name,pts,mat(name+' material',color,0),.00013);visibility(o,[smooth(((f-1)/24-2.8)/.65) for f in range(1,121)])
 assert 0<(hit-nominal).length<.00401
 dump('wear-relationship.json',dict(source_variant='CASED_STEEL_WEAR_CUTAWAY',source_authored_maximum_depth_m=.004,nominal=list(nominal),current=list(hit),illustrative_profile_change_m=(hit-nominal).length,emitter=list(src),outer_radius_fixed=RO,geometry_not_deepened=True,interpretation='Travel-time distance principle; mud velocity and tool position required; not direct thickness or calibrated field wear'))
 save('D',s,steel,e)
def save(case,s,steel,e):
 s['scope']='v007 bounded visual-communication test only; full18s integration not released';s['section']='Static from first frame; no earth/casing/cement opening animation';s['signal_source']='Actual S02 v011 digital wavefront key shape and colors, native S04 cap-to-steel hit';s['limits']='Illustrative response pixels, not physical propagation through backing or material photography'
 for a in bpy.data.actions:
  if a.library:continue
  for l in a.layers:
   for st in l.strips:
    for bag in st.channelbags:
     for fc in bag.fcurves:
      for p in fc.keyframe_points:p.interpolation='CONSTANT' if fc.data_path.startswith('hide') else 'LINEAR'
 s.frame_set(1);out=folder(case)/'Scenes'/('S04_'+case+'_communication_v007.blend')
 for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(out.parent))
 bpy.ops.wm.save_as_mainfile(filepath=str(out),relative_remap=False)
 r=[math.hypot(v.co.y,v.co.z) for v in steel.data.vertices];dump('native-'+case+'.json',dict(scene=str(out),event=e,source_steel='CASED_STEEL_WEAR_CUTAWAY',retained_vertex_count=len(steel.data.vertices),radial_bounds=[min(r),max(r)],geometry_action=bool(steel.animation_data),frames=120,fps=24,library_paths=[l.filepath for l in bpy.data.libraries]))
def render(case,bench=False):
 p=folder(case);bpy.ops.wm.open_mainfile(filepath=str(p/'Scenes'/('S04_'+case+'_communication_v007.blend')),use_scripts=False,load_ui=False);s=bpy.context.scene;rows=[]
 for f in ([1,32,42,72,108] if bench else range(1,121)):
  s.frame_set(f);s.render.filepath=str(p/('Previews' if bench else 'Work')/f'{case}_{f:04d}.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);elapsed=time.perf_counter()-t;rows.append(dict(frame=f,seconds=elapsed));dump(('benchmark-' if bench else 'timings-')+case+'.json',rows);print('TEST',case,f,elapsed,flush=True)
  if elapsed>=5:raise RuntimeError('Frame cap exceeded')
if __name__=='__main__':
 args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else ['build','B'];mode,case=args[:2]
 if mode=='build':wear() if case=='D' else response(case)
 else:render(case,mode=='benchmark')





