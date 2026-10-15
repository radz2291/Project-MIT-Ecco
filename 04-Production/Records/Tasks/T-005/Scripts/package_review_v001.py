"""Build local B101 review sheet, interface record and task closure evidence."""
import json,hashlib,shutil,re
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[4];TASK=ROOT/'Records/Tasks/T-005';ASSET=ROOT/'Shared/Assets/ECCO'
old=Path(r'C:\Users\RZ1\Desktop\RZ\261008-MIT-Ecco\04-Project\01-ECCO_First_Ping-Test\02-Previews')
for name in ['Client_Confirmed_Sensor.png','IMPLEMENTATION_REPORT.md']:
    dst=ASSET/'Originals'/name
    if not dst.exists():shutil.copy2(old/name,dst)
    assert dst.read_bytes()==(old/name).read_bytes()
build=json.loads((TASK/'Evidence/build-evidence_v001.json').read_text());verify=json.loads((TASK/'master-verification_v001.json').read_text());assert verify['all_pass']
sheet=Image.new('RGB',(1600,1170),'#111820');draw=ImageDraw.Draw(sheet)
font=lambda n:ImageFont.truetype(r'C:\Windows\Fonts\segoeui.ttf',n)
draw.text((30,18),'ECCO | B101 product master inspection | v001',font=font(30),fill='white')
draw.text((30,65),'PROVISIONAL HARDWARE - source mesh preserved - engineering acceptance pending O04 / O14',font=font(21),fill='#e9bd72')
labels=['Full housing / source +X longitudinal','Opposite side / unchanged tessellation','Large sensing recess beside rectangular cover','X=0 end / thread and shoulder datum unverified']
for index,(name,label) in enumerate(zip(['overview','opposite','sensor-closeup','end-X0'],labels)):
    x=30+(index%2)*790;y=118+(index//2)*460
    im=Image.open(TASK/'Previews'/('ECCO_'+name+'_v001.png')).convert('RGB');im.thumbnail((760,428));sheet.paste(im,(x,y))
    draw.text((x,y+430),label,font=font(18),fill='#cdd7e3')
draw.text((30,1060),'Measured: L 2400.000 mm | maximum axis diameter 304.800 mm | recess plane X 730 mm | 120 deg spacing',font=font(21),fill='white')
draw.text((30,1100),'Unresolved: nominal 2250 mm / pin-shoulder datum / mud sensor / plugged replacement. No added plugs or acoustic faces.',font=font(19),fill='#e9bd72')
sheet.save(TASK/'Previews/ECCO_inspection-sheet_v001.png')
interface='''# ECCO provisional master v001 — interface and replacement record

T-005 / B101, 15 October 2026. Internal mechanical foundation for Radzi review. No MIT engineering or rights approval is created.

## Source and measured geometry

Import the **ECCO_MASTER_v001** collection from [ECCO_master_v001.blend](ECCO_master_v001.blend), using a relative Blender library path. The inspection cameras sit outside this collection. Preserve v001 when creating later versions. This master wraps the earlier registered import; STEP was not independently retessellated in this run.

Source geometry: one connected mesh, 348,876 vertices, source X longitudinal, coordinates originally in mm with object scale 0.001; scene metres, scale_length 1. No rescaling, vertex/topology edits, fabricated acoustic faces, plugs, closures or internals. [Original imported scene](Originals/Source_Imported_ecco.blend) and original STEP copy are byte-preserved. [Annotated reference](Originals/Client_Confirmed_Sensor.png) identifies the larger recess beside the rectangular cover; the [historical implementation report](Originals/IMPLEMENTATION_REPORT.md) supplies the recess-centre interpretation. Its older delivery paths and approval language are historical, not current authority.

| Item | Inspected value | Limit |
|---|---|---|
| Overall source X bounds | 0 to 2.400000095 m | Source mesh ends, not pin shoulders; 2.25 m nominal brochure unresolved |
| World bounding box Y / Z span | 0.302608788 / 0.303737700 m | Different extrema occur at different azimuths |
| Maximum diameter about source X axis | 0.304800137 m | Corresponds to nominal 12 in / 0.3048 m; not thread/clearance certification |
| Imaging recess plane | X = 0.730 m | Inherited rim centres; not verified transducer faces |
| Sensor angles in source YZ plane | 39 / 159 / 279 degrees | Three references separated by 120 degrees |
| Recess-centre radius | approx. 0.129 m | Historical rim-centre interpretation, not active-face offset |
| Source end interfaces | source X=0 and X=2.400 m bounds | Top/box vs bottom/pin and shoulder coordinates not assigned as certified datums |
| Mud sensor | Unlocated | Hidden placeholder has no usable coordinate |

Brochure pp.1–3 states three imaging sensors at 120 degrees, plane 600 mm above the lower pin shoulder, top 6-5/8 F.H. box, bottom 6-5/8 F.H. pin, fishing neck 8.25 in, minimum ID 2.25 in, minimum casing ID 12.3 in. These are source specifications, not measurements validated by this mesh. Do not rescale to force nominal agreement. A 600 mm shoulder offset cannot be checked without identifying the shoulder. The preserved imported mesh has no independently established manufacturing revision or thread fit.

## Stable interfaces

| Name | Use |
|---|---|
| ECCO_ROOT | Whole assembly translation; source origin retained |
| ECCO_ROTATION_X | Local X rotation in radians; child of root. Confirm end/viewpoint before clockwise drilling animation |
| ECCO_GEOMETRY_REPLACEABLE / ECCO_HOUSING_SOURCE_MESH | Replaceable geometry only, parented to rotation control |
| ECCO_SENSOR_REFERENCES / ECCO_SENSOR_REF_01–03 | Separate recess-centre transforms; local +Z points radially outward. Pending acoustic face confirmation |
| ECCO_SENSOR_PLANE_PROVISIONAL | X=0.730 m reference; no rendered surface |
| ECCO_MUD_SENSOR_UNLOCATED | Hidden, unusable placeholder; do not bind effects |
| ECCO_EFFECTS_EMPTY | Reserved separate effects collection; no physical simulation |
| ECCO_CUTAWAY_TOOLS / ECCO_CUTTER_PREVIEW_ONLY | Hidden section cutter, follows rotation; optional Boolean on housing disabled for viewport/render |

Rotation/scanning references are separated without guessing physical subassemblies from a continuous mesh. The section modifier is an illustrative editing interface; it does not validate internal hardware and is not used in inspection renders. All geometry remains monolithic because supplied component identities are absent. Hardware-dependent internal/cutaway claims remain blocked.

## Plugged replacement procedure — O14

1. Register received file, date, supplier/version, rights and SHA-256; preserve it in Originals. Do not overwrite v001.
2. Inspect units, source axes, complete bounds, axial/radial dimensions, closures, pad profile, top/box and lower/pin identity, thread/shoulder datums, imaging count/positions/face normals and dedicated mud sensor. Compare measured values to v001 and supplied engineering evidence; never assume unchanged sensors.
3. Build a new versioned master; map geometry into source coordinates deliberately. Reparent to controls, preserve stable names where compatible, remap sensor references from evidence and reattach optional section modifier to the replacement housing. Record any incompatible interface changes.
4. Relink a test consumer, exercise axial travel and full rotation, visibility and section controls; verify sensor origins, pulse/echo return/contact, well/bit/casing clearances, camera occlusion and continuity for every affected mechanism/shot.
5. Save new inspection views, comparisons and hashes; update manifests/blockers and ticket evidence. Reopen affected accepted reviews where the change is substantive. Record which supported hardware version the film depicts before B4.

S01–S07 visible-product assets and B102/B201–B205 require compatibility review before reuse. Missing replacement does not stop independent preparation, but prevents claiming replacement compatibility or final hardware acceptance. Radzi supplies the model and obtains MIT decisions on length/datum, transducer detail and mud sensor.
'''
(ASSET/'README_v001.md').write_text(interface,encoding='utf-8')
report='''# T-005 / B101 — product master validation report v001

15 October 2026. Stable Rolladice task `911d2198-d82e-450b-a4f5-a1f6dfb517d9`, run `efba46c6-104b-4d70-b8a0-ae4c31a6af19`, worker `codex-t005-01a13f65`; reviewer Radzi. Authority: direct instruction to execute this ticket. Live A02/T-2 and A04/T-4 were Done; pinned roadmap revision 2 checked against fresh handoff before claiming.

## Result for review

Reusable **provisional v001** master produced, with unchanged housing geometry and separate rotation/translation controls, imaging recess references, empty effects namespace and disabled illustrative section tool. Manufacturing subassemblies and internal hardware are not invented. B101 bounded inspection/wrapper work is complete for review; MIT engineering acceptance, replacement acceptance and downstream geometry-dependent release remain open.

- [Inspection sheet](Previews/ECCO_inspection-sheet_v001.png); four actual Workbench views at frame 1, 1280×720.
- [Reusable master](../../../Shared/Assets/ECCO/ECCO_master_v001.blend), local ignored binary.
- [Interface, measurements and replacement procedure](../../../Shared/Assets/ECCO/README_v001.md).
- [Build/source hashes and render timings](Evidence/build-evidence_v001.json), [fresh-open self-checks](master-verification_v001.json), [output integrity manifest](Evidence/output-manifest_v001.json).
- [Reproducible build](Scripts/build_master_v001.py), [saved-master verification](Scripts/verify_master_v001.py), [review package generator](Scripts/package_review_v001.py).

## Evidence and checks

Source imported scene opens in Blender 5.2.2 LTS; preserved source STEP/imported .blend copies match byte hashes. Source/master coordinates and loop topology signatures match, transforms match after parenting, and vertex count remains 348,876. One connected component was measured; no physical manufacturing split can be inferred. Bounding-box dimensions 2.400000095 × 0.302608788 × 0.303737700 m; maximum X-axis diameter 0.304800137 m matches nominal 12 inches. Three inherited recess-centre references are at source X=.730 m and 39/159/279° with 120° spacing; nearby source vertices exist at that plane. Reference origins are not validated transducer faces.

Fresh saved file reopened in a separate process. Root axial travel (+100 mm) and 90° X rotation move all references coherently with maximum error below 0.000001 m. Optional Boolean is off; geometry collection contains only the source housing. Source STEP relative reference resolves; saved master has no external image or linked-library dependency. A separate [linked consumer](Evidence/library-consumer_v001.blend) was saved and reopened, verifying relative library resolution, housing inclusion and inspection-camera exclusion; see [library checks](Evidence/library-check_v001.json). Four renders were inspected visually through the labeled sheet, including opposite side and source X=0 end; raw overview/sensor close-up inspected separately. All views derive from the saved master at default geometry/control state. Total measured render time is approximately 3.04 seconds (individual values in build evidence); no animation or expensive render was required for this B1 inspection task.

Official live MCP read-only access confirmed the user's unsaved default Cube/Camera/Light scene; it was left unchanged. The MCP saved-file helper failed because its server environment lacks BLENDER_PATH. Isolated saved-file work used the installed official Blender executable instead. First verification harness falsely flagged an unlinked appended source object's unevaluated matrix and a library datablock introduced by that comparison; failure evidence is retained. Linking the comparison object for dependency evaluation and measuring saved dependencies before appending corrected the harness; no master change was needed. Final self-checks pass. These are executor self-checks, not independent MIT verification.

## Unresolved engineering / review questions

1. O04 / BL01: confirm current housing revision and reconcile 2400 mm source length with nominal 2250 mm. Do not scale by assumption.
2. O04: identify lower pin shoulder and verify the brochure's 600 mm sensor-plane offset; confirm exact acoustic faces/orientations and mud sensor. Rim centres plus client annotation establish a provisional placement route, not all internals.
3. O14: receive and inspect plugged replacement; compare closures, units/dimensions, sensors and controls, then rerun affected checks. Replacement has not arrived and no swap success is claimed.
4. Radzi: review the source-preserving master/interface and inspection sheet for provisional foundation use. BL01 continues to block unsupported geometry-dependent claims; B102 assemblies require approved compatible dimensions under BL02/O05. No downstream ticket was launched.

## Closure / publication state

Base checkout: branch main, commit `ffa19e6b4792ddc859e8f93da10f8c7e073f2f95`; starting working tree clean. Candidate is explicitly **uncommitted**. All retained outputs are under 04-Production; source originals outside this checkout are preserved and copied into the asset's Originals folder. STEP and .blend remain Git-ignored, saved locally only; no commit, push, remote media backup, public publication, client contact or engineering approval is implied. Updated asset and blocker registers link this review version. See output manifest for exact bytes/SHA-256. Rolladice is the live review authority; Radzi alone accepts.

## Reproduce

Use `C:/Program Files/Blender Foundation/Blender 5.2/blender.exe --background <Originals/Source_Imported_ecco.blend> --python <Scripts/build_master_v001.py>`, then `--background <ECCO_master_v001.blend> --python <Scripts/verify_master_v001.py>`. Build refuses differing preserved original copies. Build modifies only its background process and versioned local outputs; do not rerun over a manually revised v001. Run package_review_v001.py with bundled Python/Pillow to recreate the labeled sheet and output manifest.
'''
(TASK/'report.md').write_text(report,encoding='utf-8')
files=[]
for p in sorted(list(ASSET.rglob('*'))+list(TASK.rglob('*'))):
    if p.is_file() and p.name!='output-manifest_v001.json':
        files.append({'path':p.relative_to(ROOT.parent).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'local_only_binary':p.suffix.lower() in ['.blend','.stp']})
(TASK/'Evidence/output-manifest_v001.json').write_text(json.dumps({'version':'v001','files':files,'publication':'Uncommitted; no push or remote media backup','self_checks_pass':verify['all_pass']},indent=2),encoding='utf-8')
print('PACKAGED',len(files),'files')
