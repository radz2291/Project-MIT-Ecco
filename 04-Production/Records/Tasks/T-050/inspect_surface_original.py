"""Read-only identification of original surface and underwater context parts."""
import bpy, json
from pathlib import Path

task = Path(__file__).resolve().parent
data = {
    'source': bpy.data.filepath,
    'collections': [
        {'name': c.name, 'objects': len(c.all_objects),
         'direct_names': [o.name for o in list(c.objects)[:24]]}
        for c in bpy.data.collections
    ],
    'named_parts': [
        {'name': o.name, 'type': o.type,
         'collections': [c.name for c in o.users_collection],
         'dimensions': list(o.dimensions), 'location': list(o.location)}
        for o in bpy.data.objects
        if any(w in o.name.lower() for w in
               ['riser','wellhead','bop','seabed','pipe','base','guide','casing','template'])
    ],
}
(task/'Evidence'/'surface-original-parts.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
print(json.dumps(data))
