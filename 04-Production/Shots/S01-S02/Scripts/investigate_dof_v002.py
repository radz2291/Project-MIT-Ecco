"""Matched diagnosis only; never edit/save the approved production native."""
import bpy,sys,json,time,hashlib
from pathlib import Path
from mathutils import Vector
Q=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/Shots/S01-S02')
source=Q/'Scenes/S01-S02_production_v026.blend';source_hash=hashlib.sha256(source.read_bytes()).hexdigest()
assert Path(bpy.data.filepath)==source
proof=Q/'Scenes/S01-S02_DOF_investigation_v002.blend';assert not proof.exists()
bpy.ops.wm.save_as_mainfile(filepath=str(proof),copy=True,compress=True)
bpy.ops.wm.open_mainfile(filepath=str(proof),use_scripts=False)
s=bpy.context.scene;s.frame_set(386);c=s.camera;c.data=c.data.copy();A=Vector(json.loads((Q/'Notes/refinements_v025.json').read_text())['retargeted_beams'][1]['source'])
focus=bpy.data.objects.new('Investigation focus at transmitter source',None);s.collection.objects.link(focus);focus.location=A
c.data.dof.use_dof=True;c.data.dof.focus_object=focus;c.data.dof.aperture_fstop=32;s.display.shading.use_dof=True
s.render.resolution_x=960;s.render.resolution_y=540;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA'
P=Q/'Previews/DOF-investigation-v002';P.mkdir(exist_ok=True)
# Native render reevaluates visibility F-curves, so freeze this ONE diagnostic
# frame in the disposable copy before suppressing measurement/legacy objects.
for o in s.objects:
 if o.library or not o.animation_data:continue
 if o.animation_data.action:
  for l in o.animation_data.action.layers:
   for st in l.strips:
    for bag in st.channelbags:
     for fc in bag.fcurves:
      if fc.data_path in ['hide_render','hide_viewport']:fc.mute=True
 for fc in o.animation_data.drivers:
  if fc.data_path in ['hide_render','hide_viewport']:fc.mute=True
for o in s.objects:
 if o.hide_get() and not o.library:o.hide_render=True
objects=[bpy.data.objects[n] for n in ['ONE WALL - old history and current cells share topology','Shared fine measurement display']];flags=[(o,o.hide_render,o.hide_get()) for o in objects];records=[]
try:
 for label,measurement,dof in [('full_dof',True,True),('hardware_dof',False,True),('hardware_sharp',False,False)]:
  for o,hr,hv in flags:o.hide_render=hr if measurement else True;o.hide_set(hv if measurement else True)
  c.data.dof.use_dof=dof;s.render.filepath=str(P/(label+'.png'));bpy.context.view_layer.update();t=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t;records.append({'name':label,'measurement':measurement,'dof':dof,'seconds':dt});assert dt<5
finally:
 for o,hr,hv in flags:o.hide_render=hr;o.hide_set(hv)
result={'source_sha256':source_hash,'source_hash_unchanged':hashlib.sha256(source.read_bytes()).hexdigest()==source_hash,'source_depth_m':-(c.matrix_world.inverted()@A).z,'camera_lens_mm':c.data.lens,'tests':records,'scope':'Matched one-frame investigation only; proof scene is a copy, never integrated.'}
(Q/'Notes/dof_investigation_v002.json').write_text(json.dumps(result,indent=2))
