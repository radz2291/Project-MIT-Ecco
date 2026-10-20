# S04 B/C v008 — solid sections and casing-bound resonance

21 October 2026. **Bounded matched-composition and short-response proof for owner review. Part D paused. No full18-second integration or finishing.**

## What this proof asks

Can the rendered image show a recognizable tool/sensor, internal fluid gap, actual steel wall and different exterior backing, while keeping the response visibly attached to the casing? The owner agreed to this treatment after rejecting v007's hollow-looking sections, hidden backing difference and detached pixels. The earlier narrative, engineering dimensions, distinct stations and matched-comparison principle remain in force.

## What changed

- Static planar section passes essentially through the sensing plane (50 micrometre display offset). New intersections and closed cut faces expose the occupied steel/cement/channel volumes; the world does not open or close during playback. The old face-deletion method left uncapped edges and is not reused.
- Original local v006 cement/organic-channel geometry and canonical `CASED_STEEL_WEAR_CUTAWAY` supply the surfaces. Supported sensor station remains X=-0.32 m; channel station X=-1.50 m. Original dimensions and retained source coordinates are preserved; no new wear, exaggerated gap or shifted interface.
- Solid tan cement, darker grey steel, pale internal fluid tint and restrained cyan exterior-channel volume separate the layers. ECCO remains the actual linked assembly. The exterior fluid volume is stationary, outside the steel and inside the cement annulus; no stream, decal or disappearing cement.
- The internal fluid tint is a limited visibility volume within the gap near the sensor. Its inner radial display bound follows the provisional cap exit (approximately0.131 m), not a newly asserted tool dimension or physical fluid boundary. It does not change the casing or sensor-to-wall distance. This is a simple preview treatment, not realistic final fluid shading.
- Same sensor-relative 46 mm camera at both stations. A more side-facing view exposes the closed steel thickness and a separate visible gap to the sensor. No orbit, travelling camera or full-scene continuity redesign is included.
- Floating backing cells, contact cubes and front sample cubes are removed. The existing S02 fan-shaped cyan sends and finer emerald primary returns remain. The response is a smooth fading brightness band on the actual inner steel and its exposed section face, within the existing wall thickness. No casing deformation.
- Main send/contact/receive anchors remain0.6/1.2/1.8s in both cases. The supported band decays quickly. The channel-associated band persists longer, with restrained later return fronts. The first echo is not delayed until the ringing stops. All timing, brightness and visible bands are slowed illustrative communication, not simulated ultrasonic frequencies or calibrated data.

## Physics and limits

A pulse travels through the internal fluid to the inner casing interface. There is an initial reflection, while energy entering the steel can produce repeated reflections/resonance. The material and coupling outside steel influence the decay. The image therefore compares casing ring-down, not arbitrary glowing penetration into distant cement.

This general basis is supported by [SLB Oilfield Review, casing inspection explanation](https://www.slb.com/-/media/files/oilfield-review/2-casing-corr-2-english). [SLB Isolation Scanner](https://www.slb.com/products-and-services/innovating-in-oil-and-gas/well-construction/well-cementing/cement-evaluation/isolation-scanner) describes limitations of conventional pulse-echo interpretation when cement/fluid acoustic contrasts are small. These sources establish a general principle, not ECCO-specific performance or certification. The local CasedHole_v002 interface remains the geometry source.

No cement penetration distance, quantitative bond strength, material classification, wall thickness or measured defect size is inferred from these graphics. A longer-looking response alone is not proof of a particular fluid or defect. No pulse is drawn travelling to a hidden formation reflector and returning as the primary casing echo. The backing volumes are illustrative physical context, not a direct photograph or reconstructed acoustic image behind steel.

## Review files

- `../Previews/S04_BC_matched-resonance_v008.mp4`: synchronized five-second B/C comparison. Each physical image1280x720; caption bars added outside that image, pair2560x820,24fps.
- `../Previews/S04_B_capped-resonance_v008.mp4`, `S04_C_capped-resonance_v008.mp4`: individual five-second tests.
- `../Previews/S04_BC_send_unlabelled_v008.png`, `S04_BC_contact_unlabelled_v008.png`, `S04_BC_decay_unlabelled_v008.png`: exact delivered frames25/32/55 with no explanatory labels.
- `../Previews/S04_B_material-guide_v008.png`, `S04_C_material-guide_v008.png`: same native camera, materials and frame25 as the video, with guide labels only. No alternate fluid geometry, opacity or camera introduced for the guide.
- `../Scenes/S04_B_capped-resonance_v008.blend`, `S04_C_capped-resonance_v008.blend`: editable native candidates. D is not included.

## Self-review

The tan/cyan backing conditions are now different in the actual video, not only in a clarification image. Steel and cement have closed visible section faces. The wavefronts occupy the internal gap; the bright response is fixed to the steel. Equal-time decay frames show a settled supported case and a remaining channel-associated response. These observations come from sampled chronological frames, not an independent audience test.

The close view shows the ECCO barrel and side port, not the whole2.4 m tool. Full product recognition and the larger well context still belong to A. Owner review must decide whether the close composition and the restrained response difference read clearly at normal speed. The exterior fluid remains a cyan preview representation; final realistic fluid material is not established. No human, client or engineering approval is self-declared.

## Technical verification and presentation correction

`verification.json` records manifold closures, maximum retained-source-coordinate error, fixed camera/tool/solids, relative library resolution, full120-frame native wall/cap clearance samples, source hashes and camera matching. `build-B/C.json` retain complete native event provenance and section details. Original nominal ID/OD and exterior channel relationship are unchanged.

An initial transparent Workbench batch showed stripes despite the channel and cement surfaces being separated along the inspection ray. A same-frame backface-culling test removed the artifact without changing geometry. The delivered scene uses backface culling consistently in B/C, including labelled guides. `cap-overlap.json` and `culling-test.log` preserve that investigation. Source meshes remain closed; this is a visibility setting, not a new missing wall or animated opening.

Final representative frames were benchmarked before batch. All delivered per-frame timings, final render totals and complete three-video decode results are in `media-verification.json` and `timings-B/C.json`. Earlier draft frame rendering cost92.556 s in total and is separately recorded in `superseded-transparency-batch.json`; it is not the delivered render cost. Setup, loads, benchmarks, annotation renders and encoding are excluded from frame-only totals. No claim of a complete session wall-clock total.

Final delivered B:120 frames,42.998 s total,0.358 s mean,1.078 s maximum. C:120 frames,44.329 s total,0.369 s mean,0.971 s maximum. Combined final frame rendering87.327 s (1 min27.3 s). Every delivered frame is below the five-second cap; both means meet the approximate one-second iteration target. Three MP4s decoded completely. Final frames1/25/32/55/78 were sampled for physical context, send, contact and decay; this is not a claim of an independent normal-speed audience test.

The used rendering helpers and exact S02 fan-shape data are copied locally into `Scripts/proof_helpers.py` and `Data/Section2-front-shapes.json`, with provenance recorded in `helper-provenance.json`. Rebuilding uses the preserved v006 native baseline and canonical shared masters; it does not require running a v007 script. Native playback needs neither helper script nor Python handlers.

Previous v006/v007 scenes, S02 and canonical masters are preserved. The current unsaved Blender inspection session was queried but not replaced. Natives, videos and raw frames remain local. Git synchronization of reports/scripts is not a native-media backup. Review these tests before any full-section integration.
