import bpy,pathlib,time,json,sys
T=pathlib.Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/Records/Tasks/T-056');kind='context' if '--context' in sys.argv else 'isolated';P=T/'Previews/Ribbon_v011'/kind;P.mkdir(parents=True,exist_ok=True);s=bpy.context.scene;records=[]
for f in range(1,121):
 s.frame_set(f);s.render.filepath=str(P/f'frame_{f:04d}.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t;records.append({'frame':f,'seconds':dt});(T/f'formation-batch-{kind}_v011.json').write_text(json.dumps({'frames':120,'fps':24,'duration_s':5,'resolution':[s.render.resolution_x,s.render.resolution_y],'samples':s.eevee.taa_render_samples,'records':records},indent=2))
 if dt>=5:raise RuntimeError('STOP: full render exceeded5seconds')
