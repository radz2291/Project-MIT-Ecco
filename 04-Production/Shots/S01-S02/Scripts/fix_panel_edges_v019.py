"""Disable obsolete independent acquired-row borders; use tile-derived edges only."""
import bpy,json,datetime,hashlib
from pathlib import Path
Q=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/Shots/S01-S02')
assert bpy.data.filepath.endswith('S01-S02_production_v018.blend')
out=Q/'Scenes/S01-S02_production_v019.blend';assert not out.exists()
if bpy.data.is_dirty:
 p=Q/'Scenes'/('Before_panel_edges_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S')+'.blend')
 bpy.ops.wm.save_as_mainfile(filepath=str(p),copy=True,compress=True)
rows=[]
for ob in bpy.context.scene.objects:
 if not ob.name.startswith('Unified acquired row '):continue
 previous=[]
 if ob.animation_data and ob.animation_data.action:
  ob.animation_data.action=ob.animation_data.action.copy()
  for layer in ob.animation_data.action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for fc in bag.fcurves:
      if fc.data_path in ['hide_render','hide_viewport']:
       previous.append({'path':fc.data_path,'keys':[list(k.co) for k in fc.keyframe_points]});fc.mute=True
 ob.hide_render=True;ob.hide_viewport=True;ob.hide_set(True)
 ob['Superseded border']='Use actual revealed-tile edges from the shared fine-display local style.'
 rows.append({'object':ob.name,'old_visibility':previous})
assert len(rows)==13,len(rows)
bpy.context.scene.frame_set(386);bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True)
record={'scene':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'source':'S01-S02_production_v018.blend','cause':'Independent acquired-row borders retained original previs timing: second row turns on371, current second glitch starts382. First border329 overlaps first glitch322..331, hiding the mismatch.','fix':'Disable duplicate old acquired-row borders for all six targets. Existing tile-derived edges now establish exactly with revealed geometry, including center-out glitch motion.','disabled_legacy_borders':rows,'unchanged':['camera','beam/pulse/contact/tile timings and shape','final-display exclusions and point-free lines/fill style','shared masters','camera viewing wedge'],'gap_investigation':'Blue-shell central opening is the existing camera viewing wedge; no physical BHA discontinuity. Diagnostic recorded separately; no gap edit included.'}
(Q/'Notes/panel_edges_v019.json').write_text(json.dumps(record,indent=2))
result={'saved':str(out),'old_borders_disabled':len(rows)}
