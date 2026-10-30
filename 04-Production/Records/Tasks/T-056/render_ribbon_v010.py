import bpy,pathlib,time,json,math,sys
T=pathlib.Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/Records/Tasks/T-056');P=T/'Previews/Ribbon_v010';s=bpy.context.scene;records=[]
frames=[300,309,316] if '--batch' not in sys.argv else [298+i/3 for i in range(79)]
for i,f in enumerate(frames):
 s.frame_set(math.floor(f),subframe=f%1);s.render.filepath=str(P/(f'motion_{i:04d}.png' if '--batch' in sys.argv else f'benchmark_{f}.png'));t=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t;records.append({'frame':f,'seconds':dt});(T/('ribbon-batch_v010.json' if '--batch' in sys.argv else 'ribbon-benchmarks_v010.json')).write_text(json.dumps({'camera':s.camera.name,'resolution':[s.render.resolution_x,s.render.resolution_y],'samples':s.eevee.taa_render_samples,'records':records},indent=2))
 if dt>=5:raise RuntimeError('Frame cap exceeded')
