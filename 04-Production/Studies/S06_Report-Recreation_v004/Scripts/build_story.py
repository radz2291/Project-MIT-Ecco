import bpy,math,json,time,hashlib,sys
import numpy as np
from pathlib import Path
from mathutils import Vector,Quaternion
from bpy_extras.object_utils import world_to_camera_view
B=Path(__file__).resolve().parents[1];PROD=B.parents[1]
D=np.load(B/'Data/story_field.npz');R=float(D['R']);H=float(D['H']);raw=D['radius'];G=D['geometry'];amp=D['amplitude'];nz,na=raw.shape
rr=np.c_[raw,raw[:,0]];gg=np.c_[G,G[:,0]];aa=np.c_[amp,amp[:,0]]
TH,ZZ=np.meshgrid(np.linspace(0,math.tau,na+1),D['z']);nc=na+1
faces=[(j*nc+k,j*nc+k+1,(j+1)*nc+k+1,(j+1)*nc+k) for j in range(nz-1) for k in range(na)]
bpy.ops.wm.read_factory_settings(use_empty=True)
font=bpy.data.fonts.load('C:/Windows/Fonts/segoeui.ttf')
def link(ob):s.collection.objects.link(ob);return ob
def mat(name,col,lit=False,metal=0,rough=.4,power=1,alpha=1):
    m=bpy.data.materials.new(name);m.diffuse_color=(*col,1);m.use_nodes=True;n=m.node_tree.nodes;n.clear();l=m.node_tree.links
    out=n.new('ShaderNodeOutputMaterial');sh=n.new('ShaderNodeBsdfPrincipled' if lit else 'ShaderNodeEmission')
    if lit:
        sh.inputs['Base Color'].default_value=(*col,1);sh.inputs['Metallic'].default_value=metal;sh.inputs['Roughness'].default_value=rough
    else:sh.inputs[0].default_value=(*col,1);sh.inputs[1].default_value=power
    if alpha<1:
        tr=n.new('ShaderNodeBsdfTransparent');mix=n.new('ShaderNodeMixShader');mix.inputs[0].default_value=alpha;l.new(tr.outputs[0],mix.inputs[1]);l.new(sh.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],out.inputs[0]);m.surface_render_method='BLENDED'
    else:l.new(sh.outputs[0],out.inputs[0])
    return m
def mesh(name,verts,fs,ma):
    me=bpy.data.meshes.new(name);me.from_pydata(verts,[],fs);me.update();me.materials.append(ma);return link(bpy.data.objects.new(name,me))
def curve(name,pts,ma,width=.0007,parent=None):
    cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=width;cu.bevel_resolution=0;sp=cu.splines.new('POLY');sp.points.add(len(pts)-1)
    for p,co in zip(sp.points,pts):p.co=(*co,1)
    cu.materials.append(ma);o=link(bpy.data.objects.new(name,cu));o.parent=parent;return o
def text(name,body,pos,size,ma,parent=None):
    cu=bpy.data.curves.new(name,'FONT');cu.body=body;cu.font=font;cu.size=size;cu.materials.append(ma)
    o=link(bpy.data.objects.new(name,cu));o.location=pos;o.rotation_euler=(math.pi/2,0,0);o.parent=parent;return o
def plane(name,x0,x1,z0,z1,y,ma):return mesh(name,[(x0,y,z0),(x1,y,z0),(x1,y,z1),(x0,y,z1)],[(0,1,2,3)],ma)
def palette(vals,cols):return np.stack([np.interp(vals.ravel(),np.linspace(0,1,len(cols)),np.array(cols)[:,i]) for i in range(3)],1)
GC=palette((gg+1)/2,[(.55,.055,.032),(.80,.40,.28),(.80,.90,1),(.08,.39,.80),(.012,.13,.50)])
AC=palette(aa,[(.09,.036,.008),(.28,.11,.023),(.53,.27,.055),(.79,.51,.18),(.97,.79,.39)])
def colored(name,verts,fs,cols,lit=False,alpha=1,power=1):
    m=mat(name+' material',(1,1,1),lit,rough=.65,alpha=alpha,power=power);o=mesh(name,verts,fs,m)
    co=o.data.color_attributes.new(name='Illustrative sample colors',type='FLOAT_COLOR',domain='POINT');co.data.foreach_set('color',np.c_[cols,np.ones(len(cols))].astype('f').ravel())
    nd=m.node_tree.nodes;v=nd.new('ShaderNodeVertexColor');v.layer_name=co.name;sh=nd.get('Principled BSDF') if lit else nd.get('Emission');m.node_tree.links.new(v.outputs['Color'],sh.inputs['Base Color'] if lit else sh.inputs[0]);return o
