# Shared acoustic events — T46

**Ready for T45 integration against accepted T44 continuity release a08d0ec.** Current native candidates A_v009 and B_v010 preserve predecessors, link direct BHA v007 with nested v006, and pass the strict packet/source/coverage checks. The four-second playable demo and five selected review stills are complete. Exact current native/media/source hashes and limits are in [manifest_v002.json](manifest_v002.json). The prior [hold handoff](../../../Records/Tasks/T-046/hold-handoff_v001.md) remains historical evidence.

18 October 2026. Asset-stage implementation candidate for Radzi review. Controlling direction: T43 VD03 completion amendment and the V3 S02/S04 contracts. No film shot, reconstruction or A-OUTPUT package is built here.

`Acoustics_v003.blend` publishes effect-only `ACOUSTICS_MASTER`. Its nine prototypes contain three cyan send arcs, three emerald return arcs, a curved contact cup, a fine local patch and a fixed acquired-point marker. It contains no hardware or environment. Prototype +Z is propagation/normal; consumer binding supplies sampled pose. Units are metres; shared geometry is not rescaled hardware. Version v002 changes only the arc curve radius from 0.450 to 0.495 mm. The final v003 reduces it to 0.120 mm after actual macro views showed the earlier arcs too thick; local binding turns the fan into the visible circumferential plane. The earlier library and consumers remain preserved.

## Bind a real event

Add this package's `Scripts` directory to Blender Python's search path. In a scene containing exactly one actual sensor reference and one named wall instance, update the depsgraph and call:

```python
from acoustic_event_v002 import sample_native_event
from acoustic_binding_v001 import bind_event
from acoustic_verify_v002 import verify_packet
event = sample_native_event(
    'ECCO_SENSOR_REF_01', 'CASING_CUTAWAY', 'consumer-event-01',
    send_s=.5, contact_s=1.0, receive_s=1.5,
    patch_lifetime_s=.65)
objects = bind_event(event, frames=96, fps=24, library_version='v003')
verification = verify_packet(event, objects=objects, frames=96, fps=24)
```

Use the wall object's actual saved name. The cased package uses its own actual casing name rather than relabeling the open-hole example. The sampler evaluates the linked sensor's local +Z and world pose. It requires exactly one retained temporary imaging cap, samples that cap's actual outer exit, records the unchanged reference separately, then takes the first native BVH wall intersection. Missing or ambiguous caps raise an error. The current cap is 2mm proud of the inherited reference; the exit is a provisional geometric convention, not a newly certified transducer datum. It records emitter/receiver identity, emitter local reference, reference_world_m, native emitter_surface object/hash/offset, sampled exit world pose, hit/normal, wall library/object/version/hash and illustrative seconds. `validate_event` checks the full metadata and actual source hashes; `validate_native_event` resamples the actual placed cap and wall. Event exports conform to `ecco-acoustic-event-v001`; actual exports use `native_ray_intersection_illustrative_timing`, while declared fixtures must retain their different provenance.

The binding links shared mesh/curve/material data relatively when the consumer is saved. The local event objects own native keyframes. No runtime handler or auto-run script is needed for playback after fresh reopen. `ACOUSTICS_CONTROL_<event_id>` owns opacity and visibility; source event timing/lifetime remain explicit metadata. To change timing/lifetime or sampled geometry, edit the event and rebind rather than edit the saved hit arbitrarily. Hardware, camera, assembly animation and wall remain consumer-owned. Shared prototype geometry/materials remain master-owned.

Hold the assembly through `hold_emitter_until_s` when using these fixed-pose event samples. Common send/contact/receive times describe the leading front. `arc_phases` records three fronts with 0, 0.07 and 0.14-second lag; `packet_intervals`, `packet_end_s` and `hold_emitter_until_s` include the final return at receive_s + 0.14 seconds. The complete schema is [event-interface_v002.json](event-interface_v002.json). The demos rotate and travel between complete packets. The return therefore reaches the same actual registered sensor; acquired contact points remain fixed in the world during later motion. Arcs taper at their sampled endpoints and terminate within the wall, without a beam continuing through it. A cup and patch briefly identify contact; the point persists. This is illustrative information choreography, not a visible physical emission or acquired field measurement.

## Reuse and revision

The two local reuse tests have distinct cameras, frame ranges and event timings. They share T44 hardware/environment and this effect package. For revision propagation, capture all current library paths as absolute paths before reloading a successor; then preserve camera/timing/local animation, save a new consumer with relative links and fresh-open. Use Blender's exposed library path resolved against the current consumer: actual nested paths are normalized there. Strict existence/hash checks apply; no basename fallback is allowed. The first attempted v002/v003 relocation exposed shifted unrelated library paths; those files are retained as failed attempts. Repaired v004 consumers demonstrate bounded v001→v002 shared revision with camera, timing and world-control animation preserved. Native v006 successors correct the emission exit to the actual retained cap face and use geometry-derived inside-annulus cameras. V008 links v003 thin arcs and reduces the fixed point to 0.300 mm radius. Current A v009 and B v010 add the accepted T44 continuity release and complete packet timing. B v010 reverses only its axial camera offset after actual visibility checks found the far rim exposed in its preserved predecessor.

Check the returned `all_pass` and individual results from `verify_packet` in the actual saved consumer. It checks each front in both directions, finite envelopes, actual cap/reference hold and native source/contact positions. Fresh native checks and actual selected renders cover the final candidates; no runtime handler or automatic script execution is required.

Relevant future V3 consumers: S02-A, S02-B, S02-C, S04-B and S04-D. These are planning mappings, not migrated movie shots. A-CASED uses the same binding against its own native steel contact; A-OUTPUT may consume the portable event record later. Full waveform systems, maps, reconstruction, calibrated response and actual movie timing remain outside this package.

## Provenance and limits

Accepted native T44 BHA v007, its nested v006, environment v009 and nested ECCO film v002 remain immutable. A v009 and B v010 attach the canonical 12m continuation to their existing hardware instance. The source housing remains 2.400 m along +X. The inherited three sensor references remain one plane, 120° apart; their source status does not establish a newly certified transducer face/shoulder datum. No mud-sensor coordinate is invented. B201 v006 supplied inspected design precedent for fixed ray contact, monostatic return and schematic timing; its legacy geometry and ten-second score are not copied into consumers.

The minimal `Echo arrival` cue is explicitly labeled `Schematic timing`, uses no invented numbers and appears after contact. Segoe UI is loaded from the installed Windows system font and is not redistributed. This is a bounded arrival cue, not the full GRAPHICS/OUTPUT system.

Benchmarks and visual results are recorded in the [task report](../../../Records/Tasks/T-046/report.md). Rendering requires T45's serialized queue. Start at 1280×720/24 fps/EEVEE16/Vulkan/AgX Medium High Contrast, benchmark complete render-to-file calls and keep every sample strictly below 5s before batches. Normal-cache performance never resolves the documented T44 empty-cache initialization exception.

All `.blend`, MP4 and raw frame files remain local and Git-ignored on this machine. Exact paths/hashes and backup status are in the manifest; no native upload or off-machine backup is claimed. T45 alone integrates permitted scripts/reports/evidence/selected stills. Human appearance, narration-led comprehension and technical acceptance remain Radzi/client review.





