import bpy,json,re,hashlib
from pathlib import Path
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');B=R/'04-Production/Shared/Assets/Environment/Borehole';D=R/'04-Production/Shared/Demos';T=R/'04-Production/Records/Tasks/T-055/Palette_v012';T.mkdir(exist_ok=True,parents=True)
bpy.context.preferences.filepaths.save_version=0
colors=[(.29,.265,.225,1),(.38,.325,.25,1),(.255,.25,.23,1),(.335,.295,.245,1),(.31,.28,.235,1),(.27,.26,.24,1),(.245,.225,.20,1)]
bpy.ops.wm.open_mainfile(filepath=str(B/'World_environment_v011.blend'),load_ui=False)
fingerprint=lambda: {o.name:hashlib.sha256(b''.join(__import__('struct').pack('fff',*v.co) for v in o.data.vertices)).hexdigest() for o in bpy.data.objects if o.type=='MESH'}
before=fingerprint();mats={}
for o in bpy.data.collections['WORLD_REGIONAL_DESCENT'].objects:
 m=re.match(r'REGIONAL_UNIT_(\d+)',o.name)
 if not m:continue
 i=int(m.group(1))-1
 if i not in mats:
  mat=bpy.data.materials.new('Geology v012 muted earth unit '+str(i+1));mat.diffuse_color=colors[i];mat.use_nodes=True
  n=mat.node_tree.nodes;l=mat.node_tree.links;bs=n.get('Principled BSDF');bs.inputs['Roughness'].default_value=.93
  tex=n.new('ShaderNodeTexCoord');noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=2.5;noise.inputs['Detail'].default_value=2
  l.new(tex.outputs['Object'],noise.inputs['Vector']);ramp=n.new('ShaderNodeValToRGB')
  ramp.color_ramp.elements[0].color=tuple(c*.83 for c in colors[i][:3])+(1,);ramp.color_ramp.elements[1].color=colors[i]
  l.new(noise.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs[0],bs.inputs['Base Color']);mats[i]=mat
 o.data.materials.clear();o.data.materials.append(mats[i])
wall=bpy.data.objects['WORLD_S02_PHYSICAL_CUTAWAY_MESH'];wall.data.materials.clear();wall.data.materials.append(mats[4])
assert before==fingerprint()
out=B/'World_environment_v012.blend';bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True,relative_remap=False)
meta=json.loads((B/'World_interface_v011.json').read_text());meta.update(version='v012',native=out.relative_to(R).as_posix(),native_sha256=hashlib.sha256(out.read_bytes()).hexdigest());meta['palette']={'colors_linear_rgba':colors,'intent':'Muted warm grey, brown and beige. Illustrative rock units, no target highlight. Host and exact local wall share unit5 material.'};(B/'World_interface_v012.json').write_text(json.dumps(meta,indent=2))
bpy.ops.wm.open_mainfile(filepath=str(D/'Surface_descent_demo_v002.blend'),load_ui=False)
for lib in list(bpy.data.libraries):
 if Path(lib.filepath).name=='World_environment_v011.blend':lib.filepath=str(out);lib.reload()
s=bpy.data.scenes['World — layered descent'];bpy.context.window.scene=s
for screen in bpy.data.screens:
 for area in screen.areas:
  if area.type=='VIEW_3D':
   area.spaces.active.shading.type='SOLID';area.spaces.active.shading.color_type='MATERIAL';area.spaces.active.region_3d.view_perspective='CAMERA'
demo=D/'Surface_descent_demo_v003.blend';bpy.ops.wm.save_as_mainfile(filepath=str(demo),compress=True,relative_remap=False);bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(demo),compress=True,relative_remap=False)
bpy.ops.wm.open_mainfile(filepath=str(demo),load_ui=False)
assert all(Path(bpy.path.abspath(l.filepath)).exists() for l in bpy.data.libraries)
(T/'verification.json').write_text(json.dumps({'geometry_unchanged':True,'links_resolve':True,'rendered':False,'world':str(out),'demo':str(demo),'palette':colors},indent=2))
print('READY',str(demo))
