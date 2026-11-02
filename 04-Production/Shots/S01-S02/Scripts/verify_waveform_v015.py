import bpy,json,math,sys
from pathlib import Path
from mathutils import Vector
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');Q=R/'04-Production/Shots/S01-S02';A=R/'04-Production/Shared/Assets/Effects/Waveform';sys.path.insert(0,str(A/'Scripts'))
from pulse_asset_api import set_input
def sample(o,f):
 bpy.context.scene.frame_set(f);e=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=e.to_mesh();co=[tuple(v.co) for v in m.vertices];at={n:[v.value for v in m.attributes[n].data] for n in ['wf17_u','wf17_component'] if n in m.attributes};e.to_mesh_clear();return co,at
base=[]
for v in ['v019','v020']:
 bpy.ops.wm.open_mainfile(filepath=str(A/f'Waveform_shared_{v}.blend'),use_scripts=False);base.append(sample(bpy.data.objects['WF_PULSE_FIELD'],18)[0])
assert base[0]==base[1]
bpy.ops.wm.open_mainfile(filepath=str(Q/'Scenes/S01-S02_production_v015.blend'),use_scripts=False);s=bpy.context.scene;assert s.frame_end==1248
assert all(Path(bpy.path.abspath(l.filepath)).exists() for l in bpy.data.libraries)
o=bpy.data.objects['WF sequence event 1'];opening=[]
for f in range(300,306):
 co,a=sample(o,f);opening.append(max(a.get('wf17_u',[0])));assert abs(opening[-1]-(f-300)/5)<.003
for f in [306,307]:
 co,a=sample(o,f);assert max(abs(sum(v[2] for v in co[i:i+4])/4) for i in range(0,len(co),4))<1e-8
for f in [308,341,360,368,401,417,418]:
 co,a=sample(o,f);assert min(a['wf17_u'])==0 and max(a['wf17_u'])==1;assert set(a['wf17_component'])=={1 if f<368 else 2}
assert not sample(o,423)[0]
def height():
 co,a=sample(o,323);return max(abs(sum(v[2] for v in co[i:i+4])/4) for i in range(0,len(co),4))
on=height();set_input(o.modifiers[0],'Amplitude breath',0.);off=height();ratio=on/off;assert abs(ratio-(1+.32*math.sin(math.tau*15/48)))<.0001
set_input(o.modifiers[0],'Amplitude breath',.32)
records=json.loads((Q/'Notes/waveform_v013_install.json').read_text())['events'];errors=[];holds=[]
for i,r in enumerate(records):
 st=300+144*i;poses=[]
 for f in [st+68,st+118,st+123,st+132]:
  s.frame_set(f);poses.append([tuple(row) for row in bpy.data.objects['BHA sequence assembly'].matrix_world]);B=Vector(r['wall']);pt=Vector(r['surface_hit']);direction=(pt-B).normalized();hits=[]
  for ins in bpy.context.evaluated_depsgraph_get().object_instances:
   if ins.is_instance and ins.object.name==r['surface']:
    inv=ins.matrix_world.inverted();yes,p,n,idx=ins.object.ray_cast(inv@B,(inv.to_3x3()@direction).normalized())
    if yes:hits.append((ins.matrix_world@p-pt).length)
  assert hits and min(hits)<.0001;errors.append(min(hits))
 assert all(p==poses[0] for p in poses);holds.append(i+1)
 s.frame_set(st+54);wall=bpy.data.objects['ONE WALL - old history and current cells share topology'];ev=wall.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=ev.to_mesh();import re
 count=sum(1 for p in mesh.polygons if re.match(r'Unified cell '+str(i+1)+r'(\s|$)',mesh.materials[p.material_index].name));ev.to_mesh_clear();assert count==16,('viewing wedge removed target faces',i+1,count)
(Q/'Notes/waveform_v015_verification.json').write_text(json.dumps({'default_v020_exact_v019':True,'reopen_links':True,'opening_route_fractions':opening,'straight_setup_306_307':True,'continuous_endpoints_and_colors':True,'amplitude_on_off_ratio_at323':ratio,'expected_ratio':1+.32*math.sin(math.tau*15/48),'held_targets':holds,'max_cap_ray_error_m':max(errors),'scene_frames':1248,'cycle_seconds':6},indent=2));print('V015_POLISH_VERIFIED')
