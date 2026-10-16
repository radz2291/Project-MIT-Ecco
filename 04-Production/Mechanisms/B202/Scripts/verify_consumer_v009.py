import bpy,sys,math,json,hashlib
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[4];BASE=ROOT/'04-Production/Mechanisms/B202';DATA=BASE/'Data/v009';E=ROOT/'04-Production/Records/Tasks/T-008/Evidence/v009';sys.path.insert(0,str(BASE/'Scripts'))
from acquisition_core_v009 import *
from replay_interface_v009 import apply_event_pose,grid_at_time
C=read_json(BASE/'acquisition_config_v009.json');INDEX=read_json(DATA/'index_v009.json');manifest=read_json(E/'consumer_manifest_v009.json');checks=[];outputs=[]
def check(name,p,detail=None):
    out={'check':name,'pass':bool(p)}
    if detail is not None:out['detail']=detail
    checks.append(out)
def update(c):c.update_tag();bpy.context.view_layer.update()
def evaluated(o):
    ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();vs=[tuple(v.co) for v in me.vertices];ids=[p.value for p in me.attributes['cell_index'].data] if 'cell_index' in me.attributes else [];ev.to_mesh_clear();return vs,ids
master=BASE/'Scenes/B202_measured-envelope_master_v009.blend';bpy.ops.wm.open_mainfile(filepath=str(master));s=bpy.context.scene;c=bpy.data.objects['B202_CONTROL'];update(c)
check('consumer index provenance hash',manifest['source_data_index_sha256']==hashlib.sha256((DATA/'index_v009.json').read_bytes()).hexdigest())
check('relative product library resolves',all(lib.filepath.startswith('//') and Path(bpy.path.abspath(lib.filepath)).exists() for lib in bpy.data.libraries))
check('legacy visual-only geometry/amplitude cannot render',all(bpy.data.collections[n].hide_render and bpy.data.collections[n].hide_viewport for n in ['B202_INFORMATION','B202_PHYSICAL_WALL']))
for name,meta in manifest['objects'].items():
    o=bpy.data.objects[name];case=meta['case'];grid=read_json(DATA/'interpolation_fixture_grid_v009.json.gz') if case=='interpolation_fixture' else read_json(DATA/INDEX['cases'][case]['files']['grid']);cells=[grid['cells'][i] for i in meta['vertex_cells']]
    check('cell lineage '+name,[v.value for v in o.data.attributes['cell_index'].data]==meta['vertex_cells'])
    check('derived radius positions '+name,all((v.co-Vector((p['x_m'],p['radius_m']*math.cos(p['azimuth_rad']),p['radius_m']*math.sin(p['azimuth_rad'])))).length<1e-6 for v,p in zip(o.data.vertices,cells)))
    check('quantity scalar '+name,all(abs(a.value-(p['delta_radius_m'] if meta['field']=='radius' else p['echo_strength']))<1e-6 for a,p in zip(o.data.attributes['delta_radius_m' if meta['field']=='radius' else 'echo_strength'].data,cells)))
    attr=next(n for n in o.data.materials[0].node_tree.nodes if n.type=='ATTRIBUTE').attribute_name;check('distinct colormap input '+name,attr==('geometry_display' if meta['field']=='radius' else 'echo_strength_display'))
    expected=[(p['delta_radius_m']+.0012)/.0266 if meta['field']=='radius' else (p['echo_strength'] or 0)/.4 for p in cells]
    check('display normalization comes only from named scalar '+name,all(abs(a.value-v)<1e-6 for a,v in zip(o.data.attributes[attr].data,expected)))
