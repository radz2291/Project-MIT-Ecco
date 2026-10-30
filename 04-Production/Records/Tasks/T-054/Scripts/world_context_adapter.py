"""Explicit World physical context, separate from local measured displays."""
import bpy,json
from pathlib import Path
from mathutils import Matrix
R=Path(__file__).resolve().parents[5];T=R/'04-Production/Records/Tasks/T-054';A=R/'04-Production/Shared/Assets';world=A/'WellAssembly/World_environment_v010.blend'
records=[]
for sid in ['S03','S06']:
 bpy.ops.wm.open_mainfile(filepath=str(T/'Consumers'/f'{sid}_shared-digital_v001.blend'),load_ui=False)
 # Full physical shell avoids inventing a mirrored inner surface. The local
 # viewing cut is a display window only, not a change to the World source.
 with bpy.data.libraries.load(str(world),link=True) as (a,b):b.collections=['WORLD_FORMATION_IRREGULAR_FULL']
 src=next(o for o in b.collections[0].objects if o.type=='MESH')
 hide=['SOLID EARTH - borehole cutaway half-space','GROUND FRONT HALF - closes tunnel for interior camera'] if sid=='S03' else ['Rock sectional mass','Rock sectional mass.001','Fixed borehole context | open viewing sector']
 for name in hide:bpy.data.objects[name].hide_render=True
 g=bpy.data.node_groups.new(sid+' local physical World window','GeometryNodeTree');g.interface.new_socket(name='Geometry',in_out='OUTPUT',socket_type='NodeSocketGeometry');l=g.links
 oi=g.nodes.new('GeometryNodeObjectInfo');oi.inputs['Object'].default_value=src;oi.transform_space='ORIGINAL'
 # canonical X→section Z, Y→X, Z→Y; determinant+1. No radius scaling.
 tr=g.nodes.new('GeometryNodeTransform');tr.inputs['Rotation'].default_value=Matrix(((0,1,0),(0,0,1),(1,0,0))).to_euler();l.new(oi.outputs['Geometry'],tr.inputs['Geometry'])
 p=g.nodes.new('GeometryNodeInputPosition');sep=g.nodes.new('ShaderNodeSeparateXYZ');l.new(p.outputs[0],sep.inputs[0])
 def math(op,a,b):
  n=g.nodes.new('ShaderNodeMath');n.operation=op
  for k,v in enumerate([a,b]):
   if isinstance(v,(float,int)):n.inputs[k].default_value=v
   else:l.new(v,n.inputs[k])
  return n.outputs[0]
 low=-10 if sid=='S03' else -1.2;high=10 if sid=='S03' else 1.2
 sel=math('MAXIMUM',math('LESS_THAN',sep.outputs['Z'],low),math('GREATER_THAN',sep.outputs['Z'],high))
 # Open front hemisphere; same side as the existing section's camera window.
 sel=math('MAXIMUM',sel,math('LESS_THAN',sep.outputs['Y'],0))
 delete=g.nodes.new('GeometryNodeDeleteGeometry');delete.domain='FACE';l.new(tr.outputs[0],delete.inputs[0]);l.new(sel,delete.inputs['Selection'])
 with bpy.data.libraries.load(str(A/'DigitalEnvironment/Digital_style_v001.blend'),link=True) as (a,b):b.materials=['Digital earth - charcoal layered solid']
 sm=g.nodes.new('GeometryNodeSetMaterial');sm.inputs['Material'].default_value=b.materials[0];l.new(delete.outputs[0],sm.inputs[0]);out=g.nodes.new('NodeGroupOutput');l.new(sm.outputs[0],out.inputs[0])
 ob=bpy.data.objects.new(sid+' | physical World live context',bpy.data.meshes.new(sid+' physical carrier'));bpy.context.scene.collection.objects.link(ob);ob.modifiers.new('Live physical source with local window','NODES').node_group=g
 ob['placement']='Canonical X→local Z,Y→local X,Z→local Y; no radial/axial scale; local front hemisphere and axial window only'
 ob['distinction']='Physical context; local reconstructed surfaces are separate illustrative datasets, not remapped into physical samples'
 outpath=T/'Consumers'/f'{sid}_shared-digital_v002.blend';bpy.ops.wm.save_as_mainfile(filepath=str(outpath));bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(outpath))
 records.append({'section':sid,'candidate':str(outpath.relative_to(R)),'source_collection':'WORLD_FORMATION_IRREGULAR_FULL','source_object':src.name,'local_window':{'z':[low,high],'y_min':0},'mapping':[[0,1,0,0],[0,0,1,0],[1,0,0,0],[0,0,0,1]],'hidden_physical_only':hide,'status':'fit/occlusion requires visual review before selection'})
(T/'Evidence/world-context-adapters.json').write_text(json.dumps(records,indent=2));print('WORLD_CONTEXT_DONE')
