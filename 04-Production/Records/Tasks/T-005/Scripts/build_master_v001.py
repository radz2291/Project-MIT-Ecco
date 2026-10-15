"""B101 isolated build. Run with source .blend in background Blender; never saves source."""
import bpy, json, math, hashlib, time, shutil
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[4]
ASSET=ROOT/'Shared/Assets/ECCO'
TASK=ROOT/'Records/Tasks/T-005'
for p in [ASSET/'Originals', TASK/'Evidence', TASK/'Previews']:
    p.mkdir(parents=True,exist_ok=True)
def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def mesh_digest(o):
    import array
    a=array.array('f',[0.0])*(len(o.data.vertices)*3); o.data.vertices.foreach_get('co',a)
    b=array.array('i',[0])*(len(o.data.loops)); o.data.loops.foreach_get('vertex_index',b)
    return hashlib.sha256(a.tobytes()+b.tobytes()).hexdigest()
source=Path(bpy.data.filepath)
step=next((ROOT/'Shared/Assets').glob('*.stp'))
source_hash=digest(source);step_hash=digest(step)
for p in [source,step]:
    target=ASSET/'Originals'/p.name
    if target.exists(): assert digest(target)==digest(p), 'Refuse to overwrite differing original'
    else: shutil.copy2(p,target)
scene=bpy.context.scene
housing=next(o for o in scene.objects if o.type=='MESH')
assert len(scene.objects)==1
signature=mesh_digest(housing)
bounds=[housing.matrix_world@Vector(v) for v in housing.bound_box]
measured={'dimensions_m':list(housing.dimensions),'bounds_m':[[min(p[i] for p in bounds) for i in range(3)],[max(p[i] for p in bounds) for i in range(3)]], 'source_scale':list(housing.scale),'vertices':len(housing.data.vertices),'polygons':len(housing.data.polygons),'mesh_signature':signature}
# Connectivity is tessellation evidence only, never physical component identity.
parents=list(range(len(housing.data.vertices)))
def find(i):
    while parents[i]!=i:
        parents[i]=parents[parents[i]];i=parents[i]
    return i
for e in housing.data.edges:
    a,b=map(find,e.vertices)
    if a!=b: parents[b]=a
counts={}
for i in range(len(parents)):
    k=find(i);counts[k]=counts.get(k,0)+1
measured['connected_island_vertex_counts']=sorted(counts.values(),reverse=True)
master=bpy.data.collections.new('ECCO_MASTER_v001');scene.collection.children.link(master)
def coll(name):
    c=bpy.data.collections.new(name);master.children.link(c);return c
geometry=coll('ECCO_GEOMETRY_REPLACEABLE'); controls=coll('ECCO_CONTROLS');refs=coll('ECCO_SENSOR_REFERENCES');effects=coll('ECCO_EFFECTS_EMPTY'); cuts=coll('ECCO_CUTAWAY_TOOLS')
inspection=bpy.data.collections.new('B101_INSPECTION_ONLY');scene.collection.children.link(inspection)
for c in list(housing.users_collection): c.objects.unlink(housing)
geometry.objects.link(housing)
housing.name='ECCO_HOUSING_SOURCE_MESH'
housing['source_step']='//Originals/'+step.name
housing['provenance']='Preserved earlier import; not independently retessellated from STEP in T-005'
housing['status']='PROVISIONAL: O04/O14 unresolved; no added faces/plugs/closures'
def empty(name,c,parent=None,loc=(0,0,0)):
    o=bpy.data.objects.new(name,None);c.objects.link(o);o.empty_display_type='ARROWS';o.empty_display_size=.06;o.parent=parent;o.location=loc;return o
root=empty('ECCO_ROOT',controls);rot=empty('ECCO_ROTATION_X',controls,root)
root['interface']='Translate root; source longitudinal +X, X=0 mesh end, not verified pin shoulder'
rot['interface']='Rotate local X in radians; inherits axial travel from root. Physical operating direction requires end/viewpoint identification.'
housing.parent=rot
sensor_data=[]
centres=[(.730,.100251829,.081182330),(.730,-.120431874,.046229467),(.730,.020180046,-.127411796)]
for i,pos in enumerate(centres,1):
    o=empty('ECCO_SENSOR_REF_%02d'%i,refs,rot,pos)
    direction=Vector((0,pos[1],pos[2])).normalized()
    o.rotation_euler=direction.to_track_quat('Z','Y').to_euler()
    o['status']='PROVISIONAL recess rim centre from inherited report; not transducer/acoustic face'
    o['source']='Originals/Client_Confirmed_Sensor.png + IMPLEMENTATION_REPORT.md; 39/159/279 deg in source YZ plane'
    near=[v.co*.001 for v in housing.data.vertices if abs(v.co.x-730)<.05 and (Vector((v.co.y*.001,v.co.z*.001))-Vector(pos[1:])).length<.04]
    sensor_data.append({'name':o.name,'centre_m':list(pos),'outward_unit':list(direction),'angle_deg':math.degrees(math.atan2(pos[2],pos[1]))%360,'nearby_mesh_vertices_40mm':len(near),'nearby_axial_range_m':[min(v.x for v in near),max(v.x for v in near)] if near else None})
