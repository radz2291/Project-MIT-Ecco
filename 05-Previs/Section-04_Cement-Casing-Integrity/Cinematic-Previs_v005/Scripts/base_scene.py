"""Authorized S04 Stage 6 excerpt: exact linked geometry, local visibility shaders."""
import bpy,math,json,sys,time,hashlib,struct
from pathlib import Path
from mathutils import Vector
ROOT=Path(r'C:\Users\RZ1\Desktop\RZ\261013-MIT-Ecco')
BASE=ROOT/'05-Previs/Section-04_Cement-Casing-Integrity/v002'
A=ROOT/'04-Production/Shared/Assets'
SCENE=BASE/'Scenes/S04_transition-test_v002.blend'
RI=.1589405; RO=.1698625
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(n,v): (BASE/'Records'/n).write_text(json.dumps(v,indent=2),encoding='utf8')
def smooth(v):
    v=max(0.,min(1.,v)); return v*v*v*(10+v*(-15+6*v))
def material(name,color,metal=0.,rough=.5):
    m=bpy.data.materials.new(name);m.use_nodes=True
    bs=m.node_tree.nodes.get('Principled BSDF')
    bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Metallic'].default_value=metal;bs.inputs['Roughness'].default_value=rough
    return m,bs
def op(nodes,links,operation,a,b=None):
    n=nodes.new('ShaderNodeMath');n.operation=operation
    for v,i in [(a,0),(b,1)]:
        if v is None:continue
        if isinstance(v,(int,float)):n.inputs[i].default_value=v
        else:links.new(v,n.inputs[i])
    return n.outputs[0]
def ramp(nodes,links,socket,lo,hi):
    n=nodes.new('ShaderNodeMapRange');n.clamp=True;n.interpolation_type='SMOOTHSTEP'
    links.new(socket,n.inputs['Value']);n.inputs['From Min'].default_value=lo;n.inputs['From Max'].default_value=hi
    return n.outputs['Result']
def window_material(m,low,high,animated=False):
    ns=m.node_tree.nodes;lk=m.node_tree.links
    geo=ns.new('ShaderNodeNewGeometry');xyz=ns.new('ShaderNodeSeparateXYZ');lk.new(geo.outputs['Position'],xyz.inputs[0])
    angle=op(ns,lk,'ARCTAN2',xyz.outputs['Z'],xyz.outputs['Y'])
    axial=op(ns,lk,'MULTIPLY',ramp(ns,lk,xyz.outputs['X'],-2.85,-2.64),op(ns,lk,'SUBTRACT',1,ramp(ns,lk,xyz.outputs['X'],-.29,-.12)))
    angular=op(ns,lk,'MULTIPLY',ramp(ns,lk,angle,low-.035,low+.035),op(ns,lk,'SUBTRACT',1,ramp(ns,lk,angle,high-.035,high+.035)))
    strength=ns.new('ShaderNodeValue');strength.name='Inspection window only';strength.outputs[0].default_value=1
    mask=op(ns,lk,'MULTIPLY',op(ns,lk,'MULTIPLY',axial,angular),strength.outputs[0])
    out=next(n for n in ns if n.type=='OUTPUT_MATERIAL');surf=out.inputs['Surface'].links[0].from_socket
    trans=ns.new('ShaderNodeBsdfTransparent');mix=ns.new('ShaderNodeMixShader');lk.new(mask,mix.inputs[0]);lk.new(surf,mix.inputs[1]);lk.new(trans.outputs[0],mix.inputs[2]);lk.new(mix.outputs[0],out.inputs['Surface'])
    m.surface_render_method='DITHERED';m['operation']='Consumer-only illustrative visibility; source mesh coordinates unchanged'
    if animated:
        for f in range(1,145):
            t=(f-1)/24;strength.outputs[0].default_value=1-smooth((t-3.35)/.8);strength.outputs[0].keyframe_insert('default_value',frame=f)
    return strength
