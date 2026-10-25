# S06 — v004 working A–B–C cinematic study

**Approved and closed — 25 October 2026.** The owner selected the polished v004 S06 previs. Start with [APPROVED_DELIVERY.md](APPROVED_DELIVERY.md) for the exact video, editable native, approval and closure records. Historical review wording below records earlier stages and is superseded by this approval.

## Scoped transition refinement

Actual camera samples and the prior rendered frames exposed irregular distance corrections during A→B, a rapid push-in while the map changed size during B→C, and a reconstruction guide grid that remained at its old coordinates as the colored map moved into the laptop. These were presentation problems; no engineering geometry needed correction.

`Scripts/polish_transitions.py` smooths the existing camera path over a short time window, coordinates camera distance with the changing map size, and keeps the same final camera pose. The guide grid clears before the map transfer, then report paper, supporting graphics, laptop hardware and room appear in sequence. Camera smoothing reduces maximum positional second difference from approximately 0.1165 to 0.0321 scene units per frame squared; this is a motion diagnostic, not independent viewer acceptance. Geometry, topology, sample colors, all 288 geometry/amplitude shape states, text inventory and duration are verified unchanged. Every-frame boundary checks cover frames 120–236. The steel fade also uses depth-correct dithered transparency to prevent internal surfaces flashing through. The sample schedule is 16 normally, 32 during frames 90–144 and 48 during frames 228–258; this is keyed in the editable native and checked against the strict render cap. Frames 1–144 were rerendered after consecutive-frame review exposed the steel sorting issue; the initial pass timing record is retained.

The current delivery and timings are in `Records/polish-delivery.json`; source preservation and actual changes are in `polish-build.json`; saved-native and framing evidence are in `polish-verification.json`. Dense A→B and B→C review sheets accompany the clean MP4. Live Work remained revision 747 with no S06-specific ticket, so this is directly owner-authorized refinement, not a change to unrelated task statuses. The live Blender v001 scene was dirty and left untouched. Earlier source limitations and anonymous illustrative-report safeguards continue to apply.

## Animation execution — 25 October 2026

One continuous camera carries A through B into C. Reconstruction samples emerge around the source-sized ECCO; physical hardware and fixed rock recede through a visibility transition. Only the separate data surface unfolds. The camera retreats to retain the complete surface, straightens as it reaches the flat map, then follows the same sample vertices into the report's geometry track. Independent amplitude follows into its own track. The camera pulls back to reveal the laptop and settles with a subtle final movement.

The animated native contains packed fonts and directly appended source hardware, without original report images or external Blender libraries. Reports remain illustrative and anonymous. `Scripts/animate_story.py` preserves originally hidden construction helpers; laptop target coordinates include their full parent transform. The existing still native remains unchanged. The dirty running Blender scene was left untouched.

Full-sequence QA prompted a bounded correction within v004: the unfolding camera now continuously aims at the displayed surface and checks both boundary columns and both end contours, while the laptop fade uses depth-correct dithered transparency. Frames 96–288 were rerendered; frames 1–95 are retained from the initial run. Both initial and retained-frame timing records remain available, and the delivery record separates retained-frame cost from total batch rendering including repairs. The preview still has modest low-sample grain during transparency; this is deliberately inexpensive previs.

`Records/animation-verification.json` records saved-native, sample correspondence, source mesh, text inventory, coordinate and conservative radial-clearance checks. `Records/animation-render-timings.json` records every final render call. `Records/animation-delivery.json` records actual video length, full decode and render/encoding timings. Rendering uses 1280 × 720 EEVEE with 16 samples; the batch stops if any frame reaches five seconds. Initial cold shader compilation checks exceeded the cap and are disclosed separately; the batch was released only after a passing representative benchmark.

