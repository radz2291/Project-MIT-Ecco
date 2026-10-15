"""B102 gated Blender builder. Pending production inputs; NOT scene-validated.

Run only in a fresh background Blender, with -- <confirmed-config.json>.
Preserves linked ECCO/BHA; refuses to save incomplete/unsupported assemblies.
"""
import bpy
import json
import math
import sys
import hashlib
sys.dont_write_bytecode=True
from pathlib import Path
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
from compatibility_v001 import validate_config

args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
if len(args) != 1:
    raise SystemExit('Supply exactly one confirmed configuration; no default dimensions')
config_path = Path(args[0]).resolve()
c = json.loads(config_path.read_text(encoding='utf-8'))
asset = Path(__file__).resolve().parents[1]
product = (config_path.parent / c['product_library']).resolve()
if not product.is_file():
    raise SystemExit('Product source unavailable')
if hashlib.sha256(product.read_bytes()).hexdigest() != c.get('product_sha256'):
    raise SystemExit('Product source hash changed or was not pinned; reinspect before use')
# Measurement is read from linked mesh world geometry, not nominal brochure OD.
with bpy.data.libraries.load(str(product), link=True) as (src, dst):
    if c['product_collection'] not in src.collections:
        raise SystemExit('Product collection unavailable')
    dst.collections = [c['product_collection']]
product_collection = dst.collections[0]
housing = next(o for o in product_collection.all_objects if o.name == 'ECCO_HOUSING_SOURCE_MESH')
points = [housing.matrix_world @ v.co for v in housing.data.vertices]
for subcollection in product_collection.children:
    if subcollection.name == 'ECCO_TEMPORARY_CLOSURES':
        points += [o.matrix_world @ v.co for o in subcollection.all_objects
                   if o.type == 'MESH' for v in o.data.vertices]
tool_od = 2 * max(math.hypot(p.y, p.z) for p in points)
gate = validate_config(c, tool_od)
if not gate['ready']:
    raise SystemExit(json.dumps(gate, indent=2))
bha_path = (config_path.parent / c['bha_library']).resolve()
if not bha_path.is_file():
    raise SystemExit('Inspected BHA library unavailable')
with bpy.data.libraries.load(str(bha_path), link=True) as (src, dst):
    if c['bha_collection'] not in src.collections:
        raise SystemExit('BHA collection unavailable')
    dst.collections = [c['bha_collection']]
bha_collection = dst.collections[0]
bha_points = [o.matrix_world @ v.co for o in bha_collection.all_objects
              if o.type == 'MESH' for v in o.data.vertices]
if not bha_points:
    raise SystemExit('BHA source has no inspectable mesh envelope')
assembly_od = max(tool_od, 2*max(math.hypot(p.y,p.z) for p in bha_points))
gate = validate_config(c,assembly_od)
if not gate['ready']:
    raise SystemExit(json.dumps(gate,indent=2))
output = asset / 'WellAssembly_variants_v001.blend'
if output.exists():
    raise SystemExit('Refuse to overwrite a saved candidate; version the output')
# Only this isolated background process is cleared, after input gates pass.
for scene in list(bpy.data.scenes):
    if scene != bpy.context.scene:
        bpy.data.scenes.remove(scene)
scene = bpy.context.scene
for o in list(scene.objects):
    bpy.data.objects.remove(o, do_unlink=True)
master = bpy.data.collections.new('WELL_ASSEMBLY_v001')
scene.collection.children.link(master)


def collection(name):
    col = bpy.data.collections.new(name)
    master.children.link(col)
    return col


controls = collection('ASSEMBLY_CONTROLS')
linked = collection('ASSEMBLY_LINKED_HARDWARE')
root = bpy.data.objects.new('ASSEMBLY_TRAVEL_X', None)
controls.objects.link(root)
root['interface'] = 'Translate X in metres. Orientation/end mapping requires supplied BHA datum confirmation.'
rotation = bpy.data.objects.new('ASSEMBLY_ROTATION_X', None)
controls.objects.link(rotation)
rotation.parent = root
rotation['interface'] = 'Rotate local X in radians; sign must be confirmed from surface-to-bottom orientation.'
root.location.y = c['eccentricity_m']
for name, col in [('PRODUCT_LINK', product_collection), ('BHA_LINK', bha_collection)]:
    obj = bpy.data.objects.new(name, None)
    obj.instance_type = 'COLLECTION'
    obj.instance_collection = col
    linked.objects.link(obj)
    obj.parent = rotation


