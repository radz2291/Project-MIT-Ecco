"""Run through official Blender MCP in preserved active rough scene. Shot-only binding."""
import bpy, re, json
from pathlib import Path
from mathutils import Vector
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco')
Q=R/'04-Production/Shots/S01-S02'; A=R/'04-Production/Shared/Assets'
s=bpy.context.scene
assert 'BHA sequence assembly' not in bpy.data.objects
product=bpy.data.objects['ECCO actual linked product']
baseline={}
for f in range(1,529):
 s.frame_set(f);baseline[f]={'camera':[list(r) for r in s.camera.matrix_world],'lens':s.camera.data.lens,'product':[list(r) for r in product.matrix_world]}

def linked(path,kind,names):
 with bpy.data.libraries.load(str(A/path),link=True) as (a,b):setattr(b,kind,names)
 return getattr(b,kind)

def stash(name,objects):
 c=bpy.data.collections.new(name);s.collection.children.link(c)
 for ob in objects:
  c.objects.link(ob)
  for prev in list(ob.users_collection):
   if prev!=c:prev.objects.unlink(ob)
 c.hide_viewport=True;c.hide_render=True
 return c

# The BHA master nests ECCO at identity. Preserve all existing product animation.
col=next((c for c in bpy.data.collections if c.name=='WORLD_HARDWARE' and c.library and 'BHA_film_v008' in c.library.filepath),None)
if col is None:col=linked('Hardware/BHA/BHA_film_v008.blend','collections',['WORLD_HARDWARE'])[0]
assembly=product.copy();assembly.name='BHA sequence assembly';assembly.instance_collection=col;s.collection.objects.link(assembly)
stash('REPLACED standalone product and original string',[product,bpy.data.objects['Drill string - axis']])
assembly['binding']='BHA v008 WORLD_HARDWARE, internal ECCO identity; inherited source action/slot unchanged.'
# Rebuild only the cylindrical continuation from the inspected collar endpoint x=-1.5.
old=bpy.data.objects['Drill string - axis'];me=old.data.copy();lo=min(v.co.z for v in me.vertices);hi=max(v.co.z for v in me.vertices)
for v in me.vertices:v.co.z=(v.co.z-lo)/(hi-lo)
string=bpy.data.objects.new('Sequence string connected above BHA',me);s.collection.objects.link(string)
for path,index,expr in [('location',2,'z+1.5'),('scale',2,'30-(z+1.5)')]:
 fc=string.driver_add(path,index);var=fc.driver.variables.new();var.name='z';var.type='TRANSFORMS';var.targets[0].id=assembly;var.targets[0].transform_type='LOC_Z';var.targets[0].transform_space='WORLD_SPACE';fc.driver.expression=expr

field=bpy.data.objects['WF_LIVE_FIELD'];group=field.modifiers[0].node_group
def val(m,name,value):
 ident=next(x.identifier for x in m.node_group.interface.items_tree if getattr(x,'in_out','')=='INPUT' and x.name==name)
 getattr(m.properties.inputs,ident).value=value
events=[]
for i in range(1,7):
 snd=bpy.data.objects[f'DW {i} SEND front0 core'];echo=bpy.data.objects[f'DW {i} ECHO front0 core']
 def window(ob):
  fs=[int(k.name[5:]) for k in ob.data.shape_keys.key_blocks if k.name.startswith('Frame')];return min(fs),max(fs)
 start,contact=window(snd);es,receipt=window(echo)
 s.frame_set(start);a=snd.matrix_world.translation.copy();b=bpy.data.objects[f'DW {i} fixed native contact pin'].matrix_world.translation.copy()
 assert .001<(b-a).length<.1
 ob=bpy.data.objects.new(f'WF sequence event {i}',field.data);s.collection.objects.link(ob);ob.location=a
 m=ob.modifiers.new('Shared waveform; local event binding','NODES');m.node_group=group
 axis=(b-a).normalized();up=Vector((0,0,1));depth=axis.cross(up).normalized()
 params={'Start Frame':float(start),'Duration Override':3.,'Travel Override':float(contact-start),'Return Travel Override':float(receipt-es),'Echo Delay Frames':float(es-contact),'Outbound End Frame':contact+.01,'Return End Frame':receipt+.01,'Lock Event Timing':1.,'Gap Length m':(b-a).length,'Route Axis':tuple(axis),'Transverse Axis':tuple(depth),'Up Axis':tuple(up),'Preset 0 Open 1 Cased':0,'Radius Override':3.}
 for n,v in params.items():val(m,n,v)
 ob.update_tag(refresh={'OBJECT','DATA','TIME'})
 events.append({'event':i,'object':ob.name,'start':start,'contact':contact,'echo_start':es,'receipt':receipt,'sensor':list(a),'wall':list(b),'settings':params})
 # Verify first and every subsequent cycle before retiring its old graphics.
 checks=[]
 for f in [start-1,start+3,es+2,receipt+2]:
  s.frame_set(f);ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=ev.to_mesh();checks.append([f,len(mesh.vertices)]);ev.to_mesh_clear()
 assert checks[0][1]==0 and checks[-1][1]==0 and checks[1][1]>0 and checks[2][1]>0,checks
 events[-1]['geometry_checks']=checks
 stash(f'REPLACED original waveform travel {i}',[o for o in list(s.objects) if o.name.startswith(f'DW {i} ') and ('SEND front' in o.name or 'ECHO front' in o.name)])

