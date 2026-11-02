# ECCO-057 — transmitter focus investigation only

Recommendation: render hardware/signal and transparent measurement as separate color/alpha layers, using the same camera and focus plane. Apply camera depth of field within each layer before compositing. A matched one-frame test now keeps the signal sharp through the blue measurement layer. This is a feasible direction, not an approved film integration or completed animation treatment.

## Findings

1. Focus placement is correct. At386 the120mm camera's transmitter focus depth is0.258768m. A raycast with measurement and waveform excluded hits the actual `TEMP | Imaging port 2 | removable acoustic cap` at0.258753m: a15micrometre difference. The camera's ray points at the intended transmitter face.
2. Workbench applies its depth blur to the combined color and scene-depth buffers. A transparent foreground surface can therefore influence the blur of hardware already visible through it. This interpretation agrees with the observed full-layer versus isolated-layer comparison and [Blender's Workbench DOF implementation](https://raw.githubusercontent.com/blender/blender/main/source/blender/draw/engines/workbench/workbench_effect_dof.cc). That source is upstream main, supporting the architecture; the installed5.2.2 behavior was tested locally. [Blender's pass documentation](https://docs.blender.org/manual/en/latest/render/layers/passes.html) also distinguishes image/depth passes from transparency-capable masking; a single flattened depth image cannot encode every overlapping transparent layer.
3. Earlier native-render isolation was incomplete. Existing `hide_render`/`hide_viewport` animation resets manual visibility during render evaluation. Merely hiding the measurement in the viewport did not remove its rendered fill. For this disposable still, visibility animation was frozen and hidden legacy geometry suppressed. No visibility curves were muted in production.
4. The transmitter remains the focus in the isolated hardware pass. Adding the transparent measurement directly makes the signal/body beneath it softer. Rendering that measurement separately produces valid fractional alpha (215191 fractional-alpha pixels at960×540, sample alpha0.298), so it can be composited without covering the signal with an opaque rectangle.

## Successful bounded test

Source frame386,960×540, Workbench,120mm lens, f/64 for BOTH layers, same transmitter focus. `separate_base.png` rendered in0.986s; `separate_measurement.png` in0.449s; combined1.435s for the two passes. Composite: `Previews/DOF-investigation-v002/separate_composite.png`. Source/target relationships and beam remain unmodified. The blur varies with actual layer depth; equal-distance portions of the wall appropriately stay relatively sharp. This is a layered depth-of-field approximation, not a ray-traced optical simulation. Color compositing here is a PNG/FFmpeg feasibility proof; final integration should use consistent scene-linear color and correct premultiplied-alpha handling.

Reproduction: open local `Scenes/S01-S02_DOF_investigation_v002.blend`, run `Scripts/reproduce_dof_layers_v002.py`, then composite base and measurement with alpha-over. This proof has visibility frozen at386 and is NOT an animation scene. Raw diagnostics/timings: `dof_investigation_v002.json`.

## Proper integration design, not executed

- Keep focus attached to the physical transmitter, with shallow focus during the close-up and progressively deeper focus during pullback. Retain the approved camera path and reveal timing.
- Use named render collections/view-layer exclusions or an equivalent explicit visibility policy. Avoid per-frame hide flags fighting existing animation. Preserve existing final-display cleanup.
- Render hardware plus waveform independently from the translucent wall/grid. If near and far sides overlap and still produce blur halos, split the measurement into near/far camera-relative depth layers, then composite in depth order. A single global blur of the completed image is insufficient.
- Use fractional-alpha color passes and camera-derived depth for every participating layer; handle premultiplication and color transforms consistently. Current GPU pixel guides are drawn after the viewport color pass, so they must be assigned an appropriate layer/depth or restricted to the deep-focus portion; a native-render swap alone would drop them.
- Expose focus target/offset, aperture, enable, and pullback blend controls. Test one complete pulse/reveal exchange plus the start of pullback for alpha halos, pulse legibility and stable blur. Benchmark the COMBINED passes/composite at1080p against the strict<5s/frame limit. The960×540 still does not establish1080p or animation performance.
- EEVEE is an alternative material/render conversion requiring separate compatibility and timing checks. Cycles could supply lens-sampled transparency/DOF but has no demonstrated budget compliance here; it is not the default recommendation.

Investigation ends here as requested. No production/shared asset edits, no full rerender. Productionv026 and its31.5s video remain authoritative. Native test/media local only; report/scripts/selected evidence may be synchronized. Owner creative acceptance and animation readiness are still open.
