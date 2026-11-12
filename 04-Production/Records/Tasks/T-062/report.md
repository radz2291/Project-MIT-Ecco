# ECCO-062 · Section 7 product hero

Task UUID `0b9ce2c9-72bd-4c33-8fec-7c89dc0a940b`. Radzi authorized the shared-asset production pass and requested a short preview before a full render. Publication base is `89d323d52f671661722957dd2ad2e6ba9dd77285` from `codex/ecco061-s06`. The existing checkout and its unrelated changes were preserved.

## Editable production scene v007

The [approved v006 previs](../../../Shots/S07/Sequence_v006/Records/owner-approval_2026-10-25.md) is the selected camera and editorial source. Its native and full movie hashes matched the recorded selection. The v007 scene is `04-Production/Shots/S07/Scenes/S07_shared-product-hero_v007.blend`, SHA-256 `b5003d994df0c0a7f0ccf61aa135d97f6596936cafb67f2a0bb3f2ebcc2f7ed2`.

The housing and nine visible closures use the linked `Shared/Assets/Hardware/ECCO/ECCO_film_v003.blend` meshes and materials. Those materials use `Satin_finish_v001.blend`. The original local objects keep the v006 transforms and studio setup. The ten mesh position, topology and smooth-face digests matched the previs. On reopen in Blender 5.2.3, both relative libraries resolved and evaluated camera, light and hardware samples matched all 192 frames. Cuts remain at frames 61 and 121. The fade starts at frame 164 and the frame 190 benchmark is visually black. The supplied logo and final film assembly remain with Radzi. [Native verification](../../../Shots/S07/Notes/v007-native.json)

## Short motion preview

The picture-only preview is `04-Production/Shots/S07/Previews/S07_shared-product-hero_v007_preview.mp4`, SHA-256 `d7089986c805971ec63904d9fdad34ee48b964ab79f826fb55fe06a250885f67`. It plays 72 consecutive source frames, 105–176, at 960 × 540 and 24 fps. The excerpt covers the reverse angle, the existing cut, the close-to-wide hero pullback and the start of the fade. All 72 distinct frames decoded. Decoded samples at 105, 120, 121, 136, 156 and 176 were visually inspected for the finish, cut and pullback. The contact sheet is local at `04-Production/Shots/S07/Previews/S07_shared-product-hero_v007_preview-check.png`.

The Vulkan EEVEE profile uses 16 samples and retains the compositor and sequencer settings. After an 8.956-second cold warmup, all 12 warmed benchmarks spanning the three shots passed, peaking at 0.722 seconds. Every preview frame rendered below five seconds, with a 0.562-second maximum. PNG frames and logs are local at `04-Production/Shots/S07/Cache/v007/preview-960x540-16spp`. The native, MP4 and cache are retained locally. Off-machine backup is unverified. [Preview verification](../../../Shots/S07/Notes/v007-preview-delivery.json)

The [build and render script](../../../Shots/S07/Scripts/prepare_shared_s07_v007.py) runs in Blender background with `--disable-autoexec --python-exit-code 1 --python <script> -- build`, then with `--gpu-backend vulkan` and the `preview` stage. The preview was encoded with FFmpeg from frame 105 for 72 frames at 24 fps, H.264 CRF 17, YUV420p, no audio. The full production render awaits Radzi's direction.
