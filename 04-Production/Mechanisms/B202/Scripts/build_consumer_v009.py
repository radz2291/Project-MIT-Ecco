"""New editable consumer: display only measurement-derived grids.
Preserves v008 on disk and retains its hardware/look/controls. No keyframes.
"""
import bpy,sys,math,json,hashlib,time
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[4];BASE=ROOT/'04-Production/Mechanisms/B202';DATA=BASE/'Data/v009';E=ROOT/'04-Production/Records/Tasks/T-008/Evidence/v009';PRE=BASE/'Previews/Mechanism_v009';sys.path.insert(0,str(BASE/'Scripts'))
from acquisition_core_v009 import *
C=read_json(BASE/'acquisition_config_v009.json');INDEX=read_json(DATA/'index_v009.json');OUT=BASE/'Scenes/B202_measured-envelope_master_v009.blend';assert not OUT.exists(),'Version before overwriting consumer'
bpy.ops.wm.open_mainfile(filepath=str(BASE/'Scenes/B202_measured-envelope_master_v008.blend'));s=bpy.context.scene;c=bpy.data.objects['B202_CONTROL'];master=bpy.data.collections['B202_MEASURED_ENVELOPE_v008'];master.name='B202_MEASURED_ENVELOPE_v009'
for name in ['B202_INFORMATION','B202_PHYSICAL_WALL']:
    col=bpy.data.collections[name];col.hide_render=True;col.hide_viewport=True;col['status']='Preserved v008 visual-only layers, permanently suppressed in v009. Not acquisition outputs.'
col=bpy.data.collections.new('B202_DERIVED_DATA_v009');master.children.link(col)
case_names=list(INDEX['cases'])+['interpolation_fixture'];c['data_case']=case_names.index('irregular_layers');c.id_properties_ui('data_case').update(min=0,max=len(case_names)-1)
for key,value in {'show_reconstruction':1,'show_echo_strength':0,'show_acquired_points':0,'show_interpolated':0,'event_time_s':1000.,'eccentric_y_m':0.,'eccentric_z_m':0.}.items():c[key]=value
c['v009_case_names']=json.dumps(case_names);c['v009_scope']='Synthetic acquisition consistency. No calibrated ENP3 processing or cinematic motion. Test10 deferred T27.'
def drive(owner,path,expr,props,index=None):
    f=owner.driver_add(path) if index is None else owner.driver_add(path,index);d=f.driver;d.expression=expr
    for name,p in props.items():v=d.variables.new();v.name=name;v.type='SINGLE_PROP';v.targets[0].id=c;v.targets[0].data_path='["'+p+'"]'
def visibility(o,idx,prop):
    for p in ['hide_render','hide_viewport']:drive(o,p,f'(case!={idx}) or (1-show)',{'case':'data_case','show':prop})
travel=bpy.data.objects['B202_TOOL_TRAVEL_X'];drive(travel,'location','v',{'v':'eccentric_y_m'},1);drive(travel,'location','v',{'v':'eccentric_z_m'},2)
# Materials copy established v008 treatment, changing only named data inputs.
geom=bpy.data.materials['B202 Radius deviation / NOT echo amplitude'].copy();geom.name='B202_v009_delta_radius'
amp=bpy.data.materials['B202 Echo amplitude / NOT radius or optical rock'].copy();amp.name='B202_v009_received_echo_strength'
next(n for n in amp.node_tree.nodes if n.type=='ATTRIBUTE').attribute_name='echo_strength_display'
cyan=bpy.data.materials['B202 Circumference illustration']
def reveal_group():
    g=bpy.data.node_groups.new('B202_v009_Evidence_Reveal','GeometryNodeTree');g.interface.new_socket(name='Geometry',in_out='INPUT',socket_type='NodeSocketGeometry');g.interface.new_socket(name='Geometry',in_out='OUTPUT',socket_type='NodeSocketGeometry');inp=g.nodes.new('NodeGroupInput');out=g.nodes.new('NodeGroupOutput');delete=g.nodes.new('GeometryNodeDeleteGeometry');delete.domain='POINT'
    at=g.nodes.new('GeometryNodeInputNamedAttribute');at.data_type='FLOAT';at.inputs['Name'].default_value='ready_timestamp_s';cmp=g.nodes.new('ShaderNodeMath');cmp.operation='GREATER_THAN';drive(cmp.inputs[1],'default_value','t',{'t':'event_time_s'})
    interp=g.nodes.new('GeometryNodeInputNamedAttribute');interp.data_type='FLOAT';interp.inputs['Name'].default_value='interpolated';mul=g.nodes.new('ShaderNodeMath');mul.operation='MULTIPLY';drive(mul.inputs[1],'default_value','1-show',{'show':'show_interpolated'});both=g.nodes.new('ShaderNodeMath');both.operation='MAXIMUM'
    for a,b in [(inp.outputs[0],delete.inputs['Geometry']),(at.outputs['Attribute'],cmp.inputs[0]),(interp.outputs['Attribute'],mul.inputs[0]),(cmp.outputs[0],both.inputs[0]),(mul.outputs[0],both.inputs[1]),(both.outputs[0],delete.inputs['Selection']),(delete.outputs[0],out.inputs[0])]:g.links.new(a,b)
    return g
