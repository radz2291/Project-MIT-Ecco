# B201 — client-readiness refinement v006

New consumer of accepted Motion_v005; prior scene, preview, source masters and approvals preserved. Human acceptance of this revision is pending.

- Editable local scene: `Scenes/B201_pulse-echo_refinement_v006.blend`.
- Playable local proof: `Previews/Motion_v006/B201_pulse-echo_refinement_v006.mp4`.
- [Review report](../../Records/Tasks/T-007/report.md), [direction](direction.md), [build](Scripts/build_motion_preview_v006.py), [saved-scene verification](Scripts/verify_motion_preview_v006.py), [render](Scripts/render_motion_preview_v006.py), [encode/review packaging](Scripts/package_motion_preview_v006.py).

10 seconds,240 frames,24fps,960×540, silent. First pulse emit/contact/receive12/36/60, then150/163/176 and198/210/222. Whole-product rotation0/6/12 degrees. One clear measurement is followed by two shorter acquisitions. No B202 accumulation or reconstructed image.

Each cyan front propagates at constant speed to the wall and fades over two frames after its own arrival. The emerald return starts at the actual source-wall intersection and reaches the same physical cap. The contact cue uses42% of each prior footprint radius and48% opacity, disappears within10frames, and leaves no lasting grid.

The native `B201 timing editorial` view layer composites above the source mechanism. Packed Segoe UI, camera-facing type/curves and two conceptual peaks remain editable. `B201_MOTION_CONTROL` has `wall_stop_0..2`, `panel`, `graphic`, `sent_graphic`, `echo_graphic`, `interval_graphic` in addition to the inherited transmit/receive/fade controls. Native keys and driver nodes require no runtime handler. The first event's return peak and interval enter after its reception and fade before later acquisitions. This minimal study does not reinstate old Still05.

Use the saved compositing setup and both enabled view layers; do not render only the mechanism layer and omit the timing cue. Product geometry is an exact evaluated baseline consumer. Relative linked ECCO library and local T5/T6 masters must remain available. Version/reverify replacements. The builder refuses to overwrite an existing candidate. `package_motion_preview_v006.py` uses Pillow,NumPy and imageio-ffmpeg; this execution retained imageio-ffmpeg0.6.0 in ignored `Cache/python/`.

Timing, membrane shapes, contact light and signal peaks are illustrative. There is no measured signal, physical speed/RPM, numeric TOF, radius derivation, full-wave simulation or instantaneous rock image. Actual ENP3 face datum, mud-velocity calibration and MIT technical acceptance remain unresolved. Human cold-viewer comprehension also remains pending; a scene test cannot establish it.

Blender/MP4/raw frames/cache are organized local-only and ignored by Git. Scripts, text/JSON evidence and selected permitted review images are synchronized for review; this does not back up heavy media. Internal layout/depth/type tests remain labeled scene variants and are not review candidates.
