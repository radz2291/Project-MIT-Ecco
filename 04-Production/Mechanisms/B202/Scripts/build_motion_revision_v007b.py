"""Bounded director correction e8d322 + timing addendum 4d59c63f.
Preserve accepted opening, all datasets and scale. New presentation only.
"""
import bpy,sys,json,math,hashlib
from pathlib import Path
from mathutils import Vector,Matrix
R=Path(__file__).resolve().parents[4];B=R/'04-Production/Mechanisms/B202';E=R/'04-Production/Records/Tasks/T-027/Evidence';P=B/'Previews/MotionRevision_v007b';P.mkdir(exist_ok=True);(P/'Frames').mkdir(exist_ok=True);sys.path.insert(0,str(B/'Scripts'))
from acquisition_core_v009 import read_json
C=read_json(B/'acquisition_config_v009.json');index=read_json(B/'Data/v009/index_v009.json');source=B/'Scenes/B202-M_motion-full_v006d.blend';out=B/'Scenes/B202-M_motion-revision_v007b.blend';assert not out.exists()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();previous=read_json(E/'replay_manifest_v006d.json');hashes=dict(previous['source_hashes']);hashes[source.relative_to(R).as_posix()]=sha(source)
bpy.ops.wm.open_mainfile(filepath=str(source));s=bpy.context.scene;c=bpy.data.objects['B202_CONTROL'];main=s.camera;gaze=bpy.data.objects['T27_v005b_GAZE'];names=json.loads(c['v009_case_names']);bpy.data.collections['T27_v006d_FULL_EXTENSION'].hide_render=True
col=bpy.data.collections.new('T27_v007b_PRESENTATION');s.collection.children.link(col);spiralcol=bpy.data.collections.new('T27_v007b_SPIRAL_CONTOURS');s.collection.children.link(spiralcol);truecol=bpy.data.collections.new('T27_v007b_INSET_SOURCE');s.collection.children.link(truecol)
def smooth(t):t=max(0,min(1,t));return t*t*(3-2*t)
def key(k,v,f):c[k]=v;c.keyframe_insert(data_path='["'+k+'"]',frame=f)
def visibility(o,a,b):
    for attr in ('hide_render','hide_viewport'):
        for f,v in ((1,True),(a,False),(b+1,True)):setattr(o,attr,v);o.keyframe_insert(data_path=attr,frame=f)
def emission(name,color):
    m=bpy.data.materials.new(name);m.use_nodes=True;t=m.node_tree;t.nodes.clear();e=t.nodes.new('ShaderNodeEmission');e.inputs[0].default_value=(*color,1);o=t.nodes.new('ShaderNodeOutputMaterial');t.links.new(e.outputs[0],o.inputs[0]);return m
white=bpy.data.materials['T27 v005b expected nominal'];blue=emission('T27 v007b contour blue',(.025,.40,.72));red=emission('T27 v007b tight red',(.8,.035,.025));muted=emission('T27 v007b source qualifier',(.42,.48,.54));warm=emission('T27 v007b warm label',(.95,.65,.14));guide=emission('T27 v007b crest guide',(.32,.78,1.))
def curve(name,coords,material,width,collection=col,closed=False):
    d=bpy.data.curves.new(name,'CURVE');d.dimensions='3D';d.bevel_depth=width;d.bevel_resolution=2;sp=d.splines.new('POLY');sp.points.add(len(coords)-1);sp.use_cyclic_u=closed
    for p,v in zip(sp.points,coords):p.co=(*v,1)
    o=bpy.data.objects.new(name,d);collection.objects.link(o);d.materials.append(material);return o
def makecam(name,loc,target,lens=42,ortho=None):
    d=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,d);col.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();d.lens=lens;d.clip_start=.0002
    if ortho:d.type='ORTHO';d.ortho_scale=ortho
    return o
cmpcam=makecam('T27_v007b_COMPARISON_CAMERA',(1.5,0,0),(2.75,0,0),ortho=1.0);ampcam=makecam('T27_v007b_AMPLITUDE_CAMERA',(3.25,4.1,0),(3.25,0,0));ampcam.rotation_mode='QUATERNION'
for f,cam in ((1,main),(337,cmpcam),(433,main),(601,ampcam)):
    marker=s.timeline_markers.new('v007b view '+str(f),frame=f);marker.camera=cam
