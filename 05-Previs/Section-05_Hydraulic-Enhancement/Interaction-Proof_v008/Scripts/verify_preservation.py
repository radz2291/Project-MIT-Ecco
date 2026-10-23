import bpy,json,hashlib,time,numpy as np
from pathlib import Path
B=Path(__file__).resolve().parents[1];current=B/'Scenes/S05_internal-flow_v008.blend';prior=B.parent/'Interaction-Proof_v007/Scenes/S05_fluid-volume_v007.blend'
def value(v):
 if isinstance(v,(int,float,str,bool)):return v
 try:return list(v)
 except:return str(v)
def signature():
 d=bpy.data.objects['S05_v007_AnnularFluidDomain'];a=np.empty(len(d.data.vertices)*3,dtype=np.float32);d.data.vertices.foreach_get('co',a)
 mats=[]
 for m in d.data.materials:
  nodes=[]
  for n in m.node_tree.nodes:
   record={'name':n.name,'type':n.bl_idname,'inputs':[(i.name,value(i.default_value)) for i in n.inputs if hasattr(i,'default_value')]}
   if hasattr(n,'mapping') and hasattr(n.mapping,'curves'):record['curves']=[[list(p.location) for p in c.points] for c in n.mapping.curves]
   nodes.append(record)
  mats.append({'name':m.name,'surface_method':m.surface_render_method,'nodes':nodes,'links':[(l.from_node.name,l.from_socket.name,l.to_node.name,l.to_socket.name) for l in m.node_tree.links]})
 cam=bpy.context.scene.camera
 return {'volume_vertex_sha256':hashlib.sha256(a.tobytes()).hexdigest(),'volume_faces':[list(p.vertices) for p in d.data.polygons],'volume_materials':mats,'camera_location':list(cam.location),'camera_quaternion':list(cam.rotation_quaternion),'lens':cam.data.lens}
s=bpy.context.scene;s.frame_set(36);s.render.filepath='//../Work/Frames/S05_';bpy.ops.wm.save_as_mainfile(filepath=str(current))
native_hash=hashlib.sha256(current.read_bytes()).hexdigest();prior_hash=hashlib.sha256(prior.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(prior));old=signature();bpy.ops.wm.open_mainfile(filepath=str(current));new=signature();assert old==new,'Approved foundation changed'
s=bpy.context.scene;s.frame_set(36);s.render.filepath=str(B/'Work/reopened-frame36.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t
result={'native_sha256':native_hash,'v007_sha256':prior_hash,'approved_fluid_mesh_topology_material_nodes_and_camera_match_v007':True,'volume_vertex_sha256':new['volume_vertex_sha256'],'reopened_render_seconds':dt,'libraries':[{'path':bpy.path.abspath(l.filepath),'relative':l.filepath.startswith('//'),'exists':Path(bpy.path.abspath(l.filepath)).exists()} for l in bpy.data.libraries]}
(B/'Records/native-preservation.json').write_text(json.dumps(result,indent=2))
