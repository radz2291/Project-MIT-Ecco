"""Bounded composition / coherent-passage illustration. Not CFD."""
import bpy,math,json,time,hashlib,random
from pathlib import Path
from mathutils import Vector,Quaternion
from mathutils.bvhtree import BVHTree
B=Path(__file__).resolve().parents[1];s=bpy.context.scene
OUT=B/'Scenes/S05_focused-interaction_v006.blend'
if Path(bpy.data.filepath).parent.parent!=B:
 assert Path(bpy.data.filepath).parent.parent.name=='Interaction-Proof_v005'
 assert not OUT.exists(), 'Use a new version; preserve existing candidate'
 bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
assert Path(bpy.data.filepath).parent.parent==B
assert bpy.data.collections.get('S05_FOCUSED_PASSAGE_v006') is None, 'Already built'
bpy.data.collections['S05_READABLE_FLOW_v005'].hide_render=True
bpy.data.collections['S05_READABLE_FLOW_v005'].hide_viewport=True
for name in ['S05_Title','S05_Mode','S05_Note']:bpy.data.objects[name].hide_render=True
s.frame_set(1);bpy.context.view_layer.update()
vv=[];ff=[]
for o in bpy.data.collections['S05_LINKED_HARDWARE'].objects:
 off=len(vv);vv.extend(o.matrix_world@v.co for v in o.data.vertices);ff.extend([[off+i for i in p.vertices] for p in o.data.polygons])
tree=BVHTree.FromPolygons(vv,ff);R=.155575;OMEGA=-math.radians(5)
routes=json.loads((B.parent/'Interaction-Proof_v004/Records/planned-routes.json').read_text())
def linear(idblock):
 if idblock.animation_data and idblock.animation_data.action:
  for layer in idblock.animation_data.action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for fc in bag.fcurves:
      for k in fc.keyframe_points:k.interpolation='LINEAR'
def smooth(x):
 x=max(0,min(1,x));return x*x*(3-2*x)
def influence(z):return .32+.43*smooth((z+.15)/.23)*(1-smooth((z-.65)/.25))
def route(z):
 x=max(0,min(129.999,(z+.3)*100));i=int(x);return routes[2][i]*(1-x+i)+routes[2][i+1]*(x-i)
def surface(z,a):
 u=Vector((math.cos(a),math.sin(a),0));h=tree.ray_cast(Vector((0,0,z))+u*.18,-u,.18)[0]
 return math.hypot(h.x,h.y) if h else .105
def frame_at(z,t):
 a=route(z)+OMEGA*t*influence(z);local=a-OMEGA*t
 rs=max(surface(z+dz,local+da) for dz in [-.008,0,.008] for da in [-.10,0,.10])
 lo=rs+.0035;hi=R-.0035;r=(lo+hi)/2
 radial=min(.007,(hi-lo)/2);assert radial>.001,(z,t,radial)
 tangential=.009
 u=Vector((math.cos(a),math.sin(a),0));v=Vector((-math.sin(a),math.cos(a),0))
 return Vector((r*u.x,r*u.y,z)),u,v,radial,tangential
fx=bpy.data.collections.new('S05_FOCUSED_PASSAGE_v006');s.collection.children.link(fx)
mat=bpy.data.materials.new('S05_v006_AmberVolume');mat.use_nodes=True;n=mat.node_tree.nodes;n.clear();l=mat.node_tree.links
out=n.new('ShaderNodeOutputMaterial');vol=n.new('ShaderNodeVolumePrincipled');vol.inputs['Color'].default_value=(.64,.32,.075,1);vol.inputs['Anisotropy'].default_value=.15
vol.inputs['Emission Color'].default_value=(.64,.28,.04,1);vol.inputs['Emission Strength'].default_value=.015
l.new(vol.outputs['Volume'],out.inputs['Volume'])
coord=n.new('ShaderNodeNewGeometry');shift=n.new('ShaderNodeVectorMath');shift.operation='SUBTRACT';l.new(coord.outputs['Position'],shift.inputs[0])
for f in [1,72]:
 shift.inputs[1].default_value=(0,0,.20*(f-1)/24);shift.inputs[1].keyframe_insert('default_value',frame=f)
