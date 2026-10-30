import bpy,pathlib,json,time,numpy as np
R=pathlib.Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');T=R/'04-Production/Records/Tasks/T-056';out=[]
files=[('master',R/'04-Production/Shared/Assets/Acoustics/Waveform_shared_v014/Waveform_shared_v014.blend',30,'WF_LIVE_FIELD'),('S02',T/'Consumers/S02_waveform_shared_v014.blend',305,'WF_S02_EVENT_1'),('S04',T/'Consumers/S04_waveform_shared_v014.blend',77,'WF_S04_EVENT_1')]
for name,path,frame,objname in files:
 bpy.ops.wm.open_mainfile(filepath=str(path));s=bpy.context.scene;s.frame_set(frame);bpy.context.view_layer.update();ob=bpy.data.objects[objname];ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());a=np.array([v.co[:] for v in ev.data.vertices]);entry={'name':name,'frame':frame,'vertices':len(a),'extent':np.ptp(a,axis=0).tolist() if len(a) else []};s.render.resolution_x=640;s.render.resolution_y=360;s.render.resolution_percentage=100;s.render.filepath=str(T/'Previews'/('shared_'+name+'_v014.png'));start=time.perf_counter();bpy.ops.render.render(write_still=True);entry['full_render_seconds']=time.perf_counter()-start;entry['image']=s.render.filepath;out.append(entry)
 if entry['full_render_seconds']>=5:break
(T/'shared-benchmarks_v014.json').write_text(json.dumps(out,indent=2));print('BENCHMARKS',json.dumps(out))