check('no decorative procedural texture in active quantity materials',all(n.type not in {'TEX_NOISE','TEX_WAVE','TEX_VORONOI','TEX_MUSGRAVE'} for name in ['B202_v009_delta_radius','B202_v009_received_echo_strength'] for n in bpy.data.materials[name].node_tree.nodes))
# Evidence-based time/validity visibility, not UV/procedural reveal.
case='irregular_layers';c['data_case']=manifest['case_names'].index(case);c['show_reconstruction']=1;c['show_echo_strength']=0;c['event_time_s']=5.8;update(c);o=bpy.data.objects[f'B202_v009_{case}_radius'];vs,ids=evaluated(o);grid=read_json(DATA/INDEX['cases'][case]['files']['grid']);check('partial replay shows only completed acquired bins',0<len(vs)<len(o.data.vertices) and all(grid['cells'][i]['ready_timestamp_s']<=5.800001 for i in ids))
c['event_time_s']=1000.;update(c);check('full replay restores measured grid',len(evaluated(o)[0])==len(o.data.vertices))
c['data_case']=manifest['case_names'].index('sparse_irregular');update(c);sp=bpy.data.objects['B202_v009_sparse_irregular_radius'];check('sparse case leaves unsupported surface absent',len(evaluated(sp)[0])<len(o.data.vertices))
c['data_case']=manifest['case_names'].index('interpolation_fixture');c['show_interpolated']=0;update(c);fi=bpy.data.objects['B202_v009_interpolation_fixture_radius'];n0=len(evaluated(fi)[0]);c['show_interpolated']=1;update(c);check('interpolation requires explicit visibility opt-in',len(evaluated(fi)[0])==n0+1)
# Same measured event can position whole hardware and its real sensor reference.
evs=read_json(DATA/INDEX['cases']['eccentric_nominal']['files']['events']);event=next(e for e in evs if e['valid_tof'] and e['sensor_id']==2);c['show_tool']=1;apply_event_pose(c,event);update(c);ref=bpy.data.objects['B202_SENSOR_REF_03'];check('replay pose matches acquired emitter world origin',(ref.matrix_world.translation-Vector(event['sensor_origin_m'])).length<2e-6)
ray=(ref.matrix_world.to_3x3()@Vector((0,0,1))).normalized();check('replay pose matches acquired emitter ray',(ray-Vector(event['outward_direction'])).length<2e-6)
partial=grid_at_time(read_json(DATA/INDEX['cases']['irregular_layers']['files']['events']),C,'irregular_layers',.5);check('raw replay interface excludes future averages',all(p['ready_timestamp_s']<=.5 for p in partial['cells'] if p['measured']))
check('no cinematic animation or keyed actions',s.frame_start==s.frame_end==1 and not any(o.animation_data and o.animation_data.action for o in s.objects))
outputs.append({'path':master.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(master.read_bytes()).hexdigest(),'bytes':master.stat().st_size})
# Reopen every exact review consumer and verify its image/state correspondence.
for item in manifest['stills']:
    path=ROOT/item['scene'];bpy.ops.wm.open_mainfile(filepath=str(path));s=bpy.context.scene;c=bpy.data.objects['B202_CONTROL'];update(c)
    check('saved review state '+item['case']+'/'+item['field'],c['data_case']==manifest['case_names'].index(item['case']) and c['show_reconstruction']==int(item['field']=='radius') and c['show_echo_strength']==int(item['field']=='echo_strength'))
    check('exact image/native hashes '+item['case']+'/'+item['field'],hashlib.sha256(path.read_bytes()).hexdigest()==item['scene_sha256'] and hashlib.sha256((ROOT/item['image']).read_bytes()).hexdigest()==item['image_sha256'])
    im=bpy.data.images.load(str(ROOT/item['image']));check('image size/render path '+item['case']+'/'+item['field'],tuple(im.size)==(1280,720) and s.render.filepath==str(ROOT/item['image']))
    for p in [path,ROOT/item['image']]:outputs.append({'path':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size})
# Append the entire master to a clean scene and exercise the remapped controls.
bpy.ops.wm.read_factory_settings(use_empty=True)
with bpy.data.libraries.load(str(master),link=False) as (src,dst):dst.collections=['B202_MEASURED_ENVELOPE_v009']
bpy.context.scene.collection.children.link(dst.collections[0]);c=bpy.data.objects['B202_CONTROL'];c['data_case']=manifest['case_names'].index('irregular_layers');c['event_time_s']=5.8;c['show_reconstruction']=1;update(c);o=bpy.data.objects['B202_v009_irregular_layers_radius'];check('fresh append preserves data reveal drivers',0<len(evaluated(o)[0])<len(o.data.vertices))
check('fresh append library remains accessible',all(Path(bpy.path.abspath(l.filepath)).exists() for l in bpy.data.libraries))
before=read_json(E/'preservation_before_v009.json');check('v008 and accepted sources remain byte-preserved',all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in before.items()))
out={'passed':sum(p['pass'] for p in checks),'total':len(checks),'checks':checks,'outputs':outputs,'spec_test_10':'deferred_to_T27_not_passed','limits':'Data binding/replay primitives and static render integrity, not playable proof or cinematic QA.'};write_json(E/'verification_consumer_v009.json',out);print(json.dumps({'passed':out['passed'],'total':out['total'],'failures':[p for p in checks if not p['pass']]}));assert all(p['pass'] for p in checks)
