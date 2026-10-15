# T10 — B204 hydraulic mechanism proof v001

16 October 2026 · Rolladice task `5eb35608-da75-411f-93c9-d23e2390e976` · Project MIT ECCO · Run `6842a045-d5a2-4172-ad27-e3ceb61a75ac` · Worker `codex-t010-hydraulics` · Reviewer Radzi.

Radzi authorized “Pls work on T10.” Fresh live handoff and standard roadmap revision 2 were read; T5 and T6 were Done. Base checkout: `main`, `origin/main`, `86437b95433bb1e9feb7edd084d2fa86e0e8532f`, `radz2291/Project-MIT-Ecco`. Initial tracked/staged tree was clean. Other chats subsequently created T7/T9 work; those paths are outside this task and are preserved. Radzi authorized Git coordination in T7; T7 is the designated integrator. T10 staged only its 18 review paths before the coordination message arrived, then stopped Git mutations. T7 integrates the agreed T10-owned paths separately. No client communication or acceptance on Radzi's behalf.

## Result and exact candidate

A controllable circulation-only explanatory preview with linked accepted CAD and a separate schematic of the three sequential hydraulic functions. Product is stationary. Sources do not establish an exact hydraulic stage-to-CAD face map, so the scene does not invent one. The supported functional explanation is prepared for Review; exact end orientation/stage identities and MIT analysis remain targeted technical questions before affected B3/B4 content can lock.

| Output | Version / storage |
|---|---|
| [Editable proof](../../../Mechanisms/B204/Scenes/B204_hydraulic-proof_v001.blend) | v001; local Git-ignored Blender file |
| [Moving preview](../../../Mechanisms/B204/Previews/B204_hydraulic-proof_v001.mp4) | v001; local-only H.264, silent, 12.000s, 288 frames, 24fps, 1280×720, yuv420p |
| [Review still, frame 49](../../../Mechanisms/B204/Previews/B204_inspect_f049_v001.png) | Selected generated review still synchronized with this report |
| [Use/replacement guide](../../../Mechanisms/B204/README_v001.md) | v001; relative links and controls |
| [B206 review packet](review-questions_v001.md) | Exact source-map/mode questions and analysis transfer checklist; feedback pending |
| [Output manifest](Evidence/output-manifest_v001.json) | File sizes/SHA-256 for exact candidate and inspection frames |
| [Hydraulic source/blocker register](hydraulic-register_v001.md) | Scoped asset/provenance/uncertainty addendum; refers to global O07/C08 |

All retained outputs are under `04-Production`. Machine-local root: `C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco`. Local links are not remote downloads. Scene, video, raw frames, four motion contact sheets, six additional inspection stills, brochure inspection PNG and failed trial remain local; synchronization of scripts/report/evidence/selected still does not back up those files. Candidate commit and commit-pinned report link are recorded in Rolladice after remote verification, avoiding a self-referential report hash.

## Inputs and source verification

- T5 `Shared/Assets/ECCO/ECCO_master_temporary-plugs_v002.blend`, collection `ECCO_MASTER_v002`, hash `704a91cb478a1a38304835786fa62d549df5bf5833e457cbc4da094fd6557fd7`. Linked, not copied/edited/rescaled. The original monolithic source mesh and removable closures remain intact.
- T6 `Shared/Assets/WellAssembly/WellAssembly_variants_v003.blend` and `config_authorized_v003.json`. Uses its nominal open-hole dimension (12.25in / radius 0.155575m); no BHA proxy detail or alternate interval assertion is added. T6 is used as the dimensional/configuration baseline, not appended with its entire 11.5m inspection layout.
- Original `01-Brief/ECCO_ENP3_Datasheet-1.pdf` p2 was extracted and visually read. It defines three accelerator pads, two twisted-pad sets and a diffuser, sequentially. It supports circulation-only with no string rotation, rotation-only, tripping-only and additive combinations. Its performance language is attributed manufacturer intent; no independent validation or numerical performance claim is added.
- Engineering Baseline, Decision Register, Production Workflow, preview settings and engineering-information module 09 were read. S05 V2 captions and C08 feedback were checked. This is B2 mechanism work; no actual S01–S07 shot or cinematic contract is claimed.
- Bounded filename search of `01-Brief`, `02-Reference`, `04-Production/Shared` for FEA/CFD/hydraulic names and common analysis extensions returned no source analysis candidate. This agrees with prior A02 evidence, but does not establish that MIT has no analysis.

