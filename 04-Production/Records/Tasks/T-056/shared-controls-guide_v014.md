# Editable shared waveform — v014

Open `04-Production/Shared/Assets/Acoustics/Waveform_shared_v014/Waveform_shared_v014.blend`. Select **WF_MASTER_CONTROLS**, open **Modifiers**, and edit **MASTER CONTROLS — shared across consumers**. These are native Geometry Nodes sockets. Playback works with script auto-execution disabled; no handlers, rebuilding scripts or add-on are required.

The approved v013 rolling field is the default. Its active coordinates match within 0.000000038 m at the checked frames. The default maximum frame height is approximately the 40 mm provisional oval-face height; width is approximately 40 mm. This is an authored cinematic field, not measured ECCO RF, calibrated pressure or a wave-equation solver. One fixed normalization is used, never per-frame normalization.

| Shared control | Result |
|---|---|
| Playback Speed | Speeds the master field and its demonstration contact/receipt/measurement cues together. |
| Frequency Multiplier | Changes the number and rate of internal crests; display frequency, not acoustic Hz. |
| Strength / Echo Strength | Changes outgoing-plus-return height / relative return height. |
| Decay Tightness | Tightens the smooth source envelope. |
| Source Duration Frames / One Way Frames | Changes source activity and propagation delay in the master demonstration. |
| Reference Height m / Width m | Controls artistic display dimensions. Arbitrary changed combinations can change extrema; 40 mm describes the approved defaults. |
| Emission / Color Violet / Color Cyan / Opacity Power | Changes the material appearance in Eevee/material rendering. |
| Strand Radius m | Changes actual filament thickness, including in Workbench. |

Save the shared master and reopen the consumers to reload linked changes. Both consumers link `WF_FIELD_LIVE_v014`, `WF_SHARED_CONTROLS` and the immutable parameter-domain mesh by relative paths. The master control point has no renderable faces. Source geometry and all prior proofs remain separate.

## Two consumers

- `Records/Tasks/T-056/Consumers/S02_waveform_shared_v014.blend`: original S01–S02 camera, 1–528 at 24 fps. Only DW1 traveling SEND/ECHO presentation is replaced. Send starts300, contact309, return starts310, receipt318. Native contact/history/measurement geometry and animation remain source-owned.
- `Records/Tasks/T-056/Consumers/S04_waveform_shared_v014.blend`: original continuous A–D camera, 1–432 at 24 fps. Two local wave instances replace the two sourced SEND/ECHO sets. Leading first event72.60→80.92, echo81.56→90.52; second184.60→192.92, echo193.56→202.52. Later trailing fronts retain the broader source display windows. Original casing response, world travel and wear data/actions remain source-owned.

Select **WF_S02_EVENT_1** or **WF_S04_EVENT_1/2**, open its waveform modifier. Local strength, frequency, decay, dimensions and radius multipliers affect only that instance. The local **Lock Event Timing=1** intentionally isolates source shot chronology from shared playback changes. Timing fields contain the inspected native event windows, including the send/echo delay. Unlocking or changing these fields is a deliberate shot retime and requires an affected-shot review.

**Preset 0 Open 1 Cased** is a native integer selector: 0 reproduces the open default; 1 tightens decay by1.2 and multiplies echo strength by0.8. These are illustrative display presets, not material measurements or replacements for S04 response datasets. S04 instance2 demonstrates the cased setting.

Both source shots use Workbench. Workbench ignores emission, shader colors and alpha; it displays the material's cyan viewport color. Quiet sites are therefore removed by native geometry at an alpha threshold of1e-7. Local **Radius Override=3** improves fine-strand readability in these source views without changing the shared default radius. S04 appears small in its preserved wider camera. Use the shared Eevee master to inspect the full approved luminous appearance. No shot camera was changed to enlarge the field.

Native API callers on Blender5.2 can set `modifier.properties.inputs.Socket_N.value`, then call `modifier.id_data.update_tag(refresh={'OBJECT','DATA','TIME'})` and update the view layer. This explicit dependency tag is required for programmatic in-memory tests; saved/reopened values also work. The regular modifier panel is the user interface.

The older pressure-model sample-input API remains separate evidence. v014 does not claim to reconstruct a full spatial field from an imported receiver trace, and its native controls do not imply a measured-data import workflow.

## Checks and inspection

`shared-control-tests_v014.json` records sixteen passing checks, including saved shared Strength=.8 propagating to both reopened consumers and a saved local Strength Override=.7 changing only S02. Test edits were restored byte-exact. `shared-default-comparison_v014.json` compares approved geometry; `source-preservation_v014.json` compares original geometry, shape keys, actions and custom data at the same frame. Master independent checks are under T051/Evidence.

Short clips play native frames at24fps, not slowed review: S02 frames298–324, S04 frames71–95. The small sequence sheet shows both event progressions. Native/media remain local and Git-ignored; reports/scripts/selected stills can be synchronized. Final owner inspection and acceptance of these shared files remains pending.

S04 front versus tail:80.92/90.52 are the first SEND/ECHO front endpoints; the full source sets continue through83.48/92.44. The adapter preserves those tail windows. At frame95 the shared field is empty; the small retained signal is original **Casing response tail 0**, material **Fine resonance-tail return 0**, left unchanged as section-owned response. Both original-object/action/custom-data and mesh/shape-key comparisons pass:571/548 S02 objects/data blocks and798/728 S04 objects/data blocks.
