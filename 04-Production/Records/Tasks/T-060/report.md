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
