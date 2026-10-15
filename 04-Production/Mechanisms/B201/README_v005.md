# B201 — Pulse, echo and waveform proof v005

16 October 2026. Standalone B2 proof for T7 / Radzi review, using accepted T5 plugged v002 and T6 well/assembly v003. This is a mechanism demonstration, not a final S02 shot or engineering approval.

- [Moving preview](Previews/B201_pulse-echo_v005.mp4): 18 seconds, 432 frames, 24fps, 1280×720, silent H.264.
- [Editable scene](Scenes/B201_pulse-echo_v005.blend), [builder](Scripts/build_proof_v005.py), [graphic/encoding source](Scripts/package_preview_v005.py), [verification](Scripts/verify_proof_v005.py).
- [Report](../../Records/Tasks/T-007/report.md), [technical questions](../../Records/Tasks/T-007/review-questions_v005.md), [proof register](../../Records/Tasks/T-007/proof-register_v005.md).

The first three pings produce isolated brief wall spots. The next three reveal schematic transmit and echo traces on a common time axis. The same emitting sensor receives every return. Equal outbound/return durations are slowed for inspection; the diagram's common authoring speed is not a physical sound speed. Peak heights stay constant and have no geometric meaning. Stand-off requires mud sound-speed correction; axis radius also needs the physical sensor offset and eccentricity corrections.

The entire assembly control rotates between held acquisition stations. Step-and-hold pacing isolates cause and effect; it is not a claim about continuous drilling, direction, RPM or firing schedule. Only sensor 01 emits here; all three source references remain in the linked product at 120° spacing. Full circumference/depth reconstruction belongs to B202 and later shot work.

T6's irregular full wall is sampled at world X=2.8m (an authoring coordinate, not well depth). ECCO is translated +2.07m so its inherited X=.73m sensor plane meets that section. Wall contour and distances are derived from that authored illustrative profile, not field measurements. Camera looks along +X; view orientation does not establish surface-to-bottom drilling direction.

The display is an exact plane/mesh contour of accepted plugged geometry, with separate consumer-only section curves. It does not invent an acoustic transducer or validated internals. Effects start 0.4mm outside the ray-inspected temporary cap along the inherited sensor reference; this small clearance is an authoring parameter. The actual acoustic face, mud-sensor datum, time-zero and instrument processing remain unverified. Recheck those if an affected claim is retained or hardware changes.

T5 remains externally linked by a relative path. T6 is appended as a local controllable consumer; the visible wall curve is its evaluated section. No shared master is modified. Adjusting the well or sensor configuration requires rebuilding a new version and reverifying the paths; the sampled effects do not automatically recalibrate to edited geometry. Rotation uses `ASSEMBLY_CONTROL.rotation_rad`; the waveform graphics are editable in the accompanying packaging script and derived from the saved event record. No persistent Python handler or auto-run script is required to open/play the Blender source.

Reproduction: run the builder in isolated background Blender 5.2.2 with `--render`, fresh-open the saved scene with the verification script, then run the packaging and motion-sheet scripts in Python with Pillow and imageio-ffmpeg. The builder refuses to overwrite the candidate. Existing v001–v004 scenes/scripts/logs are diagnostic history, not review candidates. Binaries, MP4 and bulk frames remain organized locally and ignored by Git; only selected stills, scripts and records are synchronized.
