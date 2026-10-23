import bpy,math,json,time,hashlib
from pathlib import Path
from mathutils import Vector
B=Path(__file__).resolve().parents[1];s=bpy.context.scene;OUT=B/'Scenes/S05_rock-scale_v013.blend'
assert not OUT.exists() and Path(bpy.data.filepath).parent.parent.name=='Interaction-Proof_v012'
prior=Path(bpy.data.filepath);prior_hash=hashlib.sha256(prior.read_bytes()).hexdigest();bpy.ops.wm.save_as_mainfile(filepath=str(OUT));s.name='S05_RockScale_StillReview_v013'
oldgroup=bpy.data.collections['S05_TRACKED_COHORT_v010'];fx=bpy.data.collections.new('S05_TRACKED_COHORT_v013');s.collection.children.link(fx);rows=[]
for old in list(oldgroup.objects):
 rock=old.copy();rock.data=old.data.copy();rock.animation_data_clear();rock.name=old.name.replace('v010','v013');fx.objects.link(rock)
 for v in rock.data.vertices:v.co*=1.5
 states=[];maxr=0
 for f in range(1,97):
  s.frame_set(f);bpy.context.view_layer.update();rock.location=old.location;rock.rotation_euler=old.rotation_euler;rock.scale=(1,1,1);bpy.context.view_layer.update()
  maxr=max(maxr,max(math.hypot((rock.matrix_world@v.co).x,(rock.matrix_world@v.co).y) for v in rock.data.vertices));states.append((old.location.copy(),old.rotation_euler.copy()))
 # Keep a 2.075 mm wall margin using the measured enlarged radial envelope.
 inward=max(0,maxr-.1535)
 for f,(loc,rot) in enumerate(states,1):
  u=Vector((loc.x,loc.y,0)).normalized();rock.location=loc-inward*u;rock.rotation_euler=rot
  for prop in ['location','rotation_euler']:rock.keyframe_insert(prop,frame=f)
 if rock.animation_data and rock.animation_data.action:
  for layer in rock.animation_data.action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for fc in bag.fcurves:
      for k in fc.keyframe_points:k.interpolation='LINEAR'
 rows.append({'name':rock.name,'linear_size_multiplier':1.5,'support_diameter_mm':2*max(v.co.length for v in rock.data.vertices)*1000,'inward_adjustment_m':inward})
oldgroup.hide_render=True;oldgroup.hide_viewport=True
s.frame_set(48);s.render.filepath=str(B/'Previews/rock-scale_still.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t;assert dt<5
s['proof_scope']='v013 50 percent larger rock fragments with v012 longer trails; still review only, animation render held.'
result={'prior_v012_sha256':prior_hash,'rocks':rows,'trail_version':'v012 unchanged','camera_fluid_hardware_borehole_unchanged':True,'still_frame':48,'render_seconds':dt,'animation_rendered':False}
(B/'Records/still-build.json').write_text(json.dumps(result,indent=2));s.render.filepath='//../Previews/rock-scale_still.png';bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
