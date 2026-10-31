# ECCO-054 — SHARED + DEMO review

Open these two small demos directly in Blender. Each opens in a useful demo camera view with a selected `DEMO CONTROLS` object. Its Object Properties → Custom Properties expose the controls. The Text Editor also contains `README — SHARED ASSET DEMO`.

- `Digital_environment_demo_v005.blend`: static view of actual linked World cutaway, approved dark-ground material and approved cyan contextual cap lines. Toggle soil or contextual lines; adjust the local axial display window. Two empty local carriers evaluate linked assets; they contain no copied section geometry.
- `Measurement_reveal_demo_v002.blend`: two authored proxy tubes (irregular and clean), sharing the actual stored-reveal and fine-style node groups. Scrub frames 1 (empty), 20 (early), 34 (partial, saved opening frame), 60 (settled). Change Start/Stagger/Settle/Arrival offset and point/line radii. Receipt is frame 8 and stored display begins later. Each local proxy has 696 vertices/672 faces; it is explicitly synthetic, not a section dataset.

These are demonstrations, not shot scenes. No original section camera, measurement dataset, unfold/laptop scene or old consumer was repackaged. Each scene has five objects: two carriers/proxies, one control empty, one demo camera and one demo light. Libraries are linked with relative paths; actual shared asset edits propagate. The established shared libraries have not been modified.

Shared editable sources remain under `04-Production/Shared/Assets/DigitalEnvironment/` and `MeasurementReveal/`. World remains `WellAssembly/World_environment_v010.blend`. Context-line geometry is a pinned derived representation: run `check_context_derivation_v004.py` before use and follow `CONTEXT_LINES_v004.md` for regeneration after World edits. Demo crop changes are display-only and do not replace World geometry.

Review list is SHARED + DEMO only. Earlier consumer scenes remain historical verification evidence and are not delivered as review entries. Native files are local and ignored by Git; tracked scripts, manifests and selected proofs provide reproducibility, not an off-machine native backup. Visual approval of the prior shared appearance is preserved; this packaging does not imply final owner acceptance.
