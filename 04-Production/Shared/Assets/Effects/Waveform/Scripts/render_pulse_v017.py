"""Budget-guarded native master orbit and maximum-density benchmark."""
import bpy,time,json,sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from pulse_graph import set_input,param
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');B=R/'04-Production/Shared/Assets/Effects/Waveform';P=R/'04-Production/Shared/Demos/Previews/Waveform_v017';frames=P/'Frames';frames.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(R/'04-Production/Shared/Demos/Waveform_demo_v017.blend'),use_scripts=False,load_ui=False)
s=bpy.data.scenes['01 Approved360'];bpy.context.window.scene=s;o=next(o for o in s.objects if o.name.endswith(' PULSE'));m=o.modifiers[0]
rows=[]
def render(f,path,label):
 t=time.perf_counter();s.frame_set(f);s.render.filepath=str(path);bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t;rows.append({'label':label,'frame':f,'seconds':dt});(B/'Render_verification_v017.json').write_text(json.dumps({'settings':{'engine':'WORKBENCH','resolution':[1280,720],'AA':8,'fps':24},'rows':rows},indent=2));assert dt<5,('Render cap failed',dt)
# Deliberately overlapping 5-pulse17-strand send/return, beyond approved default load.
set_input(m,'Pulse count override',5);set_input(m,'Strand count override',17);set_input(m,'Reflection after tail',False);set_input(m,'Reflection delay',0.)
render(36,P/'heaviest_frame036.png','maximum density overlap')
for name,val in [('Pulse count override',0),('Strand count override',0),('Reflection after tail',True),('Reflection delay',2.)]:set_input(m,name,val)
render(18,P/'default_benchmark.png','approved default')
for f in range(1,193):render(f,frames/f'frame_{f:04}.png','approved orbit')
print('ORBIT17_DONE',len(rows),max(r['seconds'] for r in rows))
