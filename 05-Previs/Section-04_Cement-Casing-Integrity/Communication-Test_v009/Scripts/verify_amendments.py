import bpy,bmesh,json,math,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
B=Path(__file__).resolve().parents[1];OLD=B.parent/'Communication-Test_v008';result={}
def mesh_hash(o):
 return hashlib.sha256(json.dumps({'vertices':[list(v.co) for v in o.data.vertices],'faces':[list(p.vertices) for p in o.data.polygons],'matrix':[list(r) for r in o.matrix_world]},sort_keys=True).encode()).hexdigest()
def samples():
 s=bpy.context.scene;rows=[]
 for f in range(1,121):
  s.frame_set(f);bpy.context.view_layer.update();wave=[]
  for o in s.objects:
   if o.name.startswith('S02 sourced') or o.name.startswith('Casing response tail'):
    wave.append((o.name,list(o.location),list(o.scale),o.hide_render,list(o.data.materials[0].diffuse_color)))
  rows.append({'waves':wave,'camera':[list(r) for r in s.camera.matrix_world],'lens':s.camera.data.lens,'world':list(bpy.data.objects['WORLD_CONTROL'].items())})
 return hashlib.sha256(json.dumps(rows,sort_keys=True).encode()).hexdigest()
for case in 'BC':
 before=OLD/'Scenes'/f'S04_{case}_capped-resonance_v008.blend';after=B/'Scenes'/f'S04_{case}_formation-acquisition_v009.blend'
 bpy.ops.wm.open_mainfile(filepath=str(before),load_ui=False,use_scripts=False)
 names=[o.name for o in bpy.context.scene.objects if o.type=='MESH' and (o.name.startswith('STEEL -') or o.name.startswith('Cement ') or 'Stationary organic fluid' in o.name or o.name=='Internal fluid visibility volume')]
 hashes={n:mesh_hash(bpy.data.objects[n]) for n in names};old_waves=samples();env=[]
 for f in range(1,121):
  bpy.context.scene.frame_set(f);env.append([bpy.data.objects['STEEL-ATTACHED resonance band '+str(k)].data.materials[0].diffuse_color[3] for k in range(24)])
 bpy.ops.wm.open_mainfile(filepath=str(after),load_ui=False,use_scripts=False);s=bpy.context.scene
 assert all(mesh_hash(bpy.data.objects[n])==h for n,h in hashes.items());assert old_waves==samples()
 record=json.loads((B/'Records'/f'build-{case}.json').read_text());error=max(abs(record['envelope'][k][f]-env[f][k]) for k in range(24) for f in range(120));assert error<1e-7
 earth=bpy.data.objects['FORMATION - closed source-guided continuation to frame edge'];bm=bmesh.new();bm.from_mesh(earth.data);assert all(e.is_manifold for e in bm.edges);bm.free();assert not earth.animation_data
 min_r=min(math.hypot(v.co.y,v.co.z) for v in earth.data.vertices);assert min_r>=.22225-1e-6
 tree=BVHTree.FromPolygons([earth.matrix_world@v.co for v in earth.data.vertices],[tuple(p.vertices) for p in earth.data.polygons]);cam=s.camera;coverage=[]
 for u,v in [(0.005,.03),(.005,.5),(.005,.97),(.10,.5)]:
  w=.01*cam.data.sensor_width/cam.data.lens;h=w*s.render.resolution_y/s.render.resolution_x;target=cam.matrix_world@Vector(((u-.5)*w,(v-.5)*h,-.01));hit=tree.ray_cast(cam.location,(target-cam.location).normalized(),5)[0];assert hit is not None,(case,u,v);coverage.append({'uv':[u,v],'hit':list(hit)})
 libs=[{'path':l.filepath,'exists':Path(bpy.path.abspath(l.filepath)).exists()} for l in bpy.data.libraries];assert all(l['path'].startswith('//') and l['exists'] for l in libs)
 fragments=[o for o in s.objects if o.name.startswith('STEEL-BOUND acquisition segment')];assert len(fragments)==96 and all(not o.modifiers for o in fragments)
 carrier_error=0;mask_margin=1
 for f in range(1,121):
  s.frame_set(f)
  for k in range(24):carrier_error=max(carrier_error,abs(bpy.data.objects['STEEL-ATTACHED resonance band '+str(k)].data.materials[0].diffuse_color[3]-env[f-1][k]*.10))
  for o in fragments:
   k=int(o.name.split('(')[1].split(',')[0]);alpha=o.data.materials[0].diffuse_color[3];mask_margin=min(mask_margin,env[f-1][k]*.95-alpha)
 assert carrier_error<1e-6 and mask_margin> -1e-6
 for o in fragments:
  if o.animation_data:
   for layer in o.animation_data.action.layers:
    for st in layer.strips:
     for bag in st.channelbags:
      assert all(fc.data_path in ['hide_render','hide_viewport'] for fc in bag.fcurves)
 result[case]={'core_geometry_hashes_unchanged':hashes,'send_return_tail_camera_tool_120_frame_hash_unchanged':old_waves,'source_envelope_max_error':error,'actual_carrier_max_error':carrier_error,'mask_within_original_envelope':mask_margin>=-1e-6,'rock_closed_manifold':True,'rock_min_radius_m':min_r,'left_margin_formation_coverage':coverage,'fixed_information_fragments':len(fragments),'relative_libraries':libs,'native_sha256':hashlib.sha256(after.read_bytes()).hexdigest()}
result['status']='Both amendments verified separately from human comprehension/creative approval. D remains paused. No full integration.'
(B/'Records/verification.json').write_text(json.dumps(result,indent=2));print('VERIFIED B/C unchanged physical geometry and wave/camera animation; envelope, rock volume/coverage and fixed acquisition finish')
