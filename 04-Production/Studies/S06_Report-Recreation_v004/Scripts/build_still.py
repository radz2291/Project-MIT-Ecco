"""One editable working still. No source-image nodes, no animation/integration."""
import bpy,math,json,time
import numpy as np
from pathlib import Path
from mathutils import Vector
B=Path(__file__).resolve().parents[1];d=np.load(B/'Data/visual_structure.npz')
bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene
s.name='S06 v004 | Report recreation | STILL REVIEW'
s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=24
s.render.resolution_x=1600;s.render.resolution_y=900;s.render.resolution_percentage=100
s.render.image_settings.file_format='PNG';s.view_settings.view_transform='Standard'
s.world=bpy.data.worlds.new('Quiet studio');s.world.use_nodes=True
s.world.node_tree.nodes['Background'].inputs[0].default_value=(.11,.15,.19,1)
s.world.node_tree.nodes['Background'].inputs[1].default_value=.25
def mat(name,color,lit=False):
    m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True;n=m.node_tree.nodes;n.clear();out=n.new('ShaderNodeOutputMaterial')
    nd=n.new('ShaderNodeBsdfPrincipled' if lit else 'ShaderNodeEmission')
    if lit:
        nd.inputs['Base Color'].default_value=(*color,1);nd.inputs['Roughness'].default_value=.38;nd.inputs['Metallic'].default_value=.15
    else:nd.inputs[0].default_value=(*color,1)
    m.node_tree.links.new(nd.outputs[0],out.inputs[0]);return m
paper=mat('Pearl paper',(.78,.82,.84));navy=mat('Deep blue stage',(.007,.018,.029));ink=mat('Editorial ink',(.028,.065,.088));muted=mat('Secondary ink',(.18,.27,.32));grid=mat('Fine grid',(.58,.67,.70));white=mat('Soft white',(.77,.87,.92));blue=mat('Profile blue',(.03,.27,.46));rim=mat('Section line',(.20,.53,.69));pale=mat('Track paper',(.88,.91,.92))
def mesh(name,verts,faces,ma):
    me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();ob=bpy.data.objects.new(name,me);s.collection.objects.link(ob);me.materials.append(ma);return ob
def plane(name,x0,x1,z0,z1,y,ma):return mesh(name,[(x0,y,z0),(x1,y,z0),(x1,y,z1),(x0,y,z1)],[(0,1,2,3)],ma)
def line(name,pts,ma=grid,width=.006):
    cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=width;cu.bevel_resolution=1;sp=cu.splines.new('POLY');sp.points.add(len(pts)-1)
    for p,co in zip(sp.points,pts):p.co=(*co,1)
    cu.materials.append(ma);ob=bpy.data.objects.new(name,cu);s.collection.objects.link(ob);return ob
fontpath=Path('C:/Windows/Fonts/segoeui.ttf');font=bpy.data.fonts.load(str(fontpath))
def text(name,body,x,z,size=.18,ma=ink,y=-.12):
    cu=bpy.data.curves.new(name,'FONT');cu.body=body;cu.font=font;cu.size=size;cu.materials.append(ma)
    ob=bpy.data.objects.new(name,cu);s.collection.objects.link(ob);ob.location=(x,y,z);ob.rotation_euler=(math.pi/2,0,0);return ob
plane('Backdrop',-20,20,-15,15,2,navy)
plane('Editorial paper',-7.52,7.52,-4.02,4.02,.6,paper)
text('Title','Borehole interpretation',-7.0,3.24,.38)
text('Subtitle','From reconstructed form to engineering insight',-6.98,2.88,.155,muted)
text('Status','REPORT-INSPIRED RECONSTRUCTION',3.55,3.45,.126,muted)
text('Status detail','Illustrative visual study',5.20,3.13,.155,muted)
line('Header rule',[(-7,.2,2.64),(7,.2,2.64)],grid,.005)
# The 3D form remains a graphic sculpture rather than steel or a physical borehole model.
plane('Sculpture stage',-7.0,-2.55,-3.02,2.39,.40,navy)
text('Sculpture heading','Reconstructed form',-6.72,2.03,.21,white,y=-1.6)
text('Sculpture footer','REPORT SHAPE  /  RECREATED IN 3D',-6.71,-2.76,.105,white,y=-1.6)
tracks=[(-2.13,-.94,'Profile'),(-.52,1.22,'Sections'),(1.65,4.20,'360° geometry'),(4.61,7.00,'Amplitude')]
for x0,x1,title in tracks:
    plane('Ground '+title,x0,x1,-3.02,1.94,.20,pale)
    text('Heading '+title,title,x0,2.14,.20)
    line('Baseline '+title,[(x0,.1,-3.03),(x1,.1,-3.03)],grid,.004)
