"""Bounded actual-image repairs; all predecessor scenes stay immutable."""
import bpy,json,hashlib
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parents[5];A=ROOT/'04-Production/Shared/Assets';T=ROOT/'04-Production/Records/Tasks/T-047';S=T/'Scenes';E=T/'Evidence'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.relative_to(ROOT).as_posix()
def openfile(p):bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False,use_scripts=False)
def dump(p,d):p.write_text(json.dumps(d,indent=2),encoding='utf8')
def save(p):
 assert not p.exists(),p
 for l in bpy.data.libraries:l.filepath=bpy.path.relpath(bpy.path.abspath(l.filepath),start=str(p.parent))
 bpy.ops.wm.save_as_mainfile(filepath=str(p),relative_remap=False)
def arc_channels():
 return {o.name:[(fc.data_path,fc.array_index,[list(k.co) for k in fc.keyframe_points]) for layer in o.animation_data.action.layers for st in layer.strips for b in st.channelbags for fc in b.fcurves] for o in bpy.data.objects if o.get('shared_package')=='Acoustics' and ('_SEND_' in o.name or '_RETURN_' in o.name)}
src=S/'CasedSupport_v010.blend';old=sha(src);openfile(src);s=bpy.context.scene;s.frame_set(1);arcs=arc_channels();cam=dict(location=list(s.camera.location),rotation=list(s.camera.rotation_euler),lens=s.camera.data.lens);removed=[];scaled=[]
for o in list(bpy.data.objects):
 if not o.library and o.name.startswith('CASED_') and '_RESPONSE_' in o.name:removed.append(o.name);bpy.data.objects.remove(o,do_unlink=True)
 elif o.get('shared_package')=='Acoustics' and ('CONTACT_CUP' in o.name or 'FINE_PATCH' in o.name):
  for layer in o.animation_data.action.layers:
   for st in layer.strips:
    for b in st.channelbags:
     for fc in b.fcurves:
      if fc.data_path=='scale':
       for k in fc.keyframe_points:k.co.y*=.35;k.handle_left.y*=.35;k.handle_right.y*=.35
  scaled.append(o.name)
assert len(removed)==24 and len(scaled)==4 and arcs==arc_channels();s.frame_set(1);assert cam==dict(location=list(s.camera.location),rotation=list(s.camera.rotation_euler),lens=s.camera.data.lens);s['qualitative_response']='Screen comparison lanes only. No spatial response bars or simulated steel vibration. Contact cup/patch consumer scale .35; shared pulses unchanged.';out=S/'CasedSupport_v011.blend';save(out);assert sha(src)==old
dump(E/'response-visual-repair_v011.json',dict(source=rel(src),source_sha256=old,candidate=rel(out),sha256=sha(out),removed_spatial_response_bars=removed,contact_cup_patch_scaled=.35,scaled_objects=scaled,all_acoustic_arc_keys_preserved=True,camera_timing_preserved=True,event_export='actual-cased-events_v009.json'))
# Widen the actual full-ID section; no source vertices or4mm recess change.
src=S/'CasedWearSection_v008.blend';old=sha(src);openfile(src);s=bpy.context.scene;before=s.camera.data.ortho_scale;s.camera.data.ortho_scale=.70
if 'SECTION_LIGHT' in bpy.data.objects:bpy.data.objects['SECTION_LIGHT'].data.energy=5
out=S/'CasedWearSection_v011.blend';save(out);assert sha(src)==old
dump(E/'wear-section-framing_v011.json',dict(source=rel(src),candidate=rel(out),sha256=sha(out),old_ortho_scale=before,new_ortho_scale=.70,geometry_unchanged=True,lighting='Section light50→5W to preserve gray surface rather than white clipping'))
# A matched native layer section extracts actual longitudinal mesh edges atX−1.5.
openfile(out);s=bpy.context.scene
for o in list(bpy.data.collections['DERIVED_NATIVE_SECTION'].objects):bpy.data.objects.remove(o,do_unlink=True)
col=bpy.data.collections.new('DERIVED_NATIVE_LAYER_SECTION');s.collection.children.link(col);names=['CASED_STEEL_NOMINAL_FULL','CASED_CEMENT_LEFT_FULL','CASED_CEMENT_RIGHT_FULL','CASED_EXTERIOR_CHANNEL_FULL'];records=[]
for name in names:
 source=bpy.data.objects[name];m=source.data;n=len(m.vertices)//4;assert len(m.vertices)==4*n;xs=[v.co.x for v in m.vertices];assert min(xs)<=-1.5<=max(xs)
 points=[(-1.5,m.vertices[j].co.y,m.vertices[j].co.z) for j in range(n)]+[(-1.5,m.vertices[2*n+j].co.y,m.vertices[2*n+j].co.z) for j in range(n)];faces=[(j,j+1,n+j+1,n+j) for j in range(n-1)];data=bpy.data.meshes.new('SECTION_'+name);data.from_pydata(points,[],faces);data.update();o=bpy.data.objects.new(data.name,data);col.objects.link(o);data.materials.append(source.data.materials[0]);o['source_mesh']=name;o['source_hash']=sha(A/'CasedHole/CasedHole_v002.blend');o['basis']='Native axial edge intersection atX−1.5, exact transverse coordinates; no exploded offsets or rescaling.'
 records.append(dict(source_mesh=name,source_hash=o['source_hash'],source_x_bounds_m=[min(xs),max(xs)],angular_points=n,extracted_vertices=len(points),material=source.data.materials[0].name))