Review media: `Previews/S06_animation-contact_v004.jpg` and `Previews/S06_animation-poster_v004.png`. These are a previs review, not final cinematic finishing or a claim of measured engineering data. Media/native/data are local; the D-drive copy is same-machine recovery. Only generic implementation and records are published. Exact synchronization is recorded locally in `Records/sync-verification.json`.

## Retained still-review record

The following preserves the composition decisions and checks preceding animation. Statements about animation pending describe that earlier review stage, superseded by the execution record above.

## Current scene direction contract

**Purpose:** ECCO's recorded information becomes a reconstructed borehole, opens into an organized map, and can be examined as engineering output on a laptop. The audience includes non-specialists and engineering viewers. This is an illustrative processed-data explanation, not a live telemetry shot or authentic field result.

| Beat | Intended sequence timing | Review image and camera purpose |
|---|---|---|
| A | 0–4 s | Actual ECCO geometry in a fixed sectional borehole. Diagonal view maintains product context; indexed surface samples and fine contours establish the reconstruction. The graphic seam has just begun opening. |
| B | 4–9 s | The same samples form the curling data surface, with an independent warm amplitude panel. Dark visualization space and an oblique view separate the representation from physical rock. The complete pair fits inside the frame. |
| C | 9–12 s | A bright recreated report sits inside a modeled laptop. Screen, bezel, hinge and keyboard establish a physical destination. The report remains the main subject. |

These are three composition states, not verified camera travel or event timing. The intended A→B environmental recession and B→C screen match remain to be animated after still review. The proposed orbit must preserve screen direction and avoid crossing steel/rock. Actual camera poses are recorded in `Records/ABC-build.json`; no spline or operational motion was invented for the stills.

**Preserve:** canonical hardware dimensions, earlier studies, report-inspired band structure, independent amplitude, anonymous labels and one v004 working revision. **Change:** replace the completed-object opening with contextual reconstruction; replace the flat report board with a laptop destination. **Review question:** can each still communicate its distinct discovery and do they read as one visual progression? Camera continuity, audience comprehension at normal playback and engineering/client acceptance remain unverified.

## Coherent illustrative data and source safeguards

The earlier standalone v004 report and v002 unfolding used different sources. For this approved still approach, `derive_story.py` authors one new explicitly illustrative radius field from the existing anonymous report-inspired visual trends. It uses a scene reference radius of 0.19 m with a maximum authored deviation of 0.0025 m and a 2.4 m display interval. These values establish a controlled proxy around the actual-size tool; they are **not recovered report measurements**. Colors have been normalized for readability, so their contrast is not a calibrated magnitude. No source text, values, names, dates or original PDF imagery is displayed.

A, B, C's miniature and C's geometry map share the identical sample colors and radius grid. C's profiles and sections are calculated from that grid. The source report's visual amplitude channel remains independent, and its colors match between B and C. The source graphic is not a validated full circumferential dataset; periodic seam handling and authored radius mapping are documented illustrative choices, not a recovery algorithm.

The physical rock is fixed. Only the separate graphic representation has stored opening poses. No rock or steel is animated to peel. `ECCO_master_temporary-plugs_v002.blend` supplies the hardware; local vertex coordinates and root scale remain unchanged. Its provisional caps and unresolved manufacturing/interface limits remain as documented by the source master. No shared master was modified.

## Current deliverables and verification

- `Previews/S06_ABC_review-strip_v004.jpg` — one review strip.
- `Previews/S06_A_v004.png`, `S06_B_v004.png`, `S06_C_v004.png` — individual 1280 × 720 stills.
- `Scenes/S06_ABC_study_v004.blend` — one editable native with separate A, B and C scenes.
- `Data/story_field.npz` — local illustrative shared field.
- `Records/ABC-build.json`, `ABC-verification.json`, `story-data.json` — timings, actual camera poses, correspondence and limitations.

