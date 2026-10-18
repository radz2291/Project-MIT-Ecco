"""P01 read-only saved-file inventory. Run with isolated background Blender; never save scenes."""
import bpy, json, hashlib, pathlib, datetime
ROOT = pathlib.Path(__file__).resolve().parents[5]
OUT = ROOT / '04-Production/Records/Tasks/T-042/Evidence/asset-inspection_v001.json'
PATHS = [
 'Shared/Assets/ECCO/ECCO_master_temporary-plugs_v002.blend',
 'Shared/Assets/WellAssembly/WellAssembly_variants_v003.blend',
 'Mechanisms/B201/Scenes/B201_pulse-echo_v005.blend',
 'Mechanisms/B201/Scenes/B201_pulse-echo_refinement_v006.blend',
 'Mechanisms/B202/Scenes/B202_measured-envelope_master_v009.blend',
 'Mechanisms/B202/Scenes/B202-M_motion-revision_v007b.blend',
 'Mechanisms/B203/Scenes/B203_retrieval_v002.blend',
 'Mechanisms/B203/Scenes/B203_support_v002.blend',
 'Mechanisms/B203/Scenes/B203_channel_v002.blend',
 'Mechanisms/B203/Scenes/B203_wear_v002.blend',
 'Mechanisms/B204/Scenes/B204_hydraulic-proof_v001.blend',
]
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
 return h.hexdigest()
def value(v):
 if isinstance(v,(str,int,float,bool)):return v
 try:return list(v)
 except Exception:return str(v)
records=[]
for rel in PATHS:
 p=ROOT/'04-Production'/rel
 rec={'path':p.relative_to(ROOT).as_posix(),'exists':p.exists()}
 if p.exists():
  before=sha(p)
  try:
   bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False,use_scripts=False)
   s=bpy.context.scene
   rec.update({'opened':True,'bytes':p.stat().st_size,'sha256':before,
    'units':{'system':s.unit_settings.system,'scale_length':s.unit_settings.scale_length},
    'render':{'engine':s.render.engine,'x':s.render.resolution_x,'y':s.render.resolution_y,'percentage':s.render.resolution_percentage,'fps':s.render.fps,'fps_base':s.render.fps_base},
    'frames':[s.frame_start,s.frame_end],'object_count':len(bpy.data.objects),
    'collections':[c.name for c in bpy.data.collections if not c.library],
    'controls':[{'name':o.name,'type':o.type,'properties':{k:value(o[k]) for k in o.keys() if k!='_RNA_UI'}} for o in bpy.data.objects if o.type=='EMPTY' and ('CONTROL' in o.name or o.name in ['ECCO_ROOT','ECCO_ROTATION_X'] or 'SENSOR_REF_' in o.name)],
    'libraries':[{'path':l.filepath,'exists':pathlib.Path(bpy.path.abspath(l.filepath)).exists()} for l in bpy.data.libraries],
    'missing_images':[i.filepath for i in bpy.data.images if i.source=='FILE' and not i.packed_file and i.filepath and not pathlib.Path(bpy.path.abspath(i.filepath,library=i.library)).exists()],
    'source_unchanged':before==sha(p)})
  except Exception as e:rec.update({'opened':False,'error':str(e)})
 records.append(rec)
 OUT.parent.mkdir(parents=True,exist_ok=True)
 OUT.write_text(json.dumps({'time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'blender':bpy.app.version_string,'method':'isolated background; scripts disabled; no save or render','assets':records},indent=2),encoding='utf-8')
 print('P01_INSPECT',rel,rec.get('opened'),flush=True)
