"""v003: movement-history tails with stronger gentle near-pad entrainment.
Authored kinematic motion only. No source geometry edits or physical solver.
"""
import bpy,math,json,random,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
B=Path(__file__).resolve().parents[1];OLD=B.parent/'Interaction-Proof_v002'
OUT=B/'Scenes/S05_twisted-pad_interaction_v003.blend';s=bpy.context.scene
assert not OUT.exists()
assert Path(bpy.data.filepath).resolve()==(OLD/'Scenes/S05_twisted-pad_interaction_v002.blend').resolve()
assert not bpy.data.is_dirty
s.frame_set(1);bpy.context.view_layer.update()
vv=[];ff=[]
for o in bpy.data.collections['S05_LINKED_HARDWARE'].objects:
 off=len(vv);vv.extend(o.matrix_world@v.co for v in o.data.vertices);ff.extend([[off+i for i in p.vertices] for p in o.data.polygons])
tree=BVHTree.FromPolygons(vv,ff);OMEGA=-math.radians(5);R=.155575
src=(OLD/'Scripts/revise.py').read_text()
exec(src[src.index('def rot('):src.index('random.seed(123)')].replace('OMEGA*.3*w','OMEGA*.65*w').replace('3.0*angular_delta','2.4*angular_delta'))
particles=json.loads((OLD/'Records/particle-tracks.json').read_text())
DT=1/120;START=-840;END=715
for p in particles:
 z=-.28+p['phase']*1.2;a=base(z)+p['lane']+OMEGA*(START*DT)*influence(z)
 p['pos']=constrain(Vector((.137*math.cos(a),.137*math.sin(a),z)),START*DT,p['r'])
 p['velocity']=velocity(p['pos'],START*DT,p['lane'],p['r'])
 p['history']=[p['pos'].copy()];p['generation']=[0];p['gen']=0
for step in range(START,END):
 t=step*DT
 for p in particles:
  wanted=velocity(p['pos'],t,p['lane'],p['r'])
  p['velocity']=p['velocity'].lerp(wanted,1-math.exp(-DT/.12))
  p['pos']=constrain(p['pos']+p['velocity']*DT,t+DT,p['r'])
  if p['pos'].z>.98:
   a=math.radians(16)+p['lane'];p['pos']=Vector((.137*math.cos(a),.137*math.sin(a),-.30));p['gen']+=1;p['velocity']=velocity(p['pos'],t+DT,p['lane'],p['r'])
  p['history'].append(p['pos'].copy());p['generation'].append(p['gen'])
# Save to successor only after trajectory construction succeeds.
bpy.ops.wm.save_as_mainfile(filepath=str(OUT));s.name='S05_Hydraulic_Interaction_v003'
for name in ['S05_DYNAMIC_FLOW_v002','S05_MOVING_TAPERED_TAILS_v002']:
 bpy.data.collections[name].hide_render=True;bpy.data.collections[name].hide_viewport=True
fx=bpy.data.collections.new('S05_HISTORY_FLOW_v003');s.collection.children.link(fx)
mat=bpy.data.materials['S05_v002_AmberFluid'];NR=41;SIDES=6
def linear(idblock):
 if idblock.animation_data and idblock.animation_data.action:
  for layer in idblock.animation_data.action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for fc in bag.fcurves:
      for k in fc.keyframe_points:k.interpolation='LINEAR'
def point_at(p,index):
 a=max(0,min(len(p['history'])-2,int(index)));return p['history'][a].lerp(p['history'][a+1],max(0,min(1,index-a)))
def clearance(pt,t):
 q=rot(pt,-OMEGA*t);rr=math.hypot(q.x,q.y);u=Vector((q.x/rr,q.y/rr,0))
 hit=tree.ray_cast(Vector((0,0,q.z))+u*.18,-u,.18)[0]
 radial=rr-math.hypot(hit.x,hit.y) if hit else 1
 return min(tree.find_nearest(q)[3],radial,R-rr)
