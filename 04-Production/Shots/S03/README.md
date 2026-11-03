# S03 production sequence

ECCO-058 · first collaboration checkpoint · 3 November 2026

Open [S03 production v001](Scenes/S03_production_v001.blend) locally. It is a Blender Save As of the owner-selected S03 v036. It retains the continuous camera, authored motion and markers, 432 frames at 24 fps, and the local geometry and amplitude displays. White marks nominal size, blue enlargement and red a tight region. The separate amplitude reveal and illustrative provenance label are retained. No waveform, guides or DOF were added.

[Opening comparison](Previews/S03_continuity_v001.jpg) shows the end of the reviewed S01–S02 v026 export on the left and the saved S03 opening on the right. The blue bore and rings carry over visually. The camera moves from a wide side view to a closer view looking into the opening, and the surrounding line treatment changes. The S03 cases remain a separate illustrative reconstruction. The editable S01–S02 continuity reference is Scenes/S01-S02_production_v027_clean.blend under Shots/S01-S02.

The selected source and five-second reference clip are under 05-Previs/Section-03_The-Earth-Revealed/v036. The source full clip was sampled across the sequence. The candidate was reopened and rendered at frames 1, 216, 241 and 432. EEVEE at 960 × 540 took 1.340–2.945 seconds per PNG. No new motion batch was run at this checkpoint.

The saved candidate has zero linked Blender libraries. Blender's general path scan still reports an inherited reference to the removed v006 amplitude test scene. That path was already absent in v036. It did not prevent reopening or rendering the sampled frames. See [verification](Notes/verification_v001.json).

Shared contextual lines v004 were derived from World v010, pinned to SHA-256 9cb7d5c946e8573abc05af4ee3c12492610a982c1773a6437f90a762055fb540. The local v010 hash is 67e789b370746ecb58fd186acf4678e4d64ad4da92aee1fb0a7e9bade1179538. The checkpoint keeps the v036 context. Any shared context integration needs the matching World source or regenerated lines and a check through the actual S03 camera.

The Blender file and preview media remain local. Off-machine backup is unverified. The next collaborative decision is whether the framing jump at the cut should stay or be softened. Ticket wrap awaits Radzi's direction.

## Shared context proof v002

The current World pin passes. The opening-frame lines-only proof exceeded the render cap and shows visible cyan line endings at the bore edge. v001 remains the working scene. See [the proof note](Notes/shared-lines-proof_v002.md).

## Paired shared environment proof v003

The linked World ground and matching digital lines reopen correctly together. The opening frame exceeded the render cap and still shows cyan slivers along the bore edge. See [the paired proof note](Notes/shared-environment-proof_v003.md).

## Compute-space look proof v006

The owner redirected S03 to a floating borehole in a shot-local compute space. See [the look proof](Notes/compute-space-proof_v006.md).

## Rectangular compute room proof v007

A wide planar grid replaces the cylindrical coordinate field. See [the box-room proof](Notes/compute-box-proof_v007.md).

## Compute room with walls v008

The side and back walls form a visible corner around the floating bore. See [the v008 proof note](Notes/compute-room-proof_v008.md).

## Larger compute room proof v009

The room is about 44% wider, 32% deeper and 42% taller than v008. The review camera and bore framing are retained. Both the side and back walls remain visible. Local proof: Scenes/S03_compute-room-proof_v009.blend. Review stills: Previews/S03_compute-room_v009_angle.png and Previews/S03_compute-room_v009_opening.png. The scene reopened with zero linked libraries. Opening and angled stills took 4.978 and 2.540 seconds at 960 × 540. Motion and batch qualification remain pending.

## Wider compute room proof v010

The room width increases from 6.2 to 8.7 scene units (40%). The side and back walls remain visible at the same review angle. Local scene: Scenes/S03_compute-room-proof_v010.blend. Stills: Previews/S03_compute-room_v010_angle.png and Previews/S03_compute-room_v010_opening.png. Reopened with zero linked libraries. At 960 × 540, the cold opening took 5.242 seconds and the angled still 2.240 seconds. Full motion and batch settings remain unqualified.

## Wider back wall v011

