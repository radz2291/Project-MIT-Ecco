import bpy,sys,json
from pathlib import Path
from mathutils import Vector
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[4];T=ROOT/'04-Production/Records/Tasks/T-046';S=T/'Scenes';E=T/'Evidence';sys.path.insert(0,str(HERE));from build_sensing_v001 import save,snapshot,dump
for kind in ['A','B']:
 bpy.ops.wm.open_mainfile(filepath=str(S/f'Sensing_reuse_{kind}_v004.blend'),load_ui=False,use_scripts=False);s=bpy.context.scene
 before=snapshot();cam=s.camera;cam.location=(1.08,-.65,.225) if kind=='A' else (1.4,-.65,.19);target=Vector((1.23,.06,.125));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=95 if kind=='A' else 85
 # Existing camera-parent schematic cue follows framing automatically; adapt width to new lens.
 ratio=55/95 if kind=='A' else 48/85
 for o in s.objects:
  if o.parent==cam:
   o.location.x*=ratio;o.location.y*=ratio;o.scale=(ratio,ratio,ratio)
 after=snapshot();assert before['timing']==after['timing'] and before['world_control_animation']==after['world_control_animation']
 rows=[]
 for f in [17,23,31,40]:
  s.frame_set(f);bpy.context.view_layer.update();rows.append(dict(frame=f,visible=[o.name for o in s.objects if o.get('shared_package')=='Acoustics' and not o.hide_render]))
 s.frame_set(17);save(S/f'Sensing_reuse_{kind}_v005.blend');dump(E/f'camera_repair_{kind}_v005.json',dict(before=before,after=after,reason='v004 cameras looked through retained top formation; v005 sights through open cutaway into native sensor gap',visible_effects=rows))
