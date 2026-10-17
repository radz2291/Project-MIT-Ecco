"""One still only. Freeze a new consumer; preserve all earlier work/masters."""
import bpy,json,hashlib,time,math
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
P=Path(__file__).resolve().parents[3];M=P/'Mechanisms/B201';R=P/'Records/Tasks/T-007/Evidence/Still_01'
src=M/'Scenes/B201_integrated_v011.blend';out=M/'Scenes/B201_sensor-origin_still01_v001.blend';png=M/'Previews/Still_01/B201_sensor-origin_still01_v001.png'
if out.exists():raise RuntimeError('Refuse overwrite; version proposal')
hashes={str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [P/'Shared/Assets/ECCO/ECCO_master_temporary-plugs_v002.blend',P/'Shared/Assets/WellAssembly/WellAssembly_variants_v003.blend']}
bpy.ops.wm.open_mainfile(filepath=str(src));s=bpy.context.scene;s.frame_set(1);bpy.context.view_layer.update()
# Freeze evaluated local control values before removing their motion/drivers.
for o in list(s.objects):
 if o.library is None:
  mat=o.matrix_basis.copy()
  if o.animation_data:o.animation_data_clear()
  o.matrix_basis=mat
for n in ('B201_PULSE_ECHO','B201_CONTACT_HISTORY','B201_SPATIAL_GRAPHICS'):
 c=bpy.data.collections.get(n)
 if c:c.hide_render=True;c.hide_viewport=True
# Physically exclude diagnostic groups; no illustrative locator geometry.
for o in list(s.objects):
 if o.library is None and o.type in ('EMPTY','FONT'):o.hide_render=True
for c in bpy.data.collections:
 if c.name.startswith('B201_') and c.name not in ('B201_REGISTERED_WALL_CUTAWAY','B201_REVIEW_CAMERA'):c.hide_render=True
s.frame_start=1;s.frame_end=1;s.frame_set(1)
cam=s.camera;cam.location=(2.56,-.31,.48);target=Vector((2.81,-.01,.106))
cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.rotation_euler.rotate_axis('Z',math.radians(-8))
cam.data.type='PERSP';cam.data.lens=65;cam.data.sensor_width=36;cam.data.clip_start=.005;cam.data.clip_end=50
cam.data.dof.use_dof=False
s.render.engine='BLENDER_EEVEE';s.render.resolution_x=1920;s.render.resolution_y=1080;s.render.resolution_percentage=100
s.render.image_settings.file_format='PNG';s.render.filepath=bpy.path.relpath(str(png),start=str(out.parent))
s.world.use_nodes=True;bg=s.world.node_tree.nodes.get('Background');bg.inputs['Color'].default_value=(.025,.034,.045,1);bg.inputs['Strength'].default_value=.12
mat=bpy.data.materials.new('Still01 neutral wall / proposed look');mat.diffuse_color=(.032,.043,.049,1);mat.use_nodes=True
bs=mat.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.032,.043,.049,1);bs.inputs['Roughness'].default_value=.88
wall=bpy.data.objects['T6_IRREGULAR_VIEW_WINDOW'];wall.data.materials.clear();wall.data.materials.append(mat)
lights=bpy.data.collections.new('STILL01_LIGHTING');s.collection.children.link(lights)
def area(name,pos,aim,power,size,color):
 data=bpy.data.lights.new(name,'AREA');data.energy=power;data.shape='DISK';data.size=size;data.color=color
 o=bpy.data.objects.new(name,data);lights.objects.link(o);o.location=pos;o.rotation_euler=(Vector(aim)-o.location).to_track_quat('-Z','Y').to_euler()
area('Broad soft key',(2.55,-.18,.62),(2.8,0,.1),38,.42,(.84,.91,1.))
area('Long shoulder reflection',(3.0,.25,.40),(2.8,0,.06),26,.35,(1.,.91,.79))
area('Quiet fill',(2.55,-.42,.16),(2.8,0,.12),7,.28,(.65,.8,1.))
s.view_settings.view_transform='AgX';s.view_settings.exposure=-.8
s['review_scope']='Still01 sensor origin only. No diagnostic markers, pulse, waveform, motion or approval implied.'
s['direction_contract']='//../direction.md'
for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(out.parent))
bpy.context.view_layer.update()
materials=[]
for o in bpy.data.collections['ECCO_MASTER_v002'].all_objects:
 if o.type=='MESH':materials.append({'object':o.name,'materials':[m.name for m in o.data.materials if m]})
bpy.ops.wm.save_as_mainfile(filepath=str(out),relative_remap=False)
bpy.ops.wm.open_mainfile(filepath=str(out));s=bpy.context.scene;bpy.context.view_layer.update()
t=time.perf_counter();bpy.ops.render.render(write_still=True);elapsed=time.perf_counter()-t
e={'scene':str(out.relative_to(P)),'image':str(png.relative_to(P)),'scene_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'image_sha256':hashlib.sha256(png.read_bytes()).hexdigest(),'render_seconds':elapsed,'resolution':[1920,1080],'engine':s.render.engine,'camera':{'location':list(s.camera.location),'rotation':list(s.camera.rotation_euler),'lens_mm':s.camera.data.lens},'inputs':hashes,'materials_inspected':materials,'source_hashes_unchanged':all(hashlib.sha256((P/rel).read_bytes()).hexdigest()==h for rel,h in hashes.items()),'links_resolve':all(Path(bpy.path.abspath(l.filepath)).is_file() for l in bpy.data.libraries),'hidden_groups':[{'name':n,'hidden':bpy.data.collections[n].hide_render} for n in ('B201_PULSE_ECHO','B201_CONTACT_HISTORY','B201_SPATIAL_GRAPHICS')],'animation_rendered':False,'human_approval':'pending'}
(R/'build-render_still01_v001.json').write_text(json.dumps(e,indent=2));print('STILL01_PASS',elapsed)
