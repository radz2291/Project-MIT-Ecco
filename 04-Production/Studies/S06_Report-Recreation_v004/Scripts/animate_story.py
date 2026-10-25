"""Animate the approved v004 still direction without modifying the still native."""
import bpy,math,json,time
import numpy as np
from pathlib import Path
from mathutils import Vector,Quaternion
from mathutils.kdtree import KDTree
from bpy_extras.object_utils import world_to_camera_view
B=Path(__file__).resolve().parents[1];bpy.ops.wm.open_mainfile(filepath=str(B/'Scenes/S06_ABC_study_v004.blend'))
D=np.load(B/'Data/story_field.npz');R=float(D['R']);H=float(D['H']);raw=D['radius'];nz,na=raw.shape;nc=na+1
rr=np.c_[raw,raw[:,0]];TH,ZZ=np.meshgrid(np.linspace(0,math.tau,nc),D['z'])
AA=bpy.data.scenes['A | Borehole to reconstruction'];BB=bpy.data.scenes['B | Same surface unfolds'];CC=bpy.data.scenes['C | Laptop engineering payoff']
U=bpy.data.scenes.new('S06 v004 | continuous cinematic study');bpy.context.window.scene=U
U.render.engine='BLENDER_EEVEE';U.eevee.taa_render_samples=16;U.render.resolution_x=1280;U.render.resolution_y=720;U.render.resolution_percentage=100;U.render.fps=24;U.frame_start=1;U.frame_end=288;U.render.image_settings.file_format='PNG';U.view_settings.view_transform='AgX';U.world=AA.world.copy()
def add(o):
    if o.name not in U.objects:U.collection.objects.link(o)
for o in AA.objects:
    if o.type!='CAMERA' and o.name!='Illustrative status':add(o)
amps=[o for o in BB.objects if o.name.startswith(('B | independent amplitude','B | amplitude samples','Amplitude edge'))]
for o in amps:add(o)
for o in CC.objects:
    if o.type!='CAMERA' and o.name not in ('C | same geometry map','C | independent amplitude'):add(o)
cam=AA.camera.copy();cam.data=AA.camera.data.copy();cam.animation_data_clear();cam.data.animation_data_clear();cam.name='Continuous S06 camera';add(cam);U.camera=cam;cam.rotation_mode='QUATERNION'
def ease(a):a=max(0,min(1,a));return a*a*a*(a*(a*6-15)+10)
def span(f,a,b):return ease((f-a)/(b-a))
def coords(p):
    dist=R*TH;curl=math.tau*R*(1-p);t=(dist-curl)/R;dev=(rr-R)*(1-p)
    return np.stack([np.where(dist<curl,(R+dev)*np.sin(t),dist-curl),np.where(dist<curl,-(R+dev)*np.cos(t),-R-dev),ZZ],-1).reshape(-1,3).astype('f')
surf=U.objects['A | reconstructed wall beginning to open'];dots=U.objects['A | indexed reconstruction samples'];guides=[o for o in U.objects if o.type=='CURVE' and o.name.startswith('A ')]
base=coords(.065);kd=KDTree(len(base))
for i,pt in enumerate(base):kd.insert(pt,i)
kd.balance()
guide_ids={o.name:np.array([kd.find(p.co[:3])[1] for p in o.data.splines[0].points]) for o in guides}
ids=np.array([j*nc+k for j in range(0,nz,2) for k in range(0,nc,2)])
offset=np.array([v.co[:] for v in dots.data.vertices]).reshape(-1,6,3)-base[ids,None,:]
states=[coords(i/48) for i in range(49)]
animated=[surf,dots]+guides
for o in animated:
    if o.data.shape_keys:o.shape_key_clear()
    initial=states[0] if o==surf else (states[0][ids,None,:]+offset).reshape(-1,3) if o==dots else states[0][guide_ids[o.name]]
    k=o.shape_key_add(name='Closed reconstruction');k.data.foreach_set('co',initial.astype('f').ravel())
    for i,state in enumerate(states[1:],1):
        values=state if o==surf else (state[ids,None,:]+offset).reshape(-1,3) if o==dots else state[guide_ids[o.name]]
        k=o.shape_key_add(name='Opening %02d'%i);k.data.foreach_set('co',values.astype('f').ravel());k.value=0
