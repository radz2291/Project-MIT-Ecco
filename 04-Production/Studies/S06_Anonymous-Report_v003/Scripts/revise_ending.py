"""Targeted final-three-second replacement. Original v002 camera/data preserved through f216."""
import bpy,math,json
from pathlib import Path
from mathutils import Vector
B=Path(__file__).resolve().parents[1];BASE=B.with_name('S06_Sculpted-Information_v002')
bpy.ops.wm.open_mainfile(filepath=str(BASE/'Scenes/S06_cinematic-study_v002.blend'))
s=bpy.context.scene;cam=s.camera;s.frame_set(216)
camloc=cam.location.copy();camrot=cam.rotation_quaternion.copy();lens=cam.data.lens
keep=('Recorded geometry','Registration','Seam','Measured section','Source status','Sequence identity')
for ob in list(s.objects):
    if ob.type not in ('LIGHT','CAMERA') and not ob.name.startswith(keep):bpy.data.objects.remove(ob,do_unlink=True)
old=list(s.objects)
for ob in old:
    if ob.type in ('MESH','CURVE','FONT'):
        # Existing HUD render keys removed; preserve its original visible state through f216.
        if ob.type=='FONT':
            ob.animation_data_clear()
        ob.hide_render=False;ob.keyframe_insert('hide_render',frame=216)
        for f in range(229,289):
            ob.hide_render=True;ob.keyframe_insert('hide_render',frame=f)
# Keep the same camera until the revised ending; only a very small dolly afterward.
for f in range(217,289):
    t=(f-217)/71;u=t*t*(3-2*t)
    cam.location=camloc+Vector((0,-.035*u,0));cam.rotation_quaternion=camrot;cam.data.lens=lens
    cam.keyframe_insert('location',frame=f);cam.keyframe_insert('rotation_quaternion',frame=f);cam.data.keyframe_insert('lens',frame=f)

def ease(t):t=max(0,min(1,t));return t*t*(3-2*t)
created=[];mats=[]
def material(name,color,image=None,phase='report'):
    ma=bpy.data.materials.new(name);ma.use_nodes=True;n=ma.node_tree.nodes;n.clear();l=ma.node_tree.links
    em=n.new('ShaderNodeEmission');em.inputs[0].default_value=(*color,1)
    if image:
        tex=n.new('ShaderNodeTexImage');tex.image=image;tex.interpolation='Linear';l.new(tex.outputs['Color'],em.inputs[0])
    tr=n.new('ShaderNodeBsdfTransparent');mx=n.new('ShaderNodeMixShader');mx.name='ENDING_REVEAL';out=n.new('ShaderNodeOutputMaterial')
    l.new(tr.outputs[0],mx.inputs[1]);l.new(em.outputs[0],mx.inputs[2]);l.new(mx.outputs[0],out.inputs[0]);ma.surface_render_method='BLENDED'
    for f in range(216,289):
        value=ease((f-217)/11) if phase=='bridge' else ease((f-231)/14)
        mx.inputs[0].default_value=value;mx.inputs[0].keyframe_insert('default_value',frame=f)
    mats.append(ma);return ma
def register(ob):
    s.collection.objects.link(ob);ob.parent=cam;created.append(ob)
    ob.hide_render=True;ob.keyframe_insert('hide_render',frame=216)
    ob.hide_render=False;ob.keyframe_insert('hide_render',frame=217)
    return ob
def panel(name,x0,x1,y0,y1,z,ma):
    me=bpy.data.meshes.new(name);me.from_pydata([(x0,y0,z),(x1,y0,z),(x1,y1,z),(x0,y1,z)],[],[(0,1,2,3)])
    uv=me.uv_layers.new(name='Crop UV')
    for loop,co in zip(uv.data,[(0,0),(1,0),(1,1),(0,1)]):loop.uv=co
    me.materials.append(ma);return register(bpy.data.objects.new(name,me))
font=next(f for f in bpy.data.fonts if f.name!='Bfont' and f.filepath)
def text(name,body,x,y,size,ma):
    cu=bpy.data.curves.new(name,'FONT');cu.font=font;cu.body=body;cu.size=size;cu.materials.append(ma)
    ob=register(bpy.data.objects.new(name,cu));ob.location=(x,y,-1.985);return ob
navy=material('Neutral transition',(.00225,.004,.00625),phase='bridge')
panel('Separate-example transition',-.76,.76,-.45,.45,-2.04,navy)
paper=material('Anonymous report paper',(.88,.90,.91));ink=material('Editorial ink',(.025,.055,.08));secondary=material('Editorial secondary',(.16,.23,.28))
panel('Anonymous editorial frame',-.645,.645,-.335,.34,-2.015,paper)
text('Neutral editorial title','Engineering output',-.59,.265,.031,ink)
text('Explicit dataset boundary','Separate report example',.26,.275,.015,secondary)
text('Anonymous status','ANONYMOUS GRAPHIC EXCERPTS',-.589,.225,.011,secondary)
# Keep native crop aspect ratios; panels are graphic fragments, not a calibrated report.
height=.45;ratios={'profile':67/228,'sections':114/245,'shape':97/228,'geometry':89/228,'amplitude':89/228}
names=list(ratios);gap=.025;total=height*sum(ratios.values())+gap*(len(names)-1);x=-total/2
placements=[]
for name in names:
    w=height*ratios[name];im=bpy.data.images.load(str(B/f'Media/{name}.png'),check_existing=False);im.name='Anonymous '+name;im.pack()
    ma=material('Source excerpt '+name,(1,1,1),im)
    ob=panel('Anonymous graphic '+name,x,x+w,-.257,.193,-2.005,ma)
    ob['source_status']='Cropped report graphics; source text removed; separate example from unfolding'
    placements.append({'panel':name,'xy_bounds':[x,x+w,-.257,.193],'aspect_preserved':True});x+=w+gap
text('Evidence boundary','Graphic excerpts from an existing report; not the preceding illustrative dataset.',-.589,-.298,.0125,secondary)
for action in bpy.data.actions:
    for layer in action.layers:
        for strip in layer.strips:
            for bag in strip.channelbags:
                for fc in bag.fcurves:
                    if fc.data_path=='hide_render':
                        for k in fc.keyframe_points:k.interpolation='CONSTANT'
s.name='S06 v003 | Anonymous report ending'
s['scope']='Owner Option C ending revision; real graphic excerpts; no source text or dataset continuity claim'
s['source_data']='//../../S06_Sculpted-Information_v002/Data/surface_samples.npz'
s.frame_set(1);bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=str(B/'Scenes/S06_cinematic-study_v003.blend'),relative_remap=False)
(B/'Records/ending-layout.json').write_text(json.dumps({'base':'S06 cinematic study v002','unchanged_frames':[1,216],'changed_frames':[217,288],'timing':'9.0-9.5s illustrative map fades to neutral; 9.6-10.2s separate anonymous report appears; hold to 12s','neutral_labels_only':True,'full_source_page_packed':False,'panels':placements},indent=2),encoding='utf-8')
print('ENDING READY')