def local_shared(source,name,collection,mat=None):
    ob=bpy.data.objects.new(name,source.data);collection.objects.link(ob);ob.matrix_world=source.matrix_world.copy()
    ob['source_object']=source.name;ob['source_library']=bpy.path.abspath(source.library.filepath) if source.library else ''
    ob['geometry_policy']='Identical linked mesh datablock; no vertex edits, displacement or rescaling'
    if mat:
        for slot in ob.material_slots:slot.link='OBJECT';slot.material=mat
    return ob
def line(name,points,col,color,r=.00024):
    d=bpy.data.curves.new(name,'CURVE');d.dimensions='3D';d.bevel_depth=r;d.bevel_resolution=2
    sp=d.splines.new('POLY');sp.points.add(len(points)-1)
    for p,v in zip(sp.points,points):p.co=(*v,1)
    ob=bpy.data.objects.new(name,d);col.objects.link(ob)
    m=bpy.data.materials.new(name+' display');m.use_nodes=True;ns=m.node_tree.nodes;ns.clear();lk=m.node_tree.links
    out=ns.new('ShaderNodeOutputMaterial');em=ns.new('ShaderNodeEmission');em.inputs[0].default_value=(*color,1);em.inputs[1].default_value=.8
    tr=ns.new('ShaderNodeBsdfTransparent');mix=ns.new('ShaderNodeMixShader');val=ns.new('ShaderNodeValue');val.name='Recorded comparison visibility'
    lk.new(val.outputs[0],mix.inputs[0]);lk.new(tr.outputs[0],mix.inputs[1]);lk.new(em.outputs[0],mix.inputs[2]);lk.new(mix.outputs[0],out.inputs['Surface']);d.materials.append(m);m.surface_render_method='DITHERED'
    for f in range(1,145):
        val.outputs[0].default_value=smooth(((f-1)/24-3.35)/.95);val.outputs[0].keyframe_insert('default_value',frame=f)
    return ob
def light(name,pos,target,energy,size,color=(1,1,1)):
    d=bpy.data.lights.new(name,'AREA');d.energy=energy;d.shape='DISK';d.size=size;d.color=color;d.use_shadow=False
    o=bpy.data.objects.new(name,d);bpy.context.scene.collection.objects.link(o);o.location=pos;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();return o
