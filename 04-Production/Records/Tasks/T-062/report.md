# ECCO-062 · Section 7 product hero

Task UUID `0b9ce2c9-72bd-4c33-8fec-7c89dc0a940b`. Radzi authorized the shared-asset production pass and requested a short preview before a full render. Publication base is `89d323d52f671661722957dd2ad2e6ba9dd77285` from `codex/ecco061-s06`. The existing checkout and its unrelated changes were preserved.

## Editable production scene v007

The [approved v006 previs](../../../Shots/S07/Sequence_v006/Records/owner-approval_2026-10-25.md) is the selected camera and editorial source. Its native and full movie hashes matched the recorded selection. The v007 scene is `04-Production/Shots/S07/Scenes/S07_shared-product-hero_v007.blend`, SHA-256 `b5003d994df0c0a7f0ccf61aa135d97f6596936cafb67f2a0bb3f2ebcc2f7ed2`.

The housing and nine visible closures use the linked `Shared/Assets/Hardware/ECCO/ECCO_film_v003.blend` meshes and materials. Those materials use `Satin_finish_v001.blend`. The original local objects keep the v006 transforms and studio setup. The ten mesh position, topology and smooth-face digests matched the previs. On reopen in Blender 5.2.3, both relative libraries resolved and evaluated camera, light and hardware samples matched all 192 frames. Cuts remain at frames 61 and 121. The fade starts at frame 164 and the frame 190 benchmark is visually black. The supplied logo and final film assembly remain with Radzi. [Native verification](../../../Shots/S07/Notes/v007-native.json)

## Short motion preview

The picture-only preview is `04-Production/Shots/S07/Previews/S07_shared-product-hero_v007_preview.mp4`, SHA-256 `d7089986c805971ec63904d9fdad34ee48b964ab79f826fb55fe06a250885f67`. It plays 72 consecutive source frames, 105–176, at 960 × 540 and 24 fps. The excerpt covers the reverse angle, the existing cut, the close-to-wide hero pullback and the start of the fade. All 72 distinct frames decoded. Decoded samples at 105, 120, 121, 136, 156 and 176 were visually inspected for the finish, cut and pullback. The contact sheet is local at `04-Production/Shots/S07/Previews/S07_shared-product-hero_v007_preview-check.png`.

The Vulkan EEVEE profile uses 16 samples and retains the compositor and sequencer settings. After an 8.956-second cold warmup, all 12 warmed benchmarks spanning the three shots passed, peaking at 0.722 seconds. Every preview frame rendered below five seconds, with a 0.562-second maximum. PNG frames and logs are local at `04-Production/Shots/S07/Cache/v007/preview-960x540-16spp`. The native, MP4 and cache are retained locally. Off-machine backup is unverified. [Preview verification](../../../Shots/S07/Notes/v007-preview-delivery.json)

The [build and render script](../../../Shots/S07/Scripts/prepare_shared_s07_v007.py) runs in Blender background with `--disable-autoexec --python-exit-code 1 --python <script> -- build`, then with `--gpu-backend vulkan` and the `preview` stage. The preview was encoded with FFmpeg from frame 105 for 72 frames at 24 fps, H.264 CRF 17, YUV420p, no audio. The full production render awaits Radzi's direction.

## Ending polish v008

Radzi requested a less abrupt ending and a small, slow turn. The previous preview ended at frame 176, partway through the fade. v008 eases into a 16° turn around the tool's existing longitudinal X control from frame 142, then continues at about 8.7° per second until the end. The fade begins two frames earlier at frame 162 and reaches black at frame 190. All 192 camera and light samples matched v007, and the tool poses matched through frame 142. The shared libraries resolve on reopen and the full tool stays in frame from frame 156 onward. [Ending verification](../../../Shots/S07/Notes/v008-ending.json)

The editable scene is `04-Production/Shots/S07/Scenes/S07_soft-ending_v008.blend`, SHA-256 `d24c56dfc81417b2d7a8fb3591dcb00646a1890b3d153e926f8dd617d53fb3a2`. The picture-only preview is `04-Production/Shots/S07/Previews/S07_soft-ending_v008_preview.mp4`, SHA-256 `0f3eca8ef3de1286335b2b2911c63e11363d67ac7ba4022bb2ef9d4e86d5789e`. It plays 88 consecutive source frames, 105–192, at 960 × 540 and 24 fps. It reuses the 38 verified v007 images through frame 142. Frame 142 matched a fresh v008 render pixel for pixel. All 50 revised frames rendered under five seconds with a 1.890-second peak. The nine warmed benchmarks peaked at 0.511 seconds. The cold warmup took 2.247 seconds.

