import bpy,json,pathlib,os,hashlib
from mathutils import Vector
R=pathlib.Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');T=R/'04-Production/Records/Tasks/T-056';O=T/'Consumers';O.mkdir(exist_ok=True);master=R/'04-Production/Shared/Assets/Acoustics/Waveform_shared_v014/Waveform_shared_v014.blend';sources=json.loads((T/'consumer-source-events_v014.json').read_text());mapping=[]
def val(mod,name,value):
 ident=next(x.identifier for x in mod.node_group.interface.items_tree if getattr(x,'in_out','')=='INPUT' and x.name==name);getattr(mod.properties.inputs,ident).value=value
def sample(ob,f):
 bpy.context.scene.frame_set(int(f),subframe=f-int(f));return ob.matrix_world.translation.copy()
for key,src in sources.items():
 path=R/src['source'];bpy.ops.wm.open_mainfile(filepath=str(path));s=bpy.context.scene
 with bpy.data.libraries.load(str(master),link=True) as (a,b):b.node_groups=['WF_FIELD_LIVE_v014'];b.collections=['WF_SHARED_CONTROLS'];b.meshes=['WF_PARAMETER_DOMAIN']
 s.collection.children.link(b.collections[0]);group=b.node_groups[0];mesh=b.meshes[0]
 hidden=bpy.data.collections.new('WF_REPLACED_TRAVEL_ONLY — original actions retained');s.collection.children.link(hidden);hidden.hide_render=True;hidden.hide_viewport=True
 replaced=[]
 for ob in list(bpy.data.objects):
  if (key=='S02' and ob.name.startswith('DW 1 ') and ('SEND front' in ob.name or 'ECHO front' in ob.name)) or (key=='S04' and ob.name.startswith('S02 sourced ') and ('SEND front' in ob.name or 'ECHO front' in ob.name)):
   replaced.append(ob.name);hidden.objects.link(ob)
   for c in list(ob.users_collection):
    if c!=hidden:c.objects.unlink(ob)
 hidden.hide_viewport=False
 events=[]
 if key=='S02':
  p=json.loads((T/'ribbon-build_v010.json').read_text());events=[(Vector(p['path_start']),Vector(p['path_end']),300.,309.,310.,318.,(0,0,1),0)]
 else:
  for suffix in ['', '.001']:
   snd=next(o for o in src['objects'] if o['name']=='S02 sourced SEND front 0'+suffix);ech=next(o for o in src['objects'] if o['name']=='S02 sourced ECHO front 0'+suffix)
   def window(o):
    c=next(c for c in o['curves'] if c[0]=='hide_render');fs=[p[0] for p in c[2] if p[1]<.5];return min(fs),max(fs)
   start,contact=window(snd);es,receipt=window(ech);a=Vector([min(p[1] for p in next(c for c in snd['curves'] if c[0]=='location' and c[1]==i)[2]) for i in range(3)]);z=Vector([max(p[1] for p in next(c for c in snd['curves'] if c[0]=='location' and c[1]==i)[2]) for i in range(3)]);events.append((a,z,start,contact,es,receipt,(1,0,0),0 if not suffix else 1))
 hidden.hide_viewport=True
 instances=[]
 for i,(a,z,start,contact,es,receipt,up,preset) in enumerate(events):
  assert (z-a).length>.001 and (z-a).length<.1, 'Invalid source route'
  ob=bpy.data.objects.new('WF_'+key+'_EVENT_'+str(i+1),mesh);s.collection.objects.link(ob);ob.location=a;axis=(z-a).normalized();up=Vector(up);depth=axis.cross(up).normalized();mod=ob.modifiers.new('WAVEFORM — local timing and overrides','NODES');mod.node_group=group
  # Local travel windows are owned by the source scene. Playback is deliberately locked.
  params={'Radius Override':3.,'Start Frame':start,'Duration Override':2.56 if key=='S04' else 3.,'Travel Override':contact-start,'Return Travel Override':receipt-es,'Echo Delay Frames':es-contact,'Outbound End Frame':contact+(2.56 if key=='S04' else 0.01),'Return End Frame':receipt+(1.92 if key=='S04' else 0.01),'Lock Event Timing':1.,'Gap Length m':(z-a).length,'Route Axis':tuple(axis),'Transverse Axis':tuple(depth),'Up Axis':tuple(up),'Preset 0 Open 1 Cased':preset}
  for n,v in params.items():val(mod,n,v)
  ob['README']='Linked shared field, local event timing locked to native source. Preset is illustrative display, not calibrated material response.';instances.append({'object':ob.name,'start':list(a),'wall':list(z),'settings':params})
 s.frame_set(305 if key=='S02' else 77);bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);bpy.context.view_layer.objects.active=ob
 target=O/(key+'_waveform_shared_v014.blend');bpy.ops.wm.save_as_mainfile(filepath=str(target),relative_remap=True)
 for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(os.path.normpath(bpy.path.abspath(lib.filepath)))
 bpy.ops.wm.save_as_mainfile(filepath=str(target));mapping.append({'name':key,'baseline':str(path),'candidate':str(target),'frames':[1,299,300,305,309,310,314,318,324,528] if key=='S02' else [1,72,77,81,86,93,184,190,200,205,261,300,432],'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'camera':s.camera.name,'range':[s.frame_start,s.frame_end],'fps':s.render.fps,'instances':instances,'replaced_travel_objects':replaced})
(T/'consumer-mapping_v014.json').write_text(json.dumps(mapping,indent=2));print('SAVED_TWO_CONSUMERS')
