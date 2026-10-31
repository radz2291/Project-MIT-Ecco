"""World v011 regional geology successor; never edits v010 or Digital assets."""
import bpy,json,math,hashlib,array,sys
from pathlib import Path
from mathutils import Vector
R=next(p for p in Path(__file__).resolve().parents if (p/'04-Production').is_dir());B=R/'04-Production/Shared/Assets/Environment/Borehole';T=R/'04-Production/Records/Tasks/T-055/Revision_v006';src=B/'World_environment_v010.blend';dst=B/'World_environment_v011.blend'
assert not dst.exists() or '--replace-unpublished' in sys.argv or '--package-only' in sys.argv,'Preserve existing candidate; choose successor explicitly'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def snapshot():
 out={}
 for o in bpy.data.objects:
  if o.type!='MESH':continue
  m=o.data;coords=array.array('f',[0])*(len(m.vertices)*3);m.vertices.foreach_get('co',coords);loops=array.array('i',[0])*len(m.loops);m.loops.foreach_get('vertex_index',loops);polys=[(p.loop_start,p.loop_total,p.material_index) for p in m.polygons];keys={k.name:[tuple(v.co) for v in k.data] for k in m.shape_keys.key_blocks} if m.shape_keys else {}
  out[o.name]={'geometry_sha256':hashlib.sha256(coords.tobytes()+loops.tobytes()+json.dumps([polys,keys]).encode()).hexdigest(),'matrix':[list(r) for r in o.matrix_world],'vertices':len(m.vertices),'faces':len(m.polygons)}
 return out
def package_scene():
 connected=bpy.data.collections['WORLD_DESCENT_CONNECTED']
 for c in bpy.data.collections:c.use_fake_user=True
 for scene in bpy.data.scenes:
  for child in list(scene.collection.children):scene.collection.children.unlink(child)
  scene.collection.children.link(connected)
 text=bpy.data.texts.get('README — World v011') or bpy.data.texts.new('README — World v011')
 text.clear();text.write('WORLD v011 — connected regional descent\nDefault scene links WORLD_DESCENT_CONNECTED exactly once. It combines WORLD_REGIONAL_DESCENT and the exact preserved S02 destination cutaway.\nAll v010 variants remain selectable library collections with fake users. Link a selected variant or connected collection into a consumer; do not stack competing walls.\nCanonical (X,Y,Z)=(sourceZ+735,sourceX,sourceY), metres. Regional depth -120..-1020m, outer radius180m, seven illustrative units. Exact destination -750..-720m reserved.\nGeology is illustrative, not field data or engineering certification. No shot cameras/lights/actions included. Source v010 and accepted Digital assets remain unchanged.\nSee World_interface_v011.json for provenance, placement and ownership.')
if '--package-only' in sys.argv:
 source_hash=sha(src);bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False);old_names=set(c.name for c in bpy.data.collections);original=snapshot()
 bpy.ops.wm.open_mainfile(filepath=str(dst),load_ui=False);before_package=snapshot();members={c.name:sorted(o.name for o in c.objects) for c in bpy.data.collections};package_scene();bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(dst),compress=True)
 bpy.ops.wm.open_mainfile(filepath=str(dst),load_ui=False);after=snapshot();assert before_package==after;assert all(after[k]==v for k,v in original.items());assert old_names<=set(c.name for c in bpy.data.collections);assert all(sorted(o.name for o in bpy.data.collections[k].objects)==v for k,v in members.items());assert all([c.name for c in scene.collection.children]==['WORLD_DESCENT_CONNECTED'] for scene in bpy.data.scenes);assert sha(src)==source_hash
 interface=json.loads((B/'World_interface_v011.json').read_text());interface['native_sha256']=sha(dst);interface['default_scene_root']=['WORLD_DESCENT_CONNECTED'];interface['retained_collection_policy']='All predecessor variants retained as selectable fake-user library collections; collection hide flags unchanged.';(B/'World_interface_v011.json').write_text(json.dumps(interface,indent=2))
 evidence=json.loads((T/'world-evidence.json').read_text());evidence.update(native_sha256=sha(dst),default_scene_roots={scene.name:[c.name for c in scene.collection.children] for scene in bpy.data.scenes},all_previous_collection_names_retained=True,retained_previous_collection_names=sorted(old_names),packaging_all_geometry_unchanged=True,embedded_readme=True);(T/'world-evidence.json').write_text(json.dumps(evidence,indent=2));print('WORLD_V011_PACKAGED',sha(dst));sys.exit(0)
source_hash=sha(src);bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False);before=snapshot();old_collections={c.name:sorted(o.name for o in c.objects) for c in bpy.data.collections};source=bpy.data.objects['WORLD_S02_PHYSICAL_CUTAWAY_MESH'];verts=[v.co.copy() for v in source.data.vertices]
# Recover actual faceted outer edge and inner end profiles. No radial rescaling.
def angle(p):
 a=math.atan2(p.z,p.y)
 return a+2*math.pi if a<math.radians(-5.01) else a
