# S04 v007 — bounded visual communication review

20 October 2026. Owner-authorized tests only. No full 18-second integration, finishing or client acceptance.

## Assessment and treatment

v006 already sampled the actual inner casing mesh. No separate invisible helper wall was found by name or event binding. Its animated face-material viewing window hid the physical interaction surface, and the near-sensor view compressed the sideways travel. This revision removes that presentation mechanism in the test successor and holds the section open from frame 1.

The actual approved S02 v011 native scene and existing video reference were inspected. SEND front `Frame305` and ECHO front `Frame314` shape-key coordinates, source colors and line widths were extracted. These are the source of the fine curved cyan send and finer emerald return here, adapted to the actual S04 cap-to-steel standoff. There are three fronts per packet, wall-fixed contact pixels and no diamond marker. This reuses the signal language without importing Section 2's stored-history semantics as a cement diagnostic map.

The two comparison views hold the sensor at right, steel toward center and exposed backing at left. They use the same 45 mm lens and sensor-relative transform at distinct fixed stations: X=-0.32 m supported and X=-1.50 m channel-backed. Sections, channel, cement and tool remain stationary throughout each test. Only explanatory signal/reaction visibility changes. This is a controlled comparison proof, not the final travelling camera shot.

One intentional refinement explained before execution: the primary return has identical timing in B and C. The longer channel-associated reaction persists after the return. Delaying the entire return until the reaction faded would incorrectly suggest an increased wall distance. These timings are illustrative, not a numerical acoustic acquisition model.

## Files to review

- `../Test-1_Matched-Response/Previews/S04_BC_matched-response_v007.mp4`: five-second, 24fps synchronized comparison, 1920x540. Separate B and C videos and native scenes are alongside it.
- `../Test-1_Matched-Response/Previews/S04_BC_Contact_v007.png`: equal-time contact view.
- `../Test-1_Matched-Response/Previews/S04_BC_Response-decay_v007.png`: equal-time settled-versus-persistent response.
- `../Test-2_Inner-Wear/Previews/S04_D_test_v007.mp4`: five-second, 24fps wear/reference/profile proof, 1280x720.
- `../Test-2_Inner-Wear/Previews/S04_D_Physical_v007.png` and `S04_D_Overlay_v007.png`.
- Editable natives: `../Test-1_Matched-Response/Scenes/S04_B_communication_v007.blend`, `S04_C_communication_v007.blend`; `../Test-2_Inner-Wear/Scenes/S04_D_communication_v007.blend`.

## Meaning and geometry safeguards

Steel nominal inner radius 0.1589405 m; fixed outer radius 0.1698625 m; cement outer radius 0.22225 m. No engineering rescaling. The v006 organic channel derivative is retained. Its original closed source volume is outside steel and inside the cement annulus; the test display uses a fixed sectional subset. It is not a decal, moving stream or disappearing cement.

Surface contact pixels lie on actual ray intersections with retained steel. Backing cells have fixed positions in the exposed backing coordinates and change only visibility/intensity. B is compact and short-lived; C is modestly longer axially, fragmented and slower to decay, with the same cyan visual family. There is no ray travelling through steel/cement to an unseen reflector. Cells are explanatory information, not a physical simulation, direct image, universal defect classifier or proof of a specific fluid.

The full-shell wear mesh has an angular wrap seam at the source groove. As explained before execution, the test uses the package's **existing `CASED_STEEL_WEAR_CUTAWAY` variant**, whose angular domain contains the rounded groove on both sides. The source formula is unchanged: authored maximum 4 mm, smooth axial cosine-squared taper and angular Gaussian. This is an explicit source-variant selection, not a silently remodelled or enlarged defect. Every retained display vertex is an exact source coordinate; no displacement/modifiers, fixed outside radius. The actual sampled center recess is approximately 3.976 mm due to mesh sampling.

Wear is shown first with no graphics, then a fine dashed original-inner contour, then the current cyan contour and a small reference-to-current bracket connected to sensor-to-wall distance. No thickness value or calibrated field wear depth is rendered. Travel-time distance interpretation requires fluid-velocity correction and tool-position/eccentricity treatment. The provisional temporary sensor cap is a graphical emission exit, not a certified transducer datum.

Plausibility reference: [IPA, Determining drill pipe wear inside casing using ultra sonic measurements (1996)](https://www.ipa.or.id/id/publications/determining-drill-pipe-wear-inside-casing-using-ultra-sonic-measurements) describes localized grooves from tool-joint contact and notes they need not lie on the low side. Its instrument-specific thickness method and capabilities are not transferred to ECCO. Package interface: `04-Production/Shared/Assets/CasedHole/README_v002.md` and its native build formula remain the actual geometry authority.

## Self-review and limits

1. Sensor, steel and backing are distinguishable in the matched close view, but full ECCO recognition and the larger pipe/layer context still depend on the future A establishing view. This proof intentionally holds a close composition.
2. The fine fronts travel sideways between the actual sensor exit and visible steel. Native ray and display visibility checks pass.
3. B/C share the same mechanism, packet scale, framing and timing. Sensor-relative camera difference is below 0.000001 m.
4. Equal-time response decay is visibly different in sampled frames. Normal-speed owner review remains necessary; this is not an independent audience-comprehension result.
5. Fixed geometry and moving/fading cyan/emerald explanatory effects are separate. The channel is present from frame 1, never animated into existence.
6. **Wear physical discovery remains the weakest result.** At true shallow depth, simple Workbench shading makes the unmarked recess subtle. The original/current overlay communicates the difference more clearly than the physical-only image. Do not claim this criterion fully resolved and do not deepen the feature to obtain approval.
7. The profile relationship is registered to actual geometry, with the outer steel fixed. It is not a wall-thickness or field-calibration claim.
8. The S02 signal family is retained; these static comparison proofs do not validate the final continuous camera journey. No full integration is released by this report.

Recommendation: review B/C in motion and approve or adjust their response contrast first. For D, review whether the physical discovery needs a different light/composition proof before integration. Geometry should remain unchanged.

## Verification and performance evidence

`verification.json` records fresh-open library resolution, native hashes, retained-source vertex checks, stationary camera/control, actual contact visibility, channel-volume bounds and source hashes. `native-B/C/D.json` preserve complete native event provenance. `wear-relationship.json` records the registered profile intersection. `benchmark-*.json` records representative pre-batch checks; `timings-*.json` records all delivered frames; `media-verification.json` records totals, encodes and complete video decoding.

Preview rendering is Workbench/FXAA, Section 2-style material colors and simple studio lighting. Startup/loading, setup, benchmarks and encoding are separate from per-frame render totals. Exact batch totals are in `media-verification.json`. This is inexpensive previs, not a realistic final finish. Sampled chronological frames were inspected; no claim of watching every frame at normal speed or testing with an independent viewer.

Delivered render batches (120 frames each): B 57.374 s total / 0.478 s mean / 1.590 s maximum; C 74.339 s / 0.619 s / 2.090 s; D 75.496 s / 0.629 s / 2.115 s. Total frame rendering 207.209 s (3 min 27.2 s), excluding setup, scene startup, benchmarks, image annotation and encoding. Every delivered frame was strictly below 5 seconds; the mean meets the approximate one-second iteration target.

Original v006, S02 and shared masters are preserved. Current unsaved Blender UI was not replaced. Natives, videos, raw frames and private inspection data stay local; repository synchronization is not a native-media backup. Previous versions and proofs remain intact.
