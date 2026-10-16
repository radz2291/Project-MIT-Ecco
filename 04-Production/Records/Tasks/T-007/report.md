# T7 — Constant-speed contact correction v005

Task fbe3e8c3-5ccf-4205-9aa4-48832b0d2cd3. Base00a2f042b8c00d6f6160bd2de2545c768fbf6d20. Radzi accepts v004 overall but rejects the outgoing signal easing out on reaching the surface. This pass removes that deceleration. Prior v004 and approved stills retained. Still05/waveform/distance graphics remain KIV/excluded.

## Review summary

[Updated 10-second preview](../../../Mechanisms/B201/Previews/Motion_v005/B201_pulse-echo_fast-preview_v005.mp4): outgoing cyan wave travels at a constant per-station speed before, at and beyond the actual wall contact. The same spatial intersection drives the rock's local cell response; contact age now uses the actual propagation speed to retain the cell maturation/decay duration. The emerald return and sensor reception timing are unchanged.

Camera, source hardware, actual wall, lighting, colors and fine cell design are preserved. The surface grows more promptly as a consequence of the uninterrupted wave. No new beat, text, waveform or finishing. Three ping cycles,240 frames,24fps,960x540,silent.

Measured native render time: **0.687 seconds/frame average; 2.006 seconds slowest**. All 240 frames remain below10 seconds. All delivered frames decoded successfully; 240 distinct, no blank frames. [Video QA](Evidence/Motion_v005/video-qa.json) | [Render timing](Evidence/Motion_v005/render-progress.json) | [Output manifest](Evidence/Motion_v005/output-manifest.json). Representative contact buildup and reception frames visually inspected.

## Editable source and verification

Scene: `04-Production/Mechanisms/B201/Scenes/B201_pulse-echo_fast-preview_v005.blend`.

[Build](../../../Mechanisms/B201/Scripts/build_motion_preview_v005.py) | [Contact material](../../../Mechanisms/B201/Scripts/wall_contact_flow_v005.py) | [Render](../../../Mechanisms/B201/Scripts/render_motion_preview_v005.py) | [Verification](Evidence/Motion_v005/verification.json) | [Direction contract](../../../Mechanisms/B201/direction.md).

55 saved-scene checks pass: source wall and exact evaluated product geometry unchanged, camera/relative libraries preserved, three outgoing contacts and same-original-cap receptions correct, first emerald response not early, no Still05/text/diagnostics. Additional checks measure actual saved wave-apex displacement for nine frames spanning each wall contact: speed equals that station's stand-off divided by leg frames throughout. Native keys/material nodes; no frame-handler dependency.

Accepted T5 plugged v002 and T6 well v003, Still03 v013 and Still04 v003 remain unchanged. Preview consumer geometry is replaceable. Emit/contact/receive frames remain8/28/48,88/107/126,168/185/202; station rotations0/6/12 degrees. This is slowed illustrative timing, not physical sound speed/RPM, validated acoustic simulation or literal rock-texture acquisition. O04 calibration and B206/MIT review remain open. No client contact.

[Contact buildup](Evidence/Motion_v005/Decoded/decoded_f031.png) | [Surface settling and return](Evidence/Motion_v005/Decoded/decoded_f038.png) | [First reception](Evidence/Motion_v005/Decoded/decoded_f048.png)

## Review and synchronization

Review question: does the outgoing signal now reach the surface with the correct uninterrupted motion? The rest of v004's direction is retained. Exact v005 moving candidate awaits visual review; full T7 is not self-accepted. Still05 remains excluded and broad waveform work deferred at owner instruction.

Implementation/report/evidence and three selected review frames synchronize to authorized main. Exact containing SHA and pinned report are recorded in Rolladice after fresh remote verification. Blend, MP4 and raw frames remain organized locally only, without implied remote media backup. Prior report archived as report_motion_v004.md. No downstream scope or final finishing.
