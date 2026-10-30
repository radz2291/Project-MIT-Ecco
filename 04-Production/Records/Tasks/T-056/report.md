# ECCO-056 — Pressure-field proof awaiting owner feedback

30 October 2026. **Incomplete shared-asset ticket: model-driven visual proof v007 is ready; final presentation and reusable open-hole/cased package are not accepted or complete.**

Current review: [pressure-proof report](pressure-proof-report_v007.md), [outbound](Previews/pressure_outbound_v007.png), [contact](Previews/pressure_contact_v007.png), [return](Previews/pressure_return_v007.png). Local motion: `Previews/pressure-field_v007_slow-review.mp4`, 4.375 seconds, 105 quarter-frame samples at 24fps. This plays the original native camera four times slower; model microseconds are mapped separately.

The pulse is generated from an explicit assumed 1-D model using the inspected 24.5758528mm gap. Signed pressure drives color/opacity at fixed spatial slices. Twelve model/input tests pass. All 105 full render-to-file calls are below 5 seconds: max 2.353 seconds, mean 1.170 seconds at 640×360 Eevee16. Source, relative links and camera were checked by the master against the reopened candidate. No measured ECCO signal or full-wave validation is claimed.

Research: [local input audit](local-waveform-research.md), [numeric inventory](local-signal-data-audit.json), [primary-source synthesis](waveform-research.md). No identified recorded RF time series was found in the bounded local candidates. B202 scalar events and S03/S06 display arrays are not RF data. Small authored source/receiver CSVs and explicit metadata are in `Shared/Assets/Acoustics/PressureField_v005`; native candidate is `Shared/Assets/Acoustics/PressureField_v007/S02_pressure-field-proof_v007.blend`. Both paths are relative to `04-Production`.

Decision history is retained locally: v001 graph panel superseded by owner 3D direction; v002 blank Eevee failed; v003 moving packet rejected as worm-like; v004 fixed path still judged wire-like; v005 Workbench pressure bands failed as dark stacks; v006 emissive bands improved but fixture too bright; v007 lowers fixture lighting and is the current proof. Earlier native/video/images are preserved. The old wire-controls scaffold is unvalidated and excluded from this publication candidate.

Task UUID `80c559e4-7e88-4acd-bfbf-46448545076a`; parent ECCO-051; worker `ECCO-056-builder-20261030`; run `24259eb9-f2c3-4e00-ac1a-6ab31bda81e6`; base `bb9a503c8d69ae0cf5ba20273a5280d130cc1949`. Current authority includes the owner's research/data-driven improvement request. Master alone publishes permitted files and records the verified remote commit. Native/video/raw frames remain local; no off-machine backup or media upload is claimed.

Next: receive owner feedback on the pressure representation, then finish the scoped controllable library, open-hole/cased variants and required consumer migration checks. Work remains waiting; no finished Review/Done or final visual acceptance claim.
