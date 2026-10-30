# ECCO-056 — Local waveform evidence and model inputs

30 October 2026. Owner says v004 still reads like a wire and requests research into waveform shape and a data-driven animation. **No further wire/path presentation is finalized.** Root handles external primary-source acoustics research; this note records only local evidence.

## Main finding

No identified recorded ultrasonic RF time/amplitude series was found in the bounded project search. The project contains useful geometry and **synthetic scalar** travel-time/echo-strength records, but those are not sampled waveforms. We can drive a later proof from explicitly modeled samples; calling that actual measured ECCO data would be false.

`audit_local_signal_data.py` searched `01-Brief`, `02-Reference`, `03-Context`, `04-Production`, `05-Previs` for common numerical-data/binary formats, excluding cache/scratch/dependency folders. It found 16 candidate files and inspected eight NPZ headers, plus the B202 compressed event record separately. `local-signal-data-audit.json` records paths, fields and limits. This is not proof that data does not exist in an unknown format, outside this checkout or on another machine.

## What is actually available

| Source | What it supports | What it does not support |
|---|---|---|
| `01-Brief/Chat/chat.md:196–219` | Client explanation: ping returns to same sensor; travel time relates to stand-off; waveform amplitude relates to formation response. Line206 names a forwarded WaveformExpress executable. | The named executable was not found in the inspected project. A chat filename is not an available numerical export; no executable was launched. |
| `01-Brief/Chat/chat.md:251` | Client's qualitative cement explanation: prolonged ringing for free casing; dulled response for cement-supported casing. | Exact oscillation frequency, decay constant, amplitude calibration or usable RF samples. |
| `04-Production/Records/Tasks/T-002/Evidence/datasheet-text_v001.txt:12–21,115–120` | Multi-frequency ultrasonic sensors and an in-situ mud-property sensor; application-specific tuning. | No numeric carrier frequency, bandwidth, sample rate, transmit impulse, receive filter, Q/damping or raw waveform series in the inspected text. |
| `04-Production/Mechanisms/B202/B202_acquisition_model_v009.md:9–17,22–35` | Explicit illustrative ray geometry, authored sound speed, scalar travel time, scalar echo-strength factors. Geometry and source/receiver IDs can ground a model's path. | Explicitly does not solve elastic wave fields, cross-talk, diffraction, bandwidth or ENP3 processing; real mud calibration, gain, blind zone, waveform estimator and beam properties are unknown. |
| `04-Production/Mechanisms/B202/Scripts/acquisition_core_v009.py:17–33` | Authored impedance contrast, incidence, two-way attenuation and range factors generate unitless strength. | No time samples or oscillation. The absolute impedance reflection coefficient even discards polarity; it is insufficient to recover a signed RF waveform. |
| `04-Production/Mechanisms/B202/Scripts/build_acquisition_v009.py:68–72` | Event explicitly tagged `synthetic_illustrative`; stores scalar `tof_2way_s`, `echo_strength`, sensor pose/direction and provenance. | These events cannot be relabeled raw recorded RF. `comparison_trace_depth3m_v009.csv` is an azimuth/depth profile of those scalars, despite “trace” in the filename. |
| `04-Production/Shared/Assets/Acoustics/Scripts/acoustic_event_v002.py:60` | Native sensor-to-wall intersection, same receiver identity, geometric anchors. | Timing explicitly says `illustrative_not_acoustic_velocity`; not acoustic samples. |
| `04-Production/Studies/S06_Report-Recreation_v004/README.md:45,77` | Authored radius field and normalized report-inspired visual trends. NPZ keys: radius/geometry/amplitude/theta/z/diameter. | No recovered report measurements; no waveform time axis, sampling metadata or RF samples. Other S03/S06 NPZ files are geometry/profile/normalized amplitude arrays, not time-domain RF. |
| `04-Production/Records/Tasks/T-002/report.md:55`; `03-Context/01_Foundation/02-ENGINEERING_BASELINE.md:73` | Original supplied field report exists, identified as ENP1, with rights constraints. | It is not ENP3 waveform data and cannot supply permission to publish field material. No private field-log values or imagery were copied into this research record. |

## Model-ready local inputs and missing inputs

Ready: the actual S02 proof source/return point and wall point are inspected; one-way distance is 0.0245758528m in the saved geometry. Send and return anchors match. Native event frames300/309/318 provide **cinematic timing**, not physical signal time. Geometry and animation timing must remain separate when generating samples.

B202's `acquisition_config_v009.json:3–16,33–39` offers reproducible **authored demo** values (sound speed, density, attenuation, incidence and range factors). These could be deliberately reused as a labeled synthetic fixture after the model is chosen, not silently promoted to measured ENP3 parameters. It has no transducer impulse response or waveform generator.

For an actual recorded-data proof, request a permitted export of one transmit/receive trace or small trace set: sample timestamps or sampling interval/rate, signed amplitudes and their units, time-zero/trigger definition, sensor/tool identity, acquisition frequency/bandwidth if known, gain/filter/normalization information, wall/medium context and permission for the intended use. Without those, a graph-shaped image cannot recover a faithful numerical waveform.

For a model-driven proof, first choose and label a pulse/receiver model from primary sources. Source pulse/transducer response, propagation delay/attenuation, reflection/interaction, receiver response and noise should determine samples; camera playback should display those samples without pretending display seconds equal acoustic microseconds. Which of these parameters are measured versus assumed must be explicit. Local evidence supports the need for these inputs, not their missing values.

The prepared `Shared/Assets/Acoustics/WaveformControls_v001/Scripts/fixed_waveform.py` is an **unvalidated controls scaffold**, not the new signal model or accepted presentation. It keeps geometry static and can preserve sample provenance, but its authored brightness envelope is not acoustic simulation. Development/finalization was stopped on the owner's research request.
