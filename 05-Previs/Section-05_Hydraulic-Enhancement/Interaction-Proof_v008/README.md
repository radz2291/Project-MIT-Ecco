# S05 v008 — Internal flow and carried cuttings

The owner approved **v007's fluid-volume concept** as the foundation. v008 preserves that volume and adds three sparse groups of soft amber wisps to make upward travel and the bend around the pad easier to follow. Each group follows the same path as one matte cutting. Scope remains one three-second proof for review; full Section 5 is not released.

## Deliverables

- `Previews/S05_internal-flow_v008.mp4` — 72 frames, 24 fps, 1280 × 720.
- `Previews/interaction_still.png` — matching frame 36.
- `Scenes/S05_internal-flow_v008.blend` — editable source, reopened at frame 36.
- `Previews/review.html` — local player and chronological frame sheet.

## Change and preservation

Three groups contain three wisps each, offset in depth and sideways within the annulus. They are softly tapered, partially transparent, diffusely shaded and non-emissive. Their trajectories remain continuous with no wrap/reset. Each group follows behind one cutting through the approach, the turn around the actual pad, and the upward exit. The same geometry-aware field supplies both motions: independent upward progression plus partial influence from the turning tool. The wisps are not parented to hardware.

The three existing irregular cuttings retain v007's sizes and trajectories. Increased matte facet contrast and subtle roughness help separate them from the steel. Their maximum support diameters remain 14–16 mm; actual mesh extents are approximately 10–13 mm length and 6 mm thickness. They are authored illustrative fragments, not measured field samples.

The accepted fluid mesh, topology, material nodes and camera were compared directly by reopening v007 and v008 and match. The body, borehole, continuous connected rotation, palette and source dimensions are preserved. No new fluid representation or shared-master edit was introduced.

## Checks

- All nine evaluated wisp meshes and three cuttings checked against steel and fluid boundaries at 72 output frames plus 71 halfway points: no intersections; all remain inside the fluid domain.
- Minimum checked moving-element distance: 8.186 mm from steel, 4.593 mm from the borehole wall, 3.593 mm inside the fluid boundary.
- Accepted annular boundary checked fully against steel; common rigid transform and cylindrical invariance preserve its relative clearance. Camera remains stationary and hardware connected, with no axial translation.
- The shared ECCO source and v007 native hashes remain unchanged. Prior versions are retained.
- All 72 encoded frames decoded successfully. Agent inspected a matching still and twelve chronological decoded frames; normal-playback comprehension remains the owner's review decision.
- Final batch mean **1.904 s/frame**, maximum **2.122 s/frame**. All batch and representative benchmark renders were under five seconds; the slowest representative benchmark was 4.609 seconds.
- Native reopened, relative source link resolved, and a fresh frame-36 render matches the original output pixel-for-pixel.

This remains authored illustrative transport, not CFD, actual RPM or hydraulic-performance validation. Wisps are motion cues inside the accepted fluid, not measured streamlines. Geometric checks do not prove audience understanding or every unsampled instant of movement. Review whether the groups now make direction, pad redirection and transported cuttings clear at normal speed.

## Storage and reproduction

Local root: `C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/05-Previs/Section-05_Hydraulic-Enhancement/Interaction-Proof_v008/`.

Native SHA-256: `0c3e0864eab93105494fe1790ff9f8a1bf97ab024fcb60b6387e6b4e8df6ac4f`.

Video SHA-256: `a55df3fe4d32df2927179e0c4736aabc8cde38d0e87762ddf318024201841b51`.

Source: `04-Production/Shared/Assets/ECCO/ECCO_film_v002.blend`, SHA-256 `df656a5c4bc48f081a4b6365c7969df55d15c7da53ddb96be20875e931d26584`.

Build from v007 using `Scripts/build.py`, then `verify.py`, representative benchmarks, `render_chunk.py`, `package.py` and `verify_preservation.py`. The build uses the retained v004 route data and v006 field functions and refuses to overwrite an existing candidate. Records contain evidence and timings. Native, video and raw frames remain local; scoped scripts, records and selected stills are published. Recovery-copy and publication details are in `Records/backup-verification.json` and `Records/sync-verification.json`.

**Stop: focused v008 proof ready for owner review. No 18-second integration.**
