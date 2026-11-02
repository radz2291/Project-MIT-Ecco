# S01–S02 collaborative production

Final editable handoff: **`Scenes/S01-S02_production_v027_clean.blend`**. Owner-requested cleanup removed558unused legacy objects; native19.1→3.3MB. Thirty sampled camera/BHA/wall/signal checks and five visual comparisons preserve the v026 presentation. [Closure, controls and deferred work](Notes/closure_v027.md) · [Deliverable hashes](Notes/closure_manifest_v027.json). DOF remains investigation-only; it is not applied to production. Execution prepared for human Review on3November2026.

Visual source preserved: `Scenes/S01-S02_production_v026.blend`. Owner-marked first bottom contour omitted; later contours and all timing retained. See `Notes/no_first_contour_v026.json` and `Previews/No-first-contour-v026/first_panel.png`. Measurement follows the actual bore interior with clearance for2mm contours. Rings build over4frames,2frames behind the blue reveal, then persist. On/off, delay and build duration controls are native object properties. Earlier [refinement handoff](Notes/refinements_v025_handoff.md).

Full v026 scene render: `Previews/Full-v026/S01-S02_full_v026.mp4` —31.5seconds,1080p24FPS. [Render and review handoff](Notes/full_v026_handoff.md). Active7m47s, elapsed11m32s including crash recovery, avg0.618s/frame.

Grid controls: N → World Grid; run START HERE pixel-guides text after reopening. Entries below describe historical implementation stages.

ECCO-057: 2cd3cc2d-92b1-456c-92c6-556fb4526f4f. Owner requested wrap and cleanup; final execution handoff prepared for Review. Historical collaboration checkpoints below are superseded by the closure record.

Baseline: `05-Previs/Section-02_Measurement-History/v011/Continuation/Scenes/S01-S02_continuous_v011.blend`, frames 1–528 at 24 fps (22 seconds); handoff frame 240. Source preserved. Camera matrices/lenses match eight sampled frames; original event animation retained.

Linked: Surface v006, World v013 using canonical_to_s02 placement, ECCO v003, waveform v015, measurement-reveal v001 node groups. Relative libraries resolve on reopen. Source environment proxies retained in a disabled collection. Existing local measurement/history geometry and source string remain.

Implemented v002: BHA v008 WORLD_HARDWARE replaces standalone ECCO, with internal ECCO v003 and original movement. Sequence string connects to inspected collar endpoint X=-1.5m, continuing to source Z=30m. Original standalone instance/string retained disabled; optional shared 12m continuation is not stacked onto the sequence string. Six waveform v015 objects use individual source send/contact/echo/receipt windows and sensor/wall routes. Old travelling graphics retained disabled; contact cues stay local. Shared measurement reveal reads shot-local receipt frames318/360/402/450/498/524, history starts and reveal order. Shared fine styling follows the revealed wall; source topology/material animation retained. No shared masters changed. Signals and geology remain illustrative, not measured or certified physics.

Preserved unsaved session: `Scenes/S01-S02_session_before_v002.blend`. Base commit0cfd75e3a8745d1ff3790fe7dcae2abe72bed336. All528 camera matrix/lens and assembly transforms match the preserved session. Reopen has no missing library paths; both reveal groups survive. Six waveform events pass before/during/after geometry checks. Sampled BHA radial-fit checks found no outside samples on covered directions at240/300/432/528; cutaway rays without wall hits are explicitly uncovered, not certified. Near-contact at432 remains a review point. See Notes/integration_v002.json, verification_v002.json and native_manifest_v002.json (exact native SHA256).

New previews: `Previews/measurement_cycle1_v002.mp4` (299–326 at24fps) and `Previews/stored_history_v002.mp4` (440–464 at24fps), no retiming; both decode successfully. Workbench480×270 AA off, shadows/cavity off. Underground preview only culls distant rig/ocean/regional geology; exact linked local physical wall retained. Full scene restored before saving production native. Cycle frames1.34–1.56s; history0.67–1.76s full render-to-file. Logs: Notes/motion_cycle1_v002.json and motion_history_v002.json. Clips prove hardware/effects behavior, not final lighting or full surface descent. Native/media local only; no off-machine backup claimed.

Full-environment640×360 AA5 stills passed2.89–4.50s. A later480×270 test failed at528 (5.514s) and stopped; see Notes/motion_benchmarks_v002.json. Culling benchmark passes1.47–3.20s. No unrestricted full-scene batch profile is claimed. Saved480×270 defaults are inspection settings; benchmark again before any full-scene batch. Rough-v001 stills and evidence retained.

Latest trial v004 replaces the early visible slit with Surface v008's complete viewing passage and flared entry sleeve. Camera timing advances smoothly by up to2f over89–112 so rock begins95, then returns to original timing; later112–528 curves and World v014 reveal unchanged. Proof `Previews/Entry-v004/S01-S02_pipe_to_rock_v004.mp4` covers85–105 at24fps,0.93–1.06s/frame, full environment. Earlier v003 proof remains for comparison. See latest handoff for geometry/timing details and sampled checks. Final look, full-journey proof and owner acceptance remain open. Wrap only on his instruction.

Waveform investigation: [organic demo comparison and shared amendment recommendation](Notes/waveform_review_v001.md). Read-only review; v007/master unchanged.

Full v016 preview now available: `Previews/Full-v016/S01-S02_full_v016.mp4`. 756 frames at24FPS,31.5seconds,640x360. Render job wall time551.806s (9m11.8s); active export383.355s, average0.507s/frame; wall average0.730s/frame, max1.157s. Decode756frames/31.5seconds, zero drops/duplicates. Native unchanged; full-shot owner review pending. [Timing record](Notes/full_v016_summary.json). Video local only.

