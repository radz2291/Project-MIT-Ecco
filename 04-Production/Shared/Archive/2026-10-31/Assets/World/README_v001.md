# A-WORLD shared asset interface

T44 · 18 October 2026 · Candidate for Radzi review. Source/master versions and hashes are in [manifest_v004.json](manifest_v004.json). This releases reusable interfaces for subsequent authorized builders; no film shot or final timeline is delivered here.

## Canonical candidates

Paths below are relative to `04-Production/Shared/Assets/`.

| Component | Local master / collection | Source and boundary |
|---|---|---|
| ECCO | `ECCO/ECCO_film_v002.blend` / `ECCO_FILM` | Material/smooth-shading derivative of T5 plugged v002. All product mesh topologies/vertices and three sensor references preserved. Original T5 remains unchanged. |
| BHA | `BHA/BHA_film_v002.blend` / `WORLD_HARDWARE` | One relative linked ECCO; sourced T6 collar diameters, simplified crossover sleeves and generic fixed-cutter bit silhouette. Authored lengths/details, unverified threads and actual MIT placement. |
| WELL/CASING | `WellAssembly/World_environment_v004.blend` / named `WORLD_*` groups | T6 v003 base meshes and profiles preserved; material refinement, upper host-rock section and bounded shoe rim added. Contains no ECCO. v003 is the preserved working rollback. |
| MUD | Same environment / `WORLD_MUD` | Low-opacity rear-annulus optical film. Fluid-filled context is optically simplified; this is not a simulated full fluid volume or an accurate optical model. |
| SURFACE | `Surface/Surface_context_v002.blend` / `WORLD_SURFACE` | Owner-designated IntoTheInvisible `01_SURFACE` collection: 442 objects / 20,652 vertices. Source geometry/layout retained, copied animation removed, PBR materials simplified and polished; quiet-water plate added. |

Local root: `C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco`. Native libraries and copied original are Git-ignored and local only; public reports/stills are not native-media backup. The copied rig original is `Surface/Originals/IntoTheInvisible_Shot01.blend`; its hash matches the unchanged external source. Its historical camera, well, tool, mechanism, geology and lighting are excluded from the reusable asset.

## Units, placement and source truth

Scene unit scale is one metre. ECCO's preserved imported object has scale **0.001** because its mesh vertices are millimetres; this is the existing source conversion, not a new scale change. Its evaluated length remains 2.400 m. Do not apply another 0.001 factor or silently change it to the brochure's nominal 2.25 m.

Longitudinal X is the shared downhole coordinate basis. The selected illustrative assembly places uphole collars at negative X and the bit beyond X=2.9 m; exact source pin/box end identification remains unverified. Whole assembly motion uses one collection instance. The environment boundary is X=0: cased interval [-5.5,0], open interval [0,6] m. These are illustrative local extents, not a well-depth claim. Casing body ID 12.515 in / OD 13.375 in, upper host 17.5 in; lower hole/bit gauge 12.25 in. Nominal centered geometry passes checks; loaded/eccentric/dogleg passage, connections/drift and engineering safety are unvalidated.

Three `ECCO_SENSOR_REF_01`–`03` retain X≈0.730 m and 120-degree spacing on one plane. They are inherited recess-rim references, not independently verified transducer faces. `ECCO_MUD_SENSOR_UNLOCATED` is a placeholder and must never emit or provide a measurement. Later sensing builders inspect actual face/contact registration.

Surface uses +Z up. `SURFACE_ROUTE_ANCHOR` maps source +X to surface -Z with +90 degrees about Y. Use the director's match cut; do not combine the local downhole world with a fictitious kilometre-scale transparent earth model. Offshore is a director-selected illustrative setting, not an actual deployment location.

## Stable consumer controls

[world_controls.py](Scripts/world_controls.py) creates only local collection instances, custom properties and Blender drivers. It copies no product meshes, uses no persistent Python handlers and needs no scripts enabled when reopening a saved consumer. Call `create_world(asset_dir)` from Blender with the absolute `Shared/Assets` directory. It returns `WORLD_PLACEMENT`, `WORLD_CONTROL` and an instance dictionary.

| Control | Default / behavior |
|---|---|
| `WORLD_PLACEMENT` | Rigid location/rotation of the entire context; scale stays 1 |
| `travel_m`, `rotation_rad` | 0.5 m, 0.4 rad; drives the single hardware collection instance, including all collars/bit and ECCO |
| `variant` | 0 nominal / 1 irregular (default) / 2 spiral |
| `cutaway` | 1 rear half / 0 full open-hole and casing/cement surfaces |
| `show_hardware`, `show_open`, `show_casing`, `show_cement` | Independent 0/1 visibility |
| `show_formation`, `show_shoe`, `show_mud` | Independent 0/1 visibility of rear-section host rock, shoe rim and optical mud film |

