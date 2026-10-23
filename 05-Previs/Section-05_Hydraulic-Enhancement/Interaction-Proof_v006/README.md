# S05 v006 — One-pad interaction study

The camera holds while a connected amber passage carries a few rock fragments upward around a rotating twisted pad. This is a three-second composition test for owner review. Full Section 5 integration and finishing remain unreleased.

## Review files

- `Previews/S05_focused-interaction_v006.mp4` — 72 frames, 24 fps, 1280 × 720, three seconds.
- `Previews/composition.png` — representative frame 36, matching the motion proof.
- `Scenes/S05_focused-interaction_v006.blend` — editable candidate, reopened in Blender at frame 36.
- `Previews/review.html` — local looping player and chronological review sheet.

## What changed

The view is wider than v005 and held still throughout. The tool runs diagonally across the frame, exposing the selected passage before and after the prominent pad. The camera looks from a new azimuth, so the bend is visible beside that pad. Neighbouring hardware remains as context. The fixed half-section is rotated 25 degrees around the axis to face the camera; its dimensions, inner radius, and physical wall are unchanged. There is no animated cutaway.

The eighteen-path presentation is hidden in this successor. One route from v004's geometry-derived route family is retained and expanded into a finite, closed fluid volume. Its mottled amber density moves upward, keeping the overall approach, bend and exit connected. This is a visualization of selected fluid, not a separate gas, a free fluid surface, or a material coating. Five irregular matte cuttings enter, traverse and leave this same route at staggered times; not all five are visible simultaneously. No persistent guide curves, sparks or annotations carry the explanation.

## How rotation affects the illustration

The original ten connected hardware wrappers continue their common clockwise rotation, viewed from the surface looking downhole. The authored rate remains 5 degrees per second, slowed for readability and not an operating-RPM claim. There is no axial tool translation.

The selected route follows the source pad's measured open passage. Its angular position receives a spatially varying fraction of the tool's rotation (32–75%); its radial position and finite cross-section are fitted to the actual rotating steel. Upward density motion and cutting transport continue independently. The fluid objects have no hardware parent. Thus the selected passage changes around the moving pad rather than spinning as painted lines on its surface.

This is authored, geometry-aware kinematics. The amber density is explanatory shading, not a calculated fluid-density field. It does not solve pressure, viscosity, turbulence, conservation or hydraulic performance. The earlier ENP3 functional-stage/end-identity limitations remain; no new engineering validation is implied.

## Verification

- Full effect-versus-hardware triangle checks at all 72 output frames and 71 halfway points: no intersections.
- All effect vertices checked against the analytic cylindrical wall and radial first-hit steel boundary at those times: positive clearance.
- Minimum sampled distance to steel: 7.396 mm; minimum wall clearance: 3.500 mm. These are visualization clearances, not operating specifications.
- Hardware remains rigidly connected, with unchanged source mesh data and borehole radii. Static tool-to-wall minimum gap remains 3.175 mm.
- Camera matrix remains constant. Actual root rotation runs from 0 to -14.792 degrees over sampled frames 1–72.
- All 72 encoded frames decoded successfully. Render/write mean 0.647 seconds; maximum 1.080 seconds. Representative benchmark frames were also below the strict five-second cap.
- Native reopened with its relative ECCO master link resolving. Previous v004 and v005 hashes match the retained baselines; v001–v005 all remain present. Shared source hash remains unchanged.

The checks are discrete geometric tests, not proof at every continuous instant or CFD validation. The agent inspected the static frame and twelve chronological decoded frames. Whether the interaction reads immediately at normal playback speed remains the owner's review decision. In particular, the soft amber volume treatment is still an experiment; technical clearance does not establish its visual success.

## Files and preservation

Root: `C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/05-Previs/Section-05_Hydraulic-Enhancement/Interaction-Proof_v006/`.

Linked master: `04-Production/Shared/Assets/ECCO/ECCO_film_v002.blend`, SHA-256 `df656a5c4bc48f081a4b6365c7969df55d15c7da53ddb96be20875e931d26584`.

Native SHA-256: `dd73a973be899906b7cb52c1724b2390202f192a64c809d0487e5698d052c91e`.

MP4 SHA-256: `6a53883e1f473adb670a804b172ef946b7f0828c8cba134ee04ef025e5efaec3`.

The `Scripts/` directory records build, intersection verification, render and packaging. Build uses v005 plus v004's planned routes and refuses to overwrite an existing built candidate. `Records/` contains timings, geometry results, preservation hashes and native/media verification. Native, video and raw frames remain local; only scoped text records, scripts and selected review stills are published. See `Records/sync-verification.json` for publication and local backup evidence.

**Stage 6: limited proof ready for review. No complete 18-second build.**
