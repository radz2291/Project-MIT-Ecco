"""B202-S reusable still-development master. No motion/keyframes/handlers.
Run in isolated background Blender. All user/shared originals remain untouched.
"""
import bpy, math, json, hashlib, time
from pathlib import Path
from mathutils import Vector, Matrix
ROOT=Path(__file__).resolve().parents[4];BASE=ROOT/'04-Production/Mechanisms/B202';E=ROOT/'04-Production/Records/Tasks/T-008/Evidence'
T5=ROOT/'04-Production/Shared/Assets/ECCO/ECCO_master_temporary-plugs_v002.blend'
T6=ROOT/'04-Production/Shared/Assets/WellAssembly/WellAssembly_variants_v003.blend'
OUT=BASE/'Scenes/B202_measured-envelope_master_v007.blend'
assert not OUT.exists(),'Refuse overwrite: version edited assets'
hashfile=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sources={p.relative_to(ROOT).as_posix():hashfile(p) for p in (T5,T6)}
bpy.ops.wm.open_mainfile(filepath=str(T6));s=bpy.context.scene
rig=bpy.data.objects['ASSEMBLY_CONTROL'];rig['cutaway']=0
profiles={}; source_faces=None
for mode,name in [(1,'irregular'),(2,'spiral')]:
    rig['variant']=mode;rig.update_tag();bpy.context.view_layer.update()
    ev=bpy.data.objects[name.upper()+'_FULL'].evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh()
    profiles[name]=[tuple(v.co) for v in me.vertices]
    if source_faces is None:source_faces=[tuple(p.vertices) for p in me.polygons]
    ev.to_mesh_clear()
product=bpy.data.collections['ECCO_MASTER_v002']
for c in list(s.collection.children):s.collection.children.unlink(c)
master=bpy.data.collections.new('B202_MEASURED_ENVELOPE_v007');s.collection.children.link(master)
def coll(name):
    c=bpy.data.collections.new(name);master.children.link(c);return c
controls=coll('B202_CONTROLS');toolcol=coll('B202_REPLACEABLE_HARDWARE');layers=coll('B202_INFORMATION');envcol=coll('B202_PHYSICAL_WALL');review=coll('B202_REVIEW_CAMERAS_LIGHTS')
def empty(name,c,parent=None):
    o=bpy.data.objects.new(name,None);c.objects.link(o);o.parent=parent;return o
ctrl=empty('B202_CONTROL',controls)
props={'travel_m':2.,'rotation_rad':0.,'profile':0,'show_tool':1,'show_wall':0,'show_envelope':1,'show_sections':1,'show_samples':0,'show_nominal':1,'show_amplitude':0,'depth_reveal_m':4.8,'scan_fraction':1.,'geometry_opacity':.8,'amplitude_opacity':.9}
props.update(depth_start_m=1.5,show_depth_sections=1)
for k,v in props.items():ctrl[k]=v
ctrl['meaning']='0 irregular T6; 1 tight illustrative; 2 spiral T6. No calibrated data or animation.'
ctrl['coordinate_note']='Source X metres; travel+rotation controls entire hardware; wall measurements remain fixed. End/drilling sign not certified.'
for k in ['geometry_opacity','amplitude_opacity','scan_fraction']:ctrl.id_properties_ui(k).update(min=0,max=1)
ctrl.id_properties_ui('profile').update(min=0,max=2)
ctrl.id_properties_ui('depth_reveal_m').update(min=1.5,max=4.8)
def drive(owner,path,expr,props,index=None):
    f=owner.driver_add(path) if index is None else owner.driver_add(path,index);d=f.driver;d.expression=expr
    for name,p in props.items():
        v=d.variables.new();v.name=name;v.type='SINGLE_PROP';v.targets[0].id=ctrl;v.targets[0].data_path='["'+p+'"]'
def visibility(o,expr,props):
    for path in ('hide_render','hide_viewport'):drive(o,path,expr,props)
