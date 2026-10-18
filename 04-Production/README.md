# MIT / ECCO — Production workspace

## Current cycle and ownership — 18 October 2026

OWNER-AUTHORIZED CURRENT CYCLE — 18 October 2026. Supersedes earlier mechanical-first, B2 pairing, separate still/animation and editable 3D storyboard gates. T31 is completed. Visual source: ECCO - Cinematic Film Storyboard, board ID 8466dd02-7299-4e68-85fc-f95d0d61931e; V3, 22 shots S01-A through S07-C, seven sequences, 90 seconds. Repository source: 03-Context/02_Storyboard/V3/; board/source mapping: 04-Production/Records/Storyboard-Board-V3/README.md.

Cycle: shared-component planning → shared assets and AI-director execution instructions → actual movie shots using fast renders → Radzi assembles film and handles client feedback → affected shot/shared-asset revisions → delivery. Radzi alone owns film assembly/editing, narration/sound integration and final timeline. Agents deliver individual shots and organized editable sources; no agent film assembly ticket.

Planning/orchestration creates placeholders only for visual instructions. A separate AI directing agent owns visual treatments and shot execution instructions using the V3 board, Scene Director skill and Directorial Identity. Blender executes approved instructions. Mechanical boards remain engineering information references.

Shared assets must have canonical masters, stable controls, source/version records, relative links and a shot-consumer map. Decide hardware/BHA/bit, environment, pulse/contact/echo and graphic treatment consistently before dependent shot builds. Reuse verified existing work; do not assume historical acceptance covers new uses. A shared revision propagates through references, then affected shots are checked/rerendered.

Current shot-production render budget: STRICTLY LESS THAN 5 SECONDS PER FRAME on the executing machine at the chosen working settings. Benchmark representative and heaviest frames before batch rendering; record settings and timings. Reduce cost if the limit fails; do not silently raise the cap. This is fast-render actual movie production, not expensive final rendering. Any later expensive delivery-render stage requires a separate owner decision.

Preserve engineering/client constraints, provenance and useful prior evidence. No invented technical approval. Save under 04-Production; masters in Shared/Assets; use V3 shot IDs and map historical IDs explicitly. Commit/push permitted tracked records/scripts/config/evidence, verify remote, attach exact report/commit and local media paths. Heavy/restricted media exclusions remain. Only Radzi accepts results. Only one planning ticket is created now; propose later build/directing/shot tickets after inventory, do not create or execute them automatically.

Active Work project ID: `a0b9b971-e282-42f0-a25f-0c78729eff87`. The prior MIT ECCO and PREVIS projects are archived; their unfinished tickets and old gates are superseded. T42/P01 is the sole new planning ticket. This section supersedes historical B2/B3/B4 phase references below and elsewhere. Source constraints and asset evidence remain valid within their recorded limits.


Updated: 18 October 2026. Operating conventions authorized by Radzi; technical content, scope and production acceptance retain their recorded status.

## Root and ownership

The producer identifies the local working repository as `C:\Users\RZ1\Desktop\RZ\261013-MIT-Ecco`. Work in its `04-Production` directory. Existing shared assets must be inspected in the actual checkout; remote documentation does not inspect the Windows filesystem. Use the actual checkout root when working elsewhere; portable records use repository-relative paths and exact case.

- Rolladice Work / project **MIT ECCO** (ID `a0b9b971-e282-42f0-a25f-0c78729eff87`) owns live tickets, assignments, dependencies, pinned standards, runs, review and acceptance.
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
| `Shots/<section>/<V3-shot-id>/`, e.g. `Shots/S02/S02-A/` | Shot-specific `Scenes/`, `Scripts/`, `Graphics/`, `Previews/` and later `Renders/` |
| `Edit/Projects/`, `Edit/Previews/` | Radzi-owned assembly/timeline and full-film previews; agents do not edit or assemble the film |
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

## Current production baseline and incoming plugged ECCO version

**Superseding owner decision, 16 October 2026:** the current T5 plugged master v002 is usable as the production baseline, including final imagery. Accepted T6 well/assembly v003 supports B2. The client is expected to supply only a plugged product revision, not a complete BHA/bit package; the owner's estimate of roughly 5% change is not an inspected dimensional result. Do not wait for that delivery to continue. If it arrives, compare actual differences before deciding whether to replace the baseline.

Use sourced, simplified collars/adapters/bit for surrounding assembly. B3 agents refine only the details visible or necessary for the shot's explanation, within the existing shared asset structure; a separate full engineering BHA reconstruction is not required. Declare authored dimensions/placement and avoid unsupported close-ups or claims of exact threads/operating fit. Keep material mechanism, component-order, movement and fit questions explicit for targeted review. O05/O14 remain traceable without being blanket holds. At B4 record the exact film hardware version and resolve only issues material to retained content, or agree a simpler view/scope. Do not demand unavailable drawings for details neither shown nor claimed.

Historical report, 15 October 2026: the client will provide a new plugged ECCO version. File, delivery date and exact changes are not yet inspected or confirmed. Track this under O14 in the central Decision Register.

B101 must keep replaceable product geometry separate from animation controls, documented sensor references and effects. Choose practical Blender interfaces after inspecting actual files; preserve original source and identify which provisional master/version each proof uses. B102 derives compatible clearances/configurations from inspected dimensions, not from an assumed replacement.

Continue non-blocked foundation and mechanism work using explicitly provisional assets. When the replacement arrives: register source/version and inspect units, dimensions, closures, sensor count/locations and animation interfaces; compare against the current master; create a versioned replacement; check relinking/controls and re-run affected geometry, pulse-contact, clearance, camera/occlusion and continuity checks. Preserve earlier evidence and record affected shots.

Do not automatically overwrite a shared master, invent unavailable geometry or promise a zero-rework swap. Missing replacement data blocks dependent claims/final hardware acceptance where material; it does not automatically block independent preparation. Before B4, record which client-supported product version the retained film depicts and resolve replacement-related issues.

## Decision provenance

15 October 2026: Radzi authorized integrating Rolladice into repo instructions and required all task outputs to be organized within the actual production folder before closure. This supersedes the earlier proposed separate/external production-store default for locally generated outputs. Existing supplied assets may remain at their inspected source until registered/imported; public Git publication and client distribution remain separate from local saving. This operating amendment does not record MIT engineering approval, a fixed deadline or completion of any production ticket.
