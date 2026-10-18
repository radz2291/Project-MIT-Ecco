"""Reusable strict saved-scene packet verification, no rendering or file save.

verify_packet(event, objects=None) may run in a combined consumer. It checks all
three fronts separately across saved frames, actual cap/reference hold through
the final trailing return, first wall contact and finite curve envelopes. Wall
and cap are static during a packet; acquisition timing remains illustrative.
"""
import bpy,math
from mathutils import Vector
from acoustic_event_v002 import validate_event,validate_native_event,native_instance,wall_tree

def verify_packet(event,objects=None,frames=None,fps=None,tolerance=2e-5):
 s=bpy.context.scene;fps=fps or s.render.fps;frames=frames or range(s.frame_start,s.frame_end+1);old=s.frame_current;checks=[];details=[]
 def check(name,p,detail=None):checks.append(dict(name=name,passed=bool(p),detail=detail))
 check('complete strict event/source metadata',validate_event(event))
 s.frame_set(round(event['send_s']*fps)+1);bpy.context.view_layer.update();check('actual native cap/wall/hash/offset re-sampling',validate_native_event(event))
 ref,refpose=native_instance(event['emitter_ref']);cap,capmatrix=native_instance(event['emitter_surface']['object']);wall,wallmatrix,tree=wall_tree(event['wall_source']['object'])
 src=Vector(event['emitter_world_m']);hit=Vector(event['hit_world_m']);direction=Vector(event['direction_world']);distance=(hit-src).length
 if objects is None:objects={o.name:o for o in s.objects if o.name.startswith(event['event_id']+'_ACOUSTICS_')}
 else:objects={o.name:o for o in objects.values()}
 arcs={}
 for role in ['SEND','RETURN']:
  found=[o for o in objects.values() if '_'+role+'_' in o.name]
  check('exactly three '+role+' objects',len(found)==3,[o.name for o in found])
  for i in range(1,4):
   matches=[o for o in found if o.name.endswith('_'+role+'_%02d'%i)]
   check(role+' unique front '+str(i),len(matches)==1)
   if len(matches)==1:arcs[(role,i)]=matches[0]
 maximum_envelope_penetration=0;minimum_cap_margin=1;maximum_ref_motion=0;maximum_cap_motion=0;maximum_wall_motion=0
 states={k:dict(visible_frames=[],max_position_error_m=0,max_visible_world_error_m=0,wrong_visibility_frames=[],active_scale_max=0) for k in arcs}
 # Hidden viewport objects may retain stale matrix_world in Blender. Check their
 # saved position channels directly, and evaluated matrices for visible fronts.
 channels={}
 for key,ob in arcs.items():
  curves=[fc for layer in ob.animation_data.action.layers for strip in layer.strips for bag in strip.channelbags for fc in bag.fcurves]
  channels[key]={fc.array_index:fc for fc in curves if fc.data_path=='location'}
 for f in frames:
  s.frame_set(f);bpy.context.view_layer.update();t=(f-1)/fps
  if event['send_s']<=t<=event['hold_emitter_until_s']:
   _,pose=native_instance(event['emitter_ref']);_,cp=native_instance(event['emitter_surface']['object']);_,wp=native_instance(event['wall_source']['object'])
   maximum_ref_motion=max(maximum_ref_motion,max(abs(pose[r][c]-refpose[r][c]) for r in range(4) for c in range(4)))
   maximum_cap_motion=max(maximum_cap_motion,max(abs(cp[r][c]-capmatrix[r][c]) for r in range(4) for c in range(4)))
   maximum_wall_motion=max(maximum_wall_motion,max(abs(wp[r][c]-wallmatrix[r][c]) for r in range(4) for c in range(4)))
  for (role,i),ob in arcs.items():
   phase=event['arc_phases'][i-1];start=phase['send_s'] if role=='SEND' else phase['contact_s'];end=phase['contact_s'] if role=='SEND' else phase['receive_s'];u=max(0,min(1,(t-start)/(end-start)));expected=src+direction*(distance*u) if role=='SEND' else hit-direction*(distance*u)
   state=states[(role,i)];saved=Vector([channels[(role,i)][j].evaluate(f) for j in range(3)]);state['max_position_error_m']=max(state['max_position_error_m'],(saved-expected).length)
   should_be_visible=start<=t<end and event['visible'] and event['opacity']>.001
   if bool(not ob.hide_render)!=bool(should_be_visible):state['wrong_visibility_frames'].append(f)
   if ob.hide_render:continue
   state['visible_frames'].append(f);state['active_scale_max']=max(state['active_scale_max'],max(ob.scale));state['max_visible_world_error_m']=max(state['max_visible_world_error_m'],(ob.matrix_world.translation-expected).length)
   ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=ev.to_mesh()
   for v in mesh.vertices:
    p=ob.matrix_world@v.co;delta=p-src;minimum_cap_margin=min(minimum_cap_margin,delta.dot(direction))
    if delta.length<1e-8:continue
    wh,_,_,dist=tree.ray_cast(src,delta.normalized(),10)
    if wh is not None:maximum_envelope_penetration=max(maximum_envelope_penetration,delta.length-dist)
   ev.to_mesh_clear()
 for key,state in states.items():
  label=key[0]+' front '+str(key[1]);check(label+' has actual nondegenerate visible progression',len(state['visible_frames'])>=2 and state['active_scale_max']>.2,state)
  check(label+' phase visibility matches declared per-front interval',not state['wrong_visibility_frames'],state['wrong_visibility_frames'])
  check(label+' sampled source/contact/return positions match phase',state['max_position_error_m']<tolerance,state['max_position_error_m'])
  check(label+' visible evaluated world position matches phase',state['max_visible_world_error_m']<tolerance,state['max_visible_world_error_m'])
  details.append(dict(role=key[0],arc_index=key[1],**state))
 check('reference held through final return packet',maximum_ref_motion<3e-6,maximum_ref_motion)
 check('actual native cap held through final return packet',maximum_cap_motion<3e-6,maximum_cap_motion)
 check('sampled wall fixed through packet',maximum_wall_motion<3e-6,maximum_wall_motion)
 check('all finite arc envelopes within first native wall',maximum_envelope_penetration<tolerance,maximum_envelope_penetration)
 check('all finite arc envelopes outside native cap exit plane',minimum_cap_margin>=-tolerance,minimum_cap_margin)
 s.frame_set(old)
 return dict(event_id=event['event_id'],checks=checks,all_pass=all(x['passed'] for x in checks),per_arc=details,max_envelope_penetration_m=maximum_envelope_penetration,min_cap_margin_m=minimum_cap_margin,scope='saved-frame native geometric/phase checks; not calibrated acoustics or human acceptance')
