# Shared waveform candidate — shot v009

ECCO-057,2 November2026. Owner authorized a versioned shared waveform with preserved Organic and a short-event rolling preset, a complete S01–S02 proof and S04 open/cased reuse checks. Current candidate scene: `../Scenes/S01-S02_production_v009.blend`, saved/open311. Originalv007 camera motion retained. Dirty starting session preserved in `S01-S02_session_before_waveform_v009.blend`; v007/full22s render remains baseline. No whole-film rerender for this trial.

## Result and scope

New reusable master: `Shared/Assets/Effects/Waveform/Waveform_shared_v016.blend`. Two native presets: Organic0 preservesv015; Short1 has rolling crests, a tapered mesh stroke visible in solid playblasts and controlled overlap between outgoing tail and reflected wave. Shared source owns the behavior and seven style controls; each shot owns its timing/route/context. [Controls and semantics](../../../Shared/Assets/Effects/Waveform/README_v016.md).

Only **WF sequence event1** usesv016. Its field carrier and node group both link to the new master. Other five events stayv015. Source emission300/contact309/return start310/receipt318 and measurement reveal timings remain. The outgoing tail now fades through313 instead of cutting at contact, creating a short overlap with the return; the whole field is empty by318. The short profile uses its own packet fraction and explicit landmarks; the old3frame Duration Override is retained only for Organic compatibility. Camera/lens curves and evaluated measurement-wall geometry matchv007 at the checked frames.

The field is an illustrative display. The two coordinated sine components and strand phase offsets roll within a traveling envelope; the carrier is not sped up10times. Default Short height/width stayed below40.1mm in the fixture checks. Peak stroke factor1.5 plus envelope taper gives thinner, fading strands; material glow/alpha still requires material rendering. The visible look remains for owner judgment.

## Review media

- `../Previews/Waveform-v009/S01-S02_waveform_v009.mp4`: actual scene frames299–336,38frames/24fps,1920x1080. Includes send/contact/return and the measurement settling afterward.
- `compare_v007_left_v009_right.mp4`: original left, candidate right, synchronized native-time cycle.
- `compare_v007_left_v009_right_3x.mp4`: same comparison repeated three times for easier viewing (114frames/4.75s), without slow playback.
- Four native scenes in `Shared/Demos/Waveform_demo_v016.blend`: Organic reference; Short S01–S02; Short S04 open; Short S04 cased. Organic96frame and S04 two27frame movies are under `Shared/Demos/Previews/Waveform_v016/`.

S04 is checked in isolated sensor/wall fixtures using recorded gaps, event windows and open/cased flags, plus a numerical test of its actual rotated basis. These are not approved-section renders or a silent S04 migration. An initial solid sensor fixture obscured the field; its native is retained as `Waveform_demo_v016_occluded_fixture.blend`. The final demo uses an open sensor ring. Fixtures and cue graphics are illustrative; no section data was altered.

## Evidence

Organic default at10sample frames: zero coordinate difference fromv015. Sourcev015 hash unchanged. Seven shared controls independently change and restore the Short geometry while Short controls leave Organic unchanged. Enabled-off, open/cased restore, precontact return absence, overlap, geometry fade and empty-at-receipt pass. Default fixture span under40.1mm; S04 basis error2.2e-9m. Fixture measurement cue appears after receipt.

Actual shot38frame1080p proof: max0.861s/frame. Four1280x720 fixture benchmarks: max1.339s. Fixture150frame640x360 batches: max0.418s. Every measured full render-to-file passes strict<5s. All six encoded videos decode their expected frame counts. Before/after event PNGs299/324 match originalv007 exactly.

Native fresh reopen passes: same camera/lens action hashes; same evaluated measurement-wall hashes at299/309/311/318/328/336; other five waveform groups unchanged; libraries resolve. UI socket order/bounds/descriptions were finalized after geometry proofs; no formula/default change. Current native/master/video hashes are in manifests. Waveform is fully native GN; the separate existing pixel-grid overlay still uses its START HERE helper.

Scripts and JSON/txt under Scripts/Notes reproduce build, shared controls, fixtures, native comparisons, rendering and packaging. Candidate source is clean2objects/2meshes/1material/4groups, no cameras/libraries. Native/video/raw frames local only, no new off-machine backup claimed. Appearance approval and wider migration remain open; task not closed.