reveal=reveal_group()
def attribute(mesh,name,values,kind='FLOAT'):
    a=mesh.attributes.new(name,kind,'POINT')
    for p,v in zip(a.data,values):p.value=v
def object_mesh(name,vs,fs,mat):
    me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(name,me);col.objects.link(o);me.materials.append(mat)
    for p in me.polygons:p.use_smooth=True
    mod=o.modifiers.new('Only acquired/completed bins; interpolation opt-in','NODES');mod.node_group=reveal;return o
def point_group():
    g=bpy.data.node_groups.new('B202_v009_Acquired_Point_Display','GeometryNodeTree');g.interface.new_socket(name='Geometry',in_out='INPUT',socket_type='NodeSocketGeometry');g.interface.new_socket(name='Geometry',in_out='OUTPUT',socket_type='NodeSocketGeometry');inp=g.nodes.new('NodeGroupInput');out=g.nodes.new('NodeGroupOutput');pts=g.nodes.new('GeometryNodeMeshToPoints');pts.mode='VERTICES';ico=g.nodes.new('GeometryNodeMeshIcoSphere');ico.inputs['Radius'].default_value=.0012;ico.inputs[' subdivisions' if ' subdivisions' in ico.inputs else 'Subdivisions'].default_value=1;mat=g.nodes.new('GeometryNodeSetMaterial');mat.inputs['Material'].default_value=cyan;inst=g.nodes.new('GeometryNodeInstanceOnPoints')
    for a,b in [(inp.outputs[0],pts.inputs['Mesh']),(ico.outputs[0],mat.inputs['Geometry']),(pts.outputs['Points'],inst.inputs['Points']),(mat.outputs[0],inst.inputs['Instance']),(inst.outputs[0],out.inputs[0])]:g.links.new(a,b)
    return g
points_display=point_group();manifest={'case_names':case_names,'objects':{},'source_data_index_sha256':hashlib.sha256((DATA/'index_v009.json').read_bytes()).hexdigest(),'stills':[]}
for idx,case in enumerate(case_names):
    grid=read_json(DATA/'interpolation_fixture_grid_v009.json.gz') if case=='interpolation_fixture' else read_json(DATA/INDEX['cases'][case]['files']['grid'])
    vs,fs,ids=mesh_from_grid(grid,show_interpolated=True);cells=[grid['cells'][i] for i in ids]
    for field,mat,prop in [('radius',geom,'show_reconstruction'),('echo_strength',amp,'show_echo_strength')]:
        if field=='echo_strength':
            # No amplitude-colored vertex exists where this channel is invalid.
            allowed={j for j,p in enumerate(cells) if p['valid_amplitude']};field_faces=[f for f in fs if all(j in allowed for j in f)]
        else:field_faces=fs
        o=object_mesh(f'B202_v009_{case}_{field}',vs,field_faces,mat);visibility(o,idx,prop)
        o['data_case']=case;o['quantity']='delta_radius_m' if field=='radius' else 'echo_strength';o['lineage_grid']=('Data/v009/interpolation_fixture_grid_v009.json.gz' if case=='interpolation_fixture' else 'Data/v009/'+INDEX['cases'][case]['files']['grid'])
        for name,vals,kind in [('cell_index',ids,'INT'),('radius_m',[p['radius_m'] for p in cells],'FLOAT'),('delta_radius_m',[p['delta_radius_m'] for p in cells],'FLOAT'),('echo_strength',[p['echo_strength'] or 0 for p in cells],'FLOAT'),('ready_timestamp_s',[p['ready_timestamp_s'] for p in cells],'FLOAT'),('measured',[int(p['measured']) for p in cells],'FLOAT'),('interpolated',[int(p['interpolated']) for p in cells],'FLOAT'),('geometry_display',[(p['delta_radius_m']+.0012)/(.0254+.0012) for p in cells],'FLOAT'),('echo_strength_display',[(p['echo_strength'] or 0)/.4 for p in cells],'FLOAT')]:attribute(o.data,name,vals,kind)
        manifest['objects'][o.name]={'case':case,'field':field,'vertex_cells':ids,'vertices':len(vs),'faces':len(field_faces)}
    # Event point cloud uses reconstructed hits; it has no copied ground truth.
    sourcecase='irregular_layers' if case=='interpolation_fixture' else case
    evs=read_json(DATA/INDEX['cases'][sourcecase]['files']['events']);ps=reconstruct(evs,C);o=object_mesh(f'B202_v009_{case}_acquired_points',[p['position_m'] for p in ps],[],cyan)
    visibility(o,idx,'show_acquired_points');attribute(o.data,'ready_timestamp_s',[p['timestamp_s'] for p in ps]);attribute(o.data,'interpolated',[0]*len(ps));attribute(o.data,'event_sequence',list(range(len(ps))),'INT');o['source_event_ids']=json.dumps([p['sample_id'] for p in ps]);o['quantity']='registered_measurement_points';o['data_case']=case
    mod=o.modifiers.new('Sparse acquired hit markers','NODES');mod.node_group=points_display