def scene(name):
    global s
    s=bpy.data.scenes.new(name);bpy.context.window.scene=s;s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=16
    s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.view_settings.view_transform='AgX'
    s.world=bpy.data.worlds.new(name+' studio');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.035,.06,.085,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.25
    s['scope']='v004 one A-B-C still review; no motion approval or sequence integration';return s
def camera(loc,target,lens=55,roll=0):
    cd=bpy.data.cameras.new(s.name+' camera');o=link(bpy.data.objects.new(cd.name,cd));o.location=loc;o.rotation_mode='QUATERNION';o.rotation_quaternion=(Vector(target)-o.location).to_track_quat('-Z','Y')@Quaternion((0,0,1),math.radians(roll));cd.lens=lens;cd.clip_start=.01;s.camera=o;return o
def light(name,loc,target,power,size,color=(.8,.9,1)):
    ld=bpy.data.lights.new(name,'AREA');ld.energy=power;ld.shape='DISK';ld.size=size;ld.color=color;o=link(bpy.data.objects.new(name,ld));o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
def cube(name,loc,scale,ma,bevel=0):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.scale=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(ma)
    if bevel:b=o.modifiers.new('Soft machined edges','BEVEL');b.width=bevel;b.segments=3;o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
    return o
def coords(p):
    # One curling display surface, peeled toward +X. Sample order never changes.
    dist=R*TH;curl=math.tau*R*(1-p);t=(dist-curl)/R;dev=(rr-R)*(1-p)
    X=np.where(dist<curl,(R+dev)*np.sin(t),dist-curl)
    Y=np.where(dist<curl,-(R+dev)*np.cos(t),-R-dev)
    return np.stack([X,Y,ZZ],-1).reshape(-1,3)
def surface(name,p,alpha):
    pos=coords(p);o=colored(name,pos,faces,GC,alpha=alpha,power=.65)
    for poly in o.data.polygons:poly.use_smooth=True
    for nm,kind,vals in [('sample_id','INT',np.c_[np.arange(nz*na).reshape(nz,na),np.arange(nz)*na].ravel()),('illustrative_radius_m','FLOAT',rr.ravel()),('depth_order','INT',np.repeat(np.arange(nz),nc)),('azimuth_rad','FLOAT',TH.ravel())]:
        at=o.data.attributes.new(nm,kind,'POINT');at.data.foreach_set('value',vals)
    o['source']='Data/story_field.npz';o['p']=p;o['meaning']='Coordinate representation only. No physical wall movement.'
    o.shape_key_add(name='Review pose')
    for pp,nm in [(0,'Closed'),(1,'Flat')]:
        k=o.shape_key_add(name=nm);k.data.foreach_set('co',coords(pp).astype('f').ravel());k.value=0
    return o,pos
def points(name,pos,cols,ids,size):
    vs=[];fs=[];cc=[];base=np.array([(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)])*size
    octfs=[(0,2,4),(2,1,4),(1,3,4),(3,0,4),(2,0,5),(1,2,5),(3,1,5),(0,3,5)]
    for ix in ids:
        off=len(vs);vs.extend(pos[ix]+base);fs.extend(tuple(off+k for k in f) for f in octfs);cc.extend([cols[ix]]*6)
    return colored(name,vs,fs,np.array(cc),power=2.2)
def guides(pos,prefix,bright=False):
    cmat=mat(prefix+' guide color',(.20,.46,.72),power=1.4)
    for j in range(0,nz,8):curve(prefix+' depth contour',pos[j*nc:(j+1)*nc],cmat,.00062)
    for k in range(0,nc,12):curve(prefix+' length contour',pos[k::nc],cmat,.00040)
    seam=mat(prefix+' seam',(.64,.85,1),power=1.6)
    for k in (0,na):curve(prefix+' opening edge',pos[k::nc],seam,.0012)
    for j in (0,nz-1):curve(prefix+' visible end contour',pos[j*nc:(j+1)*nc],seam,.0014)
def hud(cam,body):
    ma=mat('Quiet caption',(.38,.52,.64),power=.7);o=text('Illustrative status',body,(0,0,0),.012,ma,cam);o.rotation_euler=(0,0,0);w=2*36/cam.data.lens;o.location=(-w*.45,-w*.246,-2);o.data.size=w*.008

