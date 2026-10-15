import bpy,json,math
from pathlib import Path
from mathutils import Vector
root=Path(__file__).resolve().parents[3]
src=root/'Shared/Assets/ECCO/ECCO_master_temporary-plugs_v002.blend'
bpy.ops.wm.open_mainfile(filepath=str(src))
o=bpy.data.objects['ECCO_HOUSING_SOURCE_MESH']
pts=[o.matrix_world@v.co for v in o.data.vertices]
bins=[]
for i in range(120):
    a=i*.02;b=a+.02
    rr=sorted(math.hypot(p.y,p.z) for p in pts if a<=p.x<b)
    bins.append({'x':round(a,3),'max_radius':max(rr) if rr else None})
out=root/'Records/Tasks/T-010/Evidence/geometry-profile_v001.json'
out.write_text(json.dumps({'object':o.name,'vertices':len(pts),'max_axis_radius_m':max(math.hypot(p.y,p.z) for p in pts),'source_x_bounds_m':[min(p.x for p in pts),max(p.x for p in pts)],'profile_note':'Vertex-sample maxima by 20mm bin, not continuous cross-section ray measurements. Empty bins are not absent geometry.','bins':bins,'objects':[x.name for x in bpy.context.scene.objects]},indent=2))