The room widens toward the back from 8.7 to 11.745 scene units, with the foreground width, depth, height and cameras retained from v010. The side wall and back corner remain visible. Local scene: Scenes/S03_compute-room-proof_v011.blend. Stills: Previews/S03_compute-room_v011_angle.png and Previews/S03_compute-room_v011_opening.png. The scene reopened without library links. The 960 × 540 opening and angle took 9.370 and 2.281 seconds. Motion and batch settings are pending.

## S02 profile match proof v012

S03 v012 fits the visible continuous wall to the full bore surface of the actual S02 v027 reveal carrier before its viewing wedge. The S03 recorded-wall placement restores the same source depth and the azimuth is retained. All 473,548 vertices hit the source with zero misses. Maximum radial change 49.33 mm. The S03 room and cameras carry forward from v011. Existing contour graphics and amplitude are separate displays and were not re-fitted in this proof. The depth bounds are clamped by 0.1 mm at the source ends to avoid edge misses.

Local scene: Scenes/S03_matched-S02-proof_v012.blend. Reopened without linked libraries. Opening and angle stills: Previews/S03_matched-S02_v012_opening.png and Previews/S03_matched-S02_v012_angle.png. Two 640 × 360 stills took 3.015 and 1.141 seconds. Motion and full overlay alignment remain pending.

## Final establishing camera clearance v013

Based on the selected v011 room and original S03 bore. The v011 pullback left the room through the camera-side wall. v013 extends that wall 3.8 scene units and carries the floor and wall grid with it. The animated camera path stays as authored. Checks on every frame 241–432 put the camera inside all four room panel planes, with minimum clearance of 1.16 scene units. Rendered frames 313 and 432 confirm an unobstructed view of the bore display and the final amber strip. Frame 1 was also rendered. At 640 × 360 the three stills took 4.472, 0.882 and 1.760 seconds. Full motion render pending. Local native: Scenes/S03_compute-room-proof_v013.blend. Final still: Previews/S03_compute-room_v013_establishing.png.

## Establishing room edges v014

Following the marked final still, v014 moves the visible side wall 3.5 scene units outward and extends the room panels toward the foreground, back and above the frame. At frame 432 the room covers the former foreground gap and the amber bore display stays visible. Frames 241–432 retain 1.16 scene units minimum clearance to the checked room planes. The original S03 bore profile and camera move carry through. Saved scene: Scenes/S03_compute-room-proof_v014.blend. Stills: Previews/S03_compute-room_v014_opening.png, S03_compute-room_v014_pullback.png and S03_compute-room_v014_establishing.png. The 640 × 360 spot checks took 8.864, 52.193 and 39.634 seconds. No batch settings qualified in this run.

Full v014 motion preview: Previews/S03_compute-room_v014_full.mp4. All 432 frames decoded, 18 seconds at 24 fps. 480 × 270 EEVEE, four samples, compositor and ray tracing disabled. Slow render attempts stopped and resumed from retained frames. Maximum accepted render-to-file frame 4.114 seconds. Native scene and MP4 are local.

## Wraparound establishing orbit v016

Radzi clarified the orbit with an overhead sketch. v016 starts from v014 and blends the existing pullback into a 265-degree elliptical path around the bore, with the camera aimed toward its midpoint. Frames 270–432 were verified after reopen for saved position, rotation and room clearance, minimum 1.555 scene units. The scene opens in Blender Camera View at frame 270 for direct review. Local native: Scenes/S03_wraparound-orbit_v016.blend. No v016 motion render was requested for this checkpoint.

## Centered orbit and closed room v017

v017 keeps the wraparound camera positions and centers the bore midpoint in the image throughout frames 270–432. The camera aim and lens shift ease into center over frames 258–270. A front wall and ceiling meet the existing room panels, giving four walls, floor and ceiling. After reopen, the maximum normalized center error was 0.000000477 and minimum camera clearance across all six planes was 1.555 scene units. The local native was opened in Blender at frame 270 for viewport review. Scene: Scenes/S03_centered-orbit-closed-room_v017.blend. No v017 render was run.

## Orbit-only BHA wireframe v018

