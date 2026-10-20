import bpy,bmesh,math,json,time,sys,importlib.util
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from bpy_extras.object_utils import world_to_camera_view
B=Path(__file__).resolve().parents[1];OLD=B.parent/'Communication-Test_v007';R=B.parents[2]
spec=importlib.util.spec_from_file_location('proof_helpers',B/'Scripts/proof_helpers.py');h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
RAD=Vector((0,math.cos(math.radians(39)),math.sin(math.radians(39))));TAN=Vector((0,-RAD.z,RAD.y));CUT=.00005
def record(n,v):(B/'Records'/n).write_text(json.dumps(v,indent=2))
def section(o,color):
 o.data=o.data.copy();o.animation_data_clear();bm=bmesh.new();bm.from_mesh(o.data);inv=o.matrix_world.inverted();normal=(o.matrix_world.to_3x3().transposed()@TAN).normalized();co=inv@(TAN*CUT)
 bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-7,plane_co=co,plane_no=normal,clear_outer=True,clear_inner=False)
 cut=[e for e in bm.edges if e.is_boundary and all(abs((v.co-co).dot(normal))<2e-6 for v in e.verts)]
 caps=bmesh.ops.holes_fill(bm,edges=cut,sides=0)['faces'] if cut else []
 for p in caps:p.smooth=False
 if caps:bmesh.ops.triangulate(bm,faces=caps)
 bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));boundary=sum(e.is_boundary for e in bm.edges)
 bm.to_mesh(o.data);bm.free();o.data.materials.clear();o.data.materials.append(h.mat('Solid sectional '+o.name,color));o.data.update()
 for p in o.data.polygons:p.material_index=0
 for sl in o.material_slots:sl.link='DATA'
 o.hide_render=False;o.hide_viewport=False;o['section']='Static planar cut with closed cut faces; original occupied volume and interfaces retained'
 return dict(object=o.name,cap_edges=len(cut),boundary_edges=boundary,vertices=len(o.data.vertices),faces=len(o.data.polygons))
def annular_patch(n,xc,ri,ro,halfangle,length,material):
 # A small explanatory visibility volume within the actual internal fluid gap.
 vs=[];faces=[];N=32;phi=math.radians(39)
 for x in [xc-length/2,xc+length/2]:
  for rad in [ri,ro]:
   for j in range(N+1):
    a=phi-halfangle+2*halfangle*j/N;vs.append((x,rad*math.cos(a),rad*math.sin(a)))
 q=N+1
 for j in range(N):
  faces.extend([(j,j+1,q+j+1,q+j),(2*q+j,3*q+j,3*q+j+1,2*q+j+1),(j,2*q+j,2*q+j+1,j+1),(q+j,q+j+1,3*q+j+1,3*q+j)])
 faces.extend([(0,q,3*q,2*q),(N,2*q+N,3*q+N,q+N)])
 return h.addmesh(n,vs,faces,material)
