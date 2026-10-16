"""Isolated background build: three cheap composition studies, no shared edits."""
import bpy, math, json, hashlib, time
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[4]
BASE=ROOT/'04-Production/Mechanisms/B202'
EVID=ROOT/'04-Production/Records/Tasks/T-008/Evidence'
T6=ROOT/'04-Production/Shared/Assets/WellAssembly/WellAssembly_variants_v003.blend'
T5=ROOT/'04-Production/Shared/Assets/ECCO/ECCO_master_temporary-plugs_v002.blend'
assert not (BASE/'Scenes/B202_study_A_v003.blend').exists(), 'Version before overwrite'
sources={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (T5,T6)}
bpy.ops.wm.open_mainfile(filepath=str(T6))
rig=bpy.data.objects['ASSEMBLY_CONTROL'];rig['variant']=1;rig['cutaway']=0;rig.update_tag();bpy.context.view_layer.update()
ev=bpy.data.objects['IRREGULAR_FULL'].evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh()
verts=[tuple(v.co) for v in me.vertices];faces=[tuple(p.vertices) for p in me.polygons];ev.to_mesh_clear()
product=bpy.data.collections['ECCO_MASTER_v002']
s=bpy.context.scene
for col in list(s.collection.children):s.collection.children.unlink(col)
col=bpy.data.collections.new('B202_STUDY_v003');s.collection.children.link(col)
def material(name,color,metal=0.,rough=.5,emission=0.,alpha=1.):
    m=bpy.data.materials.new(name);m.diffuse_color=(*color,alpha);m.use_nodes=True
    n=m.node_tree.nodes.get('Principled BSDF');n.inputs['Base Color'].default_value=(*color,1);n.inputs['Metallic'].default_value=metal;n.inputs['Roughness'].default_value=rough
    n.inputs['Emission Color'].default_value=(*color,1);n.inputs['Emission Strength'].default_value=emission
    if alpha<1:
        tree=m.node_tree;out=tree.nodes.get('Material Output');mix=tree.nodes.new('ShaderNodeMixShader');trans=tree.nodes.new('ShaderNodeBsdfTransparent');mix.inputs[0].default_value=alpha
        tree.links.new(trans.outputs[0],mix.inputs[1]);tree.links.new(n.outputs[0],mix.inputs[2]);tree.links.new(mix.outputs[0],out.inputs['Surface'])
        m.surface_render_method='DITHERED'
    return m
rock=material('Physical rock / neutral illustration',(.105,.085,.065),rough=.92)
cyan=material('Mapped circumference / illustrative',(.015,.65,.85),rough=.35,emission=.9)
blue=material('Derived geometry / not amplitude',(.012,.16,.38),rough=.65,emission=.1,alpha=.20)
white=material('White nominal bit-size reference',(.9,.94,1),rough=.4,emission=.6)
hardware=bpy.data.objects.new('B202_ECCO_LINK_v002',None);col.objects.link(hardware);hardware.instance_type='COLLECTION';hardware.instance_collection=product;hardware.location=(2,0,0)
hardware['source']='Accepted T5 v002 unchanged; travel placement 2m is illustrative'
def mesh(name,v,f,mat):
    data=bpy.data.meshes.new(name);data.from_pydata(v,[],f);data.update();o=bpy.data.objects.new(name,data);col.objects.link(o);data.materials.append(mat)
    for p in data.polygons:p.use_smooth=True
    return o
def cropped(name,back,mat):
    ids={i for i,v in enumerate(verts) if 1.85<=v[0]<=4.45 and (not back or v[1]>=-.00001)}
    fs=[f for f in faces if all(i in ids for i in f)];used=sorted({i for f in fs for i in f});mapping={j:i for i,j in enumerate(used)}
    return mesh(name,[verts[i] for i in used],[tuple(mapping[i] for i in f) for f in fs],mat)
physical=cropped('Physical T6 wall / rear half cutaway',True,rock)
envelope=cropped('Reconstructed envelope / exact T6 evaluated wall',False,blue)
envelope['meaning']='Conceptual radius geometry, exact T6 authored profile; not acquired measurements'
rows={}
for v in verts:rows.setdefault(round(v[0],5),[]).append(v)
def row(x):return sorted(rows[min(rows,key=lambda z:abs(z-x))],key=lambda v:math.atan2(v[2],v[1]))
def curve(name,points,mat,r=.00065,closed=True):
    d=bpy.data.curves.new(name,'CURVE');d.dimensions='3D';d.bevel_depth=r;d.bevel_resolution=2
    sp=d.splines.new('POLY');sp.points.add(len(points)-1)
    for p,v in zip(sp.points,points):p.co=(*v,1)
    sp.use_cyclic_u=closed;o=bpy.data.objects.new(name,d);col.objects.link(o);d.materials.append(mat);return o
