"""Render-source packaging for A03: existing vector storyboard -> 22 shot preview sheets.
No AI hardware generation, source SVG alteration, restricted-log copying or Blender operation.
"""
from pathlib import Path
import base64, hashlib, html, importlib.util, json, os

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('a03',HERE/'build_inventory_v001.py')
inv=importlib.util.module_from_spec(spec); spec.loader.exec_module(inv)
ROOT=inv.ROOT
PACK=HERE/'Previews/v002'
esc=html.escape

def relative(p,origin): return Path(os.path.relpath(p,origin)).as_posix()
def save(p,s): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(s,encoding='utf-8')
def svg_uri(svg): return 'data:image/svg+xml;base64,'+base64.b64encode(svg).decode('ascii')
def placeholder():
 return b'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="540" viewBox="0 0 960 540"><rect width="960" height="540" fill="#102535"/><rect x="270" y="70" width="420" height="400" rx="14" fill="#ecf2f4"/><path d="M315 160 H645 M315 192 H575" stroke="#9babb3" stroke-width="8"/><rect x="315" y="230" width="330" height="170" rx="8" fill="#d4e0e6"/><text x="480" y="278" text-anchor="middle" font-family="Arial" font-size="22" fill="#324c5c">ENP1 REPORT</text><text x="480" y="316" text-anchor="middle" font-family="Arial" font-size="20" fill="#324c5c">PERMISSION PENDING</text><text x="480" y="355" text-anchor="middle" font-family="Arial" font-size="16" fill="#526b7b">NO REAL DATA DISPLAYED</text><text x="480" y="502" text-anchor="middle" font-family="Arial" font-size="20" fill="#bcd7e5">Conditional reveal / approved alternative needed</text></svg>'''

CSS='''*{box-sizing:border-box}html,body{margin:0;width:1920px;height:1280px;overflow:hidden;background:#edf2f5;color:#162e3d;font-family:Arial,sans-serif}.page{height:1280px;padding:42px 60px 30px;display:flex;flex-direction:column}.eyebrow{font-size:19px;letter-spacing:2px;color:#58717f;text-transform:uppercase;display:flex;justify-content:space-between}.head{display:flex;align-items:flex-start;gap:35px;margin:20px 0 24px}.id{font-size:54px;font-weight:700;white-space:nowrap;color:#0c5774}.title{font-size:32px;line-height:1.18;font-weight:600;margin:4px 0 0;max-width:1450px}.stage{height:622px;display:flex;align-items:center;justify-content:center;gap:22px}.beat{flex:1;min-width:0;text-align:center}.beat img{display:block;width:100%;height:560px;object-fit:contain}.beat:only-child{max-width:1120px}.beat figcaption{font-size:20px;line-height:1.2;margin-top:10px;color:#455f6e}.beat{margin:0}.notes{display:grid;grid-template-columns:1fr 1fr;gap:34px;margin-top:22px;flex:1}.notes section{border-top:2px solid #c9d7df;padding-top:14px}.notes h2{font-size:17px;letter-spacing:2px;text-transform:uppercase;color:#0c5774;margin:0 0 10px}.notes p{font-size:22px;line-height:1.32;margin:0 0 10px}.notes .end{font-size:20px;color:#4b6574}.footer{border-top:1px solid #c8d6de;padding-top:12px;display:flex;justify-content:space-between;font-size:17px;color:#58717f;gap:40px}.badge{color:#92652c}'''

entries=[]; elapsed=0
for r in inv.rows:
 sid,ps,seconds,purpose,inputs,end,camera,info,review,blockers=r
 s=sid[:3]; dest=ROOT/f'04-Production/Shots/{s}/{sid}/Previews'
 sourcehtml=dest/f'{sid}_inventory-preview_v002.html'; png=sourcehtml.with_suffix('.png')
 beats=[]; sources=[]
 for number in ps:
  p=inv.panels[s][number-1]
  restricted=s=='S06' and number==5
  if restricted:
   svg=placeholder(); label='P5 · Placeholder only — rights unresolved'
   sources.append({'panel':number,'path':p.relative_to(ROOT).as_posix(),'included':False,'reason':'Restricted ENP1 image not read/copied; placeholder generated.'})
  else:
   svg=p.read_bytes()
   # Do not accidentally embed an unknown raster or external dependency.
   if b'<image' in svg and not (s=='S07' and number==4):
    raise ValueError('Unexpected embedded image: '+str(p))
   label='P'+str(number)+' · '+p.stem.split('_',1)[1].replace('_',' ')
   sources.append({'panel':number,'path':p.relative_to(ROOT).as_posix(),'included':True,'sha256':hashlib.sha256(svg).hexdigest()})
  beats.append('<figure class="beat"><img alt="'+esc(label)+'" src="'+svg_uri(svg)+'"><figcaption>'+esc(label)+'</figcaption></figure>')
 condition='CONDITIONAL SOURCE / RIGHTS HOLD' if sid in ('S05-03','S06-03') else 'STORYBOARD-BASED PREVIEW'
 if sid=='S05-03':
  info='Existing integrated-stage illustration only. MIT analysis is pending (C08); this is NOT FEA/CFD. '+info
 document='<!doctype html><html><head><meta charset="utf-8"><title>'+sid+' inventory preview v002</title><style>'+CSS+'</style></head><body><main class="page"><div class="eyebrow"><span>MIT ECCO · A03 SHOT INVENTORY · v002</span><span>'+str(elapsed).zfill(2)+'–'+str(elapsed+seconds).zfill(2)+'s · '+str(seconds)+'s proposed</span></div><header class="head"><div class="id">'+sid+'</div><h1 class="title">'+esc(purpose)+'</h1></header><div class="stage">'+''.join(beats)+'</div><div class="notes"><section><h2>Camera / transition intent</h2><p>'+esc(camera)+'</p><p class="end"><b>Resolve on:</b> '+esc(end)+'</p></section><section><h2>Information beats</h2><p>'+esc(info)+'</p><p class="end"><b>Review:</b> '+esc(review)+'</p></section></div><footer class="footer"><span class="badge">'+condition+'</span><span>Conceptual diagrams · not product-accurate renders · no new camera design · blockers '+esc(blockers)+'</span></footer></main></body></html>'
 save(sourcehtml,document)
 entries.append({'shot':sid,'panels':ps,'start_seconds':elapsed,'end_seconds':elapsed+seconds,'purpose':purpose,'html':sourcehtml.relative_to(ROOT).as_posix(),'png':png.relative_to(ROOT).as_posix(),'sources':sources,'camera_intent':camera,'review':review,'blockers':blockers})
 elapsed+=seconds

