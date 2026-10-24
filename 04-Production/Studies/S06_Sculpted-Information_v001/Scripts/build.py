"""Fresh S06 proof. Only source values/data reused; no historical S06 architecture."""
import bpy, math, json, time
import numpy as np
from pathlib import Path
from mathutils import Vector, Quaternion

B=Path(__file__).resolve().parents[1]
D=np.load(B/'Data/surface_samples.npz')
R=.156
raw=D['radius_m']; nz,na=raw.shape
r=np.c_[raw,raw[:,0]]
theta=np.linspace(0,math.tau,na+1)
depth=D['depth_from_interval_top_m']; H=float(depth[-1])
TH,DP=np.meshgrid(theta,depth)
ZZ=H/2-DP
DEV=r-R

def coords(p):
    # Constant reference arc length. The radial residual becomes color on the final map.
    c=1-p
    if c<1.e-7:
        xx=R*(TH-math.pi); yy=np.zeros_like(TH)
    else:
        q=c*TH
        xx=R*np.sin(q)/c-R*math.pi*p+DEV*c*np.sin(q)
        yy=R*(1-np.cos(q))/c-DEV*c*np.cos(q)
    return np.stack([xx,yy,ZZ],axis=-1).reshape(-1,3).astype('f')

sc=bpy.data.scenes.new('S06 | Sculpted information | fresh proof v001')
bpy.context.window.scene=sc
sc.render.engine='BLENDER_EEVEE'
sc.eevee.taa_render_samples=8
sc.render.resolution_x=960;sc.render.resolution_y=540;sc.render.resolution_percentage=100
sc.render.fps=24;sc.frame_start=1;sc.frame_end=120
sc.render.image_settings.file_format='PNG'
sc.render.film_transparent=False
sc.world=bpy.data.worlds.new('S06 quiet navy');sc.world.use_nodes=True
sc.world.node_tree.nodes['Background'].inputs[0].default_value=(.012,.021,.031,1)
sc.world.node_tree.nodes['Background'].inputs[1].default_value=.45
sc.view_settings.view_transform='Standard'
sc.view_settings.look='None'
sc.view_settings.exposure=0;sc.view_settings.gamma=1

def link(o):sc.collection.objects.link(o);return o
def mat(name,col,emission=True,fade=False):
    m=bpy.data.materials.new(name);m.diffuse_color=(*col,1);m.use_nodes=True
    n=m.node_tree.nodes;n.clear();l=m.node_tree.links
    if emission:
        sh=n.new('ShaderNodeEmission');sh.inputs[0].default_value=(*col,1);sh.inputs[1].default_value=1
    else:
        sh=n.new('ShaderNodeBsdfPrincipled');sh.inputs['Base Color'].default_value=(*col,1);sh.inputs['Roughness'].default_value=.76
    out=n.new('ShaderNodeOutputMaterial')
    if fade:
        tr=n.new('ShaderNodeBsdfTransparent');mix=n.new('ShaderNodeMixShader');mix.name='REPORT_REVEAL'
        mix.inputs[0].default_value=0;l.new(tr.outputs[0],mix.inputs[1]);l.new(sh.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],out.inputs[0]);m.surface_render_method='BLENDED'
    else:l.new(sh.outputs[0],out.inputs[0])
    return m

white=mat('Fine ivory data reference',(.63,.76,.82))
seam=mat('Reference seam - restrained amber',(.56,.35,.12))
gridmat=mat('Data-space register',(.045,.09,.13))
blue=mat('Geometry blue',(.04,.35,.66))

