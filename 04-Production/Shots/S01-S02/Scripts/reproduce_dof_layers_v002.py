"""Replay the researched ONE-FRAME layered camera proof; not a shot build."""
import bpy,time,json
from pathlib import Path
Q=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/Shots/S01-S02');P=Q/'Previews/DOF-investigation-v002'
assert bpy.data.filepath.endswith('S01-S02_DOF_investigation_v002.blend')
s=bpy.context.scene;assert s.frame_current==386,'Proof visibility is frozen at386; not valid for animation.'
c=s.camera;wall=bpy.data.objects['ONE WALL - old history and current cells share topology'];fine=bpy.data.objects['Shared fine measurement display'];flags={o.name:o.hide_render for o in s.objects}
c.data.dof.use_dof=True;c.data.dof.aperture_fstop=64;times=[]
try:
 for name,foreground in [('separate_base',False),('separate_measurement',True)]:
  for o in s.objects:o.hide_render=(o not in [wall,fine,c]) if foreground else (True if o in [wall,fine] else flags[o.name])
  s.render.film_transparent=foreground;s.render.filepath=str(P/(name+'.png'));t=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t;times.append(dt);assert dt<5
finally:
 for o in s.objects:o.hide_render=flags[o.name]
 s.render.film_transparent=False
result={'frame':386,'size':[s.render.resolution_x,s.render.resolution_y],'pass_seconds':times,'production_modified':False}
