import bpy,pathlib,time,json,sys,math
ROOT=pathlib.Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');TASK=ROOT/'04-Production/Records/Tasks/T-056';OUT=TASK/'Previews/Pressure_v007';OUT.mkdir(parents=True,exist_ok=True)
s=bpy.context.scene;records=[]
frames=[305.5] if '--bench-all' not in sys.argv else [305.5,310.5,316.5]
if '--batch' in sys.argv:frames=[298+i*.25 for i in range(105)]
for idx,f in enumerate(frames):
 s.frame_set(math.floor(f),subframe=f%1);s.render.filepath=str(OUT/(f'sample_{idx:04d}.png' if '--batch' in sys.argv else f'benchmark_{f:.2f}.png'))
 t=time.perf_counter();bpy.ops.render.render(write_still=True);elapsed=time.perf_counter()-t
 records.append({'native_frame':f,'seconds_full_render_to_file':elapsed})
 (TASK/('pressure-batch_v007.json' if '--batch' in sys.argv else 'pressure-benchmark_v007.json')).write_text(json.dumps({'engine':s.render.engine,'resolution':[s.render.resolution_x,s.render.resolution_y],'samples':s.eevee.taa_render_samples,'records':records},indent=2))
 if elapsed>=5:raise RuntimeError(f'Frame cap exceeded {elapsed}; stopping')
