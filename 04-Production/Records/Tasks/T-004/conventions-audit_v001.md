# Production conventions audit v001

15 October 2026 · Local self-check, not independent engineering verification.

Actual checkout: `C:\Users\RZ1\Desktop\RZ\261013-MIT-Ecco`; `main`; origin `https://github.com/radz2291/Project-MIT-Ecco.git`; base `c35e5174aa47e60e0d5204e1e2a87071185968df`.

| Check | Observed result / handling |
|---|---|
| Canonical entry and workspace rules | AGENTS.md, context map and production README read locally; task/pin refreshed through Rolladice. |
| Existing changes | Three foundation documents modified; Records contains A01 and active A02 work. Preserve all. A03 also has a live run. No cross-task register edits. |
| Shared masters | Shared/Assets exists and contains README plus a supplied STEP file. The earlier “reported empty” statement is historical, not current inventory. A02 owns provenance and validation. |
| Current STEP placement | Existing file is directly under Shared/Assets. Do not move it during concurrent inventory. B101 should preserve/copy into an asset-specific Originals directory, register hashes and update references before adopting a master. |
| Mechanisms / shots / edit | Create destinations only when real outputs are produced; absent folders are not missing deliverables for A04. No placeholder Blender scenes. |
| Source protection | Existing source-imported Blender file is outside this checkout and available read-only for future intake; not a validated master. |
| Heavy-file policy | Root .gitignore excludes STEP, Blender, videos, render/cache and Scratch outputs. Local saving does not commit or back up them. |
| Rights | No ENP1 field-log image copied, exported or included. O08/O13 remain canonical decisions. |
| Closure | A04 settings, handoff, report and verification are retained beneath Records; links and proposed timeline arithmetic checked. |

## Versioned path conventions

All paths below are **planned examples**, not files created or proven to work. Prefix with `04-Production/`. Increment version when submitting a changed candidate; never overwrite the reviewed source. Record exact paths and hashes in the owning asset/shot/task record.

| Role | Proposed destination |
|---|---|
| Supplied product original | `Shared/Assets/ECCO/Originals/<exact-supplied-filename>` |
| Reusable product master | `Shared/Assets/ECCO/ECCO_master_v001.blend` |
| Reused script | `Shared/Scripts/<purpose>_v001.py` |
| Product intake script | `Records/Tasks/T-005/Scripts/inspect_master_v001.py` |
| Product inspection preview | `Records/Tasks/T-005/Previews/ECCO_master-inspection_v001.png` |
| Mechanism proof | `Mechanisms/B201/Scenes/B201_echo-proof_v001.blend` |
| Mechanism script | `Mechanisms/B201/Scripts/B201_echo-proof_v001.py` |
| Mechanism playblast | `Mechanisms/B201/Previews/B201_echo-proof_v001.mp4` |
| Shot source / script | `Shots/S02/S02-01/Scenes/S02-01_blocking_v001.blend` / `Shots/S02/S02-01/Scripts/S02-01_blocking_v001.py` |
| Shot playblast | `Shots/S02/S02-01/Previews/S02-01_blocking_v001.mp4` |
| Full edit / preview | `Edit/Projects/ECCO_animatic_v001.<editor-extension>` / `Edit/Previews/ECCO_animatic_v001.mp4` |

`S02-01` is only a naming example; A03 owns the actual shot inventory. Preserve shared geometry in the master and shot animation in shot files. Validate relative links after copying/moving; do not duplicate masters per shot.

## Record ownership

A02 owns the asset manifest; A03 owns shot/blocker registers. A04 owns [preview settings](../../preview-settings_v001.md) and this audit. Global questions remain in the [Decision Register](../../../../03-Context/01_Foundation/06-DECISIONS_AND_READINESS.md). A04 does not create a competing backlog or approval register. Downstream records should reference this exact settings version, then record any confirmed replacement version and its impact on frame mapping, previews and edit.
