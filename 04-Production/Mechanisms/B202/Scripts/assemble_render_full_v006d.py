"""Reuse identical unchanged renders; retain explicit per-frame provenance."""
from pathlib import Path
import shutil,json,hashlib
from PIL import Image,ImageChops
R=Path(__file__).resolve().parents[4];B=R/'04-Production/Mechanisms/B202';P=B/'Previews/MotionFull_v006d';E=R/'04-Production/Records/Tasks/T-027/Evidence';checks=[];rows=[]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for f,version in [(336,'v006b'),(337,'v006b'),(384,'v006b'),(432,'v006b'),(456,'v006c'),(480,'v006c'),(528,'v006c'),(540,'v006b')]:
    a=Image.open(B/f'Previews/MotionFull_{version}/proof_{f:04d}.png').convert('RGB');d=Image.open(P/f'proof_{f:04d}.png').convert('RGB');ok=ImageChops.difference(a,d).getbbox() is None;assert ok,f;checks.append({'frame':f,'version':version,'pixel_identical_to_final_saved_consumer':ok})
for f in range(1,553):
    version='v006c' if 433<=f<=528 else 'v006b';source=B/f'Previews/MotionFull_{version}/Frames/frame_{f:04d}.png';target=P/f'Frames/frame_{f:04d}.png';assert source.exists();shutil.copy2(source,target);rows.append({'frame':f,'source':source.relative_to(R).as_posix(),'sha256':sha(target)})
for f in range(553,721):
    p=P/f'Frames/frame_{f:04d}.png';assert p.exists(),f;rows.append({'frame':f,'source':'Rendered directly from final v006d saved scene','sha256':sha(p)})
result={'status':'PASS','frame_count':720,'inherited_frames':552,'final_direct_render_frames':168,'unchanged_view_pixel_checks':checks,'frames':rows,'scope':'Unchanged frames reused from same build family, with exact sampled pixel identity against final saved consumer; changed tight96frames rendered v006c, changed warm168frames rendered v006d. Full native consumer can regenerate all720frames.'}
(E/'render_provenance_v006d.json').write_text(json.dumps(result,indent=2));print('RENDER_ASSEMBLY_PASS',len(rows))
