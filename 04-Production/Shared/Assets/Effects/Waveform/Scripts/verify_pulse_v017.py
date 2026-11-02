"""Saved-file behavioral checks and bounded Workbench render for pulse release."""
import bpy,sys,json,math,time,hashlib
from pathlib import Path
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).parent))
from pulse_graph import set_input,param
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');B=R/'04-Production/Shared/Assets/Effects/Waveform';P=R/'04-Production/Shared/Demos/Previews/Waveform_v017';P.mkdir(parents=True,exist_ok=True)
report={'checks':[],'renders':[]};checks=report['checks']
def check(name,condition,detail=None):
 checks.append({'name':name,'pass':bool(condition),'detail':detail});assert condition,(name,detail)
def mesh(o,frame):
 bpy.context.scene.frame_set(frame);bpy.context.view_layer.update();e=o.evaluated_get(bpy.context.evaluated_depsgraph_get());return e,e.to_mesh()
def vals(m,n):return [v.value for v in m.attributes[n].data]
def sample(o,f):
 e,m=mesh(o,f);co=[tuple(v.co) for v in m.vertices];attrs={n:vals(m,n) for n in ['wf17_component','wf17_u','wf17_strand','wf17_ring','wf17_Send head arrival','wf17_Send tail arrival','wf17_Return start','wf17_Return head arrival','wf17_Return tail arrival','wf17_Cycle frames'] if n in m.attributes};e.to_mesh_clear();return co,attrs
def signature(o,f=18):
 co,a=sample(o,f);return len(co),sum(c[2] for c in co),sum(sum(x*x for x in c) for c in co)
bpy.ops.wm.open_mainfile(filepath=str(B/'Waveform_shared_v017.blend'),load_ui=False,use_scripts=False)
s=bpy.context.scene;o=bpy.data.objects['WF_PULSE_FIELD'];c=bpy.data.objects['WF_MASTER_CONTROLS'];mod=o.modifiers[0];cm=c.modifiers[0]
check('clean library',len(bpy.data.objects)==2 and len(bpy.data.cameras)==0 and len(bpy.data.libraries)==0 and len(bpy.data.shape_keys)==0)
check('native groups',len(bpy.data.node_groups)==3)
co,a=sample(o,18);check('finite visible field',len(co)>1000 and all(math.isfinite(x) for v in co for x in v),len(co))
for n,want in [('Send head arrival',21),('Send tail arrival',41),('Return start',43),('Return head arrival',59),('Return tail arrival',79),('Cycle frames',96)]:check(n,abs(a['wf17_'+n][0]-want)<.001,a['wf17_'+n][0])
for f in [1,4,80,96]:check('quiet frame '+str(f),len(sample(o,f)[0])==0)
check('loop matches',signature(o,18)==signature(o,114))
base=signature(o)
for name,value in [('Pulse count',1),('Pulse spacing',9.),('Variation seed',7),('Spike width',.6),('Height m',.02),('Strand count',17),('Strand separation',0.),('Ribbon depth m',.006),('Strand radius m',.0002),('Show head tail',False)]:
 old=param(cm,name).value;set_input(cm,name,value);sig=signature(o);check('live shared '+name,sig!=base,{'base':base,'changed':sig});set_input(cm,name,old)
for name,value in [('Enabled',False),('Mode 0 Both 1 Send 2 Return',2),('Pulse count override',5),('Strand count override',1),('Strand separation override',.1),('Strength multiplier',.5),('Width multiplier',2.),('Radius multiplier',2.),('Show markers',False)]:
 old=param(mod,name).value;f=33 if name=='Pulse count override' else 18;before=signature(o,f);set_input(mod,name,value);check('instance '+name,signature(o,f)!=before);set_input(mod,name,old)
set_input(mod,'Reflection enabled',False);check('return disabled',len(sample(o,60)[0])==0);set_input(mod,'Reflection enabled',True)
set_input(mod,'Loop',False);check('one shot remains quiet',len(sample(o,114)[0])==0);set_input(mod,'Loop',True)
set_input(mod,'Mode 0 Both 1 Send 2 Return',2);_,a=sample(o,18);check('return-only immediate',min(a['wf17_component'])>=2 and a['wf17_Return start'][0]==5);set_input(mod,'Mode 0 Both 1 Send 2 Return',0)
s.render.fps=30;_,a=sample(o,18);check('FPS duration',abs(a['wf17_Return tail arrival'][0]-97.5)<.001,a['wf17_Return tail arrival'][0]);s.render.fps=24
set_input(mod,'Speed',2.);_,a=sample(o,18);check('speed coherently scales',abs(a['wf17_Return tail arrival'][0]-42)<.001);set_input(mod,'Speed',1.)
set_input(mod,'Fit end frame',60.);_,a=sample(o,18);check('fit exact completion',abs(a['wf17_Return tail arrival'][0]-60)<.001);set_input(mod,'Fit end frame',0.)
old=tuple(param(cm,'Outgoing color').value);set_input(cm,'Outgoing color',(.8,.2,.1,1));sample(o,18);col=tuple(bpy.data.materials['WF17 Outgoing color band16'].diffuse_color);check('color driver safe with scripts disabled',max(abs(col[i]-[.8,.2,.1][i]) for i in range(3))<.001,col);set_input(cm,'Outgoing color',old)
aa=bpy.data.objects.new('test A',None);bb=bpy.data.objects.new('test B',None);s.collection.objects.link(aa);s.collection.objects.link(bb);set_input(mod,'Use anchor objects',True);set_input(mod,'Start anchor',aa);set_input(mod,'End anchor',bb)
for end,up in [((.02,.03,.01),(0,0,1)),((0,0,.1),(0,0,1)),((.1,0,0),(1,0,0)),((.1,0,0),(0,0,0))]:
 aa.location=(0,0,0);bb.location=end;set_input(mod,'Up axis',up);co,a=sample(o,18);heads=[Vector(x) for x,k in zip(co,a['wf17_component']) if k==3];center=sum(heads,Vector())/len(heads);expected=Vector(end)*(13/16);check('anchor basis '+str(end)+str(up),(center-expected).length<1e-6 and all(math.isfinite(x) for v in co for x in v),list(center))
