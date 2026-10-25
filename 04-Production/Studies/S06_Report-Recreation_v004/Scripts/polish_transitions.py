"""Scoped motion/fade polish from the reviewed v004 animation; source untouched."""
import bpy,json,math,hashlib
import numpy as np
from pathlib import Path
from mathutils import Vector,Quaternion
from bpy_extras.object_utils import world_to_camera_view
B=Path(__file__).resolve().parents[1];source=B/'Scenes/S06_cinematic-study_v004.blend'
bpy.ops.wm.open_mainfile(filepath=str(source));s=bpy.context.scene;cam=s.camera
def ease(x):
 x=max(0,min(1,x));return x*x*x*(x*(x*6-15)+10)
def span(f,a,b):return ease((f-a)/(b-a))
def gauss(a,sigma=7):
 k=np.arange(-24,25);w=np.exp(-.5*(k/sigma)**2);w/=w.sum();p=np.pad(a,((24,24),(0,0)),mode='edge');return np.array([np.sum(p[i:i+49]*w[:,None],axis=0) for i in range(len(a))])
old=[]
for f in range(1,289):
 s.frame_set(f);old.append({'frame':f,'camera':list(cam.location),'quaternion':list(cam.rotation_quaternion),'lens':cam.data.lens})
pos=np.array([x['camera'] for x in old]);quat=np.array([x['quaternion'] for x in old])
for i in range(1,288):
 if quat[i]@quat[i-1]<0:quat[i]*=-1
smoothpos=gauss(pos);smoothq=gauss(quat);smoothq/=np.linalg.norm(smoothq,axis=1)[:,None]
cam.animation_data_clear();cam.data.animation_data_clear()
endpos=Vector(pos[-1]);endq=Quaternion(quat[-1]);front=Vector((0,1,0)).to_track_quat('-Z','Y')
field=np.load(B/'Data/story_field.npz');R=float(field['R']);H=float(field['H'])
screen=bpy.data.objects['Laptop screen contents'];s.frame_set(288);bpy.context.view_layer.update();reportcenter=screen.matrix_world@Vector((.745,-.055,.70))
endtarget=Vector((0,.12,1.09));score=[]
for f in range(1,289):
 w=span(f,58,82);loc=Vector(pos[f-1]).lerp(Vector(smoothpos[f-1]),w);rot=Quaternion(quat[f-1]).slerp(Quaternion(smoothq[f-1]),w);lens=float(old[f-1]['lens'])
 if f>=176:
  u=span(f,208,236);center=Vector(((math.tau*R+.565)/2,-R,0)).lerp(reportcenter,u)
  center=center.lerp(endtarget,span(f,232,282))
  aq=front.slerp(endq,span(f,204,280));alens=48-2*span(f,200,244)
  height=H*(1-u)+1.06*u
  # Apparent height decreases steadily; no surge as the map shrinks in world space.
  fraction=.85-.30*span(f,212,280)
  distance=height*alens/(36*(720/1280)*fraction)
  aloc=center+(aq@Vector((0,0,1)))*distance
  settle=span(f,246,288);aloc=aloc.lerp(endpos,settle);aq=aq.slerp(endq,settle)
  handoff=span(f,176,204);loc=loc.lerp(aloc,handoff);rot=rot.slerp(aq,handoff);lens=lens*(1-handoff)+alens*handoff
 cam.location=loc;cam.rotation_quaternion=rot;cam.data.lens=lens;cam.data.shift_x=0;cam.data.shift_y=0
 cam.keyframe_insert('location',frame=f);cam.keyframe_insert('rotation_quaternion',frame=f);cam.data.keyframe_insert('lens',frame=f)
 score.append({'frame':f,'camera':list(loc),'quaternion':list(rot),'lens':lens})
