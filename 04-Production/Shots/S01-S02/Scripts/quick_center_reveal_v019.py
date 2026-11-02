"""Land on the patch's middle grid point; reveal middle cells to boundary."""
import bpy,json,sys,re,time,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
Q=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/Shots/S01-S02');sys.path.insert(0,str(Q.parents[1]/'Shared/Assets/Effects/Waveform/Scripts'))
from pulse_asset_api import get_input,set_input
out=Q/'Scenes/Waveform_center_reveal_fast_v019.blend';assert not out.exists();assert 'reveal_fast_v018' in bpy.data.filepath
if bpy.data.is_dirty:bpy.ops.wm.save_as_mainfile(filepath=str(Q/f'Scenes/Before_center_reveal_{int(time.time())}.blend'),copy=True,compress=True)
s=bpy.context.scene;s.frame_set(340);o=bpy.data.objects['WF sequence event 1'];m=o.modifiers[0];w=bpy.data.objects['ONE WALL - old history and current cells share topology'];faces=[p for p in w.data.polygons if w.data.materials[p.material_index].name.startswith('Unified cell 1 ')];indices=sorted({i for p in faces for i in p.vertices});pts=[w.matrix_world@w.data.vertices[i].co for i in indices]
middle=sum(pts,Vector())/len(pts);center=min(pts,key=lambda p:(p-middle).length);A=o.matrix_world@Vector(get_input(m,'Origin'));oldB=A+Vector(get_input(m,'Route axis'))*get_input(m,'Gap length m')
# Build in coordinates near zero to avoid large scene-depth precision loss.
raw=BVHTree.FromPolygons([w.matrix_world@v.co-A for v in w.data.vertices],[tuple(p.vertices) for p in faces]);ray=(center-A).normalized();hit=raw.ray_cast(Vector(),ray,.15);assert hit[0] is not None;B=A+hit[0];gap=(B-A).length;axis=(B-A).normalized();side=axis.cross(Vector((0,0,1))).normalized();up=side.cross(axis).normalized()
for k,v in {'Gap length m':gap,'Route axis':tuple(axis),'Transverse axis':tuple(side),'Up axis':tuple(up)}.items():set_input(m,k,v)
ordered=sorted(faces,key=lambda p:((w.matrix_world@p.center)-B).length);groups=[]
for rank,p in enumerate(ordered):
 group=rank//4;name='Unified cell 1 edge0 reveal'+str(group);p.material_index=next(i for i,mat in enumerate(w.data.materials) if mat and mat.name==name);w.data.attributes['ecco_reveal_order'].data[p.index].value=group*1.5;groups.append({'face':p.index,'group':group,'distance_mm':(w.matrix_world@p.center-B).length*1000})
endpoint=o.matrix_world@(Vector(get_input(m,'Origin'))+Vector(get_input(m,'Route axis'))*get_input(m,'Gap length m'));nearest=raw.find_nearest(endpoint-A);err=nearest[3]*1000;assert err<.01,err;assert (B-center).length<.0001
centerfaces=[x['face'] for x in groups if x['group']==0];assert len(centerfaces)==4
s.frame_set(325);bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True)
(Q/'Notes/quick_center_reveal_v019.json').write_text(json.dumps({'scene':str(out),'scope':'first exchange alignment/reveal review; approved pulse shape and timing unchanged','old_endpoint':list(oldB),'new_endpoint':list(endpoint),'patch_middle_grid_point':list(center),'patch_center_alignment_mm':(B-center).length*1000,'beam_wall_error_mm':err,'group_order':groups,'center_cells':centerfaces,'edge_spread_offsets':[0,1.5,3,4.5],'topology':'existing patch/grid retained, beam retargeted to central grid intersection; four central tiles then outward to edges/corners','signal':'only route basis and gap changed; waveform style/timing untouched','preview':[300,353],'fps':24},indent=2));result={'saved':str(out),'beam_wall_error_mm':err,'center_alignment_mm':(B-center).length*1000,'center_cells':centerfaces}