All 88 encoded frames decoded. Nine sample images were inspected from the video and the final three frames were checked for black-level luminance. The [revision script](../../../Shots/S07/Scripts/polish_ending_s07_v008.py) uses the same Blender background build and preview stages as v007. The native, MP4, contact sheet and cache remain local. [Preview verification](../../../Shots/S07/Notes/v008-preview-delivery.json)

## Turn during the close pullback v009

Radzi asked to see the tool turn while it is still near the camera. The v009 turn starts at frame 121 with about 0.397° per frame and slows through the pullback and fade. The angle reaches 2.66° at frame 128, 5.37° at frame 136 and 16° at the end. The v008 camera, lighting and fade values match at all 192 frames. The earlier shots' tool poses match through frame 120. Both relative shared libraries resolved on reopen. [Animation and scene verification](../../../Shots/S07/Notes/v009-turn.json)

The editable scene is `04-Production/Shots/S07/Scenes/S07_turn-during-pullback_v009.blend`, SHA-256 `bcee70f3d816ec690d4f6ff1d937801db27c6154d0d59f055db6b52ca6c90cff`. The local MP4 is `04-Production/Shots/S07/Previews/S07_turn-during-pullback_v009_preview.mp4`, SHA-256 `79515531d47f8226991a7c4852f121a597096b0ed058539f29ba109d91526c96`. It reuses frames 105–120 and renders frames 121–192 with the revised turn. The first hero frame matches the previous revision pixel for pixel. Nine warmed benchmarks peaked at 0.797 seconds, and all 72 new images rendered below five seconds with a 0.470-second maximum.

All 88 video frames decoded at 960 × 540 and 24 fps. Nine encoded frames were inspected, including five during the close pullback. The last three frames reached black level. The cache is local under `04-Production/Shots/S07/Cache/v009/preview-960x540-16spp`. The [revision script](../../../Shots/S07/Scripts/turn_during_pullback_s07_v009.py) uses the established Blender background build and preview stages. [Preview verification](../../../Shots/S07/Notes/v009-preview-delivery.json)

## Full Section 7 picture v009

Radzi requested the complete Section 7 render after reviewing the v009 close-up turn. The picture-only MP4 is `04-Production/Shots/S07/Previews/S07_turn-during-pullback_v009_full.mp4`, SHA-256 `41fd5738450ec940d2af009ada5001ef649ca3f8305862ca09cb76a08278ac46`. It runs eight seconds at 960 × 540 and 24 fps. It includes the opening detail glide, reverse angle and close-up turn through the final pullback and fade. The saved v009 scene above supplied the render and reopened with both relative shared libraries resolved.

The Vulkan EEVEE profile uses 16 samples and the existing compositor and sequencer, matching the v009 preview. Seventeen warmed benchmarks across all three shots peaked at 0.546 seconds. Cold warmup took 2.173 seconds. The `full` stage of the revision script rendered frames 1–104, with a 1.271-second maximum. Frames 105–192 reuse the verified preview images. Fresh full-run checks for frames 105, 121, 136, 174 and 192 matched those cached images pixel for pixel. Raw frames and timings are local at `04-Production/Shots/S07/Cache/v009/full-960x540-16spp`.

FFmpeg encoded frames 1–192 to H.264 CRF 17, YUV420p, with no audio stream. All 192 frames decoded. The 189 frames before the closing black were distinct. Twelve decoded samples were inspected across both cuts, the cache join, the pullback and the black ending. The local review sheet is `04-Production/Shots/S07/Previews/S07_turn-during-pullback_v009_full-check.png`. Native and video stay local, with off-machine backup unverified. [Full delivery verification](../../../Shots/S07/Notes/v009-full-delivery.json)

## Owner approval and handoff · 12 November 2026

Radzi approved the complete v009 render and directed wrap in Codex. The eight-second picture-only MP4 above is the selected Section 7 picture for film assembly. The matching v009 Blender scene is the editable handoff. Earlier versions remain available as production history.

At wrap, both deliverable hashes matched the recorded v009 values. A fresh decode confirmed 192 frames at 960 × 540 and 24 fps, with 189 distinct frames before the closing black and no audio stream. Blender 5.2.3 reopened the scene and verified its 1–192 frame range and both relative libraries. The native and MP4 are retained locally. Off-machine backup remains unverified. Radzi owns logo insertion, audio, film assembly and client delivery.
