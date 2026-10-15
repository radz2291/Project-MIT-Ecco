# MIT / ECCO — Production workspace

Updated: 15 October 2026. Operating conventions authorized by Radzi; technical content, scope and production acceptance retain their recorded status.

## Root and ownership

The producer identifies the local working repository as `C:\Users\RZ1\Desktop\RZ\261013-MIT-Ecco`. Work in its `04-Production` directory. `Shared/Assets` already exists locally and is reported empty; this remote documentation update does not inspect or populate the Windows filesystem. Use the actual checkout root when working elsewhere; portable records use repository-relative paths and exact case.

- Rolladice Work / project **MIT ECCO** (ID `c04ff6c8-4447-4ad1-ada8-09a2c9a5d4a6`) owns live tickets, assignments, dependencies, pinned standards, runs, review and acceptance.
- GitHub/repository owns technical sources, decisions, editable implementation, scripts and evidence records. Existing `01-Brief`, `02-Reference` and `03-Context` remain canonical for their subjects.
- Local production media belongs inside this checkout even when ignored by Git. A file on disk is not necessarily committed, pushed or backed up. Record those distinctions.
- The central [Decision Register](../03-Context/01_Foundation/06-DECISIONS_AND_READINESS.md) owns global technical questions and approval evidence. The production blocker register references its decision IDs instead of maintaining contradictory approval states.
- Do not copy the live ticket backlog into a competing repo status file. Link each execution report to its stable Rolladice task ID and number.

## Folder destinations

Create folders as needed; do not create empty production scenes or claim assets exist because a directory exists.

| Path beneath 04-Production | Purpose |
|---|---|
| `Shared/Assets/<asset-name>/` | Reusable product, well, assembly, effects and branding masters; preserve supplied originals in an `Originals/` subfolder when imported |
| `Shared/Scripts/` | Scripts/configuration genuinely reused by multiple mechanisms or shots |
| `Mechanisms/<mechanism-id>/Scenes/` | Standalone mechanism proofs, e.g. B201 pulse/echo |
| `Mechanisms/<mechanism-id>/Scripts/` | Mechanism-specific implementation |
| `Mechanisms/<mechanism-id>/Previews/` | Moving tests and inspection frames |
| `Shots/S01/S01-01/` through `Shots/S07/<shot-id>/` | Shot-specific `Scenes/`, `Scripts/`, `Graphics/`, `Previews/` and later `Renders/` |
| `Edit/Projects/`, `Edit/Previews/` | Editable assembly/timeline and versioned full-film previews |
| `Delivery/<version>/` | Agreed masters, compressed copies and source handover package |
| `Records/` | Asset manifest, shot register, blocker register and confirmed preview settings |
| `Records/Tasks/T-<number>/` | Task report, review questions, verification evidence and recovery/sync notes |
| `Scratch/T-<number>/` | Disposable task experiments; never the sole location of a deliverable |

Use zero-padded task folders, e.g. `T-002`. For a task with no production scene, its report in `Records/Tasks/T-002/` is sufficient. A02 produces the asset manifest, A03 the shot/blocker registers, and A04 validates settings and these conventions against the actual checkout. Do not fabricate their contents now.

Use meaningful versioned names such as `S02-01_blocking_v001.blend` and `B201_echo-proof_v001.mp4`. Record which version is under review; avoid `final-final` naming. Prefer relative Blender links (within the project), preserve source masters and validate links after moving files. Do not duplicate shared masters into every shot.

## Start an authorized task

1. Read root AGENTS.md and the relevant context route. Inspect repository identity, branch, base commit and working tree; preserve unrelated user changes.
2. Read the live MIT ECCO ticket plus a fresh handoff through Rolladice Work. Inspect dependencies, latest pinned standards, inputs and criteria; a pasted handoff is a starting reference, not proof that live state is unchanged.
3. The producer's instruction to execute a particular ticket authorizes its bounded work. It does not approve unknown engineering or authorize all downstream tickets. Preparing a handoff or scheduling a ticket alone does not launch Codex or authorize broader scope.
4. Check asset access and tool availability. Resolve any stale standard pin against the actual latest requirements; never blindly acknowledge a changed requirement. Do not bypass incomplete dependencies.
5. Claim through `run_start` with a stable worker identity before ticket execution. Follow the connector's current API. Read the latest workspace revision before each write, use unique operation IDs and reuse the same ID on retries.
6. Report through `run_update` with the returned run ID and the same worker identity; heartbeat every few minutes. Leases expire after 15 minutes. If another worker owns the task or the lease is lost, stop ticket mutations and resolve ownership before resuming.
7. Execute and verify within the ticket scope. Continue routine in-scope repairs without repeated permission requests. Record precise blockers; continue independent authorized work when safe. Do not start another ticket without authority for it.

