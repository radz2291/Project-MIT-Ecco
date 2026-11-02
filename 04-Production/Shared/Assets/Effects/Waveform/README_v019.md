# Persistent handshake beam — v019

Owner-requested extension: beam establishes the connection first; a pulse is the message moving along the connected line. Cyan outgoing, violet feedback. No pulse markers or independent packet clipping in Beam mode. Previous masters remain intact.

Native `Waveform_shared_v019.blend`; builder `Scripts/build_pulse_v019.py`; interface `Waveform_interface_v019.json`. Four local timing controls:

- **Beam mode** default false: true selects continuous connected line instead of finite packets. False preservesv018 coordinates exactly (verified).
- **Beam opening frames** default1: quick straight connection growth.
- **Beam setup frames** default3: opening plus quiet handshake before the pulse clock starts; keep this longer than opening.
- **Beam closing frames** default1: retracts line only after complete exchange.

Production consumer v014 uses Both directions, one-shot, speed1,6frame pulse travel,10frame response window,2frame feedback delay, pulse count1, width1, no ringing and no markers. The beam stays attached to both surfaces while the pulse deforms it. Full line is cyan through outgoing stage, then violet through feedback. It is not two simultaneous overlaid beams. Travel duration is an illustrative readable screen timing, not a calibrated acoustic measurement.

Beam mode is checked for the Both-direction configuration used here. Other direction/FPS/fit/loop combinations require targeted consumer review. Source remains clean2objects/3native node groups, no runtime Python. New native source is local-only with hash in interface; no off-machine backup claimed. v017 remains the appearance-approved demo reference; v019 is the current owner-authorized beam iteration, pending visual acceptance.
