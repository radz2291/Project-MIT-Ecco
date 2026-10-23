import bpy, math, json, hashlib, time
from pathlib import Path
from mathutils import Vector, Quaternion
import numpy as np
B=Path(__file__).resolve().parents[1];s=bpy.context.scene;cam=s.camera
def fingerprint():
 s.frame_set(198);bpy.context.view_layer.update()
 h=hashlib.sha256()
 def add(v):h.update(json.dumps(v,sort_keys=True,default=str).encode())
 for me in sorted(bpy.data.meshes,key=lambda x:x.name):
  add([me.name,len(me.vertices),len(me.polygons)])
  a=np.empty(len(me.vertices)*3,dtype=np.float32);me.vertices.foreach_get('co',a);h.update(a.tobytes())
  a=np.empty(len(me.loops),dtype=np.int32);me.loops.foreach_get('vertex_index',a);h.update(a.tobytes())
  if me.shape_keys:
   for key in me.shape_keys.key_blocks:
    a=np.empty(len(key.data)*3,dtype=np.float32);key.data.foreach_get('co',a);h.update(a.tobytes())
 for mat in sorted(bpy.data.materials,key=lambda x:x.name):
  add([mat.name,tuple(mat.diffuse_color)])
  if mat.node_tree:
   for n in mat.node_tree.nodes:
    add([n.name,n.type])
    for inp in n.inputs:
     if hasattr(inp,'default_value'):
      val=inp.default_value
      try:val=list(val)
      except TypeError:pass
      add([inp.identifier,val])
   add([(l.from_node.name,l.from_socket.identifier,l.to_node.name,l.to_socket.identifier) for l in mat.node_tree.links])
 cameraactions={a.animation_data.action.name for a in [cam,cam.data] if a.animation_data and a.animation_data.action}
 for a in sorted(bpy.data.actions,key=lambda x:x.name):
  if a.name in cameraactions or 'v019_CAMERA' in a.name or 'Camera' in a.name:continue
  add(a.name)
  for layer in a.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for fc in bag.fcurves:add([fc.data_path,fc.array_index,[(list(k.co),k.interpolation) for k in fc.keyframe_points]])
 for f in [1,120,198,288,432]:
  s.frame_set(f);bpy.context.view_layer.update()
  for o in sorted(s.objects,key=lambda x:x.name):
   if o==cam:continue
   add([f,o.name,[list(r) for r in o.matrix_world],o.hide_render,o.hide_viewport,o.parent.name if o.parent else None])
 return h.hexdigest()
def pose(d,az,zcam,zlook,lens,roll,shiftx=0,shifty=0):
 a=math.radians(az);cam.location=(d*math.cos(a),d*math.sin(a),zcam)
 cam.rotation_mode='QUATERNION';cam.rotation_quaternion=(Vector((0,0,zlook))-cam.location).to_track_quat('-Z','Y')@Quaternion((0,0,1),math.radians(roll))
 cam.data.lens=lens;cam.data.shift_x=shiftx;cam.data.shift_y=shifty
if globals().get('MODE','study')=='study':
 source=Path(bpy.data.filepath);assert source.name=='S05_full-cinematic_v018.blend'
 s.frame_set(198)
 baseline={'source':str(source),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'immutable_scene_fingerprint':fingerprint(),'frame_reference':432,'description':'Mesh coordinates/topology/shapekeys, materials/nodes/links, noncamera action curves, object transforms and visibility sampled at five frames. Camera/render settings excluded.'}
 (B/'Records/source-baseline.json').write_text(json.dumps(baseline,indent=2))
 bpy.ops.wm.save_as_mainfile(filepath=str(B/'Scenes/S05_camera-direction_v019.blend'))
 cam.animation_data_clear();cam.data.animation_data_clear()
 s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=75;s.eevee.taa_render_samples=4
 specs=[
  ('A_low',96,[.72,-18,-.78,.02,40,-22,-.025,0]),
  ('A_threequarter',96,[1.08,-25,-.61,.02,46,-30,-.02,0]),
  ('B_sculpture',205,[.92,-20,.65,.34,47,-30,.025,.015]),
  ('B_passage',205,[1.06,12,.37,.32,50,-58,.025,.025]),
  ('C_revelation',420,[2.35,-12,1.65,.28,46,-65,0,0]),
  ('C_perspective',420,[1.85,-20,1.70,.28,40,-73,0,0])]
 out=[]
 for name,f,p in specs:
  s.frame_set(f);pose(*p);bpy.context.view_layer.update();s.render.filepath=str(B/'Previews'/('study_'+name+'.png'))
  t=time.perf_counter();bpy.ops.render.render(write_still=True);out.append({'name':name,'frame':f,'pose':p,'seconds':time.perf_counter()-t})
 (B/'Records/arrival-study.json').write_text(json.dumps(out,indent=2));result={'studies':out}
