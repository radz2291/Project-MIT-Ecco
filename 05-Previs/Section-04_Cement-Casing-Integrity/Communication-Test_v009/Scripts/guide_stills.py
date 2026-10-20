import bpy,json,math
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
B=Path(__file__).resolve().parents[1]
for case in 'BC':
 bpy.ops.wm.open_mainfile(filepath=str(B/'Scenes'/f'S04_{case}_formation-acquisition_v009.blend'),use_scripts=False,load_ui=False);s=bpy.context.scene;s.frame_set(25);cam=s.camera
 e=json.loads((B/'Records'/f'build-{case}.json').read_text())['event'];src=Vector(e['emitter_world_m']);hit=Vector(e['hit_world_m']);rad=Vector(e['direction_world']);tan=Vector((0,-rad.z,rad.y));xc=hit.x
 W=.01*cam.data.sensor_width/cam.data.lens;H=W*720/1280
 m=bpy.data.materials.new('Guide white');m.diffuse_color=(1,1,1,1);c=bpy.data.materials.new('Guide pointer');c.diffuse_color=(.8,.95,1,1)
 def pt(u,v):return cam.matrix_world@Vector(((u-.5)*W,(v-.5)*H,-.01))
 def text(body,u,v,size=23):
  d=bpy.data.curves.new(body,'FONT');d.body=body;d.size=H*size/720;o=bpy.data.objects.new(body,d);s.collection.objects.link(o);o.location=pt(u,v);o.rotation_euler=cam.matrix_world.to_euler();d.materials.append(m)
 def arrow(u,v,world):
  q=world_to_camera_view(s,cam,world);a=Vector((u,v));b=Vector((q.x,q.y));di=(a-b).normalized();side=Vector((-di.y,di.x));coords=[a,b,b+di*.012+side*.005,b,b+di*.012-side*.005]
  d=bpy.data.curves.new('Guide pointer','CURVE');d.dimensions='3D';d.bevel_depth=H*.001;sp=d.splines.new('POLY');sp.points.add(len(coords)-1)
  for p,uv in zip(sp.points,coords):p.co=(*pt(*uv),1)
  o=bpy.data.objects.new('Guide pointer',d);s.collection.objects.link(o);d.materials.append(c)
 text('B — CEMENT BACKING' if case=='B' else 'C — EXTERIOR FLUID CHANNEL',.025,.945,29)
 text('Solid cement' if case=='B' else 'Fluid where cement is absent',.035,.78,22);arrow(.23,.75,Vector((xc,0,0))+rad*.195+tan*.00011)
 text('Rock formation',.025,.55,22);arrow(.16,.51,Vector((xc,0,0))+rad*.29+tan*.0001)
 text('STEEL WALL',.31,.15,24);arrow(.43,.20,Vector((xc,0,0))+rad*.164+tan*.00013)
 text('Internal fluid gap',.40,.80,22);arrow(.54,.76,Vector((xc+.015,0,0))+rad*.145+tan*.00012)
 text('ECCO side sensor',.73,.67,23);arrow(.76,.63,src)
 text('Same physical section and camera as the video. Only labels added.',.025,.065,19)
 text('Illustrative geometry / slowed acoustic visualization — not field data',.025,.025,17)
 s.render.filepath=str(B/'Previews'/f'S04_{case}_material-guide_v009.png');bpy.ops.render.render(write_still=True)
