"""S07 complete owner-authorized sequence. Source hardware is never edited."""
import bpy,math,json,hashlib,shutil
from pathlib import Path
from mathutils import Vector,Quaternion
from bpy_extras.object_utils import world_to_camera_view
B=Path(__file__).resolve().parents[1]; R=B.parents[3]
SRC=R/'04-Production/Shared/Assets/ECCO/ECCO_film_v002.blend'
for folder in ('Scenes','Previews','Cache','Graphics','Records'): (B/folder).mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(SRC));s=bpy.context.scene;s.name='S07 | Monumental Precision'
for o in bpy.data.objects:
 o.animation_data_clear()
 if o.type=='MESH' and 'CUTTER' not in o.name:
  o['S07_source_object']=o.name
  for slot in o.material_slots:
   if slot.material:
    original_material=slot.material;slot.link='OBJECT';slot.material=original_material.copy();slot.material.name='S07 satin | '+o.name
    m=slot.material;m.use_nodes=True;nd=m.node_tree.nodes;nd.clear();out=nd.new('ShaderNodeOutputMaterial');bs=nd.new('ShaderNodeBsdfPrincipled')
    bs.inputs['Base Color'].default_value=(.24,.29,.34,1);bs.inputs['Metallic'].default_value=.85;bs.inputs['Roughness'].default_value=.30
    if 'Imaging port' in o.name:bs.inputs['Base Color'].default_value=(.12,.17,.19,1);bs.inputs['Roughness'].default_value=.32
    m.node_tree.links.new(bs.outputs['BSDF'],out.inputs['Surface'])
 if 'CUTTER' in o.name:o.hide_render=True;o.hide_viewport=True
for o in list(bpy.data.objects):
 if o.type in ('CAMERA','LIGHT'):bpy.data.objects.remove(o,do_unlink=True)
s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=32
s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100
s.render.fps=24;s.frame_start=1;s.frame_end=192;s.render.image_settings.file_format='PNG';s.render.film_transparent=False
s.view_settings.view_transform='AgX';s.view_settings.look='AgX - Medium High Contrast';s.view_settings.exposure=0
s.world=bpy.data.worlds.new('S07 charcoal studio');s.world.use_nodes=True
s.world.node_tree.nodes['Background'].inputs[0].default_value=(.075,.095,.12,1)
s.world.node_tree.nodes['Background'].inputs[1].default_value=.35
def obj(name,data):
 o=bpy.data.objects.new(name,data);s.collection.objects.link(o);return o
def aim(o,p):o.rotation_euler=(Vector(p)-o.location).to_track_quat('-Z','Y').to_euler()
def area(name,loc,target,power,color,sizex,sizey):
 ld=bpy.data.lights.new(name,'AREA');ld.energy=power*.42;ld.color=color;ld.shape='RECTANGLE';ld.size=sizex;ld.size_y=sizey
 o=obj(name,ld);o.location=loc;aim(o,target);return o