# Map the same sample vertices directly into the laptop's geometry panel.
bpy.context.view_layer.update()
def authored_world(o):
    return authored_world(o.parent) @ o.matrix_parent_inverse @ o.matrix_basis if o.parent else o.matrix_basis.copy()
target=bpy.data.objects['C | same geometry map'];ctarget=np.array([authored_world(target)@v.co for v in target.data.vertices],dtype='f')
reportkey=surf.shape_key_add(name='Settle into laptop geometry track');reportkey.relative_key=surf.data.shape_keys.key_blocks['Opening 48'];reportkey.data.foreach_set('co',ctarget.ravel());reportkey.value=0
amp=U.objects['B | independent amplitude'];amptarget=bpy.data.objects['C | independent amplitude'];actarget=np.array([authored_world(amptarget)@v.co for v in amptarget.data.vertices],dtype='f');amp.shape_key_add(name='Independent amplitude');ak=amp.shape_key_add(name='Laptop amplitude track');ak.data.foreach_set('co',actarget.ravel());ak.value=0
amp_parent=bpy.data.objects.new('Amplitude following opening edge',None);add(amp_parent)
for o in amps:o.parent=amp_parent

# Recoverable material visibility controls, preserving original steel and rock shading.
def visibility(m):
    n=m.node_tree.nodes;l=m.node_tree.links;out=next(x for x in n if x.type=='OUTPUT_MATERIAL');source=out.inputs[0].links[0].from_socket;l.remove(out.inputs[0].links[0]);tr=n.new('ShaderNodeBsdfTransparent');mix=n.new('ShaderNodeMixShader');mix.name='SHOT_VISIBILITY';mix.inputs[0].default_value=1;l.new(tr.outputs[0],mix.inputs[1]);l.new(source,mix.inputs[2]);l.new(mix.outputs[0],out.inputs[0]);m.surface_render_method='BLENDED';return mix.inputs[0]
