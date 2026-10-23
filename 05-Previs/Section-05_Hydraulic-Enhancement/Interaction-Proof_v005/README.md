# S05 v005 — readable moving fluid and cuttings

23 October 2026 · Stage 6 bounded six-second revision · ready for owner review.

This version preserves v004's geometry, eighteen annular routes, depth distribution, upward transport and continuous clockwise tool rotation. It changes how the movement is shown: compact shaded amber segments replace the long bright trails, twelve matte chips travel with the flow, and the camera holds still for the middle four seconds.

- [Six-second video](Previews/S05_twisted-pad_interaction_v005.mp4), 1280×720, 24 fps, 144 frames.
- [Interaction still](Previews/interaction.png), [entry](Previews/entry.png), [exit](Previews/exit.png), [decoded chronology](Previews/motion-review.jpg).
- [Editable Blender scene](Scenes/S05_twisted-pad_interaction_v005.blend), reopened with its relative source link and left open at frame 72.
- [Previous v004 video](../Interaction-Proof_v004/Previews/S05_twisted-pad_interaction_v004.mp4) is preserved for comparison.

## Focused changes

**Fluid:** retain 28% of each existing visible movement history as a short rounded segment. Its maximum cross-section diameter increases from 1.7 to 2.6 mm, while emission drops from 0.65 to 0.16 and ordinary surface shading provides shape. Leading-centre animation and the three-depth placement remain unchanged. There are no persistent full-path guides in the rendered collection. Fifty fluid segments remain visible; four existing representative markers are instead shown as additional cuttings on those same trajectories. All eighteen routes remain represented by fluid segments.

**Cuttings:** twelve irregular, flattened, matte faceted chips, up from eight. Their maximum support diameter is 11.2 mm, fitted to available clearance, not a measured size distribution. Lighter neutral stone facets distinguish them from amber tracers. They have no emission or amber tails. Four added chips follow existing foreground fluid tracks; coincident fluid segments are hidden so the rocks cannot acquire an apparent spark tail. Existing chip motion continues; no independent decorative motion was added.

**Camera:** an exact hold at v004's middle composition for frames 25–120 (four seconds of output frames), with small eased moves before and after. The existing 48 mm lens and framing language remain. Tool and flow continue moving during the hold. No source hardware translation, pad-only rotation or borehole change is introduced.

These are illustrative tracer and chip display choices. Geometry-aware motion remains the authored v004 model, not CFD, calibrated particle transport, an operating-RPM claim or hydraulic-performance evidence. The source dimensions, provisional covers and unresolved source-stage/end identities remain as previously recorded. Full Section 5 is not built here.

## Checks and limits

- [Continuity](Records/continuity-verification.json): camera matrix is unchanged across the hold. All eighteen fluid routes remain. Evaluated leading centres differ from evaluated v004 by at most 0.000000239 m (floating-point scale). The earlier authored sample records differ slightly from Blender's absolute shape-key evaluation in both versions; the check compares evaluated source to evaluated successor. Original v004 hash is unchanged.
- [Output-frame geometry](Records/geometry-verification.json): 144 output times, 62 visible effect meshes, no steel intersections. Minimum sampled steel distance 2.68 mm; borehole-wall clearance 3.50 mm.
- [Midpoint geometry](Records/geometry-half-frame.json): 143 between-frame times also pass. Minimum sampled steel distance 2.13 mm. These 287 discrete checks are geometric evidence, not a proof at every continuous instant or a fluid-physics validation. Source CAD normals remain unsuitable as the sole exterior test; radial first-hit checks and triangle intersections are used separately.
- Shared source and original v001 hashes also remain unchanged. All ten hardware transforms preserve the existing rigid clockwise rotation and zero translation.
- [Representative benchmark](Records/benchmark.json): 0.770 / 0.545 / 0.516 seconds including file write. [Batch timings](Records/render-timings.json): mean **0.537 s/frame**, maximum **0.694 s/frame**. Every sample remains below five seconds and approximately one second; existing application caches were used.
- [Media verification](Records/media-verification.json): encoded H.264 decoded fully to 144 RGB frames. Stills come from the actual video. [Fresh-open check](Records/fresh-open.json): saved native reopened and the relative source library resolves.

Agent inspected the full-size interaction frame and twelve chronological decoded frames. The long-line appearance is reduced, stone chips have separate matte silhouettes, and the held composition isolates tool/flow movement. The shorter tracers also provide less persistent path context; normal-speed comprehension of the full incoming → interaction → redirection → upward sequence remains the owner's review decision. No independent viewer test, engineering approval or owner acceptance is claimed.

The existing [S05-B contract](../../../04-Production/Shots/S05/S05-B/direction.md) remains the controlling direction record. **Full 18-second integration and finishing remain unreleased.** Prior versions are retained. Native/video/cache stay local; no off-machine media backup is claimed. Scoped script/report/still publication is recorded in `Records/sync-receipt.json`.

Reproduction: open clean v004 and run `Scripts/refine.py` once with `__file__` set; it refuses an existing v005 output. Run `Scripts/verify.py` with default output times and with `HALF=True`, then `Scripts/verify_continuity.py`. Benchmark before `Scripts/render_chunk.py` using bounded `START`/`END`; package with `Scripts/package.py`. A failed initial build was discarded by reopening v004; its initial saved copy remains in Work. Final build clamps the tracer end-profile before fractional exponentiation. Preserve review candidates before any rerun.
