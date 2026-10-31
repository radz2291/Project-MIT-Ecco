"""Surface v006 plus bounded linked S01-S02 environment demonstration.
Run in installed Blender background. Original scenes and active v005 remain untouched.
"""
import bpy, math, json, hashlib, sys
from pathlib import Path
from mathutils import Vector, Matrix
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco')
T=R/'04-Production/Records/Tasks/T-055/Revision_v006'
A=R/'04-Production/Shared/Assets'
D=R/'04-Production/Shared/Demos'
T.mkdir(parents=True,exist_ok=True)

def save(p):
    bpy.context.preferences.filepaths.save_version=0
    for l in bpy.data.libraries:l.filepath=bpy.path.abspath(l.filepath)
    bpy.ops.wm.save_as_mainfile(filepath=str(p),compress=True,relative_remap=False)
    bpy.ops.file.make_paths_relative()
    bpy.ops.wm.save_as_mainfile(filepath=str(p),compress=True,relative_remap=False)

def material(name,color,roughness=.5,metallic=0):
    m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
    bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*color,1)
    bs.inputs['Roughness'].default_value=roughness;bs.inputs['Metallic'].default_value=metallic
    return m

def ocean(name,cutaway=False):
    col=bpy.data.collections.new(name);bpy.context.scene.collection.children.link(col)
    n=100;extent=1500;vs=[];fs=[]
    for j in range(n+1):
        y=(j/n*(extent if cutaway else 2*extent))-(0 if cutaway else extent)
        for i in range(n+1):
            x=-extent+2*extent*i/n
            z=.18*math.sin(.065*x+.031*y)+.09*math.sin(.11*y-.025*x)
            vs.append((x,y,z))
    for j in range(n):
        for i in range(n):
            k=j*(n+1)+i;fs.append((k,k+1,k+n+2,k+n+1))
    me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update()
    o=bpy.data.objects.new(name,me);col.objects.link(o)
    o.data.materials.append(material(name+' blue sea',(.025,.16,.22),.22,.25))
    for p in me.polygons:p.use_smooth=True
    o['mean_waterline_z_m']=0.;o['illustrative_wave_height_m']=.54
    return col

def instance(path,col,name,matrix=None,scene=None):
    with bpy.data.libraries.load(str(path),link=True) as (a,b):b.collections=[col]
    o=bpy.data.objects.new(name,None);(scene or bpy.context.scene).collection.objects.link(o)
    o.instance_type='COLLECTION';o.instance_collection=b.collections[0]
    if matrix is not None:o.matrix_world=Matrix(matrix)
    return o

def setup(s):
    s.render.engine='BLENDER_WORKBENCH';s.render.resolution_x=800;s.render.resolution_y=450
    s.render.resolution_percentage=100;s.render.fps=24;s.display.render_aa='8'
    sh=s.display.shading;sh.light='STUDIO';sh.color_type='MATERIAL';sh.show_shadows=True
    sh.show_cavity=True;sh.background_type='WORLD';s.world.color=(.035,.045,.055)
    s.render.image_settings.file_format='PNG'

def camera(s,name,pos,target,lens=40,ortho=None):
    d=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,d);s.collection.objects.link(o)
    o.location=pos;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
    d.lens=lens;d.clip_start=.01;d.clip_end=10000
    if ortho:d.type='ORTHO';d.ortho_scale=ortho
    s.camera=o;return o

def surface():
    previous=A/'Environment/Surface/Surface_descent_v005.blend'
    if not previous.exists():previous=R/'04-Production/Shared/Archive/2026-10-31/Assets/Surface/Surface_descent_v005.blend'
    bpy.ops.wm.open_mainfile(filepath=str(previous),load_ui=False)
    for o in list(bpy.data.objects):
        if any(c.name=='SURFACE_DESCENT_EARTH_SOURCE' for c in o.users_collection):bpy.data.objects.remove(o,do_unlink=True)
    ec=bpy.data.collections.get('SURFACE_DESCENT_EARTH_SOURCE')
    if ec:bpy.data.collections.remove(ec)
    for me in list(bpy.data.meshes):
        if not me.users:bpy.data.meshes.remove(me)
    ocean('SURFACE_OCEAN_FULL');cut=ocean('SURFACE_OCEAN_CUTAWAY',True)
    cut.use_fake_user=True
    # Reusable alternatives are stored, not stacked in the library's default scene.
    bpy.context.scene.collection.children.unlink(bpy.data.collections['SURFACE_OCEAN_CUTAWAY'])
    info=bpy.data.objects['SURFACE_DEScent_INFO']
    info['ownership']='Surface: equipment and sea only. World owns all geology and destination wall.'
    info['world_destination']='World_environment_v011 / WORLD_DESCENT_CONNECTED'
    txt=bpy.data.texts.new('README Surface v006')
    txt.write('Link SURFACE_RIG_SUBSEA_v004 plus exactly one ocean: SURFACE_OCEAN_FULL or SURFACE_OCEAN_CUTAWAY. Mean waterline Z=0; seabed -120m. Pontoons -20..-14m. Geology is exclusively World v011. Camera-access cuts remain illustrative; no engineering certification. No cameras, lights or section animation. Full sea is for the moving descent; half-sea is an explanatory cutaway alternative.\n')
    save(A/'Environment/Surface/Surface_descent_v006.blend')