gallerycss='''*{box-sizing:border-box}body{margin:0;background:#0d1b26;color:#e7f0f5;font:16px/1.5 Arial,sans-serif}header,main{max-width:1500px;margin:auto;padding:32px}header h1{font-size:38px;margin:12px 0}header p{color:#adc1ce;max-width:1100px}nav{display:flex;gap:12px;flex-wrap:wrap;position:sticky;top:0;padding:14px 32px;background:#102635;z-index:2}a{color:#89d6f6}nav a{padding:6px 20px;border:1px solid #385767;border-radius:7px;text-decoration:none}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(420px,1fr));gap:24px}.card{border:1px solid #2b4555;border-radius:12px;overflow:hidden;background:#142b3a}.card img{display:block;width:100%;height:auto}.card .copy{padding:20px}.card h3{margin:0 0 8px;font-size:21px}.card p{font-size:15px;color:#bdd0da}.section{scroll-margin-top:90px;margin:30px 0 70px}.pill{color:#f5c789;font-size:13px;text-transform:uppercase;letter-spacing:1px}.meta{color:#8faab9;font-size:14px}.card a.image{display:block}.small{font-size:13px}details{margin-top:12px}summary{cursor:pointer;color:#89d6f6}footer{padding:25px 32px;color:#91aaba}'''
nav=''.join(f'<a href="#{s}">{s}</a>' for s in inv.folders)
sections=[]
for s in inv.folders:
 cards=[]
 for e in entries:
  if not e['shot'].startswith(s): continue
  im=relative(ROOT/e['png'],PACK); editable=relative(ROOT/e['html'],PACK)
  cards.append(f'<article class="card"><a class="image" href="{im}" target="_blank"><img loading="lazy" src="{im}" alt="{e["shot"]} preview"></a><div class="copy"><div class="meta">{e["start_seconds"]:02d}–{e["end_seconds"]:02d}s proposed · Panels '+', '.join(map(str,e['panels']))+f'</div><h3>{e["shot"]}</h3><p>{esc(e["purpose"])}</p>'+('<div class="pill">Conditional source/rights hold</div>' if e['shot'] in ('S05-03','S06-03') else '')+f'<a href="{im}" target="_blank">Open full image</a> · <a href="{editable}" target="_blank">Editable preview page</a><details><summary>Camera intent / review</summary><p>{esc(e["camera_intent"])}</p><p>{esc(e["review"])}</p><p class="small">{esc(e["blockers"])}</p></details></div></article>')
 sections.append(f'<section class="section" id="{s}"><h2>{s}</h2><div class="grid">'+''.join(cards)+'</div></section>')
gallery='<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>A03 · 22 shot previews · v002</title><style>'+gallerycss+'</style></head><body><header><div class="pill">MIT ECCO · A03 review · v002</div><h1>22 proposed shots, now visual.</h1><p>One image per proposed shot, preserving its existing storyboard beats, camera/transition intent and information sequence. Click an image to inspect it full size. These are source-based storyboard previews, not new shot designs or Blender renders. Hardware is diagrammatic, timing is provisional and the total remains 90 seconds.</p><p>S05 analysis stays illustrative while MIT media is pending. S06 real-log use is shown only as a placeholder; no restricted field data is included. S02 C Spatial Cinematic remains conceptual direction for later moving previs.</p></header><nav>'+nav+'</nav><main>'+''.join(sections)+'</main><footer>Saved locally under 04-Production · No public upload, commit or backup implied · Radzi review required</footer></body></html>'
save(PACK/'gallery_v002.html',gallery)
save(PACK/'preview-manifest_v002.json',json.dumps({'version':'v002','task_id':'1ff92ebd-4585-4d64-b638-5b127d6c8314','request':'Changes requested: Can you generate image for me preview each shot','kind':'Source-vector storyboard preview sheets; not AI-generated new compositions or scene renders','shots':entries},indent=2))
print(f'Saved {len(entries)} preview source pages and gallery. No restricted image read/copied.')