Derived 7,355 feature edges from 15 parts of shared BHA_film_v008, including ECCO housing, collars, adapters and bit. The shot-local copy is reduced radially to 69.6% and axially to 98.2% for illustrative fit inside the bore. The source master was not edited. The wireframe is hidden through frame 269 and visible from 270. The wall becomes translucent during the orbit so the wire reads through the amplitude display. Reopen checks passed at frames 1, 145, 241, 269, 270, 372 and 432. Frame 432 rendered at 480 × 270 in 4.810 seconds. Native: Scenes/S03_orbit-BHA-wireframe_v018.blend, saved at frame 372. No full animation render.

## Opaque bore with contextual BHA v019

The v018 x-ray shader was removed and the original opaque wall output restored. The subdued BHA wire remains orbit-only from frame 270. The drill tip projects 0.62 scene units beyond the bore end. The sparse rear wire pipe continues from local Z 1.5 to 8.4. The frame 380 still rendered in 4.463 seconds at 480 × 270 and shows the orange surface taking priority, with contextual wire extending outside the crop. The native was reopened and visibility verified. Local scene: Scenes/S03_orbit-BHA-context_v019.blend. Still: Previews/S03_orbit-BHA-context_v019_f0380.png. Full animation render pending.

## Section 2 BHA sizing v020

S02 v027 at frame 756 uses a unit-scale BHA assembly with the bit pointing down the negative Z axis and a 127 mm diameter uphole string. v020 restores full source scale to the S03 wire. The traced BHA has a 310.429 mm maximum outside envelope and 4.725 m axial span. The tail uses the 127 mm S02 diameter, and the drill tip still extends 0.62 m outside the bore. A radial ray check found no wall crossings at 8,056 sampled wire endpoints inside the bore. Minimum sampled radial clearance was 3.947 mm before line thickness. The orange wall remains opaque. This is a visual fit check of the sampled wire geometry. Local scene: Scenes/S03_orbit-BHA-source-scale_v020.blend. No v020 render.

Full v020 preview: Previews/S03_orbit-BHA_v020_full.mp4. All 432 frames decoded, 18 seconds at 24 fps. 480 × 270 EEVEE at four samples, compositor and ray tracing disabled. The first cold startup exceeded the cap. The retry passed and the maximum accepted render-to-file frame was 4.846 seconds. The native and MP4 stay local.

## Camera polish v021

Reviewed v020 camera transforms and identified the fastest zoom around frames 205–211, the sharpest turn around 254–258, and the reframing and speed change into the orbit. Smoothed the inspection zoom and pullback handoff. After reopening, the handoff peak turn fell from 4.065 to 2.760 degrees per frame, peak lens shift per frame from 0.02064 to 0.01086, and the peak positional second difference from 0.02161 to 0.01646 scene units. The orbit center and room clearance checks pass. See Notes/camera-polish_v021.json. Scene: Scenes/S03_camera-polish_v021.blend, opened for viewport review at frame 245. No new motion render.

## Exposed BHA ends and full render v022

Clipped the BHA wires to the exposed drill and pipe ends outside the bore axial span, avoiding interior bleed-through while retaining the v021 camera polish. Orbit visibility starts at frame 270. Native: Scenes/S03_exposed-BHA-ends_v022.blend. Full MP4: Previews/S03_exposed-BHA_v022_full.mp4. All 432 frames decoded at 24 fps, 18 seconds, 480 × 270. Slowest production frame 1.039 seconds. Native and MP4 remain local.

## Extended orbit and fixed titles v023

The timeline extends by 120 frames to 552 at 24 fps (23 seconds). The orbit carries through frame 385 into a 205-degree continuation that eases to a stop. Smoothed entry camera transforms around the reported frames 272–278. Geometry Through Depth and Acoustic Amplitude / Recorded Data now face camera in a fixed screen position with lens-compensated size and the existing visibility timing. The saved scene reopened with the bore centered and camera inside the room through the extended orbit. Local native: Scenes/S03_extended-orbit_v023.blend. No v023 render. Evidence: Notes/extended-orbit_v023.json.

## Subtle fixed titles v024

Both camera-fixed titles are 34% smaller and use a muted blue-white. The local scene reopened and was launched at frame 380 for viewport review. Scene: Scenes/S03_subtle-titles_v024.blend. No v024 render.

## Two Tight accents v025

