"""T9 standalone mechanism proofs. Run in isolated background Blender.
No live scene changes. Authored examples, not acoustic simulation or field data.
"""
import bpy, math, json, time, hashlib
from pathlib import Path
from mathutils import Vector
BASE=Path(__file__).resolve().parents[1]
PROD=BASE.parents[1]
EVID=PROD/'Records/Tasks/T-009/Evidence'
SOURCE=PROD/'Shared/Assets/WellAssembly/WellAssembly_variants_v003.blend'
PRODUCT=PROD/'Shared/Assets/ECCO/ECCO_master_temporary-plugs_v002.blend'
RI=12.515*.0254/2; RO=13.375*.0254/2; HOST=17.5*.0254/2
CASES=[('retrieval',144),('support',144),('channel',144),('wear',144)]
rows=[]
def tube(name,x0,x1,ri,ro,z=0,color=(.45,.5,.56,1),channel=False,wear=False):
    verts=[];faces=[];ni=60;na=72
    for layer,r in enumerate((ri,ro)):
        for i in range(ni+1):
            x=x0+(x1-x0)*i/ni
            for j in range(na+1):
                a=-math.pi/2+math.pi*j/na
                d=.004*math.exp(-(a/.28)**2)*math.sin(math.pi*i/ni)**2 if wear and layer==0 else 0
                verts.append((x,(r+d)*math.cos(a),z+(r+d)*math.sin(a)))
    size=(ni+1)*(na+1)
    for layer in range(2):
        for i in range(ni):
            for j in range(na):
                q=layer*size+i*(na+1)+j;faces.append((q,q+1,q+na+2,q+na+1))
    for i in (0,ni):
        for j in range(na):
            q=i*(na+1)+j;faces.append((q,q+size,q+size+1,q+1))
    for j in (0,na):
        for i in range(ni):
            q=i*(na+1)+j;faces.append((q,q+na+1,q+na+1+size,q+size))
    me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update()
    o=bpy.data.objects.new(name,me);bpy.context.scene.collection.objects.link(o);o.color=color
    if channel:
        for k,c in enumerate((color,(.10,.42,.82,1))):
            mat=bpy.data.materials.new(name+str(k));mat.diffuse_color=c;o.data.materials.append(mat)
        for p in me.polygons:
            points=[me.vertices[v].co for v in p.vertices];xc=sum(v.x for v in points)/len(points)
            yc=sum(v.y for v in points)/len(points);zc=sum(v.z-z for v in points)/len(points)
            a=math.atan2(zc,yc)
            p.material_index=int(-1.2<=xc<=1.2 and .25<=a<=.85)
    if channel:
        selected=[tuple(p.vertices) for p in me.polygons if p.material_index==1]
        remaining=[tuple(p.vertices) for p in me.polygons if p.material_index==0]
        blue=bpy.data.meshes.new(name+'_water');blue.from_pydata(verts,[],selected);blue.update()
        bo=bpy.data.objects.new(name+'_water',blue);bpy.context.scene.collection.objects.link(bo);bo.color=(.10,.42,.82,1)
        me.clear_geometry();me.from_pydata(verts,[],remaining);me.update()
        o.location.z=.35;bo.location.z=.35
        o['display']='Exploded outside layer +0.35m for visibility only; vertex coordinates remain physical local section'
    elif name.startswith('Outside_'):o.location.z=.35
    return o
def line(name,points,color,r=.008):
    cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=r;cu.bevel_resolution=2
    sp=cu.splines.new('POLY');sp.points.add(len(points)-1)
    for p,co in zip(sp.points,points):p.co=(*co,1)
    o=bpy.data.objects.new(name,cu);bpy.context.scene.collection.objects.link(o);o.color=color;return o