travel=empty('B202_TOOL_TRAVEL_X',controls);spin=empty('B202_TOOL_ROTATION_X',controls,travel)
drive(travel,'location','t',{'t':'travel_m'},0);drive(spin,'rotation_euler','r',{'r':'rotation_rad'},0)
linked=empty('B202_LINKED_T5_ORIGINAL',toolcol);linked.instance_type='COLLECTION';linked.instance_collection=product;linked.hide_render=True;linked.hide_viewport=True
def material(name,color,metal=0,emission=0,opacityprop=None):
    m=bpy.data.materials.new(name);m.use_nodes=True;m.diffuse_color=(*color,1);tree=m.node_tree;n=tree.nodes.get('Principled BSDF');n.inputs['Base Color'].default_value=(*color,1);n.inputs['Metallic'].default_value=metal;n.inputs['Roughness'].default_value=.5;n.inputs['Emission Color'].default_value=(*color,1);n.inputs['Emission Strength'].default_value=emission
    if opacityprop:
        mix=tree.nodes.new('ShaderNodeMixShader');tr=tree.nodes.new('ShaderNodeBsdfTransparent');tree.links.new(tr.outputs[0],mix.inputs[1]);tree.links.new(n.outputs[0],mix.inputs[2]);tree.links.new(mix.outputs[0],tree.nodes.get('Material Output').inputs[0]);drive(mix.inputs[0],'default_value','a',{'a':opacityprop});m.surface_render_method='DITHERED'
    return m
steel=material('B202 Hardware presentation / no metallurgy claim',(.12,.15,.18),metal=.6)
rock=material('B202 Physical wall context',(.07,.055,.04))
cyan=material('B202 Circumference illustration',(.015,.45,.65),emission=.7)
white=material('B202 White nominal bit-size',(.9,.93,1),emission=.5)
geom=material('B202 Radius deviation / NOT echo amplitude',(.02,.15,.4),emission=.15,opacityprop='geometry_opacity')
amp=material('B202 Echo amplitude / NOT radius or optical rock',(.7,.4,.07),emission=.12,opacityprop='amplitude_opacity')
def rampmat(m,attr,colors):
    tree=m.node_tree;n=tree.nodes.get('Principled BSDF');a=tree.nodes.new('ShaderNodeAttribute');a.attribute_name=attr;a.label=attr+' / illustrative only';r=tree.nodes.new('ShaderNodeValToRGB');r.color_ramp.elements.remove(r.color_ramp.elements[1]);r.color_ramp.elements[0].position=colors[0][0];r.color_ramp.elements[0].color=(*colors[0][1],1)
    for pos,c in colors[1:]:r.color_ramp.elements.new(pos).color=(*c,1)
    tree.links.new(a.outputs['Fac'],r.inputs[0]);tree.links.new(r.outputs[0],n.inputs['Base Color']);tree.links.new(r.outputs[0],n.inputs['Emission Color'])
rampmat(geom,'geometry_display',[(0,(.65,.015,.008)),(.0449,(.85,.88,.93)),(.08,(.05,.5,.85)),(.5,(.015,.2,.55)),(1,(.005,.035,.14))])
rampmat(amp,'amplitude_display',[(0,(.09,.025,.006)),(.3,(.28,.095,.012)),(.65,(.7,.37,.035)),(1,(1,.8,.13))])
# Copies are in source-local coordinates, with shared move/spin parents. Source
# topology remains byte equivalent; material assignment never touches T5.
copies=[]
def source_matrix(o):
    q=o.rotation_quaternion if o.rotation_mode=='QUATERNION' else o.rotation_euler.to_quaternion()
    local=Matrix.LocRotScale(o.location,q,o.scale)
    return source_matrix(o.parent)@o.matrix_parent_inverse@local if o.parent else local
for original in product.all_objects:
    if original.type!='MESH' or 'CUTTER' in original.name:continue
    o=bpy.data.objects.new('B202_PRESENTATION_'+original.name,original.data.copy());toolcol.objects.link(o);o.parent=spin;o.matrix_basis=source_matrix(original);o.data.materials.clear();o.data.materials.append(steel);o['source_object']=original.name;copies.append(o)
    visibility(o,'1-show',{'show':'show_tool'})
radials=[]
for o in copies:
    mat=source_matrix(bpy.data.objects[o['source_object']]);radials.extend(math.hypot((mat@v.co).y,(mat@v.co).z) for v in o.data.vertices)
