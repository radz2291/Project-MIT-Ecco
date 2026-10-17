"""Reopen baseline and candidate, check actual saved geometry/events/graphics."""
import bpy,json,hashlib,array,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
P=Path(__file__).resolve().parents[3]; E=P/'Records/Tasks/T-007/Evidence/Motion_v006'; r=json.loads((E/'build.json').read_text()); checks=[]
def check(name,ok): checks.append(dict(check=name,pass_=bool(ok)))
def digest(mesh):
 co=array.array('f',[0.])*len(mesh.vertices)*3; mesh.vertices.foreach_get('co',co); ids=array.array('i',[0])*len(mesh.loops); mesh.loops.foreach_get('vertex_index',ids); return hashlib.sha256(co.tobytes()+ids.tobytes()).hexdigest()
base=P/r['baseline_scene']; check('accepted v005 binary hash preserved',hashlib.sha256(base.read_bytes()).hexdigest()==r['baseline_sha256'])
for item in json.loads((P/'Records/Tasks/T-007/Evidence/Motion_v005/output-manifest.json').read_text())['outputs']:
 check('accepted v005 retained: '+item['path'],hashlib.sha256((P/item['path']).read_bytes()).hexdigest()==item['sha256'])
bpy.ops.wm.open_mainfile(filepath=str(base)); s=bpy.context.scene; bpy.context.window.view_layer=s.view_layers['FAST model and mechanism']; s.frame_set(1)
names=[x['consumer'] for x in r['product_instances']]+['T6_WALL_CONTACT_SECTION']; snap={n:digest(bpy.data.objects[n].data) for n in names}
source_camera=(list(s.camera.location),list(s.camera.rotation_euler),s.camera.data.lens)
out=P/r['scene']; check('candidate binary hash matches',hashlib.sha256(out.read_bytes()).hexdigest()==r['scene_sha256'])
bpy.ops.wm.open_mainfile(filepath=str(out)); s=bpy.context.scene; bpy.context.window.view_layer=s.view_layers['FAST model and mechanism']; s.frame_set(1)
for n,h in snap.items(): check('exact baseline mesh retained: '+n,digest(bpy.data.objects[n].data)==h)
check('camera transform and lens unchanged',source_camera==(list(s.camera.location),list(s.camera.rotation_euler),s.camera.data.lens))
for rel,h in r['inputs'].items(): check('accepted master hash: '+rel,hashlib.sha256((P/rel).read_bytes()).hexdigest()==h)
check('relative source libraries resolve',all(x.filepath.startswith('//') and Path(bpy.path.abspath(x.filepath)).is_file() for x in bpy.data.libraries))
check('packed editorial font',any(f.packed_file for f in bpy.data.fonts))
check('240 frames24fps960x540EEVEE',s.frame_end==240 and s.render.fps==24 and (s.render.resolution_x,s.render.resolution_y)==(960,540) and s.render.engine=='BLENDER_EEVEE')
check('first ping longer than both abbreviated repeats',r['events'][0]['leg_frames']>max(e['leg_frames'] for e in r['events'][1:]))
tx=sorted([o for o in s.objects if o.name.startswith('OUTGOING_WAVEFRONT_ILLUSTRATION_')],key=lambda o:o.name); echo=bpy.data.objects['RETURNING_ECHO_FIRST_RECEPTION']; contact=bpy.data.objects['ACOUSTIC_CONTACT_CONTROLLER']; ctrl=bpy.data.objects['B201_MOTION_CONTROL']; cap=bpy.data.objects['PREVIEW | TEMP | Imaging port 1 | removable acoustic cap']
root=bpy.data.objects['FAST_PREVIEW_TOOL_ROTATION']
check('all product consumers rotate under one root',all(bpy.data.objects[x['consumer']].parent==root for x in r['product_instances']))
wallob=bpy.data.objects['T6_WALL_CONTACT_SECTION']; tree=BVHTree.FromPolygons([wallob.matrix_world@v.co for v in wallob.data.vertices],[list(p.vertices) for p in wallob.data.polygons])
for e in r['events']:
 name='ping '+str(e['cycle']); receiver=Vector(e['receiver']); wall=Vector(e['wall']); speed=e['standoff_m']/e['leg_frames']
 check(name+' equal outward/return legs and event order',e['emit_frame']<e['contact_frame']<e['receive_frame'] and e['contact_frame']-e['emit_frame']==e['receive_frame']-e['contact_frame'])
 check(name+' exact rock point',tree.find_nearest(wall)[3]<2e-6)
 s.frame_set(e['contact_frame']); bpy.context.view_layer.update(); check(name+' leading front hits rock',(tx[-1].matrix_world@tx[-1].data.vertices[0].co-wall).length<2e-6)
 positions=[]
 for f in range(e['contact_frame']-5,e['contact_frame']+1): s.frame_set(f); bpy.context.view_layer.update(); positions.append(tx[-1].matrix_world@tx[-1].data.vertices[0].co)
 check(name+' saved constant velocity through impact',all(abs((b-a).length-speed)<2e-6 for a,b in zip(positions,positions[1:])))
 for i,ob in enumerate(tx):
  lag=max(x['radius_m'] for x in tx)-ob['radius_m']; f=math.ceil(e['contact_frame']+lag/speed+2); s.frame_set(f); check(name+f' shell{i} disappears after its wall arrival',ob.hide_render and ctrl[f'wall_stop_{i}']==0)
 s.frame_set(e['contact_frame']+10); check(name+' grid removed within10frames',contact['scan_fade']==0)
 s.frame_set(e['receive_frame']-1); check(name+' no early reception glow',ctrl['receive']==0)
 s.frame_set(e['receive_frame']); bpy.context.view_layer.update(); check(name+' reflected cap returns to original emitter',(echo.matrix_world@echo.data.vertices[0].co-receiver).length<2e-6)
 cap_tree=BVHTree.FromPolygons([cap.matrix_world@v.co for v in cap.data.vertices],[list(p.vertices) for p in cap.data.polygons]); check(name+' same physical cap receives',cap_tree.find_nearest(receiver)[3]<2e-6)
 s.frame_set(e['contact_frame']+1); check(name+' return originates at exact rock intersection',(echo.location-wall).length<2e-6)
