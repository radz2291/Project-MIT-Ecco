import bpy,time,json
from pathlib import Path
D=Path(__file__).resolve().parent;bpy.ops.wm.open_mainfile(filepath=str(D/'Hardware_demo_v001.blend'));s=bpy.context.scene
s.render.resolution_x=640;s.render.resolution_y=360;s.eevee.taa_render_samples=16
c=next(o for o in bpy.data.objects if o.name=='UPHOLE_CONTINUATION_CONTROL' and o.override_library);out=[]
for show in [0,1]:
    c['show']=show;c.update_tag();s.frame_set(1);bpy.context.view_layer.update();s.render.filepath=str(D/f'Hardware_demo_show{show}.png')
    t=time.perf_counter();bpy.ops.render.render(write_still=True);elapsed=time.perf_counter()-t
    out.append({'show':show,'seconds':elapsed,'under_five':elapsed<5,'resolution':[640,360],'samples':16,'output':s.render.filepath});(D/'render-evidence.json').write_text(json.dumps(out,indent=2));print(out[-1],flush=True)
    if elapsed>=5:break