s.camera.data.ortho_scale=.90;out=S/'CasedLayerSection_v011.blend';save(out);dump(E/'native-layer-section_v011.json',dict(scene=rel(out),sha256=sha(out),section_x_m=-1.5,extraction=records,source_scale=1,limits='Actual authored static condition section: steel inside cement/blue gap. Tool/fluid/formation omitted for inspection; no chemistry or flow inferred.'))
# Changed-claim verification only: screen timing, cue scale, unchanged arc channels,
# and complete projected extent of both actual section meshes.
openfile(S/'CasedSupport_v011.blend');s=bpy.context.scene;responses=json.loads((E/'actual-cased-events_v009.json').read_text())['responses'];checks=[]
assert not any(o.name.startswith('CASED_') and '_RESPONSE_' in o.name for o in bpy.data.objects if not o.library)
for response,prefix in zip(responses,['SHORT_DECAY_','LONG_DECAY_']):
 bars=[o for o in s.objects if o.name.startswith(prefix)];assert len(bars)==22;window=[]
 for f in range(1,s.frame_end+1):
  s.frame_set(f);bpy.context.view_layer.update();t=(f-1)/24;elapsed=t-response['response_start_s'];expected_any=0<=elapsed<response['response_lifetime_s'];actual_any=any(not o.hide_render for o in bars);assert actual_any==expected_any,(prefix,f)
  for o in bars:
   i=int(o.name.split('_')[-1]);expected=expected_any and i/22*response['response_lifetime_s']<=elapsed;assert (not o.hide_render)==expected,(o.name,f)
  if actual_any:window.append(f)
 checks.append(dict(response=response['support_state'],visible_frames=window,onset_end_match=True))
for path in [S/'CasedWearSection_v011.blend',S/'CasedLayerSection_v011.blend']:
 openfile(path);s=bpy.context.scene;projections=[world_to_camera_view(s,s.camera,o.matrix_world@v.co) for o in s.objects if not o.library and o.type=='MESH' and o.name.startswith(('ACTUAL_SECTION','SECTION_')) for v in o.data.vertices];assert projections and all(.02<p.x<.98 and .02<p.y<.98 and p.z>s.camera.data.clip_start for p in projections)
 checks.append(dict(scene=rel(path),actual_section_vertices=len(projections),all_vertices_inside_frame=True))
dump(E/'changed-visual-claims_v011.json',dict(passed=True,checks=checks,acoustic_arcs_geometry_keys_unchanged=True,prototypes_unchanged=True,limits='Only changed visual presentation checked; strict packet/envelope proof stays pinned to unchanged arcs/events, with previous camera10 public verification. Actual new PNG inspection follows.'))
print('T47_VISUAL_REPAIR11_PASS',flush=True)
