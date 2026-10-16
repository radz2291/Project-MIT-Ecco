# T8 / B202-S — The Measured Envelope

16 October 2026. Task `53fb67d1-e3cb-480e-a910-a544338a4470`; worker `codex-b202s-01a144ac`; run `1046b18c-7351-42b5-ab36-961f9eb99fcc`.

**Current result: three actual-Blender D1 composition proposals, v005. Awaiting Radzi's visual-direction feedback; B202-S is incomplete.** No final still approval, engineering certification, animation or T27 release. The live ticket explicitly requests a cheap A/B/C study before fuller builds. Direct user task instruction authorizes this work. Earlier deleted v001/v002 have not been restored.

Base: `8ea33ce5f83692756d73e688a914b59dbed3aca0`, established `main`, origin `https://github.com/radz2291/Project-MIT-Ecco.git`. Initial tracked tree clean; extensive unrelated local media/scripts preserved. Current task commit is recorded in Rolladice after verified push, avoiding a self-referential SHA edit.

## Review the exact candidate

Local root: `C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco`.

| State | Meaning | Exact still | Editable scene |
|---|---|---|---|
| A | Wall-registered circumference at sensor plane | [A v005](../../../Mechanisms/B202/Previews/Study_v005/B202_A_v005.png) | [A source](../../../Mechanisms/B202/Scenes/B202_study_A_v005.blend) |
| B | Successive sections and derived wall envelope through depth | [B v005](../../../Mechanisms/B202/Previews/Study_v005/B202_B_v005.png) | [B source](../../../Mechanisms/B202/Scenes/B202_study_B_v005.blend) |
| C | White nominal bit-size against blue enlargement | [C v005](../../../Mechanisms/B202/Previews/Study_v005/B202_C_v005.png) | [C source](../../../Mechanisms/B202/Scenes/B202_study_C_v005.blend) |

**Recommendation/question:** retain A/C's shared near-axial comparison and develop B with the reconstructed shape more dominant. Does this composition direction make the measured borehole the payoff, or should B become a more isolated geometry view? This decision is about D1 compositions only.

A/C make the contour/reference comparison readable at true scale; hardware naturally occludes some rear arcs. B establishes depth but its small true-scale washout can still read as a sleeve around a tool. Do not mistake this diagnostic study for the completed accumulation/reconstruction explanation. No arbitrary geometric exaggeration was introduced to hide that problem.

## Sources, implementation and checks

Accepted T5 plugged v002, accepted T6 well/assembly v003, T7 accepted Motion_v005, current live handoff/standard v2 and Measured Envelope discussion. T7 remains unchanged. Actual source files and inherited sensor transforms inspected; official Blender MCP read-only scene query found the running B201 scene. Isolated Blender 5.2.2 processes built these consumers without changing the running scene.

[Single direction contract](../../../Mechanisms/B202/direction.md) applies Scene Director, Directorial Identity and Mechanism Visual Direction Loop. [Source inspection](Evidence/source-inspection_v003.json), [exact build settings](Evidence/build_v005.json), [fresh-open verification and hashes](Evidence/verification_v005.json), [builder](../../../Mechanisms/B202/Scripts/build_study_v005.py), [verification script](../../../Mechanisms/B202/Scripts/verify_study_v005.py).

T6's evaluated authored wall supplies the reconstruction surface and section vertices. Hero contour is interpolated between adjacent T6 rows at X=2.730m: 2m illustrative placement plus .730m inherited sensor reference. No claimed calibrated sampling, acquired field data, live transmission or firing cadence. Ten local presentation meshes preserve exact T5 coordinates/topology and use local quiet shading; source linked library retained. Shared assets are unchanged. Replacement must rebuild the local presentation copies and reverify.

Three saved scenes reopened; **65/65 implementation checks pass**. Checks cover source hashes unchanged, relative library resolution, ten matching T5 meshes, common source-local sensor plane/120° reference angles, contour plane/framing, saved cameras, image dimensions/nonblank content and absent new scene animation. These are implementation self-checks, not independent engineering tests. SHA256 values are in verification JSON. All three v005 renders visually inspected at 960×540; image source/render paths recorded per saved scene. Single-frame previews do not validate rotation, axial travel, accumulation continuity or motion. Render times: A 2.21s, B 1.14s, C 0.75s.

Reproduce from repo root in PowerShell (builder refuses overwrite):

```powershell
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' --background --python '04-Production/Mechanisms/B202/Scripts/build_study_v005.py'
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' --background --python '04-Production/Mechanisms/B202/Scripts/verify_study_v005.py'
```

## Limits and next action

T6 irregular wall is outward-only. **No red tight region exists in these studies.** Develop that as a separately declared illustrative case with clearance checks after D1 feedback; do not squeeze accepted hardware or relabel a nominal segment as tight. Spiral example and distinct yellow/brown echo-amplitude imagery remain unfinished. Geometry must never transform into amplitude. No restricted ENP1 field log was used. O04 acoustic-face/datum/calibration and content-specific O05/O14 questions remain; no new client engineering approval.

B206/T12 questions to carry: interpretation/corrections from sensor stand-off to borehole radius; permissibility/meaning of undersize example with actual hardware/bit; appropriate spiral example and limits of causal claims; amplitude mapping conventions/source and numerical thresholds if later shown. Radzi facilitates technical feedback; this agent has contacted no client.

Next: Radzi reviews this exact D1 candidate; implement bounded feedback, develop remaining still treatments and obtain exact frame approvals. Only then package approved still handover for fresh-agent T27. Keep task in progress/waiting, not whole-ticket Review or Done. No checklist is ticked as complete from this partial composition study.

## Saved and synchronized scope

Current v005 PNGs, scripts, direction, source/build/verification evidence and this report are permitted review material selected for Git synchronization. Blender scenes and prior v003/v004 images stay organized locally under B202; they are not uploaded/backed up by Git. Prior scripts/build evidence retained to explain iterations. Logs stay in T8 Evidence. No task output remains solely in scratch/temp/chat. Asset manifest links this candidate; this is not a new S03 shot or an accepted shared asset.