outer={round(angle(p),8):Vector((p.y,p.z)) for p in verts if math.hypot(p.y,p.z)>19}
outer_points=[outer[a] for a in sorted(outer)]
angles=sorted(outer)
def ray_profile(points,t):
 d=Vector((math.cos(t),math.sin(t)))
 for a,b in zip(points,points[1:]):
  edge=b-a;den=d.x*edge.y-d.y*edge.x
  if abs(den)<1e-10:continue
  r=(a.x*edge.y-a.y*edge.x)/den;u=(a.x*d.y-a.y*d.x)/den
  if r>0 and -1e-6<=u<=1+1e-6:return d*r
 raise RuntimeError('No profile intersection '+str(t))
outer_ring=[outer[a].copy() for a in angles]
profiles={}
for x in [-15.,15.]:
 pts={round(angle(p),8):Vector((p.y,p.z)) for p in verts if abs(p.x-x)<1e-4 and math.hypot(p.y,p.z)<1.}
 assert len(pts)>40,(x,len(pts))
 profiles[x]=[ray_profile([pts[a] for a in sorted(pts)],t) for t in angles]
regional=bpy.data.collections.new('WORLD_REGIONAL_DESCENT');bpy.context.scene.collection.children.link(regional)
regional['provenance']='Illustrative seven broad unequal contiguous units; not a measured stratigraphic log.';regional['coordinate_system']='Canonical(X,Y,Z)=(sourceZ+735,sourceX,sourceY)';regional['source_depth_bounds_m']=[-1020.,-120.];regional['outer_radius_m']=180.;regional['destination_reserved_source_z_m']=[-750.,-720.]
colors=[(.19,.205,.21,1),(.235,.226,.205,1),(.175,.19,.20,1),(.245,.24,.22,1),(.19,.185,.175,1),(.22,.23,.235,1),(.16,.18,.19,1)]
def material(i):
 if i==4:return source.data.materials[0]  # Exact host material, unmodified.
 m=bpy.data.materials.new(f'REGIONAL unit {i+1:02} — subdued bedding');m.diffuse_color=colors[i];m.use_nodes=True;n=m.node_tree.nodes;l=m.node_tree.links;bs=n.get('Principled BSDF');bs.inputs['Roughness'].default_value=.91;pos=n.new('ShaderNodeTexCoord');sep=n.new('ShaderNodeSeparateXYZ');l.new(pos.outputs['Object'],sep.inputs[0]);scale=n.new('ShaderNodeMath');scale.operation='MULTIPLY';scale.inputs[1].default_value=1.7;l.new(sep.outputs['X'],scale.inputs[0]);sine=n.new('ShaderNodeMath');sine.operation='SINE';l.new(scale.outputs[0],sine.inputs[0]);ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=tuple(c*.95 for c in colors[i][:3])+(1,);ramp.color_ramp.elements[1].color=colors[i];l.new(sine.outputs[0],ramp.inputs[0]);l.new(ramp.outputs[0],bs.inputs['Base Color']);return m
boundaries=[-120.,-245.,-390.,-515.,-660.,-805.,-925.,-1020.];records=[]
def build_band(i,z_top,z_bottom,inner):
 cuts=sorted(set([z_bottom,z_top]+[z for z in [-750.,-720.] if z_bottom<z<z_top]));m=materials[i]
 for lo,hi in zip(cuts,cuts[1:]):
  if inner and lo>=-750 and hi<=-720:continue
  nz=max(1,math.ceil((hi-lo)/16));depths=[lo+(hi-lo)*j/nz for j in range(nz+1)];points=[];faces=[];na=len(angles)
  for z in depths:
   x=z+735
   for boundary in [0,1]:
    for j,t in enumerate(angles):
     if not inner:p=outer_ring[j] if boundary==0 else Vector((180*math.cos(t),180*math.sin(t)))
     elif boundary==1:p=outer_ring[j]
     elif abs(x+15)<1e-5 or abs(x-15)<1e-5:p=profiles[-15. if x<0 else 15.][j]
     else:r=.2+.007*math.sin(z*.021+t*2.);p=Vector((r*math.cos(t),r*math.sin(t)))
     points.append((x,p.x,p.y))
  def q(k,b,j):return k*2*na+b*na+j
  for k in range(nz):
   for j in range(na-1):
    # Only external bore/outer walls; omit internal r20 duplicate interfaces.
    b=0 if inner else 1;face=(q(k,b,j),q(k,b,j+1),q(k+1,b,j+1),q(k+1,b,j));faces.append(tuple(reversed(face)) if inner else face)
   for j in [0,na-1]:
    face=(q(k,0,j),q(k+1,0,j),q(k+1,1,j),q(k,1,j));faces.append(tuple(reversed(face)) if j==0 else face)
  # End caps only at domain exterior. Unit boundaries touch, never separated slabs.
  for k,z in [(0,lo),(nz,hi)]:
   if z in [-1020.,-120.]:
    for j in range(na-1):faces.append((q(k,0,j),q(k,1,j),q(k,1,j+1),q(k,0,j+1)))
  name=f'REGIONAL_UNIT_{i+1:02}_'+('INNER' if inner else 'OUTER')+f'_{int(-hi)}_{int(-lo)}';mesh=bpy.data.meshes.new(name);mesh.from_pydata(points,[],faces);mesh.materials.append(m);mesh.update();ob=bpy.data.objects.new(name,mesh);regional.objects.link(ob);ob['source_z_bounds_m']=[lo,hi];ob['ownership']='World illustrative regional geology only';ob['radial_zone']='bore to exact20m interface; destination omitted' if inner else 'exact20m interface to180m';records.append({'object':name,'source_z_bounds_m':[lo,hi],'inner':inner,'vertices':len(points),'faces':len(faces)})
