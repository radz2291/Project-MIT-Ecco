"""World v014: preserve v013, add matching missing front and reusable presentation GN.
Run background with v013 loaded. Consumer owns timing and modifier values.
"""
import bpy, math, json, hashlib, bisect, sys
from pathlib import Path
from mathutils import Vector
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');B=R/'04-Production/Shared/Assets/Environment/Borehole';Q=R/'04-Production/Shots/S01-S02'
src=B/'World_environment_v013.blend';dst=B/'World_environment_v014.blend'
assert not dst.exists() or '--replace-unpublished' in sys.argv
source_sha=hashlib.sha256(src.read_bytes()).hexdigest()
wall=bpy.data.objects['WORLD_S02_PHYSICAL_CUTAWAY_MESH']
def digest(ob):return hashlib.sha256(b''.join(__import__('struct').pack('fff',*v.co) for v in ob.data.vertices)).hexdigest()
before={o.name:digest(o) for o in bpy.data.objects if o.type=='MESH'}
front=bpy.data.collections.new('WORLD_DESCENT_FRONT_CLOSURE');front.use_fake_user=True
variants=bpy.data.collections.new('WORLD_DESCENT_CLOSED');variants.children.link(bpy.data.collections['WORLD_DESCENT_CONNECTED']);variants.children.link(front);variants.use_fake_user=True
# Front profiles meet both retained angular seams; the missing sector is authored interpolation.
rings={}
for v in wall.data.vertices:
 p=v.co;r=math.hypot(p.y,p.z)
 if r<1:
  a=math.atan2(p.z,p.y)
  if a<math.radians(-5.01):a+=math.tau
  rings.setdefault(round(p.x,5),[]).append((a,r))
xs=sorted(rings);edge={x:(min(rings[x])[1],max(rings[x])[1]) for x in xs}
def edges(x):
 q=(x+15)%60;u=-15+q if q<=30 else 45-q;k=max(0,min(len(xs)-2,bisect.bisect_right(xs,u)-1));a,b=xs[k:k+2];f=(u-a)/(b-a)
 return tuple(edge[a][j]*(1-f)+edge[b][j]*f for j in range(2))
boundaries=[-120,-245,-390,-515,-660,-805,-925,-1020]
for unit,(hi,lo) in enumerate(zip(boundaries,boundaries[1:]),1):
 materials=[o.data.materials[0] for o in bpy.data.collections['WORLD_REGIONAL_DESCENT'].objects if o.name.startswith(f'REGIONAL_UNIT_{unit:02}')]
 for side,(start,end,boundary) in enumerate([(225,290,225),(290,355,355)]):
  na=27;nz=math.ceil((hi-lo)/.25);vs=[];fs=[];bs=[];ds=[]
  for k in range(nz+1):
   x=lo+(hi-lo)*k/nz+735;r0,r1=edges(x)
   for outer in [False,True]:
    for j in range(na):
     deg=start+(end-start)*j/(na-1);u=(deg-225)/130;r=180 if outer else r1*(1-u)+r0*u;t=math.radians(deg)
     vs.append((x,r*math.cos(t),r*math.sin(t)));bs.append(math.radians(boundary));ds.append(math.radians(deg-boundary))
  def ix(k,b,j):return k*2*na+b*na+j
  for k in range(nz):
   for j in range(na-1):
    for b in [0,1]:
     face=(ix(k,b,j),ix(k+1,b,j),ix(k+1,b,j+1),ix(k,b,j+1));fs.append(face if b==0 else tuple(reversed(face)))
   for j in [0,na-1]:fs.append((ix(k,0,j),ix(k,1,j),ix(k+1,1,j),ix(k+1,0,j)))
  for k,z in [(0,lo),(nz,hi)]:
   if z in [-120,-1020]:
    for j in range(na-1):fs.append((ix(k,0,j),ix(k,0,j+1),ix(k,1,j+1),ix(k,1,j)))
  me=bpy.data.meshes.new(f'WORLD_FRONT_UNIT_{unit:02}_HALF_{side}');me.from_pydata(vs,[],fs);me.materials.append(materials[0]);me.update()
  for n,values in [('front_boundary',bs),('front_delta',ds)]:a=me.attributes.new(n,'FLOAT','POINT');a.data.foreach_set('value',values)
  ob=bpy.data.objects.new(me.name,me);front.objects.link(ob)
  ob['provenance']='Complementary130deg front sector. Exact retained seam radii; interpolated missing-sector profile. Illustrative, not measured.'

