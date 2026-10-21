import bpy,sys,time,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from build import convert,light,section
B=Path(__file__).resolve().parents[1];P=B.parent
mode=sys.argv[sys.argv.index('--')+1]
if mode=='build':
 bpy.ops.wm.open_mainfile(filepath=str(B/'Scenes/S04_continuous-camera_v019.blend'),use_scripts=False,load_ui=False)
 lights=[(o.name,list(o.location),o.data.energy,o.data.size) for o in bpy.context.scene.objects if o.type=='LIGHT' and not o.hide_render]
 bpy.ops.wm.open_mainfile(filepath=str(P/'Cinematic-Previs_v018/Scenes/S04_C_v018.blend'),use_scripts=False,load_ui=False);s=bpy.context.scene;s.name='C reduced-backing comparison window v019'
 for m in list(bpy.data.materials):
  if not m.library:convert(m)
 with bpy.data.libraries.load(str(B/'Scenes/S04_continuous-camera_v019.blend'),link=False) as (a,b):b.materials=['Continuous steel - fixed computed wear values v019']
 steel=bpy.data.objects['STEEL - capped true source section'];steel.data=bpy.data.objects['CASED_STEEL_WEAR_FULL'].data.copy();section(steel);steel.data.materials.clear();steel.data.materials.append(b.materials[0])
 for p in steel.data.polygons:p.material_index=0;p.use_smooth=abs(p.normal.dot(__import__('build').N))<.99
 for o in s.objects:
  if o.type=='LIGHT':o.hide_render=True
 for name,pos,power,size in lights:
  pos[0]-=1.18;light(name+' C',pos,(-1.5,.10,0),power,size)
 s.world=s.world.copy();s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.22,.27,.32,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.65
 s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=4;s.eevee.use_raytracing=False;s.render.use_compositing=False;s.view_settings.view_transform='AgX';s.view_settings.look='AgX - Medium High Contrast';s.view_settings.exposure=-.4;s.render.image_settings.compression=10
 for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(B/'Scenes'))
 bpy.ops.wm.save_as_mainfile(filepath=str(B/'Scenes/S04_C_comparison-window_v019.blend'),relative_remap=False)
else:
 bpy.ops.wm.open_mainfile(filepath=str(B/'Scenes/S04_C_comparison-window_v019.blend'),use_scripts=False,load_ui=False);s=bpy.context.scene;rows=[]
 folder=B/('Previews' if mode=='bench' else 'Work/C');folder.mkdir(exist_ok=True)
 for f in ([1,35,78] if mode=='bench' else range(1,121)):
  s.frame_set(f);s.render.filepath=str(folder/f'C_{f:04d}.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t;rows.append({'frame':f,'seconds':dt});(B/'Records'/('timings-C-'+mode+'.json')).write_text(json.dumps(rows,indent=2));print('C FRAME',f,dt,flush=True)
  if dt>=5:raise RuntimeError('Frame cap reached')
