# ECCO-051 — Native shared-asset review

Owner review happens in the shared Blender files. On 30 October 2026 Radzi reported no issues with the other previews and approved waveform v013 for now, while explicitly reserving final approval until inspecting the native assets. None of these statements marks the complete package Done.

Open the files in the production checkout: `C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco`. Heavy Blender files are local, not included in the Git publication. Keep the relative folder structure so linked libraries resolve. Review copies preserve the original shot files.

| Package | Shared Blender entry point beneath production root | What to inspect |
|---|---|---|
| 052 hardware | `04-Production/Shared/Assets/ECCO/ECCO_film_v003.blend` | ECCO geometry, sensor faces and linked satin finish |
| 052 BHA | `04-Production/Shared/Assets/BHA/BHA_film_v008.blend` | Connected assembly and continuation controls |
| 053 physical World | `04-Production/Shared/Assets/WellAssembly/World_environment_v010.blend` | Irregular borehole, cutaway, soil extent and separate variants |
| 055 surface/descent | `04-Production/Shared/Assets/Surface/Surface_descent_v005.blend` | Surface rig, subsea assembly, earth and illustrative viewing opening |
| 054 digital context | `04-Production/Shared/Assets/DigitalEnvironment/Digital_context_lines_v004.blend` | Shared relief-following contextual strata/grid; visually approved, native review pending |
| 054 digital style | `04-Production/Shared/Assets/DigitalEnvironment/Digital_style_v001.blend` | Shared cyan palette and styling |
| 054 measurement reveal | `04-Production/Shared/Assets/MeasurementReveal/Measurement_reveal_v001.blend` | Shared receipt-driven reveal controls; local measurements remain in each shot |

054 is visually approved. Its derived contextual lines require the documented source-hash preflight and regeneration after World shape changes; see `Shared/Assets/DigitalEnvironment/CONTEXT_LINES_v004.md`. 056 waveform is undergoing the authorized completion pass. Its final native entry point and controls will be added after saved-file checks. V013 is retained as the selected waveform motion reference; full shared controls/variants are a separate completion step.

For scene context, use the package reports' consumer copies: [052](../T-052/report.md), [053](../T-053/report.md), [054](../T-054/report.md), [055](../T-055/report.md), [056](../T-056/report.md). Exact versions, native hashes, local limitations and propagation checks are recorded there. Final film assembly stays with Radzi.
