import bpy,bmesh,math,json,time,sys,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
B=Path(__file__).resolve().parents[1];OLD=B.parent/'Communication-Test_v008';R=B.parents[2]
PHI=math.radians(39);RAD=Vector((0,math.cos(PHI),math.sin(PHI)));TAN=Vector((0,-RAD.z,RAD.y));CUT=.00005
def dump(n,v):(B/'Records'/n).write_text(json.dumps(v,indent=2))
def material(name,c,a=1):
 m=bpy.data.materials.new(name);m.diffuse_color=(*c,a);return m
def mesh(name,verts,faces,m):
 d=bpy.data.meshes.new(name);d.from_pydata(verts,[],faces);d.update();o=bpy.data.objects.new(name,d);bpy.context.scene.collection.objects.link(o);d.materials.append(m);return o
def visibility(o,values,step=False):
 m=o.data.materials[0];color=list(m.diffuse_color[:3])
 for f,a in enumerate(values,1):
  m.diffuse_color=(*color,a);m.keyframe_insert('diffuse_color',frame=f);o.hide_render=a<.003;o.hide_viewport=o.hide_render;o.keyframe_insert('hide_render',frame=f);o.keyframe_insert('hide_viewport',frame=f)
 for act in [m.animation_data.action,o.animation_data.action]:
  for layer in act.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for fc in bag.fcurves:
      for k in fc.keyframe_points:k.interpolation='CONSTANT' if step or fc.data_path.startswith('hide') else 'LINEAR'
def source_formation():
 # Read the same locally imported Section 2 wall used by v006/v008; masters untouched.
 bpy.ops.wm.open_mainfile(filepath=str(B.parent/'Cinematic-Previs_v006/Scenes/S04_cinematic-previs_v006.blend'),use_scripts=False,load_ui=False)
 o=bpy.data.objects['Section 2 geological surroundings - outside cement'];return BVHTree.FromPolygons([o.matrix_world@v.co for v in o.data.vertices],[tuple(p.vertices) for p in o.data.polygons])
def solid_formation(xc,tree):
 nx=64;na=48;outer=.95;vs=[];hits=0;fallback=0;inner=[]
 for layer in range(2):
  for i in range(nx+1):
   x=xc-1.2+2.4*i/nx
   for j in range(na+1):
    a=PHI-math.pi+math.pi*j/na;di=Vector((0,math.cos(a),math.sin(a)))
    if layer==0:
     hit=tree.ray_cast(Vector((x,0,0)),di,2)[0]
     if hit is None:rad=.25;fallback+=1
     else:rad=max(.22225,math.hypot(hit.y,hit.z));hits+=1
     inner.append(rad)
    else:rad=outer
    vs.append(tuple(Vector((x,0,0))+di*rad))
 n=(nx+1)*(na+1);idx=lambda i,j:i*(na+1)+j;faces=[];is_cap=[]
 for i in range(nx):
  for j in range(na):
   q=[idx(i,j),idx(i+1,j),idx(i+1,j+1),idx(i,j+1)];faces.extend([tuple(reversed(q)),tuple(k+n for k in q)]);is_cap.extend([False,False])
 for i in range(nx):
  for j in [0,na]:faces.append((idx(i,j),idx(i+1,j),idx(i+1,j)+n,idx(i,j)+n));is_cap.append(True)
 for j in range(na):
  for i in [0,nx]:faces.append((idx(i,j),idx(i,j+1),idx(i,j+1)+n,idx(i,j)+n));is_cap.append(False)
 o=mesh('FORMATION - closed source-guided continuation to frame edge',vs,faces,material('Formation earth base',(.205,.16,.115)))
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));assert all(e.is_manifold for e in bm.edges);bm.to_mesh(o.data);bm.free()
 # Quiet coherent strata: per-face display color only, no shader cost or deformation.
 palette=[]
 for k in range(16):
  q=(k-7.5)/7.5;palette.append(material('Restrained formation tone '+str(k),(.205+q*.016,.16+q*.013,.115+q*.009)))
 o.data.materials.clear()
 for m in palette:o.data.materials.append(m)
 for p in o.data.polygons:
  x=sum(o.data.vertices[v].co.x for v in p.vertices)/len(p.vertices);tone=.5+.28*math.sin((x-xc)*13)+.12*math.sin((x-xc)*31+.7);p.material_index=max(0,min(15,int(tone*15)));p.use_smooth=False
 o['meaning']='Closed geological context volume extending outside source-guided inner wall; not an acoustic data reconstruction'
 o['limits']='Existing source is sectioned; unseen angular sectors use a nominal context continuation, not field geometry'
 return dict(object=o.name,closed_manifold=True,inner_radius_bounds_m=[min(inner),max(inner)],outer_radius_m=outer,source_guided_samples=hits,unseen_sector_context_samples=fallback,axial_bounds_m=[xc-1.2,xc+1.2],section_plane_offset_m=0)
