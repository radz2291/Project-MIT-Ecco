# ECCO-049 — Shared-asset reconciliation

27 October 2026 · **C03/C04 grouping and C07 hydraulic source recorded — report only** · remaining selections stay in Review

**Start with the [image-led comparison](comparison.md) or [visual review page](review.html).** The [inventory](inventory.md), [source index](source-index.md) and [image index](image-index.md) provide the supporting detail.

The completed S01–S07 previs is the current visual baseline. Retain the common ECCO geometry and connected BHA reference; use S05 previs v020 as Radzi's selected hydraulic source and S07's clean satin finish as a candidate appearance reference. Keep camera-dependent cutaways, lights, event timing and separate data cases local. This is a component-selection proposal, with no scene migration or polishing.

## C03 — combine well environment and formation

**Owner-requested report proposal, 27 October 2026:** combine the existing well environment and formation assets into **one modular shared environment** intended for reuse across scenes. This supersedes the earlier C03 blanket “keep local” recommendation. The [decision record](owner-decisions.json) preserves Radzi's exact instruction and the scope of this amendment.

Use the existing World environment v009, Formation context v002 and Formation cased-section v002 as source packages. Reconcile their overlapping rock/casing/cement with the CasedHole layers; provide optional surface context where needed. The future master should expose separate controls for rock, borehole variants, casing, cement/channel/wear, mud, near/wide extents, detail and viewing access. Each scene can use the required parts from the common source.

**Physical-asset grouping:** casing, cement, channel and wear geometry (C04) belong within the well environment (C03). C04 is retained as a detail/comparison subsection, not a separate peer environment asset. The existing CasedHole v002 library supplies these objects; support/retrieval and pulse-response animation are separate demonstrations of their use. This is a report classification correction only.

Keep the original assets and approved shot cameras, lenses, motion, timing, local lighting and cutaway choices. Keep illustrative reconstruction/data cases distinct from physical environment geometry. Reuse across scenes is the design goal; each consumer still needs axis/unit, duplicate-layer, clearance, locked-camera and render-cost checks before adoption.

Radzi explicitly clarified: “I don't want you to combine yet. There's no implementation here. This is just for the report.” This update changes the report and review documents only. No asset implementation is authorized. No environment master has been built, no source/shot relinked, and no downstream ticket created. A later bounded build release will define the exact package and migration scope. Other component choices and acceptance of completed work remain with Radzi.

## C07 — hydraulic source selected

Radzi instructed: “For the hydraulic, We use the previs section five hydraulic.” Record **Section 5 previs v020** as the selected source for hydraulic appearance and motion: amber fluid/trails, cuttings and existing flow behavior. The earlier shared Hydraulics v003 package remains preserved historical comparison, not the selected source. Exact native/video paths and approved hashes are in [owner-decisions.json](owner-decisions.json).

This is a report-only source selection. No extraction, consolidation, polishing, camera/timing change or migration has been authorized or performed. Preserve the approved S05 source and its behavior.

## Authority and sources

- MIT ECCO task `893e2262-914e-4330-bd33-bcd2e0955290`, reference **ECCO-049**; direct owner assignment in this chat. Live ticket/handoff and discussion read at revision 773; no comments/dependencies, pinned production standard revision 1 current. Newer ticket scope explicitly supersedes the earlier assets-before-shots sequence.
- Work run `7420d077-4a27-41c6-ad4b-ddf3e8284c78`, worker `codex-ecco049-reconciliation`. Claimed before execution and maintained with progress heartbeats.
- This documentation follow-up was directly requested during owner review. Work rejected a new run because the ticket is “already complete or awaiting review”; the original run stays finished and the ticket stays Review. Only reviewed documents and references are amended.
- Inspected production checkout: `C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco`, branch `main`, base `bb9a503c8d69ae0cf5ba20273a5280d130cc1949`. Four unrelated modified direction files and existing untracked work were preserved.
- GitHub `origin/main` was 41 commits ahead at `5f6b18f642d456815f5779a2f7b3a82964abb97e`. Review integration uses the isolated `codex/ecco049-asset-reconciliation` branch from that remote base in `C:/Users/RZ1/.codex/worktrees/ecco049-review/261013-MIT-Ecco`. Only T-049 files are published; the production checkout is not advanced or cleaned.
- Read current AGENTS/production rules, Engineering Baseline/Decision Register, T42 component register, T43 shared direction, T44 canonical continuity interface/manifest, and T45–T48 releases/reports. Live Work has T44 Done and T45–T48 Review. Those packages remain comparison sources, not newly accepted replacements.