mesh=bpy.data.meshes.new('Same radius samples in every display state')
faces=[(j*(na+1)+k,j*(na+1)+k+1,(j+1)*(na+1)+k+1,(j+1)*(na+1)+k) for j in range(nz-1) for k in range(na)]
mesh.from_pydata(coords(0),[],faces);mesh.update()
surf=link(bpy.data.objects.new('Recorded geometry | illustrative S03 source',mesh))
for f in mesh.polygons:f.use_smooth=True
attr=mesh.attributes.new('source_radius_m','FLOAT','POINT');attr.data.foreach_set('value',r.ravel())
ids=mesh.attributes.new('source_sample_id','INT','POINT');ids.data.foreach_set('value',np.c_[np.arange(nz*na).reshape(nz,na),np.arange(nz)*na].ravel())
dep=mesh.attributes.new('relative_depth_m','FLOAT','POINT');dep.data.foreach_set('value',DP.ravel())
ang=mesh.attributes.new('map_azimuth_rad','FLOAT','POINT');ang.data.foreach_set('value',TH.ravel())

def geometry_color(delta):
    pale=np.array([.78,.86,.90]); deep=np.array([.025,.21,.52]);red=np.array([.61,.065,.075])
    c=np.tile(pale,(len(delta),1))
    pos=np.clip((delta-.001)/.025,0,1)**.58
    neg=np.clip((-delta-.001)/.001,0,1)**.65
    c=c*(1-pos[:,None])+deep*pos[:,None]
    c=c*(1-neg[:,None])+red*neg[:,None]
    return np.c_[c,np.ones(len(c))].astype('f')
col=mesh.color_attributes.new(name='Radius colors - retained sample values',type='FLOAT_COLOR',domain='POINT')
col.data.foreach_set('color',geometry_color(DEV.ravel()).ravel())
m=bpy.data.materials.new('White nominal | blue enlarged | red tight');m.use_nodes=True
n=m.node_tree.nodes;n.clear();l=m.node_tree.links
at=n.new('ShaderNodeVertexColor');at.layer_name=col.name
pr=n.new('ShaderNodeBsdfPrincipled');pr.inputs['Roughness'].default_value=.8;pr.inputs['Specular IOR Level'].default_value=.18
l.new(at.outputs['Color'],pr.inputs['Base Color']);l.new(at.outputs['Color'],pr.inputs['Emission Color']);pr.inputs['Emission Strength'].default_value=.22
em=n.new('ShaderNodeEmission');l.new(at.outputs['Color'],em.inputs[0]);em.inputs[1].default_value=1
mx=n.new('ShaderNodeMixShader');mx.name='SCULPTURE_TO_MAP';mx.inputs[0].default_value=0;l.new(pr.outputs[0],mx.inputs[1]);l.new(em.outputs[0],mx.inputs[2])
out=n.new('ShaderNodeOutputMaterial');l.new(mx.outputs[0],out.inputs[0]);mesh.materials.append(m)
surf['data_status']='S03 synthetic illustrative radius data, subset; not field data'
surf['unfold_meaning']='Display-coordinate transform only, not physical rock deformation'
surf['source_seam_degrees']=240
surf['reference_radius_m']=R

surf.shape_key_add(name='Closed reconstruction')
for i in range(1,33):
    key=surf.shape_key_add(name='Unfold %02d'%i);key.data.foreach_set('co',coords(i/32).ravel())

# Coarse registration lines are display guides, not claims of sensor resolution.
guide_ids=[]
for k in range(0,na+1,24):guide_ids.append([j*(na+1)+k for j in range(nz)])
for j in range(0,nz,12):guide_ids.append([j*(na+1)+k for k in range(na+1)])
def line(name,pts,material,width=.0005):
    cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=width;cu.bevel_resolution=0
    sp=cu.splines.new('POLY');sp.points.add(len(pts)-1)
    for v,p in zip(sp.points,pts):v.co=(*p,1)
    ob=link(bpy.data.objects.new(name,cu));cu.materials.append(material);return ob

# Guides deform with the exact same shape-key coordinates, with a tiny camera-side offset.
def ribbon(name,indices,material,width):
    allverts=[];ff=[]
    for j in range(len(indices)-1):
        for idx in (indices[j],indices[j+1]):
            v=coords(0)[idx];allverts.extend([v+[0,-.0008,-width],v+[0,-.0008,width]])
        b=4*j;ff.append((b,b+1,b+3,b+2))
    # Generic fixed camera-side offset isn't a true surface-normal stroke; use sparse points instead below.

