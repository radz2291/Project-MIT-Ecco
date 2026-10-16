# B202-M / T27 — Scene Direction Contract v001
**Concept:** The Shape Left Behind
**Stage:** D1 artistic premise approved by Radzi, 16 October 2026; D2 exact scene/camera blocking and D3 moving preview remain pending.
**Scope:** B202-M standalone, near-final **mechanical animation**; B3 will own integration into S02/S03 and the final full-film edit. This document is the single motion-direction contract for T27, using `rolladice-scene-directive/v0.2`. B202-S v009 model and `direction.md` remain authoritative on acquisition/information correctness.

## 1. Purpose, viewer experience, and continuity

**Creative thesis:** **ECCO moves. The acquired information stays. The camera stops following the tool and discovers the hidden borehole volume left behind by its measurements.**

Audience progression: **mystery → recognition → revelation**.
- **Prior information (S02):** T7 has established sensor origin, outward ultrasonic pulse, wall interaction and echo returning to the same sensor. Do not remake the complete ping/waveform tutorial; the waveform/distance graphic remains KIV and is not silently restored.
- **B202's information:** Repeated valid measurements establish registered points, then a borehole circumference, then shape through depth; actual nominal-vs-measured differences become visible. A separate amplitude view introduces the other echo quantity.
- **Exit toward S03 / later S06:** Irregular geometry is the hero; a later beat can introduce independent yellow/brown acoustic amplitude. **Do not animate blue geometry morphing into brown amplitude**, and reserve a full cylindrical-to-flat map unwrapping for S06/B205.
- **Editorial reference:** S02 0:19–0:22 ring handoff; S03 0:22–0:40 open-hole geometry and amplitude. These are planning windows, not a B202-M fixed runtime or a claim about actual acquisition time.

## 2. Core composition and camera score (qualitative, not fabricated CAD poses)

**Arrival A — The instrument discovers (intimacy).** Begin near the actual inherited ECCO sensor plane inside rock context, continuing the T7 spatial relationship. Whole tool rotates and advances; localized, understated cues identify measurement events. Sensor remains recognizable. Keep the physical wall and hardware legible. **No oversized wave shells or generic scanning cage.**

**Arrival B — The circumference becomes known (recognition).** A purposeful camera arc/pivot changes perspective to an oblique, near-axial composition. Valid registered wall positions progressively form an incomplete contour; a fuller irregular cross-section becomes legible only as evidence warrants. A restrained white nominal-bit-size reference may arrive when comparison adds meaning. Leave momentary reading space.

**Transition B→C — *The camera lets ECCO go* (the unique narrative action).** Camera tracking relaxes and reframes toward the wall/registered information while ECCO continues downward. The tool becomes supporting scale/context and may recede/leave frame. The acquired world-fixed points do **not** travel with the rotating tool. Camera travel must reveal expanding depth context rather than simply zoom backward on a blue cylinder.

**Arrival C — The shape left behind (main hero).** A clean, oblique three-dimensional view resolves on the reconstructed irregular borehole **through depth**. Use spatial silhouette, subtle registered sections, and selective physical-rock visibility/cutaway to help the audience read meaningful deviation **without exaggerating the wall or changing scale**. White nominal reference and blue enlargement can be shown together; a separate explicitly illustrative red tight example may be considered, subject to clearance and case labeling. Hold long enough to perceive geometry. It must not look like a loose graphic sleeve painted over a tool.

**Subsequent distinct information beat — Amplitude.** Use a camera-matched or deliberately differentiated view to introduce yellow/brown **synthetic received echo strength** as a second channel at the same measurement coordinates. Distinct reveal/cut rather than color metamorphosis. Geometry can influence uncorrected strength through stand-off/incidence, but strength colors do not create geometry.

**Camera constraints:** These are image/comprehension goals, **not actual transform coordinates, lens, easing values, or hard shot lengths**. T27 must inspect the real v009 local Blender master and T5/T6 geometry before proposing the camera path and numeric blocking. Camera moves must be motivated by new understanding; choose a cut or stillness if a fluid move reduces clarity. Guard against clipping, target snaps, occlusion and unnatural stationary drilling-tool claims.

## 3. Mechanical and information provenance

**Authoritative input:** [T8 v009 model](B202_acquisition_model_v009.md), [config](acquisition_config_v009.json), [data index](Data/v009/index_v009.json), [v009 T27 handover](../../Records/Tasks/T-008/T27_mechanism_handover_v009.md); accepted T5 v002, T6 v003, T7 Motion_v005. Native Blender master is local: `04-Production/Mechanisms/B202/Scenes/B202_measured-envelope_master_v009.blend`. This file is not in Git; verify access and exact hash on the execution machine.