check('contact area reduced to17.64percent nominal',all(abs(r['patch_after'][k]/r['patch_before'][k]-.42)<1e-6 for k in ('scan_radius_x_m','scan_radius_y_m')))
check('contact opacity reduced to48percent',abs(r['patch_after']['scan_opacity']/r['patch_before']['scan_opacity']-.48)<1e-6)
s.frame_set(59); check('echo graphic absent before reception',ctrl['echo_graphic']==0 and ctrl['interval_graphic']==0)
s.frame_set(72); check('timing graphic present after same ping reception',ctrl['echo_graphic']==1 and ctrl['interval_graphic']==1 and ctrl['sent_graphic']==1)
s.frame_set(150); check('timing overlay gone for repeated acquisition',ctrl['panel']==0 and ctrl['graphic']==0)
texts={o.data.body for o in s.view_layers['B201 timing editorial'].objects if o.type=='FONT'}; check('minimal exact copy only',texts=={'Echo timing reveals distance','Pulse sent','Echo received','Round-trip delay'})
check('editorial layer composites independently above mechanism',any(n.bl_idname=='CompositorNodeRLayers' and n.layer=='B201 timing editorial' for n in s.compositing_node_group.nodes))
check('old KIV Still05 graphics absent',bpy.data.collections.get('STILL05_MEASUREMENT_GRAPHICS') is None)
check('no B202 scene or acquisition data introduced',not any('B202' in o.name for o in s.objects))
check('no physical calibration claimed',not r['physical_time_claim'])
result=dict(passed=all(x['pass_'] for x in checks),checks=checks,executor_self_check=True,technical_approval=False)
(E/'verification.json').write_text(json.dumps(result,indent=2)); print('VERIFICATION',len(checks),result['passed'],flush=True); assert result['passed'],[c for c in checks if not c['pass_']]
