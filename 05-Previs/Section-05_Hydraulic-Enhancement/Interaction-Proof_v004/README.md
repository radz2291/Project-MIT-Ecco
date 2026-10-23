# S05 v004 — flow distributed through the annulus

23 October 2026 · Stage 6 six-second proof · ready for owner review.

The new proof spreads amber trajectories around the tool and through several depths of the open passages, including the central winding passage marked in the owner's image. Moving pads influence their routes, while fluid and cuttings keep travelling upward independently. Camera, physical source geometry, clockwise whole-tool rotation, restrained amber treatment and fixed half-section remain unchanged.

- [Six-second MP4](Previews/S05_twisted-pad_interaction_v004.mp4), 1280×720, 24 fps, 144 frames.
- [Interaction still](Previews/interaction.png), [entry](Previews/entry.png), [exit](Previews/exit.png), [decoded chronology](Previews/motion-review.jpg).
- [Editable Blender scene](Scenes/S05_twisted-pad_interaction_v004.blend), reopened with the relative source link and left open at frame 72.
- [Prior v003](../Interaction-Proof_v003/Previews/S05_twisted-pad_interaction_v003.mp4) remains available for comparison.

## Inspection and change

v003 concentrated trajectories around three narrow authored angular groups and approximately one radius. Inspection against the actual ten-object mesh assembly found wide open passages elsewhere. A 23,580-sample circumferential clearance map records the real source surface at 2-degree / 10-mm spacing. The map is a geometric inspection, not a fluid solution.

Eighteen representative circumferential routes now follow that clearance map. Fifty-four fluid markers use staggered phases, slightly different upward speeds and three depth fractions (32%, 58%, 80%) of the usable local annular gap. Eight matte rock fragments use the same family of routes with their own finite-size clearance. Fluid tail head diameter is 1.7 mm; rock trails are finer. No broad glow ribbons or new bloom are introduced.

Routes are planned through the measured open spaces with a conservative angular margin. At each 120-Hz history sample, the finite particle footprint is checked against the actual rotating mesh and its radius is placed within the usable gap. Angular motion follows a spatially varying fraction of tool rotation, 32% away from the interaction and up to 75% near it, plus the changing route shape during upward travel. This is deliberately partial coupling, not rigid parenting. All effects remain separate world-space objects. No constriction-side fallback corrections were needed in this candidate.

These are authored kinematic trajectories, not a momentum/pressure solver, measured transport, actual operating RPM or demonstrated cleaning benefit. The geometric map and finite clearances do not turn this into CFD. Inherited source-stage identification, provisional covers, axis conventions and dimensional limitations remain as recorded in v002. Tool geometry is not widened or changed for the effects.

Movement-history tails remain. Their visible length shortens before current steel overtakes older positions. Hidden display-domain recycling uses stepped interpolation at the endpoints to avoid an artificial interpolated trip back through the tool; this is not physical recirculation. The output keeps continuous incoming, pad-interaction and outgoing populations.

## Evidence

- [Coverage comparison](Records/coverage-comparison.json): over six seconds, v004 fluid heads visit 105 diagnostic 10-cm × 30-degree cells versus 51 for v003, and all 12 angular sectors versus nine. Radius range expands from 137.0–141.8 mm to 121.8–150.7 mm. These describe representative marker coverage only, not a fraction of real fluid, uniform flow or complete volumetric sampling. All non-reset v004 sampled axial steps are positive.
- [Output-frame geometry](Records/geometry-verification.json): 144 frames, 70 effect meshes, 736,704 sampled vertices; no effect/hardware triangle intersections. Minimum sampled steel distance 1.85 mm and wall clearance 3.95 mm.
- [Between-frame geometry](Records/geometry-half-frame.json): 143 halfway times also passed complete effect/hardware triangle-intersection and sampled radial-exterior checks. Minimum sampled steel distance 0.501 mm. Combined evidence covers 287 discrete times, not every continuous instant or physical validity. Source CAD nearest-normal signs remain unsuitable as the sole exterior test; radial first-hit checks and triangle intersections are used separately.
- Source and original v001 hashes remain unchanged; v003 native hash is retained in [build record](Records/build.json). All ten hardware transforms preserve rigid clockwise rotation and zero translation. Unchanged maximum tool-to-wall gap: 3.175 mm.
- [Benchmark](Records/benchmark.json): representative render/write samples 0.770 / 0.568 / 0.574 seconds. [Batch](Records/render-timings.json): mean **0.573 s/frame**, maximum **0.871 s/frame**. All below five seconds, and below the approximate one-second iteration target. Existing application caches were used; empty-cache performance is untested.
- [Media](Records/media-verification.json): actual H.264 MP4 decoded completely to 144 RGB frames. Review stills come from the encoded video. [Fresh-open check](Records/fresh-open.json): saved native reopened and source link resolves.

## Review and handoff

Agent inspected the full-size interaction frame and twelve chronological decoded frames. The central winding route now contains visible flow, the foreground markers occupy different depths, and the ordered triplet appearance is reduced. Some paths necessarily overlap steel in the 2D projection while remaining physically clear in 3D; whether the volume reads clearly at normal playback is the owner review question. No independent viewer test, engineering certification or approval is claimed.

The existing [S05-B contract](../../../04-Production/Shots/S05/S05-B/direction.md) remains the decision record. **Full 18-second integration and finishing are not released.** Prior proofs and shared masters remain intact. Native/video/cache stay local; no off-machine media backup is claimed. Publication of scripts, records and selected stills is recorded in `Records/sync-receipt.json`; no global primary-checkout synchronization claim is made.

Reproduce from clean v003: retain `Records/surface-map.json`, run `Scripts/build.py` once with `__file__` set, then `Scripts/interpolation_safety.py`. The builder refuses an existing v004 output. Run `Scripts/verify.py` for output frames and with `HALF=True` for midpoint checks; benchmark, render bounded ranges with `Scripts/render_chunk.py`, then package with `Scripts/package.py`. `Scripts/coverage.py` compares retained v003/v004 head records. Preserve saved candidates before rerunning builders.
