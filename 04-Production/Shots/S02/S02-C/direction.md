# S02-C — The Hidden Circumference

Scene Direction Contract v0.2 · shot version v001 · T43 · 18 October 2026

## State and authority

D0 complete. Approved shared concept and narration-led responsibility split apply. This detailed brief is released as a **D1 implementation test**, submitted for Radzi's review; it is not D2 execution-ready, D3 motion-approved or D4 final-approved. No production is launched by T43.

Authority: engineering/client facts → project/brand constraints → narrative → documented taste → this composition → execution convenience. Sources: [S02-C.md](/04-Production/Records/Storyboard-Board-V3/Shots/S02-C.md), [shared-direction_v001.md](/04-Production/Records/Tasks/T-043/shared-direction_v001.md), [release-index_v001.md](/04-Production/Records/Tasks/T-043/release-index_v001.md), [component-register_v001.md](/04-Production/Records/Tasks/T-042/component-register_v001.md), [07-SCENE_DIRECTION_CONTRACT_v0.2.md](/03-Context/03_Directorial_Identity/07-SCENE_DIRECTION_CONTRACT_v0.2.md). T42 inspection is inherited evidence, not a fresh Blender inspection by this director.

## Purpose, audience and premise

**Nontechnical takeaway:** Repeated directional readings reveal the wall around ECCO.

Audience: engineers and nontechnical stakeholders with mixed prior knowledge. Intended feeling: Expansion from one point to a surrounding shape. The value of this moment is making the stated relationship understandable without an unsupported performance claim. The central image and expert-verifiable meaning are the physical/data relationship below, not decorative activity.

**Narration cue:** And as ECCO turns… the unseen begins to take shape. This cue is thematic, not a replacement script or timed recording. Narration carries meaning and significance; imagery carries the discovery. Review comprehension with the intended narration (temporary read is sufficient). Voice-recording synchronization is outside T43 and does not block this brief.

## Camera score and objects/events

Film window: **17–22 s**; content duration **5 s**. Local seconds below are editorial targets, not measured mechanism cadence or fixed recording timing.

Pull back and shallow arc toward oblique along-axis view. Keep recognizable tool and near wall as landmarks; avoid abrupt orthographic jump.

| Local seconds | Visual event / gaze / arrival |
|---|---|
| 0–1.3 | Retreat from retained point to reveal another side. |
| 1.3–3.1 | Whole assembly rotation adds wall-fixed samples at different azimuths. |
| 3.1–4.3 | Partial traces become one readable irregular circumference. |
| 4.3–5 | Settle on that cross-sectional payoff, leaving space for nominal comparison. |

**Entry:** Same point, dataset and orientation as S02-B.

**Exit:** Retain exact measured outline/camera side into S03-A; nominal reference enters next.

Maintain occlusion and object identity through travel; use the stated cut/reveal rather than penetrating opaque hardware. Product/effect motion is authored in Blender; source measurements govern spatial registration. Separate camera path and gaze where useful; slow into meaningful arrivals. Exact poses, focal length, clipping and keyframes are derived from the inspected scene. This beat table is the canonical conceptual spatial score; no precision camera diagram or extra 3D storyboard is required.

## Look, lighting and atmosphere

Rock detail recedes selectively as persistent measured points take priority. Sparse trace, no dense luminous cage.

Shared tactile rock/fluid and satin metal apply where present. A broad motivated grazing key reveals shape, restrained rim separates silhouettes, and dark negative space protects the discovery. Metallic reflections describe real geometry. Downhole illumination is an explanatory lighting convention, not literal sunlight. Use depth/parallax before fog; keep fluid present without expensive volume scattering. Candidate finishes are art direction, not MIT material certification.

## Engineering information and graphics

**Fixed technical boundary / expert truth check:** One sensor plane, 120° layout; no independent rotating head. Do not claim instantaneous complete volume or that all returns occur simultaneously. Any interpolated trace identified in source manifest.

**Exact copy / information treatment:** None; narration carries turning/shape. Copy specified here is proposed for this implementation test unless already mandated by provenance; omission of optional copy is permitted when narration and imagery suffice. Required synthetic-data identification cannot be omitted. Use calm editable sans serif, stable reading positions, quiet entrances and limited simultaneous information. Font/license, scale and moving legibility must be verified at preview resolution.

Information lifecycle: introduce only at its corresponding beat; anchor measurement to its source location; retain the stated comparison through its reading hold; remove or explicitly switch channel at the exit. Physical lighting is not data. Illustrative acoustic/flow graphics do not assert visible emission, calibrated velocity or simulation results. Never invent values to improve contrast. Preserve missing/invalid samples and label interpolation; real/synthetic provenance must survive into maps and reports.

