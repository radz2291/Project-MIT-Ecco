# S05 v007 — Filled annular fluid proof

The amber fluid now fills the visible space around ENP3. Three matte fragments move upward through it and around the prominent pad. The v006 camera, linked ENP3 geometry, clockwise connected rotation and borehole dimensions are preserved.

**Status: three-second representation proof ready for owner review. Full 18-second integration remains unreleased.**

## Review

- `Previews/fluid-treatment_still.png` — representative frame 36, matching the final motion treatment.
- `Previews/S05_fluid-volume_v007.mp4` — 72 frames, 24 fps, 1280 × 720.
- `Scenes/S05_fluid-volume_v007.blend` — editable source, reopened at frame 36.
- `Previews/review.html` — local video player and chronological review sheet.

## Representation change

v006's narrow fluid tube is hidden. v007 uses a closed, finite annular volume between the actual steel exterior and the nominal borehole radius. The volume extends beyond the frame so artificial end caps do not dominate the picture. A lightly shaded transparent boundary and amber volume shading make the occupied space visible. This boundary is an explanatory sectional presentation, not an additional physical sleeve or a free liquid surface.

The static treatment was built and inspected before motion. An initially opaque candidate obscured the steel and fragments; reduced opacity, end boundaries outside the frame, and blended transparency improved separation. The agent judged the static relationship sufficient to proceed with the requested limited motion test. This is not owner acceptance or independent audience testing.

Motion comes from a world-space pattern travelling upward inside the annulus. Its sideways bend follows the v004 geometry-derived route, with a restrained fraction of the tool's angular movement. Three irregular, non-emissive fragments follow the corresponding geometry-aware path. There are no separate amber trail objects. Fragment support diameters are 14–16 mm; actual mesh extents are recorded in `Records/cutting-dimensions.json`. These are authored illustrative fragments, not measured field samples.

The fluid's inner exclusion boundary turns with the steel to preserve clearance, while its outer cylinder is rotationally invariant. This boundary motion does not represent fluid rigidly rotating: the density pattern and cutting trajectories are independent world-space motion. The hardware still turns at an authored 5 degrees per second, with no axial translation or independent pad rotation.

This is geometry-aware visual explanation, not CFD. The shading does not report physical fluid density, pressure, viscosity, turbulence, conservation or measured hydraulic performance. The inherited source functional-stage/end-identity limitations remain unchanged.

## Verification

- Complete fluid-boundary/steel triangle test and all 144,480 volume vertices checked: no intersection; positive radial exterior clearance.
- Common rigid rotation of the steel and inner exclusion boundary verified over all output frames and halfway points. This preserves their relative clearance throughout the illustrated rotation. The cylindrical wall limit is invariant.
- Three fragments checked against steel and the fluid boundary at all 72 output frames plus 71 halfway points: no intersections; fragments stay inside the fluid volume.
- Minimum checked fluid-boundary distance from steel: 0.768 mm; wall margin: 1.000 mm. These are conservative visualization offsets, not physical air gaps or operating specifications.
- Minimum fragment clearance: 8.186 mm from steel, 5.388 mm from the wall, and 4.388 mm inside the fluid boundary.
- Camera position, rotation and lens exactly match v006; camera remains stationary. Shared ECCO source and v006 hashes match their baselines. v001–v006 remain present.
- All 72 encoded frames decoded. Agent inspected the static frame and twelve chronological decoded frames; normal-speed comprehension remains the owner's review decision.
- Final batch render/write mean **1.961 s**, maximum **2.219 s**. All output frames pass the strict five-second limit. An exploratory 32-sample transparency render took 7.309 s; it was not used for batching. Sampling was reduced to 16 and frames 1, 36 and 72 rebenchmarked successfully before the batch.
- Saved native reopened with its relative source link resolving. A new frame-36 render exactly matches the original frame pixels.

The geometry checks establish implementation clearance, not physical simulation or viewer comprehension. Unsampled cutting motion is not continuously certified. The main review question is whether the filled amber volume reads as moving fluid and makes the pad interaction clear, rather than appearing to be a tinted cover.

## Source and delivery

Local root: `C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/05-Previs/Section-05_Hydraulic-Enhancement/Interaction-Proof_v007/`.

Linked master: `04-Production/Shared/Assets/ECCO/ECCO_film_v002.blend`, SHA-256 `df656a5c4bc48f081a4b6365c7969df55d15c7da53ddb96be20875e931d26584`.

Native SHA-256: `b1cf584c5e8a1d611717bb5d32739f445c103d63277f4046694772a04114202c`.

Video SHA-256: `a5b5ed96d4e1c69cdaf7bdf93270b14df9c2d0e3cd9c14541be367b3b372b6ff`.

Reproduction order from v006: `Scripts/still.py`, inspect static treatment; `refine_still.py`; `motion.py`; `final_preview_settings.py`; `verify.py`; representative benchmark; `render_chunk.py`; `package.py`. Retain v004 route data and the linked master. Existing built candidates are not overwritten by the initial build script.

Native/video/raw frames stay local. Scoped scripts, records, contract amendment and selected stills are published. Local recovery-copy and publication evidence are in `Records/backup-verification.json` and `Records/sync-verification.json`. No shared master or earlier proof was modified.
