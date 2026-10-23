import bpy,time,json
from pathlib import Path
B=Path(__file__).resolve().parents[1];s=bpy.context.scene;rows=[]
for f,name in [(1,'entry'),(96,'accelerator'),(120,'A_exit'),(121,'B_entry'),(198,'interaction'),(288,'B_exit'),(289,'C_entry'),(312,'diffuser'),(400,'pullback'),(432,'integrated')]:
 s.frame_set(f);s.render.filepath=str(B/'Previews'/('composition_'+name+'.png'));t=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t
 rows.append({'frame':f,'name':name,'complete_render_to_file_seconds':dt})
 assert dt<5,('Budget exceeded',f,dt)
result={'samples':rows,'settings':{'resolution':[1280,720],'fps':24,'engine':s.render.engine,'samples':s.eevee.taa_render_samples},'all_strictly_under_5s':True}
(B/'Records/benchmark.json').write_text(json.dumps(result,indent=2));s.frame_set(198)
