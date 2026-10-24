import bpy,sys,math,json,time
import numpy as np
from pathlib import Path
from mathutils import Vector,Quaternion
B=Path(__file__).resolve().parents[1]
mode=sys.argv[-1] if sys.argv[-1] in ('proof','journey') else 'proof'
bpy.ops.wm.open_mainfile(filepath=str(B/'Scenes/Arrival_1.blend'))
s=bpy.context.scene;cam=s.camera
for ob in s.objects:
    if ob.type=='LIGHT':ob.data.use_shadow=False
D=np.load(B/'Data/surface_samples.npz');raw=D['radius_m'];nz,na=raw.shape;R=.156
r=np.c_[raw,raw[:,0]];TH,DP=np.meshgrid(np.linspace(0,math.tau,na+1),D['depth_from_interval_top_m']);H=float(DP.max());ZZ=H/2-DP;DEV=r-R
def coords(p):
    c=1-p
    if c<1.e-7:xx=R*(TH-math.pi);yy=np.zeros_like(TH)
    else:
        q=c*TH;xx=R*np.sin(q)/c-R*math.pi*p+DEV*c*np.sin(q);yy=R*(1-np.cos(q))/c-DEV*c*np.cos(q)
    return np.stack([xx,yy,ZZ],axis=-1).reshape(-1,3).astype('f')
surf=s.objects['Recorded geometry | illustrative S03 source']
guides=[]
for k in range(0,na+1,24):guides.append([j*(na+1)+k for j in range(nz)])
for j in range(0,nz,12):guides.append([j*(na+1)+k for k in range(na+1)])
curves=[(s.objects['Registration %02d'%i],ids) for i,ids in enumerate(guides)]
curves.extend([(s.objects['Seam '+label],[j*(na+1)+k for j in range(nz)]) for label,k in [('0',0),('360',na)]])
all_shape_objects=[surf]
for ob,idx in curves:
    ob.shape_key_add(name='Closed reconstruction')
    for i in range(1,33):
        key=ob.shape_key_add(name='Unfold %02d'%i);key.data.foreach_set('co',coords(i/32)[idx].ravel())
    all_shape_objects.append(ob)
    if ob.name.startswith('Seam'):ob.data.bevel_depth=.0012
fade_materials=[m for m in bpy.data.materials if m.use_nodes and m.node_tree.nodes.get('REPORT_REVEAL')]
mapmix=surf.data.materials[0].node_tree.nodes['SCULPTURE_TO_MAP'].inputs[0]
def ease(t):t=max(0,min(1,t));return t*t*t*(t*(6*t-15)+10)
def mix(a,b,t):return np.array(a)*(1-t)+np.array(b)*t
def interpolate(f,keys):
    for k in range(len(keys)-1):
        a,b=keys[k],keys[k+1]
        if a[0]<=f<=b[0]:
            t=ease((f-a[0])/(b[0]-a[0]));return mix(a[1],b[1],t),mix(a[2],b[2],t),float(a[3]*(1-t)+b[3]*t),float(a[4]*(1-t)+b[4]*t)
    a=keys[-1];return a[1],a[2],a[3],a[4]
if mode=='proof':
    end=120;start_unfold=13;end_unfold=96
    keys=[(1,(1.15,-4,.65),(0,.12,0),3.9,-.07),(120,(0,-4,.06),(0,0,.06),3.9,0)]
else:
    end=288;start_unfold=73;end_unfold=192
    keys=[(1,(1.9,-3.3,2.3),(0,.13,0),3.95,-.43),(49,(1.7,-3.2,2.1),(0,.13,0),3.7,-.40),(132,(.9,-3.8,.8),(-.03,.20,0),3.85,-.055),(205,(0,-4,.04),(0,0,.04),3.9,0),(264,(.35,-4,.04),(.35,0,.04),4.75,0),(288,(.35,-4,.04),(.35,0,.04),4.75,0)]
s.frame_end=end;s.name='S06 '+mode+' | same data, new coordinates'
score=[]
for f in range(1,end+1):
    p=ease((f-start_unfold)/(end_unfold-start_unfold));q=32*p;low=int(q);t=q-low
    for ob in all_shape_objects:
        for i,key in enumerate(ob.data.shape_keys.key_blocks):
            if i==0:continue
            key.value=1-t if i==low else t if i==low+1 else 0
            key.keyframe_insert('value',frame=f)
    mapmix.default_value=p;mapmix.keyframe_insert('default_value',frame=f)
    loc,target,scale,roll=interpolate(f,keys)
    cam.location=loc;cam.rotation_quaternion=(Vector(target)-Vector(loc)).to_track_quat('-Z','Y')@Quaternion((0,0,1),roll);cam.data.ortho_scale=scale
    cam.keyframe_insert('location',frame=f);cam.keyframe_insert('rotation_quaternion',frame=f);cam.data.keyframe_insert('ortho_scale',frame=f)
    for name,top in [('Proof identity',True),('Source notice',False)]:
        ob=s.objects[name];ob.location=(-scale*.455,scale*(9/16)*(.435 if top else -.455),-2);ob.data.size=scale*.018
        ob.keyframe_insert('location',frame=f);ob.data.keyframe_insert('size',frame=f)
    rv=ease((f-217)/35) if mode=='journey' else 0
    for ma in fade_materials:
        sock=ma.node_tree.nodes['REPORT_REVEAL'].inputs[0];sock.default_value=rv;sock.keyframe_insert('default_value',frame=f)
    score.append({'frame':f,'unfold':p,'camera_position':list(loc),'target':list(target),'ortho_scale':scale,'roll_radians':roll,'report_reveal':rv})
# Baked samples are linear between frames; dense keyed curves avoid auto-Bezier overshoot.
for act in bpy.data.actions:
    for layer in act.layers:
        for strip in layer.strips:
            for bag in strip.channelbags:
                for fc in bag.fcurves:
                    for pt in fc.keyframe_points:pt.interpolation='LINEAR'
s['scope']='Targeted proof only; owner fresh handoff 2026-10-25; not full cinematic production'
s['source_data']='//../Data/surface_samples.npz'
s.frame_set(1);bpy.context.preferences.filepaths.save_version=0
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=str(B/f'Scenes/S06_{mode}_v001.blend'),relative_remap=False)
(B/f'Records/{mode}-camera-score.json').write_text(json.dumps(score,indent=2))
print('ANIMATION READY',mode)
