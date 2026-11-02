# Six-second beam exchanges with readable pulse motion

Radzi clarified that the former2second exchange preview should become6seconds per outgoing/feedback exchange, extending the actual S01–S02 shot. Current scene `Scenes/S01-S02_production_v015.blend`, linked sharedv020. Six cycles start300/444/588/732/876/1020 at24FPS; each occupies144frames. Entire source is1248frames/52seconds including unchanged opening and delayed final pullback. Earlier versions are preserved.

First cycle (add144 per target):

| Frame | Event |
| --- | --- |
| 300–305 | Straight cyan beam grows from transmitter over5frames |
| 305–308 | Established connection rests briefly |
| 308 | Outgoing message starts |
| 341 | Main pulse reaches Earth; tile geometry and material reveal begin together |
| 353 | Tile finishes12frame settle |
| 368 | Violet feedback begins after the tile has settled |
| about401 | Feedback spike reaches actual transmitter cap |
| 418 | Complete response finishes, line rests flat |
| 418–423 | Beam retracts over5frames |
| 432–444 | Hardware/camera turn smoothly to next target |

Pulse travel is30frames each direction (previous6). Pulse width stays1; extra time comes from travel and sequence spacing, not widening the spike. Sharedv020 adds **Amplitude breath** and **Breath period frames**: shot uses0.32/48frames so height gently rises/falls as the pulse moves. Existing route envelope/attenuation and weaker violet echo remain. Beam stays attached throughout; no packet heads/tails/dots or impact circles. These are readable illustrative timings, not real-scale sound propagation.

Tile16face geometry cues and every current-cell material's diffuse-color animation were retimed together. The color progression was sampled from its original brown→acquired style and rebuilt at impact−1/+4/+12. This corrects the earlier geometry/color mismatch. Settle completes15frames before feedback starts.

BHA holds132frames per cycle, turns12frames after beam closure. Camera follows the transmitter so its cap stays readable. A shot-local **camera viewing wedge** removes camera-facing measurement-wall faces within30degrees of the radial viewing direction, only from300 onward. Its Enabled/Viewing half angle controls are on the wall's final modifier. This clears the near-side display obstruction while retaining the actual target and physical hardware. Both a simple orbit without clearance and a fixed-direction pan were tested and rejected for late-target occlusion. Original pre300 keys remain; the existing pullback path segment is applied relative to final pose1152–1248. Film assembly still belongs to Radzi.

Native manifest `waveform_v015_install.json`; checks `waveform_v015_verification.json`; budget log `waveform_v015_render.json`. Proof `Previews/Waveform-v015/six_second_exchange_v015.mp4` is exactly144frames/6seconds. It is the first actual-scene exchange, not a full52second render. Separate pixel-grid helper remains required for the viewport overlay; waveform itself is native GN.

Checks cover5frame opening fractions, straight setup, continuous endpoints and correct send/feedback phases, actual amplitude change against disabled control, all six held cap routes, closure before rotation, defaultv020 compatibility and reopened relative links. One phase-boundary tolerance issue at raw68frames was caught and fixed before render. Native/media local-only; no off-machine backup claimed. Visual review and whole-ticket acceptance remain open.

Final proof complete:147 full1080p exports max1.306s, plus3final presentation stills max1.370s.144frame movie decodes exactly6seconds at24FPS with zero dropped/duplicated frames. First pulse/impact/return, late-target1121 and finishing1248 were visually inspected. All16faces of every target remain after the viewing cutaway;24cap-ray checks max error0.0611mm. Actual amplitude on/off ratio1.295641 matches the expected modulation. Live scene open323. Source/native hashes are recorded in interface/install manifests; scripts/reports/selected stills synchronized separately from excluded media.