def digital_finish(envelopes):
 rows=[]
 for k in range(24):
  wall=bpy.data.objects['STEEL-ATTACHED resonance band '+str(k)];cap=bpy.data.objects['STEEL THICKNESS response '+str(k)];base=envelopes[k]
  visibility(wall,[a*.10 for a in base])
  # cap shares wall's material; key only its visibility.
  for f,a in enumerate(base,1):
   cap.hide_render=a*.10<.003;cap.hide_viewport=cap.hide_render;cap.keyframe_insert('hide_render',frame=f);cap.keyframe_insert('hide_viewport',frame=f)
  cp=[v.co.copy() for v in cap.data.vertices]
  for j in range(4):
   # Four long, thin segments across the wall thickness, flush to its exposed face.
   t0=j/4;t1=(j+1)/4;verts=[cp[0].lerp(cp[3],t0)+TAN*.00003,cp[1].lerp(cp[2],t0)+TAN*.00003,cp[1].lerp(cp[2],t1)+TAN*.00003,cp[0].lerp(cp[3],t1)+TAN*.00003];faces=[(0,1,2,3)]
   used=sorted({v for p in list(wall.data.polygons)[j*4:(j+1)*4] for v in p.vertices});mapping={v:i+4 for i,v in enumerate(used)}
   for v in used:
    p=wall.data.vertices[v].co.copy();di=Vector((0,p.y,p.z)).normalized();verts.append(p-di*.000025)
   faces.extend(tuple(mapping[v] for v in p.vertices) for p in list(wall.data.polygons)[j*4:(j+1)*4])
   color=(.30,.91,.98) if (k*13+j)%17==0 else (.12,.78,.90);m=material('Acquisition scan segment '+str((k,j)),color,0);o=mesh('STEEL-BOUND acquisition segment '+str((k,j)),verts,faces,m);values=[]
   for f,a in enumerate(base,1):
    dt=(f-1)/24-1.2;tick=(f-30)//(2 if dt<.32 else 4)
    seed=(((k+1)*73856093)^((j+1)*19349663)^((tick+1)*83492791))&0xffffffff;seed^=seed>>13;seed=(seed*1274126177)&0xffffffff;seed=(seed^(seed>>16))%101
    gate=0 if seed<(48 if dt<.32 else 18) else 1
    if (k+tick)%13==0:gate*=.20
    values.append(a*.95*gate)
   visibility(o,values,step=True);o['meaning']='Display acquisition glitch anchored to the casing; multiplied by unchanged v008 response envelope. Not physical steel motion or permanent stored wall data.'
   rows.append(dict(band=k,segment=j,frames_visible=sum(v>=.003 for v in values),max_alpha=max(values)))
 return rows
def build(case):
 tree=source_formation();src=OLD/'Scenes'/f'S04_{case}_capped-resonance_v008.blend';bpy.ops.wm.open_mainfile(filepath=str(src),use_scripts=False,load_ui=False);s=bpy.context.scene
 baseline=[]
 for f in range(1,121):
  s.frame_set(f);baseline.append([bpy.data.objects['STEEL-ATTACHED resonance band '+str(k)].data.materials[0].diffuse_color[3] for k in range(24)])
 envelopes=[[baseline[f][k] for f in range(120)] for k in range(24)]
 e=json.loads((OLD/'Records'/f'build-{case}.json').read_text())['event'];xc=e['emitter_world_m'][0]
 oldrock=bpy.data.objects['Section 2 geological surroundings - outside cement'];oldrock.hide_render=True;oldrock.hide_viewport=True
 formation=solid_formation(xc,tree);segments=digital_finish(envelopes);s['scope']='v009 two owner-approved amendments only: rock context and acquisition glitch. B/C bounded proof; D paused; full integration unreleased.'
 s.frame_set(1);out=B/'Scenes'/f'S04_{case}_formation-acquisition_v009.blend'
 for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(out.parent))
 bpy.ops.wm.save_as_mainfile(filepath=str(out),relative_remap=False)
 dump('build-'+case+'.json',dict(predecessor=str(src),predecessor_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),native=str(out),formation=formation,segments=segments,event=e,envelope=envelopes,camera='Unchanged v008 camera and key state',physical_geometry='v008 tool, steel, cement, channel and fluid gap preserved exactly; rock context successor only',display='10 percent underlying smooth carrier plus envelope-gated acquisition segments. Same pattern family B/C, no moved geometry.'))
def render(case,benchmark):
 bpy.ops.wm.open_mainfile(filepath=str(B/'Scenes'/f'S04_{case}_formation-acquisition_v009.blend'),use_scripts=False,load_ui=False);s=bpy.context.scene;rows=[]
 for f in ([1,32,35,42,55,78] if benchmark else range(1,121)):
  s.frame_set(f);s.render.filepath=str(B/('Previews' if benchmark else 'Work')/f'{case}_{f:04d}.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t;rows.append(dict(frame=f,seconds=dt));dump(('benchmark-' if benchmark else 'timings-')+case+'.json',rows);print(case,f,dt,flush=True)
  if dt>=5:raise RuntimeError('Render cap exceeded')
if __name__=='__main__':
 args=sys.argv[sys.argv.index('--')+1:];mode,case=args[:2]
 if mode=='build':build(case)
 else:render(case,mode=='benchmark')
