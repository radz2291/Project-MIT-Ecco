# T27 / B202-M handover — Measured Envelope v008

**State:** complete T8 still-development package submitted for Radzi Review. D1 concept acceptance applies to A/B/C v005; exact v008 still package is not yet accepted. T27's live T8 dependency/human acceptance remains in force. This file does not authorize or launch T27. No motion was built in T8.

**Start here:** local root `C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco`; [reusable master](../../../Mechanisms/B202/Scenes/B202_measured-envelope_master_v008.blend), collection `B202_MEASURED_ENVELOPE_v008`. Master default is state B, tool hidden for the geometry payoff. All six consumers contain the same layers/controls with different presets. [Review sheet](../../../Mechanisms/B202/Previews/Stills_v008/B202_review-sheet_v008.jpg), [report](report.md), [verification/hashes](Evidence/verification_v008.json), [source correspondence](Evidence/source-correspondence_v008.json), [single direction contract](../../../Mechanisms/B202/direction.md).

## Exact inputs and reusable states

Accepted T5 plugged v002 remains a relative library; ten local presentation copies preserve its mesh coordinates/topology and source transforms. Hardware uses source X metres, 2.400m length, no rescaling. Accepted T6 well v003 supplies exact evaluated irregular and spiral surfaces. Tight is a separate authored illustration. T7 Motion_v005 is byte-preserved and remains upstream pulse/echo context; do not reintroduce its KIV waveform/distance work.

| State | Native scene under `Mechanisms/B202/Scenes/` | Still under `Previews/Stills_v008/` | Purpose |
|---|---|---|---|
| A | `B202_A_v008.blend` | `B202_A_v008.png` | Sensor-plane registered circumference + sample markers on rock |
| B | `B202_B_v008.blend` | `B202_B_v008.png` | Full irregular reconstructed geometry, hardware suppressed |
| C | `B202_C_v008.blend` | `B202_C_v008.png` | White nominal vs blue enlargement at sensor plane |
| D | `B202_D_v008.blend` | `B202_D_v008.png` | Separate red local undersize with conservative centered clearance |
| E | `B202_E_v008.blend` | `B202_E_v008.png` | Source T6 spiral-through-depth example, no asserted cause |
| F | `B202_F_v008.blend` | `B202_F_v008.png` | Independent yellow/brown echo-amplitude illustration |

## Controls, layers and coordinates

Select `B202_CONTROL`. Custom properties have drivers; no handlers or keyed actions are required. Call `control.update_tag()` and update the dependency graph after scripted changes. Enable `show_tool=1` before inspecting hardware matrices; hidden objects may retain stale unevaluated matrices.

| Property | Meaning |
|---|---|
| `travel_m`, `rotation_rad` | Whole tool + all plugs/covers + sensor references move/rotate together along/about source X. Default travel2m, rotation0. |
| `profile` | 0 irregular T6; 1 tight illustration; 2 spiral T6. Amplitude layer is separate and uses irregular wall. |
| `show_tool`, `show_wall` | Independent hardware / physical rear-half cutaway visibility. Keep real geometry fixed; reduce visual competition using visibility rather than scaling or exploding the tool. |
| `show_envelope`, `show_amplitude` | Separate radius-geometry / amplitude surfaces. Normally present one at a time; never transform radius colors into amplitude. |
| `show_sections`, `show_samples` | Contour curves / sparse illustrative wall sample markers. Samples are fixed at X2.730m; not animated acquisition history. |
| `show_nominal` | White12.25in bit-size reference; actual sourced nominal radius0.155575m. |
| `show_depth_sections` | Enable additional section/reference rings beyond the hero sensor plane. |
| `depth_start_m`, `depth_reveal_m` | Clip information surfaces/physical wall in source X, using geometry nodes; retained mesh has6.25cm axial spacing and96 angular vertices. Reveal is discretized, not physical resolution. |
| `scan_fraction` | 0–1 contour trim and sparse marker reveal. Curves have an explicit closing segment so partial trim works. This is a presentation control, not firing cadence or a three-sensor acquisition scheduler. |
| `geometry_opacity`, `amplitude_opacity` | Separate driven material opacities. Camera/lighting and all material nodes remain editable. |

