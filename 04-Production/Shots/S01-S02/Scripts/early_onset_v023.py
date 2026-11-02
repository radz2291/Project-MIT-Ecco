"""Advance the first gentle recorded rows to frame520, preserving the later sweep."""
import bpy,json,datetime,hashlib
from pathlib import Path
Q=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/Shots/S01-S02')
assert bpy.data.filepath.endswith('S01-S02_production_v022.blend')
out=Q/'Scenes/S01-S02_production_v023.blend';assert not out.exists()
if bpy.data.is_dirty:bpy.ops.wm.save_as_mainfile(filepath=str(Q/'Scenes'/('Before_early_onset_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S')+'.blend')),copy=True,compress=True)
w=bpy.data.objects['ONE WALL - old history and current cells share topology'];a=w.data.attributes['ecco_reveal_order'];history=[p for p in w.data.polygons if w.data.materials[p.material_index].name=='Recorded shell — common settled blue'];finite=[a.data[p.index].value+1 for p in history if a.data[p.index].value<90000];old_first=min(finite);new_first=518.;catchup=620.;shift=old_first-new_first;changed=0;late_unchanged=0
for p in history:
 old=a.data[p.index].value+1
 if old>=catchup:late_unchanged+=1;continue
 t=max(0.,min(1.,(old-old_first)/(catchup-old_first)));ease=t*t*(3-2*t);new=old-shift*(1-ease);a.data[p.index].value=new-1;changed+=1
w['Upward reveal']='Gentle first cells begin518 and are visible520; smoothly rejoins v022 timing by620; late sweep/camera unchanged.'
bpy.context.scene.frame_set(520);bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True)
(Q/'Notes/early_onset_v023.json').write_text(json.dumps({'scene':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'source':'S01-S02_production_v022.blend','old_first_cell':old_first,'new_first_cell':new_first,'visible_motion_frame':520,'native_cell_settle_frames':4,'rejoins_previous_timing_by':catchup,'early_history_faces_retimed':changed,'late_history_faces_unchanged':late_unchanged,'preserved':['camera/BHA motion','sixbeam/pulse/contact/localtilereveals','bluecolor/continuation/closedwide','latev022upwardsweepfrom620','finaldisplayexclusions','sharedmasters']},indent=2))
result={'saved':str(out),'first_cell':new_first,'visible_by':520,'late_timing_preserved_from':catchup}
