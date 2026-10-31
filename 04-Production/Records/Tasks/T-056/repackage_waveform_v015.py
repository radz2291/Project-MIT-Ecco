import bpy,pathlib,json,hashlib,math,os,numpy as np
from mathutils import Vector,Matrix
R=pathlib.Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');T=R/'04-Production/Records/Tasks/T-056';O=R/'04-Production/Shared/Assets/Acoustics/Waveform_shared_v015';O.mkdir(exist_ok=True);D=T/'Demos';D.mkdir(exist_ok=True);old=R/'04-Production/Shared/Assets/Acoustics/Waveform_shared_v014/Waveform_shared_v014.blend';before=hashlib.sha256(old.read_bytes()).hexdigest();frames=[1,12,18,26,30,38,54,62,68,96]
def coords(ob,f):
 bpy.context.scene.frame_set(f);bpy.context.view_layer.update();ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());return np.array([v.co[:] for v in ev.data.vertices])
def val(mod,name,v):
 ident=next(x.identifier for x in mod.node_group.interface.items_tree if getattr(x,'in_out','')=='INPUT' and x.name==name);getattr(mod.properties.inputs,ident).value=v;mod.id_data.update_tag(refresh={'OBJECT','DATA','TIME'});bpy.context.view_layer.update()
bpy.ops.wm.open_mainfile(filepath=str(old));s=bpy.context.scene;ref={f:coords(bpy.data.objects['WF_LIVE_FIELD'],f) for f in frames};origin=bpy.data.objects['WF_LIVE_FIELD'].location.copy();cam=s.camera.matrix_world.copy();cam.translation-=origin;camdata={'lens':s.camera.data.lens,'sensor_width':s.camera.data.sensor_width};axis=Vector((.00880720093846321,-.02294353395700455,0));gap=axis.length;axis.normalize()
bpy.ops.wm.read_factory_settings(use_empty=True)
with bpy.data.libraries.load(str(old),link=False) as(a,b):b.objects=['WF_LIVE_FIELD','WF_MASTER_CONTROLS']
s=bpy.context.scene;s.name='WAVEFORM — reusable field only';col=bpy.data.collections.new('WAVEFORM_ASSET');s.collection.children.link(col)
for ob in b.objects:col.objects.link(ob);ob.location=(0,0,0)
live=bpy.data.objects['WF_LIVE_FIELD'];ctrl=bpy.data.objects['WF_MASTER_CONTROLS'];live.data.materials.clear();live.data.materials.append(bpy.data.materials['WF_SHARED_FIELD_MATERIAL'])
for m in bpy.data.materials:m.use_fake_user=False
for g in bpy.data.node_groups:g.use_fake_user=False
bpy.data.orphans_purge(do_local_ids=True,do_linked_ids=True,do_recursive=True)
txt=bpy.data.texts.new('START HERE — shared waveform');txt.write('REUSABLE LIBRARY ONLY. Two objects at origin. Select WF_MASTER_CONTROLS > Modifiers to edit shared speed, frequency, strength, decay, dimensions and appearance. WF_LIVE_FIELD has local overrides and illustrative open/cased selector. Save and reopen linked demo to refresh. No rig/camera/history/dataset. No measured RF or calibrated physics. All animation native Geometry Nodes; no scripts/handlers needed. Demonstration is separately saved under T056/Demos/Waveform_demo_v015.blend.')
def opening(scene,active):
 scene.frame_start=1;scene.frame_end=96;scene.render.fps=24;scene.frame_set(30);bpy.ops.object.select_all(action='DESELECT');active.select_set(True);bpy.context.view_layer.objects.active=active
 for screen in bpy.data.screens:
  for area in screen.areas:
   if area.type=='VIEW_3D':
    sp=area.spaces.active;sp.region_3d.view_location=axis*gap*.5;sp.region_3d.view_distance=.14;sp.region_3d.view_rotation=cam.to_quaternion();sp.clip_start=.0001;sp.shading.color_type='MATERIAL'
   elif area.type=='PROPERTIES':area.spaces.active.context='MODIFIER'
opening(s,ctrl);shared=O/'Waveform_shared_v015.blend';bpy.ops.wm.save_as_mainfile(filepath=str(shared));bpy.ops.wm.open_mainfile(filepath=str(shared));live=bpy.data.objects['WF_LIVE_FIELD'];ctrl=bpy.data.objects['WF_MASTER_CONTROLS'];checks=[]
for f in frames:
 a=coords(live,f);checks.append({'frame':f,'vertices':len(a),'max_error_m':float(np.max(np.abs(a-ref[f]))) if len(a) else 0,'same_count':len(a)==len(ref[f])})
