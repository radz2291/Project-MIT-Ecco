# ECCO ENP3 — Engineering Baseline

**Version:** 0.1 · 13 October 2026  
**Status:** **Canonical** ECCO engineering facts and unresolved engineering scenarios; shot-specific client verification remains required. Visual examples/storyboards cannot supersede this source.

## Sources and authority

| Source | Location | Authority / limits |
|---|---|---|
| ENP3 technical brochure and specification | [Datasheet](../../01-Brief/ECCO_ENP3_Datasheet-1.pdf), pages 1–3 | Model-specific published dimensions and operating descriptions; not independent performance validation |
| Mr. Ahmed's explanation | [7 October chat](../../01-Brief/Chat/chat.md), especially 8:51–10:02 PM | Intended technical explanation, five applications and narrative; examples require ENP3 compatibility checks |
| Product photos | [Client images](../../01-Brief/Image/) | Visual reference; match image/version to actual ENP3 asset before relying on it |
| Approved CAD | Location/version pending | Geometry authority once registered and technically checked |
| Generated artwork and four-second sample | [Reference folder](../../02-Reference/); sample location pending | Creative/workflow evidence; not validated anatomy or acoustic simulation |

The facts below are attributed to MIT's supplied materials. They do not establish that the sample has accurately depicted them.

## Product facts to preserve

| Topic | Sourced baseline | Source |
|---|---|---|
| System | Memory While Drilling; multi-frequency ultrasonic pulse-echo; independent recording from other LWD/MWD tools in the BHA | Datasheet p.1 |
| Imaging sensors | Three sensors, 120° apart, on one sensor plane | Datasheet pp.1–3 |
| Sensor position | Plane 60 cm above the lower pin shoulder | Datasheet pp.1–3 |
| Mud sensor | Dedicated in-situ mud acoustic-property measurement and velocity correction | Datasheet pp.1–2 |
| Acquisition | Rotating and sliding modes; optimized dynamic resolution described up to 180 RPM | Datasheet p.1; p.3 |
| Body | Non-magnetic; exact alloy, physical color and finish not established | Datasheet pp.1–3 |
| Nominal length | 2.25 m / 225 cm; actual length may differ slightly | Datasheet pp.1,3 |
| Maximum OD | 12 inches at central pads | Datasheet p.3 |
| Fishing-neck OD / minimum ID | 8.25 inches / 2.25 inches | Datasheet p.3 |
| Minimum casing ID | 12.3 inches | Datasheet p.3 |
| Connections | Top 6-5/8 inch F.H. Box; bottom 6-5/8 inch F.H. Pin | Datasheet p.3 |
| Azimuthal sampling | 108 bins per revolution | Datasheet p.3 |

Do not turn every specification into an on-screen claim. Use only what a shot requires and what MIT approves for publication.

## Motion, sensing and data

- The chat describes clockwise drill-string rotation **when viewed from the surface toward the well bottom**, with slower downward progress. Do not reverse that viewpoint inadvertently.
- The stationary tool in the isolated first-ping sample is a staging choice. It must not replace rotation/translation in a shot explaining drilling or circumferential scanning.
- A sensor fires outward; an echo returns and is measured. Time of flight supports geometry; the dedicated mud measurement supplies velocity correction. An expanding luminous wall is an explanatory representation, not the physical wall being created.
- The client's formation/amplitude explanation supports a qualitative formation-imaging story. Do not imply direct oil detection, definitive lithology classification or other unsupported conclusions.
- The full client narrative includes rotation and accumulation into an image, not only a one-way flash. Decide which portion each shot explains and review it explicitly.
- Memory acquisition must not be depicted as high-bandwidth live transmission of full logs to the surface. Distinguish recording downhole from later download/processing when showing the output.
- Keep artistic time/scale exaggeration separate from a calibrated measurement. No invented numeric TOF, waveform, dimensions or calibrated color legend.

## Five applications

| Application | Explain visually | Required technical check |
|---|---|---|
| Open-hole geometry | Pulse/echo distance becomes a readable profile with asymmetry or washout | Tool/wall clearance, geometry derivation, eccentricity and applicable example |
| Formation indications | Qualitative return/amplitude pattern becomes a circumferential image | Approved colors and interpretation; do not use decorative strata as measured results |
| Cement evaluation | Casing response differs with cement support; behind-casing condition becomes a map | Free vs supported casing explanation, waveform treatment, TOC if included |
| Casing integrity | Internal profile makes wear/metal-loss concern understandable | Which observable supports the shown conclusion; no unsupported thickness inference |
| Hydraulic enhancement | Annular mud and cuttings respond to three body stages | Pad geometry, flow direction, operating mode and limits of illustrative effects |

## Hydraulic module

The datasheet p.2 defines three sequential stages:

1. **Accelerators:** three pads increase local annular-flow velocity.
2. **Twisted pads:** two sets produce mud jetting and controlled turbulence.
3. **Diffuser:** recovers pressure and addresses the low-pressure wake behind the pads.

It describes independent hole-cleaning action from **rotation only**, **tripping only** or **circulation only**, with additive combined effects. Do not depict rotation and circulation as jointly required. Confirm the mode selected for the film. Flow visualization is illustrative unless supported by a validated simulation; no invented CFD pressure values or quantified performance comparisons.

## Scenario conflicts to resolve before construction

**Dimensions:** the client chat uses 12.25-inch and 8.5-inch bit sizes, with 9-5/8-inch and 7-inch casing OD, to explain well construction generally. These must not automatically become the ENP3 scene dimensions. The sheet lists 12-inch maximum tool OD and 12.3-inch minimum casing ID. Inference from those figures: the smaller casing examples cannot be depicted as accommodating this ENP3 version. Ask for the actual ENP3 drilling/casing scenario and confirm clearances before scaling the assembly.

**Sensor/effect origin:** confirm the actual CAD sensor plane and face orientation. Prior recess-based sample effects are exploratory. Three orthogonal or gyroscope-like rings do not establish three sensors at 120°.

**Data identity:** the earlier Mi-VU report was identified as an **ENP1** test. Verify the source itself, permissions and permitted labeling before using it; never relabel it as ENP3 output.

**Asset edits:** presentation plugs, cores or end closures made for visual cleanup must be identified and reviewed. The current repository does not contain the registered production CAD or `.blend` files.

## Technical preview checklist

- [ ] Geometry/version, units, sensor count/plane and visible features are checked against the supplied asset.
- [ ] Tool, bit, casing and annulus have an approved compatible configuration.
- [ ] Rotation, translation and pulse/echo direction match the shot's operating mode.
- [ ] Origin → interaction → measured/illustrated outcome is legible.
- [ ] Artistic effects are distinguished from physical simulation and factual data.
- [ ] Memory recording and later output are represented coherently.
- [ ] Hydraulic stages and selected operating mode are correct.
- [ ] Product claims, output imagery and any numbers have approved sources.
- [ ] The client has reviewed the exact preview/version before final finishing of the mechanism.