summary=[];track_record=[]
for i,p in enumerate(particles):
 radius=.00115 if p['kind']=='fluid' else .00062
 age=.85 if p['kind']=='fluid' else .55
 maxsteps=age/DT;safe=[]
 # Historical trails can be caught by later moving steel. Shorten before that
 # happens instead of bending old samples into a new arbitrary path.
 for f in range(1,145):
  idx=(f-1)*5-START;t=(f-1)/24;limit=maxsteps
  for k in range(1,int(maxsteps)+1):
   q=p['history'][idx-k]
   if p['generation'][idx-k]!=p['generation'][idx] or clearance(q,t)<radius+.001:
    limit=max(0,k-2);break
  safe.append(limit)
 # A conservative symmetric envelope anticipates shortening, avoiding pops.
 smoothsafe=[]
 for f in range(144):smoothsafe.append(min(safe[g]+abs(f-g)*4 for g in range(max(0,f-9),min(144,f+10))))
 states=[];heads=[]
 for f in range(1,145):
  idx=(f-1)*5-START;t=(f-1)/24;length=smoothsafe[f-1]
  points=[point_at(p,idx-length*j/(NR-1)) for j in range(NR)];heads.append(list(points[0]))
  arr=[]
  for j,pt in enumerate(points):
   tangent=points[min(NR-1,j+1)]-points[max(0,j-1)]
   if tangent.length<1e-7:tangent=Vector((0,0,-1))
   tangent.normalize();u=tangent.cross(Vector((0,0,1)))
   if u.length<.01:u=tangent.cross(Vector((1,0,0)))
   u.normalize();v=tangent.cross(u).normalized()
   edge=min(smooth((pt.z+.30)/.10),smooth((.98-pt.z)/.10),smooth(length/10))
   rr=radius*(.015+.985*(1-j/(NR-1))**.9)*edge
   for k in range(SIDES):arr.append(pt+rr*(u*math.cos(k*math.tau/SIDES)+v*math.sin(k*math.tau/SIDES)))
  states.append(arr)
 faces=[(j*SIDES+k,j*SIDES+(k+1)%SIDES,(j+1)*SIDES+(k+1)%SIDES,(j+1)*SIDES+k) for j in range(NR-1) for k in range(SIDES)]
 me=bpy.data.meshes.new(f'S05_v003_TrailMesh_{i:02}');me.from_pydata(states[0],[],faces);me.materials.append(mat)
 o=bpy.data.objects.new(f'S05_v003_{p["kind"]}_HistoryTail_{i:02}',me);fx.objects.link(o)
 for poly in me.polygons:poly.use_smooth=True
 o.shape_key_add(name='Basis');me.shape_keys.use_relative=False
 for f,verts in enumerate(states[1:],2):
  key=o.shape_key_add(name=f'Frame_{f:03}')
  for v,co in zip(key.data,verts):v.co=co
 for key in me.shape_keys.key_blocks:key.interpolation='KEY_LINEAR'
 for f in [1,144]:me.shape_keys.eval_time=(f-1)*10;me.shape_keys.keyframe_insert('eval_time',frame=f)
 linear(me.shape_keys);o['meaning']='Actual prior positions of this illustrative marker; taper shortens before current moving steel overtakes history. Not parented to hardware.'
 if p['kind']=='rock':
  old=bpy.data.objects[f'S05_v002_Rock_{i:02}'];rock=old.copy();rock.data=old.data.copy();rock.animation_data_clear();rock.name=f'S05_v003_Rock_{i:02}';fx.objects.link(rock)
  for f,pos in enumerate(heads,1):
   t=(f-1)/24;rock.location=pos;rock.rotation_euler=(.16*t+.5*i,.21*t,.25*t+.2*i);edge=min(smooth((pos[2]+.30)/.10),smooth((.98-pos[2])/.10));rock.scale=(edge,)*3
   for prop in ['location','rotation_euler','scale']:rock.keyframe_insert(prop,frame=f)
  linear(rock)
 summary.append({'index':i,'kind':p['kind'],'max_history_seconds':age,'min_visible_history_seconds':min(smoothsafe)*DT,'mean_visible_history_seconds':sum(smoothsafe)/144*DT})
 track_record.append({'index':i,'kind':p['kind'],'heads':heads,'visible_history_steps':smoothsafe})
s.frame_set(72);s.render.filepath='//../Work/Frames/S05_';s['proof_scope']='v003 six-second history-trail test; stronger gentle near-pad entrainment; same camera and hardware rotation; illustrative not CFD'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
result={'tails':summary,'history_sample_rate_hz':120,'velocity_smoothing_seconds':.12,'near_pad_tangential_term':.65,'previous_term':.3,'source_v002_sha256':hashlib.sha256((OLD/'Scenes/S05_twisted-pad_interaction_v002.blend').read_bytes()).hexdigest(),'frames':144,'method':'World-space particle advection with smoothed velocity and actual movement-history trails; safe history-length envelope around current moving steel. No rigid attachment to tool; no physical solver.'}
(B/'Records/build.json').write_text(json.dumps(result,indent=2));(B/'Records/tracks.json').write_text(json.dumps(track_record))
