# T46 hold handoff — preserved local state

18 October 2026. T45 ordered immediate hold after T44 reopened for the owner-assigned uphole continuity correction. Fresh Work read revision645 showed T44 in progress. No further Blender builds/renders were launched after this instruction. Existing T46 run was set waiting; ticket remains in progress, no Review.

Worker `codex-t45-sensing-builder-v001`; run `c3f0265f-e429-442f-8d39-6d1719ccc24f`. Master alone integrates Git. Current base is the frozen prior release `df1bc5626e820dc3a0b9af286bfcca4ce498d8c0`, which is not a substitute for the pending revised T44 release.

## Exact preserved candidate

| Artifact | SHA256 |
|---|---|
| `04-Production/Shared/Assets/Acoustics/Acoustics_v003.blend` | `2a467616b68a6183a33a7fb0e4abb685642bf3da1954ccd0377f035b44fb9572` |
| `04-Production/Records/Tasks/T-046/Scenes/Sensing_reuse_A_v008.blend` | `40634d8f88069c2d0d9fdc1f890287c064bd6d36679f29554e775b40704e451a` |
| `04-Production/Records/Tasks/T-046/Scenes/Sensing_reuse_B_v008.blend` | `5e10f833249a1c930f9648925a05bcf05f7cb9d37f81f7a9a47a89b7f4325e09` |
| `04-Production/Records/Tasks/T-046/Evidence/events_A_v002.json` | `e63e67b5346aa6e6d64c5c3e6b81c7f9d9d349b06395ae36fd0140c525187572` |
| `04-Production/Records/Tasks/T-046/Evidence/events_B_v002.json` | `fe8f3fa87dc02f0932234ea01d3be6f40d9e4a01a5a55090e5cbee9616081768` |
| `04-Production/Records/Tasks/T-046/Evidence/native-verification_v001.json` | `27159cbb8e6c95f23f4da1a67aa2bb679a06426fabda80bbcb677454ee56e57b` |

Native/media root: `C:\Users\RZ1\Desktop\RZ\261013-MIT-Ecco`. All native files remain local, ignored; no upload/off-machine backup. Source hashes, prior masters and failed visual still hashes are in `Shared/Assets/Acoustics/manifest_v001.json`.

## Completed and pending

Reusable effect-only library and native event/binding adapters exist. Two linked consumers have distinct cameras/timing; bounded shared revision preserves camera/animation. Native 260 checks pass, including finite arc envelopes, actual cap-exit/contact sightlines, reference plane/120degree spacing, source dimensions/link integrity, same reference during each event and fixed world samples. This is executor verification.

The native temporary cap is 2 mm proud of the inherited sensor reference. The adapter records the unchanged reference plus exact native cap exit/object/hash/offset; this is a provisional graphical emission convention. No source geometry was edited and no transducer datum certification is claimed.

Actual v004 images failed occlusion; v006 images exposed the sensor/contact but thick edge-on arcs read as rods. Those files/logs remain preserved. Current v008 consumers link v003 thin arcs in a visible circumferential fan, with a small fixed point; those changes have NOT been rendered. No playable demo exists. Prior measured frames remain below 5 seconds on normal caches; the empty-cache exception remains unresolved.

Resume only after revised T44 release and explicit T45 restoration. Then reconcile source hashes/links/native face samples, render the queued 3-frame A sample, inspect it, benchmark representative/peak states for both consumers, render/inspect a short behavior demo, verify cased integration, and supply the exact remote candidate plus independent verdict before Review. No source replacement, later rendering or downstream execution is authorized by this handoff.

## Exact integration boundaries

Writable roots were only `Shared/Assets/Acoustics/` and `Records/Tasks/T-046/`. No Git/global-manifest/live-Blender mutation was made. `allowed-tracked_v001.json` is the exact allowed list of text/scripts/JSON records; no heavy media or failed diagnostic PNG is included. Master may integrate that concrete list while preserving unrelated changes.

The package interface is `Shared/Assets/Acoustics/README_v001.md`. Current API is stable: `sample_native_event(...)` and `bind_event(...,library_version="v003")`; native saved playback requires no handlers. Cased builder has the stable API and must sample its own true steel intersection.
