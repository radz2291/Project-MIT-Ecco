# Shared digital environment v001

`Digital_style_v001.blend` contains exact selected S03 v036 dark ground, cyan contour, luminous strata and survey-grid materials, plus a linked cyan palette. Consumer opacity, camera, lighting and data attributes stay local. S06 contour emission uses the shared palette while retaining local visibility and strength.

`Digital_world_v001.blend` reads the physical `World_environment_v010.blend` mesh through a live Geometry Nodes Object Info reference. The digital wrapper applies a separate look to the physical source. World uses canonical X axis; S03/S06 section geometry uses local Z. Never interpret a section's measured/reconstructed wall as the World physical dataset.

The linkable `ECCO World outer extent adapter v001` is retained as a **width-only comparison**, not full shape synchronization. It preserves local coordinates inside Keep inner radius (default0.3m), and maps the original outer X boundary to the current physical World's Y extent. Local wrapper settings record original outer X (S03 10m, S06 0.7517164m).

Selected v002 consumer copies instead reference `WORLD_FORMATION_IRREGULAR_CUTAWAY` directly. Inspected native caps face canonical Y, so the exact rotation is X→local Z, Y→local Y, Z→negative local X, determinant+1, with no scaling. Axial viewing windows remain local (S03−10..10, S06−1.2..1.2). The original capped cutaway is preserved; deleting half a full shell would remove visible cross-section soil and is not the selected implementation. The old physical objects have empty output modifiers so their animations cannot restore duplicate geometry. S06's shared soil shader sits inside its original local visibility chain and follows original stage hiding into the laptop scene.

Use one physical context at a placement. The section integration copies retain their local inner shape; do not also instance a competing solid wall there. Local data, amplitude and geometry colors, unfold/laptop behavior and camera remain section-owned.

World input SHA256 at release: `9cb7d5c946e8573abc05af4ee3c12492610a982c1773a6437f90a762055fb540`. Coordinate transforms, variants and physical provenance are owned by `../WellAssembly/World_interface_v010.json`.

Native files are local and Git-ignored. T-054 report owns evidence and review status. No locked previs is overwritten.