counts={'objects':len(bpy.data.objects),'cameras':len(bpy.data.cameras),'lights':len(bpy.data.lights),'meshes':len(bpy.data.meshes),'materials':len(bpy.data.materials),'node_groups':len(bpy.data.node_groups),'libraries':len(bpy.data.libraries)}
assert counts['objects']==2 and counts['libraries']==0 and counts['cameras']==0 and counts['lights']==0
bpy.ops.wm.read_factory_settings(use_empty=True)
with bpy.data.libraries.load(str(shared),link=True) as(a,b):b.collections=['WAVEFORM_ASSET']
s=bpy.context.scene;s.name='WAVEFORM — minimal linked demo';s.collection.children.link(b.collections[0]);linkedctrl=bpy.data.objects['WF_MASTER_CONTROLS'];s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=16;s.render.resolution_x=640;s.render.resolution_y=360;s.render.resolution_percentage=100;s.world=bpy.data.worlds.new('DEMO_WORLD');s.world.color=(.025,.025,.025)
def mat(name,color):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);return m
sensor=mat('Demo sensor — neutral',(.22,.27,.31));wall=mat('Demo wall — neutral',(.15,.105,.065))
bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=.02,depth=.004,location=-axis*.002);ob=bpy.context.object;ob.name='DEMO_SENSOR_FACE';ob.rotation_mode='QUATERNION';ob.rotation_quaternion=Vector((0,0,1)).rotation_difference(axis);ob.data.materials.append(sensor)
bpy.ops.mesh.primitive_cube_add(size=1,location=axis*(gap+.004));ob=bpy.context.object;ob.name='DEMO_WALL';ob.rotation_mode='QUATERNION';ob.rotation_quaternion=Vector((0,0,1)).rotation_difference(axis);ob.scale=(.12,.12,.008);ob.data.materials.append(wall)
camera=bpy.data.cameras.new('DEMO_CAMERA');camera.lens=camdata['lens'];camera.sensor_width=camdata['sensor_width'];camera.clip_start=.0001;ob=bpy.data.objects.new('DEMO_CAMERA',camera);s.collection.objects.link(ob);ob.matrix_world=cam;s.camera=ob
for name,pos,energy,size in [('DEMO_KEY',(.04,-.08,.08),.8,.1),('DEMO_FILL',(-.06,-.01,.02),.2,.08)]:
 light=bpy.data.lights.new(name,'AREA');light.energy=energy;light.shape='DISK';light.size=size;ob=bpy.data.objects.new(name,light);s.collection.objects.link(ob);ob.location=pos;ob.rotation_euler=(axis*gap*.5-ob.location).to_track_quat('-Z','Y').to_euler()
names=['FIELD_EMISSION','FIELD_WALL_CONTACT','FIELD_SENSOR_RECEIPT','FIELD_MEASUREMENT_AFTER_RECEIPT']
with bpy.data.libraries.load(str(old),link=False) as(a,b):b.objects=names
for ob in b.objects:s.collection.objects.link(ob);ob.location-=origin
# Cue dependency must resolve the new linked controls; no old source/master dependency retained.
for g in bpy.data.node_groups:
 if g.library:continue
 for n in g.nodes:
  if n.bl_idname=='GeometryNodeObjectInfo' and n.inputs['Object'].default_value and n.inputs['Object'].default_value.name.startswith('WF_MASTER_CONTROLS'):n.inputs['Object'].default_value=linkedctrl
for ob in list(bpy.data.objects):
 if not ob.library and ob.name.startswith('WF_MASTER_CONTROLS'):bpy.data.objects.remove(ob,do_unlink=True)
for ob in b.objects:ob.data.materials.clear()
for g in bpy.data.node_groups:
 if not g.library:g.use_fake_user=False
for m in bpy.data.materials:
 if not m.library:m.use_fake_user=False
bpy.data.orphans_purge(do_local_ids=True,do_linked_ids=True,do_recursive=True)
txt=bpy.data.texts.new('START HERE — demo');txt.write('Minimal sensor/wall fixture demonstrating the linked shared waveform. Edit the separate Waveform_shared_v015.blend master controls, save, then reopen this file. Demo cue groups read the same linked controls. Authored illustrative display, no shot dataset or camera.1–96 at24fps. Older v013/v014 and consumers remain untouched, outside this delivery.')
opening(s,linkedctrl);demo=D/'Waveform_demo_v015.blend';bpy.ops.wm.save_as_mainfile(filepath=str(demo),relative_remap=True)
for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(os.path.normpath(bpy.path.abspath(lib.filepath)))
bpy.ops.wm.save_as_mainfile(filepath=str(demo));bpy.ops.wm.open_mainfile(filepath=str(demo));demo_counts={'objects':len(bpy.data.objects),'cameras':len(bpy.data.cameras),'lights':len(bpy.data.lights),'libraries':[l.filepath for l in bpy.data.libraries]};assert len(bpy.data.objects)==11
assert hashlib.sha256(old.read_bytes()).hexdigest()==before
(T/'repackage-build_v015.json').write_text(json.dumps({'shared':str(shared),'demo':str(demo),'shared_counts':counts,'demo_counts':demo_counts,'default_comparison':checks,'pass':all(x['same_count'] and x['max_error_m']<1e-7 for x in checks),'v014_preserved_sha256':before},indent=2));print('REPACKAGE_SUCCESS',counts,demo_counts)