The host-rock/shoe/mud groups remain rear-section representations even in full-wall mode. They are optional context, not complete certified shoe/float equipment. For new scripted control values call `control.update_tag()` and update the dependency graph before measuring. Keyframe custom properties; use constant interpolation for discrete visibility/variant selections. Source T6 profile amplitudes/pitch are master-owned rebuild parameters, not consumer vertex-edit controls.

Consumers own cameras/lenses, keyframes/timing, lighting, rigid placement, selection/visibility, and explicitly recorded material overrides. Geometry, sensor references and source values remain master-owned. Local material overrides will intentionally mask later material revisions: record them, compare both overridden and inherited behavior during migration, and remove/review only the specific conflicting override. No material override is used in the two proof consumers. Their distinct camera keys, timing and local animation remain byte-equivalent in the recorded structured snapshots.

## Relative libraries and migration

Save consumers with explicit relative library paths and `relative_remap=False`, then freshly reopen them. The two test consumers are under `Records/Tasks/T-044/ReuseTests/`: A is 72 frames / 3 s; B is 96 frames / 4 s at 24 fps. Their `before_v003` files reference environment v003; `after_v004` reference v004. Both share hardware v002 and ECCO film v002. They are reuse tests, not S01/S04 production shots.

The bounded revision changes `WORLD_WetMineral` grain scale 38→62 per metre and roughness 0.44→0.34, with no geometry/sensor change. `build_world_t44.py -- migrate A` or `B` performs the same library-path update/reload in both consumers and asserts preserved cameras, timing and controls before saving a new file. It refuses overwrite. Existing output files must be preserved/versioned before a repeat.

For subsequent shared revisions:

1. Preserve the current working library and manifest; make a new immutable version and record the change.
2. Use [component-consumers_v004.json](../../../Records/Tasks/T-044/component-consumers_v004.json) to identify affected V3 shots. Its proposed future consumers are not existing scenes.
3. In each actual consumer, change the relevant library path to the new version and reload once. Keep camera, keyframes and allowed local controls intact. Do not append duplicate geometry.
4. Fresh-open; verify every library path, one evaluated ECCO, source geometry/refs, travel/rotation, visibility, layer order, clearance, local material overrides and entry/exit continuity.
5. Benchmark representative/heaviest states before rerendering affected outputs; record exact versions and migration status. No actual V3 shots exist in this package, so their migration status is not-started.
6. Roll back by relinking the prior immutable library, saving a separately versioned consumer, reopening and rerunning the checks. Preserved `before_v003` files are the tested rollback references.

## Fast-render profile and measured limit

Working asset tests: Blender 5.2.2, EEVEE, **Vulkan**, 1280×720 / 24 fps / 16 samples, ray tracing off, AgX / Medium High Contrast, no compositor, PNG RGB compression 15. GPU: GTX1060 3GB / driver560.94. First render in a fresh process is measured around the entire render-to-PNG operation; scene/process loading is outside that timer. No in-process warmup is excluded.

Normal driver caches are required for the measured profile. Fresh-process working tests pass below five seconds; see individual benchmark JSONs in the task evidence. The first uncached OpenGL tests took 24.57–25.13 s, and the first Vulkan initialization took 12.55 s. These failures are retained. A cleared/changed shader cache, backend, driver, machine, material or heavier shot invalidates the performance release: stop on any sample ≥5 s, simplify/retest before a batch. Do not hide initialization, average failures away or raise the cap. This is a bounded tested machine/profile result, not a guarantee of arbitrary cold-machine performance.

Example: launch isolated Blender with `--background --factory-startup --disable-autoexec --gpu-backend vulkan --python build_world_t44.py -- benchmark Reuse_A_after_v004.blend 1 36 72`. The test uses the task's saved consumer directory. `BLENDER_USER_RESOURCES` can point to the task Scratch/BlenderUser folder to isolate extension setup. Normal GPU caches remain outside that folder.

## Builder handoff and review boundaries

- A-SENSING: use the single hardware instance and preserved sensor references; bind events to its evaluated transform, verify faces/contact; no sensing events are created here.
- A-CASED: use fixed X=0 shoe/layer geography and sourced nominal dimensions; later integrate support/channel/wear without duplicating ECCO or pretending steel assembles around it.
- A-FLOW: use chosen +X downhole / -X uphole assembly convention, well inner surface and hardware envelope. Rear film is optical context only; hydraulic stage mapping, paths/cuttings and physical mode remain later work.
- A-OUTPUT/shot builders: use the component map and exact versions; no data, field evidence or live telemetry is implied. Radzi owns narration, audio, film assembly and client communication.

The generic bit is a bounded silhouette informed by [SLB's PDC bit reference](https://www.slb.com/products-and-services/innovating-in-oil-and-gas/well-construction/drilling/drill-bits/pdc-bits). Six blades, cutter positions and body lengths are authored illustrative details. It is not a selected manufacturer/MIT bit. No performance, thread-fit, material alloy or shoe certification is asserted. O04/O05/O14 retain the scope documented in the canonical decision register. Inspection lighting is for asset review; final cinematic readability, fluid/rock treatment and exact shot use still require Radzi's review.
