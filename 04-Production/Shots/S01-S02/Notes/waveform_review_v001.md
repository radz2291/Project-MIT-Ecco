# Waveform demo / shot comparison and shared amendment recommendation

ECCO-057,2 November2026. Read-only review requested by owner, extended to advise where changes belong because the waveform is reused. Current scene remains selectedv007, original camera motion. No Blender scene, shared master or native demo was changed.

## Found references

- Organic motion proof: `04-Production/Records/Tasks/T-056/Previews/rolling-wave-field-context_v013.mp4`, native24fps/4s.
- Its editable native: `04-Production/Shared/Archive/2026-10-31/Assets/Acoustics/RibbonWaveform_v013/S02_rolling-wave-field_v013.blend`.
- Current minimal linked demo: `04-Production/Shared/Demos/Waveform_demo_v015.blend`.
- Current reusable master: `04-Production/Shared/Assets/Effects/Waveform/Waveform_shared_v015.blend`.
- Shot comparison clip: `../Previews/Waveform-review-v001/current_v007_event1.mp4`, frames299–326 at24fps, extracted from the completedv007 render. Native timing retained in both references; clips have different durations, with no normalization or slow-motion comparison.

The clean v015 package preserves the v013 field through the internal group name WF_FIELD_LIVE_v014. That internal name is not evidence of an incorrect library link. Fresh native inspection found the demo/master/reference and their libraries resolve; source hashes before/after each read match. Historical T056 repackage verification documents coordinate agreement with v014; T051 independent checks document the underlying v013 match. This review freshly checked controls, source formula and native structure, not a new exhaustive geometry-equivalence test.

## Why the shot looks different

| Feature | Organic reference / current demo defaults | Selectedv007 shot |
|---|---|---|
| Source emission |30frames|3frames on all six events|
| Primary wave period |7.5frames|7.5frames, frequency multiplier1|
| Cycles during emission |4|0.4|
| Outgoing and reflected field |Overlap and interfere|Shot end gates separate them|
| Filament radius |18micrometres, local multiplier1|54micrometres, local multiplier3|
| Appearance |Eevee emissive color/alpha|Workbench SOLID/material color|
| Event timing |Start8, travel12, freely decaying tail|Source send/contact/receipt windows locked per instance|

The two-component rolling formula (frequency ratio1:1.65 and strand phase offsets) is still present. The organic motion has not been replaced by a different engine. The shot adapter compresses emission to less than one primary cycle, stops outgoing motion at the contact gate and truncates the return at receipt. This strongly favors a single traveling bulge instead of overlapping rolling crests. Thicker strands and Workbench's lack of shader emission/alpha make it read as a cage. Workbench retains the geometry's removal of effectively zero-alpha vertices, but does not show the graded shader fade.

For event1: start300, outbound gate309.01, return delay1 after9-frame travel, return gate318.01, return travel8. The outgoing component ends before the reflected component begins, removing the interference present in the demo. Both share the same24.576mm gap, approximate40mm width/height reference and unit strength/height/width overrides. The image difference is not simply a camera scale mismatch.

## Reuse and amendment boundary

Confirmed current uses: the minimalv015 demo and six local waveform instances in S01–S02v007. Earlier T056 consumer mapping also contains one S02 event and two S04 events linked to v014. Those historical copies use the same short-envelope/thick-strand pattern (S04 duration2.56frames, radius multiplier3), showing this is a reusable adapter issue. T056 explicitly excludes those historical integrated copies from the later clean-master/demo delivery. Their current migration status is not inferred; no approved S04 sequence was edited or claimed upgraded. Catalog guidance states archived/historical scene links are not maintained automatically.

**Recommended shared amendment:** keep v015 and the original organic preset intact; make a versioned shared successor with reusable rolling/short-event presentation, a controlled outgoing/return blend, thinner-strand presets and geometric taper that remains visible in playblasts. Validate both the long-form organic demo and a short-window demo. Keep its behavior native Geometry Nodes and expose controls, rather than duplicating waveform construction inside each shot. The field is illustrative display animation, not calibrated physical/acoustic data.

**Keep shot-owned:** emission placement, sensor/wall route, open/cased context, send/contact/receipt landmarks, camera and measurement reveal. A shared visual preset must not silently move these events. Copying the30-frame duration directly into an18-frame send/return window would extend wave activity beyond the current receipt/reveal. The adapter must fit readable rolling motion to each window; any needed timing extension is a separate visible shot decision.

**Migration proof:** review one complete S01–S02 send/contact/return/reveal cycle and both S04 open/cased consumer cases, with before/after timing and <5s render-to-file checks. Reopen relative links and check peak geometry, boundaries and receipt-before-reveal. Record exact upgraded consumers and keep other shots pinned. Only promote a new shared version after its focused proof; current investigation makes no native amendment.

## Evidence and limits

waveform_current_inspection.json records the six current modifier settings. waveform_demo_inspection.json records independently opened demo/master/v013 settings, embedded usage notes, libraries and unchanged hashes. Source behavior checked against T056/build_shared_gn_v014.py, field-model_v013.json, shared-controls-guide_v014.md, consumer-mapping_v014.json and repackage-report_v015.md. Two selected four-frame sheets show native-time shape evolution from the existing videos. Both videos fully decode without errors. Viewing styles differ, so the lit-vs-solid appearance comparison is qualitative; the duration/radius/gating differences are directly read from native settings and node construction.

The running Blender scene is untouched at frame316. Native/video stay local; scripts/reports/selected sheets are synchronized evidence. No engineering or owner acceptance claimed.
