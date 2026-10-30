import bpy,pathlib,json,time,shutil
R=pathlib.Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');T=R/'04-Production/Records/Tasks/T-056';records=[]
for key,start,end,benches in [('S02',298,324,[305,314]),('S04',71,95,[77,86])]:
 bpy.ops.wm.open_mainfile(filepath=str(T/'Consumers'/(key+'_waveform_shared_v014.blend')));s=bpy.context.scene;s.render.resolution_x=640;s.render.resolution_y=360;s.render.resolution_percentage=100;folder=T/'Previews'/('shared_'+key+'_frames_v014');folder.mkdir(exist_ok=True);times=[];bench=[]
 def render(frame,path):
  s.frame_set(frame);s.render.filepath=str(path);t=time.perf_counter();bpy.ops.render.render(write_still=True);elapsed=time.perf_counter()-t
  if elapsed>=5:raise RuntimeError('Render cap exceeded: '+str(elapsed))
  return elapsed
 for f in benches:bench.append({'frame':f,'full_seconds':render(f,T/'Previews'/('shared_'+key+'_'+str(f)+'_v014.png'))})
 for i,f in enumerate(range(start,end+1)):times.append(render(f,folder/(str(i+1).zfill(4)+'.png')))
 records.append({'consumer':key,'native_frames':[start,end],'fps':24,'frames':len(times),'max_full_seconds':max(times),'mean_full_seconds':sum(times)/len(times),'benchmarks':bench,'folder':str(folder)})
 (T/'shared-consumer-render_v014.json').write_text(json.dumps(records,indent=2))
print('CONSUMER_BATCH_COMPLETE',json.dumps(records))