## Asset register and implementation handoff

- **ECCO:** `04-Production/Shared/Assets/ECCO/ECCO_master_temporary-plugs_v002.blend` (registered native source; absent from Git tree, resolve in production workspace) ECCO_MASTER_v002; source longitudinal X in metres. Inspect actual sensor face/datum. Do not rescale 2.4 m to 2.25 m. Controls ECCO_ROOT, ECCO_ROTATION_X and ECCO_SENSOR_REF_01–03.
- **BHA:** `04-Production/Shared/Assets/WellAssembly/WellAssembly_variants_v003.blend` (registered native source; absent from Git tree, resolve in production workspace) WELL_ASSEMBLY_v003 / ASSEMBLY_CONTROL. Bit/adapters simplified; refine visible silhouettes only after source inspection. Avoid duplicated linked ECCO.
- **WELL:** `04-Production/Shared/Assets/WellAssembly/WellAssembly_variants_v003.blend` (registered native source; absent from Git tree, resolve in production workspace) Reuse registered spatial variants; inspect scale, layer ordering and boundaries.
- **MUD:** New implementation required; no existing asset claimed. New shared fluid visibility wrapper; bounded optical simplification, never a dry void.
- **ACOUSTICS:** `04-Production/Mechanisms/B201/Scenes/B201_pulse-echo_refinement_v006.blend` (registered native source; absent from Git tree, resolve in production workspace) Candidate source; preserve v005 baseline. Same-sensor send/return; actual engineering speed is not cinematic event duration.
- **DATA:** `04-Production/Mechanisms/B202/Scenes/B202_measured-envelope_master_v009.blend` (registered native source; absent from Git tree, resolve in production workspace) Data/v009/index_v009.json in B202 identifies cases. Preserve sample IDs, values, validity, source poses, fixed transfer functions and interpolation provenance.

**Shot-specific work:** B202 v009 valid sample events; isolate documented depth bin/station for ring while preserving real acquisition poses. No synthetic re-positioning of samples to fake a plane.

Before D2, the Blender executor verifies accessible native files, collection names, metre scale/axes, actual sensor surfaces and any visible stage/layer geometry; records exact versions and selected data case; derives lens/poses from blocking. Three sensors at 120° in one plane and the sourced shoulder reference do not substitute for coordinate inspection. Whole-tool rotation, where shown, follows the sourced clockwise view from surface looking downhole. Preserve source files and completed mechanism proofs; create versioned adapters/shot scenes.

Working profile for testing: 1280×720, 24 fps, EEVEE, 16 samples, 16:9. This is a proposed test profile, not final delivery approval. Seconds remain authoritative. Use 0.5 s handles where action permits, outside content duration; final assembly and audio belong to Radzi. Record color management, compositor and profile. Separate geometry, amplitude, signal, labels and reveal masks where used; avoid compulsory multilayer passes if they add no review value.

Targets relative to this shot folder: `Scenes/S02-C_v001.blend`, `Previews/v001/` (entry, major arrivals, peak-cost and exit stills plus continuous playblast), `Evidence/v001/` (asset/component manifest, scene-derived camera/frame score, provenance, benchmark log and review record). These are future deliverable paths, not created outputs. Update this same contract with D2 facts rather than creating competing direction specifications.

## Cost and review gates

**Likely heavy state and bounded alternative:** Fullest point/trace state; instancing and sparse lines, not layered full cylinders.

Every sampled full render-to-written-frame must be **strictly under 5 seconds**, including compositor and cold render. Benchmark entry, arrivals, peak effect, exit and any heavier state; log hardware/settings and cold plus repeat timings. No average-only pass. No render was run for T43. Simplify invisible geometry, transparent layers and particles first; never silently reduce resolution, change source scale or falsify meaning. Benchmark before batch rendering.

**Initial director critique:** the shot succeeds only if its arrival communicates the takeaway; decoration, hidden relationships and hurried reading are failure modes. Preserve successful blocking; make bounded corrections before adding effects. The specific unresolved risk is whether the proposed composition, timing and source assets support the expert check above; the executor tests this rather than assuming approval.

**Cold-viewer question:** Does this read as many measurements producing a circumference, rather than a ring attached to the tool? After the narrated moving preview, also ask why the discovery matters. Do not claim silent comprehension or infer motion approval from a still.

**Acceptance:** inspect entry, arrivals, transition and exit stills, then continuous motion with intended narration; verify source relationship separately with an expert. Record still, motion, engineering and final acceptance separately. Source uncertainty blocks only the affected claim/feature, not unrelated shot exploration. Radzi reviews the exact brief and previews; client technical review is required for unsupported engineering interpretations. Current status: no native scene, render benchmark, moving preview or client technical acceptance inspected in this task.
