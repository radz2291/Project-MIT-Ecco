# T7 / B201 — reusable pulse/contact/echo handover

Radzi visually approves Motion v005 (“Ok good”) and requests wrap. No further render/animation is requested. Full T7 remains in human Review; Still05/waveform/distance graphics KIV, B206 technical review pending.

## Exact baseline

- Native scene: `04-Production/Mechanisms/B201/Scenes/B201_pulse-echo_fast-preview_v005.blend`.
- Preview: `04-Production/Mechanisms/B201/Previews/Motion_v005/B201_pulse-echo_fast-preview_v005.mp4`.
- [Source and native keys](../../../Mechanisms/B201/Scripts/build_motion_preview_v005.py), [wall material](../../../Mechanisms/B201/Scripts/wall_contact_flow_v005.py), [saved-scene checks](Evidence/Motion_v005/verification.json), [exact file hashes](Evidence/Motion_v005/output-manifest.json).
- 240 frames,24fps,10 seconds,960x540,EEVEE32. Mean0.687s/frame,max2.006s. 55 checks and240 decoded frames. Heavy media remains local-only; synchronized repository contains scripts/reports/evidence/selected frames.

## Reuse controls and constraints

`B201_MOTION_CONTROL`: transmit,receive,outgoing_fade,return_fade. `ACOUSTIC_CONTACT_CONTROLLER`: leading_radius_m,propagation_m_per_frame,scan_fade,scan_radius_x_m,scan_radius_y_m,cell_size_m,scan_opacity,contact_band_m. Fine-cell wall response is a material on actual retained rock geometry; local signed sphere/rock distance controls arrival, varied maturation and local age decay. Outgoing radius is linear through contact. Emerald return starts at actual wall hit and first reception reaches the original physical cap.

The build reads unchanged Still04 v003 (including selected Still03 v013 treatment) and uses unchanged T5 plugged v002/T6 well v003. Product is an exact evaluated frozen preview consumer; rebuild/reverify if hardware changes. Same accepted camera, source wall snapshot and source dimensions; do not substitute a different live wall reevaluation silently. Native keys/material nodes work without handlers. Use saved fast preview view layer. Version new consumers; preserve approved stills and motion variants.

Three station angles0/6/12 degrees are a repeatability illustration. Emit/contact/receive frames8/28/48,88/107/126,168/185/202. Timing, beam surfaces, cyan sampling and emerald reception are illustrative, not calibrated acoustics/RPM or literal rock-texture measurement. Source face/time-zero O04 remains open. Do not interpret amplitude as geometric radius.

## Scope boundary

T7 owns an individual pulse-to-reception explanation and its short repetition. T8 / B202-S owns scanning/axial sample accumulation, nominal/enlarged/tight/spiral reconstruction examples and separate radius/amplitude presentation, delivered as approved stills/source handover. Fresh-agent T27 / B202-M animates that explanation after its prerequisite. Reuse B201 effects rather than rebuild them; geometry, sampling and output interpretation still require their own source checks and visual decisions. No scanning/reconstruction or downstream shot was executed during this wrap.