# A: retained product at actual source scale in a fixed sectional borehole.
scene('A | Borehole to reconstruction')
src=PROD/'Shared/Assets/ECCO/ECCO_master_temporary-plugs_v002.blend'
with bpy.data.libraries.load(str(src),link=False) as (a,b):b.collections=['ECCO_MASTER_v002']
col=b.collections[0];s.collection.children.link(col);root=bpy.data.objects['ECCO_ROOT'];root.rotation_euler=(0,-math.pi/2,0);root.location=(0,0,-H/2)
bpy.context.view_layer.update();housing=bpy.data.objects['ECCO_HOUSING_SOURCE_MESH']
coords_before=np.array([v.co[:] for v in housing.data.vertices],dtype='f');source_mesh_hash=hashlib.sha256(coords_before.tobytes()).hexdigest()
steel=mat('Review steel | source mesh unchanged',(.23,.29,.35),True,.85,.29)
for ob in col.all_objects:
    if ob.type=='MESH' and not ob.hide_render:ob.data.materials.clear();ob.data.materials.append(steel)
rot=bpy.data.objects['ECCO_ROTATION_X'];rot.rotation_euler.x=math.radians(18)
rock=mat('Contextual rock',(.006,.009,.013),True,0,.88)
n=rock.node_tree.nodes;l=rock.node_tree.links;noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=95;noise.inputs['Detail'].default_value=3;bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.65;bump.inputs['Distance'].default_value=.008;l.new(noise.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs['Normal'],n.get('Principled BSDF').inputs['Normal'])
verts=[];nrock=65
for j,z in enumerate(D['z']):
    for th in np.linspace(-1.92,1.92,nrock):
        ix=int((th%(math.tau))/math.tau*na)%na;r=float(raw[j,ix])+.009+.002*math.sin(29*th+13*z)*math.sin(31*z-8*th);verts.append((r*math.sin(th),r*math.cos(th),float(z)))
ob=mesh('Fixed borehole context | open viewing sector',verts,[(j*nrock+k,j*nrock+k+1,(j+1)*nrock+k+1,(j+1)*nrock+k) for j in range(nz-1) for k in range(nrock-1)],rock)
for poly in ob.data.polygons:poly.use_smooth=True
# Fixed rock thickness at the viewing-sector boundaries, preserving the visible inner radius.
for th in (-1.92,1.92):
    vv=[];steps=18
    for j,z in enumerate(D['z']):
        ix=int((th%math.tau)/math.tau*na)%na
        for k,rad in enumerate(np.linspace(float(raw[j,ix])+.009,.80,steps)):
            relief=(.009*math.sin(47*rad+23*z)+.008*math.sin(79*rad-51*z)+.012*math.sin(18*rad+14*z))*min(1,k/2)
            vv.append((rad*math.sin(th),rad*math.cos(th)+relief,float(z)))
    mesh('Rock sectional mass',vv,[(j*steps+k,j*steps+k+1,(j+1)*steps+k+1,(j+1)*steps+k) for j in range(nz-1) for k in range(steps-1)],rock)
o,pos=surface('A | reconstructed wall beginning to open',.065,.075)
ids=[j*nc+k for j in range(0,nz,2) for k in range(0,nc,2)]
points('A | indexed reconstruction samples',pos,GC,ids,.00105);guides(pos,'A')
light('A broad steel key',(.6,-1.1,.6),(0,0,0),38,1.4)
light('A raking rim',(-.5,.4,1),(0,0,0),90,.8,(.3,.6,1))
light('A warm fill',(-.6,-.5,-.9),(0,0,-.4),25,.7,(1,.85,.65))
cam=camera((.45,-2.25,1.10),(0,0,-.04),48,57);hud(cam,'ILLUSTRATIVE RECONSTRUCTION  /  PROCESSED AFTER THE RUN')
A=s
# B: same samples, partially unwrapped with independent warm output alongside.
scene('B | Same surface unfolds')
o,pos=surface('B | same reconstructed samples',.35,.22);guides(pos,'B')
points('B | same indexed samples',pos,GC,[j*nc+k for j in range(0,nz,2) for k in range(0,nc,2)],.00115)
x0=math.tau*R*.35+.045;aw=.52
av=np.stack([x0+aw*TH/math.tau,np.full_like(TH,-R),ZZ],-1).reshape(-1,3)
ao=colored('B | independent amplitude',av,faces,AC,alpha=.66,power=.85)
points('B | amplitude samples',av,AC,[j*nc+k for j in range(0,nz,3) for k in range(0,nc,3)],.0009)
gold=mat('Amplitude boundary',(.56,.29,.07),power=1.1)
for k in (0,na):curve('Amplitude edge',av[k::nc],gold,.001)
bg=mat('B background',(.004,.009,.017));plane('Quiet data space',-10,10,-10,10,1.8,bg)
light('B fill',(0,-2,3),(.5,0,0),50,3)
cam=camera((-1.32,-5.40,-2.76),(.31,0,0),55,53)
# Fit the complete unfolding and amplitude pair with breathing room; no accidental edge crop.
bpy.context.view_layer.update()
fitpts=[v.co.copy() for ob in (o,ao) for v in list(ob.data.vertices)[::4]]
def projected():
    v=np.array([world_to_camera_view(s,cam,p)[:2] for p in fitpts]);return v.min(0),v.max(0)
