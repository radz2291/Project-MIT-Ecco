"""Extend accepted v005b without changing its first336frames or source datasets."""
import bpy,sys,json,math,hashlib
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[4];B=R/'04-Production/Mechanisms/B202';E=R/'04-Production/Records/Tasks/T-027/Evidence';P=B/'Previews/MotionFull_v006'
P.mkdir(exist_ok=True);(P/'Frames').mkdir(exist_ok=True);sys.path.insert(0,str(B/'Scripts'))
from acquisition_core_v009 import read_json
C=read_json(B/'acquisition_config_v009.json');index=read_json(B/'Data/v009/index_v009.json')
source=B/'Scenes/B202-M_motion-proof_v005b.blend';out=B/'Scenes/B202-M_motion-full_v006.blend';assert not out.exists()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
M=read_json(E/'replay_manifest_v005b.json');hashes=dict(M['source_hashes']);hashes[source.relative_to(R).as_posix()]=sha(source)
for case in ('irregular_layers','spiral_layers','tight_layers'):
    for kind in ('events','grid'):
        p=B/'Data/v009'/index['cases'][case]['files'][kind];hashes[p.relative_to(R).as_posix()]=sha(p)
bpy.ops.wm.open_mainfile(filepath=str(source));s=bpy.context.scene;c=bpy.data.objects['B202_CONTROL'];cam=s.camera;gaze=bpy.data.objects['T27_v005b_GAZE'];col=bpy.data.collections.new('T27_v006_FULL_EXTENSION');s.collection.children.link(col);names=json.loads(c['v009_case_names'])
def smooth(t):t=max(0,min(1,t));return t*t*(3-2*t)
def key(k,v,f):c[k]=v;c.keyframe_insert(data_path='["'+k+'"]',frame=f)
def visibility(o,a,b):
    for attr in ('hide_render','hide_viewport'):
        for f,v in ((1,True),(a,False),(b+1,True)):
            setattr(o,attr,v);o.keyframe_insert(data_path=attr,frame=f)
# Suppress first-view comparison/context overlays only after the accepted clip.
for o in bpy.data.objects:
    if o.name.startswith('T27_v005b_contour_') or o.name.startswith('T27_v005b_WHITE_NOMINAL_') or o.name in ('T27_v005b_MEASURED_FOCUS_CONTOUR','T27_v005b_EXPECTED_NOMINAL_FOCUS','T27_v005b_ACTUAL_MINUS_EXPECTED'):
        for attr in ('hide_render','hide_viewport'):
            setattr(o,attr,True);o.keyframe_insert(data_path=attr,frame=337)
# Same original fixed echo ramp, emission solely for data readability.
mat=bpy.data.materials['B202_v009_received_echo_strength'];t=mat.node_tree;ramp=next(n for n in t.nodes if n.type=='VALTORGB');mix=next(n for n in t.nodes if n.type=='MIX_SHADER');em=t.nodes.new('ShaderNodeEmission');em.inputs['Strength'].default_value=1;t.links.new(ramp.outputs['Color'],em.inputs['Color']);t.links.new(em.outputs[0],mix.inputs[2])
font=bpy.data.fonts.load('C:/Windows/Fonts/segoeui.ttf');white=bpy.data.materials['T27 v005b expected nominal'];blue=bpy.data.materials['T27 v005b measured outline']
def emission(name,color):
    m=bpy.data.materials.new(name);m.use_nodes=True;nt=m.node_tree;nt.nodes.clear();e=nt.nodes.new('ShaderNodeEmission');e.inputs[0].default_value=(*color,1);o=nt.nodes.new('ShaderNodeOutputMaterial');nt.links.new(e.outputs[0],o.inputs[0]);return m
red=emission('T27 v006 tight contour',(.8,.035,.025));warm=emission('T27 v006 echo heading',(.9,.65,.24));muted=emission('T27 v006 source qualifier',(.42,.48,.54))
labels=[]
def label(text,a,b,y,material,size=.018,x=-.31):
    d=bpy.data.curves.new(text,'FONT');d.body=text;d.font=font;d.size=size;o=bpy.data.objects.new('T27_v006_label_'+text,d);col.objects.link(o);o.parent=cam;o.location=(x,y,-.7);d.materials.append(material);visibility(o,a,b);labels.append({'object':o.name,'text':text,'frames':[a,b]});return o
