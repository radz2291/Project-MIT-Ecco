"""Independent read-only source/Surface/World/demo inspection; no native saves."""
import bpy,json,hashlib,struct,array
from pathlib import Path
from mathutils import Vector,Matrix
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');T=R/'04-Production/Records/Tasks/T-055/Revision_v006';A=R/'04-Production/Shared/Assets'
surface=A/'Environment/Surface/Surface_descent_v006.blend';world=A/'Environment/Borehole/World_environment_v011.blend';demo=R/'04-Production/Shared/Demos/Surface_descent_demo_v002.blend';worlddemo=R/'04-Production/Shared/Demos/World_demo_v002.blend'
sources=json.loads((R/'04-Production/Records/Tasks/T-050/sources.json').read_text());source=next(x for x in sources if x['id']=='S02');src=R/source['native']
paths=[src,surface,world,demo,worlddemo];initial={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
result={'verifier':'ECCO-052 independent of Surface/World/demo authors','scope':'read-only background Blender; official MCP path query first; dirty interactive scene untouched','checks':{}}
def opened(p):bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False)
def bounds(o):
    v=[o.matrix_world@Vector(x) for x in o.bound_box];return {'min':[min(x[k] for x in v) for k in range(3)],'max':[max(x[k] for x in v) for k in range(3)]}
def meshdata(o,matrix=None):
    mat=matrix if matrix is not None else o.matrix_world
    return ([tuple(mat@v.co) for v in o.data.vertices],[tuple(p.vertices) for p in o.data.polygons])
def cameras(s):
    out=[]
    for f in range(1,529):
        s.frame_set(f);o=s.camera.evaluated_get(bpy.context.evaluated_depsgraph_get());out.append({'frame':f,'matrix':[list(r) for r in o.matrix_world],'lens':o.data.lens})
    return out
def libraries():return [{'path':l.filepath,'exists':Path(bpy.path.abspath(l.filepath)).is_file()} for l in bpy.data.libraries]
def meshes():
    out={}
    for o in bpy.data.objects:
        if o.type!='MESH':continue
        a=array.array('f',[0.0])*(len(o.data.vertices)*3);o.data.vertices.foreach_get('co',a);h=hashlib.sha256(a.tobytes())
        loops=array.array('i',[0])*len(o.data.loops);o.data.loops.foreach_get('vertex_index',loops);h.update(loops.tobytes())
        counts=array.array('i',[0])*len(o.data.polygons);o.data.polygons.foreach_get('loop_total',counts);h.update(counts.tobytes())
        if o.data.shape_keys:
            for key in o.data.shape_keys.key_blocks:
                a=array.array('f',[0.0])*(len(key.data)*3);key.data.foreach_get('co',a);h.update(a.tobytes())
        out[o.name]={'mesh_sha256':h.hexdigest(),'matrix':[list(row) for row in o.matrix_world]}
    return out
