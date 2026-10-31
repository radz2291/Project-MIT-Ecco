"""Copy exact references, derive complete single-shot fallback prompts and package.

No image generation, image editing, Blender execution or source mutation.
"""
import hashlib
import json
import shutil
import zipfile
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
BASE = PACKAGE.parent
ROOT = next(p for p in PACKAGE.parents if (p / '04-Production').is_dir())
SHARED = ROOT / '04-Production/Shared/References'


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def copy_exact(src, dst):
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        if digest(src) != digest(dst):
            raise RuntimeError(f'Refusing to replace changed package input: {dst}')
    else:
        shutil.copy2(src, dst)
    assert digest(src) == digest(dst)
    return {'source': str(src), 'file': dst.relative_to(PACKAGE).as_posix(),
            'sha256': digest(dst), 'bytes': dst.stat().st_size}


def write_json(path, obj):
    path.write_text(json.dumps(obj, indent=2) + '\n', encoding='utf-8')


selection = json.loads((BASE / 'selection.json').read_text(encoding='utf-8'))
assert selection['count'] == 6
assert [s['frame'] for s in selection['stills']] == [241, 278, 348, 358, 480, 528]
assert (selection['columns'], selection['rows']) == (3, 2)

refs = [
    (BASE / 'reference-grid.png', '01-blender-six-shot-grid.png', 'Composition, geometry, layout and event states', 'Existing six-frame Blender reference sheet'),
    (SHARED / 'ECCO_Product_Metal_v003/ECCO_product-four-views_reflective-metal_v005.png', '02-tool-reflective-metal.png', 'Reflective machined steel appearance', 'Physical Blender reference render, not AI generated'),
    (Path('C:/Users/RZ1/AppData/Local/Temp/codex-clipboard-e3582b1f-299d-4b6b-ab36-6bcee9fb3f17.png'), '03-rock-solid-structure.png', 'Connected solid stone forms; final dark brown palette supplied in prompt', 'User-supplied rock photograph/reference; geological identity unverified'),
]
input_records = []
for index, (source, filename, role, provenance) in enumerate(refs, 1):
    record = copy_exact(source, PACKAGE / 'inputs' / filename)
    record.update({'image_index': index, 'role': role, 'provenance': provenance})
    input_records.append(record)

copy_exact(BASE / 'selection.json', PACKAGE / 'selection.json')
frame_records = []
for item in selection['stills']:
    record = copy_exact(BASE / item['file'], PACKAGE / item['file'])
    assert record['sha256'] == item['sha256'], f"Selected frame changed: {item['id']}"
    record.update({'id': item['id'], 'native_frame': item['frame'],
                   'position': item['position'], 'title': item['title'],
                   'provenance': item['provenance']})
    frame_records.append(record)

copy_exact(Path('C:/Users/RZ1/.codex/skills/blender-keyframe-stills/scripts/compose_grid.ps1'),
           PACKAGE / 'scripts/compose_grid.ps1')

main = (PACKAGE / 'prompts/01-six-shot-final.txt').read_text(encoding='utf-8')
def section(start, end):
    return main.split('\n' + start + '\n', 1)[1].split('\n' + end + '\n', 1)[0].strip()

materials = section('PRISTINE COMMERCIAL PRODUCT', 'SOLID ROCK')
materials = materials.replace('in every panel', 'throughout this image')
rock = section('SOLID ROCK', 'SHARED LIGHTING AND CAMERA LOOK')
rock = rock.replace("each panel's", "Image 1's")
camera = section('SHARED LIGHTING AND CAMERA LOOK', 'SIX SHOTS')
camera = camera.replace("Preserve the camera position, field of view and crop of each source panel.",
                        "Preserve Image 1's camera position, field of view and crop.")
camera = camera.replace('across the sequence', 'for this shot').replace('per panel', 'in this image')
camera = camera.replace('for each camera angle', 'for this camera angle')

single_input = '''Create one finished hyperrealistic commercial image from Image 1. Use Images 2 and 3 as appearance references. Replace the Blender-preview materials and lighting throughout this shot.

REFERENCE ROLES
Image 1 controls the camera, perspective, crop, instrument geometry, scale, rock opening, clearance and frozen event state. Its grey metal and plain brown rock are preview shading to replace.
Image 2 supplies the reflective machined silver steel appearance. Preserve Image 1's geometry wherever the references differ, including open ends, genuine sensor surfaces, covers and connections. Do not transfer the product sheet's layout or grey studio background.
Image 3 supplies connected solid stone forms and surface character. Borrow its ridges, grooves and tightly bonded fine texture, using dark brown and umber instead of its orange colour or strong sunlight.'''

