# A-WORLD — surrounding formation revision

18 October 2026 · T44 revision v005 · **appearance approval pending Radzi**. This supersedes the environment coverage/image package in [v001](README_v001.md); previous masters and results remain intact. [Current hashes](manifest_v005.json) · [full-size image guide](../../../Records/Tasks/T-044/Revision_v005/review-guide.md) · [report](../../../Records/Tasks/T-044/report.md).

## Shared candidates

| Master beneath `Shared/Assets/` | Collection / purpose |
|---|---|
| `WellAssembly/World_environment_v005.blend` | Existing `WORLD_*` well/layer interfaces; six `WORLD_FORMATION_<NOMINAL/IRREGULAR/SPIRAL>_<FULL/CUTAWAY>` surrounding masses; improved `WORLD_MUD`. |
| `Formation/Formation_context_v002.blend` | `WORLD_GROUND_CONTEXT`: wide earth/strata/seafloor section and nominal well route. |
| `Formation/Formation_cased-section_v002.blend` | `WORLD_CASED_FORMATION_SECTION`: upper-host-only end section; reveal layers without foreground lower rock masking them. |
| `Surface/Surface_context_v003.blend` | `WORLD_SURFACE`: unchanged rig geometry/layout, with deliberate near water section removed. Surface v002 retains full water. |
| `BHA/BHA_film_v002.blend`, `ECCO/ECCO_film_v002.blend` | Unchanged hardware/product, source scale and sensor references; one hardware instance. |

Native root: `C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/`. Native files remain Git-ignored/local; online images/reports do not imply online native media or off-machine backup.

## Extent and source scale

Downhole formation spans **X=-8…10 m**, transverse half-width **2.4 m** (4.8 m square cross-section). A boundary representation supplies surrounding rock, cut-face relief outside the bore, grain/strata shading and wet highlights. It is illustrative geology, not simulation or a literal solid-earth volume. Keep outer axial edges outside supported close views.

Original T6 inner wall/casing/cement meshes remain exact. New backing mass sits0.7 mm behind them; geometric cut-face relief lies outside the bore. No product scaling or clearance enlargement was used. Nominal lower radius0.155575 m; casing body ID12.515 in / OD13.375 in; upper host17.5 in. T5's evaluated length remains2.400 m and its retained0.001 object scale converts mesh millimetres to metres. Original interface/sensor and engineering limits from v001 apply.

Tested close cameras are `(0.72,-0.78,0.32)` and `(0.95,-0.72,0.38)` m, 42 mm lenses, approximately0.245 m apart. Both images have255 alpha throughout: no empty studio pixels. The camera occupies the deliberately removed near formation, not the actual annular gap. This proves these poses; other camera positions/motions require edge/occlusion/cost checks.

Macro context uses the same metre/source-X basis: local X[-20,25] m, transverse half-width45 m. The approval consumer places X=0 at surface-world `(0,0,-60)` and rotates+90°Y, mapping +X to -Z. Seafloor Z=-40 and lower extent-85 m are illustrative authoring extents, not field depth/deployment. Rig scale is retained. Use an intentional water/earth section or match-cut, not a camera passing through opaque earth/steel.

## Controls and references

[formation_controls_v002.py](Scripts/formation_controls_v002.py) links v005 and returns the existing `WORLD_PLACEMENT`, `WORLD_CONTROL` and instances. `travel_m`/`rotation_rad` move the single whole BHA. `variant=0/1/2`, `cutaway=0/1`, `show_formation` select one matching mass; other layer/hardware/mud visibility controls remain consumer-owned. Geometry and sensor references remain master-owned. No persistent Python handlers are needed when reopening.

The historical `WORLD_UPPER_FORMATION` name is a compatibility alias for the irregular surrounding rear mass across both intervals, replacing the former thin sleeve. The v002 helper removes that alias instance and selects the matching group; never instance both together. All six variant/cutaway combinations and formation hide control are checked.

`WORLD_MUD` is a static muted-olive **cinematic fluid section**, occluded by real opaque hardware. It is optical context, not a full CFD volume, calibrated opacity, particles or flow/acoustic effects. Wet sheen does not claim a measurement. For layer inspection, hide bulk formation, lower open wall, hardware and mud, then link `WORLD_CASED_FORMATION_SECTION` with source casing/cement/shoe. This bounded reveal changes visibility, not dimensions or layer spacing. The macro and cased-only components are shared assets, not single-camera soil patches.

## Revision and consumers

Preserved A/B consumers were migrated v004→v005 by one environment library path/reload, then saved under `Records/Tasks/T-044/Revision_v005/Scenes/Reuse_<A/B>_formation_v005.blend`. Cameras, camera keys, frame ranges/fps, local properties and animation remain identical; fresh opens resolve relative links and one evaluated product. [Rendered proof](../../../Records/Tasks/T-044/Previews/Revision_v005/propagation_v005.jpg) · [impact map](../../../Records/Tasks/T-044/Revision_v005/component-consumers_v005.json).

For later changes: preserve/version/hash the master, identify actual consumers, relink/reload, check geometry/sensors/overrides/layers/coverage/continuity, benchmark representative/heaviest states, then rerender affected outputs. Consumer material overrides can mask shared material changes. Roll back through a new consumer version referencing v004 and rerun checks. Future V3 shots are not built or migrated by this package.

## Performance and review

Blender5.2.2 / EEVEE/Vulkan /1280×720 /24fps /16 samples, ray tracing/compositor off, AgX Medium High Contrast. Saved exposures: downhole-1.15EV, detail-0.45EV, wide-0.3EV, layer-0.7EV. Per-view timings measure the entire first render through PNG writing after a fresh file/process open, normal existing GPU caches, no excluded warmup. Known original empty-cache initialization12.55–25.13 s remains disclosed. Cache/backend/driver/machine/material or heavier-shot changes require a new benchmark; stop on any sample≥5 s before batches. No universal cold-machine guarantee or cap waiver.

Five individual full-size images are the primary approval deliverable; the overview is only an index. Radzi judges ground coverage, tactile/fluid treatment, metal detail, layer readability and simplified bit/adapters. No movie animation, sensing/flow/data effects, film assembly or new ticket is part of this revision.
