# B202 v009 — Synthetic ultrasonic mechanism

16 October 2026. Owner-approved technical addendum to T8/B202-S, following Engineering Mechanism Specification v1 and the approved bounded plan. **Synthetic forward–inverse consistency demonstration, not actual ENP3 DSP, calibrated telemetry, validated sonic performance or formation classification.** Exact specification is retained locally in T8/Private; confidential field-report metadata is not republished. No original log imagery or client video is used.

## Inputs and authority

T5 plugged v002 supplies the real source-local tool and three inherited sensor reference transforms. T6 well v003 evaluated nominal/irregular/spiral triangles supply synthetic ground truth, in source X metres. Tight is the separately labeled v008 hypothetical restriction. Shared files and v008 remain unchanged. [Configuration](acquisition_config_v009.json), [case/sensor/source index](Data/v009/index_v009.json), [source preservation snapshot](../../Records/Tasks/T-008/Evidence/v009/preservation_before_v009.json).

The imaging references are 120° apart on one plane; their inherited positions/normals are provisional proxies. The source-local .730m plane is not certified against the datasheet's pin-shoulder datum. `sensor_radial_offset_m=0` is an explicit demo calibration parameter, not confirmation of an acoustic face. Real mud calibration, blind zone, gain, waveform estimator, uncertainty, beam properties and proprietary eccentricity compensation are unknown.

All acoustic/material/schedule constants below are **authored demonstration values**: mud speed1500m/s, density1000kg/m³, attenuation4Np/m, unit transmit scale, incidence exponent2, range reference.03m, minimum-return threshold1e-6, blind-zone threshold.0001m. They are not taken from the confidential ENP1 log. Nominal radius.155575m is the accepted illustrative12.25in T6 case, not universal deployment fit.

## Deterministic forward model

[Producer](Scripts/build_acquisition_v009.py) opens T6 in an isolated background Blender process and obtains evaluated world triangles. It transforms each actual inherited sensor origin and outward direction with the **whole-tool** fixture pose. The first wall intersection is obtained from triangle geometry, not a radius lookup. Blender BVH is the fast path; numerical misses at shared triangle edges are independently checked using a float64 Möller–Trumbore intersection. A miss remains missing if no valid triangle hit exists within range. The chosen method is recorded per event. Earlier single-precision seam diagnostics are preserved locally, not counted as accepted data.

For stand-off `d`, `TOF = 2d/c_demo`. Each event is monostatic: receiver ID equals emitter ID. This is a scalar reciprocal-return model; it does not solve an elastic wave field, specular return geometry, cross-talk, diffraction, waveform bandwidth or ENP3 signal processing.

Synthetic response:

```
Z_mud = demo_density * demo_sound_speed
rho = abs(Z_material - Z_mud) / (Z_material + Z_mud)
incidence_factor = abs(dot(-ray, triangle_normal)) ** 2
attenuation = exp(-2 * alpha_demo * stand_off)
range_factor = (range_reference / (range_reference + stand_off)) ** 2
echo_strength = transmit_scale * rho * coherent_patch_factor
                * incidence_factor * attenuation * range_factor
```

This simplified normal-incidence impedance contrast and authored incidence/range factors physically motivate a **unitless synthetic received strength**, not a calibrated amplitude estimator. Uncorrected received strength can change with geometry even when material remains fixed. No proprietary compensation or reliable formation classification is implied.

Material inputs are explicit: constant6MRayl for controlled comparisons; layered4.5/7/10MRayl synthetic response, a flat boundary at X2.4m and inclined plane `X=3.35+Y-.5Z`, and an ellipsoidal weak coherent-return patch centered at `(3.8,-.15,0)m`. These are independent geological/interface fixtures, not painted rock or UV sine patterns. Material-only comparison replaces constant6MRayl with10MRayl in X[2.4,3.35). Geometry-only comparison perturbs a bounded sector of a copy of T6 irregular wall outward, leaving constant material unchanged. Seed9009 is recorded; noise is disabled.

Fixture acquisition uses13 depth stations,108 whole-tool orientations per station and all three sensors:4,212 events per full case.108 output bins are an explicit visualization choice; this does not infer raw ENP3 cadence or resolution. Fixture timestamps use.01s event increments and quasi-static poses, not physical drilling speeds. T27 must deliberately retime and unwrap rotational phase; no scene is animated in T8.

## Measurement-only inverse and reconstruction

