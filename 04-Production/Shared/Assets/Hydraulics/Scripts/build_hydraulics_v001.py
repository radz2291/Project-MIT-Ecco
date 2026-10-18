"""T48 native shared geometry, relative consumers and bounded material revision.

Only writes Hydraulics/ and T-048/. Does not render.
"""
import bpy,math,json,sys,hashlib,struct
from pathlib import Path
from mathutils import Vector
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[4];ASSET=ROOT/'04-Production/Shared/Assets';OWN=ASSET/'Hydraulics';TASK=ROOT/'04-Production/Records/Tasks/T-048';E=TASK/'Evidence';S=TASK/'Scenes'
sys.path.insert(0,str(HERE));from hydraulics_controls_v001 import create_flow,drive
sys.path.insert(0,str(ASSET/'World/Scripts'));from formation_controls_v003 import create_world
def rel(p):return p.relative_to(ROOT).as_posix()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,indent=2),encoding='utf-8')
def clean():bpy.ops.wm.read_factory_settings(use_empty=True);return bpy.context.scene
def save(p):
 for lib in bpy.data.libraries:
  if lib.parent:continue
  name=Path(lib.filepath.replace('\\','/')).name
  matches=list(ASSET.rglob(name));assert len(matches)==1,(name,matches)
  lib.filepath=bpy.path.relpath(str(matches[0]),start=str(p.parent))
 bpy.ops.wm.save_as_mainfile(filepath=str(p),relative_remap=False)
def point(t,i):
 x=2.2-2*t
 # A gentle authored azimuthal deflection over inspected raised/twisted morphology.
 # Geometry identification is not a stage performance or velocity calculation.
 a=i*math.tau/10+.22*math.sin(math.pi*max(0,min(1,(x-.5)/1.06)))**2
 return x,.154*math.cos(a),.154*math.sin(a)
