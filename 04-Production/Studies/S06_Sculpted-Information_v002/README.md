# S06 v002 — Sculpted Information

**Review candidate.** Radzi's 25 October 2026 handoff accepts v001's unfolding mechanism and authorizes this targeted 12-second cinematic revision. That acceptance does not cover this new camera/report treatment, final finishing, engineering certification or client approval. This is the single working direction and closure record.

## What changed

The opening is closer and more oblique, with perspective, raking light and more section contours taken directly from the existing geometry. The silhouette shows the source enlargement. The camera moves toward the open side of the representation as it unfolds, then straightens and pulls back to a calm, light multi-track report. The original 24,000 samples, sample IDs, longitudinal seam and all 33 saved unfolding shapes are retained exactly.

The report now contains diameter profiles, three source-derived cross-sections, a small 3D reconstruction, the original unfolding surface as the 360-degree geometry track, an azimuthal radius-spread curve and an independently authored warm amplitude track. It is a replaceable **Illustrative data** demonstrator, not actual Mi-VU software output or ENP3 field evidence.

## Scene direction

| Time | Discovery | Camera purpose |
|---|---|---|
| 0–3 s | A dimensional borehole reconstruction, including a blue enlargement | Oblique perspective with the circular opening, full length and radial outline visible; gentle arc |
| 3–9 s | The same colored samples open into an angle/depth map | Move toward the open seam side, then progressively straighten; retain the blue feature |
| 9–12 s | Related engineering outputs can be read together | Ease back into a nearly frontal report and hold; no scrolling |

The exact camera and event samples are in `Records/camera-score.json`. Geometry finishes flattening at frame 211, just before 9 seconds; the report reveals from frames 217–253 and settles for the ending. Final film position 1:16–1:28 remains editorial, not a change to the film assembly.

**Visual communication check:** recognize an irregular data surface; locate its seam and depth direction; follow the blue feature from curved to flat; avoid implying physical rock stretching, live telemetry or geometry becoming amplitude; inspect arrival frames, frame sampling, the encoded 12-second playback and numerical correspondence separately.

## Sources and truth

- Base native: `../S06_Sculpted-Information_v001/Scenes/S06_journey_v001.blend`. v001 and the user's dirty live Blender session remain untouched.
- Geometry: exact v001 `surface_samples.npz`, originally selected from Section 3 v023's authored radius field. This is synthetic illustrative geometry, not measured field data. See `Records/source.json` for source rows, columns, hash and coordinate conventions.
- Depth increases down. Azimuth 0–360° is relative to the visualization seam at original source 240°, not geographic north. Both seam edges duplicate the same samples.
- Radius values are unchanged. The original face normals pointed inward; v002 reverses face winding for outward shading without moving vertices or changing sample IDs. Extra section contours sample the retained shape keys.
- Diameter profiles are calculated as `r(theta,z) + r(theta+pi,z)`, then min/mean/max across azimuth at each depth. This is opposite-radius diameter about the source axis, not an arbitrary caliper or tool-eccentricity solution.
- Cross-sections use rows 27, 62 and 99 of the retained subset. The variation track is standard deviation of radius across azimuth, **not** repeated-run variance or a field uncertainty estimate. `Data/derived_report_arrays.npz` retains the plotted values.
- `Data/independent_amplitude.npz` is a separately defined analytic illustration on the same relative depth/azimuth coordinates. Its formula uses angle/depth alone, never radius values. It is not an acoustic simulation, inferred lithology, a recolored geometry map or a genuine measurement of this interval. Generator and separation are documented in `Scripts/refine.py` and `Records/refinement.json`.
- Colors preserve white near nominal, blue enlarged and red tight. Warm colors belong only to the separate amplitude demonstrator. No calibrated field numbers are displayed.
- Detailed output is retrieved and processed after the run. No high-bandwidth live telemetry, new product performance or instrument-accuracy claim is made.
- Only the generated public storyboard composition references were inspected. No confidential LipanBara image/readings are reproduced. No ENP1 example is relabeled ENP3.

## Authority and implementation