set_input(mod,'Use anchor objects',False);set_input(mod,'Up axis',(0,0,1));set_input(mod,'Start anchor',None);set_input(mod,'End anchor',None);bpy.data.objects.remove(aa,do_unlink=True);bpy.data.objects.remove(bb,do_unlink=True)
# Two consumers share master values but local changes stay independent.
other=o.copy();s.collection.objects.link(other);om=other.modifiers[0];set_input(om,'Strand count override',9);check('independent instance values',signature(o)==base and signature(other)!=base)
old=param(cm,'Height m').value;before=signature(other);set_input(cm,'Height m',.019);check('shared change reaches both',signature(o)!=base and signature(other)!=before);set_input(cm,'Height m',old)
set_input(om,'Use master style',False);before=signature(other);set_input(cm,'Height m',.019);check('local style isolates consumer',signature(other)==before and signature(o)!=base);set_input(cm,'Height m',old);bpy.data.objects.remove(other,do_unlink=True)
# Compare exact common route samples with approved baked proof, excluding new markers.
set_input(mod,'Route axis',(.3583680987,-.9335803986,0));set_input(mod,'Transverse axis',(-.9335803986,-.3583680987,0))
new={}
for f in [14,18,33,51,69]:
 co,a=sample(o,f);d={}
 for p,u,k,j,r in zip(co,a['wf17_u'],a['wf17_component'],a['wf17_strand'],a['wf17_ring']):
  if k in [1,2] and abs(u*16-round(u*16))<.00001:d[(k,round(u*16),round(j),round(r))]=p
 new[f]=d
bpy.ops.wm.open_mainfile(filepath=str(R/'04-Production/Shots/S01-S02/Scenes/Waveform_direction_quick_v006.blend'),load_ui=False,use_scripts=False)
errors=[];compared=0
fields=[x for x in bpy.context.scene.objects if x.type=='MESH' and any(m.name=='Finite head / tail window' for m in x.modifiers) and not x.hide_render and x.visible_get()]
check('approved proof found',len(fields)==2,[x.name for x in fields])
for f,d in new.items():
 for ob in fields:
  k=2 if 'VIOLET' in ob.name.upper() else 1;e,m=mesh(ob,f)
  if not len(m.vertices):e.to_mesh_clear();continue
  us=vals(m,'pulse_route_u');vs=vals(m,'pulse_strand_weight')
  for idx,(v,u,w) in enumerate(zip(m.vertices,us,vs)):
   key=(k,round(u*16),round((w+1)*2),idx%4)
   if abs(u*16-round(u*16))<.00001 and key in d:errors.append((v.co-Vector(d[key])).length);compared+=1
  e.to_mesh_clear()
check('approved geometry correspondence',compared>100 and max(errors)<1e-6,{'samples':compared,'max_error_m':max(errors) if errors else None})
# Linked demo is the actual packaged master, not the baked proof.
bpy.ops.wm.open_mainfile(filepath=str(R/'04-Production/Shared/Demos/Waveform_demo_v017.blend'),load_ui=False,use_scripts=False)
check('relative source link',all(x.filepath.startswith('//') and Path(bpy.path.abspath(x.filepath)).exists() for x in bpy.data.libraries),[x.filepath for x in bpy.data.libraries])
check('four independent demo cases',len(bpy.data.scenes)==4)
for name,f in [('01 Approved360',18),('03 Local variation',18),('04 Fit-end30fps',18)]:
 s=bpy.data.scenes[name];bpy.context.window.scene=s;s.frame_set(f);s.render.filepath=str(P/(name[:2]+'_frame018.png'));t=time.perf_counter();bpy.ops.render.render(write_still=True);elapsed=time.perf_counter()-t;report['renders'].append({'scene':name,'frame':f,'seconds':elapsed,'path':s.render.filepath});check('render cap '+name,elapsed<5,elapsed)
(B/'Verification_v017.json').write_text(json.dumps(report,indent=2));print('VERIFIED_V017',len(checks),max(errors))