| Check | Evidence and disposition |
|---|---|
| CAD geometry | Fresh background inspection: preserved housing, 348,876 vertices, source X length ~2.400m, maximum axis radius ~0.152400m. [Profile evidence](Evidence/geometry-profile_v001.json). Raised/twisted features are visible; geometry alone does not identify exact functional stage boundaries. No four-pad / 30-degree ENP1 description transferred to ENP3. |
| Flow direction | Annular return toward surface is sourced in the S05 captions. Source +X mapping is provisional inference from the sensor/lower-shoulder context and end appearance; exact pin/box datum remains unconfirmed. Explicit in preview and B206 packet. |
| Stage order | Three sequential functions verified against brochure p2. Separate schematic avoids unsupported face labels. Actual CAD stage map unresolved under O07. |
| Operating modes | Brochure-supported modes distinguished; only circulation-only built. No requirement that rotation/circulation occur together. No simulated fields for other modes. |
| Analysis | No CFD/FEA result used. C08 analysis panel remains pending. Exact file/run/model, variables, units, ranges, boundary conditions, interpretation and permission requested in review packet. |

## Verification and visual QA

Official Blender MCP read-only query confirmed Blender 5.2.2 LTS, a clean untitled default scene with 3 objects. Background work preserved that scene. The MCP background helper could not resolve executable `blender`; used the installed executable obtained through MCP (`C:/Program Files/Blender Foundation/Blender 5.2/blender.exe`) for isolated background builds instead.

Fresh-open verification checks relative library resolution, all 288 frames for valid drivers, constant product transform, `flow_rate=0` stops markers, and flow visibility toggle. [Evidence](Evidence/fresh-open-verification_v001.json). Marker centre radius 0.1545m is outside source mesh maximum radius and inside nominal wall radius (1.075mm centre-to-wall separation); symbol sizes are explicitly exaggerated and can cross the physical boundary. This is not a particle-clearance, hydraulic-gap or loaded-fit validation.

Full animation rendered with Workbench, 8-sample anti-aliasing, in **107.307 seconds**. Encode plus full decode/check took **13.792 seconds**. [Render settings/time](Evidence/animation-render_v001.json) · [Video checks](Evidence/encode-qa_v001.json). All 288 encoded frames decode; dimensions, frame rate and duration pass.

Visual review: full-size frames 1, 49 and 288 inspected for readable labels, complete source silhouette, visible diagram and clear illustration/provenance distinction. All 288 schematic frames reviewed in four ordered contact sheets locally (`Evidence/motion-contact_01_v001.jpg` through `04`); continuous left-to-right marker progression and intentional outlet-to-inlet respawn are visible. This is sequential-frame inspection, not a claim of real-time playback or independent human review. Source hardware remains static by design. Paths do not prove turbulence, pressure recovery, efficiency or particle transport; geometry convergence/waviness communicates qualitative intent, with uniform authored time and no calibrated legend. No physical acceleration/pressure field is calculated. The source-mesh-linked upper panel does not pretend its straight guide lines are resolved local streamlines.

Useful failed trial retained under `Evidence/Failed/B204_driver-truncation_attempt.blend` (ignored). Factory-empty scene initially had no World; builder now creates one. Overlong driver expressions were truncated by Blender; corrected using a separate normalized path property and all-frame fresh-open checks. Initial erroneous scratch path was corrected before a scene was saved. Final v001 inspection stills and video come from the corrected saved candidate.

## Reproduction

Run the versioned scripts in order with the installed Blender executable (`--background --python <script>`): `inspect_geometry_v001.py`, `build_proof_v001.py`, `render_verify_v001.py`; then bundled Python `encode_qa_v001.py`. Builder deliberately refuses existing scene overwrite. Version the candidate before editing/rebuilding, preserve earlier evidence, and re-run affected checks. Python encoding dependencies: Pillow and imageio-ffmpeg. No simulation cache or animation Python handler required.

## Review and next action

Radzi reviews this exact circulation-only candidate and consolidates the four consequential B206 questions. No T10-specific MIT answer was received; none was fabricated. Exact stage face map and end-direction confirmation remain open; approved analysis media/interpretation/rights remain C08. These are not new blanket O05/O14 holds. On returned authorized feedback, create v002 and propagate changes to affected S05 blocking/analysis integration before B4. No downstream ticket executed, no self-acceptance, no MIT engineering certification.