scale=n.new('ShaderNodeVectorMath');scale.operation='MULTIPLY';scale.inputs[1].default_value=(65,65,32);l.new(shift.outputs[0],scale.inputs[0])
noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=1;noise.inputs['Detail'].default_value=2;l.new(scale.outputs[0],noise.inputs['Vector'])
ramp=n.new('ShaderNodeMapRange');ramp.inputs['From Min'].default_value=.28;ramp.inputs['From Max'].default_value=.70;ramp.inputs['To Min'].default_value=2;ramp.inputs['To Max'].default_value=100;l.new(noise.outputs['Fac'],ramp.inputs['Value']);l.new(ramp.outputs['Result'],vol.inputs['Density']);linear(mat.node_tree)
NR=161;SIDES=16;Z0=-.08;Z1=.68
states=[]
for f in range(1,73):
 t=(f-1)/24;verts=[]
 for j in range(NR):
  z=Z0+(Z1-Z0)*j/(NR-1);p,u,v,rr,rt=frame_at(z,t)
  edge=.06+.94*min(smooth((z-Z0)/.06),smooth((Z1-z)/.06))
  for k in range(SIDES):
   q=math.tau*k/SIDES;verts.append(p+edge*(rr*math.cos(q)*u+rt*math.sin(q)*v))
 states.append(verts)
faces=[(j*SIDES+k,j*SIDES+(k+1)%SIDES,(j+1)*SIDES+(k+1)%SIDES,(j+1)*SIDES+k) for j in range(NR-1) for k in range(SIDES)]
faces.extend([tuple(reversed(range(SIDES))),tuple((NR-1)*SIDES+k for k in range(SIDES))])
me=bpy.data.meshes.new('S05_v006_FiniteFluidPassage');me.from_pydata(states[0],[],faces);me.materials.append(mat)
o=bpy.data.objects.new('S05_v006_MovingFluidVolume',me);fx.objects.link(o);o['meaning']='Selected coherent fluid passage; moving density is explanatory, not CFD. Finite volume remains outside steel.'
o.shape_key_add(name='Basis');me.shape_keys.use_relative=False
for f,verts in enumerate(states[1:],2):
 key=o.shape_key_add(name=f'Frame_{f:03}')
 for v,co in zip(key.data,verts):v.co=co
for key in me.shape_keys.key_blocks:key.interpolation='KEY_LINEAR'
for f in [1,72]:me.shape_keys.eval_time=(f-1)*10;me.shape_keys.keyframe_insert('eval_time',frame=f)
linear(me.shape_keys)
rocksource=bpy.data.objects['S05_v005_Rock_54'];random.seed(6006);tracks=[]
for i,zstart in enumerate([-.28,-.12,.045,.215,.385]):
 rock=rocksource.copy();rock.data=rocksource.data.copy();rock.animation_data_clear();rock.name=f'S05_v006_CarriedCutting_{i:02}';fx.objects.link(rock);rock.hide_render=False;rock.hide_viewport=False;rock.parent=None
 radius=.0038 if i%2 else .0045;fac=radius/max(v.co.length for v in rock.data.vertices)
 for v in rock.data.vertices:v.co*=fac
 heads=[]
 for f in range(1,73):
  t=(f-1)/24;z=zstart+.20*t;p,u,v,rr,rt=frame_at(z,t)
  rock.location=p;rock.rotation_euler=(.37*t+i,.24*t,-.3*t+i*.7)
  edge=min(smooth((z-Z0)/.04),smooth((Z1-z)/.04));rock.scale=(edge,)*3
  for prop in ['location','rotation_euler','scale']:rock.keyframe_insert(prop,frame=f)
  heads.append(list(p))
 linear(rock);tracks.append({'name':rock.name,'max_support_radius_m':radius,'heads':heads})
cam=s.camera;cam.animation_data_clear();cam.rotation_mode='QUATERNION';cam.location=(.95,.95,.43);cam.rotation_quaternion=(Vector((.025,.025,.30))-cam.location).to_track_quat('-Z','Y')@Quaternion((0,0,1),math.radians(-55));cam.data.lens=49
bpy.data.objects['S05_FixedHalfBorehole'].rotation_euler.z=math.radians(25)
s.frame_end=72;s['proof_scope']='v006 three-second single-passage composition; illustrative density advection and rotation-aware finite fluid volume; not CFD'
s.frame_set(36);bpy.context.view_layer.update();s.render.filepath=str(B/'Previews/composition.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);seconds=time.perf_counter()-t
result={'seconds':seconds,'selected_v004_route':2,'angular_influence_range':[.32,.75],'upward_speed_illustrative_m_s':.20,'domain_z_m':[Z0,Z1],'frames':72,'fps':24,'volume_rings':NR,'camera_stationary':True,'borehole_change':'Only static half-section azimuth rotated +25deg; borehole radii and source hardware unchanged','cuttings':tracks,'camera_location':list(cam.location),'camera_quaternion':list(cam.rotation_quaternion),'lens_mm':cam.data.lens}
(B/'Records/build.json').write_text(json.dumps(result,indent=2));bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
