import bpy,json,re
from pathlib import Path
R=Path(__file__).resolve().parents[5];T=R/'04-Production/Records/Tasks/T-054';A=R/'04-Production/Shared/Assets'
src=next(x for x in json.loads((R/'04-Production/Records/Tasks/T-050/sources.json').read_text()) if x['id']=='S02')
bpy.ops.wm.open_mainfile(filepath=str(R/src['native']),load_ui=False)
o=bpy.data.objects['ONE WALL - old history and current cells share topology'];me=o.data
for name in ['ecco_receipt_frame','ecco_reveal_order']:me.attributes.new(name,'FLOAT','FACE')
starts=[]
for p in me.polygons:
 name=me.materials[p.material_index].name;match=re.search(r'start(\d+)',name)
 start=int(match.group(1)) if match else -1000
 me.attributes['ecco_receipt_frame'].data[p.index].value=318 if match else -2000
 me.attributes['ecco_reveal_order'].data[p.index].value=start-442
 if match:starts.append(start)
with bpy.data.libraries.load(str(A/'MeasurementReveal/Measurement_reveal_v001.blend'),link=True) as (a,b):b.node_groups=['ECCO Stored Surface Reveal v001']
g=b.node_groups[0];m=o.modifiers.new('Shared stagger settle; local cell timing','NODES')
wrapper=bpy.data.node_groups.new('S02 local reveal parameters','GeometryNodeTree')
wrapper.interface.new_socket(name='Geometry',in_out='INPUT',socket_type='NodeSocketGeometry');wrapper.interface.new_socket(name='Geometry',in_out='OUTPUT',socket_type='NodeSocketGeometry')
wi=wrapper.nodes.new('NodeGroupInput');wo=wrapper.nodes.new('NodeGroupOutput');gn=wrapper.nodes.new('GeometryNodeGroup');gn.node_tree=g
gn.inputs['Start frame'].default_value=442;gn.inputs['Arrival offset'].default_value=.0015
wrapper.links.new(wi.outputs[0],gn.inputs[0]);wrapper.links.new(gn.outputs[0],wo.inputs[0]);m.node_group=wrapper
o['shared_reveal']='Exact source start material names drive face order; active row left to original local receipt/alpha. Stored display begins442 after existing acquisition318. Camera/data unchanged.'
bpy.ops.wm.save_as_mainfile(filepath=str(T/'Consumers/S02_shared-reveal_v001.blend'));bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
(T/'Evidence/s02-reveal-mapping.json').write_text(json.dumps({'baseline':src['native'],'candidate':'04-Production/Records/Tasks/T-054/Consumers/S02_shared-reveal_v001.blend','first_stored':min(starts),'last_stored':max(starts),'receipt_reference':318,'source_material_count':len(me.materials),'preserved':'source materials, original opacity/color keyframes, active acquisition row, geometry coordinates and topology, camera and timing'},indent=2))
print('S02_ADAPTER_DONE')