Added two small illustrative radial constrictions at the marked frame-216 locations. They use the existing radius-based color classification, with the independent amplitude map retained. The saved 552-frame scene reopened and frame 216 rendered at 480 × 270 in 3.850 seconds. Local native: Scenes/S03_tight-accents_v025.blend. Still: Previews/S03_tight-accents_v025_f0216.png. Evidence: Notes/tight-accents_v025.json. Full motion pending.

## Textured Tight accents v026

Rebuilt the two marked local constrictions from v024 with irregular surface variation and a feathered boundary. They use the same radius classifier as the existing Tight region. The independent amplitude map stays separate. Saved and reopened Scenes/S03_tight-accents_v026.blend, then rendered frame 216 to Previews/S03_tight-accents_v026_f0216.png. This was one still at 480 × 270, which took 7.8 seconds. No batch was run. Evidence: Notes/tight-accents_v026.json.

## Selected v024 full render

Radzi reverted the added Tight patches and selected Scenes/S03_subtle-titles_v024.blend. Full preview: Previews/S03_extended-orbit_v024_full.mp4. FFmpeg decoded 552 frames at 24 fps (23 seconds). 480 × 270 EEVEE at four samples, compositor and ray tracing disabled. First cold startup exceeded the cap and the retry passed. Slowest accepted frame 3.679 seconds. Native and MP4 remain local.

## Smooth orbit entry v027

At the 11-second handoff, frame 270 had a camera aim spike and abrupt BHA appearance. v027 smooths camera rotation around that point and fades the exposed BHA ends in across frames 270–290. Exact center tracking resumes after the short blend. The frame-270 turn fell from 3.515 to 2.184 degrees per frame. Frames 246–306 were rerendered at matching v024 settings. The other 491 PNGs were reused after verifying zero camera-matrix difference and identical lens and shift on all reused frames. Full preview decoded 552 frames at 24 fps. Local native: Scenes/S03_smooth-orbit-entry_v027.blend. Full preview: Previews/S03_smooth-orbit_v027_full.mp4.

## Measurement rings follow labels v028

The entrance shows white nominal rings. The three measured profiles draw and fade with their corresponding Near Nominal, Enlarged and Tight labels at stations 0, 1 and 2. The white reference remains beside each active measured profile. The measured lines use a modest emission lift, and the Tight line is fitted just inside the visible surface to avoid occlusion. Overview contours are held until the outgoing view. The saved v028 passed visibility spot checks and rendered frames 1, 122, 172 and 222. The cold opening exceeded five seconds; no full batch ran. Local scene: Scenes/S03_label-synced-rings_v028.blend. Evidence: Notes/label-synced-rings_v028.json.

## Held measurement rings v029

The Nominal Reference is fixed near the upper-left third. White rings remain visible through the interior passage. Measured rings and their world-space labels stay after reveal and leave the view through camera motion. Local native: Scenes/S03_held-measurements_v029.blend. The first 10 seconds are in Previews/S03_held-measurements_v029_first-10s.mp4. Decoded all 240 frames at 960 × 540 and 24 fps. Render resumed after intermittent time spikes. Slowest accepted frame 4.305 seconds. The full 23-second render remains pending.

## Clean orange measurement rings v030

Removed the circled duplicate Nominal Reference and footer text, plus the nominal supporting rails and radial witness ticks. The fixed upper-left label stays. Measurement station lines are orange and 1.65 times the previous line thickness. White rings still represent nominal. The room grid and reveal timing carry forward. Local native: Scenes/S03_clean-orange-rings_v030.blend. Reopened and rendered frames 48, 122, 172 and 222 at 960 × 540. Evidence: Notes/clean-orange-rings_v030.json. The cold still exceeded the batch cap, so no new motion render was run.

## Thinner green rings and entrance-only label v032

Measured rings are teal-green based on Radzi's supplied reference and about 30% thinner than v030. The white reference rings remain visible through the bore. The fixed Nominal Reference text fades as the camera enters, from frame 49 to 78, before the first measured label. Reopened and checked the opacity timing. Rendered frames 48, 172 and 222 at 960 × 540. Local scene: Scenes/S03_green-rings_v032.blend. Stills only.

## Nominal Reference fade-in v033

