import bpy
from pathlib import Path
B=Path(__file__).resolve().parents[1];p=B/'Scenes/S04_cinematic-previs_v005.blend'
bpy.ops.wm.open_mainfile(filepath=str(p),use_scripts=False,load_ui=False)
gm=bpy.data.materials['S04 ground viewing access']
for n in gm.node_tree.nodes:
 if n.type!='MAP_RANGE':continue
 # Animated upper angle currently evaluates at .23 at the saved first frame.
 if abs(n.inputs['From Min'].default_value-.195)<1e-4 or abs(n.inputs['From Min'].default_value-1.445)<1e-4:
  for f in range(1,433):
   n.inputs['From Min'].default_value=1.445;n.inputs['From Max'].default_value=1.515
   n.inputs['From Min'].keyframe_insert('default_value',frame=f);n.inputs['From Max'].keyframe_insert('default_value',frame=f)
 if abs(n.inputs['From Min'].default_value+.29)<1e-4:n.inputs['From Min'].default_value=.18;n.inputs['From Max'].default_value=.40
for name in ['S04 satin steel - inspection mask','S04 matte cement','S04 clear drilling-fluid optical cue']:
 m=bpy.data.materials[name]
 for n in m.node_tree.nodes:
  if n.type!='MAP_RANGE':continue
  if abs(n.inputs['From Min'].default_value+.29)<1e-4:n.inputs['From Min'].default_value=.18;n.inputs['From Max'].default_value=.40
  if name!='S04 clear drilling-fluid optical cue' and abs(n.inputs['From Min'].default_value-.195)<1e-4:
   for f in range(1,433):
    t=(f-1)/24
    def smooth(x):
     x=max(0,min(1,x));return x*x*x*(10+x*(-15+6*x))
    high=.23+.9*(smooth((t-1.4)/1.)-smooth((t-8.7)/.7))
    n.inputs['From Min'].default_value=high-.035;n.inputs['From Max'].default_value=high+.035
    n.inputs['From Min'].keyframe_insert('default_value',frame=f);n.inputs['From Max'].keyframe_insert('default_value',frame=f)
bpy.context.scene.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(p))
for f in [48,72,96]:
 bpy.context.scene.frame_set(f);bpy.context.scene.render.filepath=str(B/'Previews'/f'Entry_check_{f:04d}.png');bpy.ops.render.render(write_still=True)
