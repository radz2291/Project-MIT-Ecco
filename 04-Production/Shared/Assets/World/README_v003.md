# A-WORLD — bounded cleanup interface v003

18 October 2026. T44 candidate for Radzi image review. The accepted surrounding formation coverage is preserved exactly. Current libraries: `BHA/BHA_film_v006.blend`, `WellAssembly/World_environment_v009.blend`, unchanged `ECCO/ECCO_film_v002.blend`. See [manifest](manifest_v006.json), [five individual review images](../../../Records/Tasks/T-044/Revision_v006/review-guide.md) and [task report](../../../Records/Tasks/T-044/report.md).

## Use and preserved controls

Inside Blender, add this directory's `Scripts` folder to Python's import path and call `formation_controls_v003.create_world(asset_dir)`. It returns the existing placement, control and instance interface. Units remain metres, local +X longitudinal. Do not scale placement. Housing remains 2.400m with unchanged sensor references. Six variant/full-cut formation groups retain X[-8,10]m and transverse half-width2.4m. The original [coverage and supported framing guide](README_v002.md) remains applicable; no geology rebuild occurred.

Travel, rotation, variant, cutaway and existing layer visibility controls remain consumer-owned. Linked geometry and sensor references remain master-owned. `show_mud` controls the static optical cut. `show_shoe` remains a compatibility control for the retained provisional rim, whose duplicate coplanar surfaces are now hidden in the master. Source casing's flush end supplies visible boundary context; no selected shoe/float assembly is claimed. Do not restore the coincident rim for rendering. A later exact shoe replacement requires source/fit review and affected consumer checks.

## Geometry and appearance corrections

- The provisional six-blade PDC bit has broad integral blades, 48 two-part compact cutters, six recessed nozzle mouths, gauge pads and open junk courses. Reference: SLB [The Defining Series: Bits](https://www.slb.com/resource-library/oilfield-review/defining-series/defining-bits), 2016, Figure2, visually inspected. This is an authored morphology study, not an exact SLB model or selected MIT/client bit. Crown, blade dimensions, single-row cutter arrangement and adapter transition are simplified. The diagram's optional conical centre element, second cutter rows, internal fluid network and threads are omitted. Interfaces and hydraulic performance are unverified. Evaluated gauge retains12.25in; the bit stays within X[2.9,3.24]m.
- Casing cylinder corner normals replace flat polygon shading. Rim/cut normals stay crisp; coordinates/topology/dimensions are identical. The redundant illustrative shoe overlapped the last70mm of source casing, causing additional rim interference; it is preserved hidden. The redundant bit shoulder overlay is also hidden. Collar cylindrical normals are corrected without mesh changes.
- A curved, continuously blended fluid cut replaces the flat olive plane. Its vertices stay at least0.4mm within every registered bore. Tool geometry naturally occludes it. It is a static optical approximation: no free liquid surface, physically calibrated transparency, filled-volume/CFD or animated circulation claim. Hidden rear optical skin is retained for traceability.
- Close-view lighting reduces broad flattening reflections; source product materials/geometry are unchanged. Lighting remains a documented consumer override. No new shots or animation were made.

## Update existing consumers

1. Preserve the old native file and snapshot camera, timing, local controls and animations.
2. Resolve library paths against the old file, then reload environmentv009 and BHAv006. Keep the unchanged ECCO library as the single nested product reference.
3. Save As a new candidate with relative links (`relative_remap=False`). Fresh-open, check one product, six bit blades, formation coverage, layer/fluid visibility, source dimensions and local overrides. Compare the camera/timing/control snapshot.
4. Benchmark the intended/heaviest view before batch work, then rerender affected views. The two reuse consumers retain72/96frame timing and original cameras. [Consumer mapping and rollback paths](../../../Records/Tasks/T-044/Revision_v006/component-consumers_v006.json) identify the current seven inspection consumers. V3 component/shot mappings remain planning references; no actual movie shots were built or migrated.

Rollback by opening the preserved v005 consumers and libraries. Keep [prior manifest](manifest_v005.json), [prior report](../../../Records/Tasks/T-044/report_v005.md) and accepted [wide context image](../../../Records/Tasks/T-044/Previews/Revision_v005/wide_context_working_v007.png).

## Render limits and storage

Final seven fresh-process first render-to-file measurements:1.04–1.65s at1280x720/EEVEE16/Vulkan, normal existing GPU disk caches. A more complex blended-fluid shader initially took6.45s; that failed attempt is retained and prompted a simpler shader/single transparent cut before retesting. The simplified shader's first test took4.20s. Earlier empty-cache initialization12.55–25.13s remains unresolved. These results do not establish universal cold-machine compliance. Rebenchmark after cache/backend/driver/machine/material changes or heavier framing. Do not raise the strict5s cap.

All native .blend files and local reference image are Git-ignored on this Windows machine. Selected review PNGs, scripts and records are synchronized. No native upload or off-machine backup is claimed. Source originals and previous candidates are preserved. Human appearance/technical acceptance remains pending.