opened(src);original_cameras=cameras(bpy.context.scene);bpy.context.scene.frame_set(528);wall=bpy.data.objects['S02 geological wall retained section'];source_wall=meshdata(wall)
result['source']={'path':str(src),'sha256':initial[str(src)],'matches_T050':initial[str(src)]==source['sha256'],'wall_vertices':len(source_wall[0]),'wall_polygons':len(source_wall[1])}
opened(surface)
pont=[{'name':o.name,**bounds(o)} for o in bpy.data.objects if 'SubmergedPontoon' in o.name]
deck=[{'name':o.name,**bounds(o)} for o in bpy.data.objects if 'MoonpoolCrossDeck' in o.name or 'DeckWing' in o.name]
cols=list(bpy.data.collections.keys());geology=[o.name for o in bpy.data.objects if any(k in o.name.lower() for k in ['earth','geolog','formation','soil','seabed'])]
result['surface']={'objects':len(bpy.data.objects),'cameras_lights':[o.name for o in bpy.data.objects if o.type in ('CAMERA','LIGHT')],'actions':list(bpy.data.actions.keys()),'geology_candidates':geology,'collections':cols,'pontoons':pont,'deck':deck,'libraries':libraries()}
result['checks']['pontoons_submerged']=bool(pont) and all(x['max'][2]<0 for x in pont)
result['checks']['deck_above_sea']=bool(deck) and all(x['min'][2]>0 for x in deck)
result['checks']['ocean_alternatives_retained']=all(c in cols for c in ['SURFACE_OCEAN_FULL','SURFACE_OCEAN_CUTAWAY'])
result['checks']['surface_no_geology_camera_light_action']=not geology and not result['surface']['cameras_lights'] and not result['surface']['actions']
M=Matrix(json.loads((A/'Environment/Borehole/World_interface_v011.json').read_text())['canonical_to_s02'])
opened(A/'Environment/Borehole/World_environment_v010.blend');pw=bpy.data.objects['WORLD_S02_PHYSICAL_CUTAWAY_MESH'];predecessor_wall=meshdata(pw,M@pw.matrix_world);old_meshes=meshes()
opened(world)
new_meshes=meshes();result['checks']['all_predecessor_meshes_unchanged']=all(new_meshes.get(k)==v for k,v in old_meshes.items());result['predecessor_mesh_count']=len(old_meshes)
result['checks']['world_no_cameras_lights_actions']=not bpy.data.actions and not any(o.type in ('CAMERA','LIGHT') for o in bpy.data.objects)
w=bpy.data.objects['WORLD_S02_PHYSICAL_CUTAWAY_MESH'];new_wall=meshdata(w,M@w.matrix_world)
delta=max((Vector(a)-Vector(b)).length for a,b in zip(source_wall[0],new_wall[0])) if len(source_wall[0])==len(new_wall[0]) else None
inner=[i for i,v in enumerate(new_wall[0]) if v[0]*v[0]+v[1]*v[1]<1]
inner_delta=max((Vector(source_wall[0][i])-Vector(new_wall[0][i])).length for i in inner) if len(source_wall[0])==len(new_wall[0]) and inner else None
result['world']={'exact_wall_vertices':len(new_wall[0]),'max_source_wall_vertex_delta_m':delta,'source_inner_vertex_delta_m':inner_delta,'source_inner_vertices':len(inner),'topology_matches':source_wall[1]==new_wall[1],'predecessor_v010_wall_exact':predecessor_wall==new_wall,'connected_members':[o.name for o in bpy.data.collections['WORLD_DESCENT_CONNECTED'].all_objects],'wall_action':bool(w.animation_data and w.animation_data.action),'libraries':libraries(),'scope':'v010 expanded outer soil preserved exactly; original S02 inner bore compared separately.'}
result['checks']['exact_wall_geometry']=predecessor_wall==new_wall and inner_delta is not None and inner_delta<1e-4 and source_wall[1]==new_wall[1]
opened(demo);s=bpy.data.scenes['Descent — connected S01-S02'];bpy.context.window.scene=s;democam=cameras(s)
result['checks']['all528_camera_lens_identical']=democam==original_cameras
prefixes=('Cutaway earth','Formation rear','Earth seam','Opening front')
old=[o.name for o in s.objects if o.name.startswith(prefixes) or o.name in ['Ocean horizon','Seabed around drilled opening','S02 geological wall retained section','Main solid building']]
inst=s.objects['One continuous physical World'];states=[]
for f in [1,240,241,528]:
    s.frame_set(f);e=inst.evaluated_get(bpy.context.evaluated_depsgraph_get());states.append({'frame':f,'scale':list(e.scale),'matrix':[list(r) for r in e.matrix_world],'hide_render':e.hide_render,'collection':e.instance_collection.name if e.instance_collection else None})
result['demo']={'scenes':list(bpy.data.scenes.keys()),'old_slab_objects':old,'world_instance_states':states,'world_action':bool(inst.animation_data and inst.animation_data.action),'world_drivers':len(inst.animation_data.drivers) if inst.animation_data else 0,'libraries':libraries()}
result['checks']['no_old_slabs']=not old
result['checks']['world_present_constant_from1']=all(not x['hide_render'] and x['collection']=='WORLD_DESCENT_CONNECTED' and x['matrix']==states[0]['matrix'] for x in states) and not result['demo']['world_action'] and not result['demo']['world_drivers']
opened(worlddemo);result['world_demo']={'libraries':libraries(),'scenes':list(bpy.data.scenes.keys())};result['checks']['world_demo_links_v011']=any(x['path'].endswith('World_environment_v011.blend') for x in result['world_demo']['libraries'])
result['checks']['libraries_resolve']=all(x['exists'] for key in ['surface','world','demo','world_demo'] for x in result[key]['libraries'])
result['checks']['native_inputs_unchanged']=all(hashlib.sha256(p.read_bytes()).hexdigest()==initial[str(p)] for p in paths)
result['native_hashes']=initial
result['checks']['released_world_hash']=initial[str(world)]=='39387e654f33ff63931f7863860b957064777c3587fe1a4f6207d8003589e8df'
result['pass']=all(result['checks'].values()) and result['source']['matches_T050'];result['review_state']='Final released native read-only verification; visual acceptance belongs to Radzi. No render performed.'
(T/'independent-verification-final.json').write_text(json.dumps(result,indent=2));print(json.dumps({'pass':result['pass'],'checks':result['checks']},indent=2),flush=True)
