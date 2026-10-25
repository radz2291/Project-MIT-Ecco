"""Extend saved v001 geometry and shape keys. No radius or source-ID edits."""
import bpy, math, json, sys, time, hashlib
import numpy as np
from pathlib import Path
from mathutils import Vector, Quaternion
B=Path(__file__).resolve().parents[1]
OLD=B.with_name('S06_Sculpted-Information_v001')
bpy.ops.wm.open_mainfile(filepath=str(OLD/'Scenes/S06_journey_v001.blend'))
s=bpy.context.scene;cam=s.camera
s.name='S06 v002 | Sculpted Information'
for ob in list(s.objects):
    if ob.type not in ('CAMERA','LIGHT') and not ob.name.startswith(('Recorded geometry','Registration','Seam')):
        bpy.data.objects.remove(ob,do_unlink=True)
surf=s.objects['Recorded geometry | illustrative S03 source']
shape_objects=[o for o in s.objects if o.type in ('MESH','CURVE') and o.data.shape_keys]
for o in shape_objects:o.data.shape_keys.animation_data_clear()
cam.animation_data_clear();cam.data.animation_data_clear()
for m in bpy.data.materials:
    if m.use_nodes:m.node_tree.animation_data_clear()
data=np.load(B/'Data/surface_samples.npz');raw=data['radius_m'];nz,na=raw.shape;R=.156
depth=data['depth_from_interval_top_m'];H=float(depth[-1]);angles=np.linspace(0,math.tau,na+1)
rad=np.c_[raw,raw[:,0]];TH,DP=np.meshgrid(angles,depth);ZZ=H/2-DP
closed=np.array([v.co[:] for v in surf.data.vertices])
base_hash=hashlib.sha256(closed.astype('f').tobytes()).hexdigest()
# Establish outward-facing shading from the actual radial direction.
normal_dot=[]
for p in list(surf.data.polygons)[::300]:
    center=p.center;normal_dot.append(p.normal.dot(Vector((center.x,center.y-R,0))))
flipped=float(np.mean(normal_dot))<0
if flipped:surf.data.flip_normals()
pr=surf.data.materials[0].node_tree.nodes.get('Principled BSDF')
pr.inputs['Emission Strength'].default_value=.015
pr.inputs['Roughness'].default_value=.64
pr.inputs['Specular IOR Level'].default_value=.25
mapmix=surf.data.materials[0].node_tree.nodes['SCULPTURE_TO_MAP'].inputs[0]
for ob in s.objects:
    if ob.name.startswith('Registration'):ob.data.bevel_depth=.00045
    if ob.name.startswith('Seam'):ob.data.bevel_depth=.0007
reg=bpy.data.materials['Data-space register'].node_tree.nodes.get('Emission')
reg.inputs[0].default_value=(.15,.23,.29,1)
s.world.node_tree.nodes['Background'].inputs[0].default_value=(.009,.016,.025,1)
s.world.node_tree.nodes['Background'].inputs[1].default_value=.25
for ob in s.objects:
    if ob.type=='LIGHT':
        ob.data.use_shadow=False
        if 'Key' in ob.name:ob.location=(-1.1,-.55,1.6);ob.data.energy=32;ob.data.size=.8
        elif 'Fill' in ob.name:ob.location=(1.2,-1,-.4);ob.data.energy=6;ob.data.size=1.6
        else:ob.location=(.5,1.1,.8);ob.data.energy=22;ob.data.size=.65
        ob.rotation_euler=(Vector((0,.156,.1))-ob.location).to_track_quat('-Z','Y').to_euler()
cam.data.type='PERSP';cam.data.lens=52;cam.data.sensor_width=36;cam.data.clip_start=.01
s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100
s.eevee.taa_render_samples=16;s.frame_start=1;s.frame_end=288;s.render.fps=24
s.render.image_settings.file_format='PNG'

