# T-006 / B102 — provisional well and assembly variants v003

16 October 2026. Task `0d01c109-a994-461b-b4c1-2fd3661f6fac`; run `7acbe4f9-c0f8-4a46-ac43-98a4d1693005`; worker `codex-t006-build-v003-01a13f79`; reviewer Radzi.

## Result for review

Completed Radzi's authorized **provisional illustration**: separate cased/open intervals, nominal/irregular/spiral lower-hole variants, casing/cement cutaways, live controls, simplified labeled BHA/adapters/bit and five moving previews. **O05 remains open for MIT confirmation before technical lock.** No actual deployment, thread/shoulder/shoe/dogleg/load or operating-safety acceptance claimed. No downstream ticket or S01-S07 shot started.

Authority: direct instruction to proceed with researched dimensions as a provisional illustration, adapt the builder for separate intervals, complete variants/controls/previews and simplify unknown BHA placement/adapters. This releases the earlier hold for that bounded scope. Fresh handoff/pinned roadmap v2 checked; live T2/T3/T4 Done and T5 accepted. [Earlier report](report_before-v003.md) and research preserved.

## Outputs

- [Combined 22-second preview](Previews/v003/B102_all-variants_v003.mp4), [review sheet](Previews/v003/B102_variants_review-sheet_v003.jpg), [evaluated wall-profile comparison](Previews/v003/B102_profile-comparison_v003.png).
- [Reusable master](../../../Shared/Assets/WellAssembly/WellAssembly_variants_v003.blend), collection **WELL_ASSEMBLY_v003**; [controls/replacement guide](../../../Shared/Assets/WellAssembly/README_v003.md), [authorized config](../../../Shared/Assets/WellAssembly/config_authorized_v003.json), [builder](../../../Shared/Assets/WellAssembly/Scripts/build_variants_v003.py).
- [Master checks](Evidence/variants-verification_v003.json), [five consumer checks](Evidence/preview-consumer-checks_v003.json), [editable appended-consumer checks](Evidence/editable-consumer-checks_v003.json), [render timings/hashes](Evidence/preview-renders_v003.json), [video QA](Evidence/video-qa_v003.json), [output integrity](Evidence/output-manifest_v003.json).

| Case | Moving preview | Editable saved preview | Frames / duration | Render |
|---|---|---|---|---:|
| Nominal | [MP4](Previews/v003/B102_nominal_v003.mp4) | [Blend](Previews/v003/nominal/B102_nominal_preview_v003.blend) | 96 / 4s | 24.213s |
| Irregular | [MP4](Previews/v003/B102_irregular_v003.mp4) | [Blend](Previews/v003/irregular/B102_irregular_preview_v003.blend) | 96 / 4s | 22.002s |
| Spiral | [MP4](Previews/v003/B102_spiral_v003.mp4) | [Blend](Previews/v003/spiral/B102_spiral_preview_v003.blend) | 96 / 4s | 21.816s |
| Cased | [MP4](Previews/v003/B102_cased_v003.mp4) | [Blend](Previews/v003/cased/B102_cased_preview_v003.blend) | 96 / 4s | 22.124s |
| Interval transition | [MP4](Previews/v003/B102_interval-transition_v003.mp4) | [Blend](Previews/v003/interval-transition/B102_interval-transition_preview_v003.blend) | 144 / 6s | 33.418s |

Workbench 1280x720 / 24fps. Silent H.264/yuv420p. Final render total **123.573 seconds**, 528 frames / 22s; excludes initial pass superseded by saved-link repair, encoding and checks. Initial timing evidence retained; no finishing-budget promise.

## Provenance and boundaries

Accepted T5 temporary plugged v002 remains linked by relative path/hash `704a91cb478a1a38304835786fa62d549df5bf5833e457cbc4da094fd6557fd7`; housing, nine closures, source references and original masters unchanged. Official MCP read-only query found default Cube/Camera/Light scene; left unchanged. Isolated background Blender 5.2.2 produced the asset/consumers.

Upper: 17.5in host, 13.375in casing OD, 12.515in nominal ID, ideal cement annulus. Lower: 12.25in nominal hole/bit gauge. Casing is not placed in the smaller lower hole. Published 12.359in drift stays a separate reference. [Research](research-standard-scenario_v002.md) and config retain source URLs and inch values.

