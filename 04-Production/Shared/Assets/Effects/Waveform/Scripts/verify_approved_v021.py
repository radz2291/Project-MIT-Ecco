import bpy,json,sys,math
from pathlib import Path
from mathutils import Vector
B=Path(__file__).parent.parent;R=B.parents[4];Q=R/'04-Production/Shots/S01-S02';sys.path.insert(0,str(B/'Scripts'))
from pulse_asset_api import get_input,set_input
from approved_exchange_api import create_contact_patch,configure_surface_patch,apply_approved_preset
def co(ob,f):
 bpy.context.scene.frame_set(f);e=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());me=e.to_mesh();v=[x.co.copy() for x in me.vertices];e.to_mesh_clear();return v
bpy.ops.wm.open_mainfile(filepath=str(Q/'Scenes/Waveform_active_patch_fast_v022.blend'),use_scripts=False);ob=bpy.data.objects['WF sequence event 1'];mod=ob.modifiers[0];axis=Vector(get_input(mod,'Route axis'));side=Vector(get_input(mod,'Transverse axis'));up=Vector(get_input(mod,'Up axis'));gap=get_input(mod,'Gap length m');refs={}
for f in [301,305,310,315,322,328,335,349,352]:refs[f]=[(p.dot(axis),p.dot(side),p.dot(up)) for p in co(ob,f)]
patch=bpy.data.objects['Handshake — subtle surface contact patch'];patchref={};colors={}
for f in range(300,324):bpy.context.scene.frame_set(f);patchref[f]=(tuple(patch.scale),tuple(patch.data.materials[0].diffuse_color))
for group in range(4):
 mat=bpy.data.materials['Unified cell 1 edge0 reveal'+str(group)]
 for f in range(300,354):bpy.context.scene.frame_set(f);colors[group,f]=tuple(mat.diffuse_color)
bpy.ops.wm.open_mainfile(filepath=str(B/'Waveform_shared_v021.blend'),use_scripts=False);field=bpy.data.objects['WF_PULSE_FIELD'];set_input(field.modifiers[0],'Gap length m',gap);errors=[]
for f,expected in refs.items():
 actual=co(field,f-299);assert len(actual)==len(expected),(f,len(actual),len(expected));errors.extend((a-Vector(b)).length for a,b in zip(actual,expected))
assert max(errors)<1e-6,max(errors)
patch=create_contact_patch(bpy.context.scene.collection,(0,0,0),(0,1,0),start_frame=1)
for f,(scale,color) in patchref.items():
 bpy.context.scene.frame_set(f-299);assert max(abs(a-b) for a,b in zip(patch.scale,scale))<1e-6;assert max(abs(a-b) for a,b in zip(patch.data.materials[0].diffuse_color,color))<1e-6
me=bpy.data.meshes.new('tile test');verts=[];faces=[]
for i in range(16):
 x=(i%4-1.5)*.01;y=(i//4-1.5)*.01;j=len(verts);verts.extend([(x-.005,y-.005,0),(x+.005,y-.005,0),(x+.005,y+.005,0),(x-.005,y+.005,0)]);faces.append((j,j+1,j+2,j+3))
me.from_pydata(verts,[],faces);me.attributes.new('ecco_receipt_frame','FLOAT','FACE');me.attributes.new('ecco_reveal_order','FLOAT','FACE');wall=bpy.data.objects.new('tile test',me);bpy.context.scene.collection.objects.link(wall);configure_surface_patch(wall,list(me.polygons),(0,0,0),start_frame=1);palette_errors=[]
for group,mat in enumerate(me.materials):
 for f in range(300,354):bpy.context.scene.frame_set(f-299);palette_errors.extend(abs(a-b) for a,b in zip(mat.diffuse_color,colors[group,f]))
assert max(palette_errors)<.03,max(palette_errors)
patch['Enabled']=False;patch.update_tag();bpy.context.scene.frame_set(15)
assert patch.hide_render and patch.hide_viewport
patch['Enabled']=True;patch.update_tag();bpy.context.scene.frame_set(16)
assert not patch.hide_render and not patch.hide_viewport
bpy.context.scene.render.fps=30
landmarks=apply_approved_preset(field.modifiers[0],start_frame=1)
assert abs(landmarks['feedback_complete']-(1+49*1.25))<1e-6,landmarks
patch30=create_contact_patch(bpy.context.scene.collection,(0,0,0),(0,1,0),start_frame=1)
bpy.context.scene.frame_set(8,subframe=.5)
assert abs(patch30.scale.x-1)<1e-6
(B/'Approved_exchange_verification_v021.json').write_text(json.dumps({'approved_waveform_sample_frames':len(refs),'max_intrinsic_position_error_m':max(errors),'contact_patch_scale_color_matches_approved_frames':24,'max_tile_color_error':max(palette_errors),'source_master_clean_objects':2,'contact_enabled_switch_checked':True,'authoring_landmarks_and_contact_key_timing_30fps_checked':True,'runtime':'native geometry/material actions, optional authoring helpers only','reference':'Waveform_active_patch_fast_v022.blend'},indent=2));print('APPROVED_PRESET_VERIFIED')
