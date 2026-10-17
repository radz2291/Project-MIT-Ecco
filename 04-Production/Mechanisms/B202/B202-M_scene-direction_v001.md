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

## 9. Director feedback → bounded v004 revision, 17 October 2026

T27 discussion `b94637dc-0785-4585-92f4-967b433bdda2` rejects v003's visual explanation while preserving its synthetic mechanism. The floating patch, attached-looking ring and short sleeve did not communicate D1. D2/D3 remains unapproved; keep T27 in progress. Return one cheap revised proof, then targeted review before full expansion.

**Approach:** start within the actual sensor/wall gap, pull out through a continuous solid-rock cutaway, recognize the persistent circumference, then stop following ECCO and hold on the reconstructed well. Use all **13 existing v009 stations / 4,212 events / three metres**, retimed without regenerating events, stretching geometry or filling gaps. Fourteen seconds provides opening recognition, compressed depth replay and a final release/hold. This remains the bounded proof; amplitude/spiral/tight development waits.

Exact review candidate: `Scenes/B202-M_motion-proof_v004e.blend`, frames 1–336 / 24 fps / 960×540. Local preliminary v004/a–d composition/debug candidates are preserved. Numeric per-frame camera and event score: `Records/Tasks/T-027/Evidence/replay_manifest_v004e.json`.

| Frames | Camera and understanding | Acquisition |
|---|---|---|
| 1–34 | Inside-annulus macro (1.72, .145, .027), gaze (1.75, .145, .003), 28 mm. Source wall and tool face occupy opposite sides of the actual gap; .2 mm near clipping is a camera setting, not geometry alteration. | Slowed sensor0 event, wall contact 14–18, same-sensor return 32; first points 34. |
| 35–96 | Pull out to (.75, .46, .34), gaze (1.90, 0, 0) by 90; lens eases to 42 mm. Establish enclosing solid-rock context and circumference. | First station whole-tool rotation; inverse points/adjacent acquired contour. |
| 97–176 | Initially follow moving sensor plane; by 144 camera (1.05, .85, .62), gaze (2.4, 0, 0). | Subsequent stations: four transfer frames without acquisition, eleven retimed rotation/acquisition frames. Explicit time-lapse, no real cadence claim. |
| 177–276 | Camera releases to (.5, 2.0, 1.15), gaze (3.05, 0, 0) by 230. Rock presentation fades 170–276; white nominal references arrive 240. | Only acquired v009 data. Surface bins wait for all contributing records. |
| 277–336 | Hold the three-metre result while ECCO moves onward; settle to (.4, 1.9, 1.08), same gaze. | No additional events. Prior points remain fixed; glyphs become smaller as surface takes priority. No geometry scaling or amplitude conversion. |

**Presentation and limits:** unchanged T6 inner-wall vertices plus authored .68 m square outer rock mass and sealed cut faces; exterior dimension is visual context, not sourced geology. Sector .07–1.4 rad opens toward camera. Physical wall coordinates never feed measured geometry. Fixed radius/amplitude scales and source masks remain. A 10 μs evidence-cutoff bias accommodates float32 above 32 seconds, far below original 10 ms spacing.

**Re-review:** judge the moving enclosing context, actual-scale interaction, persistence when ECCO advances and final measured borehole. The underlying irregularity is subtle and remains unexaggerated. Scene/data checks do not establish visual comprehension. No exact camera/preview, acoustic-face datum or full explanation is accepted by this revision.

## 10. Audience insight refinement — bounded v005b, 17 October 2026

Discussion `acd516d6-c107-4274-9a3e-6fa9a2022099` recognizes v004e's mechanical/camera improvement but withholds D2/D3 approval. Audience includes non-engineering stakeholders/investors. New emphasis, within D1: **the expected perfect hole differs from the actual measured hole; that difference continues through depth.** Preserve acquisition/release and test this insight before expansion. No premium finishing or amplitude sequence is requested here.

**One comparison, same coordinates/scale:** choose the existing `irregular_layers` v009 section at X=2.75 m, whose valid cached grid has approximately 2.6–25.2 mm of enlargement around the nominal radius. Do not alter those radii. An aligned white nominal circle, blue measured contour and filled blue enlargement band make the difference explicit. Band interiors connect the two source/reference boundaries; they are explanatory comparison, not additional acquired samples. Quiet labels **Expected hole / Measured hole** distinguish the reference and synthetic derived result.

Exact version `Scenes/B202-M_motion-proof_v005b.blend`, 336 frames / 24 fps / 14 seconds. Raw event values/IDs/poses, all 13 stations and masks remain unchanged; only illustrative display timing/composition/material presentation changes. The X2.75 section has all contributors by frame96; focus enters105 and is held front-on132–204, avoiding future data. Other stations finish off-frame by168. Context data objects are hidden105–204 for the dedicated comparison, then displayed as already-acquired volume from205. This is an explicit presentation-view switch, not a claim that fresh measurements materialize at205.

