"""B204 circulation-only proof. Authored paths are illustrative, never CFD.
Run in background Blender; source masters and the live scene stay untouched.
"""
import bpy,math,json,hashlib,time,sys
from pathlib import Path
from mathutils import Vector
P=Path(__file__).resolve().parents[1]; PROD=P.parents[1]
TASK=PROD/'Records/Tasks/T-010'; OUT=P/'Scenes/B204_hydraulic-proof_v001.blend'
if OUT.exists(): raise RuntimeError('Candidate already exists; version before rebuilding')
src=PROD/'Shared/Assets/ECCO/ECCO_master_temporary-plugs_v002.blend'
well=PROD/'Shared/Assets/WellAssembly/WellAssembly_variants_v003.blend'
cfg=json.loads((well.parent/'config_authorized_v003.json').read_text())
assert hashlib.sha256(src.read_bytes()).hexdigest()==cfg['product_sha256']
bpy.ops.wm.read_factory_settings(use_empty=True)
s=bpy.context.scene;s.unit_settings.system='METRIC';s.render.engine='BLENDER_WORKBENCH'
s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100
s.render.fps=24;s.frame_start=1;s.frame_end=288
s.display.shading.light='STUDIO';s.display.shading.studiolight_rotate_z=.5
s.display.shading.color_type='OBJECT';s.display.shading.show_shadows=True
s.display.shading.show_cavity=True;s.display.shading.cavity_type='BOTH'
s.world=bpy.data.worlds.new('B204_world')
s.display.shading.background_type='WORLD';s.world.color=(.055,.065,.08)
s.view_settings.view_transform='Standard'
s.display.render_aa='8'
with bpy.data.libraries.load(str(src),link=True) as (a,b):b.collections=['ECCO_MASTER_v002']
col=bpy.data.collections.new('B204_ILLUSTRATIVE_FLOW');s.collection.children.link(col)
def obj(name,data=None):
    o=bpy.data.objects.new(name,data);col.objects.link(o);return o
rig=obj('HYDRAULIC_CONTROL');rig['flow_rate']=1.;rig['flow_visible']=1;rig['cuttings_visible']=1
rig['mode']='CIRCULATION ONLY: stationary tool; authored flow paths, not CFD'
rig['mapping']='Source +X return direction is provisional; no CAD-stage labels'
rig.id_properties_ui('flow_rate').update(min=0,max=3,description='Illustrative playback multiplier; no physical units')
inst=obj('ECCO_LINK_v002');inst.instance_type='COLLECTION';inst.instance_collection=b.collections[0];inst.location.z=.43
def curve(name,points,color,r=.001):
    c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.bevel_depth=r;c.bevel_resolution=1
    sp=c.splines.new('POLY');sp.points.add(len(points)-1)
    for v,p in zip(sp.points,points):v.co=(*p,1)
    o=obj(name,c);o.color=(*color,1);return o
white=(.82,.87,.9);cyan=(.05,.8,.88);orange=(1,.55,.12);gray=(.24,.29,.34)
def text(name,body,x,z,size=.045,color=white):
    d=bpy.data.curves.new(name,'FONT');d.body=body;d.size=size;d.extrude=0
    o=obj(name,d);o.location=(x,-.28,z);o.rotation_euler.x=math.pi/2;o.color=(*color,1);return o
text('Title','B204  /  HYDRAULIC MECHANISM',-.28,.99,.066)
text('Mode','CIRCULATION ONLY   |   Tool stationary',-.28,.88,.043,cyan)
text('CADLabel','Accepted plugged CAD v002  /  annular return toward source +X  >',-.28,.73,.039)
text('Mapping','End-direction inference pending MIT review; hydraulic stage locations unassigned.',-.28,.15,.036)
text('DiagramLabel','FUNCTIONAL SCHEMATIC  /  no dimensional or CAD-stage correspondence',-.28,-.02,.038)
text('S1','01  ACCELERATOR',-.18,-.53,.041)
text('S2','02  TWISTED PADS',.7,-.53,.041)
text('S3','03  DIFFUSER',1.63,-.53,.041)
text('D1','Local acceleration',-.18,-.61,.034)
text('D2','Redirection / agitation',.7,-.61,.034)
text('D3','Pressure-recovery intent',1.63,-.61,.034)
text('Limit','ILLUSTRATIVE FLOW  /  not CFD or MIT FEA  /  no performance scale',-.28,-.78,.041,cyan)
text('Legend','Cyan: authored mud paths     Amber: illustrative cuttings     Marker sizes exaggerated',-.28,-.88,.034)
# Rear-half annular outline uses accepted T6 nominal diameter. No new well claims.
R=cfg['intervals']['lower_open']['hole_diameter_inches']*.0254/2
for a in (0,math.pi):
    curve('Nominal_annulus_outline',[(x,R*math.sin(a),.43+R*math.cos(a)) for x in (-.08,2.48)],gray,.001)
for x in (-.08,2.48):
    curve('Annulus_end',[(x,R*math.sin(a),.43+R*math.cos(a)) for a in [i*math.pi/32 for i in range(33)]],gray,.001)
for j in range(4):
    angle=math.pi*(j+.5)/4
    curve('Illustrative_annular_guide',[(x,-.1545*math.sin(angle),.43+.1545*math.cos(angle)) for x in (-.06,2.46)],cyan,.00055)
