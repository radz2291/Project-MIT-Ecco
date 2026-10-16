import bpy,json,hashlib,array,math
from pathlib import Path
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
P=Path(__file__).resolve().parents[3];E=P/'Records/Tasks/T-007/Evidence/Motion_v002';r=json.loads((E/'build.json').read_text());checks=[]
def check(name,value):checks.append({'check':name,'pass':bool(value)})
def digest(mesh):
 co=array.array('f',[0.])*len(mesh.vertices)*3;mesh.vertices.foreach_get('co',co)
 ids=array.array('i',[0])*len(mesh.loops);mesh.loops.foreach_get('vertex_index',ids)
 return hashlib.sha256(co.tobytes()+ids.tobytes()).hexdigest()
source=P/'Mechanisms/B201/Scenes/B201_returning-echo_still04_v003.blend';bpy.ops.wm.open_mainfile(filepath=str(source));snap={}
for inst in bpy.context.evaluated_depsgraph_get().object_instances:
 ob=inst.object
 if inst.is_instance and ob.type=='MESH' and (ob.name.startswith('TEMP |') or ob.name=='ECCO_HOUSING_SOURCE_MESH'):
  me=ob.to_mesh();snap[ob.name]=digest(me);ob.to_mesh_clear()
check('accepted Still04 source unchanged',hashlib.sha256(source.read_bytes()).hexdigest()==r['source_still04_sha256'])
out=P/r['scene'];bpy.ops.wm.open_mainfile(filepath=str(out));s=bpy.context.scene;bpy.context.window.view_layer=s.view_layers['FAST model and mechanism'];s.frame_set(1);bpy.context.view_layer.update()
check('candidate saved hash',hashlib.sha256(out.read_bytes()).hexdigest()==r['scene_sha256'])
for rel,h in r['inputs'].items():check('accepted master unchanged '+rel,hashlib.sha256((P/rel).read_bytes()).hexdigest()==h)
check('preview product preserves exact evaluated topology and vertex coordinates',all(digest(bpy.data.objects[x['consumer']].data)==snap[x['source']] for x in r['product_instances']))
check('fixed accepted camera',list(s.camera.location)==r['camera']['location'] and list(s.camera.rotation_euler)==r['camera']['rotation'] and s.camera.data.lens==r['camera']['lens_mm'])
check('fast EEVEE960x540 profile',s.render.engine=='BLENDER_EEVEE' and s.render.resolution_x==960 and s.render.resolution_y==540 and s.eevee.taa_render_samples==32)
check('10 seconds constant24fps native timeline',s.frame_start==1 and s.frame_end==240 and s.render.fps==24)
check('relative libraries resolve',all(x.filepath.startswith('//') and Path(bpy.path.abspath(x.filepath)).is_file() for x in bpy.data.libraries))
check('Still05 scene collection absent',bpy.data.collections.get('STILL05_MEASUREMENT_GRAPHICS') is None)
check('no visible text/waveform/distance graphics',not any(o.type=='FONT' for o in s.view_layers['FAST model and mechanism'].objects))
for name in ('B201_PULSE_ECHO','B201_CONTACT_HISTORY','B201_SPATIAL_GRAPHICS'):check('legacy diagnostics excluded '+name,s.view_layers['FAST model and mechanism'].layer_collection.children[name].exclude)
wallob=bpy.data.objects['T6_WALL_CONTACT_SECTION'];tree=BVHTree.FromPolygons([v.co for v in wallob.data.vertices],[list(p.vertices) for p in wallob.data.polygons]);control=bpy.data.objects['B201_MOTION_CONTROL'];cap=bpy.data.objects['PREVIEW | TEMP | Imaging port 1 | removable acoustic cap'];tx=bpy.data.objects['OUTGOING_WAVEFRONT_ILLUSTRATION_3'];echo=bpy.data.objects['RETURNING_ECHO_FIRST_RECEPTION']
for e in r['events']:
 receiver=Vector(e['receiver']);wall=Vector(e['wall']);name='cycle '+str(e['cycle'])
 check(name+' sourced fixed-wall ray correspondence',tree.find_nearest(wall)[3]<1e-6)
 check(name+' correct round-trip order',e['emit_frame']<e['contact_frame']<e['receive_frame'] and e['contact_frame']-e['emit_frame']==e['receive_frame']-e['contact_frame'])
 s.frame_set(e['contact_frame']);bpy.context.view_layer.update()
 check(name+' outgoing front reaches wall',(tx.matrix_world@tx.data.vertices[0].co-wall).length<2e-6)
 check(name+' digitization begins at contact',bpy.data.objects['ACOUSTIC_CONTACT_CONTROLLER']['scan_fade']>0)
 s.frame_set(e['receive_frame']-1);check(name+' reception response not early',control['receive']==0)
 s.frame_set(e['receive_frame']);bpy.context.view_layer.update()
 check(name+' return reaches same emitting sensor',(echo.matrix_world@echo.data.vertices[0].co-receiver).length<2e-6)
 cap_tree=BVHTree.FromPolygons([cap.matrix_world@v.co for v in cap.data.vertices],[list(p.vertices) for p in cap.data.polygons])
 check(name+' receiver on original physical cap surface',cap_tree.find_nearest(receiver)[3]<2e-6)
 check(name+' exact first reception drives emerald response',control['receive']>0)
check('three early ping sampling stations',len(r['events'])==3 and [e['rotation_degrees'] for e in r['events']]==[0,6,12])
check('no real-time acoustic speed claimed',not r['physical_time_claim'])
times=json.loads((E/'inspection-render-times.json').read_text());check('all representative frames under10seconds',max(x['seconds'] for x in times)<10)
result={'checks':checks,'passed':all(x['pass'] for x in checks),'executor_self_check':True,'Still05_excluded':True,'waveform_moving_criterion':'Deferred / excluded at owner instruction','technical_review_pending':True}
(E/'verification.json').write_text(json.dumps(result,indent=2));assert result['passed'],[x for x in checks if not x['pass']];print('MOTION_VERIFY_PASS',len(checks))
