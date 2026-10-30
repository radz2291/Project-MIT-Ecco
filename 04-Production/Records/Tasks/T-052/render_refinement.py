"""Run only under master's render queue grant; no production batches."""
import bpy,time,json
from pathlib import Path
T=Path(__file__).resolve().parent
records=[]
for sid,f in [('S07',90),('S07',170),('S05',240),('S02',360)]:
    p=T/'Consumers'/f'{sid}_shared-satin_v001.blend';bpy.ops.wm.open_mainfile(filepath=str(p));s=bpy.context.scene;s.frame_set(f)
    s.render.engine='BLENDER_EEVEE';s.render.resolution_x=640;s.render.resolution_y=360;s.render.resolution_percentage=100;s.eevee.taa_render_samples=32
    s.render.image_settings.file_format='PNG';s.render.filepath=str(T/'Previews'/f'{sid}_satin_f{f:03d}_v002.png')
    t=time.perf_counter();bpy.ops.render.render(write_still=True);seconds=time.perf_counter()-t
    records.append({'frame':f,'consumer':str(p),'resolution':[640,360],'samples':32,'seconds':seconds,'passes':seconds<5,'output':s.render.filepath})
    (T/'Evidence/render-refinement.json').write_text(json.dumps(records,indent=2));print('BENCHMARK',records[-1],flush=True)
