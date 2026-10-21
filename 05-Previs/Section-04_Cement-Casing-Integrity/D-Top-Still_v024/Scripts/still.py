import bpy,json,time,hashlib
from pathlib import Path
from mathutils import Vector,Matrix
B=Path(__file__).resolve().parents[1];SRC=B.parent/'Cinematic-Previs_v022/Scenes/S04_complete_v022.blend'
bpy.ops.wm.open_mainfile(filepath=str(SRC),use_scripts=False,load_ui=False);s=bpy.context.scene;s.name='S04 D overhead still v024';s.frame_set(355);bpy.context.view_layer.update()
sx=bpy.data.objects['WORLD_CONTROL']['travel_m']+.7300000190734863
m=bpy.data.materials['ECCO D explanatory transparent housing'];m.node_tree.animation_data_clear();m.node_tree.nodes['Housing opacity - sensor remains solid'].outputs[0].default_value=1
c=s.camera;c.animation_data_clear();c.data=c.data.copy();c.data.animation_data_clear();c.rotation_mode='QUATERNION';c.data.shift_x=.12;c.data.shift_y=0
def pose(p,t):
 f=(t-p).normalized();u=Vector((-1,0,0));u=(u-f*u.dot(f)).normalized();r=f.cross(u).normalized();return Matrix((r,u,-f)).transposed().to_quaternion()
s.eevee.taa_render_samples=8
rows=[]
for i,(dx,y,z,lens) in enumerate([(.30,.12,.105,20)]):
 c.location=(sx+dx,y,z);t=Vector((sx-.03,.09,0));c.rotation_quaternion=pose(c.location,t);c.data.lens=lens;bpy.context.view_layer.update();s.render.filepath=str(B/'Previews'/f'S04_D_top_{i}_v024.png');a=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-a;assert dt<5;rows.append({'eye':list(c.location),'target':list(t),'lens':lens,'seconds':dt})
r=rows[0];c.location=r['eye'];c.rotation_quaternion=pose(c.location,Vector(r['target']));c.data.lens=r['lens'];s['scope']='Overhead drone-like still only. No animation integration; unchanged physical geometry.'
out=B/'Scenes/S04_D_top_v024.blend'
for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(out.parent))
bpy.ops.wm.save_as_mainfile(filepath=str(out),relative_remap=False)
(B/'Records/proof.json').write_text(json.dumps({'source':str(SRC),'source_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),'cameras':rows,'physical_geometry_edited':False,'integration':False},indent=2))





