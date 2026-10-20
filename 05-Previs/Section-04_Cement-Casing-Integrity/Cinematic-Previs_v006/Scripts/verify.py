import bpy,hashlib,struct,json
from pathlib import Path
B=Path(__file__).resolve().parents[1];R=B.parents[2]
old=R/'05-Previs/Section-04_Cement-Casing-Integrity/Cinematic-Previs_v005/Scenes/S04_cinematic-previs_v005.blend'
def geometry():
 out={}
 for o in bpy.context.scene.objects:
  if o.type!='MESH' or not (o.name.startswith('Steel -') or 'organic' in o.name or o.name.startswith('Cement ')):continue
  h=hashlib.sha256()
  for v in o.data.vertices:h.update(struct.pack('fff',*v.co))
  for f in o.data.polygons:h.update(str(tuple(f.vertices)).encode())
  out[o.name]=h.hexdigest()
 return out
def keys(o):
 return [(fc.data_path,fc.array_index,[(float(k.co.x),float(k.co.y)) for k in fc.keyframe_points]) for l in o.animation_data.action.layers for st in l.strips for bag in st.channelbags for fc in bag.fcurves]
bpy.ops.wm.open_mainfile(filepath=str(old),load_ui=False,use_scripts=False);before=geometry();cam=keys(bpy.context.scene.camera);travel=keys(bpy.data.objects['WORLD_CONTROL'])
bpy.ops.wm.open_mainfile(filepath=str(B/'Scenes/S04_cinematic-previs_v006.blend'),load_ui=False,use_scripts=False);s=bpy.context.scene
assert before==geometry();assert cam==keys(s.camera);assert travel==keys(bpy.data.objects['WORLD_CONTROL'])
assert s.render.engine=='BLENDER_WORKBENCH' and s.frame_end==432 and s.render.fps==24
libs=[dict(path=l.filepath,exists=Path(bpy.path.abspath(l.filepath)).is_file(),relative=l.filepath.startswith('//')) for l in bpy.data.libraries];assert all(v['exists'] and v['relative'] for v in libs)
source=json.loads((B/'Records/revision.json').read_text());assert hashlib.sha256(Path(source['source']).read_bytes()).hexdigest()==source['source_sha256']
count=sum(i.object.original.name=='ECCO_HOUSING_SOURCE_MESH' for i in bpy.context.evaluated_depsgraph_get().object_instances);assert count==1
(B/'Records/verification.json').write_text(json.dumps(dict(fresh_open=True,steel_cement_channel_vertex_topology_hashes_match_v005=True,geometry_hashes=before,camera_keys_unchanged=True,hardware_motion_keys_unchanged=True,source_section2_unchanged=True,one_ecco=True,libraries=libs,engine=s.render.engine,frames=432,fps=24),indent=2));print('VERIFICATION_PASS')

for o in s.objects:
 if o.type=='MESH' and not o.data.library:o['geometry_policy']='Local preview derivative; preserved steel/cement/channel vertex topology; materials carry cutaway alpha'
s.render.filepath=str(B/'Work/S04_');s.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(B/'Scenes/S04_cinematic-previs_v006.blend'))
