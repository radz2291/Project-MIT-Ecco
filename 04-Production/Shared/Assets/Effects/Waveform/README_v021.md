# Approved connected exchange — shared v021

Radzi approved quickv022 on 2 November 2026. This release preserves its beam, bipolar pulse, cyan send/violet feedback, active held contact patch and center-out tile glitch. Component appearance approval is separate from whole-shot and client acceptance.

Master: `Waveform_shared_v021.blend`. [Preset](Approved_beam_exchange_v001.json). Demo: `../../../Demos/Beam_exchange_approved_demo_v021.blend`, an actual-scene fixture with shot-owned camera, hardware and target assignments. Older versions remain preserved for pinned consumers.

## Reuse and controls

Link the master collection containing `WF_MASTER_CONTROLS` and `WF_PULSE_FIELD`; make a local field instance using [pulse_asset_api.py](Scripts/pulse_asset_api.py). Keep the shared controller linked. Use master style for approved defaults; turn it off for local shape overrides. Native controls include pulse count/spacing/variation/seed, positive and negative shape, height, strands/separation, width, attenuation, amplitude breathing, separate send/return colors, start/travel/reflection timing, speed, beam opening/setup/closing and Enabled. Markers are off in this preset. Changes intentionally alter the approved look.

[approved_exchange_api.py](Scripts/approved_exchange_api.py) contains optional authoring helpers:

- `apply_approved_preset(modifier, start_frame)` applies timing and returns absolute landmarks. Use with the v021 style controller.
- `create_contact_patch(collection, point, normal, start_frame, size_m, enabled, overrides)` creates the small animated patch at the actual wall hit. Overrides include color, minimum scale, breath period, arrival/reveal frames and handover. Its Enabled custom checkbox controls viewport/render visibility. Size and animation remain editable in the native object/actions.
- `configure_surface_patch(wall, faces, point, start_frame)` recreates the approved tile colors and four center-out reveal groups. Supply intended faces on a wall already using shared measurement reveal and receipt/order attributes. The approved reference is a 4 by 4 patch. Face selection and hit placement remain shot-owned.

Saved animation uses native geometry/material actions and needs no Python handlers. Helpers scale timing with scene FPS; explicit `frame_scale` supports custom choreography. If waveform speed, loops, fitted timing or phase mode changes after setup, re-author patch/reveal timing using the new event landmarks. Companion animation does not automatically follow later modifier edits.

At 24 FPS, relative frames are contact +5, pulse launch +6, reveal +22, feedback +28, return complete +49, beam closed +52. Review window is 54 frames / 2.25 seconds. The 3 mm patch gently breathes until reveal. No circular impact effect is required. Camera, real contact intersection, face selection, tool motion and event spacing belong to the shot.

## Verification and delivery

[Preset checks](Approved_exchange_verification_v021.json): nine waveform samples match approved review within 1.90e-9 m; 24 patch frames match scale/color; tile colors match exactly. Enabled visibility and 30 FPS authoring landmark/contact timing pass. This does not certify every optional control combination.

Production S01–S02 v016 uses six exchanges. All six pass centered-hit, feedback-before-turn and patch handover checks. Master has two objects, three node groups, no libraries or cameras. [SHA256 and consumers](Waveform_interface_v021.json).

Native files/videos remain local only. Scripts/configuration/reports/selected stills synchronize separately. No off-machine media backup is claimed.