# Shared reveal is driven by this shot's existing local cell identities and history starts.
reveal,fine=linked('Effects/MeasurementReveal/Measurement_reveal_v001.blend','node_groups',['ECCO Stored Surface Reveal v001','ECCO Fine Surface Style v001'])
wall=bpy.data.objects['ONE WALL - old history and current cells share topology'];me=wall.data
for name in ['ecco_receipt_frame','ecco_reveal_order']:me.attributes.new(name,'FLOAT','FACE')
counts={'history':0,'current':0,'unrecorded':0,'settled':0}
for p in me.polygons:
 name=me.materials[p.material_index].name;history=re.search(r'start(\d+)',name);current=re.search(r'Unified cell (\d+)',name)
 if history:receipt=-2000;order=int(history[1])-1;counts['history']+=1
 elif current:receipt=events[int(current[1])-1]['receipt'];order=receipt;counts['current']+=1
 elif 'unrecorded' in name:receipt=100000;order=100001;counts['unrecorded']+=1
 else:receipt=-2000;order=-2000;counts['settled']+=1
 # Start=1, stagger=1: max(1,receipt+1)+order => preserve exact history starts.
 if current:order=0
 me.attributes['ecco_receipt_frame'].data[p.index].value=receipt
 me.attributes['ecco_reveal_order'].data[p.index].value=order
wrapper=bpy.data.node_groups.new('Sequence local wall reveal binding','GeometryNodeTree')
for side in ['INPUT','OUTPUT']:wrapper.interface.new_socket(name='Geometry',in_out=side,socket_type='NodeSocketGeometry')
wi=wrapper.nodes.new('NodeGroupInput');wo=wrapper.nodes.new('NodeGroupOutput');gn=wrapper.nodes.new('GeometryNodeGroup');gn.node_tree=reveal
gn.inputs['Start frame'].default_value=1;gn.inputs['Stagger frames'].default_value=1;gn.inputs['Settle frames'].default_value=10;gn.inputs['Arrival offset'].default_value=.0015
wrapper.links.new(wi.outputs[0],gn.inputs[0]);wrapper.links.new(gn.outputs[0],wo.inputs[0]);wall.modifiers.new('Shared reveal with shot-owned receipt data','NODES').node_group=wrapper
# Fine overlay follows the evaluated revealed wall, so it cannot precede receipt.
g=bpy.data.node_groups.new('Sequence shared fine revealed wall','GeometryNodeTree');g.interface.new_socket(name='Geometry',in_out='OUTPUT',socket_type='NodeSocketGeometry')
oi=g.nodes.new('GeometryNodeObjectInfo');oi.inputs['Object'].default_value=wall;oi.transform_space='ORIGINAL'
fn=g.nodes.new('GeometryNodeGroup');fn.node_tree=fine;fn.inputs['Point radius'].default_value=.00035;fn.inputs['Line radius'].default_value=.00012
out=g.nodes.new('NodeGroupOutput');g.links.new(oi.outputs['Geometry'],fn.inputs[0]);g.links.new(fn.outputs[0],out.inputs[0])
overlay=bpy.data.objects.new('Shared fine measurement display',bpy.data.meshes.new('Fine display carrier'));s.collection.objects.link(overlay);overlay.matrix_world=wall.matrix_world;overlay.modifiers.new('Linked fine display style','NODES').node_group=g
for f,v in baseline.items():
 s.frame_set(f)
 assert v['camera']==[list(r) for r in s.camera.matrix_world] and v['lens']==s.camera.data.lens
 assert v['product']==[list(r) for r in assembly.matrix_world]
s.name='S01-S02 shared integration v002';s.frame_set(305)
for lib in bpy.data.libraries:lib.filepath=bpy.path.abspath(lib.filepath)
p=Q/'Scenes/S01-S02_production_v002.blend';bpy.ops.wm.save_as_mainfile(filepath=str(p),relative_remap=False);bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(p))
(Q/'Notes/integration_v002.json').write_text(json.dumps({'scene':str(p),'events':events,'wall_faces':counts,'all_528_camera_and_assembly_matrices_preserved':True,'string_join':'Core collar x=-1.5 => source Z+1.5, top30m; source cylindrical string data normalized, local drivers.'},indent=2))
result={'saved':str(p),'events':len(events),'wall_faces':counts,'all_528_camera_and_assembly_matrices_preserved':True}
