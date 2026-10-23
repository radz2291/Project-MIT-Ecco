# S05 hydraulic interaction v003 — smoother moving tails

23 October 2026 · Stage 6 bounded six-second proof · ready for owner review.

The amber tails now follow each marker's recent movement, rather than being rebuilt as a different local curve at every frame. A stronger but restrained sideways influence near the rotating pads connects the flow visually to the spin. Upward transport continues independently. The camera, tool geometry, tool rotation, palette and fixed half-borehole remain as in v002.

- [Six-second video](Previews/S05_twisted-pad_interaction_v003.mp4), 1280×720, 24 fps.
- [Interaction still](Previews/interaction.png), [decoded chronology](Previews/motion-review.jpg), [review page](Previews/review.html).
- [Editable Blender scene](Scenes/S05_twisted-pad_interaction_v003.blend), reopened and left open at frame 72.
- [Previous v002 video](../Interaction-Proof_v002/Previews/S05_twisted-pad_interaction_v002.mp4) for comparison.

## Method and limits

The new tails contain actual prior positions from the authored marker animation, sampled at 120 Hz: up to 0.85 seconds for fluid markers and 0.55 seconds for rock fragments. Marker velocity is smoothed over an authored 0.12-second response. The existing partial tangential entrainment coefficient changes from 0.3 to 0.65; channel steering changes from 3.0 to 2.4. These are illustrative animation controls, not measured hydraulic parameters. The field continues to include changing pad orientation and moving-boundary avoidance. Effects remain unparented to the hardware.

Old trail positions can be overtaken by later moving steel. The visible history shortens before an unsafe position, using a conservative time envelope to soften the change. It also fades near display-domain endpoints. No old sample is arbitrarily bent into a new route to preserve tail length. The tail is a visualization of motion history, not a physical rope or simulated wake. Near a pad or domain restart it can become shorter. Subframe geometry and fresh empty-cache performance are not certified.

The whole ten-object instrument assembly still rotates clockwise from the surface at an illustrative 5 degrees/second, with no translation. Source dimensions, provisional covers and existing source-axis limitations remain as documented in v002. No actual operating RPM, validated fluid solution, quantitative transport benefit or new source-stage identification is claimed. The v002 engineering assessment remains applicable; this iteration introduces no additional physical claim.

## Checks

- [Geometry](Records/geometry-verification.json): all 144 output frames; no intersections between complete effect meshes and hardware. 417,888 sampled vertices checked against steel distance and radial exterior relationship. Minimum sampled distance to steel 2.15 mm; to borehole wall 8.07 mm. The unchanged tool-to-wall gap remains 3.175 mm. All ten rigid hardware transforms and zero axial translation verified.
- [Build](Records/build.json): exact settings and visible-history limits. Original v002 SHA256 remains `919d002c38c2c4864158b382bbf6a29349c67eb44de69309c5a6a8f4018672f4`; original v001 and shared source hashes also verified unchanged.
- [Benchmark](Records/benchmark.json): representative frames 0.666 / 0.490 / 0.491 seconds including write, using existing application caches.
- [Batch](Records/render-timings.json): mean **0.520 s/frame**, maximum **0.685 s/frame**. Every sample and output frame remains below five seconds.
- [Media](Records/media-verification.json): MP4 decoded successfully to all 144 RGB frames. Review stills are extracted from the actual video.
- [Fresh open](Records/fresh-open.json): saved native reopened and relative source library resolves.

Agent inspected the full-size interaction frame and twelve chronological decoded frames. The histories remain attached to marker movement and show bends near the pads. Whether this feels sufficiently natural at normal playback remains the owner's review decision; no independent comprehension test or engineering acceptance is claimed. Full 18-second integration and finishing remain unreleased.

The existing [S05-B contract](../../../04-Production/Shots/S05/S05-B/direction.md) owns the controlling decision. Native/video/cache stay local, with no off-machine media backup claimed. Task-owned scripts, records and selected stills are eligible for publication; `Records/sync-receipt.json` records the actual scoped result. Prior versions are preserved.

Reproduction: open clean v002, run `Scripts/build.py` once with `__file__` set; it reads the retained v002 script and track record and refuses an existing v003 output. Run `Scripts/verify.py`, benchmark, then `Scripts/render_chunk.py` with `START` and `END`. Package with `Scripts/package.py` using project-local ffmpeg and Pillow. Builders must not overwrite retained review candidates.
