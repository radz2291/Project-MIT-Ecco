# S05 v019 — Camera-direction proof

The full 18-second camera proof is ready for owner review. It preserves v018 hydraulic geometry, animation and appearance. This is a bounded camera test, not a new finished production render.

## Deliverables

- `Previews/S05_camera-motion_v019.mp4` — 18 seconds, 432 frames, 24 fps, 960 x 540 lightweight EEVEE playblast.
- `Previews/A_arrival.png`, `B_arrival.png`, `C_arrival.png` — three authored 1280 x 720 compositions.
- `Previews/three-arrivals.jpg` — the three views together.
- `Previews/motion-contact-sheet.jpg` — chronological frames covering travel, arrivals and the cut.
- `Scenes/S05_camera-direction_v019.blend` — editable source, camera baked at each frame; original flow controls retained.
- `Records/camera-score.md` — purpose, timing, taste application and AI Director self-critique.

## What changed

A looks upward along the lower body and rises into a nearly upright sculptural arrival. B cuts closer, opens the pad flank through a short partial arc, then slows down for the existing fragment interaction. C continuously follows the flow into the upper region, then retreats and changes its gaze to reconnect the working body. The final camera holds for about 1.3 seconds while circulation and hardware rotation continue.

The final view deliberately crops the remote shaft ends and the existing finite fluid-volume boundaries. It shows the connected hydraulic working regions, not a complete dimensional catalogue view. A more elevated test exposed an amber end disc; that camera was rejected without altering fluid geometry.

## Preservation and verification

Reopened source/candidate comparison matches **3412 content entries**: scene meshes and shape keys, bound hydraulic animation, materials/node values and links, object visibility and transforms at five frames. Legacy hidden camera-parented labels are compared in their local coordinates. No new particle system, fluid simulation, material, light, hardware or environment geometry was introduced. The v018 file SHA remains unchanged.

All 432 camera samples pass the center-target wall-occlusion, camera/solid separation and upward screen-direction checks. Minimum camera-to-solid distance is 0.632 m. At least one original core fragment is geometrically visible in all 82 frames of the principal observation interval. These tests support visibility and continuity; they do not establish audience comprehension. Existing v018 sampled flow/solid clearance evidence remains applicable because the bound scene content is unchanged.

The first broad hash check was too inclusive: it compared the world transforms of hidden labels parented to the camera and unused datablocks. The corrected bound-content comparison distinguishes those expected camera-dependent differences from changes to the hydraulic scene. The diagnostic history is retained.

## Performance

Three arrivals and transition/entry stills were benchmarked before the playblast. Playblast settings: EEVEE 4 samples, 960 x 540. Arrival stills: EEVEE 6 samples, 1280 x 720. No material refinements.

- Mean playblast frame: **0.822 seconds**.
- Slowest playblast frame: **1.083 seconds**.
- Aggregate 432-frame render time: **354.9 seconds**.
- First-to-last render span: **358.8 seconds**, including tool/chunk overhead; excludes encoding.
- All 432 frames decoded from the MP4 and every delivered frame rendered in less than 5 seconds.

## Self-review and limits

The inspected arrival stills now have distinct visual roles: perspective-led lower-body arrival, close pad/passage observation and broad integrated composition. The central mechanism gets a quiet recognition interval and the ending settles. This addresses v018's repeated framing approach through camera direction alone.

Normal-speed automated visual playback could not be completed: both browser and desktop playback tools failed to initialize with a missing kernel-assets path. The encoded sequence and chronological stills are verified; owner viewing remains necessary to judge the cut, arc pace and final reveal. No independent viewer acceptance is claimed.

Hydraulic acceleration and diffuser behavior remain qualitative. Exact functional stage-face mapping is still unresolved. Existing occasional wisp/metal visual alignment and low-sample grain were not altered during this camera test. The final view reduces individual fragment size. The film allocation remains provisionally 58–76 seconds; Sections 6/7 and narration were not retimed.

## Records and storage

Owner authority: `Records/owner-direction.txt`. Existing S05-A/B/C scene contracts record this proposed camera revision without marking it accepted. Live Work was read at revision 701: T43 done, T48 review. No archived work resumed.

Native scene, MP4 and exact shared dependency have hash-matching same-machine copies under `D:/MIT-ECCO-Render-Recovery/S05-v019-Previs/`; this is not offsite backup. Heavy media remains local. Reports/scripts/selected review stills are scoped for Git publication; exact publication evidence is recorded separately in `Records/sync-verification.json`.
