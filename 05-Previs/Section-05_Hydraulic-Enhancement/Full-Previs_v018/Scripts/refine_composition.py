import bpy,math,json
from pathlib import Path
from mathutils import Vector,Quaternion
B=Path(__file__).resolve().parents[1];s=bpy.context.scene;cam=s.camera
def smooth(x):
 x=max(0,min(1,x));return x*x*(3-2*x)
for m in bpy.data.objects['S05_FixedHalfBorehole'].data.materials:
 for p in m.node_tree.nodes:
  if p.type=='BSDF_PRINCIPLED':
   p.inputs['Base Color'].default_value=(.055,.045,.032,1);p.inputs['Metallic'].default_value=0;p.inputs['Roughness'].default_value=.97;p.inputs['Specular IOR Level'].default_value=.1
for f in range(1,121):
 q=smooth((f-1)/119);d=2.3-.60*q;az=math.radians(-13+13*q);zlook=-.24+.28*q
 cam.location=(d*math.cos(az),d*math.sin(az),zlook+.24-.11*q)
 cam.rotation_quaternion=(Vector((0,0,zlook))-cam.location).to_track_quat('-Z','Y')@Quaternion((0,0,1),math.radians(-48))
 for prop in ['location','rotation_quaternion']:cam.keyframe_insert(prop,frame=f)
s.frame_set(198);s.render.filepath='//../Previews/interaction.png';bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
result={'change':'Warmer darker matte rock to distinguish formation from steel; A slightly wider and oblique to establish annulus and accelerator together.'}
(B/'Records/composition-refinement.json').write_text(json.dumps(result,indent=2))
