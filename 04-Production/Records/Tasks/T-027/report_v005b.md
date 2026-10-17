# T27 / B202-M — expected versus measured, bounded v005b proof

**17 October 2026 · D2/D3 visual approval pending · T27 In Progress.** Response to discussion `acd516d6-c107-4274-9a3e-6fa9a2022099`: preserve v004e's mechanism/release, but make the non-engineer takeaway explicit before showing depth. **The expected perfect hole differs from the measured actual hole, and the difference continues through depth.** No full expansion or finishing requested/performed.

Task `486a2a68-c921-4f2d-9323-5115a6f9340a`; worker `codex-b202m-20261016`; run `c15761c0-2097-46f8-b795-0aba7f938924`; execution base `5c4c83f01d7363d60820f7480e31b544acd9ab26`. Latest discussion/fresh handoff read before new run; T8 Done, pinned standard v2 current. Fresh remote synchronization during closure brought the audience amendments through `9e0942c`; amended Scene Director, contract, Module09 and MIT identity were read and the required audience/test fields added to the existing contract. Preserve [v004e report](report_v004e.md), [v003 report](report_v003.md), native proofs and all accepted sources. Unrelated B201 working changes are excluded from this task's commit.

## Review exact v005b

- [14-second playable proof](../../../Mechanisms/B202/Previews/MotionProof_v005b/B202-M_motion-proof_v005b.mp4), 336 frames / 24fps / 960×540.
- [Entry / acquisition / comparison / release / hero sheet](../../../Mechanisms/B202/Previews/MotionProof_v005b/B202-M_review-sheet_v005b.jpg).
- [Recognizable expected-versus-measured frame168](../../../Mechanisms/B202/Previews/MotionProof_v005b/decoded_0168.jpg).
- [Local review player](../../../Mechanisms/B202/Previews/MotionProof_v005b/review_v005b.html).
- [Editable Blender consumer](../../../Mechanisms/B202/Scenes/B202-M_motion-proof_v005b.blend).
- [Single direction contract §10: audience purpose, camera/event score and view switch](../../../Mechanisms/B202/B202-M_scene-direction_v001.md).
- [Exact event/focus provenance](Evidence/replay_manifest_v005b.json), [fresh-open scene/comparison checks](Evidence/verification_motion-proof_v005b.json), [all-frame video QA/output hashes](Evidence/playback_qa_v005b.json).

Root `C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco`. All production outputs are organized under `04-Production`; Blender/video/bulk frames remain local ignored media, not backed up/uploaded by Git. Reports/scripts/evidence and selected permitted stills are committed/pushed and remote verified; exact candidate commit/report links go to Rolladice. No restricted field-log media.

## What stayed unchanged

Same accepted T5 v002/T6 v003, v009 measurement-only inverse, `irregular_layers` data case, 13 depth stations/4,212 original events, three whole-tool sensors/same-sensor reception, masks, fixed radius/amplitude normalization, wall-fixed points and camera-release premise. No new events, stretched geometry, exaggerated radii, pseudo-log or acoustic calibration claim. Recorded source fixture is a compressed synthetic time-lapse, not actual ENP3 firing/drilling timing. Independent amplitude remains retained but hidden and outside this geometry gate. T7 untouched; v004e native hash preserved.

## What was visually redesigned

1. Abbreviate the opening/acquisition. All stations complete by frame168; transfers still contain no acquisition. This supports the result rather than spending equal time on every sensor event.
2. Select the **existing X=2.75m measured section**, with approximately 2.6–25.2mm enlargement around the nominal radius, as the decisive recognition beat. This was selected from inspected data, not generated or enlarged for appearance.
3. Align a white nominal circle and blue measured contour in the **same coordinates at 1:1 geometry scale**. Fill only the real enlargement between them with a dark-blue comparison band. Hold front-on frames132–204 (three seconds), with quiet **Expected hole / Measured hole** labels. Nominal is a reference, not measurement. The blue section is derived synthetic data, not field output.
4. Temporarily isolate this section: other context data displays are hidden105–204, while their values and world positions remain intact. The focus section's contributors already exist by96. Acquisition continues in the fixture outside this comparison view until168. At205, resume the already-acquired three-metre volume and release the camera through depth. This is an explicit explanatory view switch, not new data appearing without evidence.
5. Keep the comparison section fixed within the volume. Use closer final framing of the actual variable region, allowing interval endpoints outside frame. Bypass physical-light washing of the **unchanged original fixed-range blue ramp**, using a lighting-independent map and .95 opacity so radius variation retains tonal hierarchy. This changes presentation, not quantity, source values or geometry. No premium finishing.

The earlier partial-frame comparison study v005 is kept locally; v005b corrects framing and data-map contrast. Source variation remains unexaggerated. The final hero's comprehension is a viewer judgment; this report does not self-approve it.

## Validation and limitations

**2,056 fresh-open checks pass**, including original indexed raw-event hash, complete event IDs, per-frame exact receipt/masks/no-future averages, fixed inverse points, coverage-only contours, unchanged source rock vertices/closed cutaway, source preservation, acquisition paused in transfers, same-sensor return and three-metre source extent. Additional comparison checks verify all108 measured cells against the original grid, every nominal point's true radius, every band endpoint joining actual/reference, source contributors available before focus display, full outline inside the held frame, 1:1 object scales and resolving font dependency. These are agent synthetic checks, not MIT acoustic certification or visual acceptance.

**All336 encoded frames decode**, at 24fps /14.0seconds /960×540, with exact output hashes. Key comparison/hero frames and the six-frame sequence were visually inspected; sound-off comprehension remains a human D2/D3 judgment. The quiet labels use system Segoe UI, a local font dependency rather than locked MIT brand typography. Technical face/datum, mud/eccentricity correction, cadence and interpretation remain MIT review questions. White nominal is deliberately separate from derived synthetic measurements; blue is radius deviation, never echo amplitude or optical rock color.

Official Blender inspection reported unsaved changes in the open v004e session. That session was left intact; v005b was constructed, checked and rendered independently in background Blender 5.2.2. No unsaved user scene was replaced or saved. Bundled Python/Pillow/numpy plus the established task-cache imageio_ffmpeg0.6.0 encode/decode the preview.

## Requested next review

**With sound off, can a non-engineer immediately see expected circle versus actual contour, then understand that the deviation continues through depth as ECCO moves on?** Review the playable v005b, comparison168 and final hero336. The discussion requires Radzi's visual approval before full expansion/closure; T27 remains in progress, run waiting after synchronized delivery. No Done or film/client acceptance is claimed.

Under the newly synchronized audience amendment, a separate **cold-viewer result remains pending**: show this actual preview to an uninstructed non-specialist before explaining the message and ask **“What did ECCO discover, and why would knowing that be useful?”** Record their answer verbatim against v005b. The agent's comprehension and numerical checks are not that audience result. No outside viewer was contacted. Expert provenance/technical review is a distinct pending acceptance lens. Grounded significance is knowledge of actual hole geometry versus only nominal size; no operational savings, safety or financial benefit is invented.

Implementation: [build v005b](../../../Mechanisms/B202/Scripts/build_motion_proof_v005b.py), [verify v005b](../../../Mechanisms/B202/Scripts/verify_motion_proof_v005b.py), [encode/decode/package](../../../Mechanisms/B202/Scripts/package_motion_proof_v005b.py). Build refuses native overwrite; version further changes. Full amplitude/case sequence and final moving acceptance remain later work after this audience-insight gate.
