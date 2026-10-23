import hashlib, json, shutil
from pathlib import Path
from PIL import Image, ImageChops

B = Path(__file__).resolve().parents[1]
ROOT = B.parents[2]
backup_root = Path('D:/MIT-ECCO-Render-Recovery/S05-v017-Still-Review')
def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

approved = Image.open(B/'Previews/rich-amber_still.png').convert('RGBA')
rendered = Image.open('D:/MIT-ECCO-Render-Recovery/S05-v017-RenderCache/Frames/S05_0048.png').convert('RGBA')
exact = approved.size == rendered.size and approved.tobytes() == rendered.tobytes()
assert exact, 'Rendered frame differs from approved still'
native = B/'Scenes/S05_rich-amber_v017.blend'
assert digest(native) == '900fa8fc795a864eb2b6a4727b96817154f65d5678998b886d92fc7992c52abe'
files = [native, B/'Previews/S05_rich-amber_v017.mp4', ROOT/'04-Production/Shared/Assets/ECCO/ECCO_film_v002.blend']
backups = []
for p in files:
    q = backup_root/p.relative_to(ROOT)
    q.parent.mkdir(parents=True, exist_ok=True)
    if not q.exists():
        shutil.copy2(p,q)
    assert digest(p) == digest(q)
    backups.append({'source':str(p),'backup':str(q),'sha256':digest(p)})
result = {'owner_release':'Good approve.. pls render', 'scope':'Approved v017 four-second focused proof only', 'frame48_pixel_identical_to_approved_still':exact, 'native_sha256':digest(native), 'native_reopened_in_live_blender_at_frame':48, 'relative_shared_library_exists':True, 'visual_inspection':'12 chronological decoded frames inspected: three fragments remain identifiable from entry through pad passage to exit; no obvious missing frames or image discontinuities. Normal-speed viewer acceptance remains with owner.', 'geometry':'Unchanged from approved native; inherits v012 longer-wisp and v013 enlarged-rock 191-time-sample clearance checks. Material-only v017; illustrative motion, not CFD.', 'same_machine_backup':backups, 'full_18_second_integration':'Not released or rendered'}
(B/'Records/animation-verification.json').write_text(json.dumps(result,indent=2)+'\n')
media = json.loads((B/'Records/media-verification.json').read_text())
(B/'README.md').write_text('''# S05 v017 — Approved amber treatment, four-second render

Owner approved the v017 still and requested rendering on 23 October 2026. The approved slightly lifted fog and richer matching amber rocks/trails are retained exactly. Fluid strength is 0.44 of v014, surface alpha 0.011; rock/trail linear RGBA (1.0, 0.48, 0.035, 1). Longer trails and 50% larger fragments retain their checked motion and geometry.

## Delivery

- Video: `Previews/S05_rich-amber_v017.mp4` — 4 seconds, 96 frames, 24 fps, 1280 x 720, H.264.
- Editable native: `Scenes/S05_rich-amber_v017.blend`.
- Review page: `Previews/review.html`; chronological contact sheet: `Previews/motion-review.jpg`.
- Entry, interaction and exit stills are beside the video. The original approved still remains `Previews/rich-amber_still.png`.

## Verification

EEVEE, 6 samples. Representative preflight frames 1/48/96 rendered in 1.87/1.14/1.12 seconds. All 96 batch frames stayed below five seconds; maximum 1.662 seconds, mean 1.079 seconds. The MP4 decoded completely to 96 frames. Batch frame 48 is pixel-identical to the approved still. Native hash is unchanged; reopened in live Blender at frame 48 with a valid relative ECCO source link.

Twelve chronological decoded frames were inspected. The same three fragments travel through the passage. This is illustrative motion; existing v012/v013 geometry checks are inherited, not CFD validation. Owner normal-speed review of this rendered proof remains pending. Full 18-second integration is not released.

## Storage and recovery

Previous proofs and shared masters are preserved. Native, video and shared dependency have matching same-machine recovery copies under `D:/MIT-ECCO-Render-Recovery/S05-v017-Still-Review/`, preserving relative paths. Frame cache: `D:/MIT-ECCO-Render-Recovery/S05-v017-RenderCache/Frames` (kept on D because C has limited space). Heavy media remains local, not offsite. See `Records/animation-verification.json` and `Records/media-verification.json`; exact source-control publication evidence is saved locally in `Records/animation-sync-verification.json` after push.
''',encoding='utf-8')
contract = ROOT/'04-Production/Shots/S05/S05-B/direction.md'
txt = contract.read_text(encoding='utf-8')
txt = txt.replace('## Controlling v017 color balance still — 23 October 2026','## Controlling v017 approved treatment and focused render — 23 October 2026',1)
txt = txt.replace('**Still approval pending; no animation rendered.** Full integration remains unreleased.','**Owner approved v017 still and authorized its four-second render on 23 October 2026.** Delivered `Interaction-Proof_v017/Previews/S05_rich-amber_v017.mp4` (96 frames, 24 fps, 1280 x 720). EEVEE 6 samples; batch mean 1.079 s and maximum 1.662 s per frame. All frames decoded; frame 48 is pixel-identical to the approved still. Native remains byte-identical and was reopened at frame 48 with valid relative source dependency. Twelve chronological decoded frames inspected. Motion review remains with owner; full 18-second integration remains unreleased. Records: `Interaction-Proof_v017/Records/animation-verification.json` and `media-verification.json`.',1)
contract.write_text(txt,encoding='utf-8')
print(json.dumps({'pixel_match':exact,'verified_backups':len(backups),'media':media}))
