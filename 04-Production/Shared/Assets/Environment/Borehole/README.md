# World — v011 with pinned v010 retained

`World_environment_v011.blend` adds seven illustrative regional geological units to the exact existing v010 physical variants. No measured stratigraphic log is claimed.

- `WORLD_DESCENT_CONNECTED`: regional geology plus exactly one existing S02 destination wall. Use alone for the connected descent.
- `WORLD_REGIONAL_DESCENT`: regional mass only, reserving the S02 local interval. Do not add a second destination wall when using the connected collection.
- All v010 physical collection names, mesh geometry, shape keys and transforms are retained. Cameras, lights and section measurement/history animation are excluded.
- `World_interface_v011.json` and `Scripts/world_interface_v011.py` provide selection and placement. Canonical axis X remains; `canonical_to_s02` maps to the descent's vertical Z.
- Illustrative sea/seabed at source Z=0/-120m; regional formation extends to -1020m with180m outer radius. The existing local S02 bore shape is unchanged.

Focused borehole demo: `04-Production/Shared/Demos/World_demo_v002.blend`. Connected surface-to-wall demo: `04-Production/Shared/Demos/Surface_descent_demo_v002.blend`.

World v010 and its interface/helper remain active and byte-exact for the accepted Digital v004 derivation and other pinned consumers. This revision does not automatically upgrade those assets or historical shot files. Final appearance/native acceptance remains with Radzi.