The active source is the local-only `Records/owner-handoff.txt`. The actual Rolladice storyboard was read at revision 14, limited to S06-A/B/C shot cards and their corresponding generated images. Their composition and report breadth informed the revision; their old timings, mechanism-building workflow and historical `direction.md` files were not adopted. Current architecture is 3/6/3 seconds.

Scene Establishment v1.1.0 was read from the current publishing checkout, alongside AI Director, Scene Director, creative personality, camera language and engineering/source guidance. Three arrival compositions were rendered and reviewed before the final path was baked. Initial tests exposed crop, bright highlights and seam occlusion; framing, light power and approach side were corrected. No alternate unfolding mechanism was created.

Live Work revision 747 has no S06-v002 ticket. Execution follows this direct owner handoff; no old ticket was resumed, duplicate ticket invented or unrelated status changed. Official Blender Lab MCP was used for a read-only live-scene check. Isolated Blender 5.2 background processes built and rendered the successor.

## Deliverables

- [12-second cinematic study](Previews/S06_cinematic-study_v002.mp4)
- [Three arrival stills](Previews/S06_three-arrivals_v002.jpg)
- Individual stills: `Previews/S06_arrival_01_v002.png`, `02`, `03`; the last is the report composition.
- [Editable scene](Scenes/S06_cinematic-study_v002.blend)
- [Appendable unfolding collection](Scenes/S06_unfolding-component_v002.blend): append `S06_UNFOLD_COMPONENT_v002`; includes 43 source-matched mesh/contour objects with baked unfolding controls.
- Native mesh attributes and 33 shape keys retain reusable unfolding controls; `Scripts/refine.py` extends v001 rather than rebuilding its mechanism.
- [Motion sampling](Previews/S06_motion-sampling_v002.jpg) and local `Previews/review.html` player.
- Source-level checks: `Records/verification.json`. Render/decode checks: `Records/benchmark.json`, `render-timings.json`, `media-verification.json`.

## Self-review and remaining limits

The opening gives the surface more presence and makes its enlargement outline easier to inspect than v001. The middle view shows two separating seam edges, and the report has substantially clearer breadth and hierarchy. The blue enlargement is unobstructed and inside the image throughout all 288 frames according to scene ray casts and projection checks. The smaller red region is hidden by the cylindrical surface during the early view and becomes readable during flattening; the blue region is the continuous landmark.

This source remains smoother than the deliberately dramatic generated storyboard. The tight region is shallow and subtle. No radius exaggeration was applied to imitate that artwork. Fine secondary report text is intended to support output recognition, not be read completely in three seconds. This is a silent preview; narration, sound and independent viewer/engineering review remain outside the completed checks.

Technical checks reopen the saved native, compare all shape keys and sample values with v001/original source, verify depth/seam correspondence, recalculate report curves, regenerate the independent amplitude field, and inspect dependencies. These are implementation checks, not engineering signoff.

The actual MP4 was decoded in full (288 frames, no decoder errors) and played through to 12.00 seconds at 1× in the local review player. Browser captures at presentation size and rendered time samples were inspected; this is agent playback/frame review, not an independent cold-viewer test. The report edges enter the frame during the pullback and are fully contained for the final hold.

**Rendering:** EEVEE, 16 samples, 1280×720, 24 fps. Delivered animation: **0.479 seconds/frame average**, **4.207 seconds maximum**, **138.084 seconds total frame rendering**. All 288 frames and the three pre-batch benchmark frames passed the strict under-five-second cap. Total excludes setup, exploratory arrival tests, benchmarks, source validation and video encoding. Exact evidence is in `Records/media-verification.json`.

## Storage and stop boundary

Scenes, videos and raw frame cache remain local. Selected review stills, source arrays, scripts and records are permitted for source control. Publication uses the isolated D: publishing checkout to preserve unrelated C: changes. Exact candidate hashes, backup destination and remote SHA are recorded in `Records/asset-manifest.json` and local `Records/sync-verification.json`.

Stop after this v002 study for owner review. No Section 7, final finishing or full-film assembly has begun.
