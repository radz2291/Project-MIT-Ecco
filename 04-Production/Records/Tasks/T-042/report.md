# P01 shared component plan for the V3 film

**Review candidate v001, 18 October 2026.** Reuse T5 plugged ECCO v002 and T6 well v003, adapt existing mechanism proofs into shared components, and build the missing surface, film graphics and data-unwrapping pieces. All 22 V3 shots are mapped across 12 component groups and the full 90 seconds.

**Next proposed ticket: D-FILM, shared visual decisions and V3 shot instructions, owned by a separate AI directing agent.** Release its component decisions progressively, then build the five proposed asset packages and individual shots. Radzi alone assembles/edits the film, integrates narration/sound and handles client feedback.

## Review package

- [Shared component register](component-register_v001.md): reuse/refine/build decisions, canonical locations, controls, linking and revision propagation.
- [Build order and render gate](build-plan_v001.md): five proposed asset packages, shot release order, consequential decisions and strict under-5-second-per-frame benchmark procedure.
- [22 shot instruction placeholders](direction-placeholders_v001.md): source-linked slots for the directing agent; [machine-readable consumer map](shot-map_v001.json).
- [Saved asset inspection](Evidence/asset-inspection_v001.json) and [live board source index](Evidence/source-index_v001.json).
- [Package verification](Evidence/package-verification_v001.json).

## Findings that affect production

1. Eleven selected native files open in Blender 5.2.2 in isolation, with resolved linked libraries, no reported missing image dependencies and unchanged file hashes. This checks access and interfaces; it does not re-certify earlier geometry/animation or benchmark new shots.
2. Existing T6 BHA uses generic collars/adapters and a bit-gauge ring. Surface scenery, visible bit/shoe detail and reusable well-fluid treatment need bounded work after direction. The production baseline permits simplified hardware; a complete client BHA package is not a prerequisite.
3. B201 v006 and B202-M v007b remain review candidates. B203 support/channel/wear are standalone explanatory sections; they need actual product integration and common controls. B204 is a circulation-only illustration with unresolved CAD stage mapping. Reuse the evidence and logic, preserving those limits.
4. S06 needs a new deterministic unwrap adapter using the same depth/azimuth samples. S06-C/S07-A need permitted output or a clearly labeled demonstration; fictional screen contents and restricted ENP1 report pixels are excluded.
5. The supplied original MIT logo exists in V3. Its final icon/full-logo lockup is still a decision. Camera, lighting, effects appearance and graphic execution remain explicitly unfilled directing-agent slots.

## Authority and inspection record

Task **T42 / P01**, ID `8dee7aec-9270-460f-84a6-6a4450b74e69`, active MIT ECCO project `a0b9b971-e282-42f0-a25f-0c78729eff87`. Direct owner assignment in this chat authorizes planning. Fresh Work handoff: no dependencies; current standard `2c80cc39-8e66-46a2-b2c9-862ba00df080` revision 1. Run `c8d3a597-8df8-412d-b4ac-8c1642da5a3a`, worker `codex-p01-t42-20261018`.

Read live V3 board `8466dd02-7299-4e68-85fc-f95d0d61931e`, revision 14: start guide, seven sequence guides and all 22 shot cards. Source-index records exact card/version IDs. Read engineering baseline, decision register, client feedback C01–C09 and T5/T6/T7/T8/T9/T10/T27 source/interface records. No new technical claims depend on external research.

The live 18 October standard supersedes older mechanical-first/B2/still-animation/editable-storyboard workflow gates. Before synchronization, four owner-cycle documentation commits were fetched and fast-forwarded to `8bfab793e9b8dc601b287d2ef7916959fc4551d7`; the updated AGENTS and production README now match this plan. P01 does not resume retired tasks or create a competing roadmap. Source facts and publication restrictions still apply.

Initial checkout: clean `main`, upstream origin/main, base `c4f882e971b316656ac7b9dbeb961908f6238620`, authorized remote `https://github.com/radz2291/Project-MIT-Ecco.git`. All P01 outputs are under `04-Production/Records/Tasks/T-042/`. Local project root is `C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco`.

Official Blender Lab MCP read-only query could not connect at `127.0.0.1:9876`. Saved-file inspection used the installed Blender executable in a separate background process, scripts disabled when opening each scene, with no scene save or render. Reproduce the inventory with:

```powershell
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' --background --factory-startup --python '04-Production/Records/Tasks/T-042/Scripts/inspect_assets_v001.py'
```

No production scene, visual treatment, moving preview, render benchmark or downstream ticket was created. The benchmark protocol is prepared; actual speed and new-shot readability remain to be tested in execution. Historical heavy assets remain organized local-only and ignored by Git.

## Review and synchronization

Radzi reviews the component grouping, proposed next directing ticket and build order. The proposal preserves V3 timing, source constraints and Radzi's sole assembly role. No self-acceptance or engineering/client approval is implied.

Package verification passes 121 coverage, placeholder, path, source-preservation and asset-availability checks. All 11 data cases' indexed files exist and the B202 registered T5/T6 hashes match the inspected sources. These are executor self-checks, not a new data-model or render-performance validation.

Only this task's explicit text/JSON/script files are synchronized. The containing candidate commit, pinned report link and fresh remote verification are attached to Rolladice after push. No heavy scenes, videos or restricted report imagery are published. Revisions to this plan should preserve v001 evidence and update the consumer map consistently.
