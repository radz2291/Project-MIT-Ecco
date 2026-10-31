"""Focused linked World and Surface demos; preserves all source libraries."""
import bpy,pathlib,json,math,time,hashlib
from mathutils import Vector
R=pathlib.Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');T=R/'04-Production/Records/Tasks/T-051';D=T/'Demos';D.mkdir(exist_ok=True)
outputs=[]
def camera(scene,name,pos,target,scale):
 data=bpy.data.cameras.new(name);ob=bpy.data.objects.new(name,data);scene.collection.objects.link(ob);ob.location=pos;ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler();data.type='ORTHO';data.ortho_scale=scale;scene.camera=ob
def settings(s):
 s.render.engine='BLENDER_WORKBENCH';s.render.resolution_x=640;s.render.resolution_y=360;s.render.resolution_percentage=100;s.display.shading.light='STUDIO';s.display.shading.color_type='MATERIAL';s.display.shading.show_shadows=True;s.display.shading.show_cavity=True;s.render.fps=24
def build(kind,source,colname,views):
 bpy.ops.wm.read_factory_settings(use_empty=True);p=R/source;before=hashlib.sha256(p.read_bytes()).hexdigest()
 with bpy.data.libraries.load(str(p),link=True) as (a,b):b.collections=[colname]
 col=b.collections[0]
 for i,(name,pos,target,scale) in enumerate(views):
  s=bpy.context.scene if i==0 else bpy.data.scenes.new(name);s.name=name;s.collection.children.link(col);settings(s);camera(s,name+' camera',pos,target,scale)
  if kind=='Surface':
   me=bpy.data.meshes.new('Demo seabed');me.from_pydata([(-40,-40,-120),(40,-40,-120),(40,40,-120),(-40,40,-120)],[],[(0,1,2,3)]);o=bpy.data.objects.new('DEMO ONLY seabed reference',me);s.collection.objects.link(o)
  if kind=='World':
   s.display.shading.color_type='SINGLE';s.display.shading.single_color=(.65,.65,.65);s.display.shading.show_shadows=False
  if (kind=='Surface' and i==0) or (kind=='World' and i==1):
   rot=s.camera.rotation_euler.to_matrix().transposed();pts=[rot@(o.matrix_world@Vector(v)) for o in col.all_objects if o.type=='MESH' for v in o.bound_box]
   lo=Vector(tuple(min(p[k] for p in pts) for k in range(3)));hi=Vector(tuple(max(p[k] for p in pts) for k in range(3)));mid=(lo+hi)/2
   s.camera.location+=s.camera.rotation_euler.to_matrix()@Vector((mid.x-(rot@s.camera.location).x,mid.y-(rot@s.camera.location).y,0));s.camera.data.ortho_scale=max(hi.x-lo.x,(hi.y-lo.y)*640/360)*1.15
  for area in bpy.context.screen.areas:
   if area.type=='VIEW_3D':area.spaces.active.region_3d.view_perspective='CAMERA'
 bpy.context.window.scene=bpy.data.scenes[views[0][0]]
 txt=bpy.data.texts.new('README — '+kind+' demo');txt.write('DEMO ONLY. Linked shared master: '+source+'\nUse the scene dropdown for '+', '.join(x[0] for x in views)+'.\nThe shared asset is editable in its source library. Camera/framing and seabed reference belong only to this demo. No section camera, measurement dataset or production timeline is included.\n'+('Choose other World variants in the shared master; do not stack competing full/cutaway variants. Authored previs geometry.\n' if kind=='World' else 'Surface master includes the approved illustrative camera-access opening; equipment dimensions are previs adaptations.\n'))
 out=D/(kind+'_demo_v001.blend');bpy.ops.wm.save_as_mainfile(filepath=str(out));bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(out));assert hashlib.sha256(p.read_bytes()).hexdigest()==before
 outputs.append({'path':str(out.relative_to(R)),'source':source,'source_sha256':before,'scenes':[x[0] for x in views],'sha256':hashlib.sha256(out.read_bytes()).hexdigest()})
build('World','04-Production/Shared/Assets/WellAssembly/World_environment_v010.blend','WORLD_FORMATION_IRREGULAR_CUTAWAY',[('World — borehole detail',(0,-4,0),(0,0,0),2),('World — outer extent',(30,-40,35),(0,0,0),58)])
build('Surface','04-Production/Shared/Assets/Surface/Surface_descent_v005.blend','SURFACE_RIG_SUBSEA_v004',[('Surface — assembly overview',(200,-280,100),(0,0,-35),190),('Surface — subsea detail',(12,-18,-108),(0,0,-118),19)])
(T/'Evidence/environment-demo-build.json').write_text(json.dumps(outputs,indent=2));print(json.dumps(outputs))
