"""Native viewport pixel-stroke guides: edge-only meshes, no surfaces/thickness.
Includes cut faces, seabed, and surface-following bore grids derived from World v014.
"""
import bpy,math,json,hashlib
from pathlib import Path
from mathutils import Vector
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');B=R/'04-Production/Shared/Assets/Environment/Borehole';Q=R/'04-Production/Shots/S01-S02';out=B/'World_motion_grid_v002.blend';assert not out.exists()
bpy.ops.wm.read_factory_settings(use_empty=True)
world=B/'World_environment_v014.blend';source_hash=hashlib.sha256(world.read_bytes()).hexdigest()
with bpy.data.libraries.load(str(world),link=True) as (a,b):b.collections=['WORLD_DESCENT_CONNECTED','WORLD_DESCENT_FRONT_CLOSURE']
retained,front=b.collections
root=bpy.data.collections.new('WORLD_PIXEL_GUIDES_v002');bpy.context.scene.collection.children.link(root)
def empty():return {'vs':[],'es':[],'axis':[],'coord':[],'boundary':[],'delta':[]}
def edge(d,a,b,axis,coord,ba=0.,bb=0.,da=0.,db=0.):
 i=len(d['vs']);d['vs'].extend([tuple(a),tuple(b)]);d['es'].append((i,i+1));d['axis'].append(axis);d['coord'].append(coord);d['boundary'].extend([ba,bb]);d['delta'].extend([da,db])
cut=empty()
for deg,sign in [(-5,-1),(225,1)]:
 a=math.radians(deg);normal=(0,-math.sin(a)*.02*sign,math.cos(a)*.02*sign)
 def p(x,r):return (x,r*math.cos(a)+normal[1],r*math.sin(a)+normal[2])
 for j in range(901):edge(cut,p(-285+j,.85),p(-285+j,180),0,j)
 for j in range(180):edge(cut,p(-285,.85+j),p(615,.85+j),1,j)
top=empty()
for k in range(-179,180):
 end=math.sqrt(180**2-k*k);gap=math.sqrt(max(0,1.-k*k))
 for swap in [False,True]:
  for lo,hi in [(-end,-gap),(gap,end)]:
   if hi-lo>.001:edge(top,(615.02,k,lo) if swap else (615.02,lo,k),(615.02,k,hi) if swap else (615.02,hi,k),2,abs(k))
def bore(objects,isfront):
 d=empty();rows={}
 for ob in objects:
  if ob.type!='MESH':continue
  if not isfront and not ('_INNER_' in ob.name or ob.name=='WORLD_S02_PHYSICAL_CUTAWAY_MESH'):continue
  ba=ob.data.attributes.get('front_boundary');de=ob.data.attributes.get('front_delta')
  for v in ob.data.vertices:
   p=v.co;r=math.hypot(p.y,p.z)
   if r>=1:continue
   a=math.degrees(math.atan2(p.z,p.y))
   if a< -5.01:a+=360
   pos=Vector((p.x,p.y*(r-.003)/r,p.z*(r-.003)/r));boundary=ba.data[v.index].value if ba else 0.;delta=de.data[v.index].value if de else 0.
   rows.setdefault(round(p.x,5),{})[round(a,5)]=(pos,boundary,delta)
 xs=sorted(rows)
 if not xs:return d
 amin=min(rows[xs[0]]);amax=max(rows[xs[0]])
 targets=sorted(set([amin,amax]+[a for a in range(0,360,30) if amin<a<amax]))
 for x in xs:
  row=rows[x];angles=sorted(row)
  if abs(x-round(x))<.0001:
   for a,b in zip(angles,angles[1:]):
    p,pa,pd=row[a];q,qa,qd=row[b];edge(d,p,q,3,x+285,pa,qa,pd,qd)
 for x,y in zip(xs,xs[1:]):
  # Only connect adjacent rings within one source band's/profile's extent.
  if y-x>.501:continue
  for target in targets:
   row=rows[x];nextrow=rows[y];a=min(row,key=lambda z:abs(z-target));b=min(nextrow,key=lambda z:abs(z-target));p,pa,pd=row[a];q,qa,qd=nextrow[b];edge(d,p,q,4,0.,pa,qa,pd,qd)
 return d
back=bore(list(retained.all_objects),False);forward=empty()
for side in ['HALF_0','HALF_1']:
 d=bore([o for o in front.all_objects if side in o.name],True);base=len(forward['vs']);forward['vs'].extend(d['vs']);forward['es'].extend((a+base,b+base) for a,b in d['es'])
 for key in ['axis','coord','boundary','delta']:forward[key].extend(d[key])
# Geometry Nodes filters dense edge guides. Native viewport wire rasterization
# supplies screen-space line width; no Curve-to-Mesh or material strips exist.
g=bpy.data.node_groups.new('WORLD pixel guide controls v002','GeometryNodeTree');g.use_fake_user=True
spec=[('Geometry','INPUT','NodeSocketGeometry',None),('Geometry','OUTPUT','NodeSocketGeometry',None),('Enabled','INPUT','NodeSocketBool',False),('Show cut faces','INPUT','NodeSocketBool',True),('Show seabed','INPUT','NodeSocketBool',True),('Show bore','INPUT','NodeSocketBool',True),('Component','INPUT','NodeSocketInt',0),('Depth spacing m','INPUT','NodeSocketFloat',25.),('Radial spacing m','INPUT','NodeSocketFloat',10.),('Seabed spacing m','INPUT','NodeSocketFloat',10.),('Bore ring spacing m','INPUT','NodeSocketFloat',15.)]
for name,side,typ,value in spec:
 sock=g.interface.new_socket(name=name,in_out=side,socket_type=typ)
 if value is not None:sock.default_value=value
