import bpy,time,json
from pathlib import Path
Q=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/Shots/S01-S02');P=Q/'Previews/Waveform-v009';P.mkdir(exist_ok=True)
exec(bpy.data.texts['START HERE — pixel guides'].as_string());m=bpy.app.driver_namespace['ecco_pixel_module'];s=bpy.context.scene;original=s.frame_current;rows=[]
try:
 for f in range(299,337):
  t=time.perf_counter();s.frame_set(f);m.export(P/f'frame_{f:04}.png',1920,1080);dt=time.perf_counter()-t;rows.append({'frame':f,'seconds':dt})
  (Q/'Notes/waveform_v009_render.json').write_text(json.dumps(rows,indent=2))
  if dt>=5:raise RuntimeError('Render cap failed')
finally:s.frame_set(original)
result={'frames':len(rows),'max_seconds':max(x['seconds'] for x in rows)}
