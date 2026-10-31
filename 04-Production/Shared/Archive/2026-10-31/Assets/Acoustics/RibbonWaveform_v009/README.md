# Ribbon waveform v009 — sensor-sized filament proof

Proof only; owner presentation choice remains pending. v007 is preserved byte-for-byte as a liked pressure-field alternative; v008 is retained as the denser diagnostic ribbon.

V009 uses 32 static fine filaments. The assumed normalized pulse CSV from PressureField_v005 drives an artistic height profile. Each strand has a fixed sample offset (up to ±0.14 of the pulse), amplitude fan (0.3–1), and depth position. Positive and negative peaks are normalized separately to ±20.0195 mm; endpoints remain at zero. This is a deliberate display warp, not faithful multichannel data, measured ECCO signal, fluid displacement, or a new wave simulation.

Size comes from the evaluated linked `TEMP | Imaging port 2 | removable acoustic cap`: full height40.039 mm and transverse width40.000 mm. The cap is provisional scene geometry, not a certified hardware measurement. The preserved route is24.576 mm long. This makes the ribbon wider and taller than the gap; it does not match the long aspect ratio of the reference images. The context still proves the requested sensor-face scale under the original CAM_S01_Continuous camera. Part of the outer fan approaches the upper image edge under that camera; no camera reframing was imposed.

Shader highlight runs outward300–309 and returns309–318 at half gain. The baseline stays visible. Geometry, object transforms, phase and vertex coordinates remain fixed. Seven saved-file frame comparisons pass identical geometry+matrix hashes with varying shader head/gain. Cyan/violet are artistic layer colors, not pressure signs or measured values.

Rendering: context640×360/Eevee16; isolated960×540/Eevee32, optical Fog Glow. Context2.349 seconds; polished isolated benchmark2.108 seconds, full render-to-file. Final isolated source collections excluded, late324 clean. Motion uses79 samples across native298–324 at1/3-frame increments,24fps =3.292seconds,3× slow review. Dark-stage camera is a separate proof camera; source context camera unchanged. Native sources remain local; no remote heavy-media backup is claimed.

Source sample: ../PressureField_v005/Data/source_pulse.csv and its metadata. Build and verification scripts plus evidence reside in Records/Tasks/T-056. All older proofs and supplied source files remain intact.

