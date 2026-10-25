import bpy,math,json,time
from pathlib import Path
from mathutils import Vector,Quaternion
B=Path(__file__).resolve().parents[1]
for folder in ['Scenes','Records','Previews','Cache']: (B/folder).mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(B.parent/'Sequence_v003/Scenes/S07_Monumental-Precision_v003.blend'))
s=bpy.context.scene;s.frame_set(84);cam=s.camera;focus=bpy.data.objects['Camera focus target'];out=B/'Previews/Survey';out.mkdir(exist_ok=True)
for data in [cam,cam.data,focus]:data.animation_data_clear()
records=[]
for name,x,r,deg,tx,roll in [('rear-sensor',.52,.78,150,.50,-22),('rear-collar',-.25,.72,155,.20,-22)]:
 a=math.radians(deg);p=Vector((x,-r*math.cos(a),r*math.sin(a)));t=Vector((tx,0,0));cam.location=p;cam.rotation_quaternion=(t-p).to_track_quat('-Z','Y')@Quaternion((0,0,1),math.radians(roll));focus.location=t;cam.data.shift_x=0;cam.data.dof.aperture_fstop=12
 s.render.filepath=str(out/(name+'.png'));start=time.perf_counter();bpy.ops.render.render(write_still=True);sec=time.perf_counter()-start;records.append({'name':name,'seconds':sec,'camera':list(p),'target':list(t)});print(name,sec,flush=True)
 if sec>=5:raise RuntimeError('Render cap exceeded')
(B/'Records/survey.json').write_text(json.dumps(records,indent=2))

