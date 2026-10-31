import bpy,json,math,hashlib
from pathlib import Path
from mathutils import Vector
T=Path(__file__).resolve().parents[1];R=T.parents[3];A=R/'04-Production/Shared/Assets';D=T/'Demos'
bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene
s.name='Hardware | Shared assets review'
def linked_collection(path,name):
    with bpy.data.libraries.load(str(path),link=True) as (a,b):b.collections=[name]
    return b.collections[0]
ecco=linked_collection(A/'ECCO/ECCO_film_v003.blend','ECCO_FILM')
bha=linked_collection(A/'BHA/BHA_film_v008.blend','BHA_CONTINUITY_PREVIEW')
s.collection.children.link(bha)
over=bha.override_hierarchy_create(s,bpy.context.view_layer,do_fully_editable=True)
if bha.name in s.collection.children:s.collection.children.unlink(bha)
control=next(o for o in over.all_objects if o.name.startswith('UPHOLE_CONTINUATION_CONTROL'))
for key,value in [('show',0),('length_m',2.0)]:
    control.property_overridable_library_set('["'+key+'"]',True)
    control[key]=value
    prop=control.override_library.properties.add('["'+key+'"]');prop.operations.add('REPLACE')
# Both exhibits remain linked to their shared geometry and satin. Only the BHA
# control hierarchy is overridden locally, to expose the existing controls.
if over.name in s.collection.children:s.collection.children.unlink(over)
def exhibit(name,col,location):
    o=bpy.data.objects.new(name,None);o.instance_type='COLLECTION';o.instance_collection=col;o.location=location;s.collection.objects.link(o);return o
e=exhibit('ECCO | linked standalone',ecco,(0,0,1.1));b=exhibit('BHA | linked connected assembly',over,(0,0,-1.1))
def label(text,loc,size=.20):
    d=bpy.data.curves.new(text,'FONT');d.body=text;d.size=size;d.extrude=0;o=bpy.data.objects.new(text,d);s.collection.objects.link(o);o.location=loc;o.rotation_euler=(math.pi/2,0,0)
    m=bpy.data.materials.get('Demo lettering') or bpy.data.materials.new('Demo lettering');m.diffuse_color=(.55,.7,.8,1);d.materials.append(m)
label('ECCO  /  shared satin',(-.2,-.25,1.55));label('BHA  /  connected core',(-.2,-.25,-.55))
cd=bpy.data.cameras.new('Hardware review camera');cam=bpy.data.objects.new('Hardware review camera',cd);s.collection.objects.link(cam);s.camera=cam
cam.location=(1.2,-11,2.2);target=Vector((1.2,0,0));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cd.type='ORTHO';cd.ortho_scale=8.0;cd.clip_end=100
for name,loc,power,size in [('Broad key',(1,-4,5),1000,6),('Edge reflection',(1,2,4),1200,5),('Soft fill',(-3,-2,0),600,4)]:
    ld=bpy.data.lights.new(name,'AREA');ld.energy=power;ld.shape='DISK';ld.size=size;o=bpy.data.objects.new(name,ld);s.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector((1,0,0))-o.location).to_track_quat('-Z','Y').to_euler()
s.world=bpy.data.worlds.new('Review studio');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.045,.055,.07,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.3
s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=16;s.render.resolution_x=960;s.render.resolution_y=540;s.render.resolution_percentage=100
s.view_settings.view_transform='AgX';s.render.fps=24;s.frame_start=1;s.frame_end=1
s['review_instructions']='Two linked exhibits only. BHA source control override: UPHOLE_CONTINUATION_CONTROL, show 0/1 and length_m. Default show0;2m when enabled. Source masters untouched.'
s['shared_finish']='Linked ECCO | Satin finish v001; no copied finish node group.'
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type=='VIEW_3D':
            area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.shading.type='MATERIAL';area.spaces.active.overlay.show_overlays=False
bpy.ops.object.select_all(action='DESELECT');b.select_set(True);bpy.context.view_layer.objects.active=b
bpy.ops.wm.save_as_mainfile(filepath=str(D/'Hardware_demo_v001.blend'));bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
print('DEMO_SAVED',bpy.data.filepath,'CONTROL',control.name)
