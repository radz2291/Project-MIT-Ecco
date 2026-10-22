# S05 — Twisted-pad interaction proof v001

23 October 2026. **Stage 6 limited proof, ready for owner review.** Direct authorization: [owner handoff](Records/Owner-handoff.txt) and subsequent request to use a new previs folder. This is not the complete Section 5 or a final render.

The proof shows a stationary ENP3 body inside a fixed half-section of the borehole. Fine flow guides bend between the actual raised pads. Moving tracer dashes and small matte rock fragments follow the same paths upward. The question for review is whether the pad shape visibly explains the change in flow direction.

## Review files

- [Six-second MP4](Previews/S05_twisted-pad_interaction_v001.mp4), 144 frames, 24 fps, 1280×720, silent normal-speed playback.
- [Review page](Previews/review.html), including video and matched palette comparison.
- [Editable Blender scene](Scenes/S05_twisted-pad_interaction_v001.blend).
- Same-video stills: [entry](Previews/entry.png), [interaction](Previews/interaction.png), [exit](Previews/exit.png).
- [Amber/cyan comparison](Previews/palette-comparison.jpg). Both historical directions preserved; amber is the trial MP4 palette, not a final palette decision.
- [Chronological decoded frames](Previews/motion-review.jpg).

Absolute root: `C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/05-Previs/Section-05_Hydraulic-Enhancement/Interaction-Proof_v001/`.

## Reused and new

Reused: linked mesh data from `04-Production/Shared/Assets/ECCO/ECCO_film_v002.blend`, including its provisional removable closures. Original 0.001 CAD unit conversion and 2.400 m housing length retained. Native -X uphole convention comes from the current T44/T48 layout. A rigid rotation puts return flow toward scene +Z. The simplified borehole inherits the existing 0.31115 m nominal ID; this is the project's illustrative open-hole scenario, not a new deployment qualification.

Inspected B204 v001 and T48 Hydraulics v003 references, implementation and existing preview stills. B204's separate schematic and provisional +X direction were not carried into the new scene. T48's outer-envelope paths were also not copied: they did not adequately expose the local pad interaction for this test. Their continuous guide / moving dash / matte-cutting language informed the new effects.

New: local linked-mesh wrappers with satin-steel material overrides; simplified fixed section and lighting; nine slender paths in three circumferential channel groups; 36 moving dashes and 18 faceted rock fragments; six-second close oblique upward camera move; editable quiet captions. No shared master edits or tool rotation/translation.

## Flow method and verification

An authored angular path follows the spaces between inspected raised surfaces. Radial raycasts and nearest-surface checks constrain its position outside the hardware. This is a geometry-aware illustration, **not** a fluid solver, CFD result, measured transport, or quantitative velocity/pressure prediction. Rock fragments use the same path and time field as the tracers. The display-domain loops fade at the ends; there is no physical recirculation loop.

- [Source dimensions and build](Records/build.json): actual source geometry inspected; product file SHA256 unchanged.
- [Geometry check](Records/geometry-verification.json): all visible local hardware triangles included; 21,600 path samples. Conservative full-effect support bound leaves at least 2.15 mm to hardware and 21.51 mm to the nominal wall. These are scene clearance checks, not fluid-physics validation. Hardware matrices remain fixed over all 144 frames.
- [First render](Records/benchmark-first.json): 1.213 s, including write, with the machine's existing GPU/application cache. No warmup render omitted. Fresh empty-cache performance was not tested.
- [All frame timings](Records/render-timings.json): average 0.516 s, slowest 0.722 s. Every batch frame and representative sample was below 5 s.
- [Media check](Records/media-verification.json): complete MP4 decoded as 144 RGB frames at 1280×720; six seconds at the encoded 24 fps. Entry/interaction/exit stills were extracted from this MP4.
- [Fresh-open check](Records/fresh-open.json): saved scene reopened successfully; relative product library resolves. The proof is open in Blender.

## Self-review and limitations

Inspected full-resolution entry/interaction/exit views, matched palettes and 12 chronological frames decoded from the MP4. The source pads are legible, the foreground guides turn between them, and the camera preserves that relationship. Fragment motion and camera movement are keyed continuously; normal-speed audience comprehension remains for the owner to assess. No independent viewer or engineering approval is claimed.

The rock fragments remain small at normal playback size. Sparse guides avoid covering the steel, but the reaction may still need stronger visual emphasis after review. Amber separates this from cyan acoustics; cyan offers a cooler alternative. Neither is locked here. Fluid is optically simplified and represented primarily by trajectories and suspended solids; opaque mud is intentionally absent.

Exact pin/box identity and certified accelerator/twisted-pad/diffuser face assignments remain unresolved in the source register. The close-up uses inspected raised/twisted morphology and is labeled illustrative. No claimed acceleration ratio, turbulence intensity, pressure recovery, wake benefit, or pack-off prevention is proven by these paths. The 2.400 m source / 2.25 m brochure discrepancy remains unchanged.

## Handoff and next step

The existing [S05-B Scene Direction Contract](../../../04-Production/Shots/S05/S05-B/direction.md) owns the approved decisions and implementation amendment; no parallel direction specification was created. Live Work revision 701 was read; T43/T44 are done and T48 is in review. No Section 5 execution ticket exists there. This proof uses the explicit chat authorization; no shared-asset ticket was reopened and no new ticket was invented.

Review the six-second video for one question: **does the flow visibly change direction because of the pad geometry, while carrying small rock fragments?** Then choose amber or cyan. Stop here for that review. Full 18-second S05 production, finishing, other-section retiming, narration/sound and film assembly are not released.

Native scene, MP4 and raw frames remain local. No off-machine media backup is claimed. Task-owned scripts, records and selected review images are eligible for Git publication; the synchronization receipt records the actual publication outcome. All previous sections and shared assets are preserved.

Reproduction: use Blender 5.2; run `Scripts/build.py` in an empty/review-safe Blender session, then `Scripts/refine_preview.py`. The builder refuses to overwrite the candidate. Run `Scripts/verify.py`, benchmark, then `Scripts/render_chunk.py` with bounded `START`/`END` globals. `Scripts/package.py` uses the project-local ffmpeg and Pillow. It deliberately does not modify existing production sources.
