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
