# T44 — A-WORLD bounded visual cleanup

18 October 2026. Candidate for Radzi image approval; executor work complete, not accepted as Done.

Task: `b77297cc-0600-4a17-8fb9-ba95cc3d6220`, active MIT ECCO project `a0b9b971-e282-42f0-a25f-0c78729eff87`. Authority: Radzi's request to inspect new discussion and owner-agreed review comment `b9543a37-2583-48d4-84b8-d251b9ebe98b` (18 October06:40UTC). Base commit: `85902bb01b9669c592e2f5c058d54337ff9d3e1f`. Current T42/T43 source contracts and production rules apply. Previous [report](report_v005.md) and candidates preserved.

## Result and review images

The accepted surrounding formation coverage is unchanged. This pass replaces the rounded bit placeholder with a documented provisional six-blade PDC study; corrects native casing normals and coincident rim interference; refines static fluid and hardware reflections. No new animation, movie shots, environment rebuild or film assembly.

Primary deliverable: [five individually viewable approval images](Revision_v006/review-guide.md). Please judge bit silhouette/cutter layout, steel-layer readability, fluid presence and retained tool detail. [Bit-face detail](Previews/Revision_v006/BHA_face_working_v010.png), [bit/adapter side view](Previews/Revision_v006/BHA_detail_working_v010.png), [steel/cement/formation](Previews/Revision_v006/layers_working_v010.png), [nearby A](Previews/Revision_v006/downhole_A_working_v010.png), [nearby B](Previews/Revision_v006/downhole_B_working_v010.png). The [compact index](Previews/Revision_v006/approval-overview_v006.jpg) accompanies the full-size PNGs. Preserve [accepted wide context](Previews/Revision_v005/wide_context_working_v007.png).

## Native changes and source limits

- BHA filmv006: six broad integral blades,48two-part compact cutters, six recessed nozzle mouths, open junk courses and gauge pads. Evaluated12.25in gauge and X[2.9,3.24]m envelope checked. Reference: SLB [The Defining Series: Bits](https://www.slb.com/resource-library/oilfield-review/defining-series/defining-bits),2016, Figure2; labelled image visually inspected. [Reference/simplification record](Revision_v006/source-reference_v006.md). This is authored provisional morphology, not an exact manufacturer or MIT/client bit. Crown, cutter count/rake and transition are simplified; secondary cutter rows, central conical element, internal hydraulics and threads omitted. No connection/fit/performance certification. Redundant coplanar shoulder overlay retained hidden; collar cylindrical normals corrected without coordinate/topology changes.
- Environmentv009: casing diagnosis found18,816flat-shaded faces, including18,432cylindrical faces, correct radial winding, no modifiers/custom normals and a simple material. Analytic radial corner normals smooth cylindrical surfaces while rims/cuts remain crisp. Geometry/topology/dimensions are identical. A second cause at the front rim was the provisional shoe's coplanar overlap with source casing over the last70mm; redundant mesh retained hidden. The flush source casing end remains the visible shoe-boundary context. Exact shoe/float equipment remains unverified. The compatibility `show_shoe` switch does not restore this hidden overlap.
- Static fluid: the flat olive plane is replaced by a curved, continuously blended optical cut inside every registered bore; a duplicate rear skin is retained hidden. Tool geometry occludes it naturally. Simplified green-grey transparency and restrained reflections replace the solid-strip appearance. This is not a free liquid surface, calibrated filled volume, CFD or flow animation. New lighting overrides reduce broad highlight flattening. Product geometry/material files remain unchanged.
- All accepted formation mass meshes, source wall/layer meshes, rig/wide/cased-host context, T5/T6 originals, sensor references, source scales and previous native candidates are hash/geometry verified unchanged. Housing remains2.400m. No clearance enlargement, source rescale or duplicated ECCO.

## Saved candidates and propagation

Current [native manifest/hashes](../../../Shared/Assets/World/manifest_v006.json), [usage/migration guide](../../../Shared/Assets/World/README_v003.md), [component/consumer map](Revision_v006/component-consumers_v006.json).

Local root: `C:\Users\RZ1\Desktop\RZ\261013-MIT-Ecco\04-Production`.

- `Shared\Assets\BHA\BHA_film_v006.blend`, collection `WORLD_HARDWARE`.
- `Shared\Assets\WellAssembly\World_environment_v009.blend`, existing named collections/controls.
- Unchanged nested product: `Shared\Assets\ECCO\ECCO_film_v002.blend`.
- Seven final consumers: `Records\Tasks\T-044\Revision_v006\Scenes\{BHA_detail,BHA_face,layers,downhole_A,downhole_B,Reuse_A,Reuse_B}_cleanup_v010.blend`.
- New builder interface: `formation_controls_v003.create_world(asset_dir)`; old interfaces/candidates remain preserved.

Both reuse consumers adopt shared revisions by library-path reload/Save As, with original cameras,72/96frame timing, local controls and animation intact. Every saved migration stage records equality. The additional bit-face camera is a separate static inspection; it does not replace a reuse camera. [Propagation comparison](Previews/Revision_v006/propagation_v006.jpg) and native migration evidence accompany the individual images. No actual V3 movie-shot consumers exist yet; inherited component-to-shot mapping identifies later checks without authorizing production.

## Verification and render budget

[Native verification](Revision_v006/Evidence/native-verification_v006.json):96checks pass, including all preserved file hashes, unchanged source/environment geometry, casing normals, hidden overlap, fluid bounds, evaluated bit gauge/envelope, fresh relative links, one ECCO/six bit blades, control variants and end-to-end camera/timing/control retention. These are executor self-checks, not independent engineering or visual acceptance.

Full first render-to-file measurements, separate fresh processes,1280x720/EEVEE16/Vulkan on GTX1060/driver560.94, AgX Medium High Contrast, no compositor/raytracing/shadows, normal existing GPU disk caches, no warmup render excluded:

| Saved consumerv010 | Seconds |
|---|---:|
| Bit/adapter side |1.037|
| Bit face |1.051|
| Layer section |1.193|
| Downhole A |1.533|
| Downhole B |1.648|
| Reuse A |1.461|
| Reuse B |1.460|

All seven final renders are strictly below5s. Timers wrap the entire render-to-file call; process/file loading is excluded. A superseded complex blended-fluid shader took6.448s on its first new-shader render. That failure is retained, prompted removing shader noise/angle logic and duplicate transparent overdraw, and no batch was launched on the failed setting. The simplified shader first test took4.197s before the final gauge/joint pass. [Package evidence](Revision_v006/Evidence/package-verification_v006.json) retains every benchmark, including failures. Prior empty-cache initialization12.55–25.13s remains unresolved: normal-cache timings do not establish universal cold-machine compliance. Rebenchmark cache/backend/driver/machine/material changes or heavier views; do not raise the cap.

Executor inspected the individual full-size saved-candidate renders. Both close views retain full opaque formation coverage. Final beauty/technical interpretation remains Radzi's review.

## Storage, synchronization and handoff

Selected review stills, scripts, manifests and records are synchronized to the established repository; the exact remote-verified containing commit/report links are attached to live T44 after push. Heavy .blend files, prior/intermediate samples, logs and the inspected manufacturer image remain local/Git-ignored. No native-media upload or off-machine backup is claimed. Unrelated generated source image remains untouched.

Next action: Radzi reviews the five images, with previously accepted environment coverage retained. T44 returns to Review; no self-acceptance or downstream shot/effects work. Source/interface questions about exact client bit, threads and shoe equipment remain explicitly provisional.