| Frames | Camera/event score | Audience job |
|---|---|---|
| 1–18 | Actual gap macro retained; wall contact7–9 and same-sensor return17, first points18. | Briefly establish a physical measurement. |
| 19–60 | Pull out to (.75,.46,.34), gaze(1.90,0,0), 42mm; source first-station whole-tool rotation. | Relate the instrument to the enclosing wall and persistent readings. |
| 61–104 | Compressed remaining stations, each two transfer frames without events then seven rotation/acquisition frames. Camera through(1.5,.65,.5), gaze(2.6,0,0) at98; rock presentation fades70–104. | Transfer attention from sensing to the acquired section. |
| 105–132 | Align camera to(2.05,0,0), gaze(2.75,0,0), 35mm. Isolate the actual X2.75 measured section and nominal reference, with no scaling. | Let the irregular contour differ visibly from the expected circle. |
| 132–204 | Hold three seconds. Two quiet sans-serif labels; complete outline inside frame. | Give non-engineers time to recognize expected versus actual. |
| 205–270 | Known full data volume resumes; camera releases to(.5,2,1.15), gaze(3.05,0,0), lens42mm. Focus section stays world-fixed as part of the volume. | Show that the changing deviation continues through depth. |
| 271–336 | Approach the measured shape to(1.3,1.2,.65), gaze(3.1,0,0); tool continues away beyond the retained data. | Geometry owns the frame; source-profile variation stays at real scale. |

Fixed original geometry ramp/normalization retained. The data shader bypasses physical lighting that washed the blue scale toward white; it is presentation of the same radius field, not a new palette/quantity, amplitude or optical rock color. Geometry opacity .95 improves the solid shape's hierarchy. End framing may crop the interval's ends to prioritize its most variable region; the full measured source still spans three metres. All expected/reference contours remain distinct from acquired measurements. Segoe UI is a local system-font dependency, not an approved brand-font selection.

**Review sought:** sound-off recognition of the white expected circle versus blue measured contour, followed by understanding that this deviation builds the borehole shape. Entry, acquisition and release remain supporting evidence. The earlier v004e and initial v005 study are preserved. D2/D3 remains open; no full-sequence/engineering acceptance is inferred.

### Mixed-audience proof record (17 October amendment applied)

```yaml
audience:
  groups: [engineers, non_engineering_stakeholders, investors]
  prior_knowledge: mixed_no_prior_drilling_knowledge_assumed
  nontechnical_takeaway: "The actual hole can differ from the expected circle; ECCO provides information about that difference while drilling."
  why_it_matters: "It reveals actual hole geometry instead of relying only on nominal bit size; no savings, safety or ROI claim is made."
  expert_truth_check: "White is an expected nominal reference; blue is synthetic v009 measurement-derived radius, in matching coordinates and scale, with source coverage and provenance preserved."
  discovery_or_comparison: "White expected circle versus existing X2.75m actual contour, then the same deviation through depth."
  planned_context: "Sound off; two labels Expected hole / Measured hole; accompanying review identifies synthetic data. No explanatory narration required by this candidate."
  cold_viewer_question: "What did ECCO discover, and why would knowing that be useful?"
  cold_viewer_method: "Show the actual v005b playable preview to an uninstructed non-specialist before explaining its intended message; record their answer verbatim."
  cold_viewer_result: pending_not_yet_tested_with_an_uninstructed_viewer
  domain_review: pending_MIT_specific_processing_and_interpretation
  director_review: pending_Radzi_D2_D3
```

The implementation and agent's reading are not a cold-viewer result. Radzi/T26's targeted preview review remains necessary; any actual non-specialist response must be recorded against this exact version. No outside viewer was contacted. The new audience guidance at commit `9e0942c` was synchronized during closure and read before submitting this revision.

## 11. Authorized full mechanical extension — v006d, 17 October 2026

Radzi accepted v005b as “good enough” in the execution chat and then explicitly instructed continuation. This clears the bounded geometry/camera direction gate; it does not accept the full sequence or certify engineering. Preserve the first336 frames exactly as saved. Construct a separate consumer; leave the dirty open v004e session untouched.

Implemented full score: 720frames /24fps /30seconds. Frames337–432 show `spiral_layers` as an explicitly labelled illustrative recorded geometry example, using an oblique camera glide to reveal changing profile direction through depth. Frames433–528 show `tight_layers` with a front-on nominal-versus-measured section at X2.75m; full section433–456, approach457–480 and close view481–528 of the minimum-radius region; red comes from the existing fixed radius map. No tool or bit is visible in either example, and no passage or causal diagnosis is implied. These are cuts between different completed source cases, never a morph or fresh acquisition. Frames529–552 return to the original irregular geometry; frames553–720 cut to the distinct echo-strength quantity on exactly those same positions, with yellow/brown fixed normalization and a gentle lateral camera move. Geometry precedes amplitude; no unwrapping or field-log imagery.