# Comparison copies preserve true local coordinates and unit scale. Translation
# stages DIFFERENT cases side-by-side; each nominal/measured pair shares a parent.
grids={case:read_json(B/'Data/v009'/index['cases'][case]['files']['grid']) for case in ('irregular_layers','tight_layers','spiral_layers')};comparisons=[]
for case,stage_y,material in (('irregular_layers',.23,blue),('tight_layers',-.23,red)):
    cells=grids[case]['cells'][432:540];parent=bpy.data.objects.new('T27_v007b_STAGE_'+case,None);col.objects.link(parent);parent.location=(0,stage_y,.055);parent['meaning']='Display translation of a separate illustrative case; no radius/axis scaling.'
    actual=[(x['x_m'],x['radius_m']*math.cos(x['azimuth_rad']),x['radius_m']*math.sin(x['azimuth_rad'])) for x in cells];nominal=[(x['x_m'],C['nominal_radius_m']*math.cos(x['azimuth_rad']),C['nominal_radius_m']*math.sin(x['azimuth_rad'])) for x in cells]
    for kind,coords,m,width in (('nominal',nominal,white,.00045),('measured',actual,material,.00018 if case=='tight_layers' else .00065)):
        o=curve('T27_v007b_COMPARE_'+case+'_'+kind,coords,m,width,closed=True);o.parent=parent;o['source_case']=case;o['source_cells']=json.dumps(list(range(432,540)));visibility(o,337,432);comparisons.append(o.name)
    if case=='irregular_layers':
        me=bpy.data.meshes.new('v007b enlargement band');me.from_pydata(actual+nominal,[],[(i,(i+1)%108,(i+1)%108+108,i+108) for i in range(108)]);ob=bpy.data.objects.new('T27_v007b_ENLARGEMENT_BAND',me);col.objects.link(ob);ob.parent=parent;me.materials.append(bpy.data.materials['T27 v005b true enlargement comparison band']);visibility(ob,337,432)
    else:
        tightcells=cells;mincell=min(cells,key=lambda x:x['delta_radius_m']);angle=mincell['azimuth_rad'];point=Vector(actual[cells.index(mincell)]);focus=point.copy();focus.y=C['nominal_radius_m']*math.cos(angle);focus.z=C['nominal_radius_m']*math.sin(angle)
        for kind,coords,m in (('nominal',nominal,white),('measured',actual,red)):curve('T27_v007b_INSET_'+kind,coords,m,.00010,truecol,True)
# Render a source-coordinate close view before adding any editorial overlay.
# Detail magnification = plane_width .14 / ortho_window .028 = 5x relative to
# comparison_camera ortho_width1.0. No measured coordinates/radii are scaled.
s.frame_set(480);c['show_tool']=0;c['show_reconstruction']=0;c['show_echo_strength']=0;c['show_acquired_points']=0;c.update_tag();spiralcol.hide_render=True
closecam=makecam('T27_v007b_INSET_CAMERA',(2.66,focus.y,focus.z),focus,ortho=.028);s.camera=closecam;s.render.resolution_x=512;s.render.resolution_y=512;s.render.filepath=str(P/'tight_detail_source_v007b.png');bpy.ops.render.render(write_still=True);truecol.hide_render=True;spiralcol.hide_render=False;s.render.resolution_x=960;s.render.resolution_y=540
image=bpy.data.images.load(str(P/'tight_detail_source_v007b.png'));image.filepath=bpy.path.relpath(str(P/'tight_detail_source_v007b.png'),start=str(out.parent));m=bpy.data.materials.new('T27 v007b actual source-camera inset');m.use_nodes=True;t=m.node_tree;t.nodes.clear();tex=t.nodes.new('ShaderNodeTexImage');tex.image=image;em=t.nodes.new('ShaderNodeEmission');output=t.nodes.new('ShaderNodeOutputMaterial');t.links.new(tex.outputs['Color'],em.inputs[0]);t.links.new(em.outputs[0],output.inputs[0]);me=bpy.data.meshes.new('Source-camera inset display');me.from_pydata([(-.07,-.07,0),(.07,-.07,0),(.07,.07,0),(-.07,.07,0)],[],[(0,1,2,3)]);uv=me.uv_layers.new();
for loop,co in zip(uv.data,[(0,0),(1,0),(1,1),(0,1)]):loop.uv=co
ob=bpy.data.objects.new('T27_v007b_DETAIL_INSET_5X',me);col.objects.link(ob);ob.parent=cmpcam;ob.location=(.26,-.20,-.7);me.materials.append(m);visibility(ob,337,432);ob['source_camera']=closecam.name;ob['view_magnification']=5.;ob['source_grid_cell']=mincell['index']
# A quiet source-anchored locator indicates WHERE the reduced radius is, while
# the full circumference remains visible above its separate detail inset.
parent=bpy.data.objects['T27_v007b_STAGE_tight_layers'];outer=point.copy();outer.y*=1.14;outer.z*=1.14;o=curve('T27_v007b_TIGHT_LOCATION_GUIDE',[point,outer],red,.0007);o.parent=parent;visibility(o,337,432)
# Source-registered station contours and a sampled crest guide show spatial twist.
spiral_objects=[];crest=[];crest_cells=[]
for di in range(13):
    cells=grids['spiral_layers']['cells'][di*108:(di+1)*108];coords=[(x['x_m'],x['radius_m']*math.cos(x['azimuth_rad']),x['radius_m']*math.sin(x['azimuth_rad'])) for x in cells];o=curve('T27_v007b_SPIRAL_SECTION_'+str(di),coords,blue,.0009,spiralcol,True);o['grid_cells']=json.dumps([x['index'] for x in cells]);visibility(o,433,528);spiral_objects.append(o.name);peak=max(cells,key=lambda x:x['radius_m']);crest_cells.append(peak['index']);crest.append(coords[cells.index(peak)])
