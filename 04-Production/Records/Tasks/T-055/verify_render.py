import bpy,json,time,sys,hashlib
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[4];T=Path(__file__).resolve().parent;A=R/'04-Production/Shared/Assets'
mode=sys.argv[-1];records=[]
for sid in ['S01','S02']:
 p=T/'Consumers'/f'{sid}_shared-descent_v001.blend';bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False);s=bpy.context.scene
 libs=[{'raw':l.filepath,'exists':Path(bpy.path.abspath(l.filepath)).is_file()} for l in bpy.data.libraries]
 assert all(l['exists'] and l['raw'].startswith('//') for l in libs)
 record={'candidate':str(p.relative_to(R)),'libraries':libs,'camera_samples':[]}
 for f in [1,60,90,120,180,220,240]+([241,264,528] if sid=='S02' else []):
  s.frame_set(f);record['camera_samples'].append({'frame':f,'camera_z':s.camera.matrix_world.translation.z,'lens':s.camera.data.lens})
 records.append(record)
 if mode=='render' and sid=='S02':
  s.render.engine='BLENDER_WORKBENCH';s.render.resolution_x=640;s.render.resolution_y=360;s.render.resolution_percentage=100;s.display.render_aa='32';s.render.image_settings.file_format='PNG'
  for f in [1,90,240,264]:
   s.frame_set(f);s.render.filepath=str(T/'Previews'/f'S02_descent_f{f:03}_v001.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);elapsed=time.perf_counter()-t
   record.setdefault('renders',[]).append({'frame':f,'seconds':elapsed,'pass':elapsed<5,'path':s.render.filepath});print('RENDER',f,elapsed,flush=True)
   if elapsed>=5:break
(T/'Evidence'/('render-benchmarks.json' if mode=='render' else 'reopen-verification.json')).write_text(json.dumps(records,indent=2))
print('CHECKED',mode)
