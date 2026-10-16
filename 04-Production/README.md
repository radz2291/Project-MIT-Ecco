# MIT / ECCO — Production workspace

Updated: 16 October 2026. Operating conventions authorized by Radzi; technical content, scope and production acceptance retain their recorded status.

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
5. Save `Records/Tasks/T-<number>/report.md`: stable task ID/number, authority, base commit and exact reviewed artifact versions (record uncommitted state only for interrupted/incomplete work), input versions, output paths, checks/results, review questions, blockers and next action. Include exact commands and inspectable previews where useful. Do not claim independent verification for self-checks.
6. Commit and push the task's permitted tracked outputs under the synchronization rule below. Verify the remote contains the candidate commit. Then update Rolladice with the commit SHA/link, a commit-pinned report link, output references, concise result, checks and limitations. Use relative paths plus machine-local root where needed; do not pretend a local path is a remotely accessible download.
7. Report a finished run and submit completed work to Review under the connector's lifecycle. Incomplete/blocked work stays visibly incomplete. Only Radzi accepts reviewed work as Done. The organization requirement applies to human tasks' supporting agent work too.

### Required commit and remote synchronization

Owner authority: Radzi requested automatic task commit/push for online review and confirmed this rule on 16 October 2026. It supersedes the earlier optional "commit when authorized" closure language for authorized task outputs. It does not authorize unrelated changes or publication of excluded/private material.

- Inspect the checkout, remote URL, branch and upstream before Git writes. Use the established authorized destination in `radz2291/Project-MIT-Ecco`; respect branch protections and any task-specific branch instruction. If no destination is established, record that missing input rather than pushing elsewhere.
- Stage explicit task-owned paths after inspecting the staged diff. Include the review report, implementation scripts, configuration, relevant text/JSON evidence and a small selection of permitted review stills. Exclude credentials, private commercial records, restricted field data and bulk/raw frame sequences. Preserve unrelated staged and unstaged changes; do not absorb them into this task's commit.
- Make a scoped commit and push normally to the authorized remote/branch. No force-push, destructive reset or branch-protection bypass. If behind upstream, integrate safely without discarding user work; handle routine in-scope conflicts and recheck affected outputs.
- Verify using a fresh remote read that the exact candidate commit is reachable on the destination branch. A successful local commit or an unverified push command is insufficient.
- Attach the full candidate SHA and GitHub commit link to Rolladice, plus a report link pinned to that commit. The report describes verified artifact versions/hashes; its own containing commit is recorded in Rolladice to avoid a self-referential commit-hash edit loop.
- Parallel workers must agree on one integrator for Git mutations in a shared checkout. Workers supply exact owned paths and evidence; the integrator commits/pushes the agreed outputs without sweeping unrelated files. Each worker's task waits for the relevant remote commit before Review. Separate worktrees may use task branches, with integration and review lineage made explicit.
- On permission/network/push failure or unresolved destination, save local work and record the exact sync blocker in the task report and Rolladice. End or pause the run truthfully according to the connector lifecycle; keep the task visibly incomplete/blocked rather than submitting a falsely synchronized result. Resume synchronization when possible.

Existing heavy-media exclusions remain in force. Blender binaries, MP4s, caches and renders stay organized locally with exact paths/versions and explicit backup/handover status. Remote review of reports/stills does not imply that local media was uploaded or independently inspected. This rule does not require reopening already accepted historical tasks. No client contact or delivery is implied by task completion.

## B2 pairing amendment — 16 October 2026

Blender supplies grounded baseline stills and actual scene constraints; T26 discusses and critiques them with Radzi, with optional generated references; Blender implements selected bounded changes. Repeat where needed. T26 is an ongoing partner across B2, not a completed-package prerequisite. Follow [B2 paired workflow](B2-VISUAL_APPROVAL.md), which supersedes earlier sequential direction/implementation rules. Technical dependencies remain; approvals apply to specific treatments and motion scope. Preserve T7's completed still phase and authorized continuation.

## Directorial work during development

B1 builds reusable hardware/environment foundations. **B2 requires model-integrated engineering scenes guided by the Scene Director skill and relevant Directorial Identity modules**, including information provenance. Follow the [16 October B2 visual approval amendment](B2-VISUAL_APPROVAL.md): representative framing, coherent explanatory action and editable scenes suitable for direct B3 reuse. Detached schematics remain supporting evidence. B3 adds camera choreography and shot/edit transitions; it does not rebuild B2's explanation.

