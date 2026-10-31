# ECCO provisional master v001 — interface and replacement record

T-005 / B101, 15 October 2026. Internal mechanical foundation for Radzi review. No MIT engineering or rights approval is created.

## Source and measured geometry

Import the **ECCO_MASTER_v001** collection from [ECCO_master_v001.blend](ECCO_master_v001.blend), using a relative Blender library path. The inspection cameras sit outside this collection. Preserve v001 when creating later versions. This master wraps the earlier registered import; STEP was not independently retessellated in this run.

Source geometry: one connected mesh, 348,876 vertices, source X longitudinal, coordinates originally in mm with object scale 0.001; scene metres, scale_length 1. No rescaling, vertex/topology edits, fabricated acoustic faces, plugs, closures or internals. [Original imported scene](Originals/Source_Imported_ecco.blend) and original STEP copy are byte-preserved. [Annotated reference](Originals/Client_Confirmed_Sensor.png) identifies the larger recess beside the rectangular cover; the [historical implementation report](Originals/IMPLEMENTATION_REPORT.md) supplies the recess-centre interpretation. Its older delivery paths and approval language are historical, not current authority.

| Item | Inspected value | Limit |
|---|---|---|
| Overall source X bounds | 0 to 2.400000095 m | Source mesh ends, not pin shoulders; 2.25 m nominal brochure unresolved |
| World bounding box Y / Z span | 0.302608788 / 0.303737700 m | Different extrema occur at different azimuths |
| Maximum diameter about source X axis | 0.304800137 m | Corresponds to nominal 12 in / 0.3048 m; not thread/clearance certification |
| Imaging recess plane | X = 0.730 m | Inherited rim centres; not verified transducer faces |
| Sensor angles in source YZ plane | 39 / 159 / 279 degrees | Three references separated by 120 degrees |
| Recess-centre radius | approx. 0.129 m | Historical rim-centre interpretation, not active-face offset |
| Source end interfaces | source X=0 and X=2.400 m bounds | Top/box vs bottom/pin and shoulder coordinates not assigned as certified datums |
| Mud sensor | Unlocated | Hidden placeholder has no usable coordinate |

Brochure pp.1–3 states three imaging sensors at 120 degrees, plane 600 mm above the lower pin shoulder, top 6-5/8 F.H. box, bottom 6-5/8 F.H. pin, fishing neck 8.25 in, minimum ID 2.25 in, minimum casing ID 12.3 in. These are source specifications, not measurements validated by this mesh. Do not rescale to force nominal agreement. A 600 mm shoulder offset cannot be checked without identifying the shoulder. The preserved imported mesh has no independently established manufacturing revision or thread fit.

## Stable interfaces

| Name | Use |
|---|---|
| ECCO_ROOT | Whole assembly translation; source origin retained |
| ECCO_ROTATION_X | Local X rotation in radians; child of root. Confirm end/viewpoint before clockwise drilling animation |
| ECCO_GEOMETRY_REPLACEABLE / ECCO_HOUSING_SOURCE_MESH | Replaceable geometry only, parented to rotation control |
| ECCO_SENSOR_REFERENCES / ECCO_SENSOR_REF_01–03 | Separate recess-centre transforms; local +Z points radially outward. Pending acoustic face confirmation |
| ECCO_SENSOR_PLANE_PROVISIONAL | X=0.730 m reference; no rendered surface |
| ECCO_MUD_SENSOR_UNLOCATED | Hidden, unusable placeholder; do not bind effects |
| ECCO_EFFECTS_EMPTY | Reserved separate effects collection; no physical simulation |
| ECCO_CUTAWAY_TOOLS / ECCO_CUTTER_PREVIEW_ONLY | Hidden section cutter, follows rotation; optional Boolean on housing disabled for viewport/render |

Rotation/scanning references are separated without guessing physical subassemblies from a continuous mesh. The section modifier is an illustrative editing interface; it does not validate internal hardware and is not used in inspection renders. All geometry remains monolithic because supplied component identities are absent. Hardware-dependent internal/cutaway claims remain blocked.

## Plugged replacement procedure — O14

1. Register received file, date, supplier/version, rights and SHA-256; preserve it in Originals. Do not overwrite v001.
2. Inspect units, source axes, complete bounds, axial/radial dimensions, closures, pad profile, top/box and lower/pin identity, thread/shoulder datums, imaging count/positions/face normals and dedicated mud sensor. Compare measured values to v001 and supplied engineering evidence; never assume unchanged sensors.
3. Build a new versioned master; map geometry into source coordinates deliberately. Reparent to controls, preserve stable names where compatible, remap sensor references from evidence and reattach optional section modifier to the replacement housing. Record any incompatible interface changes.
4. Relink a test consumer, exercise axial travel and full rotation, visibility and section controls; verify sensor origins, pulse/echo return/contact, well/bit/casing clearances, camera occlusion and continuity for every affected mechanism/shot.
5. Save new inspection views, comparisons and hashes; update manifests/blockers and ticket evidence. Reopen affected accepted reviews where the change is substantive. Record which supported hardware version the film depicts before B4.

S01–S07 visible-product assets and B102/B201–B205 require compatibility review before reuse. Missing replacement does not stop independent preparation, but prevents claiming replacement compatibility or final hardware acceptance. Radzi supplies the model and obtains MIT decisions on length/datum, transducer detail and mud sensor.
