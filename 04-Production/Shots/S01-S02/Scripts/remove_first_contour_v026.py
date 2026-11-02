"""Omit the owner's marked bottom contour; retain all later rings and timing."""
import bpy,json,hashlib,time,sys,datetime
from pathlib import Path
Q=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/Shots/S01-S02')
assert bpy.data.filepath.endswith('S01-S02_production_v025.blend')
out=Q/'Scenes/S01-S02_production_v026.blend';assert not out.exists()
if bpy.data.is_dirty:bpy.ops.wm.save_as_mainfile(filepath=str(Q/'Scenes'/('Before_v026_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S')+'.blend')),copy=True,compress=True)
ob=bpy.data.objects['Shared fine measurement display']
def contours():
 bpy.context.scene.frame_set(756);ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();rows=[]
 for p in m.polygons:
  mat=m.materials[p.material_index]
  if mat and (mat.name=='Unified wall pale major contours' or mat.name.startswith('Contour soft build')):
   rows.append(sum(m.vertices[i].co.z for i in p.vertices)/len(p.vertices))
 ev.to_mesh_clear();return rows
before=contours();wrapper=ob.modifiers[0].node_group.copy();ob.modifiers[0].node_group=wrapper
groupnode=next(n for n in wrapper.nodes if n.type=='GROUP');g=groupnode.node_tree.copy();groupnode.node_tree=g;g.name='S01-S02 contours without first boundary v026'
mtc=g.nodes['Mesh to Curve.001'];selection=mtc.inputs['Selection'].links[0].from_socket
wall=bpy.data.objects['ONE WALL - old history and current cells share topology'];bottom=min(v.co.z for v in wall.data.vertices);threshold=bottom+.12
pos=g.nodes.new('GeometryNodeInputPosition');sep=g.nodes.new('ShaderNodeSeparateXYZ');g.links.new(pos.outputs['Position'],sep.inputs[0])
gate=g.nodes.new('ShaderNodeMath');gate.operation='GREATER_THAN';gate.label='Skip first bottom contour';gate.inputs[1].default_value=threshold;g.links.new(sep.outputs['Z'],gate.inputs[0])
mask=g.nodes.new('ShaderNodeMath');mask.operation='MULTIPLY';mask.label='Later contours only';g.links.new(selection,mask.inputs[0]);g.links.new(gate.outputs[0],mask.inputs[1]);g.links.new(mask.outputs[0],mtc.inputs['Selection'])
ob['First boundary contour omitted']=True;ob.update_tag();bpy.context.view_layer.update();after=contours()
old_later=[z for z in before if z>threshold];assert len(after)==len(old_later),(len(before),len(after),len(old_later));assert min(after)>threshold
bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True)
bpy.ops.wm.open_mainfile(filepath=str(out),use_scripts=False)
sys.path.insert(0,str(Q/'Scripts'));import final_render_visibility as display
P=Q/'Previews/No-first-contour-v026';P.mkdir(exist_ok=True);timings=[]
with bpy.context.temp_override(window=bpy.context.window_manager.windows[0]):
 for frame,name in [(536,'first_panel'),(620,'during_reveal'),(756,'wide')]:
  bpy.context.scene.frame_set(frame);t=time.perf_counter();display.export(P/(name+'.png'),1920,1080);dt=time.perf_counter()-t;assert dt<5;timings.append({'frame':frame,'seconds':dt})
bpy.context.scene.frame_set(536);bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True)
record={'scene':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'source':'v025','omitted_ring_z':bottom,'mask_threshold_z':threshold,'major_faces_before':len(before),'major_faces_after':len(after),'later_major_faces_preserved':len(old_later),'first_ring_removed':min(after)>threshold,'stills':timings,'scope':'Only first major contour branch selection changed; fitted wall, later contours, controls, blue reveal and all camera/beam animation preserved. Shared masters unchanged.'}
(Q/'Notes/no_first_contour_v026.json').write_text(json.dumps(record,indent=2));result=record