# Lightweight reusable marker mesh; positions driven without Python handlers.
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=1)
temp=bpy.context.object;mesh=temp.data;bpy.data.objects.remove(temp,do_unlink=True)
def driver(o,index,expr,extra=None):
    d=o.driver_add('location',index).driver;d.expression=expr
    v=d.variables.new();v.name='rate';v.type='SINGLE_PROP';v.targets[0].id=rig;v.targets[0].data_path='["flow_rate"]'
    for name,prop in (extra or {}).items():
        v=d.variables.new();v.name=name;v.type='SINGLE_PROP';v.targets[0].id=o;v.targets[0].data_path=prop
def visible(o,prop):
    d=o.driver_add('hide_render').driver;d.expression='1-v'
    v=d.variables.new();v.name='v';v.type='SINGLE_PROP';v.targets[0].id=rig;v.targets[0].data_path='["'+prop+'"]'
for j in range(32):
    a=math.pi*((j%4)+.5)/4;phase=(j//4)/8
    o=obj('Mud_annular_%02d'%j,mesh);o.scale=(.006,.003,.003);o.color=(*cyan,1)
    o.location=(0,-.1545*math.sin(a),.43+.1545*math.cos(a))
    driver(o,0,f'-.06+2.52*(((frame-1)*rate/96+{phase})%1)')
    visible(o,'flow_visible')
# Conceptual path contraction, turning and spreading. These are drawn explanatory
# marks in a separate panel, not reconstructed hydraulic geometry or flow fields.
def path(t,side):
    x=-.18+2.7*t
    r=.16-.085*min(1,t/.3) if t<.3 else (.075 if t<.67 else .075+.085*(t-.67)/.33)
    wob=.025*math.sin((t-.3)*48)*math.sin(math.pi*max(0,min(1,(t-.3)/.37))) if .3<t<.67 else 0
    return (x,-.05,-.29+side*r+wob)
for side in (-1,1):
    curve('Conceptual_streamline',[path(i/120,side) for i in range(121)],cyan,.002)
for x in (.63,1.53):curve('Stage_separator',[(x,.05,-.47),(x,.05,-.1)],gray,.001)
for j in range(18):
    side=1 if j%2 else -1;phase=j/18
    o=obj('Diagram_mud_%02d'%j,mesh);o.color=(*cyan,1);o.scale=(.012,.012,.012)
    # Sampled linear position keys are directly editable; flow_rate drives time.
    o['phase']=phase
    o['t']=phase
    d=o.driver_add('["t"]').driver;d.expression=f'((frame-1)*rate/96+{phase})%1'
    v=d.variables.new();v.name='rate';v.type='SINGLE_PROP';v.targets[0].id=rig;v.targets[0].data_path='["flow_rate"]'
    driver(o,0,'-.18+2.7*t',{'t':'["t"]'})
    driver(o,2,f'-.29+{side}*(.16-.085*min(1,t/.3) if t<.3 else (.075 if t<.67 else .075+.085*(t-.67)/.33))+.025*sin((t-.3)*48)*sin(pi*max(0,min(1,(t-.3)/.37)))*(.3<t<.67)',{'t':'["t"]'})
    o.location.y=-.07;visible(o,'flow_visible')
for j in range(6):
    o=obj('Diagram_cutting_%02d'%j,mesh);o.color=(*orange,1);o.scale=(.018,.008,.013)
    t=f'(((frame-1)*rate/120+{j/6})%1)'
    driver(o,0,f'-.18+2.7*{t}');driver(o,2,f'-.29+.04*sin(18*{t}+{j})')
    o.location.y=-.1;visible(o,'cuttings_visible')
camdata=bpy.data.cameras.new('B204_review_camera');cam=obj('B204_review_camera',camdata)
cam.location=(1.15,-6,.09);cam.rotation_euler=(Vector((1.15,0,.09))-cam.location).to_track_quat('-Z','Y').to_euler()
camdata.type='ORTHO';camdata.ortho_scale=3.7;s.camera=cam
s.render.image_settings.file_format='PNG';s.render.filepath=str(P/'Previews/Frames/B204_')
for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(lib.filepath,start=str(OUT.parent))
s.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
evidence={'blender':bpy.app.version_string,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'well_sha256':hashlib.sha256(well.read_bytes()).hexdigest(),'nominal_wall_radius_m':R,'flow_marker_center_radius_m':.1545,'source_max_radius_m':.1524000685,'center_radial_clearance_m':R-.1545,'frames':[1,288],'fps':24,'resolution':[1280,720],'mode':'circulation only','stage_to_CAD_map':'unassigned; MIT review pending','motion':'authored uniform timing, not physical velocity','source_scene_mutated':False}
(TASK/'Evidence/build-verification_v001.json').write_text(json.dumps(evidence,indent=2))
start=time.perf_counter()
for f in (1,49,97,145,193,241,288):
    s.frame_set(f);s.render.filepath=str(P/f'Previews/B204_inspect_f{f:03d}_v001.png');bpy.ops.render.render(write_still=True)
(TASK/'Evidence/still-render_v001.json').write_text(json.dumps({'seconds':time.perf_counter()-start}))
