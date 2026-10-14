# ECCO ENP3 Storyboard V2 — Section 02

**0:10–0:22 | The First Ping / Reveal the Principle**  
**Status:** Reconciled with Ahmed's comment #2; visual direction ready for client review, NOT technically approved.  
**Previous sequence replaced:** isolated pulse → returning echo → one point → more pulses → ring.  
**New sequence:** early isolated light spots → waveform arrival-time proof → 2–3 additional waveforms → circumferential measurement.

## Section introduction — Padlet-ready
We begin with one ultrasonic ping in near darkness. It reaches the wall, briefly illuminating a small spot, and its echo returns to the originating sensor. After two or three such pings, the same event is represented as a waveform. The interval between transmission and echo arrival provides the sound-travel time used to estimate distance to the wall. A few further waveforms demonstrate repeated measurements as the full drill string rotates. Finally, accumulated readings form a measured 360° borehole outline.

**Core message:** ECCO sends sound, measures the returning echo's travel time and progressively reconstructs the surrounding borehole.

## Panel 1 — The first isolated ping (0:10–0:12)
**Image:** `01_First_Isolated_Ping.svg`

A single ultrasonic pulse is emitted toward the dark borehole wall. When the acoustic energy reaches the rock, one small area briefly appears illuminated. The echo then returns to the same sensor. This introduces the principle visually, without a chart or technical explanation.

## Panel 2 — Two or three more light spots (0:12–0:14)
**Image:** `02_Repeated_Ping_Spots.svg`

The sequence repeats two or three times. Each ping momentarily reveals another nearby part of the wall as ECCO's sensor orientations change with the rotating drill string. The flashes remain short and localized. We deliberately do not reveal a complete image yet.

## Panel 3 — Reveal the waveform and arrival time (0:14–0:16)
**Image:** `03_First_Waveform_TOF.svg`

We connect one visible pulse-and-echo event to a stylized waveform. The first signal indicates transmission, while the later response represents the arriving echo. A highlighted interval shows the measured two-way travel time. With the mud's sound speed and known sensor position, this is used to estimate the distance to the borehole wall, and consequently the hole radius.

## Panel 4 — A few additional waveforms (0:16–0:19)
**Image:** `04_Additional_Waveforms.svg`

Two or three further waveform samples appear as the tool continues to rotate. Their arrival times vary with changes in sensor-to-wall distance. Corresponding measured positions build progressively around the well. This demonstrates repeated measurements before revealing the resulting geometry.

## Panel 5 — Circumferential measurement emerges (0:19–0:22)
**Image:** `05_Measured_360_Ring.svg`

Accumulated wall measurements resolve into an irregular 360° cross-sectional outline around ECCO. The three ultrasonic sensors are located around one plane, 120° apart. The complete drill string rotates with the tool, enabling measurements around the circumference; the measurement markers remain attached to the rock wall rather than rotating with the tool.

**Transition into Section 3:** Retain one measured ring and begin extending the measurements through depth. Section 3 then compares nominal drill-bit diameter with the actual wall geometry.

## Production and engineering guardrails
- Three ultrasonic imaging sensors, 120° apart, in one common axial plane. Actual hardware positions must be verified from MIT CAD; diagrammatic locations are not product drawings.
- Transmitted pulse and returned echo use the **same sensor**. No separate receiver or one-way sensing animation.
- The **entire drill string/tool rotates**; not a rotating internal sensor in an otherwise stationary tool.
- The waveform is conceptual. For round-trip echo time Δt and velocity of ultrasound in mud c, **radial stand-off distance = c × Δt / 2**. Radius from tool axis additionally depends on physical sensor offset, and other corrections, including eccentricity.
- Sound is invisible: the cyan glow and localized illuminated spots are cinematic representation only.
- This section illustrates **travel-time geometry**. Separate amplitude-based imaging is introduced later in Section 3.
- The exact wall geometry and early waveform pacing remain subject to Ahmed's review.

## Padlet update instruction
Replace only Section 2's five existing panel images and captions with these V2 panels. Keep all other Padlet sections as V1 until their revisions are reviewed. Mark this section **V2 — Awaiting Technical Confirmation**; do not mark it client-approved.
