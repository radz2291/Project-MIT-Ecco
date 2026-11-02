# Flat lead/tail controls — v018

Versioned extension of approvedv017; source preserved. Master `Waveform_shared_v018.blend`, interface `Waveform_interface_v018.json`, reproducible builder `Scripts/build_pulse_v018.py`. Both master and per-instance Local panels expose:

- **Lead rest frames**: delays the pulse shape within its packet. Automatic train duration includes this extra blank lead. Default0 keepsv017 timing.
- **Flat after age**: above0, response after this local pulse age becomes exactly flat and ringdown is disabled. Default0 preserves the previous response. Use Tail allowance to extend the flat baseline, without broadening Pulse width.

Other controls and capacities retainv017 semantics. The v013 S01-S02 scene uses lead2, flat after6, width1, pulse count1, tail allowance12 (total train14), ringing0 and per-instance style. This is an authorized visual iteration, not a new appearance approval for all consumers. v017 remains the approved demo reference and existing consumers remain pinned. Source has the same clean2-object native structure and no runtime handlers.

Consumer: `Shots/S01-S02/Scenes/S01-S02_production_v013.blend`, six coordinated events. Hardware holds during each complete send/return, then moves. Camera and tile timing belong to that shot. The local native master is excluded media; exact SHA256 is in its interface. No remote native backup is claimed.