def material(name,color,emission=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True;b=m.node_tree.nodes.get('Principled BSDF');b.inputs['Base Color'].default_value=(*color,1);b.inputs['Roughness'].default_value=.68;b.inputs['Emission Color'].default_value=(*color,1);b.inputs['Emission Strength'].default_value=emission;return m
def master():
 s=clean();s.unit_settings.system='METRIC';s.unit_settings.scale_length=1
 col=bpy.data.collections.new('HYDRAULICS_GEOMETRY');s.collection.children.link(col)
 col['version']='v001';col['units_axes']='metres; +X selected downhole in immutable T44 layout; return -X'
 col['status']='Illustrative circulation-only; no CFD, calibrated velocity/pressure, exact stage-face map, wake or efficiency claim'
 amber=material('FLOW_ContinuousAmber',(.65,.205,.024),.20);matte=material('FLOW_MatteCuttings',(.20,.16,.105))
 for i in range(10):
  cu=bpy.data.curves.new('FLOW_PATH_%02d_GEOMETRY'%i,'CURVE');cu.dimensions='3D';cu.resolution_u=1;cu.bevel_depth=.00045;cu.bevel_resolution=2;cu.use_path=True;cu.path_duration=100
  sp=cu.splines.new('POLY');sp.points.add(240)
  for j,p in enumerate(sp.points):p.co=(*point(j/240,i),1)
  o=bpy.data.objects.new('FLOW_PATH_%02d'%i,cu);col.objects.link(o);cu.materials.append(amber);o['kind']='Continuous annular circulation guide, not acoustic arc';o['direction']='uphole -X from X2.2 to0.2'
 # Small faceted octahedron with exact bounding sphere radius0.7mm.
 r=.0007;vs=[(r,0,0),(-r,0,0),(0,r,0),(0,-r,0),(0,0,r),(0,0,-r)];fs=[(0,2,4),(2,1,4),(1,3,4),(3,0,4),(2,0,5),(1,2,5),(3,1,5),(0,3,5)]
 me=bpy.data.meshes.new('CUTTING_GEOMETRY');me.from_pydata(vs,[],fs);me.materials.append(matte);o=bpy.data.objects.new('CUTTING_GEOMETRY',me);col.objects.link(o);o.hide_render=True;o.hide_viewport=True
 for name,x,bounds in [('LOWER',1.455,[1.35,1.56]),('MIDDLE',1.115,[.88,1.35]),('UPPER',.69,[.5,.88])]:
  o=bpy.data.objects.new('FLOW_REGION_'+name,None);o.location=(x,0,0);o['source_x_bounds_m']=bounds;o['confidence']='Morphological screen region only; exact accelerator/twisted/diffuser assignment unverified';col.objects.link(o)
 p=OWN/'Hydraulics_v001.blend';save(p)
 # One bounded shared material revision; all linked geometry remains identical.
 col['version']='v002';amber.node_tree.nodes.get('Principled BSDF').inputs['Emission Strength'].default_value=.32;amber['revision']='v002; amber emission .20->.32; geometry unchanged, no calibrated brightness meaning'
 save(OWN/'Hydraulics_v002.blend')
def settings(s):
 s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=16;s.eevee.use_raytracing=False;s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.fps=24;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.image_settings.compression=15;s.render.film_transparent=False;s.render.use_compositing=False;s.view_settings.view_transform='AgX';s.view_settings.look='AgX - Medium High Contrast'
 w=bpy.data.worlds.new('FLOW_ReviewWorld');w.use_nodes=True;w.node_tree.nodes['Background'].inputs[0].default_value=(.13,.16,.20,1);w.node_tree.nodes['Background'].inputs[1].default_value=.45;s.world=w
def light(col,name,loc,target,power,size,color):
 d=bpy.data.lights.new(name,'AREA');d.energy=power;d.shape='DISK';d.size=size;d.color=color;d.use_shadow=False;o=bpy.data.objects.new(name,d);col.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
def snapshot():
 s=bpy.context.scene;c=s.camera
 return dict(camera=dict(name=c.name,matrix=[list(r) for r in c.matrix_world],lens=c.data.lens),timing=[s.frame_start,s.frame_end,s.render.fps],controls={o.name:{k:o[k] for k in o.keys()} for o in bpy.data.objects if not o.library and o.name.endswith('_CONTROL')},animation={o.name:[(fc.data_path,fc.array_index,[[float(p.co.x),float(p.co.y)] for p in fc.keyframe_points]) for fc in o.animation_data.action.layers[0].strips[0].channelbag(o.animation_data.action_slot).fcurves] for o in bpy.data.objects if not o.library and o.animation_data and o.animation_data.action})
def consumer(kind):
 s=clean();settings(s);s.unit_settings.system='METRIC';s.unit_settings.scale_length=1;s.frame_start=1;s.frame_end=72 if kind=='A' else 96;s['task']='T48 linked shared-asset reuse/behavior test; not an actual V3 film shot';s['consumer']=kind
 root,wc,instances=create_world(ASSET);wc['travel_m']=.5;wc['rotation_rad']=0;wc['variant']=0;wc['cutaway']=1;wc['show_casing']=0;wc['show_cement']=0;wc['show_shoe']=0;wc['show_mud']=1
 fp,fc,wrap=create_flow(OWN/'Hydraulics_v001.blend',root);fp.location.x=.5
 fc['phase']=0 if kind=='A' else .21;fc['speed']=.16 if kind=='A' else .12;fc['density']=10 if kind=='A' else 7
 # Source components and flow use the same unscaled assembly placement.
 c=bpy.data.collections.new('FLOW_CONSUMER_CAMERA_LIGHT');s.collection.children.link(c)
 d=bpy.data.cameras.new('FLOW_CAMERA_'+kind);cam=bpy.data.objects.new('FLOW_CAMERA_'+kind,d);c.objects.link(cam);s.camera=cam;d.lens=48 if kind=='A' else 52;d.clip_start=.001;d.clip_end=100
 locs=[(2.25,-2.35,.78),(2.06,-2.27,.70)] if kind=='A' else [(1.67,-1.03,.43),(1.44,-1.0,.41)]
 targets=[(1.62,0,0),(1.45,0,0)] if kind=='A' else [(1.56,0,0),(1.35,0,0)]
 for frame,loc,targ in [(1,locs[0],targets[0]),(s.frame_end,locs[1],targets[1])]:
  cam.location=loc;cam.rotation_euler=(Vector(targ)-cam.location).to_track_quat('-Z','Y').to_euler();cam.keyframe_insert('location',frame=frame);cam.keyframe_insert('rotation_euler',frame=frame)
 light(c,'FLOW_KEY',(1.2,-1.1,1.5),(1.6,0,0),48,1.7,(1,.86,.68));light(c,'FLOW_EDGE',(2.1,.15,.5),(1.5,0,0),30,.7,(.50,.70,1));light(c,'FLOW_FILL',(.5,-.8,-.4),(1.2,0,0),12,1.4,(.6,.72,1))
 wc.update_tag();fc.update_tag();s.frame_set(1);bpy.context.view_layer.update();before=snapshot();save(S/('Flow_reuse_'+kind+'_v003.blend'))
 for lib in list(bpy.data.libraries):
  if Path(bpy.path.abspath(lib.filepath)).name=='Hydraulics_v001.blend':lib.filepath=bpy.path.relpath(str(OWN/'Hydraulics_v002.blend'),start=str(S));lib.reload()
 s.frame_set(1);bpy.context.view_layer.update();after=snapshot();assert before==after
 save(S/('Flow_reuse_'+kind+'_v004.blend'));dump(E/('reuse_'+kind+'_migration_v004.json'),dict(before=before,after=after,preserved_camera_timing_animation_controls=before==after,revision='Shared amber emission .20 ->.32 only; linked data reloaded once per consumer',preserved_failed_registration='Consumer v001/v002 are retained unchanged; v003/v004 repair double particle translation'))
if __name__=='__main__':
 for kind in ['A','B']:
  for v in ['v003','v004']:
   assert not (S/('Flow_reuse_'+kind+'_'+v+'.blend')).exists(),'Candidate exists; choose new versions before rebuilding'
 if not (OWN/'Hydraulics_v001.blend').exists():master()
 assert (OWN/'Hydraulics_v002.blend').exists()
 for kind in ['A','B']:consumer(kind)
 print('T48_NATIVE_BUILD_PASS')