def demo():
    src=R/'05-Previs/Section-02_Measurement-History/v011/Continuation/Scenes/S01-S02_continuous_v011.blend'
    bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False)
    # Repair only the new demonstration's link to the current accepted hardware.
    for l in list(bpy.data.libraries):
        if Path(l.filepath).name=='ECCO_film_v002.blend':
            l.filepath=str(A/'Hardware/ECCO/ECCO_film_v003.blend');l.reload()
    s=bpy.context.scene;s.name='Descent — connected S01-S02';setup(s)
    before={}
    for f in range(1,529):
        s.frame_set(f);before[str(f)]={'matrix':[list(row) for row in s.camera.matrix_world], 'lens':s.camera.data.lens}
    prefixes=('Cutaway earth','Formation rear','Earth seam','Opening front','Deck side','Deck end','Platform leg','Rig machinery','Roof trim','Service building','Upper building')
    removed=[]
    for o in list(s.objects):
        if not o.library and (o.name.startswith(prefixes) or o.name in ['Ocean horizon','Seabed around drilled opening','S02 geological wall retained section','Main solid building']):
            removed.append(o.name);bpy.data.objects.remove(o,do_unlink=True)
    surfacepath=A/'Environment/Surface/Surface_descent_v006.blend'
    worldpath=A/'Environment/Borehole/World_environment_v011.blend'
    instance(surfacepath,'SURFACE_RIG_SUBSEA_v004','Shared offshore equipment',scene=s)
    instance(surfacepath,'SURFACE_OCEAN_FULL','Shared ocean — mean waterline 0m',scene=s)
    M=json.loads((A/'Environment/Borehole/World_interface_v011.json').read_text())['canonical_to_s02']
    w=instance(worldpath,'WORLD_DESCENT_CONNECTED','One continuous physical World',M,s)
    w['visibility']='Present at full scale from frame 1; no section-boundary appearance action.'
    # The source irregular authority is a nonrendering lookup mesh for existing local data.
    # Keep its geometry and all acquisition/history animations untouched.
    s.frame_start=1;s.frame_end=528;s.frame_set(1)
    records=[]
    for f in range(1,529):
        s.frame_set(f);b=before[str(f)]
        assert b['matrix']==[list(row) for row in s.camera.matrix_world] and b['lens']==s.camera.data.lens
    s.frame_set(1)
    # Focused static views share the same masters and contain no section data.
    views=[('Surface — waterline',(145,-205,85),(0,0,-18),42,None),
           ('Surface — water column',(215,-310,50),(0,0,-40),40,380),
           ('World — layered descent',(370,-720,-460),(0,0,-510),40,1160)]
    for name,pos,target,lens,ortho in views:
        sc=bpy.data.scenes.new(name);sc.world=s.world;setup(sc);camera(sc,name+' camera',pos,target,lens,ortho)
        if name=='World — layered descent':sc.render.resolution_x=450;sc.render.resolution_y=800
        instance(surfacepath,'SURFACE_RIG_SUBSEA_v004','Shared offshore equipment',scene=sc)
        instance(surfacepath,'SURFACE_OCEAN_CUTAWAY','Ocean section — editorial viewing cut',scene=sc)
        instance(worldpath,'WORLD_DESCENT_CONNECTED','One continuous physical World',M,sc)
    text=bpy.data.texts.new('README connected descent demo')
    text.write('REVIEW DEMO. Scene dropdown: connected S01-S02 timeline (528f/24fps), waterline, water column, layered descent. Cameras/data/history from original v011 stay local. Shared Surface v006 owns equipment+ocean; World v011 owns geology+the exact existing S02 wall. World is present from frame1; no replacement at240/241. Half-ocean views are explanatory cuts. Full sea used in the moving scene. Geological units and depths illustrative, not field stratigraphy. Original scenes unchanged.\n')
    bpy.context.window.scene=s
    for area in bpy.context.screen.areas:
        if area.type=='VIEW_3D':area.spaces.active.region_3d.view_perspective='CAMERA'
    save(D/'Surface_descent_demo_v002.blend')
    (T/'demo-build.json').write_text(json.dumps({'source':str(src),'removed':removed,'camera_all_528_frames_identical':True,'wall_present_from_frame':1,'scenes':[sc.name for sc in bpy.data.scenes]},indent=2))

if __name__=='__main__':
    mode=sys.argv[-1]
    if mode=='surface':surface()
    elif mode=='demo':demo()
