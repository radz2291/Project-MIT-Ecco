"""Owner steering: first rock-interior view at95. Local smooth two-frame advance.
Camera returns to original timing by112; original action retained for recovery.
"""
import bpy,json
from pathlib import Path
Q=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/Shots/S01-S02');s=bpy.context.scene;c=s.camera;ad=c.animation_data
assert not c.get('frame95_entry_retime',False)
old=ad.action;slotid=ad.action_slot.identifier;old.use_fake_user=True
def curves(action,slot):return [fc for l in action.layers for st in l.strips for bag in st.channelbags if bag.slot_handle==slot.handle for fc in bag.fcurves]
source={ (fc.data_path,fc.array_index):fc for fc in curves(old,ad.action_slot)}
new=old.copy();new.name='S01-S02 camera frame95 entry v004';ad.action=new;ad.action_slot=next(slot for slot in new.slots if slot.identifier==slotid)
def smooth(t):t=max(0,min(1,t));return t*t*(3-2*t)
def warp(f):
 if f<=89 or f>=112:return float(f)
 return f+2*(smooth((f-89)/6) if f<=95 else 1-smooth((f-95)/17))
mapping={f:warp(f) for f in range(89,113)}
for fc in curves(new,ad.action_slot):
 src=source[(fc.data_path,fc.array_index)]
 for p in fc.keyframe_points:
  f=round(p.co.x)
  if f in mapping:p.co.y=src.evaluate(mapping[f])
 fc.update()
c['frame95_entry_retime']=True;c['entry_original_action']=old.name;c['entry_retime_scope']='Only89–112; up to2f advance, first rock-interior95; source timing restored by112, later reveal unchanged.'
s.frame_set(95)
(Q/'Notes/entry_v004_retime.json').write_text(json.dumps({'original_action':old.name,'new_action':new.name,'mapping':mapping,'first_rock_frame':95,'source_frame_at95':warp(95),'source_timing_restored':112,'lens':'Unchanged26mm in affected interval','owner_authority':'User steering: cave view only begins around95 at pipe-to-earth transition.'},indent=2))
result={'frame95_camera_position':list(c.matrix_world.translation),'source_time_at95':warp(95),'original_timing_from112':True}
