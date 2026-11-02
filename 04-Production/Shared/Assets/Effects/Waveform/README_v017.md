# Approved sharp pulse — shared v017

Radzi approved the sharp finite-pulse animation and its 360° camera proof on 2 November 2026. This version packages that design as a live, reusable Geometry Nodes asset. The defaults keep the approved three varied heartbeat-like pulses, cyan send, violet reflection, separate moving head and tail, and wide strand separation. The waveform changes shape as it travels; it is not a frozen shape translated down an axis.

- Master: [Waveform_shared_v017.blend](Waveform_shared_v017.blend).
- Working examples: [Waveform_demo_v017.blend](../../../Demos/Waveform_demo_v017.blend).
- [Interface/defaults](Waveform_interface_v017.json), [behavior checks](Verification_v017.json), [render timings](Render_verification_v017.json), [release hashes and results](Release_v017.json).
- Approved source retained: `Shots/S01-S02/Scenes/Waveform_direction_quick_v006.blend`. v015 and v016 remain intact for pinned consumers and comparison.

## Two places to control it

Select **WF_MASTER_CONTROLS**, then the modifier tab, to change the common look. Select **WF_PULSE_FIELD** to change that signal's timing, route and overrides. The master contains only these two objects, no cameras or scene lighting. Controls are grouped in named modifier panels, with detailed local style panels collapsed initially.

| Control family | Available adjustments |
| --- | --- |
| Pulse train | 1–5 pulses, pulse spacing, spacing/height/width variation, repeatable variation seed, tail allowance |
| Pulse shape | Overall width, small dip before spike, spike width, undershoot, rebound, ringing amount/period/decay, dispersion and attenuation |
| Strands and size | 1–17 strands, separation, strand phase offset, height, ribbon depth, thickness, head/tail fade, endpoint height |
| Colors | Separate outgoing/reflected colors, emission strength; shared strand brightness gradient |
| Head and tail | Enable/disable markers, separate head/tail size; head waits at destination until the tail arrives |
| Playback | On/off, send+return/send-only/return-only, start frame, travel duration, speed, one-shot/loop, quiet interval |
| Reflection | On/off, wait for outgoing head or complete tail, delay, return travel, train length scale, echo strength, optional flipped pulse |
| Placement | Start/end anchor objects, or manual origin/length/basis; follows moving and rotated anchors |
| Per-instance changes | Quick pulse/strand/separation overrides; height/depth/thickness multipliers; full independent style; separate outgoing/reflected material overrides |
| Shot timing | Follow scene FPS, fit entire active send/return to an end frame, reusable timing node group and evaluated arrival-frame attributes |

**Use master style** defaults on. Quick overrides default to inherit: count0, separation−1. Turn Use master style off to use the closed Local panels for a separate style; those values start at the approved defaults. Shared colors still apply until **Use material overrides** is enabled and both materials assigned. This permits multiple different signals in one scene without altering other instances.

## Reuse without breaking another shot

1. Link the `WAVEFORM_PULSE_v017` collection from the master. Retain its controller. Make the field object local while retaining its linked mesh/node groups, or copy the linked field to a local object as the demo builder does. Link its controller into the scene so shared values evaluate.
2. Duplicate the local field object for additional signals. Modifier values are independent; the immutable parameter mesh and node groups should remain shared. Do not edit the underlying parameter mesh.
3. Assign local Start anchor and End anchor, enable Use anchor objects, and set timing. The Up axis guides the ribbon roll. Automatic basis fallback handles a vertical route or a parallel/zero up hint. Coincident/unassigned anchors fall back to the manual route. For manual routing, provide orthogonal unit axis vectors. Keep field scale uniform; use the size controls for shape changes.
4. Keep camera, lights, anchors, contact/measurement events and shot animation in the consuming scene. Animate modifier controls normally if needed. Save relative library paths. Changes to common master defaults affect linked consumers and require an affected-shot check.

Optional [authoring helper](Scripts/pulse_asset_api.py) provides `get_input`, `set_input`, `duplicate_instance` and `arrival_readouts`. Blender5.2 modifier input values live under `modifier.properties.inputs.<socket identifier>.value`; use interface names through the helper instead of assuming identifiers. No Python, handlers, add-on, shape-key bake or auto-run script is needed to play the saved asset. Simple native material drivers were tested with auto-execution disabled.