o=curve('T27_v007b_SAMPLED_ENLARGEMENT_CREST',crest,guide,.0015,spiralcol);o['grid_cells']=json.dumps(crest_cells);o['meaning']='Guide joins adjacent measured section maxima, not extra acquired samples or diagnosed cause.';visibility(o,433,528)
# Fixed0–0.4 normalization retained, with one declared higher-contrast transfer
# function used for every warm frame. No per-frame/case normalization.
mat=bpy.data.materials['B202_v009_received_echo_strength'];ramp=next(n for n in mat.node_tree.nodes if n.type=='VALTORGB');palette=[(0.,(.012,.003,.001)),(.25,(.16,.035,.004)),(.5,(1.,.62,.04)),(1.,(1.,.95,.42))]
while len(ramp.color_ramp.elements)>1:ramp.color_ramp.elements.remove(ramp.color_ramp.elements[-1])
for i,(position,color) in enumerate(palette):
    el=ramp.color_ramp.elements[0] if i==0 else ramp.color_ramp.elements.new(position);el.position=position;el.color=(*color,1)
font=bpy.data.fonts.load('C:/Windows/Fonts/segoeui.ttf');labels=[]
def label(name,text,camera,a,b,x,y,size,material):
    d=bpy.data.curves.new(name,'FONT');d.body=text;d.font=font;d.size=size;o=bpy.data.objects.new('T27_v007b_'+name,d);col.objects.link(o);o.parent=camera;o.location=(x,y,-.7);d.materials.append(material);visibility(o,a,b);labels.append({'object':o.name,'text':text,'frames':[a,b]})
