import bpy,json,pathlib
root=pathlib.Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco')
scene=bpy.context.scene
out={'scene':scene.name,'camera':scene.camera.name,'frames':[scene.frame_start,scene.frame_end],'objects':[]}
for o in bpy.data.objects:
    if any(t in o.name.lower() for t in ['pulse','echo','contact','sensor','camera']):
        out['objects'].append({'name':o.name,'type':o.type,'location':list(o.location),'props':{k:str(v) for k,v in o.items()},'action':o.animation_data.action.name if o.animation_data and o.animation_data.action else None})
(root/'04-Production/Records/Tasks/T-056/source-inspection.json').write_text(json.dumps(out,indent=2))
