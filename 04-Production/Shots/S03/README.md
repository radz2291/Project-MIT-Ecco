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
