"""Replace bead-like marks with surface-conforming recorded-sample tiles."""
import bpy, math, json, hashlib, time
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
P=Path(__file__).resolve().parents[3];M=P/'Mechanisms/B202';E=P/'Records/Tasks/T-008/Evidence/Still_01'
SOURCE=M/'Scenes/B202_sampling-history_still01_v001.blend'
OUT=M/'Scenes/B202_sampling-history_still01_v002.blend'
IMAGE=M/'Previews/Still_01/B202_sampling-history_still01_v002.png'
assert not OUT.exists(),'Version rather than overwrite'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
record=json.loads((E/'build-render_v001.json').read_text())
assert sha(SOURCE)==record['scene_sha256']
bpy.ops.wm.open_mainfile(filepath=str(SOURCE));s=bpy.context.scene
bpy.context.window.view_layer=s.view_layers['FAST model and mechanism']
wall=bpy.data.objects['T6_WALL_CONTACT_SECTION']
tree=BVHTree.FromPolygons([wall.matrix_world@v.co for v in wall.data.vertices],[list(p.vertices) for p in wall.data.polygons])
ctl=bpy.data.objects['B202_SAMPLE_DISPLAY_CONTROL'];r=ctl['display_radius_m']
mat=bpy.data.materials['B202 recorded-location white - NOT radius colormap']
shader=mat.node_tree.nodes.get('Principled BSDF')
shader.inputs['Emission Strength'].default_value=.35
for sample in record['samples']:
    o=bpy.data.objects[sample['object']];center=Vector(sample['hit'])
    a=math.atan2(center.z,center.y);radial=Vector((0,math.cos(a),math.sin(a)))
    origin=center-radial*.00010;o.location=origin
    verts=[];corners=[]
    # Each corner is independently intersected with the retained source wall.
    for dx,da in ((-r,-r),(r,-r),(r,r),(-r,r)):
        angle=a+da/math.hypot(center.y,center.z)
        direction=Vector((0,math.cos(angle),math.sin(angle)))
        hit=tree.ray_cast(Vector((center.x+dx,0,0)),direction)[0]
        assert hit is not None
        v=hit-direction*.00010;corners.append(list(hit));verts.append((v-origin)/r)
    mesh=bpy.data.meshes.new(o.name+'_surface_tile');mesh.from_pydata(verts,[],[(0,1,2,3)]);mesh.materials.append(mat);mesh.update()
    o.data=mesh;sample['center']=list(origin);sample['corner_hits']=corners
    sample['display_offset_m']=.00010
ctl['display_form']='Flat four-corner ray-projected tiles on actual wall; 0.10mm inward presentation offset'
s['B202_scope']='Still01 v002 proposal: inherited accepted contact state with surface-conforming illustrative sample history; no new motion or approval.'
s.render.filepath=str(IMAGE)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT),relative_remap=False)
bpy.ops.wm.open_mainfile(filepath=str(OUT));s=bpy.context.scene
bpy.context.window.view_layer=s.view_layers['FAST model and mechanism']
t=time.perf_counter();bpy.ops.render.render(write_still=True)
record.update({'scene':str(OUT.relative_to(P)),'scene_sha256':sha(OUT),'image':str(IMAGE.relative_to(P)),'image_sha256':sha(IMAGE),'parent_scene':str(SOURCE.relative_to(P)),'parent_sha256':sha(SOURCE),'render_seconds':time.perf_counter()-t,'revision_reason':'Round beads could read as floating particles; replace with surface-conforming flat recorded-location tiles. Preserve camera, tool, wall, pulse and contact.'})
(E/'build-render_v002.json').write_text(json.dumps(record,indent=2))
print('B202_STILL01_V002_PASS',record['render_seconds'],flush=True)
