"""Fresh-open source correspondence and surface-placement checks, not MIT validation."""
import bpy,json,hashlib,struct
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
P=Path(__file__).resolve().parents[3];E=P/'Records/Tasks/T-008/Evidence/Still_01'
r=json.loads((E/'build-render_v002.json').read_text());checks={}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def snapshot():
    s=bpy.context.scene;s.frame_set(31);bpy.context.window.view_layer=s.view_layers['FAST model and mechanism'];bpy.context.view_layer.update()
    out={}
    for o in s.objects:
        if o.name.startswith('PREVIEW | ') or o.name=='T6_WALL_CONTACT_SECTION':
            h=hashlib.sha256()
            for v in o.data.vertices:h.update(struct.pack('<3f',*v.co))
            for p in o.data.polygons:h.update(struct.pack('<'+'I'*len(p.vertices),*p.vertices))
            out[o.name]={'mesh':h.hexdigest(),'matrix':tuple(v for row in o.matrix_world for v in row)}
    out['camera']={'matrix':tuple(v for row in s.camera.matrix_world for v in row),'lens':s.camera.data.lens}
    out['actions']=len(bpy.data.actions)
    return out
source=P/r['source'];bpy.ops.wm.open_mainfile(filepath=str(source));baseline=snapshot()
candidate=P/r['scene'];checks['candidate_hash']=sha(candidate)==r['scene_sha256']
bpy.ops.wm.open_mainfile(filepath=str(candidate));current=snapshot()
checks['exact_product_wall_geometry_and_transforms']=baseline==current
checks['no_new_animation_actions']=baseline['actions']==current['actions']
checks['T7_input_unchanged']=sha(source)==r['source_sha256']
checks['T5_T6_sources_unchanged']=all(sha(P/p)==h for p,h in r['inputs'].items())
checks['relative_libraries_resolve']=all(l.filepath.startswith('//') and Path(bpy.path.abspath(l.filepath)).exists() for l in bpy.data.libraries)
s=bpy.context.scene;wall=bpy.data.objects['T6_WALL_CONTACT_SECTION']
tree=BVHTree.FromPolygons([wall.matrix_world@v.co for v in wall.data.vertices],[list(p.vertices) for p in wall.data.polygons])
errors=[];corner_errors=[];offset_errors=[]
for p in r['samples']:
    o=bpy.data.objects[p['object']];errors.append(tree.find_nearest(Vector(p['hit']))[3])
    for v,hit in zip(o.data.vertices,p['corner_hits']):
        corner_errors.append(tree.find_nearest(Vector(hit))[3])
        offset_errors.append(abs((o.matrix_world@v.co-Vector(hit)).length-.00010))
checks['all_144_centers_on_retained_wall']=len(errors)==144 and max(errors)<1e-6
checks['all_576_tile_corners_projected_to_wall']=len(corner_errors)==576 and max(corner_errors)<1e-6
checks['saved_tile_offset_matches_0_10mm']=max(offset_errors)<1e-6
ctl=bpy.data.objects['B202_SAMPLE_DISPLAY_CONTROL'];samples=[bpy.data.objects[p['object']] for p in r['samples']]
checks['sample_collection_visible']=not s.view_layers['FAST model and mechanism'].layer_collection.children['B202_ILLUSTRATIVE_SAMPLE_HISTORY'].exclude
checks['tile_dimensions_control']=all(abs(float(o.scale.x)-ctl['display_radius_m'])<1e-7 for o in samples)
ctl['visible']=0;ctl.update_tag(refresh={'OBJECT'});s.frame_set(31);bpy.context.view_layer.update();hidden=all(o.hide_render for o in samples)
ctl['visible']=1;ctl.update_tag(refresh={'OBJECT'});s.frame_set(31);bpy.context.view_layer.update();checks['sample_visibility_control']=hidden and all(not o.hide_render for o in samples)
checks['no_sample_actions']=all(not o.animation_data.action for o in samples)
im=P/r['image'];header=im.read_bytes()[:24]
checks['PNG_1920x1080']=header[:8]==b'\x89PNG\r\n\x1a\n' and struct.unpack('>II',header[16:24])==(1920,1080)
checks['image_hash']=sha(im)==r['image_sha256']
checks['explicit_illustrative_status']=not r['actual_data'] and r['visual_approval']=='pending' and not r['new_motion']
result={'all_pass':all(checks.values()),'checks':checks,'max_center_error_m':max(errors),'max_corner_error_m':max(corner_errors),'max_display_offset_error_m':max(offset_errors),'limitations':'Implementation self-checks only. Current pose corresponds to accepted T7; historical acquisition schedule, negative-X traversal and display density are illustrative. Geometry/amplitude reconstruction not built. Visual and MIT acceptance pending.'}
(E/'verification_v002.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));assert result['all_pass']