label('comparison_title','Illustrative examples: expected versus actual',cmpcam,337,432,-.44,.24,.021,white)
label('enlarged_label','A / Enlarged',cmpcam,337,432,-.39,.205,.017,blue);label('tight_label','B / Local tight spot',cmpcam,337,432,.08,.205,.017,red)
label('detail_label','Detail view 5x',cmpcam,337,432,.18,-.12,.013,white)
label('comparison_key','White: expected hole',cmpcam,337,432,-.44,-.23,.016,white);label('comparison_synthetic','Synthetic examples',cmpcam,337,432,-.44,-.26,.013,muted)
label('spiral_title','Case C / Shape turns through depth',main,433,528,-.255,.15,.015,white);label('spiral_key','Contours and crest follow source geometry',main,433,528,-.255,.127,.0105,guide);label('spiral_synthetic','Synthetic example',main,433,528,-.255,-.153,.010,muted)
label('bridge_title','Same returned echo. Two properties.',main,529,600,-.255,.15,.015,white);label('bridge_time','Travel time: hole shape',main,529,600,-.255,.12,.013,blue);label('bridge_strength','Echo strength: acoustic response',main,529,600,-.255,.095,.013,warm);label('bridge_case','Back to example A / synthetic data',main,529,600,-.255,-.153,.010,muted)
label('amplitude_title','Example A / Echo strength',ampcam,601,720,-.255,.15,.015,warm);label('amplitude_key','Varies with material and sound path',ampcam,601,720,-.255,.127,.011,white);label('amplitude_truth','Synthetic response, not rock colour',ampcam,601,720,-.255,-.153,.010,muted)
camera=[];extension=[]
for f in range(337,721):
    if f<=432:case='tight_layers';radius=amp=0;phase='paired_geometry_examples';loc=(2.05,0,0);target=(2.75,0,0);opacity=.95
    elif f<=528:
        case='spiral_layers';radius=0;amp=0;phase='spiral_contours';u=smooth((f-433)/95);loc=Vector((.2,2.6,1.25)).lerp(Vector((.6,2.5,.7)),u);target=(3.25,0,0);opacity=.13
    else:case='irregular_layers';radius=int(f<=600);amp=int(f>=601);phase='two_properties_bridge' if f<=600 else 'acoustic_response';loc=(.2,2.3,1.3);target=(3.25,0,0);opacity=.95
    for k,v in {'data_case':names.index(case),'show_tool':0,'show_nominal':0,'show_reconstruction':radius,'show_echo_strength':amp,'show_acquired_points':0,'show_interpolated':0,'event_time_s':1000.,'geometry_opacity':opacity,'amplitude_opacity':1.}.items():key(k,v,f)
    main.location=loc;gaze.location=target;main.data.lens=42;main.keyframe_insert(data_path='location',frame=f);gaze.keyframe_insert(data_path='location',frame=f);main.data.keyframe_insert(data_path='lens',frame=f)
    # Full circumference shown by camera orbit, never by rotating the data.
    u=smooth((f-601)/119);a=.35+math.tau*u;radial=Vector((0,math.cos(a),math.sin(a)));ampcam.location=Vector((3.25,0,0))+4.1*radial;right=Vector((1,0,0));up=radial.cross(right);ampcam.rotation_quaternion=Matrix((right,up,radial)).transposed().to_quaternion();ampcam.keyframe_insert(data_path='location',frame=f);ampcam.keyframe_insert(data_path='rotation_quaternion',frame=f)
    extension.append({'frame':f,'case':case,'phase':phase,'show_reconstruction':radius,'show_echo_strength':amp,'geometry_opacity':opacity});camera.append({'frame':f,'main_location':list(loc),'main_target':list(target),'amplitude_location':list(ampcam.location),'amplitude_quaternion':list(ampcam.rotation_quaternion)})
for action in bpy.data.actions:
    for slot in action.slots:
        for layer in action.layers:
            for strip in layer.strips:
                bag=strip.channelbag(slot)
                if bag:
                    for fc in bag.fcurves:
                        for k in fc.keyframe_points:
                            if k.co.x>=336:k.interpolation='CONSTANT' if 'hide_' in fc.data_path or fc.data_path.startswith('["') or k.co.x in (336,432,528,600) else 'LINEAR'
s.frame_end=720;s['T27_v007b_scope']='Bounded visual correction. Accepted opening retained; paired separate enlargement/tight examples, source contours/crest, two-properties bridge, fixed-range varying acoustic-response view. Library30s, not S03finaledit18s.'
s.frame_set(1);s.camera=main;s.render.filepath=str(P/'Frames/frame_');bpy.ops.wm.save_as_mainfile(filepath=str(out),relative_remap=False)
manifest={'version':'v007b','scene':out.relative_to(R).as_posix(),'source_scene':source.relative_to(R).as_posix(),'source_hashes':hashes,'extension':extension,'camera':camera,'comparison_objects':comparisons,'spiral_objects':spiral_objects,'crest_cells':crest_cells,'labels':labels,'inset':{'source_image':(P/'tight_detail_source_v007b.png').relative_to(R).as_posix(),'source_camera':closecam.name,'source_cell':mincell['index'],'magnification':5,'ortho_window_m':.028,'display_plane_width_m':.14,'comparison_ortho_width_m':1.0},'echo_palette':palette,'fixed_echo_range':C['echo_display_range'],'new_data_generated':False,'review_comments':['e8d322e8-06e4-462a-9f8e-0c0744b473a3','4d59c63f-922c-4782-8d42-8cda03ec5be5'],'cuts':[337,433,529,601]}
(E/'replay_manifest_v007b.json').write_text(json.dumps(manifest,indent=2));assert all(sha(R/p)==h for p,h in hashes.items())
for f in (168,336,384,480,552,601,648,684,720):s.frame_set(f);s.render.filepath=str(P/f'proof_{f:04d}.png');bpy.ops.render.render(write_still=True)
print('BUILD_V007_PASS')
