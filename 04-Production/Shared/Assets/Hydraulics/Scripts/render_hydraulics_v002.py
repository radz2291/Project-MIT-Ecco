"""Run only during a T45-granted bounded render slot. Full write timing gate."""
import bpy,sys,time,json,hashlib,platform,gpu
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];TASK=ROOT/'04-Production/Records/Tasks/T-048';S=TASK/'Scenes';E=TASK/'Evidence';P=TASK/'Previews/Revision_v007';P.mkdir(exist_ok=True);ARGS=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,indent=2),encoding='utf-8')
def opened(kind):
 p=S/('Flow_reuse_'+kind+'_v006.blend');proof=json.loads((E/'native-verification-summary_v007.json').read_text());assert proof['all_checks_pass']
 assert any(r['sha256']==sha(p) and r['path'].endswith(p.name) for r in proof['consumers'])
 bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False,use_scripts=False);return p
def render(kind,frame,folder,rows):
 s=bpy.context.scene;s.frame_set(frame);out=folder/('Flow_'+kind+'_f%04d.png'%frame);s.render.filepath=str(out);t=time.perf_counter();bpy.ops.render.render(write_still=True);elapsed=time.perf_counter()-t
 rec=dict(consumer=kind,frame=frame,output=str(out.relative_to(ROOT)).replace('\\','/'),seconds=elapsed,under_5=elapsed<5,sha256=sha(out));rows.append(rec);print('T48_RENDER',kind,frame,elapsed,flush=True);return rec
if ARGS[0]=='benchmark':
 rows=[]
 for kind,frames in [('A',[1,36,72]),('B',[1,48,96])]:
  src=opened(kind)
  for f in frames:
   rec=render(kind,f,P,rows)
   dump(E/'benchmark_v007.json',dict(scenes=[str(S/('Flow_reuse_'+k+'_v006.blend')) for k in ['A','B']],machine=platform.node(),gpu=dict(vendor=gpu.platform.vendor_get(),renderer=gpu.platform.renderer_get(),backend=gpu.platform.backend_type_get(),version=gpu.platform.version_get()),engine=bpy.context.scene.render.engine,samples=16,resolution=[1280,720],fps=24,color_management=['AgX','AgX - Medium High Contrast'],compositing=False,measurement='Wall clock around complete bpy.ops.render.render(write_still=True), includes initialization/render/PNG write; process and source loading excluded; first view of each saved scene is not warmed in-process',cache='Normal existing driver disk caches, not erased',known_limit='Prior T44 empty-cache initialization12.55-25.13s unresolved; no universal cold-machine pass',renders=rows,all_under_5=all(x['under_5'] for x in rows)))
   if not rec['under_5']:raise RuntimeError('Strict <5s benchmark failed; stop before batch and simplify')
elif ARGS[0]=='batch':
 bench=json.loads((E/'benchmark_v007.json').read_text());assert bench['all_under_5'] and len(bench['renders'])==6
 kind=ARGS[1];src=opened(kind);folder=P/('Frames_'+kind);folder.mkdir(exist_ok=True);rows=[]
 for f in range(1,bpy.context.scene.frame_end+1):
  rec=render(kind,f,folder,rows)
  dump(E/('batch_'+kind+'_v007.json'),dict(scene=str(src.relative_to(ROOT)).replace('\\','/'),scene_sha256=sha(src),renders=rows,all_under_5=all(x['under_5'] for x in rows)))
  if not rec['under_5']:raise RuntimeError('Strict <5s failed within batch; stopped at failing frame')
else:raise ValueError(ARGS)