def link(ob):s.collection.objects.link(ob);return ob
report=[];fade_mats=[]
def mat(name,color,fade=True):
    ma=bpy.data.materials.new('v002 '+name);ma.use_nodes=True
    n=ma.node_tree.nodes;n.clear();l=ma.node_tree.links
    em=n.new('ShaderNodeEmission');em.inputs[0].default_value=(*color,1)
    out=n.new('ShaderNodeOutputMaterial')
    if fade:
        tr=n.new('ShaderNodeBsdfTransparent');mix=n.new('ShaderNodeMixShader');mix.name='REPORT_REVEAL';mix.inputs[0].default_value=0
        l.new(tr.outputs[0],mix.inputs[1]);l.new(em.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],out.inputs[0]);ma.surface_render_method='BLENDED';fade_mats.append(ma)
    else:l.new(em.outputs[0],out.inputs[0])
    return ma
paper=mat('Report paper',(.78,.82,.84));panel=mat('Track ground',(.88,.90,.91));ink=mat('Report ink',(.025,.055,.08));dim=mat('Secondary ink',(.15,.23,.29));grid=mat('Hairline grid',(.48,.56,.61))
blue=mat('Geometry blue',(.025,.21,.52));red=mat('Geometry tight',(.61,.065,.075));warm=mat('Amplitude accent',(.5,.23,.045))
def line(name,pts,ma=grid,width=.001):
    cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=width;cu.bevel_resolution=0
    sp=cu.splines.new('POLY');sp.points.add(len(pts)-1)
    for v,p in zip(sp.points,pts):v.co=(*p,1)
    ob=link(bpy.data.objects.new(name,cu));cu.materials.append(ma);report.append(ob);return ob
# Intermediate measured section contours expose the actual radius changes.
# Positions are sampled directly from the retained v001 shape keys.
contour_ma=mat('Measured contours',(.20,.29,.35),False)
for j in range(4,nz-1,4):
    if j%12==0:continue
    ids=np.arange(j*(na+1),(j+1)*(na+1))
    ob=line('Measured section %03d'%j,closed[ids],contour_ma,.00042);report.remove(ob)
    ob['source_row']=int(data['source_row'][j]);ob['purpose']='Contour through retained geometry samples'
    for i,src in enumerate(surf.data.shape_keys.key_blocks):
        key=ob.shape_key_add(name=src.name)
        key.data.foreach_set('co',np.array([src.data[int(k)].co[:] for k in ids],dtype='f').ravel())
    shape_objects.append(ob)
def plane(name,x0,x1,z0,z1,y,ma):
    me=bpy.data.meshes.new(name);me.from_pydata([(x0,y,z0),(x1,y,z0),(x1,y,z1),(x0,y,z1)],[],[(0,1,2,3)]);me.materials.append(ma)
    ob=link(bpy.data.objects.new(name,me));report.append(ob);return ob
font=next(f for f in bpy.data.fonts if f.name!='Bfont' and f.filepath)
def text(name,body,x,z,size=.035,ma=ink,y=-.04):
    cu=bpy.data.curves.new(name,'FONT');cu.font=font;cu.body=body;cu.size=size
    ob=link(bpy.data.objects.new(name,cu));cu.materials.append(ma);ob.location=(x,y,z);ob.rotation_euler=(math.pi/2,0,0);report.append(ob);return ob
plane('Replaceable illustrative report',-2.40,2.22,-1.22,1.30,.14,paper)
text('Main report title','Borehole interpretation',-2.25,1.115,.098)
text('Report status','ILLUSTRATIVE DATA',1.25,1.17,.048,blue)
text('Report process','Retrieved & processed after the run',-2.24,1.015,.038,dim)
text('Report identity','ECCO / OUTPUT STUDY',1.25,1.075,.031,dim)
line('Header rule',[(-2.25,-.03,.98),(2.08,-.03,.98)],grid,.0015)
# The original unfolded mesh remains the geometry-map track at world x [-pi*R,+pi*R].
tracks=[(-2.18,-1.70,'Diameter','MIN / MEAN / MAX'),(-1.60,-1.05,'Sections','SELECTED DEPTHS'),(-.99,-.60,'3D shape','SAME GEOMETRY'),(-.49,.49,'360° geometry','ANGLE FROM SEAM'),(.60,1.04,'Variation','RADIAL STD. DEV.'),(1.15,2.08,'Amplitude','SEPARATE SYNTHETIC DATA')]
for i,(a,b,title,sub) in enumerate(tracks):
    plane('Track %02d'%i,a,b,-H/2,H/2,.075,panel)
    text('Track title '+title,title,a,.909,.049)
    text('Track caption '+title,sub,a,-1.015,.025,dim)
    for dep in np.linspace(0,H,7):line('Depth register',[(a,.05,H/2-dep),(b,.05,H/2-dep)],grid,.00045)
    for x in (a,b):line('Track edge',[(x,.045,-H/2),(x,.045,H/2)],grid,.0006)