If the connector is unavailable before claiming, perform only inspection/preparation unless Radzi has explicitly authorized offline execution. For an outage during an owned run, preserve authorized work and a dated recovery note in the task record; do not claim successful remote synchronization or exclusive ownership. Reconcile live state/lease before resuming shared execution.

## Division of work and review loops

Agents prepare source summaries, handoffs, preview/question packets, implementation, corrections and records. Radzi supplies unavailable local inputs, makes scope/taste decisions, communicates with MIT, and accepts reviewed work. Engineering confirmation comes from supported sources/MIT; no agent can invent it.

A01 is agent preparation, with Radzi confirming its scope summary in review. Mechanism tickets prepare the material for human B206 feedback. B301 prepares the complete review cut for human B401 acceptance. Human review feedback returns as bounded rework to the responsible agent ticket (or an explicitly scoped follow-up); preserve previous evidence and recheck dependent shots. Reopen changed prerequisites rather than leaving dependent acceptance apparently valid. D01 owns human final direction/client review, while supported technical preparation/corrections belong to C01/C02 or a scoped follow-up.

## Mandatory task closure

Before submitting any agent task to Review, or ending a blocked/failed run:

1. Save every retained output in the correct production destination. Organize scripts, scenes, graphics and previews; no deliverable may exist only in desktop/temp/scratch/chat output.
2. Remove only disposable files created by this task when safe; retain useful failed attempts and evidence in a labeled location. Never delete user work to tidy the project.
3. Verify saved files exist, editable sources open where tools permit, dependencies/relative links resolve, and the preview represents the saved candidate. State checks that could not be performed.
4. Update relevant manifests/registers with paths, versions, provenance and affected shots. Separate local-only/ignored media from tracked artifacts. Inspect `git status` and the intended diff; do not force-add media or restricted assets.
5. Save `Records/Tasks/T-<number>/report.md`: stable task ID/number, authority, base and candidate commit (or explicit uncommitted state), input versions, output paths, checks/results, review questions, blockers and next action. Include exact commands and inspectable previews where useful. Do not claim independent verification for self-checks.
6. Update Rolladice with output references, concise result, checks and limitations. Use relative paths plus machine-local root where needed; do not pretend a local path is a remotely accessible download.
7. Report a finished run and submit completed work to Review under the connector's lifecycle. Incomplete/blocked work stays visibly incomplete. Only Radzi accepts reviewed work as Done. The organization requirement applies to human tasks' supporting agent work too.

For tracked text/scripts/evidence, make a scoped commit when authorized; push only to the authorized destination. Existing heavy-media exclusions remain in force. Ignored Blender files, previews, caches and renders still need organized local storage and explicit handover/backup status. No client contact or delivery is implied by task completion.

## Development and finishing boundary

Follow [Production Workflow](../03-Context/01_Foundation/05-PRODUCTION_WORKFLOW.md): A readiness → B1 foundation → B2 mechanisms → B3 shots/full animatic → B4 mechanical/technical acceptance → C finishing → D delivery. B2 proves the mechanism; B3 proves the shot communicates it. Deferred rendering is not an excuse to omit moving previews or semantic data colors. No new AI finishing pilot is required before mechanical development.

## Decision provenance

15 October 2026: Radzi authorized integrating Rolladice into repo instructions and required all task outputs to be organized within the actual production folder before closure. This supersedes the earlier proposed separate/external production-store default for locally generated outputs. Existing supplied assets may remain at their inspected source until registered/imported; public Git publication and client distribution remain separate from local saving. This operating amendment does not record MIT engineering approval, a fixed deadline or completion of any production ticket.
