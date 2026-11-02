# Connection beam → cyan message → violet feedback → close → turn

Current actual scene `Scenes/S01-S02_production_v014.blend`, sharedv019. User changed the meaning: beam controls connection lifetime; pulse indicates message transfer. There is no independent head/tail on the pulse. All six cap-to-Earth paths and held BHA poses are retained fromv013. Camera remains the25second v013 timing.

First cycle: beam starts300, fully connects301; quiet straight connection301–302; pulse clock begins303; tile impact311; violet feedback begins321; returning pulse peak reaches cap about329; complete response337; beam closes338; BHA begins next turn342. Other events start348/396/444/492/540 and use the same offsets. Beam closes before rotation and next target. Old impact circles remain hidden. Pulse width1, count1, no ringing, no dots; cyan send and violet return use distinct shared materials.

Evidence: `waveform_v014_install.json`, `waveform_v014_verification.json`, render log `waveform_v014_render.json`. Verification checks every integer frame299–343: no output before opening/after closure; full route endpoints connected301–337; straight handshake301–302 and final resting line337; pulse motion present; cyan component1 before feedback, violet component2 after; no marker components. v019 beam-off coordinates exactly matchv018, and saved links reopen correctly.

Migration initially crashed live Blender twice. Likely cause: retaining RNA vector-array references across node-group replacement. Installer now copies vector/color values to plain tuples before replacement. Background build then saved/reopened and passed checks without crash; dirty user session was preserved before opening tested native. No claim that this fixes unrelated Blender/GPU crashes.

Preview `Previews/Waveform-v014/beam_exchange_v014.mp4`,299–348 at24FPS. Working1080p exporter benchmarks before the short batch, strict full-frame<5s cap. Native and media local-only. This is a focused visual checkpoint; whole-ticket acceptance remains open.

Completed:53 full1080p export calls, max0.814s;50-frame2.083second movie decodes with zero dropped/duplicated frames. Handshake302 and violet feedback330 visually inspected. Tested native opened in live Blender successfully and full proof exported without another crash after the input-copy fix. Prior dirty user session preserved as `Session_before_beam_preview_1793619654.blend`. Latest scene is open for review.
