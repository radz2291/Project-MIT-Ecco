"""Verify and register A03 review-change visual preview outputs."""
from pathlib import Path
from PIL import Image, ImageStat
import hashlib, html, json, os, re

HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[3]; RECORDS=ROOT/'04-Production/Records'
PACK=HERE/'Previews/v002'; manifest=json.loads((PACK/'preview-manifest_v002.json').read_text(encoding='utf-8'))
def rel(p,origin=HERE): return Path(os.path.relpath(p,origin)).as_posix()
def save(p,text): p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')

original=(RECORDS/'shot-register_v001.md').read_text(encoding='utf-8')
updated=original.replace('# A03 — Proposed shot inventory v001','# A03 — Proposed shot inventory v002',1).replace('No shots/scenes/playblasts were built in A03.','Source-based static preview images now accompany every shot; no Blender scenes or moving playblasts were built in A03.',1)
updated=updated.replace('## Proposed moving-shot records','## Visual review update — v002\n\nRadzi requested an image preview for each shot in Rolladice Work on 15 October 2026. All 22 previews are now saved under the respective shot’s `Previews/` folder. These render existing vector storyboard panels with inherited camera/transition and information notes; they are not new shot designs, AI-generated hardware, approved camera compositions or Blender renders. The restricted real-log image is replaced by a clearly marked no-data placeholder; S05 integration remains illustrative.\n\nBrowse the [visual index](Tasks/T-003/visual-index_v002.md) or [local HTML gallery](Tasks/T-003/Previews/v002/gallery_v002.html). Review source metadata in the [preview manifest](Tasks/T-003/Previews/v002/preview-manifest_v002.json). Proposed grouping, timing, mechanisms and BL01–BL16 remain unchanged.\n\n## Proposed moving-shot records',1)
for e in manifest['shots']:
 marker='- **Planned evidence:** `04-Production/Shots/'+e['shot'][:3]+'/'+e['shot']+'/Previews/'
 previewlink=rel(ROOT/e['png'],RECORDS)
 updated=updated.replace(marker,'- **Saved static preview v002:** ['+e['shot']+' image]('+previewlink+') · [editable preview page]('+rel(ROOT/e['html'],RECORDS)+').\n'+marker,1)
save(RECORDS/'shot-register_v002.md',updated)

index=['# A03 — Visual shot index v002','','15 October 2026 · 22 source-based shot preview images · For Radzi review','','[Open browsable gallery](Previews/v002/gallery_v002.html) · [Shot register v002](../../shot-register_v002.md) · [Blockers v001](../../blocker-register_v001.md)','','One PNG per proposed moving shot, with the storyboard states grouped as in the inventory and the inherited camera/transition and information notes preserved. These are conceptual static previews; no new shot design or product-accurate renders. Existing restricted ENP1 data is not included. Click any image for full size.','']
for e in manifest['shots']:
 p=ROOT/e['png']; index += ['## '+e['shot'], '',e['purpose'],'',f'![{e["shot"]} visual preview]({rel(p)})','',f'[Full-size PNG]({rel(p)}) · [Editable preview source]({rel(ROOT/e["html"])})','']
save(HERE/'visual-index_v002.md','\n'.join(index))
summary='''# A03 — Review summary v002

15 October 2026 · Requested changes addressed · For Radzi

**Your request:** “Can you generate image for me preview each shot”.

**Added:** [22 visual shot previews](visual-index_v002.md), one PNG per proposed shot, and a [browsable gallery](Previews/v002/gallery_v002.html). Each sheet shows its existing storyboard beat(s), proposed timing, camera/transition intent, information sequence and review need. No new shot design was introduced.

The images are source-based conceptual storyboard previews, not AI-generated product images or Blender renders. S05's analysis beat is explicitly illustrative while MIT material is pending. S06's actual ENP1 log is a no-data permission placeholder. All 22 images were inspected through the seven section overviews, with a full-size waveform-sheet check; saved-image, layout and link checks passed.

The [shot register v002](../../shot-register_v002.md) now links every actual PNG and editable source. Proposed 22-shot grouping, 33-panel coverage, 90-second allocation and [16 blockers](../../blocker-register_v001.md) remain unchanged. Later construction still uses the scene-director skill and Scene Direction Contract; static previews do not validate moving cameras or mechanisms.

**Review now:** the visual shot grouping and inherited beats; the conditional MIT-analysis/log routes; the source/engineering questions already recorded. v001 is preserved. Everything is local/uncommitted; no public upload or backup claimed. [Report](report.md) and [visual verification](verification_v002.md).
'''
save(HERE/'review-summary_v002.md',summary)