def attached_response(e,tree,case):
 hit=Vector(e['hit_world_m']);phi=math.atan2(hit.z,hit.y);ri=h.RI;ro=h.RO
 for k in range(24):
  x0=hit.x-.0144+k*.0012;x1=x0+.0012;vs=[]
  for x in [x0,x1]:
   for j in range(17):
    a=phi-.075+.075*j/16;d=Vector((0,math.cos(a),math.sin(a)));p=tree.ray_cast(Vector((x,0,0)),d,1)[0]
    assert p is not None;vs.append(tuple(p-d*.00008))
  faces=[(j,j+1,17+j+1,17+j) for j in range(16)]
  m=h.mat('Casing response band '+str(k),(.18,.85,.91),0);o=h.addmesh('STEEL-ATTACHED resonance band '+str(k),vs,faces,m)
  # The same response is visible on the closed steel section face, inside its true thickness.
  r0=math.sqrt(ri*ri-CUT*CUT);r1=math.sqrt(ro*ro-CUT*CUT)
  cap=[tuple(Vector((x,0,0))+RAD*r+TAN*(CUT+.00006)) for x,r in [(x0,r0),(x1,r0),(x1,r1),(x0,r1)]]
  capobj=h.addmesh('STEEL THICKNESS response '+str(k),cap,[(0,1,2,3)],m)
  alphas=[]
  for f in range(1,121):
   dt=(f-1)/24-1.2;val=0
   if 0<=dt<2.7:val=.95*math.exp(-(5.0 if case=='B' else .80)*dt)*(.22+.78*(.5+.5*math.cos(2*math.pi*3.0*dt-k*.25)))*math.sin(math.pi*(k+.5)/24)**.65
   alphas.append(val)
  h.visibility(o,alphas)
  # Shared material drives both; only the local attached geometry is visibility-keyed.
  for f,a in enumerate(alphas,1):
   capobj.hide_render=a<.005;capobj.hide_viewport=capobj.hide_render;capobj.keyframe_insert('hide_render',frame=f);capobj.keyframe_insert('hide_viewport',frame=f)
  o['meaning']=capobj['meaning']='Slowed illustrative casing resonance; no displacement, penetration depth, calibrated amplitude or hidden-reflector claim'
 # Weak later fronts explain a response tail, not a delayed primary echo.
 src=Vector(e['emitter_world_m']);d=Vector(e['direction_world']);L=(hit-src).length;u=Vector((1,0,0));v=d.cross(u).normalized();shape=h.SHAPES['ECHO']
 pts=[u*p[0]+v*p[1]-d*p[2] for p in shape['shape']]
 for j,start in enumerate([1.9] if case=='B' else [1.9,2.25,2.60,2.95]):
  m=h.mat('Fine resonance-tail return '+str(j),(.18,1,.55),0);o=h.curve('Casing response tail '+str(j),pts,m,.00010);alpha=[]
  for f in range(1,121):
   t=(f-1)/24;q=(t-start)/.60;dist=L*max(0,min(1,q));taper=max(0,min(1,dist/.006,(L-dist)/.006));o.location=hit-d*dist;o.scale=(taper,)*3;o.keyframe_insert('location',frame=f);o.keyframe_insert('scale',frame=f)
   alpha.append((.10 if case=='B' else .32*math.exp(-j*.32)) if 0<=q<1 else 0)
  h.visibility(o,alpha)
