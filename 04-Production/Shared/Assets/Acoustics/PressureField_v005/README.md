# Assumed pressure-field model v005

This package generates numerical pulse samples and uses them to show pressure passing through the inspected S02 sensor/wall gap. It is **model-driven, not measured ECCO data**. Presentation remains an owner-review proof. The later v006/v007 native files adapt the renderer/fixture without changing the model.

Sound in the fluid is represented as longitudinal pressure variation. Fixed transverse display slices change signed color and visibility; no material is shown moving sideways along a sine-shaped wire. Evident's [wave-propagation tutorial](https://ims.evidentscientific.com/en/learn/ndt-tutorials/flaw-detection/wave-propagation) explains the distinction between longitudinal and shear motion. Precision Acoustics' [transducer FAQ](https://www.acoustics.co.uk/reference/faq/) explains how resonance/damping affect pulse duration and bandwidth. Neither supplies the actual ENP3 parameters used here.

## Explicit assumptions

| Parameter | Value / status |
|---|---|
| Gap | 0.024575852808900598 m from inspected S02 source anchors |
| Fluid sound speed | Assumed 1500 m/s; not a measured mud calibration |
| Carrier | Assumed 400 kHz; not an ENP3 specification |
| Source pulse | 8 µs finite support, Hann taper multiplied by exponential decay with 6 µs time constant and sinusoidal carrier |
| Samples | 50 ns interval / 20 MHz sample rate |
| Normalization | Pulse divided by its maximum absolute sample; dimensionless pressure |
| Pressure reflection | Assumed +0.55 scalar planar-boundary coefficient |
| Attenuation | Assumed 4 Np/m, amplitude applied over actual traveled distance |
| Wave model | Linear 1-D homogeneous nondispersive fluid; one reflection |
| Absent | Beam spreading/diffraction, solid elastic modes, multiple interfaces, actual transducer/receiver response, gain/filter/noise, measured calibration |

For source samples `q(t)`, fixed distance `s` from the sensor, gap `D`, speed `c`, amplitude attenuation `a` and scalar pressure reflection `R`:

```
p_out(s,t) = exp(-a*s) * q(t - s/c)
p_return(s,t) = R * exp(-a*(2*D-s)) * q(t - (2*D-s)/c)
p_total(s,t) = p_out(s,t) + p_return(s,t)
```

Samples outside the finite source support are zero. Leading contact is at 16.3839 µs; first return is at 32.7678 µs. The receiver's returned peak is later because the source burst has duration. The returned amplitude scale is approximately 0.451832 after the assumed reflection and two-way attenuation. At the wall the two components superpose; the display uses their signed sum, not two independent arbitrary brightness animations.

The source's computed amplitude −6 dB band is approximately 274–526 kHz, with FFT peak about400.1 kHz. It is a smooth finite burst with spectral tails, **not strictly bandlimited**. These are measurements of the authored samples, not instrument bandwidth. Because each authored pulse is normalized, changing damping changes normalized shape/duration/spectrum; this model does not predict absolute transmitter power. Display gain is separate.

## Reproducible data and controls

`Scripts/pressure_model.py` supplies `Model`, `pulse_samples`, `components`, `export_model`, `read_csv`, and `verify`. `Model` exposes gap, speed, carrier, support duration, damping, sample interval, attenuation and reflection. Parameters are validated before samples are generated. Do not drive geometry/phase with cinematic animation.

`Data/source_pulse.csv` contains signed source samples; `source_pulse.json` preserves assumptions and metadata. `receiver_model.csv` contains the modeled source/returned/summed response at the sensor. `pressure_field_samples.npz` is a local numerical cache of the actual fixed spatial/time samples used for the proof.

`verify()` tests pre-source and pre-echo causal zero, contact/return timing, gain, wall superposition, changed sound speed against sampled output peaks/support, zero reflection, metadata preservation and rejection of receiver-only input as a full field. Test results are in the T-056 record. These are model self-consistency tests, not independent physical validation.

## Later recorded input

CSV uses columns `time_s,amplitude`; its companion JSON must identify `kind`, `source_label`, `signal_role`, `time_unit`, `amplitude_unit` and `time_zero_definition`. Recorded input also requires `sensor_context`, `gain_filter`, `provenance_reference`, and `use_permission`. Retain known/unknown metadata honestly. Do not substitute ENP1 report-display arrays for a recorded time series.

`signal_role` distinguishes `source_pressure` from `receiver_trace`. A receiver voltage trace can be imported with its metadata, but `components()` refuses to infer an entire spatial field from it. Source-pressure input requires Pa or explicitly normalized pressure; other units require an explicit sourced pressure calibration. Voltage is never silently treated as pressure. Any calibration must be appropriate to the source waveform; a full transducer transfer function is not modeled here.

## Visual/cinematic mapping

Native camera animation is preserved. Physical model time is `(native_frame - 300) * (D/c) / 9`. Thus native300/309/318 align to source onset/contact/leading return. Rendering quarter-frame samples from298 through324 provides 105 frames; playback at24fps yields4.375 seconds of deliberately slowed review. This is not actual acoustic speed on a movie timeline.

The 96 fixed slices are display sampling cross-sections, not solved beam geometry. Their annular radii4.3/4.5mm are visual choices. Cyan indicates positive signed pressure and blue-violet negative pressure—not outbound versus return. Visibility/opacity derives from absolute summed pressure, with a documented0.035 cutoff and1.15 display normalization. Zero pressure is invisible. Source, field and cinematic time are separate quantities.

No original scene is overwritten. Native/video caches remain local; owner visual acceptance and final shared-library integration remain pending.