**Acquisition truth within the synthetic model:**
- Three inherited sensor **proxies** in one plane at 120°; entire drill string/tool rotates and progresses axially. Sense/echo return belongs to the *same* sensor; do not invent cross-sensor reception or rotating internal head.
- Valid events originate in the v009 recorded sensor ray, intersection, round-trip time and synthetic echo model. Sensor spatial poses and subsequent acquired points are registered to the world/well axis; past points do not orbit along with the tool.
- Inverse reconstructs from recorded pose/direction, velocity and TOF; displayed radius/deviation comes from reconstructed event data, never directly from the hidden truth wall or an arbitrary UV texture. Preserve measured/missing/interpolated provenance, fixed display ranges, sensor IDs and event IDs.
- *Acquisition coverage causes visibility.* Do not reveal unmeasured regions, visually leak future bin averages, bridge large gaps, or animate legacy `scan_fraction` / `show_sections` / v008 sine-pattern materials as a replacement for v009 records.
- The v009 production fixture uses **13 discrete depth stations × 108 whole-tool orientations × 3 sensors**, synthetic `0.01s` event spacing and a 108-bin output grid. These are **demonstration sampling choices, not real ENP3 firing cadence, drilling penetration rate, sensor timing or certified resolution**. T27 must plan visually natural continuous poses/rotation and reconcile them with actual event times/positions; no fabricated measured events or incoherent arbitrary smoothing. Where original fixtures make continuous operation ambiguous, show an explicitly illustrative *replay/time-lapse* and/or regenerate coherent new synthetic events with the same verified model in a versioned consumer; do not relabel fixture timings as real instrument behavior.
- Radius: client white nominal, blue for enlarged radius (darker means larger deviation), red for an intentionally labeled tight example; thresholds, offsets and field accuracy remain uncalibrated. Amplitude: separate warm yellow/brown echo-strength field from the synthetic impedance/incidence/attenuation response; never imply direct lithology/oil identification.
- This is memory-while-drilling acquisition. Persistent world-space visualizations are a cinematic representation of recorded/reconstructed information, **not live downhole holograms or full log data streamed to surface**. Real sensor-face/datum, mud correction, eccentricity algorithm, impedance estimates and shot scheduling remain MIT engineering questions (B206/T12).
- Hypothetical tight case: its conservative centered tool clearance is limited, and the **nominal 12.25-inch gauge bit cannot pass**. Do not depict that gauge bit passing through; do not infer operational safety, tool loading or spiral cause.

## 4. Look, information graphics, and motion restraint

- Physical rock/hardware convey credible downhole depth and scale; sourced tool silhouette is preserved. The foreground sensing action is small; the **reconstructed geometry eventually owns the strongest visual hierarchy**.
- Start from cheap, clean Eevee/Workbench-style shading with necessary semantic colors, selective translucency and readable contrast. Physical rock receding or cutaway is presentation staging, not a rock-vanishing physical process.
- No permanent HUD, arbitrary particles, giant wavefront hero, invented numerical readouts or mandatory equation. When text is useful, choose short proposed labels such as **Wellbore Geometry** / **Formation Imaging**; quiet editorial or justified spatial integration, exact copy subject to review.
- Prior v008 still images are appearance/proportion references, **not** an approved frame sequence or mandated motion. Motion quality includes event order, meaningful persistence, continuity of depth references, tool-to-wall scale, motivated camera travel, dynamic rhythm and intentional holds.

## 5. First review gate — 5–8 second low-cost moving study

**Owner-approved concept, NOT preview approval.** Begin with a short, inexpensive *moving correctness + directorial* proof, ideally spanning:
1. Whole tool rotating/advancing with one recognizable active sensor → correct wall interaction/echo event.
2. Reconstructed world-fixed valid points accumulating into an **incomplete** then more readable circumferential contour.
3. Camera beginning the crucial release: tool moves onward while registered information stays in place, offering first glimpse of depth extension.

The proof need not fit all later geometry cases or the independent amplitude beat in 5–8 seconds. Use event records/coverage rather than full-surface cosmetic fades. Provide actual playable motion (not a still contact sheet) and inspected key frames. Run the v009 replay through real-time visual playback tests; stage the spec's outstanding **test10** here and report what is verified versus still failing. Show any fixture retiming compromises plainly. Obtain Radzi's targeted D2/D3 feedback before expanding to the full B202-M moving demonstration.

**Acceptance questions for initial proof:**
- Does the audience understand that a moving tool produces wall-fixed knowledge?
- Can we follow the same sensor and physically plausible measurement relationship without another T7-length lesson?
- Do samples appear only after valid acquisition, and remain fixed in the well as ECCO moves?
- Does a real *measured ring* emerge and does the camera release meaningfully reveal depth?
- Are the motion and transition pleasant/intentional in playback, not only in 2–3 stills?
- Are data claims/unknowns honestly marked and technical maps independent?

