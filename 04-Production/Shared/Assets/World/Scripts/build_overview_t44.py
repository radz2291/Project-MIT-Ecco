import bpy,runpy,sys
from pathlib import Path
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.argv=['script','--','noop'];b=runpy.run_path(str(HERE/'build_world_t44.py'));task=b['TASK']
bpy.ops.wm.open_mainfile(filepath=str(task/'ReuseTests/Controls_stress_v001.blend'),load_ui=False,use_scripts=False)
s=bpy.context.scene;ctrl=bpy.data.objects['WORLD_CONTROL'];ctrl.animation_data_clear()
for k in ['show_open','show_casing','show_cement','show_shoe','show_formation','show_mud']:ctrl[k]=0
ctrl['travel_m']=.5;ctrl['rotation_rad']=.4;ctrl.update_tag();bpy.context.view_layer.update()
s['consumer']='Hardware';s.frame_end=1;s.frame_set(1);cam=s.camera;cam.location=(1.4,-7,2);cam.rotation_euler=(Vector((1.37,0,0))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=45
path=task/'ReuseTests/Hardware_overview_v001.blend';b['save'](path);b['benchmark'](path,[1])
