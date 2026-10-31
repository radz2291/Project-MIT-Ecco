# ECCO-051 — Shared asset integration

Current surface/World revision: [31 October v006 review](../T-055/Revision_v006/report.md). Surface v006, World v011 and connected demo v002 supersede the surface/continuity package descriptions below. Pinned World v010 consumers remain unchanged.

30 October 2026. **Implementation complete for shared-asset review; final native inspection/acceptance remains with Radzi.** Controlling input is ECCO-050 at commit `58013a6f5a907bfdfe9a7c7d63405e3306c2c42c`. The five delegated packages preserve locked source scenes and publish successor masters plus separate consumer copies. Later completion sections supersede historical incomplete status below.

## Package status

| Package | Verified result | Remaining |
|---|---|---|
| [052 hardware / finish](../T-052/report.md) | Satin master, ECCO v003, BHA core satin v001 and BHA v008; actual S07/S05/S02 saved consumers; geometry preserved; shared edit propagation; motion and still checks | Owner appearance review |
| [053 physical World](../T-053/report.md) | World v010 with exact irregular S02 wall, documented transforms and extents; S02/T44 consumers; shared edit propagation | Owner appearance review |
| [054 digital / reveal](../T-054/report-v004.md) | V004 exact cap-topology correction, shared contextual-line library, preserved S02/S06 behavior; camera/data/link and propagation checks pass | Owner visually approved v004; final native-file inspection remains |
| [055 surface / descent](../T-055/report.md) | Surface v005; actual S01/S02 consumers; seabed join, axial view opening and motion checked; shared edit propagation | Owner appearance review; opening is illustrative, not internal engineering geometry |
| [056 acoustic waveform](../T-056/report.md) | V014 live native controls match provisionally approved v013; open/cased presets, S02/S04 copies, shared/local controls and preserved source checks pass | Owner native inspection/final acceptance |

## Independent review

Master reopened source and consumer natives in isolated Blender processes and compared sampled evaluated cameras/lenses, frame ranges, fps and library resolution. Checks pass for 052,053,054,055. Native source hashes remained unchanged. Visual review includes actual S07/S05 hardware, S02 string, BHA controls, S02/T44 physical context, S01/S02 subsea passage, deep transition, S03/S06 context and successive waveform proofs. Defects and failed render attempts are retained rather than counted as successes.

Benchmarks and batches use working preview settings, not full-resolution delivery settings. Selected hardware32-sample640x360 proofs peaked2.619s; 052 motion1.331s; 053 coverage1.829s; final055 subsea motion1.893s; 054 reveal motion2.185s. Initial054 S06 13.741s and blank-image attempts were failures. Every retained passing proof uses full render-to-file timing below5s/frame. A single queue serializes rendering.

## Scope and storage

Original seven-section scenes and unrelated working changes are preserved. Local native masters/consumer paths and SHA256 values are in each package's manifest. Heavy Blender files, movies and frame caches remain local and ignored; no off-machine backup or remote native access is claimed. Selected stills, scripts and reports are published on `codex/ecco051-shared-assets` through one integrator. Exact verified commit links are attached after push.

First publication: `a86990614ce100354a7da6c1bd6d26bcaf2ad110` on `codex/ecco051-shared-assets`; local HEAD and remote branch matched after push. ECCO-052,053,055 are now in Work Review with commit-pinned reports. Original main checkout remains unchanged by Git integration. ECCO-054,056 and master are incomplete.

Waveform v007 uses explicitly assumed one-dimensional pressure samples, not measured ECCO RF. Master independently tested actual sample changes for propagation speed, distance, reflection sign/strength and superposition. Reopened native camera/range/fps/source hashes and relative libraries pass. The105frame4.375second slow-review clip passed max2.353s/frame, after three representative benchmarks max2.628s. Reviewed outbound/contact/return stills show luminous pressure-sign bands and a weaker return. Fine grain and simplified fixture lighting remain; this is representation proof, not final cinematic finishing.

This is shared-asset preparation and focused consumer proof work. It does not assemble or deliver the film, certify the engineering, supply measured ECCO waveform data, or imply Radzi/client approval. Master remains active while054/056 are unresolved.

## Owner-directed ribbon follow-up

Owner supplied four luminous multistrand references and requested full amplitude reaching the oval sensor face's height/width. V007 is a liked retained alternative, not the intended representation. Actual visible scene source is the temporary imaging-port2 cap, about40mm across; tiny2.4mm sensor markers were deliberately excluded from sizing.

V008/009 helped expose a curtain/fence appearance when many steep cycles were squeezed into the short24.576mm gap. V010 displays the2.5–5.0microsecond window of the existing assumed pulse as a broad static peak/trough, with documented artistic endpoint taper and amplitude normalization.32fine strands span the cap's full height/width; only light changes. The raw signal is unchanged and transverse height is a display mapping, not acoustic displacement.

Master inspected isolated and actual-context stills. Independent reopened checks pass for fixed evaluated geometry over7frames, height/width matching the face within1%, and centering within0.5mm. A separate20%-wider review camera shows the complete envelope; the original context camera remains intact. The79frame3.292second isolated motion proof passes max1.410s/frame at960x540/Eevee32. This is a focused representation proof; no final cinematic or shared-library acceptance is claimed.