The saved native reopens. A/B coordinates match the authored opening poses to below 0.000001 m; stored alternate shape keys are inactive in the review state. Geometry colors match exactly across A/B/C, and amplitude matches separately across B/C. The housing remains 2.400000095 m along its axis with an unchanged source mesh hash; a conservative radial check leaves approximately 0.0353 m between the opening graphic and the maximum hardware radius at the A still. This is a still-state envelope check, not swept collision validation. The B map pair fits within the image with margins. Fonts are packed, no source images or external Blender libraries are required, and all three retained renders are below five seconds per frame at EEVEE / 16 samples.

The actual stills were visually inspected. No animation or independent viewer test is claimed. Live Work remained revision 747 with no matching S06-v004 ticket; this is directly owner-authorized work. The dirty live Blender scene was queried read-only and left untouched. Native/media/data remain local with a hash-verified same-machine D-drive recovery copy; generic scripts and records use the existing publishing checkout. See `Records/sync-verification.json` for current sync evidence.

## Initial standalone report still — retained history

The following records the preceding report-only proof. Its isolated source relationship is superseded by the coherent illustrative A–B–C field described above. It remains useful reference material, not a competing new proposal.

## Direction

Recover v002's clear report composition while making the reconstructed form the visual focus. A large, softly lit form occupies a dark inset; profile, circular sections, geometry and amplitude sit on pale editorial panels. The source report's shallow horizontal banding and near-circular sections replace v002's more obviously synthetic enlargement pattern. The limited palette, precise contours and sculpted lighting supply the cinematic emphasis.

Own neutral labels only. There are no client, well, tool, date, serial, depth or measurement values. The only digits are generic graphic descriptions (3D and 360 degrees).

## Source and limits

The five anonymous graphic references prepared locally for v003 were inspected. This scene does not display those images or any PDF page. `derive_visuals.py` traces the visible silhouette, profile and circular outlines and samples separate geometry/amplitude color trends. `build_still.py` rebuilds new editable curves, colored meshes and a lit surface. The saved native contains no images or texture-image nodes; its font is packed.

This is an uncalibrated visual reconstruction, not recovered field measurements. Geometry and amplitude are independently contrast-normalized for readability. Their relative band locations follow the reference; no numeric palette or engineering dimension has been decoded. The 3D display is axisymmetric because the front silhouette cannot establish unseen shape. Its slight open lip is presentation geometry, not steel casing wall thickness. No physical scale, tool accuracy, new defect or hydraulic claim is made.

These graphics are from a separate visual example, not the illustrative samples used in the earlier unfolding. Any later integration must retain that distinction. V002's earlier camera and unfolding have not been edited; no animation was built this turn.

## Deliverables and checks

- `Previews/S06_report-recreation_v004.png` — one 1600 x 900 review still.
- `Scenes/S06_report-recreation_v004.blend` — editable standalone still scene.
- `Data/visual_structure.npz` — local dimensionless image-space observations; not measurements.
- `Records/visual-provenance.json`, `still-verification.json`, `saved-verification.json` — methods and checks.

EEVEE, 24 samples. First still render: 2.979 seconds, below the strict five-second limit. The rendered still was visually inspected. Reopened native verification checks finite coordinates, packed fonts, no linked libraries, no source images and no animation. These checks do not constitute client acceptance or an independent audience test.

The official live Blender query found a dirty v001 scene at frame 203. It was left untouched. Work ran in isolated Blender 5.2. Live Work revision 747 has no matching S06-v004 ticket; this bounded still follows the direct owner request, without creating a ticket or changing unrelated work.

## Storage and review boundary

Media, derived observations and native scene remain local. A same-machine D-drive recovery copy is provided at `D:/MIT-ECCO-Render-Recovery/S06-Report-Recreation_v004`. Only generic scripts and text/JSON records are synchronized through the existing publishing checkout. This is not an off-machine media backup.

Await feedback on this single still. Keep the same v004 paths for subsequent edits, and preserve earlier studies. No full animation, final-film assembly or client delivery is authorized by this still review.
