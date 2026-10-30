# Physical World v010

This is a versioned successor to v009 for ECCO-053. It preserves the original wall variants and adds the exact physical irregular wall from S02 v011. Only the surrounding soil expands. Existing scenes do not migrate automatically.

Use `Scripts/world_interface_v010.py` to link one named collection. `World_interface_v010.json` specifies the complete source-to-canonical and inverse placement matrices. Units are metres, the common axis is X. S02 source coordinates map as `(X,Y,Z)=(z+735,x,y)`; inverse placement restores its original depth and orientation.

- `WORLD_S02_IRREGULAR_AUTHORITY`: exact S02 physical inner wall mesh, hidden reference, no measured samples or display animation. Canonical axial extent −15 to +15m. This is authored illustrative geometry, not surveyed or calibrated data.
- `WORLD_S02_PHYSICAL_CUTAWAY`: the source's retained angular opening and inner wall, with its outer boundary extended from 0.32m to 20m. The `Outer_soil_margin_25m` shape key extends only the outside to 25m; it does not enlarge the borehole.
- Existing `WORLD_FORMATION_{NOMINAL,IRREGULAR,SPIRAL}_{FULL,CUTAWAY}` collections retain wall geometry and axial extent while extending their outer boundary from 2.4m to 20m transverse half-width. These outer cross-sections are square, so the corners reach 28.284m radial distance; the S02 outer boundary is cylindrical with radius20m. The legacy `outer_radius_m` metadata means half-width for these square modules, as clarified here.
- Existing casing and cement collections remain distinct physical layers. The selected Formation_context_v002, Formation_cased-section_v002 and CasedHole_v002 libraries are preserved as referenced modules. Their full/cutaway, nominal/wear and supported/channel variants are alternatives; do not stack competing variants.

Choose exactly one matching wall and formation variant at each placement. Set local instance `hide_render`/`hide_viewport` for layer visibility, and use the instance matrix for placement. Do not alter global library collection visibility. Physical layer order is fluid, casing if applicable, cement, formation. S04 masks, response graphics and timing remain section-owned. Full and cutaway representations are viewing choices, not physical changes.

The source S02 radius differs intentionally from the historical 0.155575m nominal radius. Do not scale the borehole or tool to conceal a clearance discrepancy. Use the exact source/profile that belongs to the consumer and retain its local data surface. The digital builder can derive presentation from the physical authority while keeping measured/reconstructed samples local.

Migration is explicit and reversible: save a consumer copy, replace its one physical shell with a linked instance, preserve its local appearance timing, then reopen and compare the camera/lens and behavior. S01 descent context coverage is verified by its assembly worker; a downhole preview is not proof that every surface view is covered.
