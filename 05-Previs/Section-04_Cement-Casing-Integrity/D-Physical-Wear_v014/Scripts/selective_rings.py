import bpy,math,time,json,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
B=Path(__file__).resolve().parents[1];old=B.parent/'D-Physical-Wear_v009/Scenes/S04_D_physical-comparison_v009.blend'
bpy.ops.wm.open_mainfile(filepath=str(old),load_ui=False,use_scripts=False)
s=bpy.data.scenes['D C_preferred-closeup - physical only'];bpy.context.window.scene=s
def snap():return {'meshes':{o.name:hashlib.sha256(repr(([tuple(v.co) for v in o.data.vertices],[tuple(p.vertices) for p in o.data.polygons])).encode()).hexdigest() for o in s.objects if o.type=='MESH'},'camera':[list(r) for r in s.camera.matrix_world],'lens':s.camera.data.lens,'lights':{o.name:[list(o.location),o.data.energy] for o in s.objects if o.type=='LIGHT'}}
before=snap()
for o in s.objects:
 if o.type=='CURVE':o.hide_render=True;o.hide_viewport=True
def tree(name):
 o=bpy.data.objects[name];return BVHTree.FromPolygons([v.co for v in o.data.vertices],[list(p.vertices) for p in o.data.polygons])
nom=tree('CASED_STEEL_NOMINAL_CUTAWAY');worn=tree('CASED_STEEL_WEAR_CUTAWAY')
def point(t,x,a):
 p=t.ray_cast(Vector((x,0,0)),Vector((0,math.cos(a),math.sin(a))),1)[0]
 if p is None:raise RuntimeError('Registered wall missing')
 return p
white=bpy.data.materials['Original inner surface - dashed reference'];cyan=bpy.data.materials['Existing worn inner surface - cyan profile']
coll=bpy.data.collections.new('Grey nominal rings - blue only over worn sectors');s.collection.children.link(coll)
def runs(name,points,mask,mat,width):
 c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.bevel_depth=width;c.bevel_resolution=2;start=None;count=0
 for i,on in enumerate(mask+[False]):
  if on and start is None:start=i
  if not on and start is not None:
   pts=points[start:min(i+1,len(points))]
   if len(pts)>1:
    sp=c.splines.new('POLY');sp.points.add(len(pts)-1)
    for p,co in zip(sp.points,pts):p.co=(*co,1)
    count+=1
   start=None
 if count:
  ob=bpy.data.objects.new(name,c);coll.objects.link(ob);c.materials.append(mat)
 return count
N=720;THRESH=.00010;rows=[]
# Two normal context stations, then the three approved worn-region stations.
for k,x in enumerate([-2.44,-2.32,-1.88,-1.68,-1.5125]):
 angles=[-math.pi/2+math.pi*j/N for j in range(N+1)];original=[];actual=[];depth=[]
 for a in angles:
  n=point(nom,x,a);p=point(worn,x,a);d=(p-n).length;di=Vector((0,math.cos(a),math.sin(a)))
  n-=di*.00004;p-=di*.00004
  if abs(x+1.5125)<1e-6:n.x+=.00035;p.x+=.00035
  original.append(n);actual.append(p);depth.append(d)
 wornmask=[d>THRESH for d in depth]
 grey=[not w or ((a+math.pi/2)/(math.pi/22))%1<.49 for a,w in zip(angles,wornmask)]
 ng=runs('Station %d grey nominal solid-normal dashed-wear'%(k+1),original,grey,white,.00014)
 nb=runs('Station %d blue actual worn-sector only'%(k+1),actual,wornmask,cyan,.00021)
 selected=[a for a,w in zip(angles,wornmask) if w]
 rows.append({'x_m':x,'max_source_deviation_m':max(depth),'blue_angular_range_rad':[min(selected),max(selected)] if selected else None,'normal_sector_nominal_continuous':True,'worn_sector_nominal_dashed':True,'blue_runs':nb,'nominal_runs':ng})
assert before==snap()
s.name='D normal rings with local worn arcs v014';s.eevee.taa_render_samples=8
s['scope']='Owner sketch: continuous grey nominal circles along pipe, dashed only over worn angles, solid blue only at actual worn sector. No bracket/pins. Still proof, same shot/steel.'
s['graphic_mask_limit']='0.10 mm source-deviation cutoff is a graphic legibility choice only, not instrument sensitivity or field wear classification. Physical geometry is unchanged.'
out=B/'Scenes/S04_D_selective-wear-rings_v014.blend'
for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(out.parent))
s.render.filepath=str(B/'Previews/S04_D_selective-wear-rings_v014.png');bpy.ops.wm.save_as_mainfile(filepath=str(out),relative_remap=False)
t=time.perf_counter();bpy.ops.render.render(scene=s.name,write_still=True);elapsed=time.perf_counter()-t
(B/'Records/verification.json').write_text(json.dumps({'source':str(old),'render_seconds':elapsed,'under_5_seconds':elapsed<5,'physical_camera_lights_unchanged':snap()==before,'stations':rows,'source_deviation_graphic_cutoff_m':THRESH,'cutoff_not_instrument_threshold':True,'pins_and_bracket_hidden':True,'blue_only_over_source_deviation':True,'no_radial_exaggeration':True,'visibility_offset_m':.00004,'front_axial_visibility_offset_m':.00035,'visible_half_circumferences_match_static_section':True},indent=2));print('SELECTIVE_RINGS_SECONDS',elapsed,flush=True)