area('Broad satin key',(.8,-1.6,2.1),(1.1,0,0),320,(.80,.89,1),3.5,1.3)
area('Warm shoulder reflection',(1.7,1.1,1.2),(1.2,0,0),260,(1,.80,.60),3.2,.60)
area('Long edge reflection',(1.4,-.1,-1.4),(1.2,0,0),180,(.55,.76,1),3,.32)
area('Soft frontal fill',(-.1,-2,-.3),(.8,0,0),75,(.95,.97,1),2,2)
cd=bpy.data.cameras.new('S07 authored lens');cam=obj('S07 discovery camera',cd);s.camera=cam;cam.rotation_mode='QUATERNION';cd.lens=55;cd.clip_start=.01;cd.clip_end=150
focus=obj('Camera focus target',None);cd.dof.focus_object=focus;cd.dof.use_dof=True;cd.dof.aperture_fstop=8
def sm(t):t=max(0,min(1,t));return t*t*t*(t*(t*6-15)+10)
def span(f,a,b):return sm((f-a)/(b-a))
def pose(loc,target,roll):return (Vector(target)-Vector(loc)).to_track_quat('-Z','Y')@Quaternion((0,0,1),math.radians(roll))
# Starting close to the actual sensor shoulder; the glide reveals both twisted-pad regions.
near=Vector((.84,-.66,.31));near_target=Vector((.78,0,.015))
mid=Vector((1.20,-.88,.48));mid_target=Vector((1.36,0,0))
end_target=Vector((1.2,0,0));end=end_target+(Vector((.05,-3.6,2.05))-end_target)*1.58
endrot=pose(end,end_target,-48)
score=[]
for f in range(1,193):
 glide=span(f,1,86);pull=span(f,74,146)
 p=near.lerp(mid,glide).lerp(end,pull);target=near_target.lerp(mid_target,glide).lerp(end_target,pull)
 roll=-24-9*glide-15*pull
 cam.location=p;cam.rotation_quaternion=pose(p,target,roll);cd.shift_x=.16*pull;cd.shift_y=0
 focus.location=target;cd.dof.aperture_fstop=8+8*pull
 cam.keyframe_insert('location',frame=f);cam.keyframe_insert('rotation_quaternion',frame=f);cd.keyframe_insert('shift_x',frame=f);cd.dof.keyframe_insert('aperture_fstop',frame=f);focus.keyframe_insert('location',frame=f)
 score.append({'frame':f,'camera':list(p),'target':list(target),'roll_degrees':roll,'shift_x':cd.shift_x})
# Camera-space charcoal gradient; no invented studio architecture.
me=bpy.data.meshes.new('Studio cyclorama');me.from_pydata([(-40,-25,0),(40,-25,0),(40,25,0),(-40,25,0)],[],[(0,1,2,3)]);me.update()
bg=obj('Charcoal reflection field',me);bg.parent=cam;bg.location=(0,0,-30)
m=bpy.data.materials.new('Charcoal falloff');m.use_nodes=True;n=m.node_tree.nodes;n.clear();lk=m.node_tree.links
out=n.new('ShaderNodeOutputMaterial');em=n.new('ShaderNodeEmission');tex=n.new('ShaderNodeTexCoord');sep=n.new('ShaderNodeSeparateXYZ');ramp=n.new('ShaderNodeValToRGB')
ramp.color_ramp.elements[0].position=.2;ramp.color_ramp.elements[0].color=(.008,.012,.018,1)
ramp.color_ramp.elements[1].position=.8;ramp.color_ramp.elements[1].color=(.031,.043,.052,1)
lk.new(tex.outputs['Generated'],sep.inputs[0]);lk.new(sep.outputs['Y'],ramp.inputs[0]);lk.new(ramp.outputs[0],em.inputs[0]);lk.new(em.outputs[0],out.inputs['Surface']);me.materials.append(m)
# Independent editable closing labels, kept in a dedicated collection.
brand=bpy.data.collections.new('S07 EDITABLE BRANDING');s.collection.children.link(brand)
fontpath=Path('C:/Windows/Fonts/segoeuil.ttf');font=bpy.data.fonts.load(str(fontpath));font.pack()
def label(name,body,x,y,size):
 c=bpy.data.curves.new(name,'FONT');c.body=body;c.font=font;c.size=size;c.space_character=1.15
 o=bpy.data.objects.new(name,c);brand.objects.link(o);o.parent=cam;o['editable_brand_placeholder']=True
 for row in score:
  distance=(Vector(row['camera'])-Vector(row['target'])).length
  o.location=(x*distance,y*distance,-distance);o.scale=(distance,)*3
  o.keyframe_insert('location',frame=row['frame']);o.keyframe_insert('scale',frame=row['frame'])
 ma=bpy.data.materials.new(name+' fade');ma.use_nodes=True;n=ma.node_tree.nodes;n.clear();l=ma.node_tree.links
 out=n.new('ShaderNodeOutputMaterial');em=n.new('ShaderNodeEmission');em.inputs[0].default_value=(.78,.86,.91,1);tr=n.new('ShaderNodeBsdfTransparent');mx=n.new('ShaderNodeMixShader');ma.surface_render_method='BLENDED'
 l.new(tr.outputs[0],mx.inputs[1]);l.new(em.outputs[0],mx.inputs[2]);l.new(mx.outputs[0],out.inputs[0]);c.materials.append(ma)
 for f in range(1,193):mx.inputs[0].default_value=span(f,145,162);mx.inputs[0].keyframe_insert('default_value',frame=f)
 return o
