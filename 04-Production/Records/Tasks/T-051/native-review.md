# ECCO-051 — Shared assets and demos

Current delivery: 31 October 2026. Production root: C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco. Preserve the folder structure for relative links. Final acceptance follows Radzi's native inspection.

| Item | Shared master beneath 04-Production/Shared/Assets/ | Demo beneath 04-Production/Records/Tasks/ |
|---|---|---|
| ECCO hardware | ECCO/ECCO_film_v003.blend | T-052/Demos/Hardware_demo_v001.blend |
| BHA assembly | BHA/BHA_film_v008.blend | T-052/Demos/Hardware_demo_v001.blend |
| Physical World | WellAssembly/World_environment_v010.blend | T-051/Demos/World_demo_v001.blend |
| Surface/subsea | Surface/Surface_descent_v005.blend | T-051/Demos/Surface_demo_v001.blend |
| Digital environment | DigitalEnvironment/Digital_context_lines_v004.blend | T-054/Demos/Digital_environment_demo_v005.blend |
| Measurement reveal | MeasurementReveal/Measurement_reveal_v001.blend | T-054/Demos/Measurement_reveal_demo_v002.blend |
| Waveform | Acoustics/Waveform_shared_v015/Waveform_shared_v015.blend | T-056/Demos/Waveform_demo_v015.blend |

Required supporting libraries: ECCO/Satin_finish_v001.blend, BHA/BHA_core_satin_v001.blend, DigitalEnvironment/Digital_style_v001.blend and DigitalEnvironment/Digital_world_v001.blend. The digital environment is a small family of style, physical wrapper and derived contextual-line libraries.

Shared masters hold reusable components; demos link them and add examples, framing and instructions. Earlier consumer copies remain historical test evidence, outside this delivered list. Existing files and locked shots are preserved.

Waveform V015 contains only the live field and master control: two objects, two meshes, one material, two Geometry Nodes groups, no external libraries, cameras, lights, geology or recorded history. Its local origin is near zero. Default geometry matches V014 exactly at ten checked frames. Select WF_MASTER_CONTROLS for shared values and WF_LIVE_FIELD for local settings; use the Blender README. The separate11object demo provides a minimal sensor/wall fixture and causal cues. V014 and V013 are retained.

World and Surface demos provide two scenes each through the scene selector: detail/outer extent and assembly/subsea. World uses neutral geometry shading. Hardware demo uses Workbench for fast organization inspection; linked satin materials and lights remain stored.

Digital lines require the documented manual source-hash preflight and regeneration after World changes; see Shared/Assets/DigitalEnvironment/CONTEXT_LINES_v004.md. Measurement demo shapes and acoustic presets are authored illustrations, not calibrated data. Visual approval of054 and provisional V013 approval remain recorded; native acceptance stays with Radzi.

Verification and hashes: Evidence/shared-demo-independent.json, Evidence/environment-demo-build.json and package demo manifests. Heavy Blender files remain local/ignored without a new off-machine backup claim.
