"""Fast native separation slider on the owner-selected pulse train."""
import bpy,time,json
from pathlib import Path
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');Q=R/'04-Production/Shots/S01-S02';P=Q/'Previews/Waveform-direction-v004';P.mkdir(exist_ok=True);s=bpy.context.scene
if bpy.data.is_dirty:bpy.ops.wm.save_as_mainfile(filepath=str(Q/f'Scenes/Pulse_session_before_spacing_{int(time.time())}.blend'),copy=True,compress=True)
field=next(o for o in s.objects if o.name.startswith('QUICK live bends') and o.visible_get())
attr=field.data.attributes.get('pulse_strand_weight') or field.data.attributes.new('pulse_strand_weight','FLOAT','POINT')
attr.data.foreach_set('value',[2*(i//(145*4))/4-1 for i in range(len(field.data.vertices))])
g=bpy.data.node_groups.new('QUICK pulse strand separation','GeometryNodeTree');g.is_modifier=True
g.interface.new_socket(name='Geometry',in_out='INPUT',socket_type='NodeSocketGeometry');g.interface.new_socket(name='Geometry',in_out='OUTPUT',socket_type='NodeSocketGeometry')
x=g.interface.new_socket(name='Strand separation',in_out='INPUT',socket_type='NodeSocketFloat');x.default_value=.65;x.min_value=0;x.max_value=.9;x.description='0 = tight bundle;0.65 = wider height fan. Pulse timing, center strand and fixed endpoints stay unchanged.'
n=g.nodes;l=g.links;i=n.new('NodeGroupInput');out=n.new('NodeGroupOutput');pos=n.new('GeometryNodeInputPosition');sep=n.new('ShaderNodeSeparateXYZ');l.new(pos.outputs[0],sep.inputs[0]);weight=n.new('GeometryNodeInputNamedAttribute');weight.data_type='FLOAT';weight.inputs['Name'].default_value='pulse_strand_weight'
a=n.new('ShaderNodeMath');a.operation='MULTIPLY';l.new(sep.outputs['Z'],a.inputs[0]);l.new(weight.outputs['Attribute'],a.inputs[1]);b=n.new('ShaderNodeMath');b.operation='MULTIPLY';l.new(a.outputs[0],b.inputs[0]);l.new(i.outputs['Strand separation'],b.inputs[1]);v=n.new('ShaderNodeCombineXYZ');l.new(b.outputs[0],v.inputs['Z']);setp=n.new('GeometryNodeSetPosition');l.new(i.outputs['Geometry'],setp.inputs['Geometry']);l.new(v.outputs[0],setp.inputs['Offset']);l.new(setp.outputs[0],out.inputs[0])
m=field.modifiers.new('Pulse strand separation — quick option','NODES');m.node_group=g;param=getattr(m.properties.inputs,x.identifier);s.camera.data.ortho_scale=.065
rows=[]
for label,spread in [('tight',0.),('wide',.65)]:
 param.value=spread;field.update_tag();bpy.context.view_layer.update()
 for f in range(1,73):
  t=time.perf_counter();s.frame_set(f);s.render.filepath=str(P/f'{label}_{f:04}.png');bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t;rows.append({'preset':label,'frame':f,'seconds':dt})
  if dt>=5:raise RuntimeError('Render cap failed')
param.value=.65;field.update_tag();s.frame_set(14)
for ob in bpy.context.selected_objects:ob.select_set(False)
field.select_set(True);bpy.context.view_layer.objects.active=field
for area in bpy.context.screen.areas:
 if area.type=='PROPERTIES':area.spaces.active.context='MODIFIER'
bpy.ops.wm.save_as_mainfile(filepath=str(Q/'Scenes/Waveform_direction_quick_v004.blend'),compress=True)
(Q/'Notes/wave_direction_quick_v004.json').write_text(json.dumps({'option':'Strand separation','tight':0,'wide':.65,'range':[0,.9],'note':'Disposable quick proof. Scales per-strand height variation after pulse deformation; pulse phase and axial coordinates unchanged. Shared masters unchanged.','rows':rows},indent=2));result={'native':bpy.data.filepath,'control':'Modifiers > Strand separation','frames':144,'max_seconds':max(x['seconds'] for x in rows)}
