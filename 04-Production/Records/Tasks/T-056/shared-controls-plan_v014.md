# ECCO-056 — Shared controls finishing plan

Preparation only. Master accepted this plan but holds Blender builds/renders until ECCO-054 passes and explicitly releases the queue. V013 is approved for now; final owner approval requires inspecting the actual shared Blender files. The published proof is pinned at c4d205a9dac72572762e14a91d43deff5149a119.

## Minimal native implementation

Create a new shared asset version; preserve the v013 native/video byte-exact. Translate the approved v013 field into live Geometry Nodes math using the same equations, strand coordinates, constant normalization and smooth opacity. Default output must compare against v013 at representative frames, including quiet, outbound-only, overlap, return-dominant and measurement phases. Do not normalize separately per frame. Default full height/width remains approximately40mm.

A shared master-control object has a clearly named Geometry Nodes modifier UI. Its one-point geometry stores control attributes. The linked field node group reads those shared attributes; no Python handlers, arbitrary drivers or startup script are needed. The master controls and field group are linked into each consumer, while the waveform instance has local override multipliers and timing/anchor inputs. The control point has no renderable faces.

Expose speed/playback, display frequency, source duration, strength, echo strength, envelope decay/tightness, maximum height/width, colors, emission, strand width and visibility. Label frequencies/times as display values, not acoustic calibration. Keep local event timing overrides distinct from shared appearance controls. Open-hole and cased presets are explicit illustrative style/response settings, not physical material measurements. Default open-hole preset reproduces v013; cased settings do not replace section-owned response data.

## Exact consumers

1. S02 source: `05-Previs/Section-02_Measurement-History/v011/Continuation/Scenes/S01-S02_continuous_v011.blend`. New isolated copy under `04-Production/Records/Tasks/T-056/Consumers/S02_waveform_shared_v014.blend`. Preserve source camera, range, fps, datasets and local history reveal. Fit the new waveform to the actual original sensor/wall anchors and event keys; no frozen tableau or replacement review camera in this consumer.
2. S04 source: `04-Production/Shots/S04/S04-A/Previs_v033/Scenes/S04_continuous_ABCD_v033.blend`. New isolated copy under `04-Production/Records/Tasks/T-056/Consumers/S04_waveform_shared_v014.blend`. Preserve the original camera/travel, all A–D timing, datasets, casing/steel response bands and wear behavior. Replace only scoped traveling-wave presentation.

S04 metadata `send_s=4.3/6.8` is stale relative to saved action samples. The cached native inspection shows first SEND visibility72.60–80.92 and ECHO81.56–90.52; second SEND184.60–192.92 and ECHO193.56–202.52. Fresh native inspection after release must establish precise event boundaries and anchors. Preserve local gaps and chronology; do not impose v013 overlap where it conflicts with S04. S02 inspected leading events were300/309/318 with later recording; fresh consumer checks still required.

## Verification and owner inspection

- Compare live-node defaults to preserved v013 geometry/opacity at selected frames with one fixed normalization. Benchmark representative saved output below5seconds/frame before any batch.
- Save/reopen the shared file and both consumer files with auto-execution disabled. Change controls directly in Blender and verify live geometry/material change without rebuilding a script.
- Demonstrate a bounded shared edit (e.g. emission+10%) propagating to both linked consumers after reload, then restore approved defaults. Demonstrate one local amplitude override changes only its consumer.
- Verify cameras/actions/frame ranges/fps/datasets and section-owned response behavior against each source. Check relative libraries, exact hashes, local override persistence and preset limits.
- Deliver the actual shared native and both consumer paths for Radzi to inspect, with brief control instructions and small evidence. Do not claim final acceptance from automatic checks or the provisional v013 approval.

No Blender build, render or UI mutation has been performed during this preparation phase. Master remains the sole Git integrator.
