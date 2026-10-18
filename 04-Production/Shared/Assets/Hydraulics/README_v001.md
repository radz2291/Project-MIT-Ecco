# A-FLOW shared interface v001

18 October 2026 · T48 under T45 · candidate for Radzi review. Source hardware is immutable T44 `df1bc5626e820dc3a0b9af286bfcca4ce498d8c0`. This package is a continuous circulation illustration, not CFD, calibrated velocity/pressure, a wake result or a hydraulic qualification.

**Preserved on upstream hold:** T44 is being revised for uphole assembly continuity. T45 ordered further build/render work stopped. These candidates/evidence use the previous frozen T44 release. No playable demo or completed release is claimed. Consume the revised T44 release and repeat affected checks under restored ownership before continuing; see the task handoff.

Current library: `Hydraulics_v003.blend`; v001/v002 are preserved source predecessors. Top-level `HYDRAULICS_GEOMETRY` contains ten `FLOW_PATH_00–09` curves, `CUTTING_GEOMETRY`, `FLOW_TRACER_GEOMETRY` and neutral `FLOW_REGION_LOWER/MIDDLE/UPPER` anchors. Metres, unchanged source length 2.400 m; T44 selects +X downhole and −X uphole. Exact source pin/box correspondence remains unverified.

## Use

In Blender, add this directory's `Scripts` folder to the Python path, import `hydraulics_controls_v001`, and call `create_flow(library_path, placement=None, name='FLOW')`. It returns placement, local control and local wrappers. Use the same rigid unscaled placement/axial offset as `WORLD_HARDWARE`. The two tests use hardware travel0.5m, rotation0. Linked curves, particle mesh and materials stay master-owned; wrappers hold independent local control/visibility/timing. This is linked geometry reuse, not an appended geometry copy or a scene-handler system.

| Control | Meaning / tested range |
|---|---|
| `phase` | Authored circulation cycle offset; modulo1. |
| `speed` | Path cycles/second;0 freezes, default0.16. No physical velocity calibration. |
| `density` |0–10 active paths with three matte cuttings each; fixed finite pool, maximum30. |
| `flow_visible`, `cuttings_visible` | Independent visibility. |
| `stage_emphasis` |0 all;1 lower;2 middle;3 upper. A modest particle-size attention cue within neutral spatial windows; all strands/regions stay active. No activation sequence or functional stage assignment. |
| `operating_mode` |0 circulation-only;1 off. Rotation-only/tripping/combined modes are not implemented; the brochure supports them, and this test does not restrict the real tool. |

Paths are slender continuous amber guides; small sliding amber dashes make their travel visible, while cuttings are matte dark faceted slivers. Ten guides remain present over all three regions simultaneously. Deterministic particles/dashes travel uphole, wrap at the finite display domain and re-enter; this is authored illustration, not a fluid solver. No acoustic event contract or wave assets are consumed.

## Source mapping and limits

See [source map](../../../Records/Tasks/T-048/source-map_v001.md). Actual CAD inspection identifies a raised/twisted morphological span near sourceX0.50–1.56m. Neutral lower/highX `[1.35,1.56]`, middle `[0.88,1.35]`, upper/lowX `[0.50,0.88]` anchors describe regions of the current T44 layout. They do **not** certify accelerator/twisted-pad/diffuser face assignments. Such labels and feature-specific performance emphasis require annotated client/CAD confirmation. The demo retains a wider registered body/flow relationship.

The guide radius 0.154 m and finite bevel radius 0.00045 m fit the actual hardware's 0.152400077 m maximum radial envelope and nominal bore radius 0.155575 m. Matte slivers have at most 0.7 mm radial / 3 mm axial extent about their centres; amber dashes at most 0.45 mm radial / 6 mm axial extent. Continuous envelope bounds include interpolation between path nodes and all phases: hardware clearance at least 0.899 mm and wall clearance 0.854 mm for cuttings; strand/tracer hardware clearance at least 1.149 mm. No body/wall enlargement. Fresh-native checks test maximum density every frame and actual evaluated geometry. These bounds apply only to the centred nominal T44 pose and rigid placement tested; eccentricity, altered bores, other hardware or scale require rechecking.

## Revision and consumers

`Hydraulics_v002` changes the shared amber emission setting 0.20→0.32 only; identical curve coordinates and bevels. `Hydraulics_v003` gives authored cuttings a more readable axial shape/material and adds sliding amber dashes; radial envelopes and all continuous path coordinates remain unchanged. These look/shape changes have no quantitative information meaning. Two relative-linked consumers retain distinct cameras, 72/96-frame timing, independent phases/speeds/densities and all camera animation while library reloads remap the linked source. Final test files are `Records/Tasks/T-048/Scenes/Flow_reuse_A_v005.blend` and `Flow_reuse_B_v005.blend`; prior v003/v004 files preserve the first repaired registration/material proof. The shared cutting geometry update reaches both consumers through one library revision; the migration helper adds linked dash wrappers identically.

To revise: preserve the consumer; snapshot camera/timing/animation/local controls; reload its direct Hydraulics library to the immutable successor; save as a new version with direct relative links and `relative_remap=False`; fresh-open and compare snapshots, geometry hashes/material value, source links and clearance; benchmark before rendering. Nested T44 links remain relative to their owning libraries. Do not rewrite their paths against the consumer. Roll back with the preserved v003 consumers. Failed-registration v001/v002 consumers are retained solely as repair evidence, not reusable candidates.

Planned V3 consumers: S05-A/B/C. No actual movie shot or film edit was produced. Before source-specific close-ups, resolve exact end/functional map; keep all regions active and preserve uphole return.

All `.blend`, MP4 and raw frames remain local Git-ignored on Radzi's Windows machine; no remote-native access or off-machine backup is claimed. [Task report](../../../Records/Tasks/T-048/report.md) and manifest identify exact candidate versions, preview checks and render timings. The strict per-frame cap remains<5s, with T44's empty-cache initialization limitation unresolved. Human comprehension, appearance and engineering acceptance remain for Radzi/client review.
