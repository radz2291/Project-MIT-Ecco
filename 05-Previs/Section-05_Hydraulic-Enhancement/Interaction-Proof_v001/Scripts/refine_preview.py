import bpy,math,json,time
from pathlib import Path
from mathutils import Vector,Quaternion
B=Path(__file__).resolve().parents[1];s=bpy.context.scene
m=bpy.data.materials['S05_SatinSteel'];p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(.18,.22,.26,1);p.inputs['Roughness'].default_value=.36
for name,power in [('S05_Key',25),('S05_Fill',13),('S05_Rim',12)]:bpy.data.lights[name].energy=power
for o in bpy.data.collections['S05_ILLUSTRATIVE_FLOW'].objects:
 if 'Tracer' in o.name:o.data.bevel_depth=.0009
 if 'Cutting' in o.name:
  for v in o.data.vertices:v.co*=1.35
cam=s.camera;cam.animation_data_clear();cam.data.lens=48
for f,loc,target in [(1,(1.45,.54,.64),(.01,0,.20)),(72,(1.39,.59,.72),(.01,0,.28)),(144,(1.34,.65,.80),(.01,0,.36))]:
 cam.location=loc;q=(Vector(target)-cam.location).to_track_quat('-Z','Y');cam.rotation_mode='QUATERNION';cam.rotation_quaternion=q@Quaternion((0,0,1),math.radians(-18));cam.keyframe_insert('location',frame=f);cam.keyframe_insert('rotation_quaternion',frame=f)
# Native editable camera-space text; calm fixed labels, no performance figures.
font=bpy.data.fonts.load('C:/Windows/Fonts/segoeui.ttf');font.pack()
mat=bpy.data.materials.new('S05_Editorial');mat.use_nodes=True;nt=mat.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs[0].default_value=(.59,.68,.74,1);em.inputs[1].default_value=.8;nt.links.new(em.outputs[0],out.inputs[0])
for name,txt,x,y,size in [('Title','ENP3  /  HYDRAULIC INTERACTION',-.353,.183,.0105),('Mode','Circulation only  /  Tool stationary',-.353,.166,.008),('Note','ILLUSTRATIVE FLOW  /  NOT CFD',-.353,-.198,.007)]:
 cu=bpy.data.curves.new(name,'FONT');cu.body=txt;cu.font=font;cu.size=size;cu.materials.append(mat);o=bpy.data.objects.new('S05_'+name,cu);s.collection.objects.link(o);o.parent=cam;o.location=(x,y,-1);o.rotation_euler=(0,0,0)
s.frame_set(72);s.render.filepath=str(B/'Previews/interaction_amber.png');bpy.ops.wm.save_as_mainfile(filepath=str(B/'Scenes/S05_twisted-pad_interaction_v001.blend'))
t=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t
(B/'Records/benchmark-refined.json').write_text(json.dumps({'frame':72,'seconds':dt,'full_write':True}));result={'seconds':dt}
