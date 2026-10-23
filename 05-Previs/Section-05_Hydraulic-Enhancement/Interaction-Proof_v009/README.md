# S05 v009 — One tracked group of cuttings

Status: focused Stage 6 proof ready for owner review. Three seconds, 72 frames at 24 fps. Full Section 5 integration remains unreleased.

## Review files

- `Previews/S05_tracked-cuttings_v009.mp4` — motion proof, no explanatory labels.
- `Previews/interaction_still.png` — native frame 36.
- `Previews/review.html` — looping review player and chronological contact sheet.
- `Scenes/S05_tracked-cuttings_v009.blend` — editable native, opened in Blender at frame 36.

The same three matte rocks enter from the lower right, turn through the open passage beside one twisted pad, and continue upward toward the upper left. The camera stays still. All three pieces stay in frame; none are spawned, hidden, scaled away or recycled. Previous wisps and staggered cuttings are disabled only in this successor. The accepted amber fluid domain stays as quiet context.

## What drives the bend

The path uses the existing v004 route sampled from the actual steel geometry. The route bends around the pad flank. At each time, the moving pad's angular position is considered when sampling the available radial space. A partial angular influence from the common hardware rotation shifts the path while the fragments advance independently upward. They are not children of the rotating hardware.

This is authored geometry-aware motion, not a force-based fluid or particle simulation. It illustrates transport around rotating geometry; it does not establish measured fluid velocity, particle dynamics, swirl, erosion, performance or operating RPM. Continuous upward transport is authored at 0.17 m/s for this viewing test. Hardware turns clockwise from the surface looking downhole at a slowed illustrative 5 degrees/s; no hardware axial translation was added. These values are animation choices.

## Changes and preserved foundation

- Same ENP3 linked meshes, source dimensions, connected rotation, borehole dimensions, fixed section and accepted annular fluid mesh.
- Stationary view direction retained; camera translated parallel to the image plane and lens changed to 58 mm to keep the complete trip comfortably visible.
- Fluid material copied: constant low density 2.5 replaces competing density texture motion for this test. Original material remains in the native.
- Three copied irregular matte fragments keep source mesh sizes (support diameters 14–16 mm), with small depth and side offsets and slow tumbling.
- Preview reduced to EEVEE 8 samples, 1280 x 720. No additional cinematic finishing.

## Verification

`Records/geometry-verification.json`: 143 times (72 output frames plus 71 halfway samples), complete fragment triangle tests against steel and annular boundary, plus vertex containment. No sampled intersections. Minimum fragment-to-steel distance 8.35 mm; wall clearance 1.83 mm; clearance inside the fluid boundary 0.83 mm. Complete fluid-domain triangle and vertex checks pass; common rigid rotation preserves its clearance from hardware. These are discrete geometry checks, not validated fluid physics or an all-time collision proof.

`Records/tracking-verification.json`: positive upward progression, no jumps/resets, no fragment-to-fragment intersections, no steel obstruction on camera-to-fragment-center rays. All fragment vertices stay inside roughly 17–83% of frame height and 18–82% of width. Camera transform is constant. The same three objects are visible throughout the sample range.

`Records/native-preservation.json`: reopened native retains valid relative shared-source link; accepted volume geometry and linked hardware match v008. Reopened frame 36 is pixel-identical to the batch render. v008 native and shared master hashes remain unchanged.

`Records/media-verification.json`: MP4 decoded successfully to all 72 frames. Final render/write mean 1.031 s/frame, maximum 1.190 s/frame. Initial 16-sample cold still took 5.463 s; samples were reduced before the batch. Working benchmarks at frames 1, 36 and 72 took 1.00–1.15 s. No final batch frame exceeded five seconds.

## Visual review and remaining decision

The chronological decoded frames show a single connected trip and a visible sideways bend beside the pad. Removing competing groups makes object identity easier to track. Fluid appearance is deliberately quiet, and the camera does not move. Normal-speed comprehension and the strength of the perceived pad-to-flow relationship still require owner review; technical checks do not establish acceptance.

Stop here. Do not restore extra effects or begin the 18-second section until the owner accepts the movement.

## Preservation and handoff

All earlier proofs and shared masters are preserved. Heavy native/video media stays local. A hash-verified D-drive recovery copy includes native, MP4 and the relative shared-library dependency; see `Records/local-backup.json`. It is a same-machine backup, not offsite storage. Scripts, reports and selected stills are published through the separate scoped publishing checkout. Exact publication evidence is recorded in local `Records/sync-verification.json` after push.

`Scripts/build.py` builds only from v008 into a new v009 path; it refuses overwrite. `finish_build.py` records the one-time completion after adjusting full-track framing during authoring. Verification and render/package scripts are included. Geometry-aware helper code and route samples are retained in the referenced v006 and v004 folders.
