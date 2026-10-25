import bpy,json,hashlib,numpy as np
from pathlib import Path
B=Path(__file__).resolve().parents[1];P=B.parent/'Sequence_v001';old=P/'Scenes/S07_Monumental-Precision_v001.blend'
assert hashlib.sha256(old.read_bytes()).hexdigest()==json.loads((B/'Records/revision.json').read_text())['source_sha256']
frames=list(range(1,61))+list(range(146,193))
def states(path):
 bpy.ops.wm.open_mainfile(filepath=str(path));s=bpy.context.scene;res={}
 for f in frames:
  s.frame_set(f);bpy.context.view_layer.update();cam=s.camera
  vals=list(cam.location)+list(cam.rotation_quaternion)+[cam.data.lens,cam.data.shift_x,cam.data.shift_y,cam.data.dof.aperture_fstop]
  for name in ['Camera focus target','Product identification','MIT logo placeholder']:vals+=list(bpy.data.objects[name].location)+list(bpy.data.objects[name].scale)
  res[f]=vals
 return res
a=states(old);b=states(B/'Scenes/S07_Monumental-Precision_v002.blend')
maximum=max(float(np.max(np.abs(np.array(a[f])-np.array(b[f])))) for f in frames);assert maximum<1e-7
(B/'Records/reuse-verification.json').write_text(json.dumps({'prior_native_unchanged':True,'reused_frames':len(frames),'ranges':[[1,60],[146,192]],'camera_focus_and_brand_transforms_identical':True,'maximum_delta':maximum,'unchanged_geometry_lighting_materials':'Revision script modifies only camera, focus and invisible-title placement within frames61-145'},indent=2));print('REUSE VERIFIED',maximum)
