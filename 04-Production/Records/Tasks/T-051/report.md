# ECCO-051 — Shared asset integration

30 October 2026. **In progress; no owner acceptance claimed.** Controlling input is ECCO-050 at commit `58013a6f5a907bfdfe9a7c7d63405e3306c2c42c`. The five delegated packages preserve locked source scenes and publish successor masters plus separate consumer copies.

## Package status

| Package | Verified result | Remaining |
|---|---|---|
| [052 hardware / finish](../T-052/report.md) | Satin master, ECCO v003, BHA core satin v001 and BHA v008; actual S07/S05/S02 saved consumers; geometry preserved; shared edit propagation; motion and still checks | Owner appearance review |
| [053 physical World](../T-053/report.md) | World v010 with exact irregular S02 wall, documented transforms and extents; S02/T44 consumers; shared edit propagation | Owner appearance review |
| [054 digital / reveal](../T-054/report.md) | Saved S02 reveal and S06 context; shared physical World and local datasets kept distinct; camera/library checks pass | S03 contextual lines remain fragmented; correction active, package incomplete |
| [055 surface / descent](../T-055/report.md) | Surface v005; actual S01/S02 consumers; seabed join, axial view opening and motion checked; shared edit propagation | Owner appearance review; opening is illustrative, not internal engineering geometry |
| [056 acoustic waveform](../T-056/pressure-proof-report_v007.md) | Local signal inventory and primary-source research; actual source/wall anchors; v007 modeled pressure-field clip; independent model and saved-camera checks pass | Previous graph/packet/wire treatments superseded. New proof awaits owner visual choice; full controls/variants and two-consumer migration remain incomplete |

## Independent review

Master reopened source and consumer natives in isolated Blender processes and compared sampled evaluated cameras/lenses, frame ranges, fps and library resolution. Checks pass for 052,053,054,055. Native source hashes remained unchanged. Visual review includes actual S07/S05 hardware, S02 string, BHA controls, S02/T44 physical context, S01/S02 subsea passage, deep transition, S03/S06 context and successive waveform proofs. Defects and failed render attempts are retained rather than counted as successes.

Benchmarks and batches use working preview settings, not full-resolution delivery settings. Selected hardware32-sample640x360 proofs peaked2.619s; 052 motion1.331s; 053 coverage1.829s; final055 subsea motion1.893s; 054 reveal motion2.185s. Initial054 S06 13.741s and blank-image attempts were failures. Every retained passing proof uses full render-to-file timing below5s/frame. A single queue serializes rendering.

## Scope and storage

Original seven-section scenes and unrelated working changes are preserved. Local native masters/consumer paths and SHA256 values are in each package's manifest. Heavy Blender files, movies and frame caches remain local and ignored; no off-machine backup or remote native access is claimed. Selected stills, scripts and reports are published on `codex/ecco051-shared-assets` through one integrator. Exact verified commit links are attached after push.

First publication: `a86990614ce100354a7da6c1bd6d26bcaf2ad110` on `codex/ecco051-shared-assets`; local HEAD and remote branch matched after push. ECCO-052,053,055 are now in Work Review with commit-pinned reports. Original main checkout remains unchanged by Git integration. ECCO-054,056 and master are incomplete.

Waveform v007 uses explicitly assumed one-dimensional pressure samples, not measured ECCO RF. Master independently tested actual sample changes for propagation speed, distance, reflection sign/strength and superposition. Reopened native camera/range/fps/source hashes and relative libraries pass. The105frame4.375second slow-review clip passed max2.353s/frame, after three representative benchmarks max2.628s. Reviewed outbound/contact/return stills show luminous pressure-sign bands and a weaker return. Fine grain and simplified fixture lighting remain; this is representation proof, not final cinematic finishing.

This is shared-asset preparation and focused consumer proof work. It does not assemble or deliver the film, certify the engineering, supply measured ECCO waveform data, or imply Radzi/client approval. Master remains active while054/056 are unresolved.
