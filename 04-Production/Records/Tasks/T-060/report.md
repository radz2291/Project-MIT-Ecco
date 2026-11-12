# ECCO-060 · Section 5 production preparation

12 November 2026

## Starting point

Radzi directed the Section 4 workflow for Section 5, using the approved previs and matching shared components while keeping the custom ground and cement. The baseline is the owner-approved `S05_continuous-camera_v020.blend` under `05-Previs/Section-05_Hydraulic-Enhancement/Camera-Proof_v020/Scenes/`. The baseline scene and original delivery video still match their approval hashes.

## Prepared scene

The local production copy is `04-Production/Shots/S05/Scenes/S05_shared-hardware_v021.blend`, SHA-256 `64d651dbe8e70ec67e44915ee77ad2e5dffa4af3f17057c9b771161c98d03f39`. The retired ECCO v002 path in the previs was resolved in memory using the archived master for the source check. The production copy links `Shared/Assets/Hardware/ECCO/ECCO_film_v003.blend` and `Shared/Assets/Hardware/ECCO/Dependencies/Satin_finish_v001.blend` through relative paths. The satin group drives the shot material's base color, roughness and metallic inputs. Imaging caps use the shared sensor face setting.

The geometry check matched vertex coordinates, face topology and material indices for the housing and nine closures. The source rig contains only ECCO hardware. BHA v008 has no counterpart in this composition. The shot keeps its custom cutaway mesh and local section materials. The amber hydraulics and cuttings are section-owned under ECCO-050 and retain their illustrative circulation treatment.

The saved production file reopened with both relative libraries resolved. The frame range is 1–432 at 24 fps. Camera transform, lens, focus, shifts and timeline markers matched v020 at ten samples. The same samples matched the transforms and render visibility of the ten hardware objects, fixed cutaway and 79 objects in the continuous hydraulics collection. The fixed cutaway also matched its source geometry and local material assignments. [Verification](../../../Shots/S05/Notes/v021-shared-hardware.json)

## First look

Rendered and inspected frames 50, 205 and 390 at the saved previs settings, 960 × 540 in EEVEE using Vulkan. They show the lower tool tracking, interaction and final detail with the shared finish and amber circulation. The cold first still took 9.742 seconds. The next two took 0.682 and 0.710 seconds. This is a still proof. A representative warmed benchmark across the complete shot is still needed before a full batch under the strict five-second cap.

The local three-frame proof is `04-Production/Shots/S05/Previews/S05_shared-hardware_v021_look.png`. Native and preview are local, with off-machine backup unverified. The focused proof is ready for Radzi’s feedback before the complete picture-only render.

## Shared BHA v022

Radzi directed the use of shared BHA. The production candidate is `04-Production/Shots/S05/Scenes/S05_shared-bha_v022.blend`, SHA-256 `3d9049828000f6dd8a8de70ec74ae05f4f04ef88def8e12ccd9260fe2f39cea8`. The shared BHA v008 core and standard uphole joint follow the existing axial rotation at source scale. The extra 12 m continuation starts beyond the local cutaway and was omitted from the shot. The single connected assembly supplies ECCO v003 and the shared satin finish. v021 remains available as the earlier ECCO-only copy.

At ten timeline samples, the ten ECCO parts matched source mesh geometry and their prior poses within 2.13e-7 maximum matrix-component difference. The 126 accessory meshes use their shared links. Added mesh vertices inside the cutaway reached a maximum radius of 107.0 mm against the 155.57 mm wall radius. The check concerns the visual fit in this scene. Camera, cutaway and section-owned hydraulic transforms and visibility matched at all ten samples. All four relative libraries resolved on reopen.

Five 960 × 540 EEVEE Vulkan stills cover opening, lower body, interaction, detail and ending. Render-to-file times ranged from 0.608 to 2.923 seconds in this session. The sampled images show the flow and custom cutaway around the shared assembly. The local three-frame look proof is `04-Production/Shots/S05/Previews/S05_shared-bha_v022_look.png`. [Scene checks and timings](../../../Shots/S05/Notes/v022-shared-bha.json)

## Section 3 navy room look trial v023

Radzi requested a Section 3-style navy room and subtle grid, with the custom borehole cuts and amber flow retained. The local editable proof is `04-Production/Shots/S05/Scenes/S05_navy-room_v023.blend`, SHA-256 `049cc3b4f222290352644da20aa2ee3e41a718e693cf3363c3896412676548df`. The room uses navy panels and aligned muted blue floor and wall grid lines, sized to S05. The v022 camera, cutaway mesh and material assignments, linked BHA and local hydraulics were carried into the proof.

The saved file reopened with four relative libraries resolved. Camera optics and transforms, cutaway materials, BHA placement, and hydraulic material assignments and poses matched v022 at frames 50, 205 and 432. The camera stayed at least 1.45 m from the room's panel planes across all 432 timeline frames. The three 960 × 540 stills took 7.837 seconds on the first call and 0.648 and 0.687 seconds after warmup. The grid appears at the opening edge, is cropped out of the close interaction and is more apparent around the cutaway in the pullback. The proof is local at `04-Production/Shots/S05/Previews/S05_navy-room_v023_look.png`. [Scene checks and still timings](../../../Shots/S05/Notes/v023-navy-room.json)

## Stylized wall and cement v024