# Camera visible width at distance1 is 36/55=.6545, height .3682.
label('Product identification','ECCO ENP3',.225,.018,.019)
label('MIT logo placeholder','MIT LOGO',.225,-.016,.011)
# Exact approved S06 ending, packed in the compositor; editorial dissolve only.
plate=R/'04-Production/Studies/S06_Report-Recreation_v004/Cache/polished/0288.png'
shutil.copy2(plate,B/'Graphics/S06_approved-ending.png')
ng=bpy.data.node_groups.new('S07 | Editorial handoff from approved S06','CompositorNodeTree')
ng.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor');s.compositing_node_group=ng
nodes=ng.nodes;links=ng.links
rl=nodes.new('CompositorNodeRLayers');rl.scene=s;im=nodes.new('CompositorNodeImage');im.image=bpy.data.images.load(str(B/'Graphics/S06_approved-ending.png'));im.image.pack()
blur=nodes.new('CompositorNodeBlur');blur.inputs['Type'].default_value='Gaussian'
recede=nodes.new('ShaderNodeMix');recede.data_type='RGBA';recede.blend_type='MIX';recede.inputs[7].default_value=(.009,.014,.020,1)
mix=nodes.new('ShaderNodeMix');mix.data_type='RGBA';mix.blend_type='MIX';output=nodes.new('NodeGroupOutput')
links.new(im.outputs['Image'],blur.inputs['Image']);links.new(blur.outputs['Image'],recede.inputs[6]);links.new(recede.outputs[2],mix.inputs[6]);links.new(rl.outputs['Image'],mix.inputs[7]);links.new(mix.outputs[2],output.inputs['Image'])
for f in range(1,193):
 recede.inputs[0].default_value=span(f,5,28);recede.inputs[0].keyframe_insert('default_value',frame=f)
 mix.inputs[0].default_value=span(f,15,39);mix.inputs[0].keyframe_insert('default_value',frame=f)
 blur.inputs['Size'].default_value=(24*span(f,4,29),24*span(f,4,29));blur.inputs['Size'].keyframe_insert('default_value',frame=f)
rl.location=(-400,-80);im.location=(-900,200);blur.location=(-670,200);recede.location=(-450,200);mix.location=(-200,80);output.location=(40,80)
for data in list(bpy.data.objects)+list(bpy.data.cameras)+list(bpy.data.materials)+[ng]:
 ad=getattr(data,'animation_data',None)
 if ad and ad.action:
  for layer in ad.action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for fc in bag.fcurves:
      for k in fc.keyframe_points:k.interpolation='LINEAR'
s['owner_authority']='S07 Full Cinematic Production handoff, 25 October 2026; 192f full previs'
s['source_geometry_sha256']=hashlib.sha256(SRC.read_bytes()).hexdigest();s['illustrative_limits']='Source scale preserved; temporary closures retained; satin finish is art direction. No field-data provenance claim. MIT LOGO is editable placeholder.'
s.frame_set(192)
bpy.ops.wm.save_as_mainfile(filepath=str(B/'Scenes/S07_Monumental-Precision_v001.blend'))
(B/'Records/camera-score.json').write_text(json.dumps(score,indent=2))
(B/'Records/build.json').write_text(json.dumps({'source':str(SRC),'source_sha256':s['source_geometry_sha256'],'s06_plate_sha256':hashlib.sha256(plate.read_bytes()).hexdigest(),'frames':192,'fps':24,'resolution':[1280,720],'geometry_policy':'Mesh vertices and topology unchanged; object material overrides only','product_motion':'Stationary','graphic_copy':['ECCO ENP3','MIT LOGO'],'render_engine':s.render.engine,'samples':s.eevee.taa_render_samples},indent=2))
print('S07 BUILT',flush=True)
