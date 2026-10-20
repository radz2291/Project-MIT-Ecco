import bpy,bmesh,json,math,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.kdtree import KDTree
from mathutils.bvhtree import BVHTree
B=Path(__file__).resolve().parents[1];R=B.parents[2];BASE=B.parent/'Cinematic-Previs_v006/Scenes/S04_cinematic-previs_v006.blend';d=Vector((0,math.cos(math.radians(39)),math.sin(math.radians(39))));tan=Vector((0,-d.z,d.y));CUT=.00005
bpy.ops.wm.open_mainfile(filepath=str(BASE),use_scripts=False,load_ui=False)
original={}
for o in bpy.data.objects:
 if o.type=='MESH' and (o.name.startswith('Cement ') or 'Stationary organic fluid' in o.name or o.name=='CASED_STEEL_WEAR_CUTAWAY'):
  original[o.name]=[tuple(o.matrix_world@v.co) for v in o.data.vertices if tan.dot(o.matrix_world@v.co)<CUT-1e-6]
out={}
for case in 'BC':
 p=B/'Scenes'/f'S04_{case}_capped-resonance_v008.blend';bpy.ops.wm.open_mainfile(filepath=str(p),use_scripts=False,load_ui=False);s=bpy.context.scene;metadata=json.loads((B/'Records'/f'build-{case}.json').read_text());checks=[]
 for row in metadata['sections']:
  if row['object']=='Section 2 geological surroundings - outside cement':continue
  o=bpy.data.objects[row['object']];key='CASED_STEEL_WEAR_CUTAWAY' if row['object'].startswith('STEEL -') else o.name
  bm=bmesh.new();bm.from_mesh(o.data);assert all(e.is_manifold for e in bm.edges);bm.free()
  tree=KDTree(len(o.data.vertices))
  for i,v in enumerate(o.data.vertices):tree.insert(o.matrix_world@v.co,i)
  tree.balance();err=max(tree.find(Vector(co))[2] for co in original[key]);assert err<1e-6,(o.name,err)
  assert not o.animation_data and not o.modifiers
  checks.append({'object':o.name,'closed_manifold':True,'retained_original_max_error_m':err,'static':True})
 libs=[{'path':l.filepath,'exists':Path(bpy.path.abspath(l.filepath)).exists()} for l in bpy.data.libraries];assert all(x['path'].startswith('//') and x['exists'] for x in libs)
 steel=bpy.data.objects['CASED_STEEL_WEAR_CUTAWAY'];wall=BVHTree.FromPolygons([v.co.copy() for v in steel.data.vertices],[tuple(p.vertices) for p in steel.data.polygons]);event=metadata['event'];src=Vector(event['emitter_world_m']);direction=Vector(event['direction_world']);margin=1;capmargin=1;samples=0
 states=[]
 for f in range(1,121):
  s.frame_set(f);bpy.context.view_layer.update();states.append((tuple(s.camera.matrix_world),tuple(bpy.data.objects['WORLD_CONTROL'].items())))
  for o in s.objects:
   if (o.name.startswith('S02 sourced') or o.name.startswith('Casing response tail')) and not o.hide_render:
    for sp in o.data.splines:
     for cp in sp.points:
      q=o.matrix_world@cp.co.xyz;radial=Vector((0,q.y,q.z));r=radial.length;hit=wall.ray_cast(Vector((q.x,0,0)),radial.normalized(),1)[0];assert hit is not None
      m=math.hypot(hit.y,hit.z)-r;cm=(q-src).dot(direction);margin=min(margin,m);capmargin=min(capmargin,cm);samples+=1
 assert margin>-.00005 and capmargin>-.00005,(margin,capmargin)
 assert all(x==states[0] for x in states)
 assert not any('pixel' in o.name.lower() or 'information cell' in o.name.lower() for o in s.objects if not o.hide_render and not o.library)
 out[case]={'sections':checks,'relative_libraries':libs,'stationary_camera_tool_and_solids':True,'wavefront_samples':samples,'minimum_wavefront_to_native_wall_margin_m':margin,'minimum_wavefront_cap_plane_margin_m':capmargin,'native_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
a=json.loads((B/'Records/build-B.json').read_text());b=json.loads((B/'Records/build-C.json').read_text());delta=max(abs(x-y) for k in ['camera_relative_eye','camera_relative_target'] for x,y in zip(a[k],b[k]));assert delta<1e-6 and a['lens']==b['lens'];out['matched_camera_max_difference_m']=delta
out['source_hashes']={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [BASE,R/'04-Production/Shared/Assets/CasedHole/CasedHole_v002.blend',R/'05-Previs/Section-02_Measurement-History/v011/Continuation/Scenes/S01-S02_continuous_v011.blend']}
(B/'Records/verification.json').write_text(json.dumps(out,indent=2));print('VERIFIED B/C geometry, caps, stationary state, camera match, native wavefront clearance, relative links')
