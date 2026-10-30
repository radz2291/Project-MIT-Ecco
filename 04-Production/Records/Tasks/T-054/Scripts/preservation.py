import bpy,json,hashlib,array
from pathlib import Path
R=Path(__file__).resolve().parents[5];T=R/'04-Production/Records/Tasks/T-054';S={x['id']:R/x['native'] for x in json.loads((R/'04-Production/Records/Tasks/T-050/sources.json').read_text())};out=[]
def meshhash(m):
 a=array.array('f',[0])*(len(m.vertices)*3);m.vertices.foreach_get('co',a);b=array.array('i',[0])*len(m.loops);m.loops.foreach_get('vertex_index',b);return hashlib.sha256(a.tobytes()+b.tobytes()).hexdigest()
for sid,names in [('S02',['ONE WALL - old history and current cells share topology']),('S03',['ILLUSTRATIVE CONTINUOUS WALL v009']),('S06',['A | indexed reconstruction samples','A | reconstructed wall beginning to open'])]:
 baseline={};candidate={}
 bpy.ops.wm.open_mainfile(filepath=str(S[sid]),load_ui=False)
 for n in names:baseline[n]={'mesh':meshhash(bpy.data.objects[n].data),'matrix':[list(r) for r in bpy.data.objects[n].matrix_world]}
 suffix='shared-reveal_v001' if sid=='S02' else 'shared-digital_v002';bpy.ops.wm.open_mainfile(filepath=str(T/'Consumers'/f'{sid}_{suffix}.blend'),load_ui=False)
 for n in names:candidate[n]={'mesh':meshhash(bpy.data.objects[n].data),'matrix':[list(r) for r in bpy.data.objects[n].matrix_world]}
 out.append({'section':sid,'baseline':baseline,'candidate':candidate,'same_raw_sample_geometry_and_transforms':baseline==candidate})
(T/'Evidence/data-preservation.json').write_text(json.dumps(out,indent=2));print([(x['section'],x['same_raw_sample_geometry_and_transforms']) for x in out])
