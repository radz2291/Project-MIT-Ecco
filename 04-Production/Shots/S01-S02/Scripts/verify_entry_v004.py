import bpy,json,math,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');Q=R/'04-Production/Shots/S01-S02';s=bpy.context.scene;c=s.camera
s.frame_set(94);dg=bpy.context.evaluated_depsgraph_get();vs=[];fs=[];included=[]
for ins in dg.object_instances:
 ob=ins.object
 if not ins.is_instance or not ins.parent or ins.parent.original.name!='Shared offshore equipment' or ob.type!='MESH':continue
 if not (ob.name.startswith(('SUBSEA_BOPStack','SUBSEA_Foundation','SUBSEA_RiserCoupling','SUBSEA_EntrySleeve','SUBSEA_AuxiliaryLine')) or ob.name=='RIG_MarineRiser'):continue
 me=ob.to_mesh();base=len(vs);vs.extend(ins.matrix_world@v.co for v in me.vertices);fs.extend(tuple(base+i for i in p.vertices) for p in me.polygons);ob.to_mesh_clear();included.append(ob.name)
tree=BVHTree.FromPolygons(vs,fs,all_triangles=False)
def curves(action,slot):return [fc for l in action.layers for st in l.strips for bag in st.channelbags if bag.slot_handle==slot.handle for fc in bag.fcurves]
ad=c.animation_data;fcs={(f.data_path,f.array_index):f for f in curves(ad.action,ad.action_slot)}
assert c.parent is None and not c.constraints
rows=[]
for k in range(0,121):
 f=85+k*.1;p=Vector(tuple(fcs[('location',i)].evaluate(f) for i in range(3)));hit,normal,index,dist=tree.find_nearest(p)
 rows.append({'frame':round(f,1),'distance_m':dist,'signed_distance_m':(p-hit).dot(normal)})
closest=min(rows,key=lambda x:x['distance_m']);inside=[r for r in rows if r['signed_distance_m']<-.0001]
old=bpy.data.actions[c['entry_original_action']];slot=next(x for x in old.slots if x.identifier==ad.action_slot.identifier);ofcs={(f.data_path,f.array_index):f for f in curves(old,slot)}
later=max(abs(fc.evaluate(f)-ofcs[key].evaluate(f)) for key,fc in fcs.items() for f in range(112,529))
rockframe=next(f for f in range(85,106) if fcs[('location',2)].evaluate(f)<-120)
origin=Vector(tuple(fcs[('location',i)].evaluate(94) for i in range(3)));hits=[]
for a in range(0,360,5):
 hit,n,ix,dist=tree.ray_cast(origin,Vector((math.cos(math.radians(a)),math.sin(math.radians(a)),0)),4);hits.append(dist if hit is not None else None)
ctrl=bpy.data.objects['ENTRY presentation controls'];reveal=[]
for f in [114,115,120,123,141]:
 s.frame_set(f);reveal.append({'frame':f,'front_reveal':ctrl['Front reveal'],'bore_scale':ctrl['Bore scale']})
meta=json.loads((Q/'Notes/surface_v008_build.json').read_text());unchanged={p:hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in meta['sources'].items()}
d={'missing_libraries':[l.filepath for l in bpy.data.libraries if not Path(bpy.path.abspath(l.filepath)).exists()],'camera_closest_equipment_85_97':closest,'camera_probe_count':len(rows),'inside_equipment_samples':inside,'near_clip_m':c.data.clip_start,'continuous_test_objects':included,'first_camera_below_seabed_frame':rockframe,'metal_enclosure94':{'rays':len(hits),'missing':sum(x is None for x in hits)},'later_camera_curve_max_error112_528':later,'later_reveal_samples':reveal,'shared_predecessors_unchanged':unchanged}
d['pass']=not d['missing_libraries'] and rockframe==95 and later<1e-7 and not inside and closest['distance_m']>c.data.clip_start and not d['metal_enclosure94']['missing'] and all(unchanged.values())
(Q/'Notes/entry_v004_verification.json').write_text(json.dumps(d,indent=2));result=d
