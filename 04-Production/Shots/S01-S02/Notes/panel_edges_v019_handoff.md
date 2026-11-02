# Panel edge timing fix and cylinder gap inspection — v019

Owner requested fixing the second panel's rectangle appearing before its glitch, then asked whether the cylinder has a central gap.

Current native: `../Scenes/S01-S02_production_v019.blend`. Dirtyv018review session preserved as a separate Before_panel_edges copy before saving the successor. No supplied original overwritten.

Cause: old independent acquired-row border curves retain previs visibility timing. Second border turns on371, while the current second glitch starts382. First border turns on329, overlapping its glitch322–331, so the mismatch was less apparent there. Later borders had the same obsolete timing source.

Fix:13legacy acquired-row border objects retained but disabled; copied actions have only hide-render/hide-viewport channels muted. Existing surface edges derive directly from the actual revealed tiles, so they move/reveal with the glitch instead of establishing a separate rectangular frame. Approved beam/pulse/contact/tile timing, camera and shared masters unchanged. Final-displayv018content exclusions retained.

[Change record](panel_edges_v019.json). [Checks](panel_edges_v019_verification.json): first and second panels have matching0/4/12/16visible tile faces at relative18/22/25/31frames; legacy borders remain off. Four960x540stills378/382/386/392 inspected, each under0.37seconds, all linked paths resolve. No full animation rerender.

Gap: blue measurement shell has a camera-facing viewing wedge, Enabled, half-angle30degrees (60degreeopening). At528, disabling only this modifier changes evaluated shell faces34304→41024 and closes the cut strip in diagnostic views. The physical BHA remains continuous; this is a display opening, not a disconnected tool. [Diagnostic record](gap_inspection_v019.json). The modifier was restored after the test and remains unchanged in savedv019. Recommendation: close or fade the viewing wedge during the wide shot if the shell should read as continuous. Owner asked for inspection; that additional presentation change is not included yet.

Native/video local only; no off-machine media backup claimed. Reports/scripts/selected stills synchronize separately. Owner visual approval and whole-shot acceptance remain open.
