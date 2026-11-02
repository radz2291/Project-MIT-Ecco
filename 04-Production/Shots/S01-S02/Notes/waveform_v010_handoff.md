# Approved sharp waveform applied to actual S01–S02

Owner authorized migration of the approved shared waveform on2 November2026. New scene: `../Scenes/S01-S02_production_v010.blend`, built directly from the selectedv007 full scene, retaining its original camera and environment/grid setup. v009 rolling-organic trial remains preserved and unselected.

All six `WF sequence event` objects use the linked v017 parameter mesh and Geometry Nodes group, with its shared controller linked into the scene. The approved three-pulse shape, variation, strand spacing and cyan/violet colors remain shared defaults. Each field retains its original sensor origin, route basis and measured display gap. Timing is local, Loop off; shared master was not modified.

The scene's original display windows are short. This binding compresses the default20-reference-frame train to3scene frames. Travel fills the remaining outgoing/return windows. **Complete outgoing tail reaches the wall at the existing contact frame; reflection starts at the existing echo frame; complete return tail reaches the sensor at the existing receipt frame.** Heads arrive3frames before their tails. Contact/measurement cues and camera are not moved. This avoids chopping the train off when its head arrives. All three approved pulses remain; judge their readability in native24FPS playback, rather than assuming the8-second demo has the same pace.

`waveform_v010_install.json` records per-event controls/landmarks, native SHA256, camera comparison, measurement samples and reopened relative links. `waveform_v010_render.json` records three representative benchmark frames followed by first/late-cycle proofs, with strict full render-to-file<5s at1920×1080 using the existing pixel-guide exporter. Media stays under `../Previews/Waveform-v010/`. The camera, BHA, measurement reveal and other shot elements are retained.

Reopen helper: run the scene's `START HERE — pixel guides` text to restore the separate pixel-grid overlay. Waveformv017 itself needs no runtime script. Select any `WF sequence event` modifier to adjust local timing/size/spacing; edit the shared controller's source for common defaults. Linked master: [v017 control guide](../../../Shared/Assets/Effects/Waveform/README_v017.md).

This is an actual-scene integration checkpoint, not whole-ticket acceptance. Original sources remain unchanged; native scene and videos are local-only. Radzi retains final visual approval and assembly.

Proof complete:81 full render/export calls pass<5s. Clips `first_cycle_v010.mp4` (299–336,38frames) and `late_cycles_v010.mp4` (489–528,40frames) decode at24FPS with zero dropped/duplicated frames. Outgoing305 and reflected313 were visually inspected. Live Blender reset during the late batch after518; resumed from its recorded index without changing the saved native and completed528. The native is reopened for review at305.
