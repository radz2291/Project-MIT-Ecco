import bpy,pathlib,time,json
T=pathlib.Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/Records/Tasks/T-056');P=T/'Previews/Ribbon_v013/Context';P.mkdir(parents=True,exist_ok=True);s=bpy.context.scene;records=[]
for f in range(1,97):
 s.frame_set(f);s.render.filepath=str(P/f'frame_{f:04d}.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t;records.append({'frame':f,'seconds':dt});(T/'field-batch_v013.json').write_text(json.dumps({'fps':24,'duration_s':4,'resolution':[s.render.resolution_x,s.render.resolution_y],'samples':s.eevee.taa_render_samples,'records':records},indent=2))
 if dt>=5:raise RuntimeError('STOP full render >=5seconds')