# Thin line curves get baked per-frame keys after the arrivals are inspected.
guides=[]
for gi,indices in enumerate(guide_ids):
    ob=line('Registration %02d'%gi,coords(0)[indices],gridmat,.00028)
    guides.append((ob,indices))
seams=[]
for k in (0,na):
    ids0=[j*(na+1)+k for j in range(nz)]
    ob=line('Seam %s'%('0' if k==0 else '360'),coords(0)[ids0],seam,.0008)
    seams.append((ob,ids0))

for name,loc,power,size in [('Key',(-2,-3,3),180,3),('Fill',(2,-1,1),90,2),('Rim',(1,2,2),160,2)]:
    ld=bpy.data.lights.new('S06 '+name,'AREA');ld.energy=power;ld.shape='DISK';ld.size=size
    lo=link(bpy.data.objects.new(ld.name,ld));lo.location=loc;lo.rotation_euler=(Vector((0,0,0))-lo.location).to_track_quat('-Z','Y').to_euler()

camd=bpy.data.cameras.new('S06 authored camera');cam=link(bpy.data.objects.new('S06 camera',camd));sc.camera=cam
camd.type='ORTHO';camd.ortho_scale=3.65;camd.clip_start=.01;camd.clip_end=100
cam.rotation_mode='QUATERNION'

font=bpy.data.fonts.load('C:/Windows/Fonts/segoeui.ttf')
def textob(name,text,pos,size,material,align='LEFT',parent=None):
    cu=bpy.data.curves.new(name,'FONT');cu.body=text;cu.font=font;cu.size=size;cu.align_x=align
    ob=link(bpy.data.objects.new(name,cu));cu.materials.append(material)
    if parent:ob.parent=parent;ob.location=pos
    else:ob.location=pos;ob.rotation_euler=(math.pi/2,0,0)
    return ob

hud=mat('Editorial text',(.45,.59,.67))
textob('Source notice','ILLUSTRATIVE DATA',(-1.68,-.91,-2),.030,hud,parent=cam)
textob('Proof identity','ECCO / RECORDED GEOMETRY',(-1.68,.86,-2),.032,hud,parent=cam)

report=[]
paper=mat('Report ground',(.025,.043,.057),fade=True)
ink=mat('Report text',(.67,.77,.82),fade=True)
dim=mat('Report secondary',(.29,.43,.51),fade=True)
rb=mat('Report geometry blue',(.04,.32,.62),fade=True)
rr=mat('Report geometry red',(.61,.065,.075),fade=True)
def plane(name,x0,x1,z0,z1,y,ma):
    me=bpy.data.meshes.new(name);me.from_pydata([(x0,y,z0),(x1,y,z0),(x1,y,z1),(x0,y,z1)],[],[(0,1,2,3)])
    ob=link(bpy.data.objects.new(name,me));me.materials.append(ma);report.append(ob);return ob
plane('Illustrative engineering report',-.70,1.44,-1.13,1.23,.055,paper)
def rt(name,txt,x,z,size=.037,ma=ink):
    o=textob(name,txt,(x,-.022,z),size,ma);report.append(o);return o
rt('Report title','Borehole geometry',-.55,1.09,.09)
rt('Report subtitle','ILLUSTRATIVE DATA  /  PROCESSED AFTER THE RUN',-.55,1.005,.033,dim)
rt('Map title','360° geometry map',-.49,.927,.043)
rt('Az 0','0°',-.49,.872,.035,dim);rt('Az 180','180°',-.035,.872,.035,dim);rt('Az 360','360°',.42,.872,.035,dim)
rt('Profile title','Same interval',.65,.70,.060)
rt('Profile label','CROSS-SECTION',.65,.63,.038,dim)
rt('Profile source','From the blue feature',.65,.13,.038,dim)
rt('Legend title','Geometry',.65,-.04,.050)
for i,(label,ma) in enumerate([('Nominal',ink),('Enlarged',rb),('Tight',rr)]):
    z=-.14-i*.1;report.append(line('Legend '+label,[(.65,-.023,z),(.73,-.023,z)],ma,.003));rt('Legend word '+label,label,.76,z-.013,.042)
