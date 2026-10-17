# T41 — S02 cinematic 3D previs pilot

**Review candidate: experimental v003.** Prepared 17 October 2026 for Radzi. Isolated project **MIT ECCO - PREVIS**, ticket `e5545efd-9052-4fc4-8d55-65d6612d243f`. No main-project B2/B3 work resumed, and no production storyboard, creative acceptance or MIT technical approval is claimed.

## Result and review decision

Delivered one editable, reproducible 12-second Blender blocking experiment: first contact (3s), returning-time explanation (4s), then progressive circumference (5s). The camera moves continuously through those three beats. Six readable principle events lead into 111 sparse synthetic scan events across three 120-degree sectors; the final outline remains fixed to the existing wall geometry. This tests method and causal order, not final appearance or a calibrated acquisition model.

**Radzi's review:** Watch the silent clip before reading a technical explanation. Does returning sound → wall distance → surrounding shape read? Are the close views and final x-ray outline a useful basis for the next iteration? The executor's critique is that the true narrow annular gap makes signal travel small on screen, the retained rock cutaway remains visually sparse, and a foreground timing graphic is clearer than a fully spatial waveform at this cost. Human comprehension and MIT engineering reviews remain pending; passing implementation checks does not resolve them.

## Authority and investigation

Radzi explicitly requested thorough investigation followed by execution. Fresh live handoff had no dependencies or pinned standards; run claimed with stable worker `codex-t41-previs-20261017`, run `b0903d17-273f-4794-91ca-42839839da2d`. All six persisted criteria end mid-sentence in the live tool response, including the handoff. Their exact missing text was not invented. The full outcome, available criteria and linked sources bounded execution.

Read the context map, production lifecycle/closure, active AI Director and Scene Director, Scene Direction Contract and relevant personality/evidence/casebook/camera/look/typography/information modules. Checked Engineering Baseline, Decision Register, MIT identity, V2 S02 and local V3 cinematic package, including its explicit generated-image hardware errors. The existing one-plane references correct those errors; no axial emitter or separate receiver was copied. Open O03/O04/O05/O06/O14 remain traceable.

Initial checkout: `main` at `310cf98a2d0dce2dc87cd76eac524497fd388667`. Four unrelated tracked modifications and extensive untracked mechanism work were present. Official Blender MCP read-only queries confirmed Blender 5.2.2 and the existing B202 scene; it was left untouched. The owner subsequently confirmed saving it. The official CLI tool failed because `BLENDER_PATH` was unset; the installed Blender 5.2 executable successfully performed isolated background inspection/build/render/verification instead. No bridge/config changes were made.

Fetched remote main at `efff6447eb34d9a79c5173d8f87fb99409e9d4b5`. Newer T31 direction proposes 4/5/3s for main S02; this isolated ticket/V3 experiment uses 3/4/5s. Main shot contracts and T14/T33/T40 gates were not changed. Task-only Git integration uses a managed checkout based on that fetched commit, preserving the user's working checkout.

## Exact artifacts

All paths are relative to `04-Production/`; local root is `C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco`.

- [Playable local review](../../../Shots/S02/PREVIS-T041/Previews/v003/review_v003.html), [MP4](../../../Shots/S02/PREVIS-T041/Previews/v003/S02_previs_T041_v003.mp4), [review sheet](../../../Shots/S02/PREVIS-T041/Previews/v003/S02_review-sheet_v003.jpg).
- [Editable scene](../../../Shots/S02/PREVIS-T041/Scenes/S02_previs_T041_v003.blend), [builder](../../../Shots/S02/PREVIS-T041/Scripts/build_previs_v003.py), [render](../../../Shots/S02/PREVIS-T041/Scripts/render_previs_v003.py), [verification](../../../Shots/S02/PREVIS-T041/Scripts/verify_previs_v003.py), [package](../../../Shots/S02/PREVIS-T041/Scripts/package_previs_v003.py).
- [Direction and per-shot contracts](../../../Shots/S02/PREVIS-T041/direction.md), [asset register](asset-register_v003.md).
- [Build/event/camera evidence](Evidence/build_v003.json), [saved-scene checks](Evidence/verification_v003.json), [encoded-video checks](Evidence/video-qa_v003.json), [artifact hashes](Evidence/artifacts_v003.json).
- Review stills in `Shots/S02/PREVIS-T041/Previews/v003/`: exact entry f001, contact f022, reception f032, waveform f103, ring f266, exit f288; four chronological sheets sample decoded movement every six frames.

