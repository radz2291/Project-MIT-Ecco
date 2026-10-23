import bpy,json,hashlib,time,numpy as np
from pathlib import Path
B=Path(__file__).resolve().parents[1];current=B/'Scenes/S05_combined-interaction_v010.blend';prior=B.parent/'Interaction-Proof_v008/Scenes/S05_internal-flow_v008.blend'
def value(v):
 if isinstance(v,(int,float,str,bool)):return v
 try:return list(v)
 except:return str(v)
def mesh_sig(o):
 a=np.empty(len(o.data.vertices)*3,dtype=np.float32);o.data.vertices.foreach_get('co',a)
 return [hashlib.sha256(a.tobytes()).hexdigest(),hashlib.sha256(str([list(p.vertices) for p in o.data.polygons]).encode()).hexdigest()]
def signature():
 s=bpy.context.scene;s.frame_set(1);m=bpy.data.objects['S05_v007_AnnularFluidDomain'].data.materials[0];nodes=[]
 for n in m.node_tree.nodes:
  rec={'type':n.bl_idname,'name':n.name,'inputs':[(i.name,value(i.default_value)) for i in n.inputs if hasattr(i,'default_value')]}
  if hasattr(n,'mapping') and hasattr(n.mapping,'curves'):rec['curves']=[[list(p.location) for p in c.points] for c in n.mapping.curves]
  nodes.append(rec)
 return {'fluid_mesh':mesh_sig(bpy.data.objects['S05_v007_AnnularFluidDomain']),'borehole_mesh':mesh_sig(bpy.data.objects['S05_FixedHalfBorehole']),'hardware':[(o.name,o.data.name,list(o.scale)) for o in bpy.data.collections['S05_LINKED_HARDWARE'].objects],'fluid_nodes':nodes,'fluid_links':[(l.from_node.name,l.from_socket.name,l.to_node.name,l.to_socket.name) for l in m.node_tree.links],'surface_method':m.surface_render_method}
s=bpy.context.scene;s.frame_set(48);s.render.filepath='//../Work/Frames/S05_';bpy.ops.wm.save_as_mainfile(filepath=str(current));native_hash=hashlib.sha256(current.read_bytes()).hexdigest();new=signature()
bpy.ops.wm.open_mainfile(filepath=str(prior));old=signature();assert old==new,'Preservation mismatch'
bpy.ops.wm.open_mainfile(filepath=str(current));assert signature()==new
s=bpy.context.scene;m=bpy.data.objects['S05_v007_AnnularFluidDomain'].data.materials[0];motion=[]
for f in [1,48,72,96]:
 s.frame_set(f);shift=next(n for n in m.node_tree.nodes if n.type=='VECT_MATH' and n.operation=='SUBTRACT');spin=next(n for n in m.node_tree.nodes if n.type=='MATH' and n.operation=='ADD');motion.append({'frame':f,'density_z_offset_m':shift.inputs[1].default_value[2],'density_angular_offset_rad':spin.inputs[1].default_value})
assert motion[-1]['density_z_offset_m']>motion[-2]['density_z_offset_m']>motion[1]['density_z_offset_m']>motion[0]['density_z_offset_m']
s.frame_set(48);s.render.filepath=str(B/'Work/reopened-frame48.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t;assert dt<5
result={'native_sha256':native_hash,'fluid_material_nodes_links_and_mesh_match_v008_at_frame1':True,'linked_hardware_and_borehole_meshes_match_v008':True,'fluid_animation_samples':motion,'reopened_render_seconds':dt,'libraries':[{'path':bpy.path.abspath(l.filepath),'relative':l.filepath.startswith('//'),'exists':Path(bpy.path.abspath(l.filepath)).exists()} for l in bpy.data.libraries],'authorized_differences':'Extended fluid animation to 96 frames with linear extrapolation; new independent tracked cohort and wisps; camera viewing angle and lens shift; fixed section azimuth adjusted only.'}
assert all(l['exists'] and l['relative'] for l in result['libraries'])
(B/'Records/native-preservation.json').write_text(json.dumps(result,indent=2))
