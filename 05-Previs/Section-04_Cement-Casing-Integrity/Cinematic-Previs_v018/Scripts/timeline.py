import bpy,json
from pathlib import Path
B=Path(__file__).resolve().parents[1]
bpy.ops.wm.read_factory_settings(use_empty=True)
s=bpy.context.scene;s.name='S04 complete cinematic previs v018';s.frame_start=1;s.frame_end=432;s.render.fps=24
s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100
s.render.image_settings.file_format='PNG';s.view_settings.view_transform='Standard'
editor=s.sequence_editor_create()
for title,start,end in [('A - upward casing entry',1,96),('B+C - matched 50-50 response',97,264),('D - physical wear and computed loss',265,432)]:
 strip=editor.strips.new_image(title,str(B/'Work/Assembly'/f'S04_{start:04d}.png'),channel=1,frame_start=start)
 for f in range(start+1,end+1):strip.elements.append(f'S04_{f:04d}.png')
 strip.directory='//../Work/Assembly/'
 strip['native_scene_sources']='S04_A_v018.blend / S04_B_v018.blend / S04_C_v018.blend / S04_D_v018.blend'
for f,title in [(1,'A: upward entry'),(97,'B/C: same composition, two fixed locations'),(121,'Send/contact/response/return'),(265,'D: physical wear'),(292,'Reference then worn profile'),(342,'Computed depth exposure'),(396,'Final data hold')]:s.timeline_markers.new(title,frame=f)
s['scope']='18-second inexpensive previs, owner released all approved parts. Illustrative geometry and response, not field data. Native editable 3D sources accompany editorial timeline.'
s['sources']='A v006 entry, B/C v009, D v017. Same approved physical geometry; camera framing and staged graphic visibility in v018.'
s.frame_set(182)
for w in bpy.context.window_manager.windows:
 for area in w.screen.areas:
  if area.type=='VIEW_3D':area.type='SEQUENCE_EDITOR';area.spaces.active.view_type='SEQUENCER_PREVIEW'
bpy.ops.wm.save_as_mainfile(filepath=str(B/'Scenes/S04_cinematic-previs_v018.blend'))
# Reopen saved timeline and verify local media and all editorial durations.
bpy.ops.wm.open_mainfile(filepath=str(B/'Scenes/S04_cinematic-previs_v018.blend'),use_scripts=False)
s=bpy.context.scene;items=[]
for strip in s.sequence_editor.strips:
 paths=[Path(bpy.path.abspath(strip.directory))/e.filename for e in strip.elements]
 assert all(p.is_file() for p in paths)
 items.append({'name':strip.name,'start':strip.frame_final_start,'end_exclusive':strip.frame_final_end,'elements':len(paths),'all_files_exist':True})
assert sum(i['elements'] for i in items)==432
(B/'Records/timeline-verification.json').write_text(json.dumps({'reopened':True,'strips':items,'duration_frames':432},indent=2))
