# A-CASED — shared layer and condition interface

Historical pre-continuity interface. Current accepted continuity release and final consumer selection are documented in [README_v002.md](README_v002.md). Earlier native/event version references below are preserved history.

T47 `de4e8339-fbdd-4c40-9f30-bf61302ed04e`, delegated by T45. Candidate review remains Radzi's decision. Scope is reusable assets and reuse tests; no S04 movie shot or film assembly is created.

## Source and geometry

Current native master is `CasedHole_v002.blend`; previous `v001` is preserved. Metres, longitudinal +X, same unscaled T44 world frame. Casing X[-5.5,0]m; nominal internal radius .1589405m, exterior .1698625m; cement outer .22225m. These inherit T6's authorized provisional 12.515in ID /13.375in OD /17.5in host geometry through accepted T44, not a certified MIT deployment. Product remains the actual linked2.400m master, unchanged. Three inherited sensor refs atX.73m are provisional recess references, not verified acoustic faces; mud sensor remains unlocated.

Physical order is tool/fluid, steel, cement or localized channel, formation. New condition geometry is authored at the registered radii without B203's exploded offsets. B203 v002 is inspected source evidence for qualitative support, localized axial/azimuth channel and4mm pre-existing inner wear. Its old pulse system and packaged waveforms are not reused.

The channel is X[-2.5,-.4]m, azimuth[.30,.80]rad measured atan2(Z,Y), outside steel. Blue is illustrative and identifies no fluid chemistry; no flow is animated. Wear is a smooth4mm maximum inner recess aroundX-1.5m, azimuth0, length1.6m, same depth as B203. Exterior radius stays fixed. Nominal inner contours remain registered at identical scale. No direct thickness/bond strength result is claimed.

## Consumer API and overrides

Add `Scripts` to Blender's import path. After creating the accepted T44 world with `World/Scripts/formation_controls_v003.create_world(asset_dir)`, call `cased_controls_v001.create_cased(asset_dir, version='v002')`. It returns the local `CASED_CONTROL` and named linked instances. Set WORLD_CONTROL show_casing/show_cement to0 to prevent duplicate shells; retain the original formation/fluid/hardware as needed.

Stable booleans: `cutaway`, `show_steel`, `show_cement`, `show_channel`, `show_reference`, `wear`, `channel`. The two variants choose nominal/worn steel and supported/channel cement. FULL and CUTAWAY are available; cutaway retainsY>=0. Geometry/source dimensions stay master-owned. Axial/azimuth channel bounds and wear dimensions in the control are informational, not deformers. To change them, edit the named build parameters, publish a new version through `build_cased_v001.py`, migrate consumers, and reverify. Do not edit the informational metadata expecting geometry to change.

`response_from_event(event, support_state)` consumes the common T45 event dictionary and returns the prescribed casing response fields. `add_response` adds small native local decay bars. The public T46 `acoustic_binding_v001.bind_event` supplies all send/contact/return graphics from its linked effect library; T47 owns no pulse or global waveform fork. Support response is qualitative, uncalibrated and independently labeled. The initial declared fixture is retained as construction evidence; actual integrated cased events supersede it for integration claims.

The support proof's small editable screen labels use the installed Windows Segoe UI font at `C:/Windows/Fonts/segoeui.ttf`. No font file is copied or redistributed. Relocation requires that font or an intentionally substituted/rechecked font; no final film font licensing or typography approval is claimed.

Current behavior native is `T-047/Scenes/CasedSupport_v006.blend`: actual temporary-cap exit registration, T46 `Acoustics_v003.blend` thin arcs, restrained contact marker and a geometry-derived camera inside the annulus. `actual-cased-events_v006.json` retains the reference/cap distinction and exact native wall hash. The full-ID `CasedWearSection_v005.blend` is derived atX−1.5 from the real master mesh edge intersections, with white nominal and emerald actual inner edges; no scale/depth exaggeration or inferred thickness result.

## Reuse, revision and supported consumers

`T-047/Scenes/CasedReuse_A_v002.blend` and `CasedReuse_B_v002.blend` link the same master with distinct cameras and72/96frame timing. Revision v001→v002 changes master satin roughness .45→.39, preserves geometry, names and both consumer camera/timing/control snapshots. See `T-047/Evidence/revision-propagation_v002.json`. Repeat: preserve old file; resolve old paths; relink/reload the new immutable master once; save a versioned consumer with relative links; fresh-open; compare camera/timing/control snapshot; check condition masks and benchmark affected framings. Roll back by reopening the preserved v001 consumer.

V3 map: S04-A uses retrieval/casing context; S04-B uses support contrast and acoustic response; S04-C uses exterior channel; S04-D uses pre-existing inner wear/nominal reference. These are downstream consumer IDs, not completed movie shots. Any master revision requires affected-layer, event intersection, camera/occlusion and render-cost checks for every retained consumer.

## Storage and performance

Native Blender, videos and bulk frames remain organized locally and Git-ignored. No remote native upload or off-machine backup is claimed. Scripts, manifests, evidence and a few selected review PNGs go through T45's sole Git integrator. The manifest supplies exact paths/hashes.

Working settings are1280x720,24fps, EEVEE16, Vulkan, AgX Medium High Contrast, compositor off. Queue every render through T45. Whole render-to-file must be strictly<5s before batches. Benchmarks use existing driver caches; T44's prior empty-cache12.55–25.13s initialization limitation is unresolved. Fresh-process normal-cache results do not establish universal cold-machine compliance. Rebenchmark after cache/backend/driver/machine/material or framing changes.
