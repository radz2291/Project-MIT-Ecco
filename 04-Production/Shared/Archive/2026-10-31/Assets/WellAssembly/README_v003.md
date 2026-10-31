# B102 provisional well and assembly master v003

16 October 2026. Radzi explicitly authorized the researched configuration as a provisional illustration, separate cased/open intervals, complete variants/controls and moving previews, with simplified BHA/adapters and O05 preserved until MIT confirmation before technical lock. This supersedes the earlier construction hold **for that bounded provisional scope**, not the actual engineering question.

## Use the master

Use **WELL_ASSEMBLY_v003** from [WellAssembly_variants_v003.blend](WellAssembly_variants_v003.blend). Open the master directly, or append that collection into a consumer for editable local controls while retaining ECCO as an external linked product. If linking the complete well collection instead, create appropriate Blender library overrides before editing its read-only controls. Inspection camera is outside the reusable collection. Accepted T5 temporary plugged v002 remains a relative linked collection; no source mesh/closure edits, rescaling or duplication into the well asset. Preserve earlier masters and preparation files.

[Authorized configuration](config_authorized_v003.json) keeps source URLs from the [research record](../../../Records/Tasks/T-006/research-standard-scenario_v002.md). Upper interval: 17.5in host / 13.375in casing OD / 12.515in nominal body ID, with ideal full cement annulus. Lower interval: 12.25in open-hole / bit gauge. Published 12.359in drift is a **separate fit reference**, not modeled as the actual nominal casing bore. Casing is not put into the smaller lower hole. The join at world X=0 is an illustrative interval boundary, not a modeled certified casing shoe.

Scene source X is longitudinal in metres; +X is test travel, not certified pin/box identification or drilling direction. Upper interval [-5.5,0], lower [0,6] metres are illustrative preview extents. No well depth is asserted.

## Live controls

Select **ASSEMBLY_CONTROL**, then edit Custom Properties. No Python handlers are needed.

| Property | Behavior |
|---|---|
| `travel_m` | Axial displacement of linked ECCO and all BHA proxies |
| `rotation_rad` | Local X rotation of product and proxies; radians |
| `variant` | 0 nominal, 1 irregular, 2 spiral; upper cased interval stays separate |
| `cutaway` | 1 rear-half inspection section, 0 full circumference |
| `show_open`, `show_casing`, `show_cement` | Independent interval/layer visibility |
| `show_hardware`, `show_proxies` | Separate linked product and provisional BHA visibility |
| `irregular_strength`, `spiral_strength` | 0 nominal wall through 1 full authored profile; editable shape-key drivers |

For scripted changes, call `rig.update_tag()` and update the dependency graph before measuring; hidden objects must be made visible before reading evaluated shape-key geometry. Animation can keyframe these Custom Properties. Do not directly animate driven travel/rotation child transforms.

The [versioned builder](Scripts/build_variants_v003.py) regenerates interval dimensions and profile pitch from configuration. Dimensions/preview extents/pitch are rebuild parameters; they are not all live vertex controls. It refuses source-hash mismatch and candidate overwrite. Run only in isolated background Blender, not the live user scene. Version the output before rebuilding a manually edited candidate.

## Provisional geometry and limits

Nominal lower wall is 12.25in. Irregular wall adds outward-only asymmetric washout with authored 25.4mm maximum radial scale. Spiral wall adds outward-only enlargement at authored 25.4mm scale and 1.8m pitch. These are explicit illustrative parameters, not a field measurement, drilling-path claim or ECCO output. They preserve a nominal passage rather than silently forcing a gauge-sized bit through an inward tight zone. No calibrated data colors, echoes, hydraulic simulation or measured log is implied.

Separate BHA proxies: generic 8.25in OD / 2-13/16in ID collar sections; orange adapter sleeves and simple bit-gauge ring. Proxy lengths and ECCO-to-bit placement are illustrative (recorded in builder), with no detailed threads, cutters, motor or actual MIT string claimed. Orange parts identify unresolved geometry; source ENP3 F.H. and reference collar REG must not be treated as directly mating. Set `show_proxies=0` when only validated product geometry is appropriate.

## Checks and review

[Report](../../../Records/Tasks/T-006/report.md), [fresh-open self-checks](../../../Records/Tasks/T-006/Evidence/variants-verification_v003.json), [combined moving preview](../../../Records/Tasks/T-006/Previews/v003/B102_all-variants_v003.mp4), [review sheet](../../../Records/Tasks/T-006/Previews/v003/B102_variants_review-sheet_v003.jpg).

Checks cover relative source link/hash, variant/full-cutaway selection, layer toggles, live shape-key controls, manifold casing/cement/proxy shells, source collection instances and positive straight centered product clearance in the selected geometry. Bit proxy matches nominal open-hole gauge, so nominal wall contact is intentional; it is not a cutting simulation. Preview rotations/travel demonstrate interfaces, not physical drilling speed/direction. MIT deployment, adapter/shoulder/shoe, actual BHA placement, eccentric/dogleg/loaded passage, material/load and operating clearance remain unvalidated. **O05 remains open before technical lock**, as do affected O04/O14 hardware questions.

## Replacement procedure

Register incoming assembled ECCO source/version/hash; preserve T5 originals. Remeasure all visible geometry and sensor/interface references, map source axes deliberately, compare with the accepted source and relink a new version. Re-run full rotation/travel, interval passage/profile clearances, source references, cutaway/visibility, cameras and affected downstream mechanisms/shots. Do not assume unchanged dimensions or sensor positions. Reopen affected reviews if geometry or meaning changes.

Master and preview binaries are local Git-ignored files; saved locally does not imply commit, push or remote backup. Text/config/scripts/evidence are separately tracked candidates. No client communication/publication or technical acceptance is implied by workflow Review.