## Results and verification

- Located selected **S01 Gentle-10s-Finish, S02 v011, S03 v036, S04 v033, S05 v020, S06 polished v004, S07 v006**, with recorded approval/closure evidence. S04 v034 is rejected; its dark-band/pit concern remains unresolved in selected v033. [Selection evidence](Evidence/selection-evidence.json) preserves the source texts/hashes.
- Reopened **25 saved natives** in separate Blender 5.2.2 background processes with auto-execution disabled. All listed libraries exist, and every inspected source retains its pre-inspection hash. Packed/external image and font references, camera/lens animation fingerprints and object/material ownership are recorded in the [source audit](Evidence/source-audit.json) and [source lock](Evidence/source-lock.json).
- Common housing fingerprint matches the 348876-vertex film source in S01/S02/S04/S05/S06/S07. All visible canonical closure mesh shapes are also present; S05 omits the hidden cutter-preview mesh. Matching raw geometry does not establish equal materials, transforms, evaluated fit or engineering approval.
- **Seven selected review movies fully decoded: 2376 frames, no decode errors.** The [media audit](Evidence/media-audit.json) records hashes/counts. Thirty selected image derivatives plus four labeled sheets were visually inspected. [Image manifest](Evidence/image-manifest.json) records exact source movies/stills, native views, frame offsets and derivative hashes. S02's review excerpt begins at native frame169 and reuses S01 frames169–240; extraction samples are within S02 itself.
- Actual ownership differs: S01/S02 retain linked product geometry; S04 combines shared libraries with local display derivatives; S05/S06/S07 use local product copies. S05's residual ECCO library entry has no linked object datablocks. [Object member map](Evidence/component-members.json) and [geometry matches](Evidence/geometry-matches.json) distinguish these from planned consumer lists. Datablock duplicates are not simultaneous rendered-instance counts.
- **No new rendering.** Existing previews were adequate, so no diagnostic render cost or new <5s/frame benchmark is claimed. Historical costs/cache limitations remain in source records. No source save, camera/lens edit, material change, relink, retime, rebuild or film assembly occurred. The live Blender Acoustics_v003 scene was dirty; official MCP access was verified read-only and its unsaved state was left untouched.
- [Packet verification](Evidence/verification.json) passes 487 checks after the report amendments (original packet: 483 checks) covering local links, selected image/native correspondence, hashes, dependency paths, media evidence and script syntax. The retained [initial check](Evidence/verification-initial.json) flagged only its own not-yet-written verification file; the completed packet passes. Checks are executor evidence, not independent review.

## Review and limits

The [short proposal](comparison.md) contains the nine-row comparison, two remaining selection questions and a bounded later consolidation order. No downstream tickets were created. Current section allocations total **96 seconds** after S05's approved expansion; Radzi retains film timing, logo, audio, assembly and client communication.

Source length/temporary closures, unverified hydraulic stage/end mapping, illustrative sensing/flow/data, and the distinction between S03 and S06 cases remain explicit. No restricted field-log pixels were copied into the review packet. No calibrated acoustics, CFD, certified assembly/thread fit, field-output provenance, client acceptance or final-film approval is asserted.

All retained T-049 outputs are under this task folder. Detailed native dumps and selection diagnostics stay local; compact evidence, scripts, reports and selected comparison JPEGs are published. Heavy source natives/videos remain at the exact local paths in the source index. Earlier D-drive recovery statements were read, not re-audited; no new media backup/upload or off-machine recovery is claimed.

**Next action:** retain the C03 consolidation proposal in the report for future discussion; Radzi reviews the remaining component choices. Actual consolidation/polishing requires its later bounded build release. The containing commit SHA, branch, pinned report and visual index are attached to Work after fresh remote verification; this report does not embed its own containing hash.

## Reproduce inspection

From the production root, use Blender `--background --disable-autoexec --python 04-Production/Records/Tasks/T-049/Scripts/inspect_sources.py`, then the bundled Python runtime for `Scripts/summarize.py`, `Scripts/prepare_images.py`, `Scripts/build_review.py` and `Scripts/verify_packet.py`. The image script decodes existing movies; it does not render. Generated full native dumps remain local and ignored. Regeneration requires the original local media and therefore cannot run from the lightweight review worktree alone.