## Formation animation correction — v011

Owner correctly identified that v010 merely moved light over a completed shape. V011 preserves the anchored domain but changes actual mesh height through17local controls: flat start, progressive near-to-far formation, crest, weaker returning response, and an identical flat end. Both isolated and device-context clips contain120frames at24fps, five seconds each. V007/v010 native/video preservation checks pass.

Master inspected flat/growing/full/response/end states and independently reopened both v011 natives. Checks pass for changing evaluated geometry, invariant object transform and route X/Y, anchored endpoint positions within0.1micrometre, progressive rather than uniform growth, full height within1% of the40mm face, smaller response, fixed review camera/optics, relative libraries and unchanged files. Exact checks are in Evidence/formation-context-independent_v011.json and formation-isolated-independent_v011.json.

The context is intentionally a review tableau frozen at source frame305, with its own5second timing and wider review camera. The source camera datablock/action is retained separately; this is not a claim that the proof plays the original shot timing. Full render-to-file maxima: isolated1.48s and context2.38s; initial context benchmark3.254s. The waveform motion is an artistic display, not measured ECCO data or calibrated particle motion. Owner visual choice and final library work remain outstanding.

## Intent-led correction — v012

Owner approved the clarified intent: sensor on right sends toward wall on left; interaction there causes the return into that same sensor; only after reception is a measurement recorded. V012 replaces whole-ribbon growth with finite visible signals on an anchored domain. The quiet gap is empty. A localized wall response, same-face reception cue and delayed wall mark make the event order explicit. Maximum outgoing height remains approximately40mm; the echo is approximately20mm.

Master inspected quiet/departure/outgoing/contact/return/reception/measurement images and independently reopened the saved native. All sampled checks in `Evidence/causal-v012-independent.json` pass: stationary packet objects and axial sample coordinates, changing geometry, correct projected travel directions, wall response after arrival, echo originating at the wall, same-sensor emission/reception, no early receipt, no mark before the echo tail finishes, matching wall reaction/record location, full-size outgoing and smaller return, valid relative links and unchanged native file.

The seven-second clip has168frames at24fps,640x360/Eevee16. All batch frames pass below5s; maximum2.857s. The initial cold-shader benchmark failure remains documented, and interpolation amplitude loss was fixed by baking every rendered frame before the final batch. All ten retained v007/v010/v011 native/video hashes match their prior manifests. This is still an illustrative review tableau with separate cinematic timing; original datasets and source scenes are untouched. Full shared controls, variants, migration and owner visual acceptance remain incomplete.

## Fast evolving field — v013

Owner found v012 too much like a floating object and requested organic ocean-like wave motion, then explicitly authorized a fast revision. V013 uses one anchored field with a multi-frequency outgoing train and weaker delayed reflection. Crests change locally and overlap after wall contact; smooth envelopes replace finite packet cut edges. A constant whole-clip scale maintains the approximately40mm maximum height, without per-frame normalization. This is an authored cinematic field, not measured RF or literal ocean/fluid displacement.

Master inspected successive context frames and the complete every-six-frame sequence, then independently reopened the saved native. `Evidence/rolling-field-v013-independent.json` passes stationary object/axial samples, evolving local geometry, sensor-sized maximum height, quiet start/end, wall and reception cue timing, same sensor, delayed measurement, relative links and unchanged file. These tests support the motion review; they do not establish owner visual acceptance. The strands still have a fine mesh appearance in still frames; the actual four-second clip is the review artifact for the requested movement.

Native: `Shared/Assets/Acoustics/RibbonWaveform_v013/S02_rolling-wave-field_v013.blend`. Video: `Records/Tasks/T-056/Previews/rolling-wave-field-context_v013.mp4` (paths beneath `04-Production` in the main production checkout).96frames at24fps,640x360/Eevee16. Batch maximum2.26seconds/frame; benchmark maximum3.01seconds. Prior versions are preserved. Heavy scene/video remain local, without a new off-machine backup claim. Shared-library completion and full-shot integration remain pending.

## Completion pass and owner review boundary

Radzi approved v013 for now and reported no issues with the other previews, while reserving final approval until inspecting shared Blender files. He then authorized finishing054 first and056 second. During054 completion he explicitly approved its visual result. The [native review list](native-review.md) distinguishes preview approval from final native acceptance.

054 v004 uses the exact two source cap grids instead of heuristic triangle filtering. All70 strata levels yield two continuous chains and all8 grid lines one chain, with no branches or hole-crossing chains. The3mm normal offset and0.1mm source-seam tie-break are display choices; local measurements are unchanged. Root inspected frames1/120/220/288, independently reopened S02/S03/S06 copies (camera/range/fps/libraries/source preservation pass), and read/reran the saved-copy shared propagation test for digital palette and reveal, including exact restoration. The derived shared line library has a manual source-hash preflight and tested regeneration helper; it does not update automatically with World geometry. Coarse source-timed continuity proof max2.856s/frame. Current entrypoint and limits: [054 v004 report](../T-054/report-v004.md).

