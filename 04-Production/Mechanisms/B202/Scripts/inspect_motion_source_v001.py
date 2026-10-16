import bpy,json,gzip
from pathlib import Path
R=Path(__file__).resolve().parents[4]
B=R/'04-Production/Mechanisms/B202'
bpy.ops.wm.open_mainfile(filepath=str(B/'Scenes/B202_measured-envelope_master_v009.blend'))
s=bpy.context.scene
out={'camera':s.camera.name,'render_engine':s.render.engine,'objects':[{'name':o.name,'type':o.type,'parent':o.parent.name if o.parent else None,'location':list(o.location),'dimensions':list(o.dimensions)} for o in s.objects if o.type in ('CAMERA','LIGHT') or o.name in ['B202_TOOL_TRAVEL_X','B202_TOOL_ROTATION_X']], 'control':dict(bpy.data.objects['B202_CONTROL'].items()),'libraries':[{'path':l.filepath,'exists':Path(bpy.path.abspath(l.filepath)).exists()} for l in bpy.data.libraries]}
(R/'04-Production/Records/Tasks/T-027/Evidence/source_inspection_v001.json').write_text(json.dumps(out,indent=2))
print('MOTION_SOURCE_INSPECTION_PASS')