Native candidate SHA-256: `69cd1d24417fa22b608e9c8ba60f498cd4d3701b2522636bd120250f2e4bee47`. Other hashes and render times are in the linked evidence. v001 and v002 native files/renders remain locally preserved for diagnosis. v001 removed contact rock; v002 retained too large a patch and foreground hardware obscured the ring. v003 narrows the exact-source patch and explicitly labels the final ring's x-ray data visibility.

## Verification and practical limits

The candidate was reopened in a separate Blender process. Fifteen executor checks passed: frame range/rate/aspect; resolving relative library links; unchanged T5/T6 source hashes; one sensor plane and 120-degree spacing; ordered transmit/contact/reception; same-sensor endpoint positions; records only after reception; world-fixed records; 120-degree three-sector scan; continuous camera; final recognition hold; full outline projected inside frame; editable camera/gaze; no custom frame handlers. Maximum endpoint/static-position error was zero at tested endpoints; maximum per-frame camera step was 0.00770m. Camera positions are authored CGI, not physical camera-placement evidence.

Rendered saved scene to 288 Workbench frames, 640×360, 24fps, then encoded H.264 MP4 and decoded every delivered frame. Review evidence is sampled from that encoded clip. This is executor QA, not an independent viewer test. Causality is verified numerically; visual comprehension and cinematic quality are review questions.

T5 remains the 2.400m source mesh, not silently rescaled to nominal 2.25m. Recess references and ray-sampled outer presentation surfaces are not verified transducer faces. The dedicated mud sensor remains unlocated; the clip states correction/pose are required without inventing a sensor, velocity or physical number. Echo travel, waveform amplitudes and time, rotation rate, sampled dots and T6 wall shape are synthetic illustrations. No field data, accurate RPM, real waveform, calibrated distance, actual deployment or optical scanning is asserted. Source X is longitudinal; treating +X as downhole is an experimental convention because shoulder/end identity is unresolved. No certified clockwise-direction claim is made. The body and attached assembly rotate together; no drilling advance is claimed in this cross-section principle study.

The waveform is an editable camera-facing reading layer with a spatial sensor leader. Whole-body rotation continues; the final sample arcs are world-fixed and shown through foreground hardware using an explicitly labeled x-ray convention. Rock/mud visibility is a CGI cutaway, not an empty physical annulus. These are proposed explanatory choices requiring review.

## Reproduction, synchronization and next action

Run the builder in isolated Blender 5.2.2 with the organized T5/T6 native sources present; it refuses overwriting an existing candidate. Then run `render_previs_v003.py -- all`, `verify_previs_v003.py`, and the packaging script with the bundled Python/Pillow/numpy and `FFMPEG_EXE` if the existing local media-tool cache is unavailable. No installation, new MCP connection, source-master change, finishing pass or heavy render is required.

Scoped reports, contracts, scripts, JSON evidence and selected permitted review images are synchronized for online review. The exact containing commit and commit-pinned report are attached to Rolladice after push verification. Blender binaries, MP4 and raw frame folders remain organized locally and excluded from Git; local saving is not remote backup. The online HTML cannot play the excluded local video. No restricted ENP1 field-log, generated direction image or private commercial record is republished.

Next action is Radzi's review of **this exact v003 clip/scene**, followed by a bounded decision about camera/readability, x-ray convention and whether this method warrants further development. Do not self-accept, launch another ticket, resume B2 or replace main storyboard gates from this experiment.
