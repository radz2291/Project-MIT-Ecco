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
