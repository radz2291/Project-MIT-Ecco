# Amplitude breathing — sharedv020

Optional extension to v019's persistent beam. Master `Waveform_shared_v020.blend`; builder `Scripts/build_pulse_v020.py`; interface `Waveform_interface_v020.json`. New local timing controls:

- **Amplitude breath**, default0: fractional strength of smooth pulse-height variation. Zero retainsv019's shape exactly; production uses0.32.
- **Breath period frames**, default48: duration of a complete height rise/fall in reference frames. Each outgoing/feedback phase starts its own smooth modulation. Height multiplier is `1 + amount*sin(2π*phaseTime/period)`.

All other v019/flat-tail controls remain. A phase-comparison tolerance was made large enough to switch feedback correctly at larger reference-frame values. v020 with breathing0 gives the same default geometry asv019; source versions remain intact. Beam mode/Both/one-shot is the tested production configuration. Arbitrary alternative modes/FPS/fit/loops still require targeted checks.

Consumer: `Shots/S01-S02/Scenes/S01-S02_production_v015.blend`, six6second exchanges. Opening5frames/setup8, travel30,10frame reflection delay, response20, closing5, pulse width1. Tile material/geometry and camera pacing belong to the shot. Existing other consumers remain pinned. Native source local-only; SHA256 in interface; no off-machine backup claimed. Appearance awaits Radzi's review.