New labels identify “Illustrative spiral geometry”, “Illustrative tight section”, “White: expected / Red: tight section”, and “Echo strength / Reflected signal, not rock colour”. A small “Synthetic example” qualifier accompanies new data views. Text is editable, quiet camera-relative sans-serif. New camera poses are stored per frame in `Records/Tasks/T-027/Evidence/replay_manifest_v006d.json`. Spiral camera glides from(0,2.5,1.5) to(.35,2.5,1.0), gaze(3.25,0,0),42mm. Tight camera moves from(2.05,0,0) toward(2.66,yn,zn), gaze(2.75,yn,zn),35mm, where yn/zn are the nominal point at the measured minimum-radius azimuth. This is camera magnification, never geometry scaling. Final original-geometry/echo view glides from(.2,2.3,1.3) to(.5,2.4,.85), gaze(3.25,0,0),42mm. Saved-scene checks pass; exact full playable remains for human review. No numeric radius exaggeration, object scaling or new simulated events.

Audience intent remains the section10 takeaway. The warm segment adds only: the returned signal also has a separately mapped strength; its colours do not identify rock type. Human cold-viewer test: show the exact full playable without pre-explanation, sound off, ask what was discovered and what the warm colours mean; record verbatim response. This remains pending until a real response exists. Expert review separately checks source channel, masks, fixed ranges, sensor datum and uncalibrated synthetic parameters. Agent checks cannot substitute for either acceptance lens.

Version history: v006 exposed label clipping and interval crop; v006b corrected both. v006c adds the honest closer tight-section view. Earlier local native studies are preserved. Final saved-consumer validation passes7,317 checks; no new visual approval beyond the accepted v005b opening is inferred.

v006d keeps a single Synthetic example qualifier visible throughout337–720, including the separate echo-strength view.

## 12. Bounded communication correction — v007b /17 October2026

Live discussion e8d322 returns v006d for amplitude, localized restriction and spiral clarity; addendum4d59c63f sets S03 relevance/order and18second planning constraint. Preserve first336accepted frames and all original data. v006d is a mechanism library, not a30second S03 shot. Scene Director/Module09 audience-first reasoning applies; neither agent checks nor this revision is human/client acceptance.

Diagnosis: original irregular-layer echo strength spans0.034473–0.168341 (1404valid bins), with depth means0.07756–0.16687 and circumferential/weak-patch variation. Values occupy normalized0.08618–0.42085 of the fixed0–0.4 scale. The prior low-range brown ramp and one oblique flank concealed response differences; data is not near-uniform and no new synthetic case is needed. Geometry shader attributes/independent echo links resolve; no shader-type defect is asserted. Numeric histograms/percentiles are saved in Evidence/source_diagnosis_v007.json. New declared fixed colour transfer0/darkbrown,.25/brown,.5/gold,1/paleyellow preserves0–0.4 normalization for every frame. Camera views the complete circumference; no auto-normalization, painted streaks or rock-type claim.

Implementation score:337–432 shows two clearly captioned separate cases together: unchanged enlarged profile and true-scale tight profile, each registered to its own identical white nominal circle. Display-stage translation separates cases, never scales radius. Entire tight circle stays visible. Source-coordinate detail camera produces a labelled5x inset of its minimum-radius location, with a small source-anchored locator.433–528 shows all13 unchanged spiral source sections plus a guide joining their measured maximum-radius cells (guide interpolation is not extra measurement). Suppress the distracting translucent surface; data positions remain unchanged.529–600 provides a brief Same returned echo / Travel time: hole shape / Echo strength: acoustic response bridge, returning explicitly to exampleA.601–720 shows that same original irregular case’s independent amplitude field, with a360degree camera circuit around stationary data. Different-case captions prevent live-morph interpretation. No waveform tutorial or S06 unwrapping.

S03 feasibility selection for T15,18seconds total:0–3s establish white nominal reference using the inherited ring and v005b comparison control (measured overlay initially hidden);3–7s use337–432 paired enlargement/tight recognition;7–11s use433–528 source-contour/crest depth reveal;11–14s use529–600 two-properties bridge;14–18s select/retime601–720 warm response view to4seconds. These are edit recommendations, not a new shot contract, locked coordinates or approved cut. The library keeps its accepted14second opening for provenance, while B3/T15 selects the short diagnostic material rather than replaying the acquisition tutorial. S04 exit can leave along the well axis at the end of the warm view; S06 owns later unwrapping.90second full-film budget is retained.

Cold-viewer test pending actual response: show the selected beats sound-off without explanation; ask the viewer to point to the tight location, trace the spiral through depth, describe what varies in the warm view, and say whether these were one changing hole or separate examples. Record verbatim response and time context. Expert review independently checks quantities, stage/inset transforms, fixed scale, data provenance and remaining MIT acoustic/datum/calibration assumptions. No outside viewer contacted or acceptance invented.
