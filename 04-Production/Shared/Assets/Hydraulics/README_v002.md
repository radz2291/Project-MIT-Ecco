# A-FLOW current interface v002

18 October 2026 · T48 under T45 · candidate awaiting master integration and independent verification. Current manifest: [manifest_v002.json](manifest_v002.json). Previous [interface](README_v001.md), pre-continuity scenes and upstream-hold records remain historical evidence.

The flow geometry master is unchanged `Hydraulics_v003.blend`, collection `HYDRAULICS_GEOMETRY`. Current relative-linked consumers are `Records/Tasks/T-048/Scenes/Flow_reuse_A_v006.blend` and `Flow_reuse_B_v006.blend`. They consume accepted T44 commit `a08d0ecfbd6f3241298f506b3ea42613388b3baf`: direct `BHA_film_v007.blend` with immutable nested v006, unchanged ECCO v002 and environment v009, plus one linked extension and joint attached to the existing hardware instance. Source metre scale, original CAD unit conversion, sensor references, cameras, timing, camera keys and old controls are preserved.

## Linked geometry and controls

`Scripts/hydraulics_controls_v001.py` exposes `create_flow(library_path, placement=None, name='FLOW')`. It returns placement, local controls and wrappers. Linked curves/meshes/materials remain master-owned; local wrappers carry independent phase/speed/visibility controls. Current consumers are stationary circulation-only tests with the flow's rigid placement matching the hardware's 0.5 m travel and zero spin. No simulation cache, handler or custom driver namespace is needed for playback.

| Control | Meaning |
|---|---|
| `phase`, `speed` | Authored cycle offset/rate; speed 0 freezes motion. Default rate 0.16 cycles/s is not a calibrated fluid velocity. |
| `density` | 0–10 paths with three matte cuttings each; maximum 30. |
| `flow_visible`, `cuttings_visible` | Independent visibility; flow visibility includes sliding amber dashes. |
| `stage_emphasis` | 0 all, 1 neutral lower, 2 middle, 3 upper; modest attention cue, with all regions/continuous guides still active. |
| `operating_mode` | 0 circulation-only, 1 off. Other brochure-supported operating modes are outside this test. |

Ten slender continuous amber guides serve all three neutral regions simultaneously. Twenty small sliding amber dashes and up to thirty dark matte slivers follow these paths; the finite display-domain wrap represents re-entry, not a transport simulation. Cuttings are authored 6 mm axial slivers with at most 0.7 mm radial extent; dashes are 12 mm axially and at most 0.45 mm radially. No acoustic arcs/events are consumed.

## Source and clearance limits

Use [current source map](../../../Records/Tasks/T-048/source-map_v002.md). Source longitudinal length remains 2.400 m. Selected T44 +X points downhole, so return follows −X. Physical pin/box identity and certified accelerator/twisted-pad/diffuser face assignment remain unverified. Region anchors are morphological windows, not performance labels. No CFD, calibrated pressure/velocity, quantified wake/efficiency or engineering approval is implied.

`verify_hydraulics_v002.py` repairs preflight item 5: enumerate hardware by recursive collection provenance, derive the entire finite X envelope from actual guides and shapes, then clip every intersecting triangle to that slab. Faces crossing the slab remain included even when all their original vertices are outside it. All 135 visible base hardware meshes plus the revised extension/joint are considered; disjoint objects are recorded using complete bounding intervals. The actual rigid assembly registration, fixed original unit conversion, source geometry and each frame's full finite mesh are checked. Wall faceting is included, with a 1 micrometre numerical guard.

At the tested centred nominal pose, complete-shape conservative clearance is at least 0.897 mm to hardware and 0.852 mm to the actual wall. No hardware/wall enlargement occurred. These limits cover this pose and the tested 72/96-frame consumers, not arbitrary eccentricity, scaling, hardware or bore changes. Recheck affected geometry after any such change.

## Revision, playback and review

Earlier shared material and cutting-geometry revisions propagate into both consumers through relative links with cameras/timing/animation/local controls retained. Continuity migration reloads only the direct v006 BHA to v007, leaves nested v006 intact, and calls `attach_continuation` on the existing hardware instance. Preserve predecessors and save a new filename; never recursively replace the nested source. Current verification hashes actual resolved library paths, with no basename fallback.

The local [4-second demo](../../../Records/Tasks/T-048/Previews/Revision_v007/Hydraulics_behavior_B_v007.mp4) decodes all 96 frames at 24 fps/1280×720. Current selected stills are in the same folder. The camera/geometry/continuous guides remain coherent through the ordered chronology; matte cuttings and directional dashes remain subtle at actual clearance. This is disclosed for Radzi's moving-readability review, not asserted as a comprehension pass.

Six full-write samples measured 0.722–1.914 s; every demo frame measured 0.612–1.644 s at EEVEE 16/Vulkan/AgX Medium High Contrast/720p. Normal existing GPU caches were retained. Prior empty-cache initialization of 12.55–25.13 s remains unresolved; no universal cold-machine compliance is claimed. Keep the strict less-than-5 s gate and serialize rendering through T45.

All Blender/video/raw-frame files remain local Git-ignored; no off-machine backup or native upload is claimed. The master alone integrates the explicit allow-list, verifies the remote SHA and obtains fresh-context verification before Review. Radzi owns acceptance, film assembly and client communication. Planned V3 consumers are S05-A/B/C; no actual movie shot was built.
