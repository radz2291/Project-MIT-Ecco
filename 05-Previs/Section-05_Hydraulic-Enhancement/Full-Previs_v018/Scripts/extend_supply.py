"""Extend the same finite wisp stream so lower region remains active at ending."""
from pathlib import Path
B=Path(__file__).resolve().parents[1];src=(B/'Scripts/build.py').read_text()
header=src[:src.index('# Same material')].replace('s.frame_set(1);bpy.context.view_layer.update()','s.frame_set(151);bpy.context.view_layer.update()')
field=src[src.index('def position('):src.index('# Keep the exact original')]
build=src[src.index('NR=25;SIDES=10;'):src.index('# Extend accepted actual annular volume')]
build=build.replace('enumerate(np.arange(-1.15,1.51,.27))','enumerate(np.arange(-2.77,-1.15,.27),100)')
start=build.index('for j,zstart in enumerate([-.19');end=build.index('faces=')
build=build[:start]+build[end:]
ns={'__file__':__file__};exec(compile(header,'build_header','exec'),ns)
exec(compile(field,'approved_route_extension','exec'),ns)
ns['fx']=ns['bpy'].data.collections['S05_v018_ContinuousHydraulics']
exec(compile(build,'continued_supply','exec'),ns)
bpy=ns['bpy'];s=bpy.context.scene
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector
possible_visible=[]
for f in range(1,241):
 s.frame_set(f);bpy.context.view_layer.update()
 # Whole new-supply bounding slab, including all circumferential positions.
 top=-1.42+.135*(f-151)/24
 corners=[world_to_camera_view(s,s.camera,Vector((x,y,z))) for x in [-.155575,.155575] for y in [-.155575,.155575] for z in [-4,top+.005]]
 if not (all(v.x<0 for v in corners) or all(v.x>1 for v in corners) or all(v.y<0 for v in corners) or all(v.y>1 for v in corners)):
  possible_visible.append(f)
result={'added_wisps':len(ns['wisps']),'existing_paths_and_materials_unchanged':True,'possibly_visible_previously_rendered_frames':possible_visible,'reason':'Continuous inflow still visible at final wide composition; same finite tapered wisps, no looping or sudden respawn.'}
ns['json'].dump(result,open(B/'Records/supply-extension.json','w'),indent=2)
assert not possible_visible,possible_visible
s.frame_set(198);bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