rt('Coordinates','Angle →',-.49,-.97,.043,dim)
rt('Depth direction','Depth increases ↓',-.49,-1.045,.043,dim)
rt('Provenance 1','Synthetic source',.65,-.58,.040,dim)
rt('Provenance 2','No field readings',.65,-.65,.040,dim)
rt('Provenance 3','Geometry only',.65,-.72,.040,dim)
rt('Provenance 4','Amplitude is a',.65,-.84,.035,dim)
rt('Provenance 5','separate property',.65,-.90,.035,dim)

blue_row=int(np.unravel_index(raw.argmax(),raw.shape)[0]);rad=raw[blue_row]
aa=np.r_[theta[:-1],theta[-1]];rv=np.r_[rad,rad[0]]
for name,values,ma in [('Nominal',np.full_like(rv,R),dim),('Reconstructed',rv,rb)]:
    pts=[(.87+float(x)*.95,-.025,.39+float(z)*.95) for x,z in zip(values*np.sin(aa),values*np.cos(aa))]
    report.append(line('Report profile '+name,pts,ma,.0012))

def smooth(t):t=max(0,min(1,t));return t*t*t*(t*(6*t-15)+10)
def pose(loc,target,scale,roll=0):
    cam.location=loc;cam.rotation_quaternion=(Vector(target)-Vector(loc)).to_track_quat('-Z','Y')@Quaternion((0,0,1),roll);camd.ortho_scale=scale
    for name,top in [('Proof identity',True),('Source notice',False)]:
        ob=bpy.data.objects[name];ob.location=(-scale*.455,scale*(9/16)*(.435 if top else -.455),-2);ob.data.size=scale*.0125
def state(p):
    q=p*32;left=int(q);blend=q-left
    for i,k in enumerate(surf.data.shape_keys.key_blocks):
        if i==0:continue
        k.value=(1-blend if i==left else blend if i==left+1 else 0)
    cc=coords(p)
    mx.inputs[0].default_value=p
    for ob,idx in guides+seams:
        for pt,co in zip(ob.data.splines[0].points,cc[idx]):pt.co=(*co,1)
def report_value(value):
    for ma in (paper,ink,dim,rb,rr):ma.node_tree.nodes['REPORT_REVEAL'].inputs[0].default_value=value

def arrival(i):
    if i==1:
        state(0);report_value(0);pose((1.7,-3.2,2.1),(0,.13,0),3.7,-.40)
    elif i==2:
        state(.48);report_value(0);pose((.9,-3.8,.8),(-.03,.20,0),3.85,-.055)
    else:
        state(1);report_value(1);pose((.35,-4,.04),(.35,0,.04),4.75,0)

# Save three composed states before designing in-between motion.
for i in (1,2,3):
    arrival(i)
    sc['arrival']=i
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(B/f'Scenes/Arrival_{i}.blend'),relative_remap=False)
arrival(1)
bpy.ops.wm.save_as_mainfile(filepath=str(B/'Scenes/S06_unfold_working_v001.blend'),relative_remap=False)
(B/'Records/build.json').write_text(json.dumps({'source_samples':int(raw.size),'mesh_vertices':len(mesh.vertices),'nominal_radius_m':R,'height_m':H,'shape_keys':33,'display_coordinate_rule':'constant reference arc length; radial deviation retained as source data and color, relief eases to zero','source_values_changed':False,'historical_S06_contracts_used':False,'amplitude_shown':False},indent=2))
print('S06 BUILD COMPLETE',B)
