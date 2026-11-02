"""Tiny surface contact patch at handshake arrival, no impact rings."""
import bpy,json,time
from pathlib import Path
from mathutils import Vector,Matrix
Q=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/Shots/S01-S02');out=Q/'Scenes/Waveform_contact_fast_v020.blend';assert not out.exists();assert 'center_reveal_fast_v019' in bpy.data.filepath
if bpy.data.is_dirty:bpy.ops.wm.save_as_mainfile(filepath=str(Q/f'Scenes/Before_contact_patch_{int(time.time())}.blend'),copy=True,compress=True)
data=json.loads((Q/'Notes/quick_center_reveal_v019.json').read_text());B=Vector(data['new_endpoint']);normal=Vector((B.x,B.y,0)).normalized();up=Vector((0,0,1));tangent=up.cross(normal).normalized();h=.0015
mesh=bpy.data.meshes.new('Handshake contact patch 3mm');mesh.from_pydata([(-h,0,-h),(h,0,-h),(h,0,h),(-h,0,h)],[],[(3,2,1,0)]);ob=bpy.data.objects.new('Handshake — subtle surface contact patch',mesh);bpy.context.scene.collection.objects.link(ob);ob.matrix_world=Matrix((tangent,-normal,up)).transposed().to_4x4();ob.location=B-normal*.00012
mat=bpy.data.materials.new('Handshake contact muted teal');mat.diffuse_color=(.17,.43,.46,1.);mesh.materials.append(mat)
for f,v in [(304,0.),(305,.45),(306,1.),(308,.85),(311,0.)]:ob.scale=(v,v,v);ob.keyframe_insert('scale',frame=f)
for l in ob.animation_data.action.layers:
 for st in l.strips:
  for bag in st.channelbags:
   for fc in bag.fcurves:
    for k in fc.keyframe_points:k.interpolation='LINEAR'
ob['Purpose']='Only handshake contact at305; tiny3mm square on wall, no rings. Main pulse/reveal unchanged.'
bpy.context.scene.frame_set(306);bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True)
(Q/'Notes/quick_contact_v020.json').write_text(json.dumps({'scene':str(out),'scope':'First-exchange small contact cue only','point':list(B),'patch_size_mm':3,'surface_clearance_mm':.12,'appearance_frames':[305,310],'hidden_before':305,'gone_at':311,'beam_arrival':305,'signal_and_main_tile_reveal':'unchanged from quickv019','preview':[300,353],'fps':24},indent=2));result={'saved':str(out),'patch':'3mm muted teal,305–310'}
