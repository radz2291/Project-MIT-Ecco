# ECCO-055 — Shared surface and descent

Current revision: [Surface v006 / World v011](Revision_v006/report.md), authorized by Radzi on31October2026. Earlier implementation history below is retained; current paths are in the new review record.

The detailed rig and pictured subsea assembly now sit in copies of the established descent scene. The surrounding earth uses shared mesh data while camera, timing and opening motion remain local. The continuous S01–S02 copy links the released irregular World at its destination.

Task `977d9ffb-39db-41e3-aed7-e27abb712d45`; delegated by owner-authorized ECCO-051. Worker `ECCO-055-builder-20261030`, run `b278521f-5649-4336-963f-0c80b6059e40`. Base checkout `bb9a503c8d69ae0cf5ba20273a5280d130cc1949`. Technical checks and master visual inspection are complete. Master owns Git integration and review submission; no worker Git changes performed. Publication and Radzi's acceptance remain pending.

## Candidate and sources

- Current shared native: `04-Production/Shared/Assets/Surface/Surface_descent_v005.blend`; exact hashes in [artifact manifest](Evidence/artifact-manifest.json). Full exterior v004 is retained as the pre-cutaway version (SHA256 `ee75cfb3bd6f225ff28b97d1692ee8ba7931ecaf77008b6f4c8f12377acbefc2`).
- Current saved consumer copies: [S01](Consumers/S01_shared-descent_v002.blend), [continuous S02](Consumers/S02_shared-descent_v002.blend). Source-to-copy mapping and sample frames: [consumer-mappings-v002.json](Evidence/consumer-mappings-v002.json).
- Exact source paths/hashes: [T-050 source index](../T-050/source-index.md), pinned decision commit `58013a6f5a907bfdfe9a7c7d63405e3306c2c42c`. Uses S01 Gentle-10s-Finish earth, Surface v003 rig, original `03_SUBSEA`, S02 v011 local continuity, and World v010 released by ECCO-053.
- [Controls and migration](README-controls.md). No existing previs native was overwritten. All heavy native/video files remain local; no off-machine backup claim.

## Implementation

The successor contains only the chosen rig/subsea and shared earth data. Original historical cameras, tools and mechanisms are excluded. The proxy rig objects in consumer copies are removed to avoid overlapping detailed and simple versions.

The original subsea assembly assumed a seabed at Z=-160m; the selected descent uses Z=-120m. Lower subsea parts move +40m. Riser/guide spans between Z=-145 and 10 are shortened progressively; the top stays at 10 m. The foundation underside extends to exactly Z=-120, retaining its top at-118.649994. The continuous riser spans-120..10 around the unchanged drill string. Guide posts penetrate the foundation top; lower BOP sleeves surround the continuous riser. These are illustrative scene adaptations, not certified equipment dimensions or mechanical fit.

The first motion test found a solid imported BOP cap obstructing native frame 96; source footage had an open bore. Baseline/candidate raycasts identified `SUBSEA_BOPStack` at frame 96 and `RIG_MarineRiser` at94. The v005 successor adds an illustrative 0.45 m axial viewing opening through central riser/BOP/couplings/base plus a near-side 50-degree camera-access section only between Z=-121 and-100. The foundation is excluded from the wedge. Original and v004 geometry are preserved. These cuts serve the unchanged impossible-camera path; they do not claim actual internal equipment geometry. See [opening parameters](Evidence/axial-opening.json), [raycasts](Evidence/obstruction.json) and [baseline frame 96](Previews/baseline-S01_f096.png).

Far outer earth faces are widened using shared mesh data. Inner boundaries and original animated object transforms remain unchanged. The S02 destination replaces only `S02 geological wall retained section` with the relative World v010 collection instance; the original action and action slot preserve its arrival at frames 240–241. The S01-only copy ends at 240 and keeps that destination hidden, while the continuous S02 copy is the transition reference. Local datasets, camera/lens and later acquisition/history behavior are retained.

## Verification

- Selected input hashes were verified by the master before delegation. Source files remain preserved.
- Both final v002 consumers were independently reopened by the master. Frame ranges, playback rates, sampled camera transforms/lenses, unchanged source files and existing library dependencies all passed: [independent master check](../T-051/Evidence/055-independent-check.json). These are sampled camera checks, not a claim that every frame was compared.
- A bounded +.001 change to one final v005 earth vertex reached both saved/reopened S01 and S02 consumers. The master reran the check, restored the native master byte-for-byte, and reopened consumers to their original values: [final propagation and join bounds](Evidence/propagation-and-joins-v005.json).
- Initial 640×360 Workbench 32 full render-to-file times: frame 1 **2.202s**, frame 90 **1.023s**, frame 240 **0.948s**, frame 264 **1.169s**. All below 5 s: [timings](Evidence/render-benchmarks.json). These are working-proof settings, not a claim that untouched high-resolution settings meet budget.
- After foundation correction, 56 focused motion frames passed at a maximum **1.914s/frame**. Clips: [subsea travel v001](Previews/subsea-travel_v001.mp4), [deep transition](Previews/deep-transition_v001.mp4). Subsea v001 is superseded by the cutaway correction; the deep-transition geometry is unchanged.
- Corrected v005 frame 94 and 96 proofs passed at **2.155s** and **0.789s**; both now show the open brown bore and drill string. [Frame 94](Previews/S02_cutaway_f094_v002.png), [frame 96](Previews/S02_cutaway_f096_v002.png), [timings](Evidence/cutaway-benchmarks.json).
- Master rendered the final 31-frame subsea proof: every frame passed, maximum **1.893s/frame**. The native frame 60–120 span is sampled every two frames and encoded at 12 fps, retaining source playback speed. Master independently inspected frames 94/96/98/102 and confirmed the opaque cap is gone and the open bore is visible: [current subsea motion](Previews/subsea-travel_v002.mp4), [final frame timings](Evidence/cutaway-motion-timings.json).

Scripts are reproducible with installed Blender 5.2 using `--background --factory-startup --disable-autoexec --python <script>`. The official read-only connection was checked before work. Running UI scenes were never edited. `build_surface.py` creates successors; `verify_render.py -- verify` reopens; `verify_render.py -- render` benchmarks; `verify_propagation.py` performs a temporary successor-only edit and exact restoration; `motion_proofs.py` renders focused source-timed spans only.

## Remaining review

Master supplies the final publication SHA and commit-pinned report after synchronizing the explicit [publication list](publication-files.json). Native files, MP4s, raw frames and logs remain local. Radzi retains appearance acceptance; no film assembly, final movie batch, client contact or delivery was performed. No worker Blender process is running.
