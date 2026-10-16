# T7 — Fast pulse/contact/echo animation v002

Task fbe3e8c3-5ccf-4205-9aa4-48832b0d2cd3. Owner authorizes animation if rendering is below10seconds/frame and accepts lower preview quality. Explicit follow-up: **do not use Still05 in the animation**. This supersedes prior motion pause for this bounded work; earlier T26 override remains applicable. T5/T6 dependencies accepted. Full T7 is not self-accepted; waveform remains KIV/excluded.

## Review summary

[10-second native animation](../../../Mechanisms/B201/Previews/Motion_v002/B201_pulse-echo_fast-preview_v002.mp4): three cyan pulse departures → actual wall sampling → tighter emerald returns → same sensor receives. Fixed accepted camera, real ECCO/irregular wall and small whole-tool station changes between round trips. No waveform, Still05 frame, distance graphics, labels, arrows, formulas or numerical overlays. Silent technical preview,960×540,24 fps,240frames.

**Measured speed: 0.677s/frame average, 2.036s slowest.** All 240frames under 10seconds. Total native frame rendering162.98seconds, excluding setup/encoding. EEVEE 32 samples on local GTX1060. Four source-quality stills/masters retained; product presentation/shadows/transparency simplified in a separate preview consumer.

Editable scene: `04-Production/Mechanisms/B201/Scenes/B201_pulse-echo_fast-preview_v002.blend`. [Build script](../../../Mechanisms/B201/Scripts/build_motion_preview_v002.py) | [Render script](../../../Mechanisms/B201/Scripts/render_motion_preview_v002.py) | [Fast profile](../../../Mechanisms/B201/preview-settings_fast_v002.json) | [Direction contract](../../../Mechanisms/B201/direction.md).

[Wall-contact frame](Evidence/Motion_v002/Decoded/decoded_f028.png) | [First reception](Evidence/Motion_v002/Decoded/decoded_f048.png) | [Second reception](Evidence/Motion_v002/Decoded/decoded_f126.png)

## Geometry and timing

Accepted product instances are copied at exact evaluated coordinates/topology into an isolated local preview consumer; source libraries remain linked for provenance and unchanged. Native keyframes control three frozen stations 0°, 6°, 12° relative to selected pose. The wall stays fixed; each outward ray determines a real wall endpoint, and the return ends at the original cap face. One shared slowed illustrative spatial speed gives equal outbound/return legs at each station, with different intervals for different stand-offs. Sensor response begins on the exact first reception frame. This is an explanatory timing convention, not acoustic simulation, measured TOF or physical RPM. Frame events and actual source-derived endpoints are recorded in build.json.

Source Still04 v003 provides the emerald packet and sensor response; selected Still03 v013 provides the preserved wall/scan treatment. Current camera is held intentionally for cause/event/result comprehension; no new B3 camera choreography. Early ping/contact progression is present at all three stations. No physical sensing light or textured rock-image measurement claim. O04 acoustic calibration remains unresolved.

## Verification and outputs

[Saved-scene verification](Evidence/Motion_v002/verification.json): 41 checks pass, including exact evaluated product geometry, source hashes, wall correspondence, per-station round-trip order, exact outbound contact/same-sensor reception, first emerald response, fixed camera and absence of Still05/visible text. Initial checks exposed an inactive-view-layer evaluation issue; corrected by explicitly selecting the actual rendered preview view layer, then all endpoint tests passed.

[Video QA](Evidence/Motion_v002/video-qa.json): all 240 delivered frames decoded,239 distinct, no blank frames,960×540/24 fps/10seconds; representative decoded emission/contact/return/reception frames visually inspected. [Render timing](Evidence/Motion_v002/render-progress.json) | [Manifest](Evidence/Motion_v002/output-manifest.json) | [B206 review questions](review-questions_motion_v002.md) | [Scoped register](proof-register_motion_v002.md).

Benchmarks preserved: initial multi-layer EEVEE8/64samples met speed but gave stochastic transparency grain. Native blended EEVEE consumer removes that Z-mask artifact. Motion v001 preserved; v002 aligns emerald onset to exact first reception and opens in its intended preview layer. This is a lower-quality preview, not a new final material/lighting direction.

## Remaining review and synchronization

Authorized pulse/echo animation is reviewable. **Still05 remains KIV and is absent**, so the broad ticket's moving-waveform criterion is deferred at direct owner instruction; no false full-task completion. B206/MIT technical feedback and Radzi acceptance remain pending; no client contact. Corrections will be versioned and reverified.

Reviewable reports/scripts/configuration/evidence/selected stills synchronize to established main; exact containing SHA and pinned report recorded in Rolladice after fresh remote verification. Editable Blend, MP4 and bulk frames stay organized locally, without remote media backup. No final finishing, downstream task execution or self-acceptance.
