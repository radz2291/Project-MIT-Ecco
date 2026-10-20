import bpy,math,json,hashlib,time,sys
from pathlib import Path
from mathutils import Matrix,Vector
B=Path(__file__).resolve().parents[1];ROOT=B.parents[2]
old=ROOT/'05-Previs/Section-04_Cement-Casing-Integrity/Cinematic-Previs_v005/Scenes/S04_cinematic-previs_v005.blend'
src=ROOT/'05-Previs/Section-02_Measurement-History/v011/Continuation/Scenes/S01-S02_continuous_v011.blend'
out=B/'Scenes/S04_cinematic-previs_v006.blend'
def build():
 bpy.ops.wm.open_mainfile(filepath=str(old),use_scripts=False,load_ui=False)
 original={o.name:[list(v.co) for v in o.data.vertices] for o in bpy.context.scene.objects if o.type=='MESH' and (o.name.startswith('Steel -') or 'organic' in o.name or 'Cement ' in o.name)}
 with bpy.data.libraries.load(str(src),link=False) as (a,b):b.objects=['S02 geological wall retained section']
 source=b.objects[0];assert source is not None
 info=dict(name=source.name,vertices=len(source.data.vertices),materials=[m.name for m in source.data.materials],modifiers=[m.type for m in source.modifiers])
 print('S02_SOURCE',json.dumps(info),flush=True)
 # Reuse the approved S02 environment mesh and its actual Earth-stratum material.
 # Its geological borehole becomes outer formation, never the inner steel wall.
 source.animation_data_clear();source.parent=None;source.matrix_world=Matrix.Identity(4)
 source.data=source.data.copy();source.data.name='S02 geological wall - S04 outer-formation derivative'
 rr=[math.hypot(v.co.x,v.co.y) for v in source.data.vertices];rmin=min(rr);rmax=max(rr)
 for v in source.data.vertices:
  x,y,z=v.co;r=math.hypot(x,y);angle=math.atan2(y,x)
  # Translate original depth -735 to S04 X=-1.5. Reuse longitudinal scale.
  # Fit formation contact exactly outside cement, preserving outer roughness.
  radius=3.5 if r>.31 else .22225+max(0,r-rmin)
  v.co=(z+733.5,radius*math.cos(angle),radius*math.sin(angle))
 for poly in source.data.polygons:poly.use_smooth=True
 source.name='Section 2 geological surroundings - outside cement';bpy.context.scene.collection.objects.link(source);source.hide_render=False;source.hide_viewport=False
 for mod in list(source.modifiers):source.modifiers.remove(mod)
 mat=source.data.materials[0].copy();mat.name='Section 2 Earth stratum 20 - S04 viewing window';mat.animation_data_clear()
 if mat.node_tree:mat.node_tree.animation_data_clear()
 mat.use_nodes=True
 bs=mat.node_tree.nodes.get('Principled BSDF')
 if bs:bs.inputs['Base Color'].default_value=mat.diffuse_color;bs.inputs['Roughness'].default_value=.9
 print('EARTH_COLOR',list(mat.diffuse_color),flush=True)
 for slot in source.material_slots:slot.link='OBJECT';slot.material=mat
 sys.path.insert(0,str(ROOT/'05-Previs/Section-04_Cement-Casing-Integrity/Cinematic-Previs_v005/Scripts'))
 from base_scene import window_material
 window_material(mat,-1.48,1.48)
 for n in mat.node_tree.nodes:
  if n.type=='MAP_RANGE' and abs(n.inputs['From Min'].default_value+.29)<1e-4:n.inputs['From Min'].default_value=100;n.inputs['From Max'].default_value=110
 # Replace old consumer geology only. Other layers and their animations stay intact.
 for name in ['Formation facing inspection window','Formation retained rear ground']:
  o=bpy.data.objects.get(name)
  if o:o.hide_render=True;o.hide_viewport=True
 # Retained opposite half provides ground on both sides of the cutaway.
 rear=source.copy();rear.data=source.data;rear.name='Section 2 retained opposite ground';bpy.context.scene.collection.objects.link(rear);rear.rotation_euler.x=math.pi
 raw=source.data.materials[0];rear.material_slots[0].link='OBJECT';rear.material_slots[0].material=mat
 assert original=={o.name:[list(v.co) for v in o.data.vertices] for o in bpy.context.scene.objects if o.name in original}
 s=bpy.context.scene;s.frame_set(1)
 for l in bpy.data.libraries:l.filepath=bpy.path.relpath(bpy.path.abspath(l.filepath),start=str(out.parent))
 bpy.ops.wm.save_as_mainfile(filepath=str(out),relative_remap=False)
 report=dict(source=str(src),source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),source_object=info,original_radius_range=[rmin,rmax],new_min_formation_radius=.22225,adaptation='Original Z depth mapped to S04 X. Radial contact fits outside unchanged cement; only outer soil thickness expanded for frame coverage. No open-hole wall inside steel.',preserved='S04 casing/cement/channel meshes, camera and acoustic timing unchanged',geometry_check=True)
 (B/'Records/revision.json').write_text(json.dumps(report,indent=2))
def render(mode):
 bpy.ops.wm.open_mainfile(filepath=str(out),use_scripts=False,load_ui=False);s=bpy.context.scene;rows=[]
 for f in ([1,116,292,432] if mode=='benchmark' else range(1,433)):
  s.frame_set(f);s.render.filepath=str(B/('Previews' if mode=='benchmark' else 'Work')/f'S04_{f:04d}.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t;rows.append(dict(frame=f,seconds=dt));(B/'Records'/('timings-'+mode+'.json')).write_text(json.dumps(rows,indent=2));print('FRAME',f,dt,flush=True)
  if dt>=5:raise RuntimeError('Frame cap exceeded')
mode=sys.argv[sys.argv.index('--')+1] if '--' in sys.argv else 'build'
if mode=='build':build()
else:render(mode)
