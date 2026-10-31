"""T47 bounded repaired previews/demo. Each launch requires a T45 render grant."""
import bpy,sys,time,json,hashlib,platform
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
T=ROOT/'04-Production/Records/Tasks/T-047';S=T/'Scenes';E=T/'Evidence';P=T/'Previews/v012'
VERSIONS={'WearSection':'v011','LayerSection':'v011','Retrieval':'v008','Support':'v012'}
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
assert len(args)==2,'Explicit mode and granted slot identifier required'
mode,slot=args
if mode=='benchmark-repaired':cases=[('WearSection',[1]),('LayerSection',[1]),('Support',[12,18,56,76])]
elif mode=='demo':cases=[('Retrieval',range(1,97)),('Support',range(1,97))]
else:raise ValueError(mode)
P.mkdir(parents=True,exist_ok=True);rows=[]
for name,frames in cases:
 p=S/('Cased'+name+'_'+VERSIONS[name]+'.blend');native_hash=hashlib.sha256(p.read_bytes()).hexdigest()
 bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False,use_scripts=False);s=bpy.context.scene
 assert (s.render.resolution_x,s.render.resolution_y,s.render.resolution_percentage)==(1280,720,100)
 assert s.render.fps==24 and s.render.engine=='BLENDER_EEVEE' and s.eevee.taa_render_samples==16 and not s.render.use_compositing
 for f in frames:
  s.frame_set(f);folder=P/'Frames'/name if mode=='demo' else P;folder.mkdir(parents=True,exist_ok=True)
  out=folder/('Cased'+name+'_f%03d_v012.png'%f);assert not out.exists(),out
  s.render.filepath=str(out);start=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-start
  rows.append(dict(scene=p.relative_to(ROOT).as_posix(),native_sha256=native_hash,frame=f,output=out.relative_to(ROOT).as_posix(),seconds=dt,under_5=dt<5))
  record=dict(mode=mode,granted_slot=slot,samples=rows,all_under_5=all(r['under_5'] for r in rows),settings=dict(resolution=[1280,720],fps=24,engine='EEVEE',samples=16,backend='VULKAN',color='AgX Medium High Contrast',compositor=False),machine=platform.node(),measurement='Whole render(write_still=True) call including written PNG; process/file load excluded. No warmup render.',cache='Normal existing driver disk caches. Prior T44 empty-cache initialization12.55–25.13s remains unresolved; no universal cold-machine claim.',concurrency='Serialized render grant. Any actual non-render overlap must be appended truthfully by queue coordinator.')
  (E/(mode+'_v012.json')).write_text(json.dumps(record,indent=2),encoding='utf8')
  print('T47_RENDER',name,f,round(dt,4),dt<5,flush=True)
  if dt>=5:raise RuntimeError('Strict cap failed; stop and simplify before any further render')
 assert hashlib.sha256(p.read_bytes()).hexdigest()==native_hash
print('T47_RENDER_SLOT_COMPLETE',slot,mode,len(rows),flush=True)
