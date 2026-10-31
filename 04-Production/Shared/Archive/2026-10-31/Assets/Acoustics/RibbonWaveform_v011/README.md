# Ribbon formation v011 — actual geometry-motion proof

Owner asked for a full animated example in which the waveform forms, rather than light shining over an already complete shape. This separate proof preserves v007 and v010 and changes local vertex heights over a fixed route.

Seventeen local shape-key controls progressively grow the32-filament v010 profile from near sensor to wall. The near region starts earlier; the far region remains flat initially. The full crest is followed by settling, then a weaker response that develops from the wall end toward the sensor and decays fully. Object transforms, route endpoints, horizontal route coordinates and transverse width remain anchored. The first and last evaluated geometry hashes match; intermediate geometry hashes differ. At frame25, height factor nearu=.25 is0.926 while faru=.85 is0. Frame50 reaches full height. Frame120 is flat again.

This is a five-second artistic height-field animation. It reuses the v010 modeled400kHz sample window2.5–5us as shape reference; it is not an actual measured ECCO waveform, pressure-particle displacement, or physical propagation simulation. Full profile height is40.039mm plus64micrometers filament thickness, and width40mm: derived from the provisional scene sensor cap, not certified hardware dimensions. Echo height coefficient0.52 is a visual parameter. Cinematic frame timing is independent from the microsecond source sample window.

Timeline at24fps: frames1–120. Local outgoing onset8+28u and12frame rise; full crest about48–54; settle54–70. Return onset65+20(1-u),9frame rise, declining/oscillating local height then final decay105–120. Simple overall exposure follows activity; no traveling-light spotlight drives the result.

Context is an explicitly frozen native305 review tableau using the wider review camera, so the five-second formation is easy to see beside the oval sensor. The original CAM_S01_Continuous action remains in the separate context native, but this proof does not replace the locked shot camera or timing. Isolated stage excludes all source collections; only the waveform and review camera render. Source v007/v010 files remain unchanged.

Files: S02_ribbon-formation-review_v011.blend and Ribbon_formation-dark_v011.blend, locally retained with relative library paths. First full render benchmarks: context3.254s at640x360/Eevee16; isolated flat/growing/full0.328/0.360/0.448s at960x540/Eevee32. Owner acceptance and completed reusable controls/variants/consumer migration remain pending.