## Timing contract

All duration/shape values are expressed in **reference frames**, default24FPS. Start frame and Fit end frame are scene frames. With Follow scene FPS on, the durations maintain their seconds at another FPS; disabling it treats duration numbers as scene frames. Speed scales the entire event together. Fit end frame, when later than Start, overrides speed/FPS scaling to finish the active sequence exactly there. It does not stretch a single stage independently.

Default landmarks at24FPS:

| Event | Frame |
| --- | ---: |
| Send head leaves A | 5 |
| Send head reaches B | 21 |
| Complete send tail reaches B | 41 |
| Reflected head leaves B | 43 |
| Reflected head reaches A | 59 |
| Complete reflected tail reaches A | 79 |
| Next send starts | 101 |

Automatic train duration = final pulse onset + Tail allowance. Default20; explicit Train duration override0 selects automatic. Reflection delay follows either head or tail completion, depending on Reflection after tail. Mode2 starts the return immediately at Start rather than waiting for an unseen outgoing event. Reflection enabled must remain on for a return. Loop quiet frames default22 reference frames, giving96 scene frames per loop at24FPS. Loop period override is a scene-frame minimum; a shorter value cannot truncate the full event plus quiet interval. There is no pre-start looping.

`WF_PULSE_TIMING_v017` exposes calculated local time, effective speed, cycle length and absolute first-cycle arrival frames. The field carries `wf17_Send head arrival`, `wf17_Send tail arrival`, `wf17_Return start`, `wf17_Return head arrival`, `wf17_Return tail arrival`, `wf17_Cycle frames` while geometry exists. Readouts for a disabled direction are informational only. Quiet output is an empty mesh, so use the timing node group when cues are required even during silence.

## Demo and evidence

The demo scene dropdown provides: **01 Approved360** (approved orbit, two96-frame repeats), **02 Fixed review**, **03 Local variation** (five pulses/nine strands, tilted/translated anchors, yellow/green local materials), **04 Fit-end30fps** (one pulse, three strands, event ends48 at30FPS). The rings/cameras belong only to the demo. Source links are relative.

Native checks cover clean contents, approved default landmarks/quiet intervals/loop, shared and instance changes, independent consumers, colors, return-only/send/reflection behavior, speed/FPS/end fitting and rotated/vertical routes. Common waveform samples match the approved baked proof within1e-6m. Working render profile is Workbench1280×720 AA8, Standard view; record full render-to-file cost and enforce <5s/frame, including maximum17-strand/five-pulse overlapping send/return before the192-frame orbit batch.

Release result: **54 checks pass**. Sampled correspondence max error3.71e-7m. All194 render calls (two benchmarks plus192-frame orbit) pass the cap, max1.279s. [Packaged native orbit preview](../../../Demos/Previews/Waveform_v017/approved_pulse_360_v017.mp4) decodes192frames/8seconds at24FPS without dropped/duplicated frames. Selected outgoing, reflected and local-variation stills were visually inspected. Reopened demo resolves its relative master link; live Blender is open on its approved360 scene at18.

Limits: authored illustrative signal, not calibrated acoustics. A five-pulse train,17 strands and513 route samples define the supported capacity. Extreme narrowing, long routes or a whole event compressed into very few delivery frames can lose visible detail; adjust width, spacing, tail allowance and timing while watching at output FPS. Broad/long ringing may require a larger tail allowance to avoid clipping. The asset follows a straight anchor-to-anchor route; arbitrary curved paths require a separately scoped extension. This does not promise every future use case without review.

## Consumer/version status

v017 is the approved sharp-pulse family and the current catalog choice for new uses. Its only current consumer is `Shared/Demos/Waveform_demo_v017.blend`. S01-S02 productionv007 remains pinned to v015; trialv009 uses v016 on its first event. Other existing shots remain pinned. No shot silently changes version; fitting this design into their shorter event windows is a deliberate next integration step. v016's rolling organic family was not selected by this approval.

Native master/demo, raw frame sequence and MP4 remain local excluded media. Exact native SHA256 is in the interface manifest. Scripts, manifests, evidence and documentation are versioned; no off-machine native/media backup is claimed. ECCO-057 remains an ongoing collaborative shot ticket; this shared component approval does not close the whole ticket.
