# S07 v006 — impact pullback ending

Status: owner-approved S07 v006; closed on 25 October 2026. Direct owner feedback accepted the v005 direction and requested a stronger near-to-far pullback in the final shot. Shots 1 and 2 are preserved exactly; no whole-film or client approval inferred.

## Change

Only frames 121–192 change. Shot 3 starts close to the product with the camera already retreating at constant speed for its first eight frames. The retreat then slows smoothly into a centered complete-product composition, retaining a gentle drift through the fade. There is no dead start. Camera distance at the established pose is about 3.03 times its entry distance. This is an illustrative camera-composition control, not an engineering value.

The three-shot edit and eight-second duration remain. No logo, closing text or opening fade. Final black remains at frame 190. Product geometry and hardware are stationary; no product spin was introduced.

## Preservation and verification

First 120 camera records, evaluated positions/orientations and rendered image hashes match v005. These images are reused exactly. Revised source opens successfully with packed dependencies and no external libraries. Source mesh vertices/topology and all-frame hardware matrices match the canonical source. v005 native, canonical source and approved S06 artifacts retain their hashes. Dimensions, materials, lighting and existing provisional-cover/source-length limitations remain unchanged.

Third-shot entry has nonzero constant velocity; camera distance increases throughout the retreat. Final drift is 4.3% of entry translation speed. Final whole-product framing remains centered and inside the image. Cut interpolation, no branding, direct product entry and fade endpoint verified. Complete edit, boundary preview and individual clips decode without errors. Executor inspected cut and pullback frames; owner playback approval is recorded in owner-approval_2026-10-25.md.

## Rendering and handoff

Only 72 revised frames rendered after passing representative benchmarks. New rendering: 58.0 seconds, average 0.81 seconds/frame, maximum 3.24 seconds. Every revised and reused complete frame is below five seconds. 120 approved images reused. Eevee 32 samples, 1280×720, 24 fps. No expensive finishing.

Media and source links: ../README.md. Full edit plus separate shot clips supplied. Native/media local only. Hash-verified same-machine recovery: D:/MIT-ECCO-Render-Recovery/S07-Monumental-Precision_v006. Not an off-machine backup. Scripts, contracts and verification records are published to the established repository; exact remote parity is recorded in sync-verification.json. Owner retains final logo, audio and whole-film assembly.

## Closure

Selected candidate approved by the owner. Fresh native/source checks and media decodes passed; selected video/native/recovery hashes match. See closure-verification.json and owner-approval_2026-10-25.md. No matching S07 ticket exists in live Work revision 747; unrelated tickets were not changed. Prior versions and render caches are retained; no additional visual work or rendering is planned under this scope.