n=g.nodes;l=g.links;i=n.new('NodeGroupInput');o=n.new('NodeGroupOutput')
def op(typ,a,b=None):
 node=n.new('ShaderNodeMath');node.operation=typ
 for ix,v in enumerate([a,b]):
  if v is None:continue
  if isinstance(v,(int,float)):node.inputs[ix].default_value=v
  else:l.new(v,node.inputs[ix])
 return node.outputs[0]
def choose(test,a,b,typ='FLOAT'):
 node=n.new('GeometryNodeSwitch');node.input_type=typ;l.new(test,node.inputs['Switch']);l.new(a,node.inputs['True']);l.new(b,node.inputs['False']);return node.outputs[0]
axis=n.new('GeometryNodeInputNamedAttribute');axis.data_type='FLOAT';axis.inputs['Name'].default_value='grid_axis';co=n.new('GeometryNodeInputNamedAttribute');co.data_type='FLOAT';co.inputs['Name'].default_value='grid_coordinate'
spacing=choose(op('COMPARE',axis.outputs['Attribute'],3.),i.outputs['Bore ring spacing m'],choose(op('COMPARE',axis.outputs['Attribute'],2.),i.outputs['Seabed spacing m'],choose(op('COMPARE',axis.outputs['Attribute'],1.),i.outputs['Radial spacing m'],i.outputs['Depth spacing m'])))
keep=op('LESS_THAN',op('MODULO',co.outputs['Attribute'],op('MAXIMUM',spacing,1.)),.001)
delete=n.new('GeometryNodeDeleteGeometry');delete.domain='EDGE';l.new(i.outputs['Geometry'],delete.inputs['Geometry']);l.new(op('SUBTRACT',1.,keep),delete.inputs['Selection'])
show=choose(op('COMPARE',i.outputs['Component'],2.),i.outputs['Show bore'],choose(op('COMPARE',i.outputs['Component'],1.),i.outputs['Show seabed'],i.outputs['Show cut faces'],'BOOLEAN'),'BOOLEAN')
sw=n.new('GeometryNodeSwitch');sw.input_type='GEOMETRY';l.new(op('MULTIPLY',i.outputs['Enabled'],show),sw.inputs['Switch']);l.new(delete.outputs[0],sw.inputs['True']);l.new(sw.outputs[0],o.inputs[0])
records=[]
for name,d,component in [('WORLD_PIXEL_CUT_FACES',cut,0),('WORLD_PIXEL_SEABED',top,1),('WORLD_PIXEL_BORE_RETAINED',back,2),('WORLD_PIXEL_BORE_FRONT',forward,2)]:
 me=bpy.data.meshes.new(name);me.from_pydata(d['vs'],d['es'],[]);me.update()
 for attr,values,domain in [('grid_axis',d['axis'],'EDGE'),('grid_coordinate',d['coord'],'EDGE'),('front_boundary',d['boundary'],'POINT'),('front_delta',d['delta'],'POINT')]:a=me.attributes.new(attr,'FLOAT',domain);a.data.foreach_set('value',values)
 ob=bpy.data.objects.new(name,me);root.objects.link(ob);ob.display_type='WIRE';ob.show_wire=True;ob.show_all_edges=True;ob.color=(.08,.07,.06,1)
 m=ob.modifiers.new('Pixel guide spacing and visibility','NODES');m.node_group=g
 ident=next(x.identifier for x in g.interface.items_tree if getattr(x,'in_out','')=='INPUT' and x.name=='Component');getattr(m.properties.inputs,ident).value=component
 ob['component']=component;ob['meaning']='Viewport wire edges only; zero faces, no world-space stroke thickness. Bore guide consumer also uses shared presentation group for clearance/reveal.'
 records.append({'object':name,'vertices':len(me.vertices),'edges':len(me.edges),'faces':len(me.polygons)})
text=bpy.data.texts.new('START HERE pixel motion guides');text.write('Native viewport wire guides, no surface strips. Enabled off by default. Cut faces, seabed, bore can toggle independently; spacing controls filter edge attributes. Bore data sampled from World v014, offset3mm toward cavity, longitudinal guides plus selectable ring intervals. Consumer applies original clearance/front-reveal groups to bore edges. Use pixel_guides_viewport.py GPU install/export for fixed pixel strokes; native Viewport Render omits that custom overlay. No camera/time dependence in guide data. Not measurement information.\n')
bpy.context.scene.name='World optional pixel stroke guides';bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True);bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True)
assert hashlib.sha256(world.read_bytes()).hexdigest()==source_hash
d={'native':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'source_world':str(world),'source_world_sha256':source_hash,'node_group':g.name,'records':records,'stroke':'Edge-only source data; pixel_guides_viewport.py supplies fixed-pixel GPU strokes and depth-tested exports.','default_enabled':False,'consumer':'S01-S02 production v005 only','controls':{'Depth spacing m':25,'Radial spacing m':10,'Seabed spacing m':10,'Bore ring spacing m':15},'source_spacing_resolution_m':1,'bore_offset_m':.003,'seabed_hole_exclusion_m':1.,'status':'Reference guide trial; no measured-data meaning or tested AI finishing.'}
(B/'World_motion_grid_interface_v002.json').write_text(json.dumps(d,indent=2));(Q/'Notes/pixel_grid_v002_build.json').write_text(json.dumps(d,indent=2));print('PIXEL_GRID_V002_READY',records)
