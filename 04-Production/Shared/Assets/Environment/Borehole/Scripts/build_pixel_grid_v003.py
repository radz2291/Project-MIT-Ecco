"""Run against World_motion_grid_v002.blend in a separate Blender process."""
import bpy, math, json, hashlib
from pathlib import Path
B=Path(__file__).resolve().parents[1]
out=B/'World_motion_grid_v003.blend'
assert not out.exists()
g=bpy.data.node_groups['WORLD pixel guide controls v002']
g.name='WORLD pixel guide controls v003'
sock=g.interface.new_socket(name='Bore lengthwise spacing deg',in_out='INPUT',socket_type='NodeSocketFloat')
sock.default_value=90.;sock.min_value=30.;sock.max_value=180.
n=g.nodes;l=g.links;i=next(n for n in n if n.bl_idname=='NodeGroupInput')
axis=next(n for n in n if n.bl_idname=='GeometryNodeInputNamedAttribute' and n.inputs['Name'].default_value=='grid_axis')
maximum=next(n for n in n if n.bl_idname=='ShaderNodeMath' and n.operation=='MAXIMUM')
previous=maximum.inputs[0].links[0].from_socket
test=n.new('ShaderNodeMath');test.operation='COMPARE';l.new(axis.outputs['Attribute'],test.inputs[0]);test.inputs[1].default_value=4.
switch=n.new('GeometryNodeSwitch');switch.input_type='FLOAT';l.new(test.outputs[0],switch.inputs['Switch']);l.new(i.outputs['Bore lengthwise spacing deg'],switch.inputs['True']);l.new(previous,switch.inputs['False']);l.new(switch.outputs[0],maximum.inputs[0])
defaults={'Enabled':False,'Show cut faces':True,'Show seabed':True,'Show bore':True,'Depth spacing m':20.,'Radial spacing m':5.,'Seabed spacing m':10.,'Bore ring spacing m':4.,'Bore lengthwise spacing deg':90.}
for x in g.interface.items_tree:
 if getattr(x,'in_out','')=='INPUT' and x.name in defaults:x.default_value=defaults[x.name]
ctrl=bpy.data.objects.new('World pixel guide controls',None);bpy.context.scene.collection.objects.link(ctrl)
for k,v in {**defaults,'Line width px':1.2,'Line opacity':.8,'Stroke shade':.008}.items():ctrl[k]=v
records=[]
for ob in [o for o in bpy.context.scene.objects if o.name.startswith('WORLD_PIXEL')]:
 me=ob.data;axis=me.attributes['grid_axis'];co=me.attributes['grid_coordinate']
 for edge in me.edges:
  if round(axis.data[edge.index].value)==4:
   p=me.vertices[edge.vertices[0]].co
   co.data[edge.index].value=(round(math.degrees(math.atan2(p.z,p.y))/30)*30)%360
 me.update()
 for mod in ob.modifiers:
  if mod.type!='NODES':continue
  for x in g.interface.items_tree:
   if getattr(x,'in_out','')=='INPUT' and x.name in defaults:
    param=getattr(mod.properties.inputs,x.identifier);param.value=defaults[x.name]
    fc=param.driver_add('value');v=fc.driver.variables.new();v.name='control';v.type='SINGLE_PROP';v.targets[0].id=ctrl;v.targets[0].data_path='["'+x.name+'"]';fc.driver.expression='control'
 records.append({'object':ob.name,'vertices':len(me.vertices),'edges':len(me.edges),'faces':len(me.polygons)})
text=bpy.data.texts.new('v003 controls');text.write('Sparse bore preset:4m rings/90deg lengthwise lines; cut faces20m depth/5m radial. Master Enabled and three independent region switches. Run shared pixel_guides_viewport.py install() in shot for sidebar UI/export. No physical environment changes.\n')
setup=bpy.data.texts.new('START HERE — pixel guides')
setup.write("import bpy,types\nfrom pathlib import Path\np=Path(bpy.path.abspath('//Scripts/pixel_guides_viewport.py'))\nm=types.ModuleType('ecco_pixel_guides');exec(compile(p.read_text(),str(p),'exec'),m.__dict__)\nbpy.app.driver_namespace['ecco_pixel_module']=m;m.install()\n")
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True)
d={'native':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'predecessor':'World_motion_grid_v002.blend','node_group':g.name,'defaults':defaults,'records':records,'consumer':'S01-S02 production v006 only','renderer_script':'Scripts/pixel_guides_viewport.py','stroke':'Fixed screen pixels, no surface strips','source_world':'World_environment_v014.blend','status':'Owner-requested sparse cave/denser cut-face trial; not accepted or measured data'}
(B/'World_motion_grid_interface_v003.json').write_text(json.dumps(d,indent=2))
result={'saved':str(out),'defaults':defaults}