sections=[]
for i,x in enumerate([2.0,2.25,2.5,2.73,3.0,3.25,3.5,3.75,4.0,4.25]):
    pts=row(x);o=curve('Wall-registered section %02d'%i,pts,cyan);o['source']='Exact evaluated T6 irregular wall vertices';sections.append(o)
hero=sections[3];plane=row(2.73)[0][0]
# Sensor plane and nearest T6 mesh row differ by 20mm; interpolate the source
# neighboring axial rows to place the hero contour exactly at 2+.730m.
lower=max(x for x in rows if x<=2.73);upper=min(x for x in rows if x>=2.73)
lo=row(lower);hi=row(upper);t=(2.73-lower)/(upper-lower)
points=[tuple((1-t)*a+t*b for a,b in zip(v,w)) for v,w in zip(lo,hi)]
for p,v in zip(hero.data.splines[0].points,points):p.co=(*v,1)
hero['source']='Linear interpolation between adjacent T6 evaluated axial rows at actual sensor plane X=2.730m'
nominal=curve('Nominal bit-size / 12.25in reference',[(2.73,.155575*math.cos(a*math.tau/128),.155575*math.sin(a*math.tau/128)) for a in range(128)],white,.00085)
points_obj=[]
for i,v in enumerate(points[::8]):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=8,ring_count=4,radius=.0017,location=v)
    o=bpy.context.object;o.name='Illustrative wall sample %02d'%i
    for c in list(o.users_collection):c.objects.unlink(o)
    col.objects.link(o);o.data.materials.append(cyan);points_obj.append(o)
def light(name,loc,power,size,color):
    d=bpy.data.lights.new(name,'AREA');d.energy=power;d.shape='DISK';d.size=size;d.color=color;o=bpy.data.objects.new(name,d);col.objects.link(o);o.location=loc;o.rotation_euler=(Vector((2.9,0,0))-o.location).to_track_quat('-Z','Y').to_euler()
light('Broad neutral key',(2.2,-2.0,2),650,3,(.8,.9,1));light('Soft warm edge',(4.1,1.2,.6),450,2,(1,.8,.6));light('Face fill',(1,-.5,.5),100,1,(.8,.9,1))
d=bpy.data.cameras.new('B202 study camera');cam=bpy.data.objects.new(d.name,d);col.objects.link(cam);s.camera=cam;d.type='PERSP';d.lens=55;d.clip_start=.005;d.clip_end=100
# Eevee keeps this study cheap; no final-finishing materials or volumes.
s.render.engine='BLENDER_EEVEE'
s.render.resolution_x=960;s.render.resolution_y=540;s.render.resolution_percentage=100;s.render.fps=24;s.frame_start=s.frame_end=1
s.render.image_settings.file_format='PNG';s.world=bpy.data.worlds.new('B202 dark neutral space');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.025,.032,.045,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.3
s.view_settings.view_transform='AgX';s.unit_settings.system='METRIC';s.unit_settings.scale_length=1
s['B202_source_hashes']=json.dumps(sources);s['B202_status']='D1 composition proposal, not approved; no animation';s['B202_sensor_plane']=2.73
record={'source_hashes':sources,'hero_interpolation':{'lower':lower,'upper':upper,'target':2.73},'candidates':[]}
for key,loc,target in [('A',(1.97,-.69,.46),(2.73,0,0)),('B',(1.0,-2.5,1.45),(3.05,0,0)),('C',(2.35,-.8,.6),(2.73,0,0))]:
    cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();d.lens=55 if key!='B' else 60
    physical.hide_render=(key=='C');envelope.hide_render=(key!='B');nominal.hide_render=(key!='C')
    for o in sections:o.hide_render=(key!='B' and o!=hero)
    for o in points_obj:o.hide_render=(key!='A')
    for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(BASE/'Scenes'))
    s['B202_key_state']=key;s['B202_camera_target']=list(target)
    output=BASE/f'Scenes/B202_study_{key}_v003.blend';s.render.filepath=str(BASE/f'Previews/Study_v003/B202_{key}_v003.png')
    bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(output),relative_remap=False)
    start=time.time();bpy.ops.render.render(write_still=True)
    record['candidates'].append({'key':key,'scene':str(output.relative_to(ROOT)),'image':str(Path(s.render.filepath).relative_to(ROOT)),'camera':list(loc),'target':list(target),'lens_mm':d.lens,'render_seconds':time.time()-start})
    (EVID/'build_v003.json').write_text(json.dumps(record,indent=2))
print('B202_STUDY_BUILD_PASS')