lofit,hifit=projected();span=hifit-lofit;cam.data.lens*=min(1,.88/max(span))
for prop,axis in [('shift_x',0),('shift_y',1)]:
    low,high=projected();center=(low[axis]+high[axis])/2;old=getattr(cam.data,prop)
    setattr(cam.data,prop,old+.01);low2,high2=projected();deriv=((low2[axis]+high2[axis])/2-center)/.01
    setattr(cam.data,prop,old+(.5-center)/deriv)
hud(cam,'ONE GEOMETRY FIELD  /  SEPARATE AMPLITUDE CHANNEL  /  ILLUSTRATIVE')
Bscene=s
# C: new vector report held within a physical laptop, all geometry-derived panels share A/B data.
scene('C | Laptop engineering payoff')
s.view_settings.view_transform='Standard'
paper=mat('C pearl',( .80,.84,.87));ink=mat('C ink',(.025,.055,.08));dim=mat('C secondary',(.17,.25,.31));grid=mat('C grid',(.52,.62,.68));blue=mat('C blue',(.025,.23,.47));pale=mat('C panels',(.90,.93,.95))
screenroot=link(bpy.data.objects.new('Laptop screen contents',None));screenroot.location=(0,.16,.28);screenroot.rotation_euler.x=math.radians(-12)
report=[]
def reg(ob):report.append(ob);return ob
reg(plane('Screen paper',-1.49,1.49,0,1.68,-.025,paper))
reg(text('Report title','Borehole interpretation',(-1.39,-.035,1.54),.067,ink))
reg(text('Report subtitle','Reconstructed geometry and acoustic response',(-1.39,-.035,1.435),.027,dim))
reg(text('Report provenance','ILLUSTRATIVE',(.99,-.035,1.55),.028,dim))
reg(curve('Header rule',[(-1.39,-.03,1.385),(1.39,-.03,1.385)],grid,.0012))
tracks=[(-1.38,-1.00,'Profile'),(-.92,-.43,'Sections'),(-.35,.02,'3D shape'),(.10,.73,'360 geometry'),(.81,1.39,'Amplitude')]
lo=.17;hi=1.23;hh=hi-lo
for xa,xb,title in tracks:
    reg(plane('Screen '+title,xa,xb,lo,hi,-.03,pale));reg(text('Screen label '+title,title,(xa,-.04,1.285),.034,ink))
    for z in np.linspace(lo,hi,8):reg(curve('Screen guide',[(xa,-.035,z),(xb,-.035,z)],grid,.0007))
diam=D['diameter'];mi=float(diam.min());ma=float(diam.max())
for vv,cc in zip(diam,[dim,ink,blue]):reg(curve('Screen diameter from shared radius',[(-1.35+.30*float((v-mi)/(ma-mi)),-.05,hi-hh*j/(nz-1)) for j,v in enumerate(vv)],cc,.0015))
for row,zc in [(int(nz*.25),.99),(int(nz*.75),.43)]:
    for r in np.linspace(.025,.18,6):reg(curve('Screen polar guide',[(-.675+r*math.cos(a),-.045,zc+r*math.sin(a)) for a in np.linspace(0,math.tau,97)],grid,.00065))
    for a in np.linspace(0,math.tau,8,endpoint=False):reg(curve('Screen polar spoke',[(-.675,-.045,zc),(-.675+.18*math.cos(a),-.045,zc+.18*math.sin(a))],grid,.00065))
    reg(curve('Screen section from shared radius',[(-.675+.12*float(r/R)*math.cos(a),-.052,zc+.12*float(r/R)*math.sin(a)) for a,r in zip(np.linspace(0,math.tau,nc),rr[row])],blue,.0021))