empty('ECCO_SENSOR_PLANE_PROVISIONAL',refs,rot,(.730,0,0))
mud=empty('ECCO_MUD_SENSOR_UNLOCATED',refs,rot)
mud.hide_viewport=True;mud.hide_render=True;mud['status']='Unlocated. Origin is placeholder only; MUST NOT emit effects or be treated as a sensor position.'
# Non-destructive cutaway tool; off by default. No invented internal assembly.
bpy.ops.mesh.primitive_cube_add(size=1,location=(1.2,0,.25))
cutter=bpy.context.object;cutter.name='ECCO_CUTTER_PREVIEW_ONLY';cutter.dimensions=(2.8,.8,.5)
for c in list(cutter.users_collection):c.objects.unlink(cutter)
cuts.objects.link(cutter);cutter.parent=rot;cutter.display_type='WIRE';cutter.hide_render=True;cutter.hide_set(True)
modifier=housing.modifiers.new('OPTIONAL_ILLUSTRATIVE_SECTION_DISABLED','BOOLEAN');modifier.operation='DIFFERENCE';modifier.object=cutter;modifier.show_viewport=False;modifier.show_render=False
modifier.solver='EXACT'
master['status']='Provisional source-consistent mesh wrapper; not MIT hardware acceptance'
master['version']='v001';master['axis']='source X longitudinal; metres; no normalization/rescaling'
master['geometry_signature']=signature
master['replacement']='Replace only ECCO_GEOMETRY_REPLACEABLE; reverify references/controls/cutaway/clearances/occlusion; no automatic sensor relocation'
# Inspection cameras are excluded from reusable collection.
scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1;scene.unit_settings.length_unit='METERS'
scene.render.engine='BLENDER_WORKBENCH';scene.render.resolution_x=1280;scene.render.resolution_y=720;scene.render.resolution_percentage=100
scene.render.fps=24;scene.frame_start=scene.frame_end=1
sh=scene.display.shading;sh.light='STUDIO';sh.color_type='SINGLE';sh.single_color=(.57,.60,.65);sh.show_cavity=True;sh.cavity_type='BOTH';sh.show_shadows=True;sh.background_type='VIEWPORT';sh.background_color=(.055,.065,.08)
scene.render.image_settings.file_format='PNG';scene.render.filepath='//../../../Records/Tasks/T-005/Previews/'
cameras=[]
views=[('overview',(1.2,-3.5,1.6),(1.2,0,0),2.85),('opposite',(1.2,3.5,-1.6),(1.2,0,0),2.85),('sensor-closeup',(.73,1.0,.82),(.73,0,0),.72),('end-X0',(-3,0,0),(0,0,0),.55)]
for name,loc,target,scale in views:
    d=bpy.data.cameras.new('INSPECT_'+name);o=bpy.data.objects.new('INSPECT_'+name,d);inspection.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();d.type='ORTHO';d.ortho_scale=scale;cameras.append((name,o))
scene.camera=cameras[0][1]
scene['B101']='Inspection only. No acoustic simulation; provisional hardware. Render views at frame 1.'
for area in bpy.context.screen.areas if bpy.context.screen else []:
    if area.type=='VIEW_3D':
        area.spaces.active.region_3d.view_distance=3
        area.spaces.active.region_3d.view_location=(1.2,0,0)
        area.spaces.active.region_3d.view_perspective='CAMERA'
bpy.ops.wm.save_as_mainfile(filepath=str(ASSET/'ECCO_master_v001.blend'))
render_records=[]
for name,camera in cameras:
    scene.camera=camera;scene.render.filepath=str(TASK/'Previews'/('ECCO_'+name+'_v001.png'));start=time.perf_counter();bpy.ops.render.render(write_still=True)
    render_records.append({'view':name,'path':str(Path(scene.render.filepath).relative_to(ROOT)),'elapsed_seconds':time.perf_counter()-start,'frame':1,'resolution':[1280,720],'engine':'BLENDER_WORKBENCH'})
evidence={'source':str(source),'source_sha256':source_hash,'step_sha256':step_hash,'master':str(ASSET/'ECCO_master_v001.blend'),'master_sha256':digest(ASSET/'ECCO_master_v001.blend'),'blender':bpy.app.version_string,'measured':measured,'sensor_references':sensor_data,'renders':render_records,'unchanged_originals':digest(source)==source_hash and digest(step)==step_hash,'mesh_unchanged':mesh_digest(housing)==signature,'limitations':['2.400m versus nominal 2.25m unresolved; do not rescale','Shoulder datum and 600mm sensor offset not established','Mud sensor/internal transducers unlocated','No manufacturing component split inferred from mesh islands','Pending plugged replacement O14','STEP not independently retessellated; earlier import lineage only']}
(TASK/'Evidence/build-evidence_v001.json').write_text(json.dumps(evidence,indent=2),encoding='utf-8')
print('B101_BUILD_COMPLETE',json.dumps({'vertices':measured['vertices'],'islands':len(counts),'mesh_unchanged':evidence['mesh_unchanged'],'renders':render_records}))
