import bpy,json,math,sys
from pathlib import Path
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).parent))
from pulse_graph import set_input
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');B=R/'04-Production/Shared/Assets/Effects/Waveform';Q=R/'04-Production/Shots/S01-S02';out=R/'04-Production/Shared/Demos/Waveform_demo_v017.blend';assert not out.exists() or '--candidate-rebuild' in sys.argv
bpy.ops.wm.read_factory_settings(use_empty=True)
with bpy.data.libraries.load(str(B/'Waveform_shared_v017.blend'),link=True) as (a,b):b.objects=['WF_MASTER_CONTROLS','WF_PULSE_FIELD']
ctrl,source=b.objects
with bpy.data.libraries.load(str(Q/'Scenes/Waveform_direction_quick_v006.blend'),link=False) as (a,b):b.objects=['QUICK perspective360']
orbit=b.objects[0];assert orbit
axis=Vector((.3583680987,-.9335803986,0));side=Vector((-.9335803986,-.3583680987,0));up=Vector((0,0,1));gap=.0245758537
def material(name,color):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True;m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(*color,1);return m
gray=material('DEMO neutral anchors',(.32,.38,.42));warm=material('DEMO local outgoing override',(1.,.6,.05));green=material('DEMO local return override',(.12,1.,.35))
cases=[{'name':'01 Approved360','frames':192,'fps':24,'orbit':True,'start':(0,0,0),'end':tuple(axis*gap),'settings':{}},
 {'name':'02 Fixed review','frames':96,'fps':24,'orbit':False,'start':(0,0,0),'end':tuple(axis*gap),'settings':{}},
 {'name':'03 Local variation','frames':112,'fps':24,'orbit':False,'start':(-.02,.01,-.005),'end':(.02,.024,.007),'settings':{'Use master style':False,'Pulse count':5,'Strand count':9,'Strand separation':.8,'Width variation':.3,'Pulse spacing':4.8,'Echo strength':.6,'Use material overrides':True}},
 {'name':'04 Fit-end30fps','frames':60,'fps':30,'orbit':False,'start':(0,0,0),'end':tuple(axis*gap),'settings':{'Pulse count override':1,'Strand count override':3,'Fit end frame':48.,'Loop':False}}]
for j,case in enumerate(cases):
 s=bpy.context.scene if j==0 else bpy.data.scenes.new(case['name']);s.name=case['name'];bpy.context.window.scene=s;s.collection.objects.link(ctrl)
 field=source.copy();field.name=case['name']+' PULSE';s.collection.objects.link(field);mod=field.modifiers[0]
 points=[];route=Vector(case['end'])-Vector(case['start']);direction=route.normalized()
 for k,pos in enumerate([case['start'],case['end']]):
  bpy.ops.mesh.primitive_torus_add(major_radius=.011,minor_radius=.00015,major_segments=48,minor_segments=6,location=pos);anchor=bpy.context.object;anchor.name=case['name']+(' A' if k==0 else ' B');anchor.rotation_mode='QUATERNION';anchor.rotation_quaternion=Vector((0,0,1)).rotation_difference(direction);anchor.data.materials.append(gray);points.append(anchor)
 for name,val in {'Use anchor objects':True,'Start anchor':points[0],'End anchor':points[1],**case['settings']}.items():set_input(mod,name,val)
 if case['name']=='03 Local variation':set_input(mod,'Outgoing material',warm);set_input(mod,'Reflected material',green)
 if case['orbit']:s.collection.objects.link(orbit);s.camera=orbit
 else:
  data=bpy.data.cameras.new(case['name']+' camera');data.type='PERSP';data.lens=45;data.clip_start=.0001;data.clip_end=10.;cam=bpy.data.objects.new(data.name,data);s.collection.objects.link(cam);center=(Vector(case['start'])+Vector(case['end']))/2+up*.002;normal=direction.cross(up).normalized();cam.location=center+normal*.12+up*.04;cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler();s.camera=cam
 if case['name']=='03 Local variation':s.camera.location=center+(s.camera.location-center)*1.5
 s.frame_start=1;s.frame_end=case['frames'];s.render.fps=case['fps'];s.render.engine='BLENDER_WORKBENCH';s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.display.render_aa='8';s.display.shading.light='STUDIO';s.display.shading.color_type='MATERIAL';s.display.shading.show_shadows=False;s.display.shading.show_cavity=False;s.world=bpy.data.worlds.new(case['name']+' world');s.world.color=(.025,.025,.025);s.view_settings.view_transform='Standard';s.frame_set(18)
 s['pulse_case']=json.dumps(case)
for screen in bpy.data.screens:
 for area in screen.areas:
  if area.type=='VIEW_3D':area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.overlay.show_overlays=False
  if area.type=='PROPERTIES':area.spaces.active.context='MODIFIER'
bpy.context.window.scene=bpy.data.scenes['01 Approved360'];field=next(o for o in bpy.context.scene.objects if o.name.endswith(' PULSE'))
for o in bpy.context.selected_objects:o.select_set(False)
field.select_set(True);bpy.context.view_layer.objects.active=field
t=bpy.data.texts.new('START HERE pulse v017 demo');t.write('Four scene dropdown examples.01 exactly approved orbit/timing;02 fixed review;03 translated/tilted anchors, five-pulse nine-strand local style and material overrides;04 single pulse fitted to end48 at30fps. Source WF_MASTER_CONTROLS is linked/read-only here: edit shared master for common defaults. Local PULSE modifier controls timing, anchor routing, loops and overrides. No runtime scripts. Demos/cameras/anchors are separate from clean shared asset.\n')
bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True);bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True)
(B/'Waveform_demo_interface_v017.json').write_text(json.dumps({'native':str(out),'cases':cases,'source':'Waveform_shared_v017.blend'},indent=2));print('DEMO17_READY')
