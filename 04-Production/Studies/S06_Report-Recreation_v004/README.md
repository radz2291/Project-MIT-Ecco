# S06 report recreation — v004 working still

One still for owner review. This is the single working version to refine through feedback; do not create a new proposal series or integrate animation before acceptance. Earlier studies remain unchanged.

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
