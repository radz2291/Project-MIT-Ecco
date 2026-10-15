"""Package the temporary plug revision without regenerating v001 records."""
import json,hashlib,shutil,re
from pathlib import Path
from urllib.parse import unquote
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[4];TASK=ROOT/'Records/Tasks/T-005';ASSET=ROOT/'Shared/Assets/ECCO'
verify=json.loads((TASK/'Evidence/temporary-plugs-verification_v002.json').read_text());assert verify['all_pass']
img=Image.new('RGB',(1600,1110),'#111820');d=ImageDraw.Draw(img);f=lambda n:ImageFont.truetype(r'C:\Windows\Fonts\segoeui.ttf',n)
d.text((30,20),'ECCO | Temporary closures v002 | Review comparison',font=f(30),fill='white')
d.text((30,66),'Removable visual placeholders - client assembled plugged STEP pending',font=f(22),fill='#e9bd72')
for name,label,x in [('ECCO_sensor-closeup_v001.png','v001 | supplied housing',30),('ECCO_temporary-plugs_sensor-closeup_v002.png','v002 | temporary caps / plug / cover',820)]:
    im=Image.open(TASK/'Previews'/name).convert('RGB');im.thumbnail((750,422));img.paste(im,(x,115));d.text((x,550),label,font=f(21),fill='white')