mini_coords=coords(0).copy();mini_coords[:,0]=-.165+mini_coords[:,0]*.72;mini_coords[:,1]=-.11+mini_coords[:,1]*.72;mini_coords[:,2]=(hi+lo)/2+mini_coords[:,2]*(hh/H)
mini=colored('C | same geometry reconstruction',mini_coords,faces,GC,True);reg(mini)
for p in mini.data.polygons:p.use_smooth=True
for name,xa,xb,cc in [('C | same geometry map',.10,.73,GC),('C | independent amplitude',.81,1.39,AC)]:
    v=np.stack([xa+(xb-xa)*TH/math.tau,np.full_like(TH,-.055),(hi+lo)/2+ZZ*hh/H],-1).reshape(-1,3);reg(colored(name,v,faces,cc))
reg(text('Report footer','Report-inspired visual reconstruction  /  no measurement values',(-1.39,-.04,.075),.025,dim))
for ob in report:ob.parent=screenroot
body=mat('Laptop graphite',(.035,.046,.060),True,.65,.28);black=mat('Screen bezel',(.009,.012,.018),True,.22,.32);keymat=mat('Keyboard',(.018,.023,.029),True,.1,.4);keyink=mat('Keyboard markings',(.17,.21,.25))
bezel=cube('Thin screen bezel',(0,0,.84),(3.14,.075,1.84),black,.025);bezel.parent=screenroot;bezel.location=(0,.025,.84)
# Screen content is forward of the bezel front (-.0125) to stay unobscured.
base=cube('Laptop base',(0,-.64,.19),(3.16,1.7,.12),body,.045)
for row in range(5):
    for col in range(14):
        ob=cube('Keyboard key',(-1.29+col*.195,-.02-row*.15,.263),(.17,.115,.018),keymat,.009)
        if row<4:curve('Key glint',[(ob.location.x-.025,ob.location.y-.02,.274),(ob.location.x+.025,ob.location.y-.02,.274)],keyink,.002)
cube('Spacebar',(0,-.79,.263),(1.10,.11,.018),keymat,.009)
cube('Trackpad',(0,-1.12,.253),(.80,.32,.008),body,.016)
hinge=cube('Hinge',(0,.13,.25),(2.78,.10,.10),body,.025)
desk=mat('Desk',(.10,.14,.18),True,0,.6);cube('Desk',(0,0,.04),(20,20,.08),desk)
back=mat('Office background',(.07,.11,.15));plane('Office wall',-20,20,-5,15,3,back)
light('Laptop soft window',(-2,-2,5),(0,0,1),500,4,(.82,.91,1));light('Laptop side fill',(4,1,3),(0,0,1),400,3,(.55,.72,1))
cam=camera((.80,-4.05,2.42),(0,.12,1.09),46,-2)
cam.data.dof.use_dof=False
C=s
# Keep conceptual camera transforms and source checks; no animation authored.
for ss in (A,Bscene,C):
    ss['data']='//../Data/story_field.npz';ss['status']='Still composition review only';ss.frame_start=1;ss.frame_end=1
bpy.context.window.scene=A
bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=str(B/'Scenes/S06_ABC_study_v004.blend'))
records={'scenes':{},'source_native':str(src.relative_to(PROD)),'source_mesh_local_coordinates_sha256':source_mesh_hash,'housing_vertices':len(housing.data.vertices),'hardware_root_scale':list(root.scale),'shared_data_sha256':hashlib.sha256((B/'Data/story_field.npz').read_bytes()).hexdigest(),'radius_min':float(raw.min()),'source_tool_max_radius':.152400137/1,'animation_built':False}
selected=sys.argv[sys.argv.index('--shots')+1] if '--shots' in sys.argv else 'ABC'
for letter,ss in zip('ABC',(A,Bscene,C)):
    if letter not in selected:continue
    bpy.context.window.scene=ss;ss.render.filepath=str(B/f'Previews/S06_{letter}_v004.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);sec=time.perf_counter()-t
    records['scenes'][letter]={'render_seconds':sec,'under_five_seconds':sec<5,'camera_location':list(ss.camera.location),'camera_quaternion':list(ss.camera.rotation_quaternion),'lens':ss.camera.data.lens,'resolution':[1280,720]}
(B/'Records/ABC-build.json').write_text(json.dumps(records,indent=2),encoding='utf-8');print('ABC STILL STUDY READY',json.dumps(records['scenes']))
