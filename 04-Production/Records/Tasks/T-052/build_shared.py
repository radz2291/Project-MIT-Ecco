"""Versioned ECCO/BHA finish packaging; never overwrite accepted inputs."""
import bpy,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[4]; T=Path(__file__).resolve().parent
A=R/'04-Production/Shared/Assets'; E=A/'ECCO'; B=A/'BHA'
S=json.loads((R/'04-Production/Records/Tasks/T-050/sources.json').read_text()); S={s['id']:R/s['native'] for s in S}
for d in ['Consumers','Previews','Evidence']: (T/d).mkdir(exist_ok=True)
LIB=E/'Satin_finish_v001.blend'; GROUP='ECCO | Satin finish v001'
def save(p):
    bpy.ops.wm.save_as_mainfile(filepath=str(p),relative_remap=True)
    bpy.ops.file.make_paths_relative()
    bpy.ops.wm.save_as_mainfile(filepath=str(p))
def group_link():
    with bpy.data.libraries.load(str(LIB),link=True) as (a,b):b.node_groups=[GROUP]
    return b.node_groups[0]
def apply_group(mat,group,dark=False):
    mat.use_nodes=True; nodes=mat.node_tree.nodes; links=mat.node_tree.links
    bs=next(n for n in nodes if n.type=='BSDF_PRINCIPLED')
    gn=nodes.new('ShaderNodeGroup');gn.node_tree=group;gn.name='Shared satin controls';gn.label='Linked finish; lights and alpha remain local'
    gn.inputs['Sensor face'].default_value=1 if dark else 0
    for key in ['Base Color','Roughness','Metallic']:links.new(gn.outputs[key],bs.inputs[key])
    return mat
