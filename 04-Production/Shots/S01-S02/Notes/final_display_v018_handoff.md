# Final-display content review — v018

Owner requested that anything outside final render intent be absent from render outputs, and asked to confirm a close-up and final wide still. Current native: `../Scenes/S01-S02_production_v018.blend`. Originalv017 retained.

Correction to earlier explanation: tan rectangles are the six old `S02 geological contact wall` target proxies. They already had hide_render=True, but remained viewport-visible. GPU viewport export therefore captured them despite native render flags. The cyan point markers came from the shared fine surface display. The mismatch also exposed old history, temporary contact and section-boundary helpers:45previously render-hidden objects were still viewport-visible.

Current display policy:

- Include physical BHA/well/environment, six approved cyan/violet beam exchanges, active contact patch, tile reveal, surface lines/fill, owner-approved environment motion grids and restoredv017camera.
- Exclude previs target plates, old history/contact/boundary helpers, replaced waveform/impact graphics and decorative point markers.
- Keep shared masters unchanged. The fine-style node group is copied locally; only its point-instance branch is disconnected. The thin-line and surface-fill branches remain.

[final_render_visibility.py](../Scripts/final_render_visibility.py) enforces object and collection render flags at the exported frame. Saved per-view-layer visibility also hides excluded helpers for interactive review. Run native text `START HERE — final display` and use `final_display.export(...)` for subsequent playblast stills. The approved pixel-grid draw remains part of the export. Historical exporter versions/consumers are not silently migrated.

[Profile/native hash](final_display_v018.json). Live verification: zero render-hidden objects remain viewport-visible; all six tan proxies hidden; line-only style visible; all linked library paths resolve; no active export job. Camera/topology/signal/reveal values unchanged. Scene remains756frames/24FPS/31.5seconds.

Selected stills: close-up at335 during violet feedback/tile display, final wide756. Files `../Previews/Final-display-v018/close_final_v018.png` and `wide_final_v018.png`, each1920x1080. [Render timings](final_display_v018_selected_stills.json):0.367s and0.572s, under5seconds/frame. Both inspected. These are final-content candidates for the AI-reference Workbench pipeline, not completed AI-stylized film frames. No new full motion render; owner confirmation pending.

Native files local only; no off-machine media backup claimed. Scripts/profile/report/selected stills synchronize separately. Shared measurement ownership informed the local display choice; current scene queries establish actual object provenance and visibility.