for x,t in [(-.49,'0°'),(-.07,'180°'),(.40,'360°'),(1.15,'0°'),(1.53,'180°'),(1.98,'360°')]:text('Azimuth '+t,t,x,.80,.027,dim,y=-.045)
text('Depth convention','DEPTH ↓',-2.32,-1.105,.034,dim)
text('Reference status','White nominal  /  Blue enlarged  /  Red tight',-1.91,-1.105,.033,dim)
text('Amplitude status','Amplitude is not geometry',.96,-1.105,.034,dim)
# Diameter is mean/min/max of opposite-radius sums, not 2*r at one azimuth.
diam=raw+np.roll(raw,na//2,axis=1)
stats=[diam.min(1),diam.mean(1),diam.max(1)];lo=float(diam.min())-.002;hi=float(diam.max())+.002
for vals,ma,nm in zip(stats,[red,ink,blue],['Minimum','Mean','Maximum']):
    xx=-2.18+.48*(vals-lo)/(hi-lo);line('Diameter '+nm,list(zip(xx,np.full(nz,-.03),H/2-depth)),ma,.0015)
refx=-2.18+.48*(2*R-lo)/(hi-lo)
line('Nominal diameter',[(refx,-.025,-H/2),(refx,-.025,H/2)],grid,.0008)
spread=raw.std(axis=1);xx=.62+.40*spread/max(spread.max(),1e-8)
line('Azimuthal radial standard deviation',list(zip(xx,np.full(nz,-.03),H/2-depth)),blue,.002)
rows=[int(np.argmax(raw)//na),int(nz/2),int(np.argmin(raw)//na)]
for j,zc in zip(rows,[.57,0,-.57]):
    for rr,ma,nm in [(np.full(na+1,R),grid,'Nominal'),(rad[j],blue,'Source')]:
        line('Cross section '+nm,[(float(-1.325+.98*rv*math.sin(a)),-.03,float(zc+.98*rv*math.cos(a))) for a,rv in zip(angles,rr)],ma,.0012)
    text('Section depth','z / H  %.2f'%(depth[j]/H),-1.54,zc-.23,.025,dim)
# Small 3D reconstruction uses the same closed vertices and color values.
mini=surf.copy();mini.data=surf.data.copy();mini.name='Report 3D | same source samples';link(mini);report.append(mini)
mini.data.shape_keys.animation_data_clear()
for key in mini.data.shape_keys.key_blocks:key.value=0
mini.location=(-.79,-.025,0);mini.scale=(.80,.80,1)
mma=surf.data.materials[0].copy();mini.data.materials.clear();mini.data.materials.append(mma);mma.node_tree.animation_data_clear()
mma.node_tree.nodes['SCULPTURE_TO_MAP'].inputs[0].default_value=0
n=mma.node_tree.nodes;l=mma.node_tree.links;out=n.get('Material Output');oldsocket=out.inputs[0].links[0].from_socket;l.remove(out.inputs[0].links[0])
tr=n.new('ShaderNodeBsdfTransparent');mx=n.new('ShaderNodeMixShader');mx.name='REPORT_REVEAL';mx.inputs[0].default_value=0;l.new(tr.outputs[0],mx.inputs[1]);l.new(oldsocket,mx.inputs[2]);l.new(mx.outputs[0],out.inputs[0]);mma.surface_render_method='BLENDED';fade_mats.append(mma)
# Independently authored illustrative amplitude, on the same coordinate grid.
# This generator uses angle/depth ONLY. No radius array or geometry-derived quantity.
AA,DD=np.meshgrid(angles[:-1],depth/H)
amp=np.clip(.48+.20*np.sin(2*math.pi*(9*DD+.21*np.sin(AA+.4)))+.13*np.sin(2*math.pi*(28*DD+.07*np.cos(2*AA)))+.10*np.cos(3*AA-9*DD)+.05*np.sin(7*AA+60*DD),0,1).astype('f')
np.savez_compressed(B/'Data/independent_amplitude.npz',amplitude_normalized=amp,relative_depth_m=depth,relative_azimuth_radians=angles[:-1])
cols=np.array([[.075,.035,.012],[.31,.13,.025],[.67,.37,.09],[.95,.76,.36],[1,.94,.74]])
aa=np.c_[amp,amp[:,0]];cc=np.stack([np.interp(aa.ravel(),np.linspace(0,1,5),cols[:,i]) for i in range(3)],axis=1)
points=np.stack([1.15+.93*TH/math.tau,np.full_like(TH,-.015),ZZ],axis=-1).reshape(-1,3)
me=bpy.data.meshes.new('Independent amplitude samples');me.from_pydata(points,[],[tuple(p.vertices) for p in surf.data.polygons]);me.update()
co=me.color_attributes.new(name='Independent synthetic amplitude',type='FLOAT_COLOR',domain='POINT');co.data.foreach_set('color',np.c_[cc,np.ones(len(cc))].astype('f').ravel())
at=me.attributes.new('amplitude_normalized','FLOAT','POINT');at.data.foreach_set('value',aa.ravel())
am=mat('Independent amplitude field',(.7,.4,.1));nd=am.node_tree.nodes;vc=nd.new('ShaderNodeVertexColor');vc.layer_name=co.name;am.node_tree.links.new(vc.outputs['Color'],nd.get('Emission').inputs[0]);me.materials.append(am)
ob=link(bpy.data.objects.new('Report independent amplitude | illustrative only',me));report.append(ob)
ob['provenance']='Independent analytic demonstrator; not sourced from geometry or field data'
np.savez_compressed(B/'Data/derived_report_arrays.npz',diameter_min_m=stats[0],diameter_mean_m=stats[1],diameter_max_m=stats[2],radial_std_m=spread,cross_section_rows=rows)
# Small persistent editorial identity follows the camera, with film-safe margins.
hudma=mat('Editorial identity',(.36,.48,.56),False)
hud=[]
for name,body,top in [('Source status','ILLUSTRATIVE DATA / PROCESSED AFTER THE RUN',False),('Sequence identity','ECCO    /    FROM DARKNESS TO UNDERSTANDING',True)]:
    o=text(name,body,0,0,.02,hudma);report.remove(o);o.parent=cam;o.rotation_euler=(0,0,0);hud.append((o,top))

def ease(t):t=max(0,min(1,t));return t*t*t*(t*(6*t-15)+10)
def pose(loc,target,lens,roll):
    cam.location=loc;cam.rotation_quaternion=(Vector(target)-Vector(loc)).to_track_quat('-Z','Y')@Quaternion((0,0,1),roll);cam.data.lens=lens
    w=2*36/lens
    for o,top in hud:o.location=(-w*.46,w*(9/16)*(.45 if top else -.46),-2);o.data.size=w*.009
def state(p,rv):
    q=p*32;low=int(q);t=q-low
    for ob in shape_objects:
        for i,key in enumerate(ob.data.shape_keys.key_blocks):
            if i:key.value=1-t if i==low else t if i==low+1 else 0
    mapmix.default_value=p
    for ma in fade_mats:ma.node_tree.nodes['REPORT_REVEAL'].inputs[0].default_value=rv
    for o,top in hud:o.hide_render=rv>.98

keys=[(1,(.35,-2.1,3.1),(.01,.156,.08),52,-.90),
      (61,(.15,-2.30,2.85),(.02,.156,.08),52,-.83),
      (145,(-2.2,-4.25,1.30),(-.025,.18,.02),52,-.32),
      (211,(0,-5.05,.03),(0,0,.03),52,0),
      (264,(-.10,-7.15,.10),(-.10,0,.04),52,0),
      (288,(-.10,-7.08,.10),(-.10,0,.04),52,0)]

def arrival(i):
    p,rv,key=[(0,0,keys[1]),(.50,0,keys[2]),(1,1,keys[-1])][i-1]
    state(p,rv);pose(*key[1:])
    s.frame_set(1);bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all()
    bpy.ops.wm.save_as_mainfile(filepath=str(B/f'Scenes/Arrival_{i}_v002.blend'),relative_remap=False)
    s.render.filepath=str(B/f'Previews/S06_arrival_{i:02d}_v002.png');start=time.perf_counter();bpy.ops.render.render(write_still=True);elapsed=time.perf_counter()-start
    if elapsed>=5:raise RuntimeError('Arrival over frame budget: '+str(elapsed))
    return elapsed
if '--animate' not in sys.argv:
    times=[arrival(i) for i in (1,2,3)]
    (B/'Records/arrival-benchmark.json').write_text(json.dumps(times),encoding='utf-8')
else:
    score=[]
    for f in range(1,289):
        p=ease((f-73)/138);rv=ease((f-217)/36)
        state(p,rv)
        for ob in shape_objects:
            for key in list(ob.data.shape_keys.key_blocks)[1:]:key.keyframe_insert('value',frame=f)
        mapmix.keyframe_insert('default_value',frame=f)
        for ma in fade_mats:ma.node_tree.nodes['REPORT_REVEAL'].inputs[0].keyframe_insert('default_value',frame=f)
        for a,b in zip(keys[:-1],keys[1:]):
            if a[0]<=f<=b[0]:
                t=ease((f-a[0])/(b[0]-a[0]));vals=[np.array(x)*(1-t)+np.array(y)*t for x,y in zip(a[1:],b[1:])];break
        pose(*vals)
        cam.keyframe_insert('location',frame=f);cam.keyframe_insert('rotation_quaternion',frame=f);cam.data.keyframe_insert('lens',frame=f)
        for o,top in hud:o.keyframe_insert('location',frame=f);o.data.keyframe_insert('size',frame=f);o.keyframe_insert('hide_render',frame=f)
        score.append({'frame':f,'unfold':p,'report':rv,'camera':list(cam.location),'lens':float(cam.data.lens)})
    for action in bpy.data.actions:
        for layer in action.layers:
            for strip in layer.strips:
                for bag in strip.channelbags:
                    for fc in bag.fcurves:
                        for k in fc.keyframe_points:k.interpolation='LINEAR'
    s['source_data']='//../Data/surface_samples.npz';s['scope']='v002 targeted cinematic refinement; illustrative data; owner review candidate'
    s.frame_set(1);bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all()
    bpy.ops.wm.save_as_mainfile(filepath=str(B/'Scenes/S06_cinematic-study_v002.blend'),relative_remap=False)
    (B/'Records/camera-score.json').write_text(json.dumps(score,indent=2),encoding='utf-8')
(B/'Records/refinement.json').write_text(json.dumps({'base_native':str(OLD/'Scenes/S06_journey_v001.blend'),'base_vertices_sha256':base_hash,'source_values_changed':False,'surface_normals_flipped_for_outward_shading':flipped,'shape_keys_reused':len(surf.data.shape_keys.key_blocks),'geometry_samples':raw.size,'report_cross_section_rows':rows,'amplitude_provenance':'Independent analytic illustrative dataset; same relative depth and seam azimuth grid; no geometry-value dependency','amplitude_generator':'See refine.py AA/DD formula; periodic azimuth terms; no random seed or field data','timing_seconds':[3,6,3],'report_data_replaceable':True},indent=2),encoding='utf-8')
print('REFINEMENT COMPLETE')
