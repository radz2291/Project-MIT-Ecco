# T44 — shared uphole continuity correction

18 October2026. Prepared for Radzi review; new appearance approval pending. Task b77297cc-0600-4a17-8fb9-ba95cc3d6220, MIT ECCO project a0b9b971-e282-42f0-a25f-0c78729eff87. Authority: owner-requested T44 discussion174d6ae2-c620-40c0-a7b1-92c01f613dda and the user's request to inspect/handle the update. Base commit df1bc5626e820dc3a0b9af286bfcca4ce498d8c0. [Preserved preceding report](report_v006.md).

## Result and images

The actual uphole collar stopped at localX-1.5m, with no hidden continuation. Canonical BHA filmv007 nests the unchanged accepted v006 hardware and adds a lightweight12m collar continuation plus a simplified connection shoulder. It remains connected through the saved wider/furthest views; the unwanted pipe endpoint is outside their frames. Length and visibility are local controls; isolated hero shots can hide the addition. No complete string-to-rig build, exact client/thread-fit claim, actual shot or film assembly.

[Full-size review images](Revision_v007/review-guide.md): [wider connection/product view](Previews/Revision_v007/connection_wide_v003.png), [second/furthest uphole view](Previews/Revision_v007/furthest_uphole_v002.png), [unchanged consumer A](Previews/Revision_v007/Reuse_A_v002.png), [unchanged consumer B](Previews/Revision_v007/Reuse_B_v002.png), [before/after proof](Previews/Revision_v007/propagation_v007.jpg). The wider view is an intentional local cutaway and shows finite formation bounds; it does not replace the previously accepted immersive environment views.

## Canonical source, controls and migration

[Native manifest/hashes](../../../Shared/Assets/World/manifest_v007.json), [interface/migration guide](../../../Shared/Assets/World/README_v004.md), [T45 handoff](Revision_v007/handoff_v007.md).

Local root: C:\Users\RZ1\Desktop\RZ\261013-MIT-Ecco\04-Production.

- Shared\Assets\BHA\BHA_film_v007.blend: SHA256 b6b98f870064f5b9e07640bec9dadaeb457c7e45ebdb5d33d2ac18b6210acdd1. WORLD_HARDWARE preserves accepted v006 via one identity collection instance. Separate WORLD_UPHOLE_EXTENSION/WORLD_UPHOLE_JOINT provide canonical added geometry; BHA_CONTINUITY_PREVIEW provides assembled native defaults.
- World\Scripts\formation_controls_v004.py creates new composed consumers. continuation_controls_v001.attach_continuation attaches to an existing local hardware collection-instance after reloading the direct hardware library. Do not recursively replace the nested frozen v006 library.
- New UPHOLE_CONTINUATION_CONTROL.length_m defaults12m (clamped.25–40m); show0 hides extension/joint. Existing hardware visibility also hides both. Parenting inherits placement, travel and spin without duplicating geometry or adding motion tracks. Only unit continuation localX scales; OD/bore/ECCO remain unchanged.
- Native source basis: +X selected downhole, metres; original collar endpointX-1.5m. Default continuation sourceX[-13.5,-1.5]m, OD8.25in/ID2.8125in inherited generic collar reference. Simplified raised transition spansX[-1.58,-1.44]m, maxradius.107m. No exact BHA connection or thread qualification.
- Final local consumers: Revision_v007\Scenes\Reuse_A_continuity_v002.blend, Reuse_B_continuity_v002.blend, connection_wide_v003.blend, furthest_uphole_v002.blend. Original reuse cameras,72/96frame timing, independent control values/keys and source geometry are unchanged. Extra wide/furthest cameras belong only to separate static inspection files.

All accepted predecessor native hashes, ECCO geometry/sensor references, source dimensions/orientation, bit and environment are preserved. The live Blender scene has unsaved user changes and was not reopened/overwritten. Shorter continuation lengths or new camera paths require new coverage checks. T45 combined sensing/casing/flow consumers require relink, unchanged-camera/timing/control verification, source registration, contact/occlusion/clearance checks and their own benchmark/render evidence.

## Verification and performance

[Canonical native verification](Revision_v007/Evidence/native-verification_canonical_v007.json):389checks pass. These include all accepted native hashes, fresh relative links, one ECCO/continuation, exact metre scale, continuous joint to1e-5m tolerance across all original reuse frames, far endpoint outside the intended cameras, length1/12/24m, hero visibility, whole-hardware visibility and unchanged cameras/timing/old controls. Isolated preparation candidate and earlier wide framing remain preserved.

Full first render-to-file timings, separate fresh processes,1280x720/EEVEE16/Vulkan, normal existing GPU disk caches, no excluded warmup, no compositor/raytracing/shadows:

| View | Seconds |
|---|---:|
| Wider complete product/connectionv003 |2.557|
| Furthest upholev002 |1.699|
| Reuse A v002 |1.550|
| Reuse B v002 |2.045|
| Preserved earlier cropped widev002 |1.969|

Every retained revision render is strictly below5s. Timers include the complete render-to-file call; process/file loading excluded. Empty-cache startup12.55–25.13s from the prior release remains unresolved; these measurements establish normal-cache performance only. Rebenchmark changed machine/cache/backend/driver/material/heavier views, without raising the cap. The initial wide was retained after executor inspection found the product cropped; a separate perpendicular view now includes the complete assembly. Executor visual inspection and native checks do not establish Radzi appearance or engineering acceptance.

## Coordination, storage and gate

The user initially chose coordination in this chat, then directly instructed T45, “Please coordinate with T44 and get things done.” That actual user message was verified before cross-chat replies. T45 confirmed it began no extension work, granted T44 exclusive new successor paths and serialized slot T44-CONTINUITY-01 plus one replacement still, and retained sole Git integration. Slot released after five renders. No T45–T48/unrelated generated file edits, Git staging/commit/push, competing jobs or live Blender replacement by T44.

T45 receives the exact permitted file list, native/API/hash/migration handoff and actual images for inspection/scoped commit. The exact remote-verified containing commit/report links are attached to live T44 after integration. Native .blend files, intermediate samples and logs remain local/Git-ignored; no native upload or off-machine backup claimed.

Progressive release: the canonical successor/API are available for T45 integration/rechecks; human visual approval remains pending. T44 returns to Review after verified synchronization, not self-accepted Done. The Work dependency gate for T45 must be reported truthfully and cannot be bypassed by this technical release. Radzi owns appearance acceptance and film assembly.
