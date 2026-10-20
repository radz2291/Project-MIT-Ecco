# S04 B/C v009 — formation fill and acquisition finish

21 October 2026. Owner approved exactly two amendments to v008. **Five-second matched B/C proof only. Part D remains paused; full18-second integration and final finishing remain unreleased.**

## Changes

1. **Rock fills the former blank margin.** A closed formation context volume extends to the edge of the existing camera frame. The imported Section2/v006 rock surface guides its inner profile where that source exists. The original sectioned wall is preserved but hidden in this successor. In unseen angular sectors, a nominal context continuation closes the display volume; this is illustrative surrounding geology, not a newly measured borehole reconstruction. The continuation stays outside the unchanged cement exterior. No camera, ECCO, steel, cement, channel or internal-fluid geometry change.
2. **Acquisition-style finish on the existing response.** The exact v008 response envelopes are retained and recorded. A faint smooth carrier supports thin, irregular scan segments attached to the same inner-steel and exposed-thickness footprint. Stronger interruptions occur just after contact, then quieter interruptions follow the original fade. The deterministic pattern is shared by B/C; the existing B/C decay difference drives their duration. No spatial jitter, displaced steel, floating cubes, camera shake or permanent data map.

The cyan sends, emerald primary return and finer response tails are unchanged over all120 frames. The display flicker represents information acquisition; it does not claim that steel physically glitches or that a calibrated recording sequence has been simulated. The underlying qualitative pulse-echo interpretation and all v008 limitations remain in force.

## Review files

- `../Previews/S04_BC_matched-acquisition_v009.mp4`: synchronized five-second comparison,24fps. Physical image1280x720 per case; caption bars outside it.
- Individual `S04_B_formation-acquisition_v009.mp4` and `S04_C_formation-acquisition_v009.mp4`.
- `S04_BC_establish_unlabelled_v009.png`, `S04_BC_contact_unlabelled_v009.png`, `S04_BC_glitch_unlabelled_v009.png`, and `S04_BC_decay_unlabelled_v009.png`: exact delivered frames with no added guide.
- `S04_B_material-guide_v009.png` and `S04_C_material-guide_v009.png`: labels only, using the exact native video camera, physical geometry, materials and frame25.
- `../Scenes/S04_B_formation-acquisition_v009.blend` and `S04_C_formation-acquisition_v009.blend`: editable candidates with baked playback; no Python handler needed.

## Verification and review limits

`verification.json` compares the actual v008/v009 native meshes and transforms for steel, cement, channel and internal fluid. Full120-frame hashes compare the camera, tool controls, send/return/tail positions, scales, visibility and colors. Original response-envelope values are compared separately. The formation is closed/manifold and its minimum radius is checked against the cement exterior; camera rays sample the former blank left margin. Scan fragments remain fixed; only display alpha/visibility changes. Relative libraries reopen and resolve.

The first context version translated the whole formation by the old50-micrometre section offset. The clearance check detected that this could bring an unseen inner sector slightly inside the cement envelope. The delivered context uses its own zero-offset section plane and passes the clearance check. Initial draft render costs are retained separately in `superseded-context-offset-batch.json`; they are not the delivered render total.

Representative stills show continuous rock context and surface-attached digital segments. They do not constitute independent audience comprehension, owner approval or a claim that every frame was watched at normal speed. Review the moving proof to judge whether the acquisition finish is restrained enough and whether the longer C response remains clear. Rock and fluid materials remain inexpensive playblast treatments.

`media-verification.json` and `timings-B/C.json` record the delivered frames, mean/max/total render times and complete MP4 decode checks. Setup, source loads, benchmarks, guide stills, encoding and earlier attempts are separate from delivered frame-render totals. No expensive final render.

Delivered B:120 frames,44.631 s total,0.372 s mean,1.078 s maximum. C:120 frames,45.209 s total,0.377 s mean,1.014 s maximum. Combined delivered frame rendering89.840 s (1 min29.8 s). All delivered frames are strictly under5 seconds. Three MP4 files decoded completely; chronological establish/send/contact/glitch/decay stills were inspected. Native physical and travelling-wave comparisons pass; actual carrier alpha matches10 percent of the source envelope within floating-point tolerance, and acquisition masks never exceed their source envelope.

Previous versions and shared masters are preserved. Native scenes and media remain local; report/script synchronization is not a native-media backup. The existing Scene Direction Contract remains the sole decision record.