maxrad=max(radials)
nom=.155575;tight_depth=.0012;clearance_floor=.0015
assert nom-tight_depth>maxrad+clearance_floor,(maxrad,'Unsafe authored tight profile')
# T6 irregular/spiral are unchanged. Tight is a separate hypothetical post-cut
# restriction, not a hole our nominal gauge-sized bit is shown drilling through.
tight=[]
for x,y,z in profiles['irregular']:
    a=math.atan2(z,y);lobe=math.exp(-((x-2.73)/.4)**2)*math.exp(-((math.atan2(math.sin(a-2.5),math.cos(a-2.5)))/.65)**2)
    r=nom-tight_depth*lobe;tight.append((x,r*math.cos(a),r*math.sin(a)))
profiles['tight']=tight
config={'version':'v007','profile_order':['irregular','tight','spiral'],'nominal_radius_m':nom,'tight_max_radial_reduction_m':tight_depth,'tight_minimum_centered_clearance_floor_m':clearance_floor,'source_maximum_radial_envelope_m':maxrad,'tight_note':'Hypothetical local undersize only; no bit passage, drilling cause, dynamic/eccentric passage or operating safety claim. Straight centered full tool-envelope clearance bound.','source_hashes':sources,'data_identity':'All fields illustrative, not acquired field data. T6 authored profiles retained. Amplitude is independent of radius.'}
(BASE/'config_v007.json').write_text(json.dumps(config,indent=2))
def mesh(name,c,vs,fs,mat):
    d=bpy.data.meshes.new(name);d.from_pydata(vs,[],fs);d.update();o=bpy.data.objects.new(name,d);c.objects.link(o);d.materials.append(mat)
    for p in d.polygons:p.use_smooth=True
    return o
def crop(vs,back=False):
    ids={i for i,v in enumerate(vs) if 1.5<=v[0]<=4.8 and (not back or v[1]>=-1e-6)};fs=[f for f in source_faces if all(i in ids for i in f)];used=sorted({i for f in fs for i in f});mp={i:j for j,i in enumerate(used)}
    return [vs[i] for i in used],[tuple(mp[i] for i in f) for f in fs]
def reveal(o):
    g=bpy.data.node_groups.get('B202_Depth_Reveal')
    if not g:
        g=bpy.data.node_groups.new('B202_Depth_Reveal','GeometryNodeTree');g.interface.new_socket(name='Geometry',in_out='INPUT',socket_type='NodeSocketGeometry');g.interface.new_socket(name='Geometry',in_out='OUTPUT',socket_type='NodeSocketGeometry')
        inp=g.nodes.new('NodeGroupInput');out=g.nodes.new('NodeGroupOutput');pos=g.nodes.new('GeometryNodeInputPosition');sep=g.nodes.new('ShaderNodeSeparateXYZ');cmp=g.nodes.new('ShaderNodeMath');cmp.operation='GREATER_THAN';drive(cmp.inputs[1],'default_value','d',{'d':'depth_reveal_m'});delete=g.nodes.new('GeometryNodeDeleteGeometry');delete.domain='POINT'
        low=g.nodes.new('ShaderNodeMath');low.operation='LESS_THAN';drive(low.inputs[1],'default_value','d',{'d':'depth_start_m'});both=g.nodes.new('ShaderNodeMath');both.operation='MAXIMUM'
        for a,b in [(inp.outputs[0],delete.inputs['Geometry']),(pos.outputs[0],sep.inputs[0]),(sep.outputs['X'],cmp.inputs[0]),(sep.outputs['X'],low.inputs[0]),(cmp.outputs[0],both.inputs[0]),(low.outputs[0],both.inputs[1]),(both.outputs[0],delete.inputs['Selection']),(delete.outputs[0],out.inputs[0])]:g.links.new(a,b)
    mod=o.modifiers.new('World-registered axial reveal','NODES');mod.node_group=g
def curve(name,pts,mat,c=layers):
    d=bpy.data.curves.new(name,'CURVE');d.dimensions='3D';d.bevel_depth=.0007;d.bevel_resolution=2;sp=d.splines.new('POLY');sp.points.add(len(pts)-1)
    for p,v in zip(sp.points,pts):p.co=(*v,1)
    sp.use_cyclic_u=True;o=bpy.data.objects.new(name,d);c.objects.link(o);d.materials.append(mat);return o