def shell(name, col, inner, outer, profile=None):
    """Cutaway cylindrical shell along source X; 270-degree retained section.

    Tessellation and cutaway angle are inspection choices, not well dimensions.
    The profile is an illustrative radial perturbation, not measured formation.
    """
    axial_steps, angular_steps = 96, 96
    verts, faces = [], []
    for layer in range(2):
        for i in range(axial_steps + 1):
            x = c['axial_start_m'] + c['span_m'] * i / axial_steps
            for j in range(angular_steps + 1):
                a = math.pi / 4 + 1.5 * math.pi * j / angular_steps
                r = (inner if layer == 0 else outer)
                if profile:
                    r += profile(x, a)
                verts.append((x, r*math.cos(a), r*math.sin(a)))
    row = angular_steps + 1
    layer_size = (axial_steps + 1) * row
    for layer in range(2):
        offset = layer * layer_size
        for i in range(axial_steps):
            for j in range(angular_steps):
                n = offset + i*row + j
                f = (n,n+1,n+1+row,n+row)
                faces.append(f if layer else tuple(reversed(f)))
    # Close angular and axial cut boundaries for robust downstream sections.
    for i in range(axial_steps):
        for j in (0,angular_steps):
            n=i*row+j
            faces.append((n,n+row,n+row+layer_size,n+layer_size))
    for i in (0,axial_steps):
        for j in range(angular_steps):
            n=i*row+j
            faces.append((n,n+layer_size,n+layer_size+1,n+1))
    mesh=bpy.data.meshes.new(name)
    mesh.from_pydata(verts,[],faces)
    mesh.update()
    obj=bpy.data.objects.new(name,mesh)
    col.objects.link(obj)
    obj['provenance']='Configuration sources; cutaway/tessellation are inspection choices'
    return obj


nominal=collection('WELL_NOMINAL')
irregular=collection('WELL_IRREGULAR_ILLUSTRATIVE')
spiral=collection('WELL_SPIRAL_ILLUSTRATIVE')
cased=collection('WELL_CASED_CEMENT')
hole_r=c['hole_diameter_m']/2
cement_r=c['cement_outer_diameter_m']/2
# Open hole uses a surface only: no invented formation shell thickness.
def surface(name,col,profile=None):
    verts,faces=[],[]
    for i in range(97):
        x=c['axial_start_m']+c['span_m']*i/96
        for j in range(97):
            a=math.pi/4+1.5*math.pi*j/96
            r=hole_r+(profile(x,a) if profile else 0)
            verts.append((x,r*math.cos(a),r*math.sin(a)))
    for i in range(96):
        for j in range(96):
            n=i*97+j
            faces.append((n,n+1,n+98,n+97))
    mesh=bpy.data.meshes.new(name)
    mesh.from_pydata(verts,[],faces);mesh.update()
    obj=bpy.data.objects.new(name,mesh);col.objects.link(obj)
    obj['status']='Illustrative wall surface, not rock thickness or measurement data'
    return obj
surface('NOMINAL_WALL',nominal)
surface('IRREGULAR_WALL',irregular,lambda x,a:c['irregular_amplitude_m']*math.sin(3*a)*math.sin(math.pi*(x-c['axial_start_m'])/c['span_m']))
surface('SPIRAL_WALL',spiral,lambda x,a:c['spiral_amplitude_m']*math.cos(a-2*math.pi*(x-c['axial_start_m'])/c['spiral_pitch_m']))
shell('CASING',cased,c['casing_id_m']/2,c['casing_od_m']/2)
shell('CEMENT',cased,c['casing_od_m']/2,cement_r)
for col in (irregular,spiral,cased):
    col.hide_viewport=True
    col.hide_render=True
master['configuration_json']=json.dumps(c,sort_keys=True)
master['fit_gate_json']=json.dumps(gate,sort_keys=True)
master['replacement']='Reinspect product/BHA dimensions and interfaces; rerun gate, drift/shoe/deviated checks and affected shots. Never assume unchanged sensor geometry.'
scene.unit_settings.system='METRIC'
scene.unit_settings.scale_length=1
scene['status']='Provisional foundation; manual dimension/interface/visibility/clearance inspection required before use'
for lib in bpy.data.libraries:
    lib.filepath=bpy.path.relpath(lib.filepath,start=str(asset))
bpy.ops.wm.save_as_mainfile(filepath=str(output))