for dep in np.linspace(-3.0,1.94,12):
    for x0,x1,title in tracks:
        if title in ('Profile','Sections'):line('Registration '+title,[(x0,.09,dep),(x1,.09,dep)],grid,.0025)
for x in np.linspace(-2.13,-.94,5):line('Profile grid',[(x,.09,-3),(x,.09,1.94)],grid,.0025)
p=d['profile_visual'];line('Recreated profile',[(float(-1.96+.66*v),-.03,float(1.94-4.96*i/(len(p)-1))) for i,v in enumerate(p)],blue,.009)
# Two actual graphic outlines are rebuilt as editable polar curves with fine reference rings.
for j,zc in enumerate((.70,-1.82)):
    for rad in np.linspace(.13,.75,6):
        line('Polar guide',[(.35+rad*math.cos(a),.06,zc+rad*math.sin(a)) for a in np.linspace(0,math.tau,181)],grid,.003)
    for a in np.linspace(0,math.tau,8,endpoint=False):
        line('Polar spoke',[(.35,.06,zc),(.35+.75*math.cos(a),.06,zc+.75*math.sin(a))],grid,.0025)
    rr=d['sections_visual'][j]
    line('Recreated circular section',[(.35+.48*float(r)*math.cos(a),-.045,zc-.48*float(r)*math.sin(a)) for a,r in zip(np.linspace(-math.pi,math.pi,len(rr)),rr)],blue,.012)
def colored_mesh(name,verts,faces,colors,lit=False):
    ma=mat(name+' palette',(1,1,1),lit);ob=mesh(name,verts,faces,ma)
    co=ob.data.color_attributes.new(name='Recreated visual colors',type='FLOAT_COLOR',domain='POINT');co.data.foreach_set('color',np.c_[colors,np.ones(len(colors))].astype('f').ravel())
    n=ma.node_tree.nodes;vc=n.new('ShaderNodeVertexColor');vc.layer_name=co.name
    target=n.get('Principled BSDF') if lit else n.get('Emission')
    ma.node_tree.links.new(vc.outputs['Color'],target.inputs['Base Color'] if lit else target.inputs[0])
    ob['status']='Recreated graphic structure; no calibration or field measurement claim'
    return ob
def palette(a,cols):return np.stack([np.interp(a.ravel(),np.linspace(0,1,len(cols)),np.array(cols)[:,i]) for i in range(3)],1)
geo=d['geometry_visual'];amp=d['amplitude_visual'];nz,na=geo.shape
geo_cols=palette((geo+1)/2,[(.57,.22,.08),(.91,.66,.43),(.88,.92,.93),(.38,.66,.78),(.055,.29,.49)])
amp_cols=palette(amp,[(.16,.072,.022),(.39,.18,.048),(.64,.36,.11),(.84,.60,.29),(.94,.83,.57)])
faces=[(j*na+i,j*na+i+1,(j+1)*na+i+1,(j+1)*na+i) for j in range(nz-1) for i in range(na-1)]
for name,x0,x1,colors in [('Recreated geometry field',1.65,4.20,geo_cols),('Recreated amplitude field',4.61,7.00,amp_cols)]:
    verts=[(x0+(x1-x0)*i/(na-1),0,1.94-4.96*j/(nz-1)) for j in range(nz) for i in range(na)]
    colored_mesh(name,verts,faces,colors)