table={};section_xs=[1.75,2.,2.25,2.73,3.,3.5,4.,4.5]
for mode,name in enumerate(config['profile_order']):
    vs,fs=crop(profiles[name]);table[name]={'vertices':vs,'faces':fs,'sections':{}}
    obj=mesh('B202_GEOMETRY_'+name,layers,vs,fs,geom);obj['quantity']='radius_deviation';obj['profile']=name
    delta=obj.data.attributes.new('radius_deviation_m','FLOAT','POINT');display=obj.data.attributes.new('geometry_display','FLOAT','POINT')
    for i,v in enumerate(vs):d=math.hypot(v[1],v[2])-nom;delta.data[i].value=d;display.data[i].value=(d+tight_depth)/(.0254+tight_depth)
    visibility(obj,'(p!=m) or (1-show)',{'p':'profile','m':'profile','show':'show_envelope'}) if False else None
    visibility(obj,f'(p!={mode}) or (1-show)',{'p':'profile','show':'show_envelope'});reveal(obj)
    rv,rf=crop(profiles[name],True);physical=mesh('B202_WALL_'+name,envcol,rv,rf,rock);visibility(physical,f'(p!={mode}) or (1-show)',{'p':'profile','show':'show_wall'});reveal(physical)
    rows={}
    for v in profiles[name]:rows.setdefault(round(v[0],5),[]).append(v)
    def sample(x):
        a=max(t for t in rows if t<=x);b=min(t for t in rows if t>=x);lo=sorted(rows[a],key=lambda v:math.atan2(v[2],v[1]));hi=sorted(rows[b],key=lambda v:math.atan2(v[2],v[1]));t=0 if a==b else (x-a)/(b-a)
        return [tuple((1-t)*p+t*q for p,q in zip(v,w)) for v,w in zip(lo,hi)]
    for j,x in enumerate(section_xs):
        pts=sample(x);table[name]['sections'][str(x)]=pts
        o=curve(f'B202_SECTION_{name}_{j:02d}',pts,geom);o['axial_m']=x
        da=o.data.attributes if hasattr(o.data,'attributes') else None
        # Curves retain cyan source registration; geometry surface carries color.
        o.data.materials[0]=cyan
        extra='' if x==2.73 else ' or (1-allsections)'
        visibility(o,f'(p!={mode}) or (1-show) or (d<{x}) or (lo>{x})'+extra,{'p':'profile','show':'show_sections','d':'depth_reveal_m','lo':'depth_start_m','allsections':'show_depth_sections'})
        drive(o.data,'bevel_factor_end','f',{'f':'scan_fraction'})
        if x==2.73:
            for k,v in enumerate(pts[::8]):
                bpy.ops.mesh.primitive_uv_sphere_add(segments=8,ring_count=4,radius=.0015,location=v);dot=bpy.context.object
                for c in list(dot.users_collection):c.objects.unlink(dot)
                layers.objects.link(dot);dot.name=f'B202_SAMPLE_{name}_{k:02d}';dot.data.materials.append(cyan)
                visibility(dot,f'(p!={mode}) or (1-show) or (f<{k/12}) or (d<2.73)',{'p':'profile','show':'show_samples','f':'scan_fraction','d':'depth_reveal_m'})
    # Separate independent echo-amplitude scalar at the same spatial coordinates.
    if name=='irregular':
        ampobj=mesh('B202_AMPLITUDE_independent',layers,vs,fs,amp);ampobj['quantity']='echo_amplitude_illustrative';at=ampobj.data.attributes.new('amplitude_display','FLOAT','POINT')
        for i,(x,y,z) in enumerate(vs):a=math.atan2(z,y);at.data[i].value=.5+.28*math.sin(5*a+9*x)+.16*math.sin(14*x-2*math.cos(a))
        visibility(ampobj,'1-show',{'show':'show_amplitude'});reveal(ampobj)
for j,x in enumerate([1.75,2.73,4.5]):
    o=curve('B202_NOMINAL_%02d'%j,[(x,nom*math.cos(i*math.tau/128),nom*math.sin(i*math.tau/128)) for i in range(128)],white)
    extra='' if x==2.73 else ' or (1-allsections)'
    visibility(o,f'(1-show) or (d<{x}) or (lo>{x})'+extra,{'show':'show_nominal','d':'depth_reveal_m','lo':'depth_start_m','allsections':'show_depth_sections'})
for i in range(1,4):
    original=bpy.data.objects[f'ECCO_SENSOR_REF_{i:02d}'];o=empty(f'B202_SENSOR_REF_{i:02d}',controls,spin);o.matrix_basis=source_matrix(original);o['status']='Inherited reference, not calibrated acoustic face';o.empty_display_type='ARROWS';o.empty_display_size=.02
