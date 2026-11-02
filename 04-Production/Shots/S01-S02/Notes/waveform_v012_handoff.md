# Single pulse, longer leading/trailing shape

Owner reference/request: one outgoing pulse and one feedback pulse, with slightly longer head/tail. Current actual scene: `Scenes/S01-S02_production_v012.blend`. v011 retained.

All six fields: pulse count1, local Pulse width1.6 (was1), Tail allowance12 (single-pulse default7.2), Head fade1.2 (was0.8), Tail fade2.4 (was1.2). Loop off: each shot event sends one pulse and returns one reflection. The widened shape gives more time before/after its main spike; the longer train retains trailing baseline. Pre-dip, undershoot/rebound and small ringdown remain parts of one pulse, not additional train pulses. Markers retain size; head/tail length means the waveform's lead-in/trailing shape, rather than larger marker dots.

Use master style is off per field to use its approved-default local shape plus these adjustments. Sharedv017 remains unchanged for other consumers. Route, starts, colors, strand spacing,16frame travel and2frame reflection delay remain fromv011. First outgoing head316/tail328; reflection330; return head346/tail358. Existing measurement cues are still pending synchronization after waveform visual selection. Camera unchanged.

`waveform_v012_install.json` records settings and landmarks. Preview `Previews/Waveform-v012/single_pulse_v012.mp4` covers299–364 at24FPS; `waveform_v012_render.json` records representative benchmarks and full-frame export cost under strict5s. Native/media local only, no off-machine backup claimed. This is a focused visual iteration, not whole-shot acceptance.

Completed:68 full1080p export calls, maximum1.378s/frame. Preview decodes66frames/2.75seconds at24FPS with zero dropped/duplicated frames. Outgoing310 visually inspected. Live native is open at310 for review.