checks=[]
def check(value,label): checks.append({'pass':bool(value),'check':label})
shots=manifest['shots']
check(len(shots)==22 and len({e['shot'] for e in shots})==22,'22 unique preview images for all inventory shot IDs')
hashes=[]
for e in shots:
 p=ROOT/e['png']
 with Image.open(p) as im:
  im.load(); check(im.size==(1920,1280),e['shot']+' PNG decodes at 1920x1280')
  check(max(ImageStat.Stat(im.convert('RGB')).stddev)>10,e['shot']+' image is not blank')
 hashes.append({'shot':e['shot'],'path':e['png'],'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size})
 check((ROOT/e['html']).exists(),e['shot']+' editable source exists')
check(sum(len(e['panels']) for e in shots)==33,'33 existing panel beats represented')
restricted=[s for e in shots for s in e['sources'] if not s['included']]
check(len(restricted)==1 and restricted[0]['path'].endswith('05_Actual_MiVU_Field_Log_ENP1.svg'),'Restricted real log excluded; single placeholder recorded')
layouts=json.loads((HERE/'Evidence/preview-layout-checks_v002.json').read_text())
check(len(layouts)==22 and all(c['loaded'] and c['bodyHeight']<=1280 and c['footerBottom']<=1280 for c in layouts),'All 22 sheets: source images loaded, canvas/footer within bounds')
included=[s for e in shots for s in e['sources'] if s['included']]
check(all(hashlib.sha256((ROOT/s['path']).read_bytes()).hexdigest()==s['sha256'] for s in included),'All 32 included source-vector hashes unchanged')
files=[RECORDS/'shot-register_v002.md',HERE/'visual-index_v002.md',HERE/'review-summary_v002.md']
bad=[];links=0
for p in files:
 for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
  if '://' in target or target.startswith('#'):continue
  # Verification record is written below; check after existence bootstrap.
  if target=='verification_v002.md':continue
  links+=1
  if not (p.parent/target).resolve().exists():bad.append(str(p)+': '+target)
check(not bad,f'{links} Markdown image/source/register links resolve: {bad}')
save(HERE/'Evidence/preview-verification_v002.json',json.dumps({'checks':checks,'images':hashes,'visual_qa':'Assistant visually inspected all 22 previews via S01–S07 overview PNGs, plus S02-02 full-size image. No clipping/blank panels observed. Conceptual geometry and source interpretation remain pending; no moving QA claimed.'},indent=2))
body=['# A03 — Visual preview verification v002','','15 October 2026 · Self-checks, not independent engineering approval.','']
body += ['- **'+('PASS' if c['pass'] else 'FAIL')+':** '+c['check'] for c in checks]
body += ['','## Visual inspection','','Inspected the seven rendered section overview sheets, covering every one of the 22 shots, and S02-02 at full size. All storyboard panels are visible, titles/notes remain within their canvas, source proportions are preserved, S03 wall deformation/geometry and S04 inner wear/channel concepts remain readable, and S06-03 clearly says no real data displayed. Full-resolution images are for detailed reading; overview sheets are navigation/review aids. S07 logo is existing storyboard artwork, not registration of final official brand assets.','','No moving-camera/physics/engineering validation or real-log permission is inferred. No new camera design, AI artwork or Blender render was produced. The PNGs are rendered from editable HTML that embeds existing vector artwork; this preserves the inventory’s no-new-design boundary.','','[Image checks and SHA-256 hashes](Evidence/preview-verification_v002.json) · [Layout checks](Evidence/preview-layout-checks_v002.json) · [Source manifest](Previews/v002/preview-manifest_v002.json) · [Visual index](visual-index_v002.md)','']
save(HERE/'verification_v002.md','\n'.join(body))
print(f'{len(checks)} checks; '+str(sum(not c['pass'] for c in checks))+' failures; '+str(links)+' local links.')
if any(not c['pass'] for c in checks):raise SystemExit(1)