def build():
    bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;s.name='S04 Stage 6 - outside channel to inner wear'
    s.unit_settings.system='METRIC';s.unit_settings.scale_length=1;s.frame_start=1;s.frame_end=144;s.render.fps=24
    s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=4;s.eevee.use_raytracing=False
    s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.image_settings.compression=15;s.render.use_compositing=False
    s.view_settings.view_transform='AgX';s.view_settings.look='AgX - Medium High Contrast';s.view_settings.exposure=-2.0;s.render.film_transparent=False
    world=bpy.data.worlds.new('Deep well explanatory illumination');world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.10,.13,.17,1);world.node_tree.nodes['Background'].inputs[1].default_value=.24;s.world=world
    sys.path[:0]=[str(A/'World/Scripts'),str(A/'CasedHole/Scripts')]
    from formation_controls_v004 import create_world
    from cased_controls_v001 import create_cased
    root,w,instances=create_world(A)
    for k,v in dict(travel_m=-2.23,rotation_rad=0.,show_hardware=1,show_open=0,show_casing=0,show_cement=0,show_formation=0,show_shoe=0,show_mud=0,cutaway=0).items():w[k]=v
    w.update_tag();bpy.context.view_layer.update()
    cc,ci=create_cased(A,'v002')
    for k,v in dict(cutaway=0,wear=1,channel=1,show_steel=0,show_cement=0,show_channel=0,show_reference=0).items():cc[k]=v
    cc.update_tag();bpy.context.view_layer.update()
    col=bpy.data.collections.new('S04 consumer visibility and comparison');s.collection.children.link(col)
    steel,bs=material('S04 satin steel - inspection mask',(.25,.31,.35),.48,.42);window_material(steel,-1.4,.23,True)
    # Dark recessed casing floor in the gap; inner steel inspection shading remains unchanged.
    ns=steel.node_tree.nodes;lk=steel.node_tree.links
    pos=ns.new('ShaderNodeNewGeometry');sep=ns.new('ShaderNodeSeparateXYZ');lk.new(pos.outputs['Position'],sep.inputs[0])
    yy=op(ns,lk,'MULTIPLY',sep.outputs['Y'],sep.outputs['Y']);zz=op(ns,lk,'MULTIPLY',sep.outputs['Z'],sep.outputs['Z'])
    radial=op(ns,lk,'SQRT',op(ns,lk,'ADD',yy,zz));outer=op(ns,lk,'GREATER_THAN',radial,RO-.0003)
    tint=ns.new('ShaderNodeMixRGB');tint.inputs[1].default_value=(.25,.31,.35,1);tint.inputs[2].default_value=(.018,.025,.030,1)
    lk.new(outer,tint.inputs[0]);lk.new(tint.outputs[0],bs.inputs['Base Color'])
    steel_ob=local_shared(bpy.data.objects['CASED_STEEL_WEAR_FULL'],'Steel - unchanged source with viewing window',col,steel)
    cement,bs=material('S04 matte cement',(.46,.33,.17),0,.87)
    ns=cement.node_tree.nodes;lk=cement.node_tree.links;tex=ns.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=170;tex.inputs['Detail'].default_value=2;geo=ns.new('ShaderNodeNewGeometry');lk.new(geo.outputs['Position'],tex.inputs['Vector']);mix=ns.new('ShaderNodeMixRGB');mix.inputs[1].default_value=(.25,.18,.09,1);mix.inputs[2].default_value=(.53,.40,.22,1);lk.new(tex.outputs['Fac'],mix.inputs[0]);lk.new(mix.outputs[0],bs.inputs['Base Color']);window_material(cement,-1.4,.23)
    for name in ['CASED_CEMENT_UPHOLE_FULL','CASED_CEMENT_DOWNHOLE_FULL','CASED_CEMENT_LEFT_FULL','CASED_CEMENT_RIGHT_FULL']:
        local_shared(bpy.data.objects[name],name+' local window',col,cement)
    blue,bs=material('S04 possible exterior gap - illustrative blue',(.025,.22,.36),0,.58)
    # Omit the solid placeholder: the canonical cement meshes already leave an actual open channel.
    # Two shared half-masses provide surrounding ground; only the facing half is windowed.
    with bpy.data.libraries.load(str(A/'Formation/Formation_cased-section_v002.blend'),link=True) as (a,b):b.collections=['WORLD_CASED_FORMATION_SECTION']
    ground_source=next(o for o in b.collections[0].objects if o.name=='CASED_FORMATION_MASS')
    gm=ground_source.data.materials[0].copy();gm.name='S04 ground viewing access';window_material(gm,-1.48,1.48)
    front=local_shared(ground_source,'Formation facing inspection window',col,gm)
    rear=local_shared(ground_source,'Formation retained rear ground',col);rear.rotation_euler.x=math.pi
    # The existing optical mud skin is reused with an economical, weakly tinted clear display.
    fluid,bs=material('S04 clear drilling-fluid optical cue',(.06,.10,.085),0,.24)
    ns=fluid.node_tree.nodes;lk=fluid.node_tree.links;out=ns.get('Material Output');mix=ns.new('ShaderNodeMixShader');tr=ns.new('ShaderNodeBsdfTransparent');mix.inputs[0].default_value=.025;lk.new(tr.outputs[0],mix.inputs[1]);lk.new(bs.outputs[0],mix.inputs[2]);lk.new(mix.outputs[0],out.inputs['Surface']);fluid.surface_render_method='DITHERED';window_material(fluid,-1.4,.23,True)
    for name in ['MUD_CURVED_REAR_OPTICAL_SKIN','MUD_CURVED_OPTICAL_CUT']:local_shared(bpy.data.objects[name],name+' S04 clear cue',col,fluid)
    light('Soft warm key',(-1.4,1.0,1.0),(-1.6,.08,0),95,1.1,(1,.88,.73))
    light('Cool metal reflection',(-2.1,.65,-.7),(-1.6,.12,0),45,.85,(.65,.80,1))
    light('Cement separation',(-1.9,1.15,.4),(-1.5,.20,.08),30,.5,(1,.85,.65))
    light('Inner wall grazing strip',(-1.15,.10,.065),(-1.65,.16,0),3.0,.07,(.88,.94,1))
    light('Inner wall broad inspection fill',(-1.48,.085,-.015),(-1.64,.16,0),2.0,.22,(.84,.91,1))
    d=bpy.data.cameras.new('S04 proof camera');cam=bpy.data.objects.new('S04 proof camera',d);s.collection.objects.link(cam);s.camera=cam;d.lens=38;d.clip_start=.0007;d.clip_end=70;cam.rotation_mode='QUATERNION'
    p0=Vector((-.35,1.35,.60));p1=Vector((-.68,.78,.22));p2=Vector((-1.36,.20,-.035));p3=Vector((-1.48,.104,-.030));poses=[];prev=None
    for f in range(1,145):
        t=(f-1)/24;q=smooth(t/3.9);pos=(1-q)**3*p0+3*(1-q)**2*q*p1+3*(1-q)*q*q*p2+q**3*p3;pos.x-=.025*smooth(t/6)
        a=smooth((t-1.3)/2.4);target=Vector((-1.5,.17,.085)).lerp(Vector((-1.62,.1629,0)),a)
        quat=(target-pos).to_track_quat('-Z','Y')
        target-=quat@Vector((.014*smooth((t-2.8)/1.3),0,0))
        quat=(target-pos).to_track_quat('-Z','Y');roll=__import__('mathutils').Quaternion((0,0,1),math.radians(-9));quat=quat@roll
        if prev and prev.dot(quat)<0:quat.negate()
        prev=quat.copy();cam.location=pos;cam.rotation_quaternion=quat;cam.keyframe_insert('location',frame=f);cam.keyframe_insert('rotation_quaternion',frame=f)
        poses.append({'frame':f,'section_time_s':11+t,'position_m':list(pos),'target_m':list(target),'quaternion':list(quat)})
    # Comparison uses actual linked mesh coordinates at azimuth 0, not an exaggerated proxy.
    profile=sorted((float(v.co.x),math.hypot(v.co.y,v.co.z)) for v in steel_ob.data.vertices if abs(v.co.z)<1e-6 and v.co.y>0 and math.hypot(v.co.y,v.co.z)<RO-1e-6)
    profile=[p for p in profile if -2.3<=p[0]<=-.7]
    assert profile and max(r for x,r in profile)>RI+.0038
    byangle={}
    for v in steel_ob.data.vertices:
        r=math.hypot(v.co.y,v.co.z);a=math.atan2(v.co.z,v.co.y)
        if r<RO-1e-6 and -.42<=a<=.42:byangle.setdefault(round(a,6),{})[float(v.co.x)]=r
    section=[];section_x=-1.60
    for a,rr in sorted(byangle.items()):
        lo=max(x for x in rr if x<=section_x);hi=min(x for x in rr if x>=section_x)
        r=rr[lo] if hi==lo else rr[lo]+(rr[hi]-rr[lo])*(section_x-lo)/(hi-lo);section.append((a,r))
    line('Original inner surface - reference',[(section_x,(RI-.0002)*math.cos(a),(RI-.0002)*math.sin(a)) for a,r in section],col,(.85,.89,.92),.00020)
    line('Existing inner wear - source mesh section',[(section_x,(r-.00015)*math.cos(a),(r-.00015)*math.sin(a)) for a,r in section],col,(.06,.58,.78),.00020)
    dump('comparison-section.json',{'source':'CASED_STEEL_WEAR_FULL','x_m':section_x,'angular_radius_samples':section,'method':'Linear native longitudinal-edge interpolation at fixed X; exact registered radii; no exaggeration'})
    # A quiet footer identifies the example without invented engineering values.
    m=bpy.data.materials.new('S04 footer');m.use_nodes=True;ns=m.node_tree.nodes;ns.clear();out=ns.new('ShaderNodeOutputMaterial');em=ns.new('ShaderNodeEmission');em.inputs[0].default_value=(.65,.70,.72,1);em.inputs[1].default_value=.8;m.node_tree.links.new(em.outputs[0],out.inputs[0])
    text=bpy.data.curves.new('Proof provenance','FONT');text.body='SECTION 4  |  TRANSITION TEST  |  ILLUSTRATIVE GEOMETRY';text.size=.00016;text.materials.append(m);ob=bpy.data.objects.new('Proof provenance - caption added in video encode',text);col.objects.link(ob);ob.parent=cam;ob.location=(-.0089,-.00492,-.02);ob.hide_render=True
    s['scope']='Authorized six-second S04 Stage6 transition test, local11–17s; not full18-second production';s['limitations']='Fixed inspection pose; no calibrated acoustics, full retrieval/response timing or voice sync claimed. Source meshes linked, no geometry change. Clear-fluid optical approximation and temporary viewing access.'
    s['contract']='04-Production/Shots/S04/S04-A/direction.md';s.render.fps=24;s.frame_set(1)
    # Linear sampled keys avoid hidden Bezier overshoot; the sampled analytic motion is smooth.
    for action in bpy.data.actions:
        for layer in action.layers:
            for st in layer.strips:
                for bag in st.channelbags:
                    for fc in bag.fcurves:
                        for kp in fc.keyframe_points:kp.interpolation='LINEAR'
    libs={l:bpy.path.abspath(l.filepath) for l in bpy.data.libraries}
    srcs=[{'path':str(Path(p).resolve().relative_to(ROOT)),'sha256':sha(p)} for p in sorted(set(libs.values()))]
    for l,p in libs.items():l.filepath=bpy.path.relpath(p,start=str(SCENE.parent))
    s.render.filepath=str(BASE/'Previews/S04_transition-test_v002.png');bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(SCENE),relative_remap=False)
    dump('source-manifest.json',srcs);dump('camera-score.json',poses)
    dump('build-verification.json',{'scene':str(SCENE),'scope':s['scope'],'source_mesh_identity':steel_ob.data.library is not None,'wear_vertices':len(steel_ob.data.vertices),'nominal_radius_m':RI,'outer_radius_m':RO,'maximum_source_profile_radius_m':max(r for x,r in profile),'geometry_change':False,'profile_samples':profile,'ground':'Two rigid instances of canonical cased formation half-mass; facing-window shader only','hardware_pose':'T44 linked world, travel_m=-2.23, rotation_rad=0, static inspection hold','frames':144,'fps':24,'resolution':[1280,720],'samples':4,'cost_target':'Owner requests approximately1second/frame; retain actual startup and sample measurements','source_files':srcs})
    print('S04_BUILD_SAVED',str(SCENE),flush=True)
def render(mode):
    bpy.ops.wm.open_mainfile(filepath=str(SCENE),load_ui=False,use_scripts=False);s=bpy.context.scene
    frames=[144,73,1,120] if mode=='benchmark' else list(range(1,145))
    rows=[]
    for f in frames:
        s.frame_set(f);out=BASE/('Previews' if mode=='benchmark' else 'Work')/('S04_'+('benchmark_' if mode=='benchmark' else '')+f'{f:04d}.png');s.render.filepath=str(out)
        st=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-st
        rows.append({'frame':f,'seconds':dt,'under_5':dt<5,'path':str(out)});dump('timings-'+mode+'.json',{'settings':{'engine':'EEVEE','samples':s.eevee.taa_render_samples,'resolution':[1280,720],'fps':24},'cache':'Normal existing driver caches; no hidden warmup. Process/file loading excluded; known empty-cache initialization limit remains unproven.','samples':rows})
        print('S04_FRAME',f,round(dt,3),flush=True)
        if dt>=5:raise RuntimeError('Frame exceeds strict5s cap; stop before batch')
if __name__=='__main__':
    mode=sys.argv[sys.argv.index('--')+1] if '--' in sys.argv else 'build'
    if mode=='build':build()
    else:render(mode)
