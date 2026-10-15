# T-005 / B101 — temporary plug revision v002

15 October 2026. Task `911d2198-d82e-450b-a4f5-a1f6dfb517d9`; rework run `4d82f620-e5d7-443c-baae-d0180ad9bcd8`; worker `codex-t005-plugs-v002-01a13f65`; reviewer Radzi. Authorized by the producer's follow-up relaying the client request to plug holes temporarily while the assembled STEP is pending. Live prerequisites still Done and standard revision 2 unchanged. B101 reopened from Review for this bounded correction; no downstream work started.

## Current review candidate

- [Temporary plugged master v002](../../../Shared/Assets/ECCO/ECCO_master_temporary-plugs_v002.blend), reusable collection ECCO_MASTER_v002.
- [Before/after comparison](Previews/ECCO_temporary-plugs-comparison_v002.png), plus four actual 1280×720 Workbench inspection views.
- [Temporary-part interface and replacement note](../../../Shared/Assets/ECCO/README_v002.md).
- [Build evidence and placements](Evidence/temporary-plugs-build_v002.json), [fresh-open checks](Evidence/temporary-plugs-verification_v002.json), [closure/hashes/links](Evidence/temporary-plugs-closure_v002.json).
- [Preserved v001 report](report_v001.md), original source/master and original evidence retained.

## Changes and validation

Nine removable visualization parts added in ECCO_TEMPORARY_CLOSURES: three imaging caps, three smaller service plugs, three rectangular service covers. Prior First Ping housing was compared by vertex/loop signature with the current preserved source before reusing its presentation components. Mapping reverses the earlier upright presentation into the current source-X coordinate system. Reverse-view QA found the old plates too deep; all three were seated to ray-sampled pad rims and given a temporary 145x80mm footprint covering the pocket extension. These are visual placeholder dimensions only. All additions follow ECCO_ROTATION_X. The supplied housing mesh/topology/transforms and v001 file remain unchanged. Functional axial bore is retained; smaller fastener geometry is not reinterpreted as approved assembly detail.

Fresh saved v002 reopens; source signature and v001 hash match, all nine placements match the intended source transform, and +100mm axial travel / 90° rotation carries closures with error below 0.000001m. No external image/library dependency; source STEP reference resolves. Overview, opposite side, sensing recess and end views inspected visually; before/after comparison confirms seated caps/plates without filling the axial bore. Per-view elapsed render times are in build evidence. An initial post-render evidence write referenced a removed comparison object; log retained, script corrected and rerun successfully. This did not alter the source/v001. These are self-checks, not independent engineering verification.

## Limits and review

Temporary plugs are a producer-authorized visual interpretation. They are not the client's assembled STEP and do not certify all manufacturing holes or active acoustic-face construction. O04 size/datum/mud-sensor uncertainties remain; O14 assembled model is still pending. Review the closure appearance and removable-part approach. When official assembly arrives, compare actual closures and sensor faces, replace temporary parts and reverify affected mechanisms/shots. No client contact or approval is invented.

All outputs are organized under 04-Production. Base commit remains ffa19e6b4792ddc859e8f93da10f8c7e073f2f95 / main, candidate uncommitted; existing v001 changes preserved. New Blender files are local/ignored; no push, publication or remote media backup. Exact local references and limitations will be recorded on the live Rolladice task and finished run for Radzi review. The user's connected default Blender scene is untouched.