# Keep screen text and engineering graphics intact. Stagger the environment arrival.
groups={'paper':set(),'graphics':set(),'hardware':set(),'environment':set()}
for o in s.objects:
 if o.type not in ('MESH','CURVE','FONT'):continue
 if o.name in ('Screen paper',) or (o.parent==screen and o.name.startswith('Screen ') and o.type=='MESH'):g='paper'
 elif o.parent==screen and o.name!='Thin screen bezel':g='graphics'
 elif o.name in ('Desk','Office wall'):g='environment'
 elif o.name.startswith(('Laptop','Thin screen','Keyboard','Key','Spacebar','Trackpad','Hinge')):g='hardware'
 else:continue
 for m in o.data.materials:
  if m and m.use_nodes and m.node_tree.nodes.get('SHOT_VISIBILITY'):groups[g].add(m)
# Ensure every original C material is assigned, including low-level keyboard names.
for m in bpy.data.materials:
 if m.name in ('Laptop graphite','Screen bezel','Keyboard','Keyboard markings'):groups['hardware'].add(m)
schedule={'paper':(228,242),'graphics':(232,246),'hardware':(234,250),'environment':(238,258)}
assigned=set()
for g in ('paper','graphics','hardware','environment'):
 for m in groups[g]-assigned:
  assigned.add(m);sock=m.node_tree.nodes['SHOT_VISIBILITY'].inputs[0]
  for f in range(1,289):sock.default_value=span(f,*schedule[g]);sock.keyframe_insert('default_value',frame=f)
# Clear the reconstruction guides before map docking. They do not share the
# report shape key; leaving them visible produced an offset ghost rectangle.
decor=[o for o in s.objects if (o.type=='CURVE' and o.name.startswith('A ')) or o.name.startswith(('A | indexed reconstruction','B | amplitude samples','Amplitude edge'))]
dm={m for o in decor for m in o.data.materials if m}
for m in dm:
 sock=m.node_tree.nodes.get('SHOT_VISIBILITY')
 if not sock:continue
 sock=sock.inputs[0]
 for f in range(192,289):
  sock.default_value=1-span(f,196,208);sock.keyframe_insert('default_value',frame=f)
steel=bpy.data.materials.get('Review steel | source mesh unchanged')
if steel:steel.surface_render_method='DITHERED'
for f,samples in [(1,16),(90,32),(145,16),(228,48),(259,16)]:
 s.eevee.taa_render_samples=samples;s.eevee.keyframe_insert('taa_render_samples',frame=f)
for action in bpy.data.actions:
 for layer in action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for fc in bag.fcurves:
     for k in fc.keyframe_points:k.interpolation='CONSTANT' if fc.data_path=='hide_render' or fc.data_path.endswith('taa_render_samples') else 'LINEAR'
s['transition_polish']='Gaussian-smoothed source path; map-size-following camera handoff; staged screen/laptop arrival. Geometry and 12-second timeline retained.'
s.frame_set(1);bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(B/'Scenes/S06_cinematic-study_v004_polished.blend'))
def metrics(a):
 p=np.array([v['camera'] for v in a]);q=np.array([v['quaternion'] for v in a]);ang=2*np.arccos(np.clip(abs((q[1:]*q[:-1]).sum(1)),0,1))*180/math.pi
 return {'max_position_second_difference':float(np.linalg.norm(np.diff(p,n=2,axis=0),axis=1).max()),'max_rotation_step_degrees':float(ang.max()),'BC_max_position_step':float(np.linalg.norm(np.diff(p[196:252],axis=0),axis=1).max())}
record={'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'source_preserved':True,'before':metrics(old),'after':metrics(score),'fade_schedule':schedule,'materials_by_group':{g:sorted(m.name for m in ms) for g,ms in groups.items()},'changes':['Smooth automatic framing distance corrections','Camera follows changing map size during report handoff','Clear non-docking reconstruction guides before map transfer','Report paper, graphics, laptop, environment reveal in order'],'preserved':['Geometry','Field colors and sample IDs','Opening and report-match shape animation','Source hardware','Duration and final camera frame']}
(B/'Records/polish-build.json').write_text(json.dumps(record,indent=2));(B/'Records/polish-camera-score.json').write_text(json.dumps(score));print(json.dumps(record,indent=2))
