import bpy,math,json,sys
from pathlib import Path
from mathutils import Vector,Quaternion
from bpy_extras.object_utils import world_to_camera_view
out,record=map(Path,sys.argv[sys.argv.index("--")+1:])
s=bpy.context.scene
cam=s.camera
join=324

def smooth(t):
    t=min(1,max(0,t))
    return t**3*(10+t*(-15+6*t))

def state():
    return [x for r in cam.matrix_world for x in r]+[cam.data.lens,cam.data.shift_x,cam.data.shift_y]

def hardware():
    p={}
    for i in bpy.context.evaluated_depsgraph_get().object_instances:
        if i.object.name in ("PDC_WEB_AND_SHANK","UPHOLE_COLLAR","ECCO_SENSOR_REF_01"):
            o=i.object
            local=sum((Vector(c) for c in o.bound_box),Vector())/8 if o.type=="MESH" else Vector()
            p[o.name]=i.matrix_world@local
    return p

protected={}
for f in range(join,433):
    s.frame_set(f)
    protected[f]=state()
angles={}
for f in range(1,join):
    s.frame_set(f)
    p=hardware()
    sensor=p["ECCO_SENSOR_REF_01"]
    axis=(p["PDC_WEB_AND_SHANK"]-p["UPHOLE_COLLAR"]).normalized()
    a,b=[world_to_camera_view(s,cam,sensor+sign*.1*axis) for sign in (-1,1)]
    current=math.atan2((b.y-a.y)*720,(b.x-a.x)*1280)
    # Local Z roll preserves the existing path and lens target.
    strength=1-smooth((f-261)/(join-261))
    roll=(current-math.radians(-53))*strength
    cam.rotation_quaternion=cam.rotation_quaternion @ Quaternion((0,0,1),roll)
    cam.keyframe_insert("rotation_quaternion",frame=f)
    opening=1-smooth((f-8)/45)
    if opening>0:
        cam.data.lens*=1-.05*opening
        bpy.context.view_layer.update()
        uv=world_to_camera_view(s,cam,sensor)
        cam.data.shift_x+=(uv.x-.31)*opening
        cam.data.shift_y+=(uv.y-.26)*opening*720/1280
        for prop in ("lens","shift_x","shift_y"):
            cam.data.keyframe_insert(prop,frame=f)
    if f==53:
        cam.data.shift_y=0
        cam.data.keyframe_insert("shift_y",frame=f)
    if f in (1,31,63,82,194,261,285,310,323):
        bpy.context.view_layer.update()
        a,b=[world_to_camera_view(s,cam,sensor+sign*.1*axis) for sign in (-1,1)]
        angles[f]=math.degrees(math.atan2((b.y-a.y)*720,(b.x-a.x)*1280))
        if f<=261: assert abs(angles[f]+53)<1.0,(f,angles[f])
s.frame_set(1)
s.render.filepath="//../Cache/v043/S04_"
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(out.resolve()),compress=True)
bpy.ops.wm.open_mainfile(filepath=str(out.resolve()),use_scripts=False)
s=bpy.context.scene
cam=s.camera
for f,expected in protected.items():
    s.frame_set(f)
    error=max(abs(a-b) for a,b in zip(state(),expected))
    assert error<1e-6,(f,error,state(),expected)
assert all(l.filepath.startswith("//") and Path(bpy.path.abspath(l.filepath)).is_file() for l in bpy.data.libraries)
record.write_text(json.dumps({"target_screen_diagonal_degrees":-53,"measured_screen_angles":angles,
 "original_camera_matches_within_1e-6_frames":[join,432],"transition_frames":[262,323],
 "scope":"Camera rotation and opening lens/shift only"},indent=2)+"\n")
print("V043_READY",angles,flush=True)