X=0 is an illustrative interval join, not certified shoe geometry. Extents [-5.5,0] and [0,6]m, 25.4mm outward profile scales, 1.8m spiral pitch and proxy lengths/placement are explicit **authoring parameters**, not field/assembly measurements. Profiles enlarge outward, preserving the nominal passage instead of inventing a tight-hole collision. No acoustic, hydraulic or calibrated log result implied.

Separate generic collars use sourced 8.25in OD / 2-13/16in ID. Orange adapters and simple bit-gauge ring label unresolved geometry. No detailed cutter/motor/thread or actual MIT BHA claimed; F.H. and REG are not assumed to mate. Test travel/rotation is not actual drilling speed/direction. O04/O14 hardware limits remain open.

## Controls and verification

ASSEMBLY_CONTROL exposes travel_m, rotation_rad, variant0/1/2, full/cutaway, independent open/casing/cement/hardware/proxy visibility and irregular/spiral strengths. Drivers need no Python handler. Dimensions/pitch/extents rebuild from config. Open master or append its collection for editable local controls while retaining external ECCO. Complete linked well controls require appropriate library overrides; raw links are read-only. Editable appended consumer was saved/reopened and tested.

Executor self-checks pass: source/hash/relative link, O05-open metadata, six variant/cutaway combinations, visibility groups, profile strengths0/1 and outward bounds, manifold casing/cement/proxy shells, ten linked housing/closure instances, exact control matrices and positive centered product clearance across interval samples. Nominal bit-gauge wall contact is intentional, not a cutting simulation. Shoe/thread, tolerance, eccentric/deviated/loaded fit remains unvalidated.

Five preview sources reopen with source/hash, selected variant, frame range and animation endpoints matching rendered candidates. All videos fully decode at exact frame count/rate/size/duration without errors; combined cut 528 frames /22s. All raw frames inspected through chronological mosaics, with encoded keyframe sheet and full-size nominal/irregular/cased/spiral frames. Motion/closures remain coherent, walls stationary, interval boundary passes coherently and proxies stay identified. Camera intentionally frames the tool and nearby assembly; upper collar continues beyond frame. Evaluated profile slices make subtle actual-scale differences readable. This is frame-sequence inspection, not claimed real-time playback or human approval.

Initial harness required explicit dependency tagging and visible evaluated shape-key objects; corrected without asset changes. Reopening caught preview Save As double-remapping relative library paths. Saver fixed with explicit paths/relative_remap=False; all consumers rerendered from reopened corrected files and checked. Useful failure/timing evidence retained; only this run's superseded automatic .blend1 backups removed. No supplied geometry repaired/overwritten.

## Review and closure

Radzi reviews exact v003 master/previews for provisional foundation usability; only Radzi accepts Done. O05 stays open before technical lock for MIT actual deployment, BHA/adapter/shoulder/shoe/trajectory/loaded clearance. O04/O14 replacement checks remain required. Review acceptance is not MIT engineering confirmation.

Base main `2b889dcff0c58e9732d73004ec4b0c23b130bd95`; starting tree clean. Candidate **uncommitted**. All outputs under04-Production; asset/blocker/O05 records updated. Blender/MP4/raw Frames ignored/local; text/config/scripts/evidence/review stills separate candidates. No commit/push/backup/publication/client contact implied. Output references attached to Work are machine-local, not remote downloads.

Reproduce using `C:/Program Files/Blender Foundation/Blender 5.2/blender.exe --background --factory-startup --python <build_variants_v003.py>` with newly versioned output; builder refuses overwriting candidate. Verify master with `--background <master> --python <verify_variants_v003.py>`. Task Scripts contains render_variants_v003.py (save/reopen/render), inspect_preview_consumers_v003.py, test_append_consumer_v003.py, package_variants_v003.py and profile_review_v003.py. Packaging uses bundled Python `C:/Users/RZ1/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe -X utf8` with Pillow/imageio-ffmpeg. Source URLs/provisional authority stay in config; no live-scene changes required.

Rolladice closure verified: run finished, T6 in Review with all five provisional-scope criteria checked and twelve current output references attached. Task blocker cleared for the authorized illustration; O05 remains open in canonical decisions and implementation metadata. Only Radzi may accept Done.
