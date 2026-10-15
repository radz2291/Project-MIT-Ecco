# First foundation execution handoff — B101 / T-005, v001

Prepared by A04, 15 October 2026. **Preparation only; B101 has not been started or authorized by this handoff.**

Target live task: `911d2198-d82e-450b-a4f5-a1f6dfb517d9` — B101 Validate product master and sensor configuration. Reviewer Radzi. At A04 inspection it is todo, dependent on A02/T-002 and A04/T-004, neither accepted yet. Re-read live handoff, dependency states and latest pinned standard before claiming. Obtain direct bounded execution authority; do not bypass prerequisites.

## Actual accessible inputs

- [Existing supplied STEP](../../../Shared/Assets/PZ12-8301%20Main%20Housing%20ENP3%20_A_%20Modified%20TFA%20_5_%20Ready%20_TC.stp): present, 4,606,150 bytes at A04 inspection. Presence is not confirmation of product identity, scale or sensor configuration. A02 owns source registration.
- External local candidate: `C:\Users\RZ1\Desktop\RZ\261008-MIT-Ecco\04-Project\01-ECCO_First_Ping-Test\01-Blender\Source_Imported_ecco.blend`. File presence verified; A04 has not opened or inspected its scene.
- [A02 source-import inspection](../T-002/Evidence/source-imported_v001.json): current saved evidence, not accepted engineering. Records Blender 5.2.2 LTS, 24 fps and a single mesh. Reconcile with A02's completed manifest before use; do not infer sensor correctness from one mesh.
- [Engineering baseline](../../../../03-Context/01_Foundation/02-ENGINEERING_BASELINE.md), [decision register](../../../../03-Context/01_Foundation/06-DECISIONS_AND_READINESS.md), [workflow](../../../../03-Context/01_Foundation/05-PRODUCTION_WORKFLOW.md), [workspace rules](../../../README.md) and [proposed preview profile](../../preview-settings_v001.md).

Blender executable exists at `C:\Program Files\Blender Foundation\Blender 5.2\blender.exe`. Running Blender bridge availability was not tested by A04 because no running-scene work is needed here. Before interacting with the user's scene, use official `blender` MCP and a read-only query. Connection failure permits records/inspection preparation, not fabricated scene access.

## Bounded execution after release

1. Read fresh A02 outputs and hash actual inputs. Preserve originals. Use `Shared/Assets/ECCO/Originals/` for imported copies and verify byte identity. Do not move the currently inventoried STEP without reconciling references.
2. Inspect geometry, units, transforms, axes and component boundaries against source evidence; record product/sensor uncertainties under O04. Do not invent sensor details or split hardware by guesswork.
3. Save an editable reusable master only to the supported level. Record component interfaces required for rotation/scanning/cutaways; preserve source geometry and label provisional interpretations.
4. Produce simple inspection views, measured dimensions, source/master hashes and link checks. An inspection turntable may be used if useful, following the confirmed profile; no cinematic mechanism or final finishing in this task.
5. Save report and output manifest, attach exact references/checks to B101 and submit Review. No self-acceptance. Unresolved critical geometry issues keep dependent construction blocked.

## Planned output contract

These paths are **not yet produced**:

- `04-Production/Shared/Assets/ECCO/ECCO_master_v001.blend`
- `04-Production/Records/Tasks/T-005/Scripts/inspect_master_v001.py` if a script is needed.
- `04-Production/Records/Tasks/T-005/Previews/ECCO_master-inspection_v001.png` plus additional views with exact indices.
- `04-Production/Records/Tasks/T-005/master-verification_v001.json` and `report.md`.
- Update the actual A02 manifest with provenance/version, copy location, permissions/limits, affected shots and master readiness; do not claim MIT approval.

Exit checks: originals unchanged; unit/scale evidence; source-to-master geometry correspondence; supported component/sensor configuration; saved source reopens; dependencies resolve; views match saved master; uncertainties assigned with exit evidence. Hashes and file-presence evidence for this handoff are in [verification](verification_v001.json).