def build(case):
 bpy.ops.wm.open_mainfile(filepath=str(h.BASE),use_scripts=False,load_ui=False);s=bpy.context.scene;s.frame_start=1;s.frame_end=120;s.render.fps=24;s.render.engine='BLENDER_WORKBENCH';s.display.render_aa='FXAA';s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG'
 s.display.shading.light='STUDIO';s.display.shading.studio_light='paint.sl';s.display.shading.show_shadows=False;s.display.shading.show_cavity=True;s.display.shading.cavity_type='BOTH';s.display.shading.show_backface_culling=True;s.display.shading.color_type='MATERIAL';s.view_settings.view_transform='Standard';s.view_settings.look='None';s.view_settings.exposure=0;s.view_settings.gamma=1
 for o in list(s.objects):
  if o.type in ['CURVE','FONT'] or o.get('shared_package')=='Acoustics' or o.name.startswith('MUD_'):o.animation_data_clear();o.hide_render=True;o.hide_viewport=True
 w=bpy.data.objects['WORLD_CONTROL'];w.animation_data_clear();w['travel_m']=-1.05 if case=='B' else -2.23;w['rotation_rad']=0;w.update_tag();s.frame_set(1);bpy.context.view_layer.update()
 cc=bpy.data.objects['CASED_CONTROL'];cc.animation_data_clear();cc['cutaway']=1;cc['wear']=1;cc['show_steel']=1;cc.update_tag();bpy.context.view_layer.update()
 e=h.sample_native_event('ECCO_SENSOR_REF_01','CASED_STEEL_WEAR_CUTAWAY','s04-v008-'+case,.60,1.20,1.80);h.validate_native_event(e);cc['show_steel']=0;cc.update_tag();bpy.context.view_layer.update();xc=e['emitter_world_m'][0]
 bpy.data.objects['Steel - unchanged source with viewing window'].hide_render=True;bpy.data.objects['Steel - unchanged source with viewing window'].hide_viewport=True
 steel=bpy.data.objects.new('STEEL - capped true source section',bpy.data.objects['CASED_STEEL_WEAR_CUTAWAY'].data);s.collection.objects.link(steel);rows=[section(steel,(.22,.28,.32))]
 for o in list(s.objects):
  if o.name.startswith('Cement ') and o.type=='MESH':rows.append(section(o,(.68,.56,.38)))
  if o.name=='Section 2 geological surroundings - outside cement':rows.append(section(o,(.20,.15,.10)))
  if 'Stationary organic fluid' in o.name:
   rows.append(section(o,(.035,.39,.52)))
   o.hide_render=False;o.hide_viewport=False;o.data.materials[0].diffuse_color=(.035,.39,.52,.80)
   o['meaning']='Existing static fluid volume outside steel, in the absent-cement region; no flow'
 for row in rows:
  if any(t in row['object'] for t in ['STEEL','Cement','Stationary organic fluid']):assert row['boundary_edges']==0,row
 # Restrained interior fluid tint has real depth and stays inside the native steel ID.
 fluid=annular_patch('Internal fluid visibility volume',xc,.13105,h.RI-.00012,.22,.60,h.mat('Internal fluid tint',(.18,.42,.53),.13));section(fluid,(.18,.42,.53));fluid.data.materials[0].diffuse_color=(.18,.42,.53,.13);fluid['meaning']='Illustrative tint within the fluid gap near sensor, not a new physical boundary or a fluid stream'
 src=Vector(e['emitter_world_m']);hit=Vector(e['hit_world_m']);target=Vector((xc,0,0))+RAD*.148
 eye=Vector((xc-.15,0,0))+RAD*.30+TAN*.38
 cam=h.camera(eye,target,True,46)
 tree=BVHTree.FromPolygons([v.co.copy() for v in steel.data.vertices],[list(p.vertices) for p in steel.data.polygons]);viewhit=tree.ray_cast(eye,(hit-eye).normalized(),2)[0];assert viewhit is not None and (viewhit-hit).length<.001,'Contact not visible'
 h.fronts(e,tree)
 for o in list(s.objects):
  if o.name.startswith('Fine S02 front sample'):bpy.data.objects.remove(o,do_unlink=True)
 attached_response(e,tree,case)
 s['scope']='Owner-released B/C physical readability and attached resonance proof. D paused. No full integration.';s['interpretation']='Generic pulse echo principle, slowed illustrative response; no quantitative ECCO performance claim'
 for a in bpy.data.actions:
  if a.library:continue
  for layer in a.layers:
   for st in layer.strips:
    for bag in st.channelbags:
     for fc in bag.fcurves:
      for k in fc.keyframe_points:k.interpolation='CONSTANT' if fc.data_path.startswith('hide') else 'LINEAR'
 out=B/'Scenes'/f'S04_{case}_capped-resonance_v008.blend';s.frame_set(1)
 for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(out.parent))
 bpy.ops.wm.save_as_mainfile(filepath=str(out),relative_remap=False)
 record('build-'+case+'.json',dict(event=e,sections=rows,camera_relative_eye=list(eye-src),camera_relative_target=list(target-src),lens=cam.data.lens,contact_visible=True,source_geometry='CasedHole_v002; only static section closure and clipping; no source deformation',native=str(out)))
def render(case,bench):
 bpy.ops.wm.open_mainfile(filepath=str(B/'Scenes'/f'S04_{case}_capped-resonance_v008.blend'),use_scripts=False,load_ui=False);s=bpy.context.scene;rows=[]
 for f in ([1,25,32,55,78] if bench else range(1,121)):
  s.frame_set(f);s.render.filepath=str(B/('Previews' if bench else 'Work')/f'{case}_{f:04d}.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t;rows.append(dict(frame=f,seconds=dt));record(('benchmark-' if bench else 'timings-')+case+'.json',rows);print(case,f,dt,flush=True)
  if dt>=5:raise RuntimeError('Frame cap exceeded')
if __name__=='__main__':
 args=sys.argv[sys.argv.index('--')+1:];mode,case=args[:2]
 if mode=='build':build(case)
 else:render(case,mode=='benchmark')