materials=[material(i) for i in range(7)]
for i in range(7):build_band(i,boundaries[i],boundaries[i+1],False);build_band(i,boundaries[i],boundaries[i+1],True)
connected=bpy.data.collections.new('WORLD_DESCENT_CONNECTED');connected.children.link(regional);connected.children.link(bpy.data.collections['WORLD_S02_PHYSICAL_CUTAWAY']);bpy.context.scene.collection.children.link(connected);connected['policy']='Select this collection alone for regional descent and exact S02 inner destination. Do not add competing legacy walls.'
interface=json.loads((B/'World_interface_v010.json').read_text());interface.update(version='v011',native=dst.relative_to(R).as_posix(),predecessor_native=src.relative_to(R).as_posix(),predecessor_sha256=source_hash,regional={'collection':'WORLD_REGIONAL_DESCENT','connected_collection':'WORLD_DESCENT_CONNECTED','source_z_bounds_m':[-1020,-120],'canonical_x_bounds_m':[-285,615],'outer_radius_m':180,'source_cutaway_angular_bounds_deg':[math.degrees(angles[0]),math.degrees(angles[-1])],'source_cutaway_policy':'Same angular opening and full faceted profile as preserved S02 cutaway; viewed from negative sourceY','host_material':source.data.materials[0].name,'host_unit_source_z_bounds_m':[-805,-660],'bedding_coordinate_space':'TextureCoord Object local canonical X; exact destination/host material unmodified','units_source_z_boundaries_m':boundaries,'bore_radius_outside_destination_m':[.193,.207],'reserved_source_z_m':[-750,-720],'reserved_canonical_x_m':[-15,15],'destination_policy':'Exact preserved WORLD_S02_PHYSICAL_CUTAWAY supplies bore to20m; regional outer boundary uses every actual faceted20m edge vertex and identical angular opening(-5..225degrees). Original destination is unchanged.','internal_face_policy':'No duplicate regional r20 interface faces; no separate floating bedding slabs.','provenance':'Illustrative broad units, not field geology, engineering truth or calibrated logs.','ownership':'World owns geology/physical walls; section datasets and cameras remain local.'})
built_snapshot=snapshot();assert all(built_snapshot[k]==v for k,v in before.items());assert all(sorted(o.name for o in bpy.data.collections[k].objects)==v for k,v in old_collections.items());assert not any(o.type in ['CAMERA','LIGHT'] for o in bpy.data.objects);assert len(bpy.data.actions)==0
package_scene();bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(dst),compress=True);bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(dst),compress=True)
bpy.ops.wm.open_mainfile(filepath=str(dst),load_ui=False);after=snapshot();assert all(after[k]==v for k,v in before.items());assert sha(src)==source_hash;missing=[l.filepath for l in bpy.data.libraries if not Path(bpy.path.abspath(l.filepath)).exists()];assert not missing
interface['native_sha256']=sha(dst);(B/'World_interface_v011.json').write_text(json.dumps(interface,indent=2));evidence={'source_sha256':source_hash,'native_sha256':sha(dst),'preserved_v010_mesh_objects':len(before),'all_mesh_topology_shape_keys_transforms_exact':True,'all_original_collection_memberships_exact':True,'missing_libraries':missing,'cameras':0,'lights':0,'actions':0,'regional_units':7,'regional_angular_bounds_deg':[math.degrees(angles[0]),math.degrees(angles[-1])],'host_material_reused_exact':'Earth stratum 20','host_unit_source_z_bounds_m':[-805,-660],'regional_bedding_uses_local_object_coordinates':True,'regional_objects':records,'matching_outer_profile_vertices':len(outer_ring),'destination_inner_end_profile_vertices':{str(x):len(p) for x,p in profiles.items()},'original_geometry':before,'fresh_open_pass':True,'limits':'Exact native destination and regional angular bounds both -5..225degrees; same full outer profile. Interfaces touch with no overlapping regional r20 faces. No renders performed.'};(T/'world-evidence.json').write_text(json.dumps(evidence,indent=2));print('WORLD_V011_READY',sha(dst),len(records))
