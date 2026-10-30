import bpy,pathlib,json,hashlib
R=pathlib.Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');T=R/'04-Production/Records/Tasks/T-056';mapping=json.loads((T/'consumer-mapping_v014.json').read_text());results=[]
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,default=str).encode()).hexdigest()
def action(a):
 if not a:return None
 return [[[fc.data_path,fc.array_index,[[list(k.co),k.interpolation,list(k.handle_left),list(k.handle_right)] for k in fc.keyframe_points]] for layer in a.layers for strip in layer.strips for bag in strip.channelbags for fc in bag.fcurves]]
def state():
 bpy.context.scene.frame_set(1);bpy.context.view_layer.update()
 obs={};data={}
 for ob in bpy.data.objects:
  obs[ob.name]=digest({'custom':dict(ob.items()),'action':action(ob.animation_data.action if ob.animation_data else None),'type':ob.type,'data':ob.data.name if ob.data else None})
  d=ob.data
  if d is None or d.name in data:continue
  payload={'custom':dict(d.items())}
  if ob.type=='MESH':
   payload['vertices']=[list(v.co) for v in d.vertices];payload['polys']=[list(p.vertices) for p in d.polygons]
   if d.shape_keys:payload['keys']=[(k.name,[list(v.co) for v in k.data]) for k in d.shape_keys.key_blocks];payload['key_action']=action(d.shape_keys.animation_data.action if d.shape_keys.animation_data else None)
  elif ob.type=='CURVE':payload['splines']=[(x.type,[list(p.co) for p in x.points],[(list(p.co),list(p.handle_left),list(p.handle_right)) for p in x.bezier_points]) for x in d.splines]
  data[d.name]=digest(payload)
 return obs,data,digest(dict(bpy.context.scene.items()))
for m in mapping:
 bpy.ops.wm.open_mainfile(filepath=m['baseline']);ob0,d0,s0=state();bpy.ops.wm.open_mainfile(filepath=m['candidate']);ob1,d1,s1=state();od=[n for n,h in ob0.items() if ob1.get(n)!=h];dd=[n for n,h in d0.items() if d1.get(n)!=h];results.append({'consumer':m['name'],'source_objects':len(ob0),'source_data_blocks':len(d0),'object_action_custom_differences':od,'geometry_shape_action_differences':dd,'scene_custom_equal':s0==s1,'pass':not od and not dd and s0==s1})
(T/'source-preservation_v014.json').write_text(json.dumps(results,indent=2));print('SOURCE_PRESERVATION',json.dumps(results))
