"""Separate-interval provisional B102 builder. Background Blender only.

Source dimensions are in config_authorized_v003.json. Editable live controls use
drivers, no persistent Python handlers. Supplied ECCO remains a relative library.
"""
import bpy,math,json,hashlib,sys
from pathlib import Path
from mathutils import Vector
ASSET=Path(__file__).resolve().parents[1]
ROOT=ASSET.parents[2];TASK=ROOT/'Records/Tasks/T-006'
c=json.loads((ASSET/'config_authorized_v003.json').read_text())
assert c['producer_selection']=='authorized_provisional_illustration_2026-10-16'
source=(ASSET/c['product_library']).resolve()
assert hashlib.sha256(source.read_bytes()).hexdigest()==c['product_sha256']
output=ASSET/'WellAssembly_variants_v003.blend'
if output.exists():raise SystemExit('Refuse overwrite; version a manually changed candidate')
bpy.ops.wm.read_factory_settings(use_empty=True)
s=bpy.context.scene
with bpy.data.libraries.load(str(source),link=True) as (src,dst):dst.collections=[c['product_collection']]
product=dst.collections[0]
I=.0254;upper=c['intervals']['upper_cased'];lower=c['intervals']['lower_open'];p=c['illustrative_layout']
ri=upper['nominal_body_id_inches']*I/2;ro=upper['casing_od_inches']*I/2
host=upper['host_hole_diameter_inches']*I/2;hole=lower['hole_diameter_inches']*I/2
assert ri>12.3*I/2 and host>ro>ri>hole
master=bpy.data.collections.new('WELL_ASSEMBLY_v003');s.collection.children.link(master)
def coll(name,parent=master):
    q=bpy.data.collections.new(name);parent.children.link(q);return q
controls=coll('ASSEMBLY_CONTROLS');hardware=coll('LINKED_ECCO');proxies=coll('PROVISIONAL_BHA_PROXIES')
well=coll('WELL_INTERVALS');casing=coll('UPPER_CASED_INTERVAL',well)
variants=[coll('LOWER_'+name,well) for name in ('NOMINAL','IRREGULAR','SPIRAL')]
review=bpy.data.collections.new('B102_INSPECTION_ONLY');s.collection.children.link(review)
def empty(name,col,parent=None):
    o=bpy.data.objects.new(name,None);col.objects.link(o);o.parent=parent;o.empty_display_type='ARROWS';o.empty_display_size=.08;return o
rig=empty('ASSEMBLY_CONTROL',controls)
props={'travel_m':.5,'rotation_rad':0.,'variant':0,'cutaway':1,'show_open':1,'show_casing':1,
       'show_cement':1,'show_hardware':1,'show_proxies':1,'irregular_strength':1.,'spiral_strength':1.}
for k,v in props.items():rig[k]=v
for k in ('irregular_strength','spiral_strength'):rig.id_properties_ui(k).update(min=0.,max=1.)
rig.id_properties_ui('variant').update(min=0,max=2,description='0 nominal, 1 irregular, 2 spiral; upper cased interval remains separate')
for k in ('cutaway','show_open','show_casing','show_cement','show_hardware','show_proxies'):
    rig.id_properties_ui(k).update(min=0,max=1)
rig['status']='PROVISIONAL ILLUSTRATION authorized by Radzi; O05 remains open before technical lock'
rig['axes']='Source +X test travel. Pin/box source-end identification and actual BHA placement unconfirmed.'
def drive(o,path,expression,variables,index=None):
    fc=o.driver_add(path) if index is None else o.driver_add(path,index)
    d=fc.driver;d.type='SCRIPTED';d.expression=expression
    for name,prop in variables.items():
        v=d.variables.new();v.name=name;v.type='SINGLE_PROP';v.targets[0].id=rig;v.targets[0].data_path='["'+prop+'"]'
def visibility(o,expression,variables):
    for path in ('hide_render','hide_viewport'):drive(o,path,expression,variables)
travel=empty('ASSEMBLY_TRAVEL_X',controls);rotation=empty('ASSEMBLY_ROTATION_X',controls,travel)
drive(travel,'location','t',{'t':'travel_m'},0);drive(rotation,'rotation_euler','r',{'r':'rotation_rad'},0)
instance=empty('ECCO_LINK_v002',hardware,rotation);instance.instance_type='COLLECTION';instance.instance_collection=product
visibility(instance,'1-show',{'show':'show_hardware'})
def tube(name,col,x0,x1,rinner,router,cut=False,variant=None,kind='surface',strength=None):
    n=96;m=96
    # Cutaway opens toward the inspection camera (-Y); retained half has +Y.
    start,end=(-math.pi/2,math.pi/2) if cut else (0,2*math.pi)
    radii=[rinner] if kind=='surface' else [rinner,router]
    verts=[];faces=[]
    for r in radii:
        for i in range(n+1):
            x=x0+(x1-x0)*i/n
            for j in range(m+1):
                a=start+(end-start)*j/m;verts.append((x,r*math.cos(a),r*math.sin(a)))
    row=m+1;size=(n+1)*row
    for layer in range(len(radii)):
        for i in range(n):
            for j in range(m):
                z=layer*size+i*row+j;f=(z,z+1,z+row+1,z+row)
                faces.append(tuple(reversed(f)) if layer==0 and len(radii)>1 else f)
    if len(radii)==2:
        for i in (0,n):
            for j in range(m):
                z=i*row+j;faces.append((z,z+size,z+size+1,z+1))
        if cut:
            for j in (0,m):
                for i in range(n):
                    z=i*row+j;faces.append((z,z+row,z+row+size,z+size))
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update()
    obj=bpy.data.objects.new(name,mesh);col.objects.link(obj)
    # Weld only full-cylinder angular seams, never apply to linked product.
    if not cut:
        import bmesh
        bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7)
        bm.to_mesh(mesh);bm.free();mesh.update()
    if variant in (1,2):
        obj.shape_key_add(name='Basis');key=obj.shape_key_add(name='Illustrative_Profile')
        for point,v in zip(key.data,mesh.vertices):
            x,y,z=v.co;a=math.atan2(z,y)
            if variant==1:
                # Outward-only irregularity avoids arbitrary constriction of a gauge-sized bit.
                delta=p['washout_radial_m']*math.exp(-((x-2.8)/.95)**2)*(.55+.45*math.cos(3*a+.7*x))
            else:delta=p['spiral_radial_m']*(1+math.cos(a-2*math.pi*x/p['spiral_pitch_m']))/2
            point.co=(x,y+delta*math.cos(a),z+delta*math.sin(a))
        fc=key.driver_add('value');d=fc.driver;d.expression='strength'
        v=d.variables.new();v.name='strength';v.type='SINGLE_PROP';v.targets[0].id=rig;v.targets[0].data_path='["'+strength+'"]'
    obj['source']='config_authorized_v003.json; researched dimensional reference / labeled illustrative geometry'
    return obj