def setup():
    s=bpy.context.scene;s.render.engine='BLENDER_WORKBENCH';s.render.resolution_x=1280;s.render.resolution_y=400;s.render.resolution_percentage=100
    s.render.fps=24;s.frame_start=1;s.frame_end=144;s.render.image_settings.file_format='PNG'
    s.unit_settings.system='METRIC'
    sh=s.display.shading;sh.light='STUDIO';sh.color_type='OBJECT';sh.show_shadows=True;sh.show_cavity=True;sh.cavity_type='BOTH';sh.background_type='VIEWPORT';sh.background_color=(.035,.045,.065)
    cam=bpy.data.objects.new('PROOF_CAMERA',bpy.data.cameras.new('PROOF_CAMERA'));s.collection.objects.link(cam);s.camera=cam
    cam.location=(0,-8,4);cam.rotation_euler=(Vector((0,0,0))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5
    return s,cam
for case,count in CASES:
    out=BASE/f'Scenes/B203_{case}_v002.blend'
    if out.exists():
        if case=='retrieval' and not (EVID/'build-render_v002.json').exists():
            out.rename(out.with_name('B203_retrieval_v002_failed-check.blend'))
        else:raise RuntimeError('Version before rebuilding an existing candidate')
    bpy.ops.wm.read_factory_settings(use_empty=True)
    if case=='retrieval':
        with bpy.data.libraries.load(str(SOURCE),link=False) as (src,dst):dst.collections=['WELL_ASSEMBLY_v003']
        bpy.context.scene.collection.children.link(dst.collections[0])
    s,cam=setup()
    if case=='retrieval':
        rig=bpy.data.objects['ASSEMBLY_CONTROL'];rig['cutaway']=1;rig['variant']=0
        for f,t in [(1,.6),(120,-4.5),(144,-4.5)]:
            rig['travel_m']=t;rig['rotation_rad']=0;rig.keyframe_insert(data_path='["travel_m"]',frame=f)
        cam.location=(.1,-12,7);cam.rotation_euler=(Vector((.1,0,0))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=12.4
        rig.update_tag()
    elif case=='support':
        for z,kind in [(.5,'supported'),(-.5,'channel')]:
            tube('Steel_'+kind,-1.9,1.9,RI,RO,z)
            tube('Outside_'+kind,-1.9,1.9,RO,HOST,z,(.58,.38,.12,1),channel=(kind=='channel'))
            # This schematic emitter is deliberately separate from unverified CAD faces.
            pulse=line('Pulse_echo_'+kind,[(0,0,z),(0,RI,z)],(.3,.9,.95,1),.006)
            for f,scale in [(1,.01),(30,1),(60,.01),(90,1),(120,.01),(144,.01)]:
                pulse.scale.y=scale;pulse.keyframe_insert(data_path='scale',frame=f)
        cam.data.ortho_scale=5.8
        cam.location.z+=.175
    elif case=='channel':
        tube('Steel',-1.6,1.6,RI,RO)
        tube('Authored_axial_channel',-1.6,1.6,RO,HOST,color=(.58,.38,.12,1),channel=True)
        # Scan marker refers to the schematic axial coordinate used in the map.
        marker=line('Scan_plane',[(0,0,-.32),(0,0,.32)],(.3,.9,.95,1),.012)
        for f,x in [(1,-1.6),(144,1.6)]:marker.location.x=x;marker.keyframe_insert(data_path='location',frame=f)
        cam.data.ortho_scale=4.0
    else:
        tube('Unchanged_outer_casing',-1.6,1.6,RI,RO,wear=True)
        # Nominal ID reference and longer center-to-inner-wall path at worn center.
        line('Nominal_inner_reference',[(-1.6,RI,0),(1.6,RI,0)],(.95,.95,.95,1),.0015)
        ray=line('Inner_wall_distance',[(0,0,0),(0,RI+.004,0)],(.3,.9,.95,1),.003)
        for f,scale in [(1,.01),(60,1),(144,1)]:ray.scale.y=scale;ray.keyframe_insert(data_path='scale',frame=f)
        cam.location=(0,-3,1.7);cam.rotation_euler=(Vector((0,0,0))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=3.8
    for obj in s.objects:
        if obj.animation_data and obj.animation_data.action:
            for layer in obj.animation_data.action.layers:
                for strip in layer.strips:
                    for bag in strip.channelbags:
                        for fc in bag.fcurves:
                            for k in fc.keyframe_points:k.interpolation='LINEAR'
    frames=BASE/f'Previews/v002/{case}/Frames';frames.mkdir(parents=True,exist_ok=True)
    s.render.filepath=str(frames/'frame_');s['proof_kind']='B203 standalone conceptual mechanism proof; not an S04 film shot'
    s['limitations']='Authored timing/signals/channel/wear. O04/O05/O06 technical review. No field log or acoustic simulation.'
    for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(out.parent))
    bpy.ops.wm.save_as_mainfile(filepath=str(out),relative_remap=False)
    bpy.ops.wm.open_mainfile(filepath=str(out));s=bpy.context.scene
    assert all(Path(bpy.path.abspath(l.filepath)).exists() for l in bpy.data.libraries)
    s.frame_set(1);bpy.context.view_layer.update()
    checks={'relative_libraries_resolve':True,'objects':len(s.objects)}
    if case=='retrieval':
        rig=bpy.data.objects['ASSEMBLY_CONTROL'];values=[]
        for f in (1,120,144):
            s.frame_set(f);rig.update_tag();bpy.context.view_layer.update();values.append(float(rig['travel_m']))
        assert all(abs(a-b)<1e-6 for a,b in zip(values,[.6,-4.5,-4.5]))
        checks.update(travel_m=values,nominal_radial_clearance_m=RI-.3048/2,final_bit_x=[-4.5+2.9,-4.5+3.08])
        assert checks['nominal_radial_clearance_m']>0 and checks['final_bit_x'][1]<0
    if case=='wear':
        me=bpy.data.objects['Unchanged_outer_casing'].data
        radii=[math.hypot(v.co.y,v.co.z) for v in me.vertices]
        assert max(radii)<RO+1e-6 and RI+.004<RO
        checks.update(outer_radius_m=RO,authored_max_inner_radius_m=RI+.004,authored_wear_m=.004)
    s.frame_set(1);start=time.perf_counter();bpy.ops.render.render(animation=True)
    rows.append({'case':case,'frames':144,'fps':24,'render_size':[1280,400],'render_seconds':time.perf_counter()-start,'scene':str(out.relative_to(PROD.parent)).replace('\\','/'),'scene_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'checks':checks})
    (EVID/'build-render_v002.json').write_text(json.dumps(rows,indent=2))
print('B203_BUILD_RENDER_PASS')
