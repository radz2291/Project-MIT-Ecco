import bpy,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[4];T=ROOT/'04-Production/Records/Tasks/T-046';sys.path.insert(0,str(HERE));from build_sensing_v001 import save
for kind in ['A','B']:
 bpy.ops.wm.open_mainfile(filepath=str(T/f'Scenes/Sensing_reuse_{kind}_v007.blend'),load_ui=False,use_scripts=False);s=bpy.context.scene
 for o in s.objects:
  if 'FIXED_SAMPLE' in o.name and o.get('shared_package')=='Acoustics':
   for f in range(1,s.frame_end+1):o.scale=(.4,)*3;o.keyframe_insert(data_path='scale',frame=f)
 s.frame_set(17);save(T/f'Scenes/Sensing_reuse_{kind}_v008.blend')
