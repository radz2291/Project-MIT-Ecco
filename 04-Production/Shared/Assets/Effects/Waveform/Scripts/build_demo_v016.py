"""Separate linked Organic, Short/S02, Short/S04-open and Short/S04-cased fixtures."""
import bpy,math,json,sys
from pathlib import Path
from mathutils import Vector
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');B=R/'04-Production/Shared/Assets/Effects/Waveform';out=R/'04-Production/Shared/Demos/Waveform_demo_v016.blend';assert not out.exists() or '--rebuild-candidate' in sys.argv
bpy.ops.wm.read_factory_settings(use_empty=True)
with bpy.data.libraries.load(str(B/'Waveform_shared_v016.blend'),link=True) as (a,b):b.objects=['WF_LIVE_FIELD','WF_MASTER_CONTROLS']
source,ctrl=b.objects
def value(mod,name,v):
 x=next(x for x in mod.node_group.interface.items_tree if getattr(x,'in_out','')=='INPUT' and x.name==name);getattr(mod.properties.inputs,x.identifier).value=v
def material(name,color):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);return m
def constant(id):
 if not id.animation_data or not id.animation_data.action:return
 for l in id.animation_data.action.layers:
  for st in l.strips:
   for bag in st.channelbags:
    for fc in bag.fcurves:
     for k in fc.keyframe_points:k.interpolation='CONSTANT'
cases=[{'name':'01 Organic reference','preset':0,'start':8.,'contact':20.,'receipt':62.,'delay':0.,'travel':12.,'return':12.,'gap':.0245758537,'cased':0,'range':[1,96],'measure':68.},
 {'name':'02 Short S01-S02','preset':1,'start':300.,'contact':309.,'receipt':318.,'delay':1.,'travel':9.,'return':8.,'gap':.0245758519,'cased':0,'range':[298,326],'measure':319.},
 {'name':'03 Short S04 open','preset':1,'start':72.59999847,'contact':80.91999817,'receipt':90.51999664,'delay':.63999939,'travel':8.31999969,'return':8.95999908,'gap':.0278588248,'cased':0,'range':[70,96],'measure':91.51999664},
 {'name':'04 Short S04 cased','preset':1,'start':184.6000061,'contact':192.91999817,'receipt':202.52000427,'delay':.63999939,'travel':8.31999207,'return':8.96000671,'gap':.0278711039,'cased':1,'range':[182,208],'measure':203.52000427}]
for index,case in enumerate(cases):
 s=bpy.context.scene if index==0 else bpy.data.scenes.new(case['name']);s.name=case['name'];bpy.context.window.scene=s;s.collection.objects.link(ctrl)
 s.render.engine='BLENDER_WORKBENCH';s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.fps=24;s.frame_start,s.frame_end=case['range'];s.world=bpy.data.worlds.new(case['name']+' world');s.world.color=(.025,.025,.025)
 sh=s.display.shading;sh.light='STUDIO';sh.color_type='MATERIAL';sh.show_shadows=False;sh.show_cavity=False;sh.background_type='WORLD';s.display.render_aa='8';s.view_settings.view_transform='Standard'
 field=bpy.data.objects.new(case['name']+' field',source.data);s.collection.objects.link(field);mod=field.modifiers.new('Shared v016 preset and shot-local landmarks','NODES');mod.node_group=source.modifiers[0].node_group
 settings={'Motion Preset 0 Organic 1 Short':case['preset'],'Start Frame':case['start'],'Contact Frame':case['contact'],'Receipt Frame':case['receipt'],'Travel Override':case['travel'],'Return Travel Override':case['return'],'Echo Delay Frames':case['delay'],'Lock Event Timing':1.,'Gap Length m':case['gap'],'Preset 0 Open 1 Cased':case['cased'],'Radius Override':1.,'Route Axis':(1,0,0),'Transverse Axis':(0,1,0),'Up Axis':(0,0,1)}
 for name,v in settings.items():value(mod,name,v)
 sensor=material(case['name']+' sensor',(.25,.29,.32));wall=material(case['name']+' wall',(.23,.14,.08));patch=material(case['name']+' measurement cue',(.08,.6,.8))
 for name,x,mat in [('sensor',-.001,sensor),('wall',case['gap']+.001,wall)]:
  if name=='sensor':bpy.ops.mesh.primitive_torus_add(major_radius=.021,minor_radius=.0004,major_segments=64,minor_segments=6,location=(x,0,0),rotation=(0,math.pi/2,0))
  else:bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=.021,depth=.002,location=(x,0,0),rotation=(0,math.pi/2,0))
  ob=bpy.context.object;ob.name=case['name']+' '+name;ob.data.materials.append(mat)
 for mat,f in [(wall,case['contact']),(sensor,case['receipt'])]:
  base=tuple(mat.diffuse_color);mat.keyframe_insert(data_path='diffuse_color',frame=case['range'][0]);mat.diffuse_color=(.02,.75,1,1);mat.keyframe_insert(data_path='diffuse_color',frame=f);mat.diffuse_color=base;mat.keyframe_insert(data_path='diffuse_color',frame=f+2);constant(mat)
 bpy.ops.mesh.primitive_cube_add(size=1,location=(case['gap']+.007,0,-.026));cue=bpy.context.object;cue.name=case['name']+' measurement AFTER receipt';cue.data.materials.append(patch);cue.scale=(0,0,0);cue.keyframe_insert(data_path='scale',frame=s.frame_start);cue.scale=(.006,.012,.004);cue.keyframe_insert(data_path='scale',frame=case['measure']);constant(cue)
 camera=bpy.data.cameras.new(case['name']+' camera');camera.type='ORTHO';camera.ortho_scale=.092;camera.clip_start=.0001;camera.clip_end=10.;ob=bpy.data.objects.new(camera.name,camera);s.collection.objects.link(ob);ob.location=(-.065,-.11,.04);ob.rotation_euler=(Vector((case['gap']/2,0,0))-ob.location).to_track_quat('-Z','Y').to_euler();s.camera=ob
 for label,f in [('Emit',case['start']),('Contact',case['contact']),('Receipt',case['receipt']),('Measurement cue',case['measure'])]:s.timeline_markers.new(label,frame=round(f))
 s['waveform_case']=json.dumps(case);s.frame_set(round(case['contact']+2))
txt=bpy.data.texts.new('START HERE waveform v016 demo');txt.write('Four scene dropdown choices: Organic reference, Short S01-S02, Short S04 open/cased. Shared v016 source linked; camera/fixtures/cues are demo-only. S04 fixtures use recorded event windows/gaps and canonical display orientation; no approved S04 source/camera/dataset is migrated. Cue first appears after receipt. All24fps native GN, no script autoexec. Select field modifier for preset and local landmarks; MASTER source owns Short style. Authored illustration.\n')
bpy.context.window.scene=bpy.data.scenes['02 Short S01-S02'];bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True);bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True)
(B/'Waveform_demo_interface_v016.json').write_text(json.dumps({'native':str(out),'cases':cases,'scope':'isolated reusable fixtures, no approved S04 integration'},indent=2));print('DEMO_V016_READY')
