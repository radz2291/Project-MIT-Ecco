# A-WORLD — uphole continuity interface v004

18 October2026. Versioned T44 correction for Radzi review, retaining the accepted v006 source release. [Current native hashes](manifest_v007.json), [review images](../../../Records/Tasks/T-044/Revision_v007/review-guide.md), [integration handoff](../../../Records/Tasks/T-044/Revision_v007/handoff_v007.md), [report](../../../Records/Tasks/T-044/report.md). Earlier [cleanup interface](README_v003.md) and [manifest](manifest_v006.json) remain preserved.

## Canonical composition

`BHA/BHA_film_v007.blend` supplies these linked collections:

- `WORLD_HARDWARE`: identity instance of accepted BHAv006. All ECCO, bit, adapter, collar and sensor geometry remains in its unchanged predecessor libraries; there is one ECCO.
- `WORLD_UPHOLE_EXTENSION`: one normalized1m hollow collar segment, scaled longitudinally by the consumer. Its OD8.25in/ID2.8125in inherits the existing generic collar reference. No transverse scaling.
- `WORLD_UPHOLE_JOINT`: simplified raised transition across original collar endpointX-1.5m, X[-1.58,-1.44]m, maxradius.107m. It avoids a coplanar exterior overlap. No exact client hardware, pin/box/thread fit, hydraulic or deployment qualification.
- `BHA_CONTINUITY_PREVIEW`: an assembled native inspection composition with12m continuation defaults. Consumers use the three component collections and local controls through the API below. Linking only `WORLD_HARDWARE` deliberately retains the source base; migration must attach the continuation parts too.

Default continuation covers sourceX[-13.5,-1.5]m before assembly travel, using the existing +X downhole convention and metre scale. It is a bounded local string continuation, not a model connecting to the rig. The original bit, 2.400m housing, registered hole/layer dimensions, sensor references, orientation, materials and environment are unchanged.

## New consumers

With `World/Scripts` on Blender's Python import path, call `formation_controls_v004.create_world(asset_dir)`. The return shape and previous world controls remain unchanged. New local object `UPHOLE_CONTINUATION_CONTROL` has `length_m` (default12, supported.25–40m) and `show` (0/1). Extension and joint instances are returned in the existing instances dictionary. Hide with `show=0` for isolated product/bit hero shots; existing `show_hardware=0` also hides both parts.

The extension/joint are parented to the existing hardware instance. Whole assembly placement, travel, rotation and timing are inherited without new motion tracks or duplicated geometry. Only the normalized continuation's localX scale changes; its bore/OD and ECCO geometry do not scale. Shorter length settings must pass view-coverage checks again; parameter support does not guarantee every framing.

## Existing consumers and T45 migration

1. Preserve the saved predecessor and snapshot existing cameras, timing, keys, controls and source/native hashes. Resolve relative library paths against the old file before Save As.
2. Reload only the direct `BHA_film_v006.blend` library to `BHA_film_v007.blend`. The successor nests the frozen v006 library. Do not recursively replace that nested source or the ECCO/environment libraries.
3. Call `continuation_controls_v001.attach_continuation(asset_dir, hardware_instance)`, where `hardware_instance` is the consumer's existing local collection-instance of `WORLD_HARDWARE`. It returns the new control, extension/joint instances and far-endpoint marker. It works with both the original `CONSUMER_CONTROL/HARDWARE_INSTANCE` consumers and the later world API, preserving independent sensing/casing/flow controls.
4. Save a new version with all library paths relative and `relative_remap=False`. Fresh-open and verify one ECCO, one continuation, valid links, matching source mesh hashes and unchanged original camera/timing/key/control snapshots. Check joint continuity, new part visibility, exact source radius/scale, event/contact sightlines and finite hydraulic clearances in combined consumers.
5. Benchmark representative/peak views and rerender affected frames. Geometry added atX<=-1.44m must be included in occlusion/clearance checks. Do not assume T44 stills establish T45 combined-scene performance or effect readability.

Canonical native T44 consumers: `Reuse_A_continuity_v002.blend`, `Reuse_B_continuity_v002.blend`, `connection_wide_v003.blend`, `furthest_uphole_v002.blend`, under `Records/Tasks/T-044/Revision_v007/Scenes`. The two reuse cameras retain72/96frame timing and all old control values/keys. Wide/furthest are separate static inspections. Default12m far endpoint is outside both intended inspection frames and every original reuse camera frame, with the join continuous to1e-5m tolerance. Recheck any new camera path.

## Review, performance and ownership

389canonical native checks pass. All five retained full first render-to-file measurements are1.55–2.56s at1280x720/EEVEE16/Vulkan on the normal existing GPU disk cache; no warmup render excluded. The original wide was retained when a more perpendicular full-product inspection was added. Empty-cache startup12.55–25.13s remains unresolved; no universal cold-machine claim. Strict5s cap remains.

T44 owns this successor; T45 is the sole Git integrator and receives exact hashes/allow-list. Frozen predecessors and unrelated/T45–T48 files remain untouched. Native .blend files are local/Git-ignored, with no upload or off-machine backup claimed. The successor is available for scoped integration/rechecks; Radzi's new visual approval and any Work dependency gate remain pending. No actual movie shots or film assembly.
