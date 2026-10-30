import bpy,time,json,sys
from pathlib import Path
T=Path(__file__).resolve().parent
cases=[('S07',90),('S07',170),('S05',240)]
records=[]
for sid,f in cases:
    p=T/'Consumers'/f'{sid}_shared-satin_v001.blend';bpy.ops.wm.open_mainfile(filepath=str(p));s=bpy.context.scene;s.frame_set(f)
    s.render.engine='BLENDER_EEVEE';s.render.resolution_x=640;s.render.resolution_y=360;s.render.resolution_percentage=100;s.eevee.taa_render_samples=8
    s.render.image_settings.file_format='PNG';s.render.filepath=str(T/'Previews'/f'{sid}_satin_f{f:03d}_v001.png')
    t=time.perf_counter();bpy.ops.render.render(write_still=True);elapsed=time.perf_counter()-t
    records.append({'consumer':str(p),'frame':f,'resolution':[640,360],'samples':8,'seconds':elapsed,'passes':elapsed<5,'output':s.render.filepath})
    (T/'Evidence/render-benchmarks.json').write_text(json.dumps(records,indent=2));print('BENCHMARK',records[-1],flush=True)
print('DONE')