(BASE/'sampling_tables_v007.json').write_text(json.dumps(table,separators=(',',':')))
def light(name,loc,power,size):
    d=bpy.data.lights.new(name,'AREA');d.energy=power;d.shape='DISK';d.size=size;o=bpy.data.objects.new(name,d);review.objects.link(o);o.location=loc;o.rotation_euler=(Vector((3,0,0))-o.location).to_track_quat('-Z','Y').to_euler()
light('B202 broad key',(2.2,-2,2),140,3);light('B202 edge',(4,1.2,.6),80,2);light('B202 fill',(1,-.5,.5),25,1)
d=bpy.data.cameras.new('B202_STILL_REVIEW');cam=bpy.data.objects.new(d.name,d);review.objects.link(cam);s.camera=cam;d.clip_start=.005;d.clip_end=100
s.render.engine='BLENDER_EEVEE';s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.fps=24;s.frame_start=s.frame_end=1;s.render.image_settings.file_format='PNG'
s.world=bpy.data.worlds.new('B202 neutral space');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.025,.032,.045,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.3;s.view_settings.view_transform='AgX';s.unit_settings.system='METRIC';s.unit_settings.scale_length=1
for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(BASE/'Scenes'))
s['B202_sources']=json.dumps(sources);s['B202_status']='D1 concept accepted; v007 still package for Radzi Review. No animation/final approval.';s['B202_config']=json.dumps(config)
presets={
 'A':dict(profile=0,show_tool=1,show_wall=1,show_envelope=0,show_sections=1,show_samples=1,show_nominal=0,show_amplitude=0,depth_reveal_m=2.8),
 'B':dict(profile=0,show_tool=0,show_wall=0,show_envelope=1,show_sections=1,show_samples=0,show_nominal=1,show_amplitude=0,depth_reveal_m=4.8),
 'C':dict(profile=0,show_tool=1,show_wall=0,show_envelope=1,show_sections=0,show_samples=0,show_nominal=1,show_amplitude=0,depth_reveal_m=2.8),
 'D':dict(profile=1,show_tool=1,show_wall=0,show_envelope=1,show_sections=0,show_samples=0,show_nominal=1,show_amplitude=0,depth_reveal_m=2.8),
 'E':dict(profile=2,show_tool=0,show_wall=0,show_envelope=1,show_sections=0,show_samples=0,show_nominal=1,show_amplitude=0,depth_reveal_m=4.8),
 'F':dict(profile=0,show_tool=0,show_wall=0,show_envelope=0,show_sections=0,show_samples=0,show_nominal=0,show_amplitude=1,depth_reveal_m=4.8)}
for key,state in presets.items():state.update(depth_start_m=2.65 if key in 'CD' else 1.5,show_depth_sections=1 if key in 'BE' else 0)
(BASE/'presets_v007.json').write_text(json.dumps(presets,indent=2))
record={'source_hashes':sources,'config':config,'master':OUT.relative_to(ROOT).as_posix(),'candidates':[]}
for key,state in presets.items():
    for k,v in state.items():ctrl[k]=v
    ctrl['scan_fraction']=1.;ctrl.update_tag();bpy.context.view_layer.update()
    close=key in 'ACD';loc=(.3,-.55,.4) if close else (.2,-4.5,2.5);target=(2.73,0,0) if close else (3.1,0,0)
    cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();d.lens=85 if close else 60
    s['B202_state']=key;s.render.filepath=str(BASE/f'Previews/Stills_v007/B202_{key}_v007.png')
    if key=='B':bpy.ops.wm.save_as_mainfile(filepath=str(OUT),relative_remap=False)
    p=BASE/f'Scenes/B202_{key}_v007.blend';bpy.ops.wm.save_as_mainfile(filepath=str(p),relative_remap=False);t=time.time();bpy.ops.render.render(write_still=True)
    record['candidates'].append({'key':key,'state':state,'scene':p.relative_to(ROOT).as_posix(),'still':Path(s.render.filepath).relative_to(ROOT).as_posix(),'render_seconds':time.time()-t})
    (E/'build_v007.json').write_text(json.dumps(record,indent=2))
print('B202_V006_BUILD_PASS')
