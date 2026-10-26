"""Read-only native inventory. Run with Blender --background --disable-autoexec --python.

No source save, render, relink, or datablock modification is performed.
"""
import bpy, json, hashlib, pathlib, sys, time, traceback, array

ROOT = pathlib.Path(__file__).resolve().parents[5]
TASK = ROOT / '04-Production/Records/Tasks/T-049'
CONFIG = json.loads((TASK / 'sources.json').read_text(encoding='utf-8'))

def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1024*1024), b''): h.update(block)
    return h.hexdigest()

def lib(x):
    return bpy.path.abspath(x.library.filepath) if x and x.library else None

def animation(x):
    ad = getattr(x, 'animation_data', None)
    if not ad: return None
    act = ad.action
    curves = []
    if act:
        try:
            for layer in act.layers:
                for strip in layer.strips:
                    for bag in strip.channelbags:
                        for fc in bag.fcurves:
                            curves.append([fc.data_path, fc.array_index, [[*k.co, k.interpolation] for k in fc.keyframe_points]])
        except Exception: pass
    return {'action':act.name if act else None,'keys':curves,'drivers':[d.data_path for d in ad.drivers]}

def inspect(item):
    p=ROOT/item['native']; before=sha(p); start=time.perf_counter()
    bpy.ops.wm.open_mainfile(filepath=str(p), load_ui=False)
    meshes={}
    for m in bpy.data.meshes:
        a=array.array('f', [0.0])*(len(m.vertices)*3); m.vertices.foreach_get('co',a)
        ids=array.array('i',[0])*len(m.loops); m.loops.foreach_get('vertex_index',ids)
        meshes[m.name_full]={'vertices':len(m.vertices),'polygons':len(m.polygons),'geometry_sha256':hashlib.sha256(a.tobytes()+ids.tobytes()).hexdigest(),'library':lib(m)}
    objects=[]
    for o in bpy.data.objects:
        objects.append({'name':o.name_full,'type':o.type,'library':lib(o),'data':o.data.name_full if o.data else None,'data_library':lib(o.data),'parent':o.parent.name_full if o.parent else None,'instance':o.instance_collection.name_full if o.instance_collection else None,'instance_library':lib(o.instance_collection),'collections':[c.name_full for c in o.users_collection],'matrix':[list(r) for r in o.matrix_world],'dimensions':list(o.dimensions),'hide_render':o.hide_render,'materials':[m.name_full if m else None for m in o.data.materials] if o.data and hasattr(o.data,'materials') else [],'animation':animation(o),'custom':{k:str(v)[:1000] for k,v in o.items() if k!='_RNA_UI'},'text':o.data.body if o.type=='FONT' else None})
    materials=[]
    for m in bpy.data.materials:
        nodes=[]
        if m.use_nodes:
            for n in m.node_tree.nodes:
                inputs={}
                for s in n.inputs:
                    if not hasattr(s,'default_value'): continue
                    v=s.default_value
                    try: v=list(v)
                    except TypeError: v=str(v) if not isinstance(v,(str,int,float,bool)) else v
                    inputs[s.name]=v
                nodes.append({'type':n.bl_idname,'inputs':inputs,'image':n.image.name if hasattr(n,'image') and n.image else None})
        materials.append({'name':m.name_full,'library':lib(m),'diffuse':list(m.diffuse_color),'nodes':nodes})
    scenes=[]
    for s in bpy.data.scenes:
        scenes.append({'name':s.name,'frame_start':s.frame_start,'frame_end':s.frame_end,'saved_frame':s.frame_current,'fps':s.render.fps/s.render.fps_base,'engine':s.render.engine,'resolution':[s.render.resolution_x,s.render.resolution_y,s.render.resolution_percentage],'camera':s.camera.name_full if s.camera else None,'world':s.world.name_full if s.world else None,'markers':[[m.name,m.frame,m.camera.name_full if m.camera else None] for m in s.timeline_markers],'custom':{k:str(v)[:1500] for k,v in s.items() if k!='_RNA_UI'}})
    libraries=[{'raw':l.filepath,'resolved':bpy.path.abspath(l.filepath),'parent':l.parent.filepath if l.parent else None,'exists':pathlib.Path(bpy.path.abspath(l.filepath)).exists(),'sha256':sha(bpy.path.abspath(l.filepath)) if pathlib.Path(bpy.path.abspath(l.filepath)).exists() else None} for l in bpy.data.libraries]
    images=[{'name':i.name,'path':i.filepath,'resolved':bpy.path.abspath(i.filepath),'packed':bool(i.packed_file),'source':i.source,'exists':pathlib.Path(bpy.path.abspath(i.filepath)).exists() if i.filepath else None} for i in bpy.data.images if i.source!='VIEWER']
    cameras=[{'name':o.name_full,'lens':o.data.lens,'clip':[o.data.clip_start,o.data.clip_end],'animation':animation(o),'data_animation':animation(o.data)} for o in bpy.data.objects if o.type=='CAMERA']
    result={**item,'native_sha256':before,'source_unchanged':sha(p)==before,'seconds':time.perf_counter()-start,'scenes':scenes,'libraries':libraries,'images':images,'fonts':[{'name':f.name,'path':f.filepath,'packed':bool(f.packed_file)} for f in bpy.data.fonts],'collections':[{'name':c.name_full,'library':lib(c),'objects':len(c.objects)} for c in bpy.data.collections],'objects':objects,'meshes':meshes,'materials':materials,'cameras':cameras,'handlers':[repr(h) for h in bpy.app.handlers.frame_change_post]}
    (TASK/'Evidence'/f"{item['id']}_native.json").write_text(json.dumps(result,indent=2),encoding='utf-8')
    print('INSPECTED',item['id'],len(objects),'objects',len(libraries),'libraries',flush=True)
    return {'id':item['id'],'native':item['native'],'sha256':before,'unchanged':result['source_unchanged'],'objects':len(objects),'libraries':len(libraries),'missing_libraries':[l for l in libraries if not l['exists']]}

results=[]
selected_ids=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
for item in CONFIG:
    if selected_ids and item['id'] not in selected_ids: continue
    try: results.append(inspect(item))
    except Exception:
        results.append({'id':item['id'],'error':traceback.format_exc()}); print(traceback.format_exc(),flush=True)
(TASK/'Evidence/native-summary.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
