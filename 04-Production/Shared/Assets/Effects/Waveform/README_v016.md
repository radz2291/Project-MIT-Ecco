# Shared waveform v016 — candidate

Versioned ECCO-057 candidate,2 November2026. `Waveform_shared_v016.blend` contains2objects/2meshes/1material/4GN groups, no cameras or external libraries. Originalv015 is unchanged and remains the catalog baseline. [Manifest](Waveform_interface_v016.json). [Four-scene linked demo](../../../Demos/Waveform_demo_v016.blend).

## Operation

Select **WF_LIVE_FIELD → Modifiers → Motion Preset 0 Organic 1 Short**:

- **0 Organic:** originalv015 rolling field, including its material behavior. Ten default geometry samples match exactly (zero coordinate error).
- **1 Short:** two rolling spatial crests, two coordinated frequency components, tapered strand geometry and a brief post-contact outgoing/return overlap. The temporal carrier stays at a7.5frame period at frequency multiplier1. This is an authored display profile, not a30frame animation accelerated into3frames.

Select **WF_MASTER_CONTROLS → Modifiers** to edit reusable Short style:

| Shared setting | Default | Meaning |
|---|---:|---|
| Short Crests |2|Spatial crest count across the route|
| Short Packet Fraction |0.9|Width of the traveling envelope relative to gap|
| Short Contact Blend Frames |4|Outgoing tail fade after contact; clamped against return duration|
| Short Return Fade Frames |3|Fade before receipt; clamped to half the return window|
| Short Stroke Factor |1.5|Peak thickness multiplier; local Radius Override defaults1|
| Short Taper Power |0.65|Geometry-radius taper, visible in Workbench|
| Short Height Fraction |0.65|Profile height fraction of half the shared reference height|

Shared strength, echo strength, dimensions and appearance controls remain. Open/cased context remains a local illustrative selector: cased tightens decay and weakens echo as before. All animation is native Geometry Nodes, with no waveform runtime script or add-on.

## Shot-owned timing

Start Frame / Contact Frame / Receipt Frame / Echo Delay Frames and route axes/gap remain local. Zero Contact derives from Start+Travel; zero Receipt derives from Contact+Delay+Return Travel. Keep start<contact<receipt and return start before receipt. With Lock Event Timing enabled, global playback changes cannot move Short event landmarks. Source playback/frequency knobs are display controls, not physicalHz.

**Duration Override and legacy Outbound/Return End Frame gates apply to Organic.** Short uses packet fraction, explicit landmarks, contact blend and receipt fade. This deliberately allows the outgoing tail to continue briefly after contact, while the reflected front begins. It ends by receipt, before the measurement cue. At S01–S02's309contact/310return start/318receipt, a4frame tail creates a short overlap and a smooth finish. It does not move contact or measurement timing.

Source-file controls update linked consumers after reload/reopen. Local timing/style multipliers affect only their instance. Use the master for common visual behavior; preserve per-shot chronology. Review changed values at the intendedFPS; only default and recorded test settings are validated. Color/emission/alpha remain Eevee material features; geometric taper supplies Workbench fading.

## Consumers and checks

Candidate consumer: `Shots/S01-S02/Scenes/S01-S02_production_v009.blend`, event1 only. Events2–6 remainv015; v007/full render and rejected camera trialv008 are preserved. Separate `Shared/Demos/Waveform_demo_v016.blend` has Organic, Short S01–S02, S04 open and S04 cased fixtures. S04 fixtures reuse recorded event landmarks/gaps with a canonical review camera and cue; no approved S04 scene, camera or dataset is migrated.

Checks pass: Organic reference equality; pre-contact absence of return; brief overlap; zero geometry at/after receipt; geometric taper; default field bounds under40.1mm; enabled-off; open/cased change and restore; seven shared-style controls change and restore; locked playback; recorded S04 basis rotation (max error2.2e-9m). Full fixture proofs and the shot cycle stay strictly below5s/frame. [Shot handoff](../../../../Shots/S01-S02/Notes/waveform_v009_handoff.md).

The Organic fixture marks tail-receipt completion at62 and measurement at68; its simplified cue is separate from the unchanged waveform. Short fixtures use their explicit shot receipt landmarks.

Candidate only; appearance acceptance and wider migration await owner review. Native/video remain local, with no off-machine backup claim. Prior master and other consumers are not silently upgraded.