def camera_record():
    s=bpy.context.scene; old=s.frame_current; out={'range':[s.frame_start,s.frame_end],'fps':s.render.fps,'samples':[]}
    for f in sorted(set([s.frame_start,(s.frame_start+s.frame_end)//2,s.frame_end])):
        s.frame_set(f); c=s.camera
        out['samples'].append({'frame':f,'name':c.name if c else None,'matrix':[list(r) for r in c.matrix_world] if c else None,'lens':c.data.lens if c else None})
    s.frame_set(old);return out
def relink(old,new):
    for lib in list(bpy.data.libraries):
        if Path(bpy.path.abspath(lib.filepath)).name==old:
            lib.filepath=str(new);lib.reload()

# A reusable linked group lets consumer materials retain alpha/transparency overrides.
bpy.ops.wm.read_factory_settings(use_empty=True)
g=bpy.data.node_groups.new(GROUP,'ShaderNodeTree');g.use_fake_user=True
for name,typ,d in [('Sensor face','NodeSocketFloat',0),('Roughness offset','NodeSocketFloat',0),('Machining strength','NodeSocketFloat',.018)]:
    sock=g.interface.new_socket(name=name,in_out='INPUT',socket_type=typ);sock.default_value=d
for name,typ in [('Base Color','NodeSocketColor'),('Roughness','NodeSocketFloat'),('Metallic','NodeSocketFloat')]:g.interface.new_socket(name=name,in_out='OUTPUT',socket_type=typ)
n=g.nodes;l=g.links;i=n.new('NodeGroupInput');o=n.new('NodeGroupOutput')
mix=n.new('ShaderNodeMixRGB');mix.inputs[1].default_value=(.24,.29,.34,1);mix.inputs[2].default_value=(.12,.17,.19,1);l.new(i.outputs['Sensor face'],mix.inputs[0]);l.new(mix.outputs[0],o.inputs['Base Color'])
tex=n.new('ShaderNodeTexCoord');wave=n.new('ShaderNodeTexWave');wave.wave_type='BANDS';wave.bands_direction='X';wave.inputs['Scale'].default_value=650;wave.inputs['Distortion'].default_value=.35;l.new(tex.outputs['Object'],wave.inputs['Vector'])
mul=n.new('ShaderNodeMath');mul.operation='MULTIPLY';l.new(wave.outputs['Fac'],mul.inputs[0]);l.new(i.outputs['Machining strength'],mul.inputs[1])
base=n.new('ShaderNodeMath');base.operation='ADD';base.inputs[1].default_value=.291;l.new(mul.outputs[0],base.inputs[0])
off=n.new('ShaderNodeMath');off.operation='ADD';l.new(base.outputs[0],off.inputs[0]);l.new(i.outputs['Roughness offset'],off.inputs[1]);l.new(off.outputs[0],o.inputs['Roughness']);o.inputs['Metallic'].default_value=.85
g['provenance']='S07 v006 satin; authored subtle roughness, no physical machining claim';g['revision']=1
for name,dark in [('ECCO Satin Steel v001',False),('ECCO Satin Sensor v001',True)]:
    m=bpy.data.materials.new(name);m.use_fake_user=True;m.use_nodes=True;apply_group(m,g,dark)
save(LIB)
bpy.ops.wm.open_mainfile(filepath=str(S['ECCO-film']));group=group_link()
for o in bpy.data.objects:
    if o.type=='MESH' and 'CUTTER' not in o.name:
        for slot in o.material_slots:
            if slot.material:
                m=slot.material.copy();m.name='ECCO shared satin | '+o.name;apply_group(m,group,'Imaging port' in o.name);slot.link='OBJECT';slot.material=m
bpy.context.scene['source_limits']='ECCO-film v002 source geometry/closures/sensor references unchanged; provisional limits retained'
save(E/'ECCO_film_v003.blend')
# Keep connected hardware and extension controls; relink only inside successors.
bpy.ops.wm.open_mainfile(filepath=str(B/'BHA_film_v006.blend'));relink('ECCO_film_v002.blend',E/'ECCO_film_v003.blend');group=group_link()
for m in list(bpy.data.materials):
    if not m.library and 'Steel' in m.name and m.node_tree:apply_group(m,group)
save(B/'BHA_core_satin_v001.blend')
bpy.ops.wm.open_mainfile(filepath=str(S['BHA']));relink('BHA_film_v006.blend',B/'BHA_core_satin_v001.blend');relink('ECCO_film_v002.blend',E/'ECCO_film_v003.blend');group=group_link()
for m in list(bpy.data.materials):
    if not m.library and 'Steel' in m.name and m.node_tree:apply_group(m,group)
save(B/'BHA_film_v008.blend')
records=[]
for sid in ['S07','S05','S02']:
    bpy.ops.wm.open_mainfile(filepath=str(S[sid]));before=camera_record();group=group_link();changed=[]
    if sid=='S02':relink('ECCO_film_v002.blend',E/'ECCO_film_v003.blend')
    else:
        for o in bpy.data.objects:
            if o.type!='MESH' or 'CUTTER' in o.name:continue
            if not ('ECCO_HOUSING_SOURCE_MESH' in o.name or 'TEMP |' in o.name):continue
            for slot in o.material_slots:
                if slot.material and slot.material.node_tree:
                    m=slot.material.copy();m.name='T052 shared satin | '+o.name;apply_group(m,group,'Imaging port' in o.name);slot.link='OBJECT';slot.material=m;changed.append(o.name)
    out=T/'Consumers'/f'{sid}_shared-satin_v001.blend';save(out)
    records.append({'consumer':str(out.relative_to(R)),'baseline':str(S[sid].relative_to(R)),'camera_before':before,'camera_after':camera_record(),'changed_material_objects':changed,'intentional_changes':'Linked satin group in local material slots; S02 ECCO source relink only. Camera/lights/timing/geometry unchanged. Render settings unchanged in native.'})
(T/'Evidence/consumer-mappings.json').write_text(json.dumps(records,indent=2))
print('BUILD_DONE',len(records))