For **every actual shot in S01–S07**, apply the [rolladice-scene-director skill](../03-Context/00_Skill/rolladice-scene-director/SKILL.md) before construction. Read the [active Directorial Identity index](../03-Context/03_Directorial_Identity/README.md) and relevant modules rather than every document. The old AI Director Interpretation Guide is a superseded pointer. Save one Scene Direction Contract as `Shots/<section>/<shot-id>/direction.md`, using the canonical contract schema. Reference sources, technical uncertainty, camera/composition, information beats, transitions and review stage. Avoid parallel competing shot specifications.

Use cheap SVG/previs where it resolves a concrete ambiguity, then inspect actual moving previews for camera purpose, physical readability, pacing, text/data placement and transitions. B3 must demonstrate direction through motion before final lighting/material work. B301 checks continuity and directorial consistency across those contracts; B401 reviews the exact moving candidate with technical evidence. Finishing applies relevant look/typography modules and preserves accepted shot meaning; substantive changes reopen affected review.

## Current production baseline and incoming plugged ECCO version

**Superseding owner decision, 16 October 2026:** the current T5 plugged master v002 is usable as the production baseline, including final imagery. Accepted T6 well/assembly v003 supports B2. The client is expected to supply only a plugged product revision, not a complete BHA/bit package; the owner's estimate of roughly 5% change is not an inspected dimensional result. Do not wait for that delivery to continue. If it arrives, compare actual differences before deciding whether to replace the baseline.

Use sourced, simplified collars/adapters/bit for surrounding assembly. B3 agents refine only the details visible or necessary for the shot's explanation, within the existing shared asset structure; a separate full engineering BHA reconstruction is not required. Declare authored dimensions/placement and avoid unsupported close-ups or claims of exact threads/operating fit. Keep material mechanism, component-order, movement and fit questions explicit for targeted review. O05/O14 remain traceable without being blanket holds. At B4 record the exact film hardware version and resolve only issues material to retained content, or agree a simpler view/scope. Do not demand unavailable drawings for details neither shown nor claimed.

Historical report, 15 October 2026: the client will provide a new plugged ECCO version. File, delivery date and exact changes are not yet inspected or confirmed. Track this under O14 in the central Decision Register.

B101 must keep replaceable product geometry separate from animation controls, documented sensor references and effects. Choose practical Blender interfaces after inspecting actual files; preserve original source and identify which provisional master/version each proof uses. B102 derives compatible clearances/configurations from inspected dimensions, not from an assumed replacement.

Continue non-blocked foundation and mechanism work using explicitly provisional assets. When the replacement arrives: register source/version and inspect units, dimensions, closures, sensor count/locations and animation interfaces; compare against the current master; create a versioned replacement; check relinking/controls and re-run affected geometry, pulse-contact, clearance, camera/occlusion and continuity checks. Preserve earlier evidence and record affected shots.

Do not automatically overwrite a shared master, invent unavailable geometry or promise a zero-rework swap. Missing replacement data blocks dependent claims/final hardware acceptance where material; it does not automatically block independent preparation. Before B4, record which client-supported product version the retained film depicts and resolve replacement-related issues.

## Development and finishing boundary

Follow [Production Workflow](../03-Context/01_Foundation/05-PRODUCTION_WORKFLOW.md): A readiness → B1 foundation → B2 mechanisms → B3 shots/full animatic → B4 mechanical/technical acceptance → C finishing → D delivery. B2 proves the mechanism; B3 proves the shot communicates it. Deferred rendering is not an excuse to omit moving previews or semantic data colors. No new AI finishing pilot is required before mechanical development.

## Decision provenance

15 October 2026: Radzi authorized integrating Rolladice into repo instructions and required all task outputs to be organized within the actual production folder before closure. This supersedes the earlier proposed separate/external production-store default for locally generated outputs. Existing supplied assets may remain at their inspected source until registered/imported; public Git publication and client distribution remain separate from local saving. This operating amendment does not record MIT engineering approval, a fixed deadline or completion of any production ticket.