im=Image.open(TASK/'Previews/ECCO_temporary-plugs_overview_v002.png').convert('RGB');im.thumbnail((1300,470));img.paste(im,((1600-im.width)//2,595))
d.text((30,1055),'9 removable parts | original mesh and v001 preserved | functional axial bore remains open',font=f(22),fill='#e9bd72')
img.save(TASK/'Previews/ECCO_temporary-plugs-comparison_v002.png')
readme='''# ECCO temporary plugged master v002

15 October 2026 / T-005 revision following Radzi's relayed client request: “Holes needs to have plugs”; client offered an assembled STEP later and suggested temporarily working with this model. This authorizes a provisional visual closure pass, not certification of invented assembly details or a promised delivery date.

Use [ECCO_master_temporary-plugs_v002.blend](ECCO_master_temporary-plugs_v002.blend), collection **ECCO_MASTER_v002**. [v001 remains intact](ECCO_master_v001.blend); its [interface/dimensions and replacement procedure](README_v001.md) still apply. v002 is the current temporary visual candidate for review.

**ECCO_TEMPORARY_CLOSURES** contains nine removable parts: three imaging-port caps, three service-port plugs and three rectangular service covers. All parent to ECCO_ROTATION_X, so translation/rotation follows the preserved housing. Hide this collection to restore the supplied appearance. These are prior First Ping presentation components transformed back to source coordinates after confirming the earlier housing mesh matches the current source. They have neutral materials and explicit temporary metadata. No plugs were welded into or Boolean-applied to the source mesh.

Reverse-side QA showed the inherited rectangular plates were too deep. The three plates were reseated to source-mesh ray samples at the surrounding pad rim and provisionally enlarged to 145x80mm, including the pocket extension. These dimensions describe this visual placeholder only, not an engineering specification. The source axial bore remains open as a functional passage. Small fastener features remain supplied geometry; this pass does not certify every manufacturing hole. Exact closure detail, acoustic-face design, mud sensor, shoulder datum and 2.400m versus nominal 2.25m still require MIT/source reconciliation. Sensor references remain inherited rim centres; do not treat temporary caps as calibrated acoustic faces. Recheck pulse origins/occlusion for B201 when the assembled model arrives or its face specification is confirmed.

On receipt of the assembled STEP, preserve/register it, compare closures and full geometry, replace this temporary collection with supported assembly parts, then rerun control, sensor, clearance, camera and continuity checks. No incoming-file inspection or zero-rework swap is claimed.

[Comparison preview](../../../Records/Tasks/T-005/Previews/ECCO_temporary-plugs-comparison_v002.png) · [fresh-open checks](../../../Records/Tasks/T-005/Evidence/temporary-plugs-verification_v002.json)
'''
(ASSET/'README_v002.md').write_text(readme,encoding='utf-8')
report=TASK/'report.md'
archive=TASK/'report_v001.md'
if not archive.exists():shutil.copy2(report,archive)
text='''# T-005 / B101 — temporary plug revision v002

15 October 2026. Task `911d2198-d82e-450b-a4f5-a1f6dfb517d9`; rework run `4d82f620-e5d7-443c-baae-d0180ad9bcd8`; worker `codex-t005-plugs-v002-01a13f65`; reviewer Radzi. Authorized by the producer's follow-up relaying the client request to plug holes temporarily while the assembled STEP is pending. Live prerequisites still Done and standard revision 2 unchanged. B101 reopened from Review for this bounded correction; no downstream work started.

## Current review candidate

- [Temporary plugged master v002](../../../Shared/Assets/ECCO/ECCO_master_temporary-plugs_v002.blend), reusable collection ECCO_MASTER_v002.
- [Before/after comparison](Previews/ECCO_temporary-plugs-comparison_v002.png), plus four actual 1280×720 Workbench inspection views.
- [Temporary-part interface and replacement note](../../../Shared/Assets/ECCO/README_v002.md).
- [Build evidence and placements](Evidence/temporary-plugs-build_v002.json), [fresh-open checks](Evidence/temporary-plugs-verification_v002.json), [closure/hashes/links](Evidence/temporary-plugs-closure_v002.json).
- [Preserved v001 report](report_v001.md), original source/master and original evidence retained.

## Changes and validation

Nine removable visualization parts added in ECCO_TEMPORARY_CLOSURES: three imaging caps, three smaller service plugs, three rectangular service covers. Prior First Ping housing was compared by vertex/loop signature with the current preserved source before reusing its presentation components. Mapping reverses the earlier upright presentation into the current source-X coordinate system. Reverse-view QA found the old plates too deep; all three were seated to ray-sampled pad rims and given a temporary 145x80mm footprint covering the pocket extension. These are visual placeholder dimensions only. All additions follow ECCO_ROTATION_X. The supplied housing mesh/topology/transforms and v001 file remain unchanged. Functional axial bore is retained; smaller fastener geometry is not reinterpreted as approved assembly detail.

Fresh saved v002 reopens; source signature and v001 hash match, all nine placements match the intended source transform, and +100mm axial travel / 90° rotation carries closures with error below 0.000001m. No external image/library dependency; source STEP reference resolves. Overview, opposite side, sensing recess and end views inspected visually; before/after comparison confirms seated caps/plates without filling the axial bore. Per-view elapsed render times are in build evidence. An initial post-render evidence write referenced a removed comparison object; log retained, script corrected and rerun successfully. This did not alter the source/v001. These are self-checks, not independent engineering verification.

## Limits and review

Temporary plugs are a producer-authorized visual interpretation. They are not the client's assembled STEP and do not certify all manufacturing holes or active acoustic-face construction. O04 size/datum/mud-sensor uncertainties remain; O14 assembled model is still pending. Review the closure appearance and removable-part approach. When official assembly arrives, compare actual closures and sensor faces, replace temporary parts and reverify affected mechanisms/shots. No client contact or approval is invented.

All outputs are organized under 04-Production. Base commit remains ffa19e6b4792ddc859e8f93da10f8c7e073f2f95 / main, candidate uncommitted; existing v001 changes preserved. New Blender files are local/ignored; no push, publication or remote media backup. Exact local references and limitations will be recorded on the live Rolladice task and finished run for Radzi review. The user's connected default Blender scene is untouched.
'''
report.write_text(text,encoding='utf-8')
files=[ASSET/'ECCO_master_temporary-plugs_v002.blend',ASSET/'README_v002.md',report,TASK/'report_v001.md']+list(TASK.glob('Scripts/*v002.py'))+list(TASK.glob('Previews/*v002.png'))+list(TASK.glob('Evidence/*v002.json'))
files=[p for p in files if p.name!='temporary-plugs-closure_v002.json']
links=[]
for doc in [report,ASSET/'README_v002.md']:
    for target in re.findall(r'\]\(([^)]+)\)',doc.read_text(encoding='utf-8')):
        if '://' not in target:
            p=(doc.parent/unquote(target)).resolve();links.append({'target':target,'exists':p.exists() or p.name=='temporary-plugs-closure_v002.json'})
checks={'source_checks_pass':verify['all_pass'],'links_pass':all(x['exists'] for x in links),'visual_review':'All four views and before/after sheet inspected by executor','files':[{'path':p.relative_to(ROOT.parent).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files],'links':links}
(TASK/'Evidence/temporary-plugs-closure_v002.json').write_text(json.dumps(checks,indent=2),encoding='utf-8');assert checks['links_pass'];print('V002_PACKAGED',len(files),'files')
