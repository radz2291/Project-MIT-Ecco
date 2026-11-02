"""Focused camera look proof; accepted production v026 stays unchanged."""
import bpy,sys,json,time,datetime,hashlib
from pathlib import Path
from mathutils import Vector
Q=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/Shots/S01-S02');sys.path.insert(0,str(Q/'Scripts'));import final_render_visibility as display
assert bpy.data.filepath.endswith('S01-S02_production_v026.blend')
out=Q/'Scenes/S01-S02_transmitter_DOF_test_v001.blend';assert not out.exists()
if bpy.data.is_dirty:bpy.ops.wm.save_as_mainfile(filepath=str(Q/'Scenes'/('Before_DOF_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S')+'.blend')),copy=True,compress=True)
s=bpy.context.scene;cam=s.camera;cam.data=cam.data.copy();cam.data.name='S01-S02 transmitter focus camera — DOF proof'
events=json.loads((Q/'Notes/refinements_v025.json').read_text())['retargeted_beams'];s.frame_set(360);A=Vector(events[1]['source']);bha=bpy.data.objects['BHA sequence assembly']
focus=bpy.data.objects.new('DOF focus — transmitter face',None);s.collection.objects.link(focus);focus.parent=bha;focus.location=bha.matrix_world.inverted()@A;focus.empty_display_size=.005;focus.hide_render=True
cam.data.dof.focus_object=focus;cam.data.dof.aperture_blades=7;cam.data.dof.aperture_ratio=1
for w in bpy.context.window_manager.windows:
 for area in w.screen.areas:
  if area.type=='VIEW_3D':area.spaces.active.shading.use_dof=True
s.display.shading.use_dof=True
P=Q/'Previews/Transmitter-DOF-v001';P.mkdir(exist_ok=True);s.frame_set(386);rows=[]
with bpy.context.temp_override(window=bpy.context.window_manager.windows[0]):
 for name,enabled,fstop in [('sharp_reference',False,64),('subtle_f64',True,64),('stronger_f32',True,32)]:
  cam.data.dof.use_dof=enabled;cam.data.dof.aperture_fstop=fstop;bpy.context.view_layer.update();t=time.perf_counter();display.export(P/(name+'.png'),1920,1080);dt=time.perf_counter()-t;rows.append({'name':name,'fstop':fstop,'enabled':enabled,'seconds':dt});assert dt<5
cam.data.dof.use_dof=True;cam.data.dof.aperture_fstop=64
bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True)
record={'native':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'source':'S01-S02_production_v026.blend preserved','frame':386,'focus':focus.name,'focus_parent':bha.name,'focus_world':list(focus.matrix_world.translation),'lens_mm':cam.data.lens,'focus_depth_m':-(cam.matrix_world.inverted()@focus.matrix_world.translation).z,'selected_fstop':64,'stills':rows,'scope':'Close-up physical camera depth-of-field proof only; focus attached to transmitter source. Full-shot focus transition and motion not yet designed/reviewed.'}
(Q/'Notes/transmitter_dof_v001.json').write_text(json.dumps(record,indent=2));result=record