## 6. Full motion deliverable after targeted approval

Extend the proof into a watchable, near-final **mechanical animation** with:
- successive cross-sections building an irregular three-dimensional measured borehole through depth;
- white nominal comparison and correct blue enlargement, with hypothetical red tight case scoped separately and clearance-safe;
- distinct geometry-versus-amplitude meaning and a restrained transition introducing the warm field;
- editable versioned Blender motion consumer, timing/camera controls and test10/playback evidence;
- low-cost preview, exact version/frame references, verified source hashes and preserved v009 master, as T27 Review package.

**Not here:** whole S03 edit and definitive cut points (B3), photoreal premium finishing (C), MIT approval or invented accurate ENP3 calibration. **Review gates:** D1 concept approved; D2 real camera blocking/scene feasibility and early moving test pending; D3 moving animatic approval pending; final technical questions with T12. T27 must not self-accept; submit to Radzi review.

## 7. Sources and handoff

- [Active Scene Director skill](../../../03-Context/00_Skill/rolladice-scene-director/SKILL.md)
- [Directorial Identity and Scene Direction Contract](../../../03-Context/03_Directorial_Identity/07-SCENE_DIRECTION_CONTRACT_v0.2.md)
- [S02 V2](../../../03-Context/02_Storyboard/V2/ECCO_Section_02_Reveal_The_Principle_Padlet_v2/PADLET_SECTION_02_V2.md) and [S03 V2](../../../03-Context/02_Storyboard/V2/ECCO_Section_03_Open_Hole_SVG_v2/PADLET_SECTION_03_V2.md)
- [Engineering baseline](../../../03-Context/01_Foundation/02-ENGINEERING_BASELINE.md)
- [T8 v009 handover](../../Records/Tasks/T-008/T27_mechanism_handover_v009.md)

**Version note:** This contract records Radzi's explicit D1 approval of **The Shape Left Behind** in this conversation. It does not claim to have inspected an actual T27 animation, a final camera/lighting setup, or proprietary ENP3 operation. Use it with T27's live ticket, not instead of it.

## 8. First proof implementation — 17 October 2026, D2/D3 pending

Exact candidate: `Scenes/B202-M_motion-proof_v003.blend`; 192 frames / 24 fps / 8 seconds, 960×540. This appendix records inspected implementation, not new approval. The D1 premise above remains unchanged. Source/preservation and playback evidence: [T27 report](../../Records/Tasks/T-027/report.md).

| Frames | Camera / gaze / intention | Acquisition and movement |
|---|---|---|
| 1–36 | 48 mm; location (1.40, .60, .24), gaze (1.75, .08, 0), metres in source X-axis space. Recognize actual proxy sensor and a small sourced wall sector. | First event locator travels outward 1–12, contacts 12–15, returns to the same recorded sensor by 27; first points at 28. Deliberately slowed replay, not real-time acoustics. |
| 36–116 | Purposeful move to (.78, .40, .33), gaze (1.75, 0, 0) by 105; near-axial circumference recognition. | Whole-tool rotation through first station; adjacent acquired inverse events form contour edges. Physical wall sector fades 29–52 to open the illustrative cutaway. |
| 117–136 | Gaze begins releasing the sensor; camera continues to (.72, .60, .45), gaze (1.80, 0, 0) by 138. | Tool transfers .25 m between recorded stations; acquisition paused. Prior readings remain world-fixed. |
| 137–176 | Camera opens into oblique depth context. | Second station rotation; only completed v009 bins contribute to a surface. First and second sections establish .25 m of depth. |
| 177–192 | Arrive at (1.12, 1.45, .88), gaze (1.86, 0, 0); information becomes the anchor as tool advances. | Transfer toward third station; no third-station acquisition in this proof. Full volume/nominal/tight/spiral/amplitude beats await targeted review. |

Movement uses densely sampled linear keys and deliberate smooth camera/axial phrasing; gaze target and translation are separate. Full numeric frame score and event IDs are in `Records/Tasks/T-027/Evidence/replay_manifest_v003.json`. Original event values and positions are preserved; three sensor events per orientation share display receipt timing. The 1 μs cutoff bias addresses float32 rounding and is far below the original 10 ms event spacing. This is a **discrete station replay**, not continuous drilling or real ENP3 cadence. No events are fabricated between stations.

**Review priorities:** first interaction at tight actual clearance; whether the incomplete→complete ring reads; whether the camera release establishes that the information stays while ECCO moves; whether the two-station surface reads as the beginning of depth reconstruction. Final geometric revelation and separate amplitude remain later work. Review with Radzi/T26 against this exact playable candidate; no D2/D3 approval inferred from self-checks.
