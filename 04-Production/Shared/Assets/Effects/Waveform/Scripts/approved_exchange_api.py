"""Authoring helpers for the approved look. Native playback needs no Python."""
import bpy,json,math
from pathlib import Path
from mathutils import Vector,Matrix
from pulse_asset_api import set_input
PRESET=Path(__file__).parent.parent/'Approved_beam_exchange_v001.json'
def _frame_scale(preset):
 fps=bpy.context.scene.render.fps/bpy.context.scene.render.fps_base
 return (fps/preset['reference_fps'] if preset['timing']['Follow scene FPS'] else 1.)/preset['timing']['Speed']
def apply_approved_preset(modifier,start_frame=1):
 p=json.loads(PRESET.read_text())
 for k,v in p['timing'].items():set_input(modifier,k,float(start_frame) if k=='Start frame' else v)
 set_input(modifier,'Use master style',True)
 for k,v in p['quick'].items():set_input(modifier,k,v)
 return {k:start_frame+v*_frame_scale(p) for k,v in p['landmarks_relative'].items()}
def create_contact_patch(collection,point,normal,start_frame=1,size_m=None,enabled=True,overrides=None,frame_scale=None):
 preset=json.loads(PRESET.read_text());factor=_frame_scale(preset) if frame_scale is None else frame_scale;p=preset['contact_patch'];p.update(overrides or {});size=p['size_m'] if size_m is None else size_m;n=Vector(normal).normalized();up=Vector((0,0,1));up=Vector((0,1,0)) if abs(n.dot(up))>.95 else up;tangent=up.cross(n).normalized();up=n.cross(tangent).normalized();h=size/2
 mesh=bpy.data.meshes.new('Approved contact patch');mesh.from_pydata([(-h,0,-h),(h,0,-h),(h,0,h),(-h,0,h)],[],[(3,2,1,0)]);ob=bpy.data.objects.new('Active contact patch',mesh);collection.objects.link(ob);ob.matrix_world=Matrix((tangent,-n,up)).transposed().to_4x4();ob.location=Vector(point)-n*p['surface_clearance_m'];ob.hide_render=not enabled;ob.hide_viewport=not enabled
 mat=bpy.data.materials.new('Contact muted teal');mesh.materials.append(mat);base=p['color'][:3];arrival=p['arrival_after'];reveal=p['reveal_after'];half=int(p['breath_period_frames']/2)
 assert half>=1 and reveal>arrival
 keys=[(arrival-1,0.),(arrival,.45)]+[(t,1. if ((t-arrival-1)//half)%2==0 else p['min_scale']) for t in range(arrival+1,reveal+1,half)]
 if keys[-1][0]<reveal:keys.append((reveal,keys[-1][1]))
 keys.append((reveal+p['handover_frames'],0.))
 for t,v in keys:
  ob.scale=(v,v,v);ob.keyframe_insert('scale',frame=start_frame+t*factor);mat.diffuse_color=tuple(c*(.83+.17*v) for c in base)+(1.,);mat.keyframe_insert('diffuse_color',frame=start_frame+t*factor)
 for obj in [ob,mat]:
  for l in obj.animation_data.action.layers:
   for st in l.strips:
    for bag in st.channelbags:
     for fc in bag.fcurves:
      for k in fc.keyframe_points:k.interpolation='BEZIER';k.handle_left_type='AUTO_CLAMPED';k.handle_right_type='AUTO_CLAMPED'
 ob['Authored size m']=size;ob['Enabled']=enabled;ob['Recipe']='Approved_beam_exchange_v001.json'
 for prop in ['hide_render','hide_viewport']:
  fc=ob.driver_add(prop);v=fc.driver.variables.new();v.name='enabled';v.type='SINGLE_PROP';v.targets[0].id=ob;v.targets[0].data_path='["Enabled"]';fc.driver.expression='1-enabled'
 return ob
def configure_surface_patch(wall,faces,point,start_frame=1,frame_scale=None):
 p=json.loads(PRESET.read_text());factor=_frame_scale(p) if frame_scale is None else frame_scale;ordered=sorted(faces,key=lambda f:(wall.matrix_world@f.center-Vector(point)).length);materials=[]
 for group in range(4):
  mat=bpy.data.materials.new('Approved tile glitch '+str(group));wall.data.materials.append(mat);materials.append(len(wall.data.materials)-1)
  for key in p['surface']['color_profiles'][str(group)]:mat.diffuse_color=key['color'];mat.keyframe_insert('diffuse_color',frame=start_frame+key['frame']*factor)
 for rank,f in enumerate(ordered):
  group=min(3,rank*4//len(ordered));f.material_index=materials[group];wall.data.attributes['ecco_receipt_frame'].data[f.index].value=start_frame+p['landmarks_relative']['surface_reveal']*factor-1;wall.data.attributes['ecco_reveal_order'].data[f.index].value=p['surface']['group_offsets'][group]*factor
 for node in wall.modifiers[0].node_group.nodes if wall.modifiers else []:
  if node.type=='GROUP' and 'Settle frames' in node.inputs:node.inputs['Settle frames'].default_value=p['surface']['settle_frames']*factor
 return ordered
