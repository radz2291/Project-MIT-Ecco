# Exact approved demo settings in actual scene

Radzi requested the demo configuration rather than fitting it into the old short signal windows. `Scenes/S01-S02_production_v011.blend` preservesv010 and uses the approvedv017 demo settings on all six signals. Only shot start frames and placement differ. Shared style/shape/colors/strand spacing remain inherited, all quick multipliers1, no count/separation override. Camera unchanged.

Speed1, travel16, automatic train20, reflection after complete tail with2frame delay, equal return travel/train, Follow scene FPS on, Loop on with96frame period. First event: send300, head reaches316, tail reaches336, reflection begins338, return head354, return tail374, next send396. This is the demo's duration without compression, rather than v010's3-frame train/Speed6.667.

**Visual timing trial:** the old measurement/contact cues remain where they were and are no longer synchronized with the longer pulses. Multiple field events can overlap, and loops repeat. These consequences are intentional for this comparison; once the waveform motion is selected, coordinate the measurement/event choreography separately. No old-window adaptation is hidden inside the shared asset.

Native version and per-event landmarks: `waveform_v011_install.json`. Render proof: `Previews/Waveform-v011/demo_settings_v011.mp4`, frames299–395 at24FPS. `waveform_v011_render.json` records two benchmark frames and97-frame export with strict<5s/full frame. Waveform plays natively; the scene's separate pixel guide overlay uses its START HERE helper.

All retained native/media remain local-only. Whole-shot acceptance remains open. v010 preserves the earlier compressed integration; v011 is the current owner-requested comparison.

Completed proof:99 full1080p exports, maximum1.338s/frame. Encoded97frames/4.042seconds at24FPS, decode passes with zero dropped/duplicated frames. All six fields' timing inputs were compared against the shared demo defaults: exact except intentional Start frame offsets. Outgoing313 visually inspected. Native open in Blender for review.