for cut in (False,True):
    suffix='_CUTAWAY' if cut else '_FULL'
    for name,rin,rout,color,show in [('CASING',ri,ro,(.42,.5,.58,1),'show_casing'),
                                    ('CEMENT',ro,host,(.43,.36,.25,1),'show_cement')]:
        o=tube(name+suffix,casing,p['upper_start_m'],0,rin,rout,cut,kind='shell');o.color=color
        visibility(o,'(1-show) or '+('(1-cut)' if cut else 'cut'),{'show':show,'cut':'cutaway'})
        o['interval']='upper cased host 17.5in; casing13.375in OD /12.515in nominal ID; separate lower open hole'
    for v,col in enumerate(variants):
        o=tube(('NOMINAL','IRREGULAR','SPIRAL')[v]+suffix,col,0,p['lower_end_m'],hole,None,cut,v,
               strength=('irregular_strength' if v==1 else 'spiral_strength'))
        o.color=(.29,.32,.36,1)
        visibility(o,'(1-show) or (v != '+str(v)+') or '+('(1-cut)' if cut else 'cut'),
                   {'show':'show_open','v':'variant','cut':'cutaway'})
        o['profile']='Illustrative outward enlargement only; nominal12.25in, no measured field log/spiral claim'
# Simplified collars and bit gauge, with conspicuous unresolved adapters.
collar=c['generic_collar_reference'];cr=collar['od_inches']*I/2;ci=collar['id_inches']*I/2
for name,x0,x1,r0,r1,color in [
    ('UPPER_COLLAR_PROXY',-1.5,-.12,ci,cr,(.48,.5,.52,1)),
    ('UPPER_ADAPTER_UNRESOLVED',-.12,0,ci,cr,(.9,.38,.12,1)),
    ('LOWER_ADAPTER_UNRESOLVED',2.4,2.52,ci,cr,(.9,.38,.12,1)),
    ('LOWER_COLLAR_PROXY',2.52,2.9,ci,cr,(.48,.5,.52,1)),
    ('BIT_GAUGE_PROXY_NOT_CUTTERS',2.9,3.08,ci,hole,(.9,.55,.16,1))]:
    o=tube(name,proxies,x0,x1,r0,r1,False,kind='shell');o.parent=rotation;o.color=color
    o['status']='PROVISIONAL layout/length and adapter/bit representation, not manufacturer geometry or actual MIT BHA placement'
    visibility(o,'1-show',{'show':'show_proxies'})
master['config_json']=json.dumps(c,sort_keys=True)
master['replacement']='Relink accepted ECCO only after remeasuring envelope/references and rerunning clearance/control/review checks. O14 pending.'
master['O05']='Open for MIT confirmation before technical lock; provisional construction authorized 16 October2026'
camera_data=bpy.data.cameras.new('INSPECTION_CAMERA');camera=bpy.data.objects.new(camera_data.name,camera_data)
review.objects.link(camera);camera.parent=travel;camera.location=(1.2,-4,2.2)
camera.rotation_euler=(Vector((1.2,0,0))-camera.location).to_track_quat('-Z','Y').to_euler()
camera_data.type='ORTHO';camera_data.ortho_scale=4.0;s.camera=camera
s.unit_settings.system='METRIC';s.unit_settings.scale_length=1
s.render.engine='BLENDER_WORKBENCH';s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100
s.render.fps=24;s.frame_start=1;s.frame_end=96
sh=s.display.shading;sh.light='STUDIO';sh.color_type='OBJECT';sh.show_cavity=True;sh.cavity_type='BOTH'
sh.show_shadows=True;sh.background_type='VIEWPORT';sh.background_color=(.045,.055,.07)
s.render.image_settings.file_format='PNG'
s['purpose']='B1 reusable well/assembly illustration and inspection. No S01-S07 shot construction or technical lock.'
s['config']='//config_authorized_v003.json'
for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(lib.filepath,start=str(ASSET))
bpy.context.view_layer.update()
bpy.ops.wm.save_as_mainfile(filepath=str(output))
(TASK/'Evidence/variants-build_v003.json').write_text(json.dumps({'file':str(output),'sha256':hashlib.sha256(output.read_bytes()).hexdigest(),
 'source_sha256':c['product_sha256'],'blender':bpy.app.version_string,'objects':len(s.objects),'config':c},indent=2),encoding='utf-8')
print('BUILD_V003_PASS')
