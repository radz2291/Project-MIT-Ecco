import bpy,math,json,time
from pathlib import Path
from mathutils import Vector,Quaternion
from mathutils.bvhtree import BVHTree
B=Path(__file__).resolve().parents[1];s=bpy.context.scene
assert bpy.data.collections.get('S05_INTERNAL_WISPS_v011') is None
OUT=B/'Scenes/S05_trail-scale_v011.blend';assert not OUT.exists();assert Path(bpy.data.filepath).parent.parent.name=='Interaction-Proof_v010'
import hashlib
prior=Path(bpy.data.filepath);prior_hash=hashlib.sha256(prior.read_bytes()).hexdigest()
bpy.ops.wm.save_as_mainfile(filepath=str(OUT));s.name='S05_TrailScale_StillReview_v011'
bpy.data.collections['S05_INTERNAL_WISPS_v010'].hide_render=True;bpy.data.collections['S05_INTERNAL_WISPS_v010'].hide_viewport=True
s.frame_set(1);bpy.context.view_layer.update();vv=[];ff=[]
for o in bpy.data.collections['S05_LINKED_HARDWARE'].objects:
 off=len(vv);vv.extend(o.matrix_world@v.co for v in o.data.vertices);ff.extend([[off+i for i in p.vertices] for p in o.data.polygons])
tree=BVHTree.FromPolygons(vv,ff);R=.155575;OMEGA=-math.radians(5);routes=json.loads((B.parent/'Interaction-Proof_v004/Records/planned-routes.json').read_text());ns=dict(bpy=bpy,math=math,Vector=Vector,tree=tree,R=R,OMEGA=OMEGA,routes=routes)
src=(B.parent/'Interaction-Proof_v006/Scripts/build.py').read_text();exec(src[src.index('def linear('):src.index("fx=bpy.data.collections.new")],ns);linear=ns['linear'];surface=ns['surface'];influence=ns['influence']
def point_at(lane,z,t,side,depth):
 x=max(0,min(129.999,(z+.3)*100));i=int(x);a=routes[lane][i]*(1-x+i)+routes[lane][i+1]*(x-i)+OMEGA*t*influence(z);local=a-OMEGA*t
 rs=max(surface(z+dz,local+da) for dz in [-.008,0,.008] for da in [-.10,0,.10]);lo=rs+.0035;hi=R-.0035;assert lo<hi
 r=(lo+hi)/2+depth;u=Vector((math.cos(a),math.sin(a),0));v=Vector((-math.sin(a),math.cos(a),0))
 return Vector((r*u.x,r*u.y,z))+side*v,u,v
fx=bpy.data.collections.new('S05_INTERNAL_WISPS_v011');s.collection.children.link(fx);m=bpy.data.materials['S05_v008_SoftAmberWisp'];NR=25;SIDES=10;summary=[]
configs=[]
for group,zstart in enumerate([-.19,-.025,.16]):
 for lane,(side,depth,length) in enumerate([(-.004,.0005,.052),(0,.003,.065),(.004,.0045,.046)]):configs.append((2,group,lane,zstart-lane*.004,side,depth,length))
for route in [0,4,16]:
 for group,zstart in enumerate([-.15,.12,.39]):configs.append((route,group,0,zstart,0,.0015,.055))
for route,group,lane,zstart,side,depth,length in configs:
 length*=1.5
 states=[]
 for f in range(1,97):
  t=(f-1)/24;head=zstart+.135*t;verts=[]
  for j in range(NR):
   u01=j/(NR-1);z=head-length*u01;p,u,v=point_at(route,z,t,side,depth);taper=max(.018,math.sin(math.pi*u01)**.8)
   for k in range(SIDES):
    a=math.tau*k/SIDES;verts.append(p+taper*1.35*(.00125*math.cos(a)*u+.0024*math.sin(a)*v))
  states.append(verts)
 faces=[(j*SIDES+k,j*SIDES+(k+1)%SIDES,(j+1)*SIDES+(k+1)%SIDES,(j+1)*SIDES+k) for j in range(NR-1) for k in range(SIDES)]
 faces.extend([tuple(reversed(range(SIDES))),tuple((NR-1)*SIDES+k for k in range(SIDES))]);me=bpy.data.meshes.new(f'S05_v011_WispMesh_{route}_{group}_{lane}');me.from_pydata(states[0],[],faces);me.materials.append(m)
 alpha=me.attributes.new('wisp_opacity','FLOAT','POINT')
 for j in range(NR):
  for k in range(SIDES):alpha.data[j*SIDES+k].value=(.58 if route==2 else .30)*math.sin(math.pi*j/(NR-1))**.65
 o=bpy.data.objects.new(f'S05_v011_Wisp_{route}_{group}_{lane}',me);fx.objects.link(o)
 for p in me.polygons:p.use_smooth=True
 o.shape_key_add(name='Basis');me.shape_keys.use_relative=False
 for f,verts in enumerate(states[1:],2):
  key=o.shape_key_add(name=f'Frame_{f:03}')
  for v,co in zip(key.data,verts):v.co=co
 for key in me.shape_keys.key_blocks:key.interpolation='KEY_LINEAR'
 for f in [1,96]:me.shape_keys.eval_time=(f-1)*10;me.shape_keys.keyframe_insert('eval_time',frame=f)
 linear(me.shape_keys);summary.append({'name':o.name,'v004_route':route,'start_z':zstart,'speed_m_s':.135,'length_m':length})
s.frame_set(48);s.render.filepath=str(B/'Previews/trail-scale_still.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t;assert dt<5
s['proof_scope']='v011 trail width +35 percent, length +50 percent. Still review only; animation render held for owner approval.'
result={'prior_v010_sha256':prior_hash,'width_multiplier':1.35,'length_multiplier':1.5,'still_frame':48,'render_seconds':dt,'wisps':summary,'preserved':['camera and lens shift','fluid volume and material animation','hardware and rotation','rock geometry and trajectories','path centerlines and leading ends','borehole geometry and static cut'],'animation_rendered':False}
(B/'Records/still-build.json').write_text(json.dumps(result,indent=2));s.render.filepath='//../Previews/trail-scale_still.png';bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
