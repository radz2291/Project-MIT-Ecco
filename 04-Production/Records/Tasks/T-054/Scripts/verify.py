import bpy,json,hashlib,array
from pathlib import Path
R=Path(__file__).resolve().parents[5];T=R/'04-Production/Records/Tasks/T-054';out={}
def meshhash(m):
 a=array.array('f',[0])*(len(m.vertices)*3);m.vertices.foreach_get('co',a);b=array.array('i',[0])*len(m.loops);m.loops.foreach_get('vertex_index',b);return hashlib.sha256(a.tobytes()+b.tobytes()).hexdigest()
for sid,name,frames in [('S02','S02_shared-reveal_v001',[317,441,447,480,528]),('S03','S03_shared-digital_v001',[1,120]),('S06','S06_shared-digital_v001',[1,52,144,250])]:
 bpy.ops.wm.open_mainfile(filepath=str(T/'Consumers'/f'{name}.blend'),load_ui=False);s=bpy.context.scene;record={'libraries':[{'path':l.filepath,'exists':Path(bpy.path.abspath(l.filepath)).is_file()} for l in bpy.data.libraries],'cameras':[]}
 for f in frames:
  s.frame_set(f);record['cameras'].append({'frame':f,'matrix':[list(r) for r in s.camera.matrix_world],'lens':s.camera.data.lens})
  if sid=='S02':
   ob=bpy.data.objects['ONE WALL - old history and current cells share topology'];ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());record.setdefault('reveal_faces',[]).append({'frame':f,'faces':len(ev.data.polygons)})
 if sid=='S02':record['raw_mesh_hash']=meshhash(ob.data)
 if sid=='S06':record['local_data_hashes']={n:meshhash(bpy.data.objects[n].data) for n in ['A | indexed reconstruction samples','A | reconstructed wall beginning to open']}
 record['shared_groups']=[{'name':g.name,'library':g.library.filepath if g.library else None} for g in bpy.data.node_groups if g.name.startswith('ECCO')]
 out[sid]=record
# Fail closed on missing attributes; don't save these runtime changes.
bpy.ops.wm.open_mainfile(filepath=str(T/'Consumers/Reveal_two-shapes_v001.blend'),load_ui=False);s=bpy.context.scene;s.frame_set(60);o=next(o for o in s.objects if o.type=='MESH');o.modifiers[-1].show_viewport=False
o.data.attributes.remove(o.data.attributes['ecco_receipt_frame']);bpy.context.view_layer.update();out['missing_attributes_fail_closed']=len(o.evaluated_get(bpy.context.evaluated_depsgraph_get()).data.polygons)==0
(T/'Evidence/verification.json').write_text(json.dumps(out,indent=2));print('VERIFIED',out['missing_attributes_fail_closed'])
