# S05 v010 — Combined hydraulic interaction proof

Status: four-second Stage 6 proof ready for owner review. Full 18-second Section 5 remains unreleased.

## Review

- `Previews/S05_combined-interaction_v010.mp4` — 96 frames / 24 fps / four seconds, no explanatory labels.
- `Previews/interaction_still.png` — exact native frame 48.
- `Previews/review.html` — looping player and decoded chronological contact sheet.
- `Scenes/S05_combined-interaction_v010.blend` — editable native, open in Blender at frame 48.

The same three rocks approach from the lower right, bend sideways beside the rotating pad, and continue toward the upper left. Moving amber wisps precede and follow them. The fixed view exposes the amber passage between steel and the borehole boundary. This is the combined movement test requested by the owner, not final cinematic finishing.

## Diagnosis and reuse

v009 replaced v008's animated density with a constant density of 2.5 and disabled the internal wisps. That explained the lost impression of circulation. v010 appends the actual `S05_v007_SectionedFluid` material from the v008 native, including its animation. Node inputs, curve points, links, surface method and full fluid mesh match v008 at frame 1. Original upward density movement and partial angular motion continue through frame 96 using linear extrapolation.

The three persistent v009 rock meshes and matte materials are reused. No fragments spawn, disappear, shrink or reset. Their path uses the same geometry-aware route and rotation influence, with slightly more outward placement inside the existing clearance. Travel is spread over four seconds at an authored 0.135 m/s.

v006's stationary focused-camera approach is retained. The camera azimuth changes to 0 degrees, with its 49 mm lens, a diagonal composition and a small fixed lens shift to keep the complete trip in frame. A tested -10-degree view was rejected because some rocks became hidden. The static half-section azimuth changes from +25 to -20 degrees so the borehole boundary remains visible behind the selected fluid passage. This is a fixed presentation change: no opening animation, altered borehole radius or changed hardware geometry.

Eighteen soft non-emissive wisps reuse v008's material and mesh treatment, with v004 open-passage routes 0, 2, 4 and 16. Nine support the tracked group; nine quieter cues cover other representative passages. The full accepted fluid annulus remains. This deliberately uses selected paths, not all 18 v004 routes at equal density.

## How movement is coupled

The actual steel mesh supplies the radial clearance map and the existing curved route around the pad flank. Positions sample that geometry at the hardware's changing orientation. The path receives partial angular influence while advancing independently upward; no moving fragment or wisp is parented to steel. The common hardware root continues clockwise from the surface looking downhole at an illustrative 5 degrees/s, without axial translation.

The accepted density pattern advects upward at its original authored 0.20 m/s with 60% angular influence. Cuttings and supporting wisps travel at 0.135 m/s using the existing position-dependent 32–75% angular influence. Both are explanatory movement cues in the same passage; these are not solved velocities, physical density values or validated particle slip. No CFD, measured RPM or hydraulic-performance claim is made.

## Evidence

- `Records/geometry-verification.json`: all 96 output frames plus 95 halfway samples; full moving-element triangle tests against steel and the fluid boundary, plus vertex containment. No sampled intersections. Minimum moving-element steel distance 11.36 mm; borehole clearance 1.68 mm; remaining margin inside the displayed fluid boundary 0.68 mm. Static full-domain checks and common rigid rotation preserve fluid/steel separation.
- `Records/tracking-verification.json`: the same three rocks stay in frame, have positive upward progression, no sampled pair intersections and no steel obstruction on camera-to-center rays. Camera stays fixed. The middle fragment spans about 136 pixels perpendicular to the projected tool axis and bends about 102 pixels away from the line joining its screen-space endpoints at 1280 x 720. These screen measurements demonstrate a geometric bend, not viewer comprehension.
- `Records/native-preservation.json`: reopened source has a valid relative shared-master link. Hardware and borehole meshes match v008, and the restored fluid material matches. Density animation continues beyond frame 72. Reopened frame 48 is pixel-identical to the batch render.
- `Records/media-verification.json`: all 96 MP4 frames decode successfully. EEVEE 8 samples, 1280 x 720. Batch mean 1.061 seconds/frame; maximum 1.362 seconds/frame. Representative frame benchmarks also pass the strict five-second cap.
- `Records/local-backup.json`: v008, v009 and shared master hashes remain unchanged; new native, MP4 and relative shared dependency have matching D-drive recovery copies.

## Review boundary

Agent review inspected the static comparison and 12 chronological decoded video frames. The fragments move from approach to the outside of the pad profile, then continue upward, while other amber cues keep circulating. The fluid motion regression is repaired and the geometric bend is visible in the sequence. The precise question for owner normal-speed playback remains: does this read as circulating fluid being redirected and carrying cuttings, rather than surface-attached graphics? No owner or engineering acceptance is inferred from technical checks.

Stop after this focused proof. Full Section 5 integration and finishing are not started.

## Source and handoff

Owner's v010 request is the direct release. Live Rolladice Work revision 701 was read: historical S05 storyboard tasks are not resumed and no v010 proof ticket is fabricated. This report and the existing `04-Production/Shots/S05/S05-B/direction.md` hold the local proof record.

Build order: `Scripts/setup.py` from v009 into a new v010 path, then `add_motion.py`, then `finish_composition.py`. These preserve earlier natives. Verification, rendering and packaging scripts accompany the result. The route table and helper remain in v004 and v006. Full native/video/cache media stays local; D backup is on the same machine, not offsite. Scripts, reports and selected stills are published through the scoped D publishing checkout, preserving unrelated production-checkout changes. Exact remote evidence is recorded locally in `Records/sync-verification.json` after publication.