056 v014 completes the selected waveform as native Geometry Nodes with shared modifier controls, local overrides, and illustrative open/cased presets. Root independently reopened the stable master with autoexec disabled: active vertices match v013 within3.8e-8m; quiet geometry is empty; shared strength changes/restores geometry; cased preset changes geometry; relative libraries and source hashes pass. Separate root checks confirm nonzero routes, actual endpoint distances, active event geometry and empty geometry after all three mapped events. Final S02/S04 cameras, playback and frame ranges match source samples. Root also read/reran the source-preservation checker at a common frame: original object actions/custom data and geometry/shape-key comparisons pass across571/548 S02 objects/data blocks and798/728 S04 objects/data blocks.

Builder's16 control tests include a saved shared strength edit observed in both reopened consumers, byte-exact restoration, and a saved local override affecting only S02. Root viewed the master, outgoing/return frames and16-sample consumer sequence. Source-time clips contain27 S02 frames and25 S04 frames at24fps; batch maxima0.629s/0.851s, representative master2.193s. Source Workbench views remain flatter than the Eevee master and use a local radius multiplier; S04's field is small in its preserved wide view. An initial zero-route adapter bug was fixed before acceptance. A cyan tail at S04 frame95 is the untouched section-owned casing response; the new shared field is empty then. Fourteen retained prior native/video hashes pass preservation.

All five implementation packages are ready for final native inspection. Reports/scripts/evidence and selected stills are synchronized by the master; native files/video remain organized locally and ignored, without a new backup claim. No final movie batches, film assembly or client delivery occurred. Owner visual approval of054 and provisional v013 approval do not replace final inspection of the shared Blender assets. See [native review](native-review.md) and [056 controls](../T-056/shared-controls-guide_v014.md).

## Shared plus demo packaging correction — 31 October 2026

Owner inspection found waveformv014 still contained its demonstration scene. Audit of all11delivered libraries confirmed682objects in that file, including section context and experiments. Earlier controls/default checks did not establish library cleanliness. Owner authorized a shared-plus-demo delivery, excluding consumer copies from the delivered review list.

Waveformv015 is extracted at a local origin with2objects/2meshes/1material/2GN groups and no linked scenery, cameras, lights or datasets. Its separate11object demo links the clean library. Root independently reopened all six demos plus the new shared file: relative links resolve, no shot-scene library dependencies, and sampled default field geometry matchesv014 exactly. The existing focused hardware/World/Surface/digital libraries remain unchanged. No old files are deleted or relinked automatically.

Six demos cover hardware, World, Surface, digital environment, measurement reveal and waveform. World/Surface have two scenes each for detail and overview; other demos use minimal authored fixtures/proxies. Root and fresh delegated checks inspect saved camera/readme/library structure; source hashes remain unchanged. Existing consumer copies are retained as historical evidence, outside the delivery catalog. Authoritative current list: native-review.md.

Packaging proofs are working-setting previews. Hardware firstEevee frame32.895s failed and stopped; its finalWorkbench organization still1.652s passed. Initial digital environment7.424s failed; reduced-cost focused proof follows. Initial waveform demo2s met timing but failed visibility through its wall fixture; corrected demo-only framing is recorded by056. These failures do not count as passes. Final geometry/controls/source verification remains distinct from Radzi's native acceptance.

## Shared filesystem reorganization — 31 October 2026

Owner authorized the proposed Hardware/Environment/Effects structure, then explicitly directed that archive links need no maintenance. Final scope therefore repairs only active shared libraries and the six delivered demos. Historical scenes/backups and archive contents were not relinked; previous broad dependency plans were preparation only, not applied.

All240planned moves completed:25active original files,204archived files,5supplied originals and6demos. Assets now has only Hardware, Environment, Effects and README.md at its root, with eight asset folders below. Original archive files and Sources compare byte-exact to the pre-move hashes. Source duplicates, experiments and editor backups are preserved in the archive rather than deleted. Six demos now live directly under Shared/Demos. Current catalog: Shared/Assets/README.md.

Fourteen active native files required548serialized filepath changes. The bounded SDNA patcher preserves every other decoded byte; exact-original rollback was pretested and retained locally for changed files.16active native libraries and6demos freshly reopen with resolved links; clean waveform remains2objects. Four current runtime helpers received path/root-discovery changes; fresh World/casing/hydraulics checks and Digitalregeneration syntax/help pass. Digital source guard uses a relocation-specific metadata receipt after verifying filepath-only World changes; the historical derivation record remains untouched.

The connected Blender UI had an unsaved scene at an old path. Its scene was not saved or replaced. Only its current working directory moved to the new asset directory to release the empty former folder. No source visual or camera change was made. A migration-time lease expired during verification; a fresh closure attempt was claimed before final synchronization, with no competing worker ownership.

Exact map/checks: Reorganization/move-plan.json, migration-summary.json, active-native-path-proof.json, fresh-native-open-verification.json and current-runtime-verification.json. Large scan inputs and local rollback records are excluded from Git. Text paths/scripts/catalogs are published through the task worktree. Native media remains local with no new off-machine backup claim. Final acceptance remains Radzi's native inspection.