Entrance label fades in over frames 1–15, holds through frame 49, and fades out by frame 78. Saved and reopened Scenes/S03_nominal-fade-in_v033.blend and checked both fades at endpoints and intermediate frames. No v033 render.

## Full v033 preview

Full preview: Previews/S03_nominal-fade-in_v033_full.mp4. FFmpeg decoded all 552 frames at 24 fps (23 seconds). 960 × 540 EEVEE at eight samples, compositor and ray tracing disabled. Cold startup measured separately. Slowest accepted render-to-file frame 4.355 seconds. Blender native, MP4 and PNGs remain local.

## White-ring pullback v034

Nominal Reference starts fading in with the third newly drawn nominal ring at frame 35. The bore exit check places the end of interior measured rings and labels at frame 254. The middle pullback carries white reference rings only, fading them across frames 320–337 as the amplitude reveal takes over. Removed the stray overview contour object and classified fragments. The BHA wire remains. The saved scene reopened and rendered frames 42, 300 and 552 at 960 × 540. Local scene: Scenes/S03_white-ring-pullback_v034.blend. No full motion render.

## Unified room grid v035

Rebuilt the floor and four wall grids with shared corner endpoints and roughly 0.72-unit spacing. The walls use lower emission and thinner strokes. The room widens toward the back, so cross-room cells widen slightly with it. Saved scene: Scenes/S03_unified-room-grid_v035.blend. Reopened and verified grid counts. Frame 300 and 552 stills at 960 × 540 took 5.877 and 0.819 seconds. No batch render. Evidence: Notes/unified-room-grid_v035.json.

## Visible floor and wall grid v036

Increased the wall-grid stroke and emission so it reads beside the floor grid. Saved and reopened Scenes/S03_floor-and-wall-grid_v036.blend. Rendered frames 300 and 552 at 960 × 540 in 4.130 and 0.932 seconds. Stills only. Previews: S03_floor-and-wall-grid_v036_f0300.png and S03_floor-and-wall-grid_v036_f0552.png.

## Matched floor and wall color v037

The room panels use the floor's navy material and both grids share the floor grid material. The saved scene reopened and both material assignments were verified. Frame 552 rendered at 960 × 540 in 6.32 seconds on cold startup. Local scene: Scenes/S03_floor-and-wall-grid_v037.blend. Still: Previews/S03_floor-and-wall-grid_v037_f0552.png. No motion batch.

## Orbit title fades v038

Geometry Through Depth fades in on frames 280–290 and out on 301–312. Acoustic Amplitude / Recorded Data fades in on 313–327 and out on 530–552. Both stay camera-fixed and have separate opacity animation. Verified endpoints and mid-fades after reopening. Rendered frames 286, 320 and 542 at 960 × 540. Local scene: Scenes/S03_title-fades_v038.blend. Final batch pending.

## Earlier and longer Geometry Through Depth v039

Geometry Through Depth fades in on frames 260–271, holds through 319, then fades out by 330. Acoustic Amplitude starts fading in at 331 as the orange reveal begins and keeps its existing ending fade. Timing was checked after reopening, with stills at 271, 325 and 338. Local native: Scenes/S03_title-fades_v039.blend. No full render.

## Final v039 render

Previews/S03_title-fades_v039_full.mp4 decoded all 552 frames at 960 × 540, 24 fps (23 seconds). Resumed from 364 saved frames after interruption. Per-frame timings were retained for the resumed run, with a maximum accepted frame of 2.27 seconds. Native and video are local.

## Restored interior labels and complete v040 rerender

The exit hide keys introduced in v034 evaluated as hidden before their first key on the three interior labels. v040 explicitly keys visibility through frame 253 and hides at 254. Original opacity and reveal timing carry forward. Near Nominal, Enlarged and Tight were visually verified in frames 122, 172 and 222 decoded from the final MP4. All 552 frames were rerendered and decoded at 960 × 540, 24 fps, 23 seconds. Slowest accepted frame 4.927 seconds. Local native: Scenes/S03_restored-interior-labels_v040.blend. Full video: Previews/S03_restored-interior-labels_v040_full.mp4. Decoded check: Previews/S03_v040_decoded-label-check.png.
