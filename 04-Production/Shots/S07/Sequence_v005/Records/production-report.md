# S07 v005 — three moving shots from v002

Status: owner review pending. Direct owner revision, no invented Work ticket.

## Result

Rebuilt from v002, rather than the subsequent rear-traverse experiment. The eight-second sequence now has three shots: first detail 0–2.5 s, reverse beauty 2.5–5 s, full centered hero 5–8 s. Each shot opens on camera movement already underway and uses constant straight-line camera translation. There is no eased start or end within any shot. The camera also keeps moving under the final fade. The actual hardware remains stationary.

Shot 2 stays close through its final frame. Shot 3 starts on the whole product, with a distinct scale change at frame 121. No matching end/start duplication. Opening laptop dissolve removed: S07 starts directly on the product, fully visible. The S06 boundary preview uses a direct editorial cut. Both closing text objects removed; fade to black at frames 164–190 retained. Owner adds a separate logo frame in post.

## Preservation and checks

Exact source mesh vertices/topology and every hardware transform verified across all 192 frames. v002 native, canonical source and approved S06 artifacts retain their hashes. Geometry, dimensions, source scale, materials and lighting are unchanged. Source-length/provisional-cap limits remain as recorded in v001. Previous versions retained.

Saved source reopens with packed dependencies and no external libraries. Each shot's first camera interval has nonzero displacement, and every subsequent displacement vector in that shot is equal within tolerance. Cut interpolation holds the outgoing pose until the next frame. Frame 120 remains a cropped pad close-up; frame 121 shows the whole product with all projected bounds inside the image. Cut-adjacent rendered images were inspected directly. The unbounded close-up bounding-box ratio in diagnostics is not a calibrated apparent-scale measurement. Sampled whole-product views stay centered and inside frame. No opening fade or branding remains. Final native output is black within one level of dither; encoding pins the last three frames to black.

Complete edit, boundary edit and all three individual clips decoded without errors. Executor inspected timed frames and both cut boundaries; owner playback review remains pending. No cold-viewer, engineering or client acceptance is claimed.

## Rendering and files

192 frames, 24 fps, 1280×720, Eevee 32 samples. All frames newly rendered after representative benchmarks. Total rendering 191.5 seconds, average 1.00 seconds/frame, maximum 2.86 seconds/frame. Every complete frame below five seconds. Complete-edit encoding took 4.8 seconds. No expensive finishing.

Delivery links are in ../README.md. Three individual clips are under Previews/Individual-Shots. Editable source contains the three shot ranges as named timeline markers and hard camera cuts at frames 61/121.

Hash-verified same-machine recovery: D:/MIT-ECCO-Render-Recovery/S07-Monumental-Precision_v005. This is not an off-machine backup. Native/media remain local. Scripts/contracts/verification records are published to the established Git repository; exact remote parity is recorded in sync-verification.json. Final logo insertion, audio and whole-film assembly remain with the owner. Stop at review.
