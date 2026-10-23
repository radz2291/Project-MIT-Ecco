# S05 — Hydraulic interaction v002

**23 October 2026 · Stage 6 bounded proof · ready for owner review.**

The whole instrument turns slowly while amber markers and visible rock fragments travel upward around the actual pads. Longer, tapered tails show the curved flow pattern behind each moving element. The camera and source geometry are retained from v001. This is the requested six-second revision; full 18-second integration remains unreleased.

## Review

- [Six-second video](Previews/S05_twisted-pad_interaction_v002.mp4) — 1280×720, 24 fps, 144 frames.
- [Interaction still](Previews/interaction.png), [entry](Previews/entry.png), [exit](Previews/exit.png), [decoded chronology](Previews/motion-review.jpg).
- [Review page](Previews/review.html).
- [Editable Blender scene](Scenes/S05_twisted-pad_interaction_v002.blend), reopened successfully and left open at frame 72.

Root: `C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/05-Previs/Section-05_Hydraulic-Enhancement/Interaction-Proof_v002/`.

## What changed

27 moving fluid markers replace the static complete guides. Each has a tapered amber tail, up to 190 mm long and 2.3 mm diameter at its head; eight matte, irregular fragments have finer 115 mm tails. These are illustrative display dimensions, not measured particle sizes. Tails shorten at constrained corners rather than being forced through metal. They are narrow curves, without bloom or broad glowing bands. The later owner amendment specifically requested these longer moving tails to recover v001's readable pattern.

All ten existing linked hardware wrappers rotate together about the original tool axis. The root turns at an authored -5 degrees per second about world Z, approximately 30 degrees over six seconds. World +Z points toward the surface in the inherited layout, so this is clockwise from the surface looking downhole. There is no translation or independent pad rotation. Timing is slowed for explanation and is not an operating-RPM claim. The full 18-second rotation scenario is requested but has not been built or checked here.

The 48 mm camera, original gentle camera move, fixed half-borehole, lighting and satin-steel treatment remain. Amber is now owner-approved. Original source unit conversion, 2.400 m housing length, and the inherited 0.31115 m nominal borehole ID are retained. Shared source: `04-Production/Shared/Assets/ECCO/ECCO_film_v002.blend`, with its existing provisional covers. Original v001 and shared source hashes remain unchanged.

## Engineering assessment and method

Adding rotation changes the operating illustration to combined circulation and rotation. Nearby fluid can acquire sideways motion from the turning tool; the effect depends on geometry, fluid properties and operating conditions. [Sun et al., 2014](https://link.springer.com/article/10.1007/s13202-014-0118-x) supports that general mechanism, but studies a different configuration and does not validate these ENP3 paths or any transport benefit.

This proof uses an authored world-space velocity field, geometry-aware channel steering, partial tangential entrainment and moving-boundary avoidance. Particle centres are advanced at 120 Hz with a six-second preroll. Rocks use the same field with their own finite-size clearance. Positions are constrained against all ten actual hardware meshes and the borehole envelope. They are not parented to the rotating tool. Tails are short current-time direction traces behind each advected element, recomputed around the current pad orientation. They are **not literal histories of previously occupied fluid positions**, a fluid simulation, measured velocities or a prediction of pressure/turbulence/cleaning efficiency. The display domain resets beyond its endpoints; it is not a physical recirculation loop.

Exact product stage labels and pin/box identity remain unresolved from the inherited source register. No new certified deployment dimensions, performance claim or end identification is inferred. No BHA parts absent from the proof were added.

## Verification

- [Geometry verification](Records/geometry-verification.json): all 144 rendered frames checked. No triangle intersections found between complete visible effect meshes and hardware. 417,888 sampled effect vertices passed exterior radial first-hit checks. Minimum sampled hardware distance 1.19 mm; minimum sampled borehole-wall clearance 1.15 mm. Whole-tool wall clearance is 3.175 mm. Rigid transforms and zero translation verified for all ten hardware objects. These are geometric checks, not physics validation.
- Source CAD nearest-face normal signs were ambiguous at some concave regions. A first signed-normal assertion failed; the final check uses separate radial exterior tests plus complete triangle-intersection checks. This limitation and the raw signed result are retained in the verification record. Source geometry was not changed to make a test pass.
- Checks cover output frames, not a proof of all continuous subframe geometry. Motion blur is off. Tails use linear absolute shape-key interpolation; boundary re-entry is a display convention.
- [Representative render benchmark](Records/benchmark-tails.json): 0.730 / 0.506 / 0.493 seconds including file write at frames 1 / 72 / 144, on existing application/GPU caches. Empty-cache performance was not tested.
- [144-frame render timings](Records/render-timings.json): mean **0.527 seconds**, maximum **0.702 seconds**. All representative and batch frames below the strict five-second cap.
- [Media verification](Records/media-verification.json): complete H.264 MP4 decoded to 144 RGB frames. Review stills are extracted from the actual video.
- [Fresh-open verification](Records/fresh-open.json): editable scene reopened, relative source link resolves, EEVEE 1280×720 at 24 fps. Source native and v001 hashes verified unchanged.

## Review assessment and handoff

Agent inspected full-size interaction/exit samples and twelve chronological frames decoded from the video. The tails visibly curve between raised pads, fragments remain matte faceted objects, and the tool changes orientation while the camera retains the channel. Readability at normal playback is for the owner to judge; no independent viewer test, engineering certification or owner approval is claimed. Three foreground lanes are deliberately orderly; whether they still feel too diagrammatic is the main remaining creative review question.

Review question: **Can you see the instrument rotating, fluid moving upward, and the pads changing the route of fluid and rock fragments?**

The controlling amendment is in the existing [S05-B Scene Direction Contract](../../../04-Production/Shots/S05/S05-B/direction.md). Full Section 5 integration and finishing remain on hold for review of this proof. Radzi owns film assembly and sound. No new Work ticket was invented or completed shared-asset ticket reopened.

All prior versions and shared masters are preserved. Heavy native, video and frame files remain local; no off-machine media backup is claimed. Scripts, reports and selected stills are published separately with the actual result in `Records/sync-receipt.json`.

## Reproduce

Open clean v001 in Blender 5.2, run `Scripts/revise.py` with `__file__` set; it refuses to overwrite an existing v002 candidate. Run `Scripts/long_tails.py` once in the new candidate, then `Scripts/verify.py`. Benchmark before running `Scripts/render_chunk.py` in bounded `START`/`END` ranges. `Scripts/package.py` uses project-local ffmpeg and Pillow. Existing saved outputs must be preserved before rerunning builders. Failed intermediate tail construction was discarded by reopening the saved v002 candidate before the corrected tail build.