c['show_tool']=0;c['show_nominal']=0;c['show_amplitude']=0;c['show_envelope']=0;c['event_time_s']=1000.;c.update_tag();bpy.context.view_layer.update()
s.frame_start=s.frame_end=1;s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s['B202_v009_config']=json.dumps(C);s['B202_v009_scope']='Measurement-derived geometry and echo response; synthetic, no calibrated accuracy, no T27 animation.'
s.camera.location=(.2,-4.5,2.5);s.camera.rotation_euler=(Vector((3.1,0,0))-s.camera.location).to_track_quat('-Z','Y').to_euler();s.camera.data.lens=60
for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(BASE/'Scenes'))
# Keep the established white nominal reference with the new world-fixed data.
nominal=bpy.data.objects['B202_NOMINAL_01'].copy();nominal.data=nominal.data.copy();nominal.animation_data_clear();col.objects.link(nominal);nominal.name='B202_v009_WHITE_NOMINAL';nominal.hide_render=False;nominal.hide_viewport=False
for p in ('hide_render','hide_viewport'):drive(nominal,p,'1-show',{'show':'show_nominal'})
s.render.filepath=str(PRE/'irregular_layers_radius_v009.png');c['data_case']=case_names.index('irregular_layers');s['B202_v009_state']='irregular_layers / radius';bpy.ops.wm.save_as_mainfile(filepath=str(OUT),relative_remap=False)
renders=[('irregular_constant','radius'),('irregular_changed_constant','radius'),('irregular_material_changed','radius'),('irregular_constant','echo_strength'),('irregular_changed_constant','echo_strength'),('irregular_material_changed','echo_strength'),('irregular_layers','echo_strength'),('spiral_layers','radius'),('tight_layers','radius'),('sparse_irregular','radius')]
for case,field in renders:
    c['data_case']=case_names.index(case);c['show_reconstruction']=int(field=='radius');c['show_echo_strength']=int(field=='echo_strength');c.update_tag();bpy.context.view_layer.update();s['B202_v009_state']=case+' / '+field
    image=PRE/f'{case}_{field}_v009.png';scene=BASE/f'Scenes/B202_{case}_{field}_v009.blend';s.render.filepath=str(image);bpy.ops.wm.save_as_mainfile(filepath=str(scene),relative_remap=False);t=time.time();bpy.ops.render.render(write_still=True)
    manifest['stills'].append({'case':case,'field':field,'image':image.relative_to(ROOT).as_posix(),'scene':scene.relative_to(ROOT).as_posix(),'render_seconds':time.time()-t,'image_sha256':hashlib.sha256(image.read_bytes()).hexdigest(),'scene_sha256':hashlib.sha256(scene.read_bytes()).hexdigest()})
    write_json(E/'consumer_manifest_v009.json',manifest)
print('B202_V009_CONSUMER_PASS')