def group(name,isfront):
 g=bpy.data.node_groups.new(name,'GeometryNodeTree');g.use_fake_user=True
 for n,side,typ,value in [('Geometry','INPUT','NodeSocketGeometry',None),('Geometry','OUTPUT','NodeSocketGeometry',None),('Bore scale','INPUT','NodeSocketFloat',1.),('Front reveal','INPUT','NodeSocketFloat',0.)]:
  sock=g.interface.new_socket(name=n,in_out=side,socket_type=typ)
  if value is not None:sock.default_value=value
 n=g.nodes;l=g.links;i=n.new('NodeGroupInput');o=n.new('NodeGroupOutput');pos=n.new('GeometryNodeInputPosition');sep=n.new('ShaderNodeSeparateXYZ');l.new(pos.outputs[0],sep.inputs[0])
 def op(typ,a,b=None):
  z=n.new('ShaderNodeMath');z.operation=typ
  for ix,v in enumerate([a,b]):
   if v is None:continue
   if isinstance(v,(int,float)):z.inputs[ix].default_value=v
   else:l.new(v,z.inputs[ix])
  return z.outputs[0]
 r=op('SQRT',op('ADD',op('MULTIPLY',sep.outputs['Y'],sep.outputs['Y']),op('MULTIPLY',sep.outputs['Z'],sep.outputs['Z'])))
 factor=op('ADD',1.,op('MULTIPLY',op('LESS_THAN',r,1.),op('SUBTRACT',i.outputs['Bore scale'],1.)))
 if isfront:
  ba=n.new('GeometryNodeInputNamedAttribute');ba.data_type='FLOAT';ba.inputs['Name'].default_value='front_boundary'
  da=n.new('GeometryNodeInputNamedAttribute');da.data_type='FLOAT';da.inputs['Name'].default_value='front_delta'
  angle=op('ADD',ba.outputs['Attribute'],op('MULTIPLY',da.outputs['Attribute'],op('SUBTRACT',1.,i.outputs['Front reveal'])))
  y=op('MULTIPLY',op('MULTIPLY',r,factor),op('COSINE',angle));z=op('MULTIPLY',op('MULTIPLY',r,factor),op('SINE',angle))
 else:y=op('MULTIPLY',sep.outputs['Y'],factor);z=op('MULTIPLY',sep.outputs['Z'],factor)
 comb=n.new('ShaderNodeCombineXYZ');l.new(sep.outputs['X'],comb.inputs['X']);l.new(y,comb.inputs['Y']);l.new(z,comb.inputs['Z']);sp=n.new('GeometryNodeSetPosition');l.new(i.outputs['Geometry'],sp.inputs['Geometry']);l.new(comb.outputs[0],sp.inputs['Position'])
 if isfront:
  sw=n.new('GeometryNodeSwitch');sw.input_type='GEOMETRY';l.new(op('GREATER_THAN',i.outputs['Front reveal'],.999999),sw.inputs['Switch']);l.new(sp.outputs[0],sw.inputs['False']);l.new(sw.outputs[0],o.inputs[0])
 else:l.new(sp.outputs[0],o.inputs[0])
 # Smooth only the expanded interior for the camera passage; nominal downstream faces stay flat.
 current=o.inputs[0].links[0];upstream=current.from_socket;l.remove(current)
 shade=n.new('GeometryNodeSetShadeSmooth');shade.domain='FACE';l.new(upstream,shade.inputs['Geometry']);l.new(op('LESS_THAN',r,1.),shade.inputs['Selection']);l.new(op('GREATER_THAN',i.outputs['Bore scale'],1.001),shade.inputs['Shade Smooth']);l.new(shade.outputs[0],o.inputs[0])
 g['ownership']='Consumer supplies local timing; asset has no scene frame dependency. Bore scale1 reproduces retained coordinates. Front reveal0 closed,1 absent.'
 return g
group('WORLD retained bore presentation v001',False);group('WORLD front closure presentation v001',True)
for sc in bpy.data.scenes:
 for c in list(sc.collection.children):sc.collection.children.unlink(c)
 sc.collection.children.link(variants)
for c in bpy.data.collections:c.use_fake_user=True
txt=bpy.data.texts.new('README World v014');txt.write('v014 preserves every v013 mesh. WORLD_DESCENT_CLOSED adds complementary front sector. Link meshes into local consumer objects with WORLD retained bore presentation v001 / WORLD front closure presentation v001 modifiers; local controls Bore scale and Front reveal. CanonicalX bore axis. Missing-front profile interpolated, not measured. Source nominal retained wall remains exact. No shot timing, cameras or lights. Existing consumers stay pinned.\n')
assert before=={o.name:digest(o) for o in bpy.data.objects if o.name in before}
bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(dst),compress=True);bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(dst),compress=True)
assert hashlib.sha256(src.read_bytes()).hexdigest()==source_sha
meta=json.loads((B/'World_interface_v013.json').read_text());meta.update(version='v014',native=dst.relative_to(R).as_posix(),predecessor_native=src.relative_to(R).as_posix(),predecessor_sha256=source_sha,native_sha256=hashlib.sha256(dst.read_bytes()).hexdigest(),presentation={'closed_collection':'WORLD_DESCENT_CLOSED','front_collection':'WORLD_DESCENT_FRONT_CLOSURE','retained_collection':'WORLD_DESCENT_CONNECTED','node_groups':['WORLD retained bore presentation v001','WORLD front closure presentation v001'],'policy':'Nominal source meshes unchanged. Consumers own animation; Bore scale1 and Front reveal1 recover original retained cutaway. Missing130deg front is authored interpolation.'})
meta['default_scene_root']=['WORLD_DESCENT_CLOSED']
(B/'World_interface_v014.json').write_text(json.dumps(meta,indent=2));(Q/'Notes/world_v014_build.json').write_text(json.dumps({'source_sha256':source_sha,'native_sha256':meta['native_sha256'],'preserved_original_meshes':len(before),'front_meshes':len(front.objects),'actions':len(bpy.data.actions),'consumers':['S01-S02 production v003'],'pinned_consumers_unchanged':True},indent=2));print('WORLD_V014_READY')
