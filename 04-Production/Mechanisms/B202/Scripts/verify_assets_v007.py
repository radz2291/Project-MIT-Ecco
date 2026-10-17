import bpy,json,math,hashlib,struct,sys
from pathlib import Path
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[4];BASE=ROOT/'04-Production/Mechanisms/B202';E=ROOT/'04-Production/Records/Tasks/T-008/Evidence'
sys.path.insert(0,str(BASE/'Scripts'))
from sample_profile_v007 import load_tables,sample_wall
config=json.loads((BASE/'config_v007.json').read_text());presets=json.loads((BASE/'presets_v007.json').read_text());table=load_tables();checks=[];outputs=[];metrics={}
def check(name,result):checks.append({'check':name,'pass':bool(result)})
def sig(mesh):
    h=hashlib.sha256()
    for v in mesh.vertices:h.update(struct.pack('<3f',*v.co))
    for p in mesh.polygons:h.update(struct.pack('<I',len(p.vertices)));h.update(struct.pack('<'+'I'*len(p.vertices),*p.vertices))
    return h.hexdigest()
def source_matrix(o):
    q=o.rotation_quaternion if o.rotation_mode=='QUATERNION' else o.rotation_euler.to_quaternion();m=Matrix.LocRotScale(o.location,q,o.scale)
    return source_matrix(o.parent)@o.matrix_parent_inverse@m if o.parent else m
def update(c):c.update_tag();bpy.context.view_layer.update()
def evaluated(o):
    ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();v=[tuple(x.co) for x in me.vertices];ev.to_mesh_clear();return v
for key in 'ABCDEF':
    path=BASE/f'Scenes/B202_{key}_v007.blend';bpy.ops.wm.open_mainfile(filepath=str(path));s=bpy.context.scene;c=bpy.data.objects['B202_CONTROL'];update(c)
    check(key+' preset state',all(abs(c[k]-v)<1e-6 for k,v in presets[key].items()))
    check(key+' still-only scene',s.frame_start==s.frame_end==1 and not any(o.animation_data and o.animation_data.action for o in s.objects))
    check(key+' relative source libraries',len(bpy.data.libraries)>0 and all(l.filepath.startswith('//') and Path(bpy.path.abspath(l.filepath)).exists() for l in bpy.data.libraries))
    copies=[o for o in s.objects if o.name.startswith('B202_PRESENTATION_')];check(key+' housing + nine closures',len(copies)==10)
    for o in copies:
        source=bpy.data.objects[o['source_object']];check(key+' source mesh '+source.name,sig(o.data)==sig(source.data));mat=source_matrix(source)
        check(key+' source transform '+source.name,max(abs(o.matrix_basis[i][j]-mat[i][j]) for i in range(4) for j in range(4))<1e-5)
    # No surface deformation from visualization: local positions match source tables.
    for name in config['profile_order']:
        obj=bpy.data.objects['B202_GEOMETRY_'+name]
        check(key+' registered '+name,len(obj.data.vertices)==len(table[name]['vertices']) and max((Vector(v.co)-Vector(p)).length for v,p in zip(obj.data.vertices,table[name]['vertices']))<1e-6)
    im=BASE/f'Previews/Stills_v007/B202_{key}_v007.png';loaded=bpy.data.images.load(str(im));check(key+' image 1280x720',tuple(loaded.size)==(1280,720))
    check(key+' image nonblank',max(loaded.pixels[:])-min(loaded.pixels[:])>.2)
    check(key+' saved render points to exact image',Path(s.render.filepath)==im)
    check(key+' amplitude visibility independent',bpy.data.objects['B202_AMPLITUDE_independent'].hide_render==(key!='F'))
    for p in (path,im):outputs.append({'path':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size})
# Exercise controls on freshly reopened reusable master, without saving changes.
path=BASE/'Scenes/B202_measured-envelope_master_v007.blend';bpy.ops.wm.open_mainfile(filepath=str(path));s=bpy.context.scene;c=bpy.data.objects['B202_CONTROL'];update(c)
tool=[o for o in s.objects if o.name.startswith('B202_PRESENTATION_')];wall=bpy.data.objects['B202_GEOMETRY_irregular'];before=[v.co.copy() for v in wall.data.vertices];base=[o.matrix_world.copy() for o in tool]
c['show_tool']=1;update(c)
c['travel_m']=2.13;c['rotation_rad']=.7;update(c)
expected=Matrix.Translation((2.13,0,0))@Matrix.Rotation(.7,4,'X')
for o in tool:
    check('whole hardware move/spin '+o.name,max(abs(o.matrix_world[i][j]-(expected@o.matrix_basis)[i][j]) for i in range(4) for j in range(4))<2e-6)