label('Illustrative spiral geometry',337,432,.18,white)
label('Synthetic example',337,552,-.185,muted,.012)
label('Illustrative tight section',433,528,.18,white)
label('White: expected   /   Red: tight section',433,528,-.15,white,.014)
label('Hole geometry',529,552,.18,blue)
label('Echo strength',553,720,.18,warm)
label('Reflected signal, not rock colour',553,720,.15,white,.013)
label('Synthetic example',553,720,-.185,muted,.012)
# Cross-section from original tight-case measured cells, same coordinates/scale.
grid=read_json(B/'Data/v009'/index['cases']['tight_layers']['files']['grid']);cells=grid['cells'][432:540];assert all(x['measured'] and not x['interpolated'] for x in cells)
tight=[]
for name,radii,material,thickness in [('MEASURED',[x['radius_m'] for x in cells],red,.00035),('NOMINAL',[C['nominal_radius_m']]*108,white,.00025)]:
    d=bpy.data.curves.new('T27_v006_TIGHT_'+name,'CURVE');d.dimensions='3D';d.bevel_depth=thickness;d.bevel_resolution=2;sp=d.splines.new('POLY');sp.points.add(107);sp.use_cyclic_u=True
    for p,x,r in zip(sp.points,cells,radii):p.co=(x['x_m'],r*math.cos(x['azimuth_rad']),r*math.sin(x['azimuth_rad']),1)
    o=bpy.data.objects.new(d.name,d);col.objects.link(o);d.materials.append(material);o['lineage_grid']='Data/v009/'+index['cases']['tight_layers']['files']['grid'];visibility(o,433,528);tight.append(o.name)
# Original key channels ending before336 must hold, never interpolate backwards
# from a later extension key. Pin all control channels at the accepted endpoint.
s.frame_set(336);bpy.context.view_layer.update()
for k in ('data_case','show_tool','show_nominal','show_reconstruction','show_echo_strength','show_acquired_points','show_interpolated','event_time_s','geometry_opacity','amplitude_opacity','travel_m','rotation_rad'):
    key(k,c[k],336)
# A hard editorial cut changes completed datasets; no acquisition or interpolation.
camera=[];extension=[]
for f in range(337,721):
    if f<=432:
        case='spiral_layers';phase='illustrative_spiral';u=smooth((f-337)/95);loc=Vector((.5,1.8,1.05)).lerp(Vector((.9,1.65,.55)),u);target=(3.1,0,0);lens=42;radius=1;amp=0
    elif f<=528:
        case='tight_layers';phase='illustrative_tight';loc=Vector((2.05,0,0));target=(2.75,0,0);lens=35;radius=0;amp=0
    else:
        case='irregular_layers';phase='geometry_return' if f<=552 else 'separate_echo_strength';u=smooth((f-553)/167);loc=Vector((1.3,1.2,.65)).lerp(Vector((1.45,1.35,.3)),u);target=(3.1,0,0);lens=42;radius=int(f<=552);amp=int(f>=553)
    for k,v in {'data_case':names.index(case),'show_tool':0,'show_nominal':0,'show_reconstruction':radius,'show_echo_strength':amp,'show_acquired_points':0,'show_interpolated':0,'event_time_s':1000.,'geometry_opacity':.95,'amplitude_opacity':1.}.items():key(k,v,f)
    cam.location=loc;gaze.location=target;cam.data.lens=lens;cam.keyframe_insert(data_path='location',frame=f);gaze.keyframe_insert(data_path='location',frame=f);cam.data.keyframe_insert(data_path='lens',frame=f)
    camera.append({'frame':f,'location':list(loc),'target':list(target),'lens_mm':lens});extension.append({'frame':f,'case':case,'phase':phase,'show_reconstruction':radius,'show_echo_strength':amp,'cutoff_s':1000.,'show_tool':0})
# Match inherited linear keys while forcing editorial changes to be constant.
for action in bpy.data.actions:
    for slot in action.slots:
        for layer in action.layers:
            for strip in layer.strips:
                bag=strip.channelbag(slot)
                if bag:
                    for fc in bag.fcurves:
                        for k in fc.keyframe_points:
                            if k.co.x>=336:k.interpolation='CONSTANT' if 'hide_' in fc.data_path or fc.data_path.startswith('["show_') or fc.data_path=='["data_case"]' or k.co.x in (336,432,528,552) else 'LINEAR'
s.frame_end=720;s['T27_v006_scope']='30s full mechanical candidate; first336frames accepted v005b preserved; independent completed illustrative spiral/tight cases; separate original echo channel. Not field data, diagnosis, MIT certification or final film edit.'
for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(out.parent))
s.frame_set(1);s.render.filepath=str(P/'Frames/frame_');bpy.ops.wm.save_as_mainfile(filepath=str(out),relative_remap=False)
result={'version':'v006','scene':out.relative_to(R).as_posix(),'source_scene':source.relative_to(R).as_posix(),'source_hashes':hashes,'inherited_manifest':'04-Production/Records/Tasks/T-027/Evidence/replay_manifest_v005b.json','inherited_frames':[1,336],'extension':extension,'camera':camera,'tight_objects':tight,'labels':labels,'fixed_geometry_range_m':C['geometry_display_range_m'],'fixed_echo_range':C['echo_display_range'],'cuts':[337,433,529,553],'qualifier':'Synthetic recorded examples. No new events. No bit/tool passage in tight/spiral. No geometry-to-amplitude morph.'}
(E/'replay_manifest_v006.json').write_text(json.dumps(result,indent=2));assert all(sha(R/p)==h for p,h in hashes.items())
for f in (336,337,384,432,480,540,553,624,720):s.frame_set(f);s.render.filepath=str(P/f'proof_{f:04d}.png');bpy.ops.render.render(write_still=True)
print('T27_FULL_V006_BUILD_PASS')
