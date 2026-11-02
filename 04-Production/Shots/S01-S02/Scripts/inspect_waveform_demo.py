"""Read-only native comparison. Run in a separate background Blender process."""
import bpy,json,hashlib
from pathlib import Path
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco')
Q=R/'04-Production/Shots/S01-S02'
paths=[R/'04-Production/Shared/Demos/Waveform_demo_v015.blend',
       R/'04-Production/Shared/Assets/Effects/Waveform/Waveform_shared_v015.blend',
       R/'04-Production/Shared/Archive/2026-10-31/Assets/Acoustics/RibbonWaveform_v013/S02_rolling-wave-field_v013.blend']
records=[]
def value(v):
    if isinstance(v,(str,int,float,bool)) or v is None:return v
    try:return list(v)
    except:return str(v)
for path in paths:
    before=hashlib.sha256(path.read_bytes()).hexdigest()
    bpy.ops.wm.open_mainfile(filepath=str(path))
    s=bpy.context.scene
    objects=[]
    for ob in bpy.data.objects:
        mods=[]
        for m in ob.modifiers:
            if m.type!='NODES' or not m.node_group or not m.node_group.name.startswith('WF_'):continue
            vals={}
            for x in m.node_group.interface.items_tree:
                if getattr(x,'in_out','')=='INPUT' and x.socket_type!='NodeSocketGeometry':
                    try:vals[x.name]=value(getattr(m.properties.inputs,x.identifier).value)
                    except:pass
            mods.append({'group':m.node_group.name,'values':vals})
        if mods or 'FIELD' in ob.name:objects.append({'name':ob.name,'in_scene':ob.name in s.objects,'properties':{k:value(v) for k,v in ob.items()},'modifiers':mods})
    records.append({'path':str(path),'scene':s.name,'frames':[s.frame_start,s.frame_end],'fps':s.render.fps,'camera':s.camera.name if s.camera else None,'objects':objects,'texts':{t.name:t.as_string() for t in bpy.data.texts},'libraries':[{'path':l.filepath,'exists':Path(bpy.path.abspath(l.filepath)).exists()} for l in bpy.data.libraries],'sha256':before,'unchanged':hashlib.sha256(path.read_bytes()).hexdigest()==before})
(Q/'Notes/waveform_demo_inspection.json').write_text(json.dumps(records,indent=2))
print('WAVEFORM_REVIEW_DONE',[(r['scene'],len(r['objects']),r['unchanged']) for r in records])