Radzi asked to carry the styling onto the wall and cement. The custom cutaway uses matte blue charcoal on the borehole wall and lighter slate on the cut faces, with restrained grain and a soft highlight at the existing inner edge. The proof is `04-Production/Shots/S05/Scenes/S05_stylized-cutaway_v024.blend`, SHA-256 `96e3d192674d91588ec17aa6e6109ef9025c6137b2af01266ace1e0d4a1c46ed`.

The saved file reopened with four relative libraries resolved. The cutaway mesh and face material indices matched v023. Camera, BHA, navy room and amber hydraulic transforms and material assignments were checked at frames 50, 205 and 432. Three 960 × 540 stills were rendered and visually checked. The cold still took 12.539 seconds and the two warmed stills took 1.993 and 2.122 seconds. The local sheet is `04-Production/Shots/S05/Previews/S05_stylized-cutaway_v024_look.png`. [Scene checks and still timings](../../../Shots/S05/Notes/v024-stylized-cutaway.json)

## Digital borehole wall v025

Radzi requested a wireframe to help viewers distinguish the borehole from the metal BHA. The new proof draws blue cross-sections and lengthwise lines from the actual custom cutaway mesh. Brighter lines trace the cut opening, with sparser lines indicating its thickness. The original solid is retained in the native with render visibility off. The navy room, satin BHA and amber hydraulics retain their v024 settings.

The local editable proof is `04-Production/Shots/S05/Scenes/S05_wireframe-wall_v025.blend`, SHA-256 `72190b25f37f8175831a149d9faa9c8966ac1681513e37f48541845a11040f57`. It reopened with all four relative libraries resolved and the original cutaway geometry and material indices intact. Scene checks matched the camera, room, BHA and hydraulics at the review frames. Frames 50, 205 and 432 were rendered at 960 × 540 and visually checked. Cold render-to-file time was 6.269 seconds. Warm times were 2.621 and 3.909 seconds. The local proof sheet is `04-Production/Shots/S05/Previews/S05_wireframe-wall_v025_look.png`. [Scene checks and still timings](../../../Shots/S05/Notes/v025-wireframe-wall.json)

## Continuous borehole and ground v026

Radzi directed one model that combines the wall and ground to the frame edges. The new connected mesh uses all 97 samples of the custom inner bore arc at its original 155.575 mm radius. Flat ground extends outward from the two cut edges on the existing cut planes. The wire lines follow the bore and fade onto the plain navy ground. The independent room and standalone wire curves are hidden in this proof. The existing camera, BHA and amber hydraulics carry forward.

The saved scene is `04-Production/Shots/S05/Scenes/S05_continuous-ground_v026.blend`, SHA-256 `5c91c05e6a818f3e9b117a6ba6b5e0f349f6a2513b9c0b6b16c5c3b175d4ed51`. The connected mesh covered 15,120 camera rays across 432 frames, including the frame corners. Camera, hardware and hydraulic states matched at frames 50, 205 and 432. The scene reopened with four relative links resolved. Three 960 × 540 stills were visually checked. The first render took 5.911 seconds and the next two took 1.401 and 2.278 seconds. The local proof sheet is `04-Production/Shots/S05/Previews/S05_continuous-ground_v026_look.png`. [Scene checks and still timings](../../../Shots/S05/Notes/v026-continuous-ground.json)

## Graded ground grid v027

Radzi described a web-like pattern with many small cells at the bore edge and larger, fewer cells farther out. The proof uses lengthwise lines that start about 37 mm apart and widen by a factor of 1.43 for each outward interval. Cross-lines start 103.5 mm apart and double their spacing at every second lengthwise line. The surviving cross-lines stay continuous across the bands. The pattern uses the same v026 mesh and surface coordinates.

The local editable scene is `04-Production/Shots/S05/Scenes/S05_graded-ground-grid_v027.blend`, SHA-256 `d67f18958f7de5605df37b2b46da630de905b0a5809273d0203e155502057668`. It reopened with all four links resolved. Ground geometry and UV coordinates match v026. Camera, BHA and amber hydraulics matched at the three review frames. Frames 50, 205 and 432 were rendered at 960 × 540 and visually checked. The cold still took 8.454 seconds and the warm stills took 2.398 and 2.843 seconds. The local sheet is `04-Production/Shots/S05/Previews/S05_graded-ground-grid_v027_look.png`. [Scene checks and still timings](../../../Shots/S05/Notes/v027-graded-ground-grid.json)

## Continuous stretched grid v028

Radzi requested a more seamless pattern, like wrapping paper stretched over the borehole. v028 aligns the cross-lines and the initial cell widths where the wall meets the ground. Each cross-line now continues as one curve and the spacing increases smoothly with distance. The axial spacing is 1× at the lip, 2.05× at 0.36 m and 2.68× at 0.72 m.

The local scene is `04-Production/Shots/S05/Scenes/S05_stretched-grid_v028.blend`, SHA-256 `1c6d91b97d595eaee7d91cd373631bed5506c11b3f990b02419e24d8188ca95c`. The unified mesh and its surface coordinates match v027. Camera, shared BHA and amber hydraulics were checked at frames 50, 205 and 432. All four libraries resolved on reopen. The three 960 × 540 stills rendered in 3.883, 0.648 and 0.730 seconds and were visually inspected. The local sheet is `04-Production/Shots/S05/Previews/S05_stretched-grid_v028_look.png`. [Scene checks and still timings](../../../Shots/S05/Notes/v028-stretched-grid.json)
