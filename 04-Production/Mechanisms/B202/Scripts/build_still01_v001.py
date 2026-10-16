"""First grounded sampling-history proposal; isolated background Blender only."""
import bpy, math, json, hashlib, time
from pathlib import Path
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree

P=Path(__file__).resolve().parents[3]
M=P/'Mechanisms/B202'
E=P/'Records/Tasks/T-008/Evidence/Still_01'
SOURCE=P/'Mechanisms/B201/Scenes/B201_pulse-echo_fast-preview_v005.blend'
OUT=M/'Scenes/B202_sampling-history_still01_v001.blend'
IMAGE=M/'Previews/Still_01/B202_sampling-history_still01_v001.png'
assert not OUT.exists(), 'Preserve candidates; increment the version'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source_record=json.loads((P/'Records/Tasks/T-007/Evidence/Motion_v005/build.json').read_text())
assert sha(SOURCE)==source_record['scene_sha256']
for rel,expected in source_record['inputs'].items():assert sha(P/rel)==expected
bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
s=bpy.context.scene
bpy.context.window.view_layer=s.view_layers['FAST model and mechanism']
s.frame_set(31)
wall=bpy.data.objects['T6_WALL_CONTACT_SECTION']
tree=BVHTree.FromPolygons([wall.matrix_world@v.co for v in wall.data.vertices],[list(p.vertices) for p in wall.data.polygons])
history=bpy.data.collections.new('B202_ILLUSTRATIVE_SAMPLE_HISTORY')
s.collection.children.link(history)
control=bpy.data.objects.new('B202_SAMPLE_DISPLAY_CONTROL',None);history.objects.link(control)
control['visible']=1
control['display_radius_m']=.0008
control['axial_history_m']=.65
control['rotation_turns']=1.0
control['history_kind']='Illustrative historical positions; not actual data, bin scheduling, RPM or validated drilling direction'
mat=bpy.data.materials.new('B202 recorded-location white - NOT radius colormap');mat.use_nodes=True
shader=mat.node_tree.nodes.get('Principled BSDF')
shader.inputs['Base Color'].default_value=(.68,.81,.9,1)
shader.inputs['Roughness'].default_value=.5
shader.inputs['Emission Color'].default_value=(.68,.81,.9,1)
shader.inputs['Emission Strength'].default_value=.65
event=source_record['events'][0]
receiver=Vector(event['receiver'])
a0=math.atan2(receiver.z,receiver.y)
sample_records=[]
# Three paths with 120-degree phase offsets. 48 points each is a decimated
# visual history, expressly unrelated to the instrument's 108 azimuth bins.
for sensor in range(3):
    for i in range(48):
        age=(i+1)/48
        x=receiver.x+control['axial_history_m']*age
        a=a0+sensor*2*math.pi/3-control['rotation_turns']*2*math.pi*age
        radial=Vector((0,math.cos(a),math.sin(a)))
        origin=Vector((x,0,0))
        hit,normal,face,distance=tree.ray_cast(origin,radial)
        assert hit is not None,(sensor,i,x,a)
        center=hit-radial*.00035
        bpy.ops.mesh.primitive_uv_sphere_add(segments=8,ring_count=4,radius=1,location=center)
        o=bpy.context.object;o.name=f'B202_SAMPLE_s{sensor+1}_{i:03d}'
        for c in list(o.users_collection):c.objects.unlink(o)
        history.objects.link(o);o.data.materials.append(mat)
        for p in o.data.polygons:p.use_smooth=True
        for axis in range(3):
            f=o.driver_add('scale',axis);d=f.driver;d.expression='r'
            v=d.variables.new();v.name='r';v.targets[0].id=control;v.targets[0].data_path='["display_radius_m"]'
        f=o.driver_add('hide_render');d=f.driver;d.expression='1-v'
        v=d.variables.new();v.name='v';v.targets[0].id=control;v.targets[0].data_path='["visible"]'
        o['wall_hit']=list(hit);o['historical_sensor']=sensor+1;o['illustrative_age']=age
        o['wall_face']=face
        sample_records.append({'object':o.name,'sensor':sensor+1,'age':age,'hit':list(hit),'center':list(center),'ray_distance_m':distance,'wall_face':face})

s.render.resolution_x=1920;s.render.resolution_y=1080;s.render.resolution_percentage=100
s.eevee.taa_render_samples=32
s.render.filepath=str(IMAGE)
s['B202_scope']='Still01 proposal only: inherited T7 contact frame plus illustrative accumulated sample positions. No new motion, reconstruction, field data or visual approval.'
s['B202_input_scene']=str(SOURCE.relative_to(P))
for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(OUT.parent))
bpy.context.view_layer.update()
bpy.ops.wm.save_as_mainfile(filepath=str(OUT),relative_remap=False)
bpy.ops.wm.open_mainfile(filepath=str(OUT))
s=bpy.context.scene;bpy.context.window.view_layer=s.view_layers['FAST model and mechanism']
t=time.perf_counter();bpy.ops.render.render(write_still=True)
record={'scene':str(OUT.relative_to(P)),'scene_sha256':sha(OUT),'image':str(IMAGE.relative_to(P)),'image_sha256':sha(IMAGE),'source':str(SOURCE.relative_to(P)),'source_sha256':sha(SOURCE),'inputs':source_record['inputs'],'frame':31,'render_seconds':time.perf_counter()-t,'resolution':[1920,1080],'samples':sample_records,'camera':{'location':list(s.camera.location),'rotation':list(s.camera.rotation_euler),'lens':s.camera.data.lens},'actual_data':False,'visual_approval':'pending','new_motion':False,'source_unchanged':sha(SOURCE)==source_record['scene_sha256']}
E.mkdir(parents=True,exist_ok=True);(E/'build-render_v001.json').write_text(json.dumps(record,indent=2))
print('B202_STILL01_PASS',record['render_seconds'],flush=True)