check('measurements fixed while hardware moves',all((a-v.co).length<1e-10 for a,v in zip(before,wall.data.vertices)))
refs=[bpy.data.objects[f'B202_SENSOR_REF_{i:02d}'].matrix_world.translation for i in range(1,4)];angles=sorted(math.atan2(p.z,p.y) for p in refs)
check('sensor plane follows tool',all(abs(p.x-2.86)<1e-5 for p in refs));check('120deg source references',all(abs((angles[(i+1)%3]-angles[i])%math.tau-math.tau/3)<1e-5 for i in range(3)))
c['travel_m']=2.;c['rotation_rad']=0.;c['depth_start_m']=2.;c['depth_reveal_m']=3.;c['show_envelope']=1;c['profile']=0;update(c)
pts=evaluated(wall);check('depth reveal trims both ends',len(pts)>0 and all(1.99999<=v[0]<=3.00001 for v in pts))
c['depth_reveal_m']=4.8;c['depth_start_m']=1.5;update(c);check('depth full reveal restores surface',len(evaluated(wall))==len(wall.data.vertices))
for mode,name in enumerate(config['profile_order']):
    c['profile']=mode;update(c);check('profile visibility '+name,all(bpy.data.objects['B202_GEOMETRY_'+n].hide_render==(n!=name) for n in config['profile_order']))
c['show_sections']=1;c['show_depth_sections']=1;c['profile']=0;c['scan_fraction']=.4;update(c)
ring=bpy.data.objects['B202_SECTION_irregular_03'];check('azimuth reveal driver',abs(ring.data.bevel_factor_end-.4)<1e-6)
partial=evaluated(ring);c['scan_fraction']=1.;update(c);full=evaluated(ring);check('azimuth reveal changes actual curve geometry',partial!=full)
c['geometry_opacity']=.3;c['amplitude_opacity']=.6;update(c)
for name,value in [('B202 Radius deviation / NOT echo amplitude',.3),('B202 Echo amplitude / NOT radius or optical rock',.6)]:
    node=next(n for n in bpy.data.materials[name].node_tree.nodes if n.type=='MIX_SHADER');check('opacity control '+name,abs(node.inputs[0].default_value-value)<1e-6)
amp=bpy.data.objects['B202_AMPLITUDE_independent'];check('separate quantity attributes','amplitude_display' in amp.data.attributes and 'radius_deviation_m' not in amp.data.attributes)
errors=[]
for v,a in zip(amp.data.vertices,amp.data.attributes['amplitude_display'].data):
    x,y,z=v.co;theta=math.atan2(z,y);expected=.5+.28*math.sin(5*theta+9*x)+.16*math.sin(14*x-2*math.cos(theta));errors.append(abs(a.value-expected))
check('amplitude derived only from independent illustrative angular/depth field',max(errors)<1e-6)
for mat,attr in [('B202 Radius deviation / NOT echo amplitude','geometry_display'),('B202 Echo amplitude / NOT radius or optical rock','amplitude_display')]:
    attrs=[n.attribute_name for n in bpy.data.materials[mat].node_tree.nodes if n.type=='ATTRIBUTE'];check('distinct material field '+attr,attrs==[attr])
tight=bpy.data.objects['B202_GEOMETRY_tight'];minr=min(math.hypot(v.co.y,v.co.z) for v in tight.data.vertices);lower=config['nominal_radius_m']-config['tight_max_radial_reduction_m'];bound=lower-config['source_maximum_radial_envelope_m']
metrics.update(tight_sampled_min_radius_m=minr,tight_analytic_min_radius_m=lower,conservative_centered_radial_clearance_m=bound)
check('tight undersize exists',minr<config['nominal_radius_m']-.001)
check('tight full-envelope analytic clearance floor',bound>config['tight_minimum_centered_clearance_floor_m'])
check('tight samples obey analytic lower bound',minr>=lower-1e-7)
check('red and blue field signs',min(x.value for x in tight.data.attributes['radius_deviation_m'].data)<-.001 and max(x.value for x in wall.data.attributes['radius_deviation_m'].data)>.02)
# Seam continuity and exact-node lookup for the pure-Python handover helper.
for name in config['profile_order']:
    p=table[name]['vertices'][123];a=math.atan2(p[2],p[1]);q=sample_wall(table,name,p[0],a)
    check('table exact sample '+name,(Vector(q)-Vector(p)).length<1e-6)
    a=sample_wall(table,name,2.73,-1e-7);b=sample_wall(table,name,2.73,math.tau-1e-7);check('azimuth seam '+name,(Vector(a)-Vector(b)).length<1e-8)
    for angle in [i*math.tau/108 for i in range(108)]:
        p=sample_wall(table,name,2.73,angle)
        if name=='tight':check('tight polygon-interpolated clearance '+str(angle),math.hypot(p[1],p[2])-config['source_maximum_radial_envelope_m']>.0015)
for p,h in config['source_hashes'].items():check('source unchanged '+p,hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h)
outputs.append({'path':path.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size})
result={'passed':sum(c['pass'] for c in checks),'total':len(checks),'checks':checks,'metrics':metrics,'outputs':outputs,'limits':'Self-checks of illustrative assets only. Conservative centered radial fit is not dynamic/eccentric/loaded safety, bit passage, acoustic calibration, motion QA or MIT certification.'}
(E/'verification_v007.json').write_text(json.dumps(result,indent=2));print(json.dumps({'passed':result['passed'],'total':result['total'],'failures':[c for c in checks if not c['pass']],'metrics':metrics}));assert all(c['pass'] for c in checks)