hardware=[o for o in U.objects if o.type=='MESH' and not o.hide_render and (o.name.startswith(('ECCO_','TEMP |')))]
rock=[o for o in U.objects if o.name.startswith(('Fixed borehole','Rock sectional'))]
def mats(obs):return {m for o in obs if o.type in ('MESH','CURVE','FONT') for m in o.data.materials if m}
hm=[visibility(m) for m in mats(hardware)];rm=[visibility(m) for m in mats(rock)]
gm=[visibility(m) for m in mats(guides)]
dotm=dots.data.materials[0];dn=dotm.node_tree.nodes;dl=dotm.node_tree.links;out=next(n for n in dn if n.type=='OUTPUT_MATERIAL');src=out.inputs[0].links[0].from_socket;dl.remove(out.inputs[0].links[0]);attr=dn.new('ShaderNodeAttribute');attr.attribute_name='reveal_depth';val=dn.new('ShaderNodeValue');val.name='RECONSTRUCTION_PROGRESS';sub=dn.new('ShaderNodeMath');sub.operation='SUBTRACT';dl.new(val.outputs[0],sub.inputs[0]);dl.new(attr.outputs['Fac'],sub.inputs[1]);scale=dn.new('ShaderNodeMath');scale.operation='MULTIPLY';scale.inputs[1].default_value=15;scale.use_clamp=True;dl.new(sub.outputs[0],scale.inputs[0]);tr=dn.new('ShaderNodeBsdfTransparent');mix=dn.new('ShaderNodeMixShader');dl.new(scale.outputs[0],mix.inputs[0]);dl.new(tr.outputs[0],mix.inputs[1]);dl.new(src,mix.inputs[2]);dl.new(mix.outputs[0],out.inputs[0]);dotm.surface_render_method='BLENDED'
at=dots.data.attributes.new('reveal_depth','FLOAT','POINT');at.data.foreach_set('value',np.repeat((ids//nc)/(nz-1),6).astype('f'))
dotfade=visibility(dotm)
sm=surf.data.materials[0];sn=sm.node_tree.nodes;surface_alpha=sn.get('Mix Shader').inputs[0];surface_power=sn.get('Emission').inputs[1]
ampm=amp.data.materials[0];am=visibility(ampm);ampa=ampm.node_tree.nodes.get('Mix Shader').inputs[0];ampe=ampm.node_tree.nodes.get('Emission').inputs[1]
ampdec=[o for o in amps if o!=amp];adm=[visibility(m) for m in mats(ampdec)]
co=[o for o in CC.objects if o.name in U.objects and o.type in ('MESH','CURVE','FONT')]
cm=[visibility(m) for m in mats(co)]
for m in mats(co):m.surface_render_method='DITHERED'
# Increase the display's own light so the laptop retains the approved bright report in AgX.
for m in mats(co):
    if m.use_nodes:
        for n in m.node_tree.nodes:
            if n.type=='EMISSION':n.inputs[1].default_value=1.65
alights=[o for o in AA.objects if o.type=='LIGHT'];clights=[o for o in CC.objects if o.type=='LIGHT'];energies={o.name:o.data.energy for o in alights+clights}

def key_socket(socket,value,f):socket.default_value=float(value);socket.keyframe_insert('default_value',frame=f)
def pose(loc,target,lens,roll):return (Vector(loc),(Vector(target)-Vector(loc)).to_track_quat('-Z','Y')@Quaternion((0,0,1),math.radians(roll)),lens)
# Purposeful retreat, unfolding arrival, map-to-screen match, then laptop pullback.
poses=[(1,pose((.40,-2.06,1.03),(0,0,-.10),48,57)),(78,pose((.45,-2.25,1.10),(0,0,-.04),48,57)),(145,pose((-1.20,-4.90,-2.35),(.31,0,0),48,53)),(204,pose((.87,-6.80,.32),(.87,-.19,0),48,0)),(230,pose((.52,-2.20,1.72),(.56,.26,1.02),46,0)),(276,pose((.80,-4.05,2.42),(0,.12,1.09),46,-2)),(288,pose((.79,-4.02,2.41),(0,.12,1.09),46,-2))]
previous={};score=[]
for f in range(1,289):
    p=.065*span(f,72,96)+.935*span(f,96,204);u=span(f,208,236);q=p*48;idx=min(47,int(q));a=q-idx
    vals=np.zeros(49);vals[idx]=1-a;vals[idx+1]=a
    for o in animated:
        for i,k in enumerate(list(o.data.shape_keys.key_blocks)[1:49],1):
            value=float(vals[i]);token=(o.name,i)
            if f==1 or previous.get(token)!=value:
                if f>1:k.keyframe_insert('value',frame=f-1)
                k.value=value;k.keyframe_insert('value',frame=f);previous[token]=value
    reportkey.value=u;reportkey.keyframe_insert('value',frame=f);ak.value=u;ak.keyframe_insert('value',frame=f)
    amp_parent.location.x=math.tau*R*(p-.35)*(1-u);amp_parent.keyframe_insert('location',frame=f)
    for sock in hm:key_socket(sock,1-span(f,98,132),f)
    for sock in rm:key_socket(sock,1-span(f,90,124),f)
    for sock in gm:key_socket(sock,span(f,30,80)*(1-span(f,208,232)),f)
    key_socket(val.outputs[0],1.10*span(f,8,76),f);key_socket(dotfade,1-span(f,204,230),f)
    key_socket(surface_alpha,(.075*span(f,46,88)+.145*span(f,96,156))*(1-u)+u,f)
    key_socket(surface_power,.65*(1-u)+1.65*u,f)
    key_socket(am,span(f,179,207),f);key_socket(ampa,.66*(1-u)+u,f);key_socket(ampe,.85*(1-u)+1.65*u,f)
    for sock in adm:key_socket(sock,span(f,179,207)*(1-span(f,208,230)),f)
    for sock in cm:key_socket(sock,span(f,220,250),f)
    for o in alights:o.data.energy=energies[o.name]*(1-span(f,112,144));o.data.keyframe_insert('energy',frame=f)
    for o in clights:o.data.energy=energies[o.name]*span(f,220,250);o.data.keyframe_insert('energy',frame=f)
    for (fa,pa),(fb,pb) in zip(poses[:-1],poses[1:]):
        if fa<=f<=fb:
            t=span(f,fa,fb);cam.location=pa[0].lerp(pb[0],t);cam.rotation_quaternion=pa[1].slerp(pb[1],t);cam.data.lens=pa[2]*(1-t)+pb[2]*t;break
    # A gentle mid-unfold retreat keeps the opening surface inside the frame.
    retreat=.24*span(f,120,148)*(1-span(f,175,204))
    cam.location=Vector((.31,0,0))+(cam.location-Vector((.31,0,0)))*(1+retreat)
    if 96<=f<=204:
        current=coords(p);lo=current.min(0);hi=current.max(0)
        hi[0]+= .565*span(f,175,190)
        center=Vector(((lo+hi)*.5).tolist());roll=57-4*span(f,96,145)-53*span(f,145,204)
        aim=(center-cam.location).to_track_quat('-Z','Y')@Quaternion((0,0,1),math.radians(roll))
        cam.rotation_quaternion=cam.rotation_quaternion.slerp(aim,span(f,96,125))
        # Fit both boundary columns and both end contours, not only one edge.
        check=np.concatenate((current[::nc],current[nc-1::nc],current[:nc],current[-nc:]))
        if f>=179:
            check=np.concatenate((check,np.array([[hi[0],-R,-H/2],[hi[0],-R,H/2]])))
        for _ in range(3):
            bpy.context.view_layer.update()
            uv=np.array([world_to_camera_view(U,cam,Vector(v))[:2] for v in check])
            fit=float(np.max(abs(uv-.5))/.45)
            if fit<=1:break
            cam.location=center+(cam.location-center)*(1+(fit-1)*span(f,96,120))
    cam.data.shift_x=0;cam.data.shift_y=0
    cam.keyframe_insert('location',frame=f);cam.keyframe_insert('rotation_quaternion',frame=f);cam.data.keyframe_insert('lens',frame=f)
    score.append({'frame':f,'opening':p,'report_match':u,'camera':list(cam.location),'quaternion':list(cam.rotation_quaternion)})
# Hidden objects stop consuming render work after their fades finish.
for objects,on,off in [(hardware+rock,1,145),(guides+[dots],1,238),(co,216,None),(ampdec,176,238),([amp],176,None)]:
    for o in objects:
        o.hide_render=on>1;o.keyframe_insert('hide_render',frame=1)
        o.hide_render=False;o.keyframe_insert('hide_render',frame=on)
        if off:o.hide_render=True;o.keyframe_insert('hide_render',frame=off)
for action in bpy.data.actions:
    for layer in action.layers:
        for strip in layer.strips:
            for bag in strip.channelbags:
                for fc in bag.fcurves:
                    for k in fc.keyframe_points:k.interpolation='CONSTANT' if fc.data_path=='hide_render' else 'LINEAR'
# Remove unused source scenes from the animation deliverable; original still native stays intact.
for ss in list(bpy.data.scenes):
    if ss!=U:bpy.data.scenes.remove(ss)
U['scope']='Owner-authorized 12 second v004 animation from approved still direction';U['provenance']='Report-inspired illustrative geometry; not field measurements; after-run processing';U['dataset']='//../Data/story_field.npz'
U.frame_set(1);bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(B/'Scenes/S06_cinematic-study_v004.blend'))
(B/'Records/animation-score.json').write_text(json.dumps(score),encoding='utf-8');print('ANIMATION BUILT')