[Core inverse](Scripts/acquisition_core_v009.py) accepts recorded origins, directions, simulated travel times, sound speeds, echo strengths and validity only. It has **no wall mesh or ground-truth hit-position input**. Ground truth is stored separately for verification. It computes `d_est=.5*c_event*TOF`, `p_est=origin+direction*d_est`, world X/azimuth and radius relative to the declared well axis, then `delta_radius=radius-R_nom`.

The baseline is straight and centered. An eccentric test supplies a known synthetic translation and the same fixed reference axis; it does not estimate unknown tool pose or implement ENP3 eccentricity correction. Invalid/weak returns remain flagged and do not create a reconstructed vertex.

Samples are assigned to nearest configured depth and108 azimuth bins; valid contributions are averaged with saved event IDs/weights. Geometry and amplitude keep distinct lineage/validity. Every grid node records measured/interpolated flags, first/ready timestamps, contributors and values. Bins with no evidence retain null scalars. An optional **isolated one-bin** interpolation fixture references adjacent bins/events/weights and remains `measured=false`; no large-gap bridging or depth extrapolation is performed.

Displayed mesh vertices are generated **only from reconstructed radii** at registered grid centers. Faces connect four available neighboring grid nodes and never bridge missing corners. Face interiors and their colors are linear/barycentric interpolation of those node values, not additional measured pixels. Polygon interpolation and grid binning are explicit reconstruction approximations; the masks label acquired nodes versus gap-filled nodes. Under sparse acquisition large unsupported sectors remain absent. White nominal is a separate registered reference; blue/red geometry reads `delta_radius`, yellow/brown reads `echo_strength` on the same reconstructed positions. Neither colormap generates the other.

## Cases, records and reuse

Eleven acquisition cases cover nominal constant, T6 irregular constant, geometry-only change, material-only change, T6 irregular with geological response, T6 spiral, hypothetical tight, known eccentric pose, sparse arcs, missed returns and rejected weak echoes. There are42,510 total records. `Data/v009/*events*.json.gz` contains measurements/pose/factors/quality; `*truth*.json.gz` contains separate ground-truth intersections; `*grid*.json.gz` contains reconstructed fields/masks/lineage. Gzip is deterministic (zero timestamp), ordinary JSON after decompression. [Example complete bin trace](../../Records/Tasks/T-008/Evidence/v009/example_bin_trace_v009.json) is directly readable.

The v009 native consumer reuses v008 hardware/lighting/palette but permanently suppresses its visual-only information layers. New data objects expose source-case, quantity, `cell_index`, radius/deviation, received strength, measured/interpolated masks and ready time. [Replay adapter](Scripts/replay_interface_v009.py) applies a numeric event pose without keyframes. Cached full-grid display reveals bins only after **all contributing records** are available; for evolving partial-bin estimates, `grid_at_time` recomputes from records up to the cutoff, preventing future-average leakage.

## Acceptance and limits

[101 mechanism checks](../../Records/Tasks/T-008/Evidence/v009/verification_acquisition_v009.json) cover specification tests1–9, forward/inverse consistency, independent triangle/analytic references, controlled geometry/material changes, known eccentric poses, sparse/missed/weak returns, three sensors, clearance, lineage, interpolation and deterministic regeneration. [165 consumer checks](../../Records/Tasks/T-008/Evidence/v009/verification_consumer_v009.json) cover data binding, fresh saved scenes, masks/replay, separate fields, source preservation and append reuse. These are agent self-checks; same-model consistency is not independent acoustic validation.

Tolerances are explicitly model/tessellation checks: point inverse2µm; nominal96-sector cylinder versus analytic circle.1mm; grid-center versus independent ground-truth triangle ray.15mm. They are **not instrument accuracy specifications** and do not establish accuracy between acquired depth stations. Continuous display faces interpolate between stations.

Triangle-faceted tight geometry has a conservative centered full-tool radial clearance of1.8923mm (sampled minimum1.9098mm), more conservative than v008's continuous-radius1.9749mm bound. The nominal12.25in bit cannot pass; no bit is shown. No loaded/eccentric/dogleg operating-safety claim or restriction cause. Source sensor-face/datum, real mud calibration, acquisition schedule, amplitude normalization and real eccentricity processing remain MIT review items.

**Specification test10/playable proof is explicitly deferred to T27 by Radzi.** T8 delivers deterministic data, static comparisons, tested replay primitives and editable assets; it has not delivered or passed a moving proof. No public field-report reuse, measured-ENP3 claim, complete live-log telemetry or final visual/engineering approval.
