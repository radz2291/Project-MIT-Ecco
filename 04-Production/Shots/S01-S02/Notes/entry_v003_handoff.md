# Enclosed entry proof v003

2 November2026, ECCO-057. Owner explicitly authorized the closed start, enclosed bore and delayed cutaway plan. Working base16460abcbb12b82c01f17244ba67c584920b846b. No changes to other sections, film assembly or client delivery.

Current native: Scenes/S01-S02_production_v003.blend, saved/open at106. Dirty pre-change session preserved as Scenes/S01-S02_session_before_v003.blend; v002 and original previs retained. Exact native SHA256: entry_v003_manifest.json.

## Implemented

- World v014 adds complementary front-sector geometry and reusable presentation groups. All v013 source meshes preserved; v013 file hash unchanged. Source boundary radii reused; absent-front profile interpolated, not measured geology. Full seabed cap prevents the early V-shaped earth opening.
- Sequence-local objects share linked v014 meshes and groups. Local ENTRY presentation controls reproduce the retained previs curves: bore scale4.178 initially, returning to1 at141; front starts retracting115 and is absent by123. Expanded inner-wall smooth shading improves close-view readability. No change to camera action; sampled camera matrices match actual source exactly.
- Surface v007 supplies an illustrative0.66m central viewing passage through19 stack/foundation/coupling objects. Riser and outside equipment retained. The camera-access Boolean is applied before the existing modifiers, avoiding baking bevel/access effects twice. The first unpublished attempt warned about modifier order; it was rebuilt from preserved v006 with that ordering corrected. No exact equipment-internal geometry claim.
- BHA v008, six waveform bindings and shared measurement reveal fromv002 retained. The entry modifiers become nominal before arrival: the later evaluated S02 physical wall matches the original evaluated linked source exactly (including its pre-existing Outer_soil_margin_25m shape key).

## Verification and visual review

Scene saved/reopened after linking successors; all library paths resolve. See entry_v003_verification.json. Camera source samples maximum matrix error0. At106,72 horizontal rays around the camera all hit rock, with minimum wall distance0.289m versus near clip0.04m. At80,144 downward probes across four radii/all directions hit the seabed cap; maximum top-plane error4.3 micrometres. Front geometry absent by123; nominal scale1 from141 onward. World v013 and Surface v006 hashes unchanged. These checks establish authored visual coverage/continuity, not engineering simulation or certification.

The initial comparison against raw wall Basis reported a5m outer-margin difference; diagnosis identified the existing25m margin shape key. Comparing evaluated source against evaluated candidate yields0 error. No wall correction or hidden source change was used to remove that diagnostic failure.

Motion proof: Previews/Entry-v003/S01-S02_entry_reveal_v003.mp4, native frames80–152,73 frames at24fps (3.0417s), no retiming. Workbench480×270, AA off, shadows/cavity off. Full environment present; no preview culling. Every full render-to-file frame0.898–1.263s. After the Surface modifier-order repair, affected approach frames80–97 were rerendered (0.898–1.173s) and the clip re-encoded; later frames are below all modified equipment and look downward, so they retain the already rendered World proof. Final approach timings: entry_v003_approach_final_timings.json. Entire encoded clip decodes without errors; sampled decoded montage and native frames80/94/95/96/97/106/120/132/152 visually inspected. Montage: Previews/Entry-v003/entry_encoded_review_v003.png.

Not claimed: final lighting, underwater optics, final materials, engineering approval, independent verification, or full-sequence render budget. Focused entry behavior is ready for Radzi's visual feedback. No final task wrap/Review submission; only Radzi accepts. Native/video files local only, no new off-machine backup. Permitted scripts/interfaces/notes and selected stills synchronized separately.

Next: Radzi reviews the entry enclosure, subsea approach and opening timing. Continue small visible revisions fromv003; later full-sequence proof remains open.
