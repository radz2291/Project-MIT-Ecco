# ECCO-056 — Model-driven pressure proof v007

30 October 2026. **Focused proof for owner review; not a finished shared asset or accepted appearance.**

The sensor emits a finite pressure pulse, it reaches the wall and a weaker reflected pulse returns. The visual now comes from numerical pressure samples on fixed locations in the gap. There is no moving/wriggling wire or permanent path. Cyan and blue-violet show pressure sign, **not separate outbound/return categories**. Zero-pressure slices disappear.

## Review artifacts

- Native: `04-Production/Shared/Assets/Acoustics/PressureField_v007/S02_pressure-field-proof_v007.blend`.
- Motion: `Previews/pressure-field_v007_slow-review.mp4` (local; rendered quarter-frame samples at24fps,4.375seconds).
- [Outbound](Previews/pressure_outbound_v007.png), [contact region](Previews/pressure_contact_v007.png), [weaker return](Previews/pressure_return_v007.png).
- Numerical model, source/receiver CSV and metadata: `04-Production/Shared/Assets/Acoustics/PressureField_v005/`.

The native preserves original S02 camera animation. Samples use native frames298–324 in0.25-frame increments; playing105 frames at24fps is **4× slower than the native camera timing**. Physical time is separate: `(native_frame-300)*(gap/sound_speed)/9`. The model's leading contact is16.3839µs and return32.7678µs. These microseconds are model values, not measured ECCO timing.

## What is data-driven and what is assumed

The actual inspected source gap is24.5758528mm. Assumed speed1500m/s, carrier400kHz, finite8µs burst,6µs damping, attenuation4Np/m and scalar pressure reflection+0.55 generate signed numerical samples at20MHz. The source pulse is peak-normalized, so pressure is dimensionless; this does not predict absolute power. Its calculated amplitude−6dB spectral interval is approximately274–526kHz. It is a smooth finite pulse with spectral tails, not strictly bandlimited.

The fixed spatial field is the sum of a delayed attenuated outbound pulse and a delayed attenuated reflected pulse. At the wall both contributions superpose. No full elastic-wave solution, diffraction, beam spreading, multiple interfaces, actual transducer response, receiver filter or measured noise is modeled. Annular display cross-sections (4.3/4.5mm radii) are visual sampling geometry, not a solved beam size. Opacity and RGB both depend on absolute pressure; this is a disclosed nonlinear display transfer, not a calibrated luminance scale. A0.035 display cutoff removes near-zero clutter.

The [local audit](local-waveform-research.md) found no identified recorded RF series in the examined project candidates. Source CSV/JSON input accepts later samples with role, units and provenance. A receiver trace alone is rejected as a source for the whole spatial field. Recorded source voltage needs explicit sourced pressure calibration; it is not silently treated as pressure. See the [model README](../../../Shared/Assets/Acoustics/PressureField_v005/README.md) for parameters, mapping, interface and limits.

## Checks and remaining work

- Twelve numerical checks pass in `pressure-model-verification_v005.json`: causal zero, leading contact/echo limits, gain, signed wall superposition, actual sampled response under changed speed, zero reflection, metadata preservation, receiver-role refusal and explicit calibration handling.
- Source pulse metadata and small CSVs are retained. Fixed geometry was checked at seven native times (`pressure-build_v005.json`); no coordinates/transforms animate. V006/v007 change render materials/fixture light, not model/geometry.
- V007 benchmark305.5/310.5/316.5:2.628/1.116/1.118seconds full render-to-file,640×360 Eevee16. Batch timing is in `pressure-batch_v007.json`; the renderer stops on any frame≥5seconds.
- All105 batch frames completed: maximum2.353seconds, mean1.170seconds. The final frame has no pressure bands; original S02 recorded-wall cells appear after receipt as retained section behavior.
- Native reopened with relative ECCO link. Original S02 source is preserved. Master performs independent camera/model/visual checks.
- Current image is a deliberately cheap motion/data proof. Fixture light is simplified, samples have visible grain, and final cinematic appearance is not accepted.

V005 Workbench pressure images failed visually as dark stacked outlines; v006 made pressure bands luminous but fixture lighting was too bright. V007 lowers fixture lights1.515stops without lowering pressure emission and uses16samples. Earlier panel/worm/wire proofs remain retained superseded evidence.

The full reusable controls package, open-hole/cased presentation variants and final two-consumer migration are **not complete**. Owner feedback on this model-driven representation comes first. No calibrated ENP3 claim, client acceptance, field-data reuse, media upload or off-machine backup is claimed. Master alone integrates/pushes permitted files; this report is proof progress, not a finished Work submission.

## Authority and provenance

Task UUID `80c559e4-7e88-4acd-bfbf-46448545076a`, parent ECCO-051, worker `ECCO-056-builder-20261030`, run `24259eb9-f2c3-4e00-ac1a-6ab31bda81e6`. Base checkout `bb9a503c8d69ae0cf5ba20273a5280d130cc1949`. Owner explicitly requested research/data-driven improvement after v004. Primary-source grounding is [Evident's wave-propagation tutorial](https://ims.evidentscientific.com/en/learn/ndt-tutorials/flaw-detection/wave-propagation) and [Precision Acoustics' transducer FAQ](https://www.acoustics.co.uk/reference/faq/); numeric model parameters are authored assumptions, not extracted ENP3 specifications. Root's `waveform-research.md` provides the research synthesis.
