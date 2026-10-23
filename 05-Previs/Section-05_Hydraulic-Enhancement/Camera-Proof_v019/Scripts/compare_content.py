import bpy,json,hashlib
from pathlib import Path
import numpy as np
B=Path(__file__).resolve().parents[1]
def snap():
 s=bpy.context.scene;s.frame_set(198);bpy.context.view_layer.update();cam=s.camera;out={}
 def h(data):return hashlib.sha256(json.dumps(data,sort_keys=True,default=str).encode()).hexdigest()
 def animation(id):
  a=id.animation_data.action if id.animation_data else None
  if not a:return None
  # Compare the bound slot only, because Blender may share one Action among IDs.
  slot=id.animation_data.action_slot;rows=[]
  for layer in a.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     if slot and bag.slot_handle!=slot.handle:continue
     for fc in bag.fcurves:rows.append([fc.data_path,fc.array_index,fc.extrapolation,[(list(k.co),list(k.handle_left),list(k.handle_right),k.interpolation) for k in fc.keyframe_points]])
  return rows
 for o in s.objects:
  if o==cam:continue
  out['object/'+o.name]=h([o.type,o.parent.name if o.parent else None,o.hide_render,o.hide_viewport,animation(o)])
  if o.type=='MESH':
   me=o.data;digest=hashlib.sha256()
   a=np.empty(len(me.vertices)*3,dtype=np.float32);me.vertices.foreach_get('co',a);digest.update(a.tobytes())
   a=np.empty(len(me.loops),dtype=np.int32);me.loops.foreach_get('vertex_index',a);digest.update(a.tobytes())
   if me.shape_keys:
    for k in me.shape_keys.key_blocks:
     a=np.empty(len(k.data)*3,dtype=np.float32);k.data.foreach_get('co',a);digest.update(a.tobytes())
    digest.update(h(animation(me.shape_keys)).encode())
   out['mesh/'+o.name]=digest.hexdigest()
   for mat in me.materials:
    if not mat:continue
    values=[mat.name,tuple(mat.diffuse_color)]
    if mat.node_tree:
     for n in mat.node_tree.nodes:
      values.append([n.name,n.type])
      for inp in n.inputs:
       if hasattr(inp,'default_value'):
        val=inp.default_value
        try:val=list(val)
        except TypeError:pass
        values.append([inp.identifier,val])
     values.append([(l.from_node.name,l.from_socket.identifier,l.to_node.name,l.to_socket.identifier) for l in mat.node_tree.links]);values.append(animation(mat.node_tree))
    out['material/'+mat.name]=h(values)
 for f in [1,120,198,288,432]:
  s.frame_set(f);bpy.context.view_layer.update()
  for o in s.objects:
   if o!=cam:
    # Camera-parented legacy labels legitimately move with the camera; local pose must remain unchanged.
    m=o.matrix_basis if o.parent==cam else o.matrix_world
    out[f'transform/{f}/{o.name}']=h([[round(v,7) for v in row] for row in m])
 return out
baseline=json.loads((B/'Records/source-baseline.json').read_text())
bpy.ops.wm.open_mainfile(filepath=baseline['source']);a=snap()
bpy.ops.wm.open_mainfile(filepath=str(B/'Scenes/S05_camera-direction_v019.blend'));b=snap()
diff=[k for k in sorted(set(a)|set(b)) if a.get(k)!=b.get(k)]
record={'source':baseline['source'],'candidate':bpy.data.filepath,'equal':not diff,'items_compared':len(a),'differences':diff,'scope':'All scene object mesh/topology/shape-key geometry, bound noncamera animation slots, materials and nodes, object transforms across five frames. Camera-parented legacy labels compared in local coordinates. Unused orphan datablocks excluded.'}
(B/'Records/content-preservation.json').write_text(json.dumps(record,indent=2));result=record