`B202_TOOL_TRAVEL_X` → `B202_TOOL_ROTATION_X` parents all visible hardware and `B202_SENSOR_REF_01–03`. Sensor references are X.730m source-local, 120° apart; they are inherited recess references, not certified acoustic faces. Measurement surfaces, sections and markers remain world-fixed. Do not parent acquired information to tool rotation. The physical rear wall is a film cutaway, not literal removed rock.

Geometry objects `B202_GEOMETRY_irregular/tight/spiral` carry `radius_deviation_m` and `geometry_display`. The blue/red material reads only `geometry_display`; no numerical calibrated legend is implied. `B202_AMPLITUDE_independent` carries only `amplitude_display`, calculated from an independent authored azimuth/depth pattern; it has no radius input. Yellow/brown is signal-response illustration, not optical rock color, measured field data, validated lithology or oil detection.

## Build the progression in T27

Radzi's requested arc is **Scanning → Circumferential measurements → Reconstruction through depth → Geometry revelation**, with the borehole eventually the visual hero. Develop that with Scene Director, purposeful camera arrivals, natural timing and causal continuity; start with an inexpensive motion study for Radzi feedback. T8 stills anchor geometry/meaning; they do not prescribe equal durations, frozen holds, lens paths or final choreography.

Use [presets](../../../Mechanisms/B202/presets_v008.json) as explicit still states, [geometry tables](../../../Mechanisms/B202/sampling_tables_v008.json) and [lookup helper](../../../Mechanisms/B202/Scripts/sample_profile_v008.py) to create wall-registered acquisition history. `sample_wall(tables, profile, x, azimuth)` returns an interpolated point on the illustrative sampled envelope. It handles the azimuth seam and rejects outside depths. It interpolates mesh chords; it is not an acoustic ray solver or eccentricity/mud correction. For triangle-exact sensor rays or eccentric placement, ray-cast the source mesh and reverify. Sparse markers and global `scan_fraction` are not a complete capture-history rig; T27 should create per-event/per-depth history without moving prior readings with the tool. Preserve three sensor phases and derive complete-tool direction from the chosen surface-to-bottom viewpoint; source pin/box end identification is still unvalidated.

All curves/surfaces are editable independently and stored without animation. The information layer and physical wall share coordinates. Do not invent additional motion in the approved still masters; create versioned T27 consumers. Material/color representation changes that materially alter meaning return to targeted review; timing and continuity are T27's explicit responsibility.

## Clearance and limits to preserve

Tight: nominal radius155.575mm, maximum authored inward departure1.2mm; analytic minimum154.375mm. Full unchanged tool envelope radius152.400077mm leaves **1.974923mm conservative centered radial clearance**; sampled minimum radius154.378469mm. This bound covers axial travel and arbitrary axial rotation only for a straight centered tool. The interpolated polygon was checked at108 azimuths with >1.5mm residual clearance. No bit proxy is present: a nominal12.25in gauge bit would not clear the tight restriction. Do not depict it drilling or passing through this case. No restriction cause, loaded/eccentric/dogleg passage or operating-safety conclusion is established. Make only bounded changes and rerun clearance checks.

Spiral: exact T6 authored outward-only profile,25.4mm amplitude/1.8m pitch are illustrative authoring parameters, not field measurements or a diagnosis. Irregular wall is T6's outward-only washout. Hardware/face/calibration O04 and content-specific O05/O14 remain open for engineering review. No restricted ENP1 data used. Stills and controls do not prove animation continuity, real resolution or reconstruction accuracy.

## Source replacement and handoff custody

Append the whole named master collection to a fresh versioned consumer so internal drivers/node references remap together, or open a copy of the master. Reopen and test the consumer; do not link read-only controls without appropriate overrides. T5 remains replaceable. Incoming hardware requires inspecting differences, mapping transforms/sensor references, rebuilding local presentation copies, relinking and rerunning source/clearance/occlusion/continuity tests. Relinking the hidden source instance alone does not update presentation copies.

Builder/config/tables/presets/checks/report/stills are tracked review artifacts. Native `.blend` files remain organized locally and ignored; Git synchronization is not a binary backup or transfer to another machine. A T27 agent on another machine must obtain these exact binaries or rebuild with the required T5/T6 local sources; scripts cannot recover an unavailable original CAD library. Hashes for all seven native files and six PNGs are in the verification manifest. Human still acceptance and the live dependency precede T27 execution.