moments = [
    'Opening wide, native frame 241. Match the narrow vertical opening and small central tool, with the pipe continuing above the frame. This is the establishing instant before the camera moves toward the sensor. Preserve the wide scale and surrounding rock. No acoustic signal or recorded-history overlay is active.',
    'Sensor approach, native frame 278. Match the closer vertical view with the large circular sensor and smaller circular feature beneath it. The camera has moved toward the same instrument; its physical size and design remain constant. Freeze before the acoustic demonstration with surrounding housing visible. No acoustic signal or recorded-history overlay is active.',
    'Outgoing pulse, native frame 348. Match the extreme close-up: circular sensor at right, rock wall at left. Freeze the cyan wavefronts travelling from the sensor toward the left wall. Preserve their visible count, positions, spacing and curvature in Image 1. Show delicate illustrative acoustic graphics and keep the sensor edge and wavefronts readable together. Preserve this outgoing phase without adding returning green echoes or history cells.',
    'Returning echo, native frame 358. Match the sensor close-up. Freeze the small green echo arcs immediately left of the sensor travelling back toward it after the wall response. Preserve the faint farther traces where visible in Image 1. Keep this return phase and the source signal positions; do not add recorded-history cells or a new wall-impact effect.',
    'History develops, native frame 480. Match the diagonal medium-wide view, lower instrument toward bottom-left and pipe extending toward top-right. The camera is pulling back and changing angle. Freeze the partially revealed blue recorded-wall cells and thin contours at their source positions and extent. Preserve the incomplete advancing boundary, keeping the opaque steel readable beneath the restrained translucent overlay.',
    'Full history reveal, native frame 528. Match the final wide diagonal view, complete visible tool toward bottom-left and a longer pipe interval extending toward top-right. Freeze the settled blue recorded-history display at the source full visible extent. Preserve the visible open lower end and existing geometry. Keep this wide framing rather than enlarging the instrument to fill the image.',
]
single_dir = PACKAGE / 'prompts/individual'
single_dir.mkdir(parents=True, exist_ok=True)
shot_map = []
for frame, moment in zip(frame_records, moments):
    name = f"{frame['id']}-f{frame['native_frame']}-final.txt"
    text = (single_input + '\n\nPRISTINE COMMERCIAL PRODUCT\n' + materials +
            '\n\nSOLID ROCK\n' + rock + '\n\nLIGHTING AND CAMERA\n' + camera +
            '\n\nFROZEN MOMENT\n' + moment +
            '\n\nSIGNAL MEANING\nWhere present in Image 1, cyan pulses, green echoes and blue history are explanatory measurement graphics. Keep the source signal phase and extent. They are not physical wires, rigid cages or a new transparent instrument shell. Recorded history reveals previously collected information. The instrument remains physically opaque.\n\n' +
            'OUTPUT\nOne clean 16:9 image containing this single view. No collage, split screen, additional hardware, labels, text, logos, watermarks, borders or reference swatches. Preserve the source framing and frozen state with pristine steel and solid brown rock.\n')
    (single_dir / name).write_text(text, encoding='utf-8')
    shot_map.append({'id': frame['id'], 'native_frame': frame['native_frame'],
                     'position_in_combined_sheet': frame['position'],
                     'prompt': f'prompts/individual/{name}',
                     'input_1': frame['file'], 'input_2': input_records[1]['file'],
                     'input_3': input_records[2]['file'], 'output_aspect': '16:9'})
write_json(PACKAGE / 'shot-map.json', shot_map)

manifest = {
    'package': 'Section 2 six-shot Nano Banana v005', 'date': '2026-10-31',
    'scope': 'Reference inputs and prompts only; no new AI generation or Blender render',
    'selection': {'file': 'selection.json', 'sha256': digest(PACKAGE / 'selection.json'),
                  'status': 'Existing explicit six-frame selection retained unchanged'},
    'layout': {'columns': 3, 'rows': 2, 'panel_aspect': '16:9', 'canvas_aspect': '8:3',
               'reference_pixels': [2880, 1080], 'reading_order': 'row-major',
               'model_or_node_exact_output_support': 'Not verified; see individual-shot fallback'},
    'inputs': input_records, 'stills': frame_records,
    'main_prompt': 'prompts/01-six-shot-final.txt', 'individual_prompts': 'shot-map.json',
    'image_generation_tested': False, 'generated_output_accepted': False,
    'source_blender_modified': False, 'media_backup_status': 'Local package; no remote media backup claimed',
}
write_json(PACKAGE / 'manifest.json', manifest)
print(json.dumps({'copied_inputs': len(input_records), 'verified_original_frames': len(frame_records),
                  'individual_prompts': len(shot_map), 'main_prompt_characters': len(main),
                  'package': str(PACKAGE)}, indent=2))


def make_zip():
    archive = PACKAGE.with_suffix('.zip')
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for item in sorted(PACKAGE.rglob('*')):
            if item.is_file() and '__pycache__' not in item.parts:
                z.write(item, (Path(PACKAGE.name) / item.relative_to(PACKAGE)).as_posix())
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        count = len(z.namelist())
    print(json.dumps({'zip': str(archive), 'files': count, 'bytes': archive.stat().st_size,
                      'sha256': digest(archive)}))


if __name__ == '__main__':
    # QA adds verification.json before the final archive is made.
    if (PACKAGE / 'verification.json').exists():
        make_zip()