# No source images are assigned: all report regions are new meshes/curves.
# Axisymmetric reconstruction of the visible silhouette, no unseen angular shape invented.
nr=160;radius=d['silhouette_radius'];height=4.52;verts=[];colors=[]
gc=geo_cols.reshape(nz,na,3).mean(1)
for j,r in enumerate(radius):
    for a in np.linspace(0,math.tau,nr,endpoint=False):
        verts.append((.68*r*math.cos(a),.68*r*math.sin(a),height/2-height*j/(nz-1)))
        colors.append(gc[j]*.67+np.array([.31,.49,.61])*.33)
fs=[(j*nr+i,j*nr+(i+1)%nr,(j+1)*nr+(i+1)%nr,(j+1)*nr+i) for j in range(nz-1) for i in range(nr)]
hero=colored_mesh('Hero | silhouette reconstruction',verts,fs,np.array(colors),True)
for poly in hero.data.polygons:poly.use_smooth=True
hero.location=(-4.79,-.58,-.24);hero.rotation_euler=(math.radians(15),math.radians(-9),0)
# Fine open edge and selected surface contours emphasize dimensionality without increasing relief.
for j in [0,35,72,135,181,206,229,254,283,317,351,383]:
    pts=[(.6808*float(radius[j])*math.cos(a),.6808*float(radius[j])*math.sin(a),height/2-height*j/(nz-1)) for a in np.linspace(0,math.tau,201)]
    ob=line('Sculpted section contour',pts,rim,.0025 if j else .005);ob.parent=hero
# A short inner return makes the opening legible. It is presentation geometry, not casing thickness.
inner=mat('Interior shade',(.035,.10,.15),True)
top=[]
for z in (height/2,height/2-.13):
    top.extend([(.673*float(radius[0])*math.cos(a),.673*float(radius[0])*math.sin(a),z) for a in np.linspace(0,math.tau,nr,endpoint=False)])
ob=mesh('Sculpture inner lip',top,[(i,(i+1)%nr,(i+1)%nr+nr,i+nr) for i in range(nr)],inner);ob.parent=hero
text('Footer left','Recreated from report graphics. Visual structure only; no measurement values.',-6.98,-3.60,.145,muted)
text('Footer right','ILLUSTRATIVE',5.89,-3.60,.13,muted)
def area(name,loc,target,power,size,color):
    ld=bpy.data.lights.new(name,'AREA');ld.energy=power;ld.shape='DISK';ld.size=size;ld.color=color
    ob=bpy.data.objects.new(name,ld);s.collection.objects.link(ob);ob.location=loc;ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler()
area('Broad upper key',(-6,-5,6),hero.location,620,5,(.78,.89,1))
area('Side rim',(-2,1,2),hero.location,470,3,(.29,.66,1))
area('Warm soft fill',(-7,-3,-2),hero.location,160,4,(1,.85,.67))
cd=bpy.data.cameras.new('Editorial still');cam=bpy.data.objects.new('Editorial still',cd);s.collection.objects.link(cam)
cam.location=(0,-24,0);cam.rotation_euler=(math.pi/2,0,0);cd.type='ORTHO';cd.ortho_scale=16;s.camera=cam
s['scope']='One working v004 still; revise this same version through feedback. No animation or integration.'
s['provenance']='Graphic reconstruction based on anonymous report references. Not recovered measurements; different from v002 illustrative source.'
bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all()
path=B/'Scenes/S06_report-recreation_v004.blend';bpy.ops.wm.save_as_mainfile(filepath=str(path))
start=time.perf_counter();s.render.filepath=str(B/'Previews/S06_report-recreation_v004.png');bpy.ops.render.render(write_still=True);elapsed=time.perf_counter()-start
(B/'Records/still-verification.json').write_text(json.dumps({'render_seconds':elapsed,'under_five_seconds':elapsed<5,'resolution':[1600,900],'samples':24,'source_image_nodes':sum(n.type=='TEX_IMAGE' for m in bpy.data.materials if m.use_nodes for n in m.node_tree.nodes),'images':[im.name for im in bpy.data.images],'text':[o.data.body for o in s.objects if o.type=='FONT'],'objects':len(s.objects),'animation_created':False},indent=2),encoding='utf-8')
print('STILL READY',elapsed)
