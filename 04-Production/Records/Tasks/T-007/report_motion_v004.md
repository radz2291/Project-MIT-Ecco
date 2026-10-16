# T7 — Organic pulse/contact/echo preview v004

Task fbe3e8c3-5ccf-4205-9aa4-48832b0d2cd3. Base cffb7b9b0ee56feab6385607da1ea86a0efd2c9f. Radzi requests less staged surface interaction, explicitly frees motion from the still layout and authorizes the proposed causally linked refinement. Existing approvals/source assets and v002 are preserved. Still05 remains KIV and explicitly excluded.

## Review summary

[Updated 10-second preview](../../../Mechanisms/B201/Previews/Motion_v004/B201_pulse-echo_fast-preview_v004.mp4): the cyan front reaches actual rock, cells grow with local contact age, the emerald echo develops while acquisition is settling, and the same sensor receives it. Fixed camera/hardware/wall, three sampling stations, silent 960x540/24fps/240 frames. No Still05, waveform, distance graphic, labels, arrows or numbers.

The wall no longer has a separately timed global appearance/hold/fade. Its material evaluates distance from the actual sensor at each rock point and compares this with the visible front radius. Cells mature progressively with stable spatial variation and decay by their own local contact age. The fine cell structure, irregular geological influence and underlying rock shading are retained. Cyan contact seam, sampled cells and return share the same actual spatial event; echo origin remains the actual ray/rock hit. A smooth outgoing approach joins the readable surface sweep without an abrupt velocity change. The outgoing packet dissolves as the emerald return becomes legible.

This is a bounded motion refinement using Scene Director V03 cause/event/result and the existing [direction contract](../../../Mechanisms/B201/direction.md), not a new camera exploration. The old still layout is not an animation hold requirement. v003 is retained as a useful test: its local cell lifecycle worked, but its abrupt post-contact slowdown was replaced in v004.

Measured native render time: **0.698 seconds/frame average; 2.118 seconds slowest**. All 240 frames remain below10 seconds. All delivered frames decoded successfully; 239 distinct, no blank frames. [Video QA](Evidence/Motion_v004/video-qa.json) | [Render timing](Evidence/Motion_v004/render-progress.json) | [Output manifest](Evidence/Motion_v004/output-manifest.json). Representative contact buildup and reception frames visually inspected.

## Editable source and verification

Scene: `04-Production/Mechanisms/B201/Scenes/B201_pulse-echo_fast-preview_v004.blend`.

[Build](../../../Mechanisms/B201/Scripts/build_motion_preview_v004.py) | [Procedural contact material](../../../Mechanisms/B201/Scripts/wall_contact_flow.py) | [Render](../../../Mechanisms/B201/Scripts/render_motion_preview_v004.py) | [Encode/QA](../../../Mechanisms/B201/Scripts/encode_verify_motion_v004.py).

Native keyed controls and shader nodes; no frame-handler dependency. Shared accepted T5 plugged v002 and T6 well v003 stay unchanged. Exact evaluated product geometry is a replaceable preview consumer. Original Still03 v013, Still04 v003 and all previous variants are retained.

[Fresh-open verification](Evidence/Motion_v004/verification.json): 52 checks pass. Exact source wall mesh and evaluated product topology/vertices unchanged; camera unchanged; links resolve; outgoing axial contact and return-to-original-cap endpoints pass at all three stations; emerald response begins at first reception. Checks also inspect the saved wall emission graph for actual position/distance and local exponential memory, and verify that the advancing visible front drives the contact radius while the global patch envelope stays at unity.

Event frames stay 8/28/48, 88/107/126 and 168/185/202 for emit/axial-contact/reception. The shader responds to the true local sphere/rock intersection, which need not occur at the axial ray hit for every rock point. Three stations remain 0/6/12 degrees with the tool held during each round trip.

The contact approach/sweep and local response times are deliberately slowed illustrative choreography. Equal outbound/return frame intervals preserve round-trip meaning but do not claim constant physical sound speed, measured TOF, acoustic simulation, real RPM or texture acquisition from a single ping. Cyan/emerald and rock digitization are cinematic representations. O04 calibration and MIT/B206 technical review remain unresolved; no client contact or engineering certification is claimed.

[Contact buildup](Evidence/Motion_v004/Decoded/decoded_f031.png) | [Surface settling and return](Evidence/Motion_v004/Decoded/decoded_f038.png) | [First reception](Evidence/Motion_v004/Decoded/decoded_f048.png)

## Review and synchronization

Visual question: does the wall response now feel caused by the travelling wave, with a fluid transition into the echo? Exact moving candidate awaits Radzi review. Full T7 remains incomplete: Still05/waveform deferred at direct instruction, B206 feedback/human acceptance pending.

Reports/scripts/evidence and a small selection of review images are synchronized to authorized main; exact verified containing SHA and pinned report are recorded in Rolladice. Blend, MP4 and raw frames are organized locally only, without an implied remote media backup. Prior v002 report is archived as report_motion_v002.md. No final finishing or downstream task execution.
