"""Camera-only trial: progressively brake descent into first product arrival."""
import bpy,json,bisect,math
from pathlib import Path
from mathutils import Vector
Q=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/Shots/S01-S02')
assert not (Q/'Scenes/S01-S02_production_v008.blend').exists(), 'Preserve existing trial; use a new version'
s=bpy.context.scene;c=s.camera;ad=c.animation_data;old=ad.action;old.use_fake_user=True
slot_id=ad.action_slot.identifier
def curves(action,slot):
 return [fc for l in action.layers for st in l.strips for bag in st.channelbags if bag.slot_handle==slot.handle for fc in bag.fcurves]
source={(fc.data_path,fc.array_index):fc for fc in curves(old,ad.action_slot)}
start,end=141,240
def position(t):return Vector([source[('location',i)].evaluate(t) for i in range(3)])
times=[start+i/8 for i in range((end-start)*8+1)]
distances=[0.]
for a,b in zip(times,times[1:]):distances.append(distances[-1]+(position(b)-position(a)).length)
length=distances[-1]
entry_speed=(position(start)-position(start-1)).length
power=entry_speed*(end-start)/length
assert power>1
def warp(f):
 if f<=start or f>=end:return float(f)
 t=(f-start)/(end-start);distance=length*(1-(1-t)**power)
 j=min(len(times)-1,max(1,bisect.bisect_left(distances,distance)))
 span=distances[j]-distances[j-1]
 return times[j-1]+(times[j]-times[j-1])*((distance-distances[j-1])/span if span else 0)
new=old.copy();new.name='S01-S02 progressive product arrival v008';ad.action=new;ad.action_slot=next(x for x in new.slots if x.identifier==slot_id)
for fc in curves(new,ad.action_slot):
 src=source[(fc.data_path,fc.array_index)]
 for key in fc.keyframe_points:
  f=round(key.co.x)
  if start<f<end:key.co.y=src.evaluate(warp(f))
 fc.update()
new.use_fake_user=True
c['product_arrival_source_action']=old.name
c['product_arrival_scope']='Only camera pose142–239; arc-length braking, same path/endpoints. Lens/effects unchanged. First product close-up trial.'
new_curves={(fc.data_path,fc.array_index):fc for fc in curves(new,ad.action_slot)}
outside=max(abs(fc.evaluate(f)-source[key].evaluate(f)) for key,fc in new_curves.items() for f in list(range(1,start+1))+list(range(end,529)))
assert outside<1e-6
speeds=[]
for f in range(start,end):
 p=Vector([new_curves[('location',i)].evaluate(f) for i in range(3)])
 q=Vector([new_curves[('location',i)].evaluate(f+1) for i in range(3)])
 speeds.append({'frame':f,'old_m_per_frame':(position(f+1)-position(f)).length,'new_m_per_frame':(q-p).length})
s.frame_set(180);bpy.ops.wm.save_as_mainfile(filepath=str(Q/'Scenes/S01-S02_production_v008.blend'),compress=True)
report={'source_action':old.name,'new_action':new.name,'scope':[start,end],'path_length_m':length,'entry_m_per_frame':entry_speed,'ease_power':power,'outside_scope_curve_error':outside,'lens':'unchanged source action','mapping':{f:warp(f) for f in range(start,end+1)},'speeds':speeds,'assumption':'End of descent into first product close-up; end-of-clip pullback unchanged.'}
(Q/'Notes/product_arrival_v008.json').write_text(json.dumps(report,indent=2))
result={k:v for k,v in report.items() if k not in ['mapping','speeds']}
