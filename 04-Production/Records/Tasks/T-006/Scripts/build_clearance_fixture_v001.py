"""Source-sized dimensional inspection fixture, NOT a selected well assembly.

Isolated background Blender only. Never edits the linked accepted T5 asset.
"""
import bpy,json,math,time,hashlib
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[4]
TASK=ROOT/'Records/Tasks/T-006';ASSET=ROOT/'Shared/Assets/WellAssembly'
source=ROOT/'Shared/Assets/ECCO/ECCO_master_temporary-plugs_v002.blend'
expected='704a91cb478a1a38304835786fa62d549df5bf5833e457cbc4da094fd6557fd7'
assert hashlib.sha256(source.read_bytes()).hexdigest()==expected
out=ASSET/'B102_clearance-fixture_v001.blend'
if out.exists():raise SystemExit('Version output rather than overwrite an inspected fixture')
bpy.ops.wm.read_factory_settings(use_empty=True)
scene=bpy.context.scene
with bpy.data.libraries.load(str(source),link=True) as (src,dst):
    dst.collections=['ECCO_MASTER_v002']
product=dst.collections[0]
fixture=bpy.data.collections.new('B102_CLEARANCE_FIXTURE_ONLY')
scene.collection.children.link(fixture)
def empty(name,parent=None):
    o=bpy.data.objects.new(name,None);fixture.objects.link(o);o.parent=parent;return o
root=empty('FIXTURE_TRAVEL_X');rot=empty('FIXTURE_ROTATION_X',root)
instance=empty('LINKED_ACCEPTED_T5_v002',rot)
instance.instance_type='COLLECTION';instance.instance_collection=product
root['test_only']='100mm axial interface exercise; not drilling speed or validated travel range'
rot['test_only']='360deg interface exercise; not claimed drilling direction/end datum'
for frame,angle,travel in [(1,0,0),(96,2*math.pi,.1)]:
    root.location.x=travel;root.keyframe_insert('location',frame=frame)
    rot.rotation_euler.x=angle;rot.keyframe_insert('rotation_euler',frame=frame)
for obj in (root,rot):
    for fc in obj.animation_data.action.layers[0].strips[0].channelbag(obj.animation_data.action_slot).fcurves:
        for k in fc.keyframe_points:k.interpolation='LINEAR'
# Wire boundary: radius from published minimum casing ID, no casing thickness.
# Extent is source bound plus test travel; not an engineering casing length.
radius=12.3*.0254/2
curve=bpy.data.curves.new('PUBLISHED_MINIMUM_ID_BOUNDARY','CURVE')
curve.dimensions='3D';curve.bevel_depth=.0006;curve.bevel_resolution=0
for x in (0,.73,2.4,2.5):
    spline=curve.splines.new('POLY');spline.points.add(128)
    for j,p in enumerate(spline.points):
        a=2*math.pi*j/128;p.co=(x,radius*math.cos(a),radius*math.sin(a),1)
for a in (math.pi/2,3*math.pi/2):
    spline=curve.splines.new('POLY');spline.points.add(1)
    spline.points[0].co=(0,radius*math.cos(a),radius*math.sin(a),1)
    spline.points[1].co=(2.5,radius*math.cos(a),radius*math.sin(a),1)
boundary=bpy.data.objects.new('12_3in_MINIMUM_ID_REFERENCE_NO_WALL',curve)
fixture.objects.link(boundary);boundary.color=(.15,.65,.7,1)
boundary['source']='ENP3 datasheet p3 minimum casing ID 12.3in; not selected casing'
boundary['limit']='No OD, wall thickness, cement, BHA, bit or trajectory asserted'
camera_data=bpy.data.cameras.new('CLEARANCE_INSPECTION_CAMERA')
camera=bpy.data.objects.new(camera_data.name,camera_data);fixture.objects.link(camera)
camera.location=(1.25,-3,1.5)
camera.rotation_euler=(Vector((1.25,0,0))-camera.location).to_track_quat('-Z','Y').to_euler()
camera_data.type='ORTHO';camera_data.ortho_scale=3.2;scene.camera=camera
scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
scene.render.engine='BLENDER_WORKBENCH'
scene.render.resolution_x=1280;scene.render.resolution_y=720;scene.render.resolution_percentage=100
scene.render.fps=24;scene.frame_start=1;scene.frame_end=96
sh=scene.display.shading;sh.light='STUDIO';sh.color_type='OBJECT'
sh.show_cavity=True;sh.cavity_type='BOTH';sh.show_shadows=True
sh.background_type='VIEWPORT';sh.background_color=(.055,.065,.08)
scene.render.image_settings.file_format='PNG'
frames=TASK/'Previews/clearance-frames_v001';frames.mkdir(parents=True,exist_ok=True)
scene.render.filepath='//../../../Records/Tasks/T-006/Previews/clearance-frames_v001/frame_'
scene['status']='DIMENSIONAL INSPECTION FIXTURE ONLY. Not a casing/well/BHA assembly or deployment approval.'
scene['provenance']='Accepted T5 v002; source-sized 12.3in minimum ID boundary. 96 frames/24fps control test only.'
for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(lib.filepath,start=str(ASSET))
scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(out))
# Render the saved fixture in the same process, with no post-save modifications.
t=time.perf_counter();bpy.ops.render.render(animation=True)
e={'source_sha256':expected,'fixture_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),
   'frames':96,'fps':24,'resolution':[1280,720],'engine':'BLENDER_WORKBENCH',
   'render_elapsed_seconds':time.perf_counter()-t,'boundary_id_m':2*radius,
   'limit':'Only sourced minimum-ID envelope and test motion; not selected deployment'}
(TASK/'Evidence/clearance-fixture-build_v001.json').write_text(json.dumps(e,indent=2),encoding='utf-8')
