# B202 scanning/reconstruction — in development

Current candidate is **Still01 v002**, pending Radzi direction. [Task report](../../Records/Tasks/T-008/report.md) owns status/evidence; [direction](direction.md) owns the proposed composition and information lifecycle. No approved T27 handover exists yet.

Scene (local/ignored): `Scenes/B202_sampling-history_still01_v002.blend`. Review image: [Still01 v002](Previews/Still_01/B202_sampling-history_still01_v002.png). Source T7 Motion_v005 and accepted T5/T6 preserved. Frozen preview product remains replaceable through the documented T7 rebuild/reverification route; it is not automatically updated by changing only the linked library.

Open at saved frame31 with view layer **FAST model and mechanism**. New collection **B202_ILLUSTRATIVE_SAMPLE_HISTORY** contains **B202_SAMPLE_DISPLAY_CONTROL** and144 surface sample tiles. `visible` toggles samples; `display_radius_m` scales their display footprint. Changes to scripted custom properties require `update_tag` and a frame/dependency reevaluation. Build parameters `axial_history_m` and `rotation_turns` document history generation, and do not move samples live. Rebuild/version for a different path, density, wall or source; reproject tile corners after substantial size changes.

Each tile stores its source wall hit, triangle and illustrative historical sensor/age. v002 tile corners are ray projected onto actual retained T7/T6 wall geometry with0.10mm inward display offset. White denotes historical sample location only, not quantitative radius or amplitude. No literal rock illumination or instrument accuracy is asserted.

Inherited **B201_MOTION_CONTROL**, **ACOUSTIC_CONTACT_CONTROLLER**, T7 keys and materials remain intact. Playing this consumer plays inherited T7 pulse/echo only, with a static historical display: **it is not a coherent B202 animation**. New motion belongs to fresh-agent T27 after T8 acceptance. Current camera and light are inherited; final film choreography/finishing deferred.

Retain `v001` locally for the rejected bead-display comparison. No reconstruction/amplitude/unwrap assets have been made. Actual source-axis motion, scheduling and calibrated data mapping remain technical review questions, not assumptions for final lock.
