import sys
sys.dont_write_bytecode=True
import bpy,ast,json,hashlib,importlib.util,runpy,contextlib,io
from pathlib import Path
R=next(p for p in Path(__file__).resolve().parents if (p/'04-Production').is_dir());A=R/'04-Production/Shared/Assets';B=R/'04-Production/Records/Tasks/T-051/Reorganization';out={}
def mod(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def fresh():bpy.ops.wm.read_factory_settings(use_empty=True)
def libs():
 result=[{'path':l.filepath,'exists':Path(bpy.path.abspath(l.filepath)).is_file()} for l in bpy.data.libraries];assert all(l['exists'] for l in result);return result
paths=[A/'Environment/Borehole/World_environment_v010.blend',A/'Environment/Borehole/Dependencies/CasedHole_v002.blend',A/'Effects/Hydraulics/Hydraulics_v003.blend'];before={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
fresh();w=mod('world_interface_current',A/'Environment/Borehole/Scripts/world_interface_v010.py');matrix=w.s02_placement(A);assert len(matrix)==4;obj=w.link_variant(A,'WORLD_S02_PHYSICAL_CUTAWAY',placement=matrix);assert obj.instance_collection;out['world_v010']={'placement_shape':[len(matrix),len(matrix[0])],'collection':obj.instance_collection.name,'libraries':libs()}
c=mod('compatibility_current',A/'Environment/Borehole/Scripts/compatibility_v001.py');assert abs(c.radial_clearance(.2,.3)-.05)<1e-12
try:c.radial_clearance(-1,.3);raise AssertionError('Invalid diameter accepted')
except ValueError:pass
out['compatibility']={'finite_clearance_pass':True,'invalid_diameter_rejected':True}
fresh();c=mod('cased_current',A/'Environment/Borehole/Scripts/cased_controls_v001.py');ctrl,instances=c.create_cased(A);before_visible=sum(not o.hide_render for o in instances.values());ctrl['show_steel']=0;ctrl['show_cement']=0;ctrl['show_channel']=0;ctrl['show_reference']=0;ctrl.update_tag();bpy.context.scene.frame_set(2);bpy.context.view_layer.update();after_visible=sum(not o.hide_render for o in instances.values());assert before_visible>0 and after_visible==0;out['cased_v002']={'instances':len(instances),'visible_before':before_visible,'visible_all_off':after_visible,'libraries':libs()}
fresh();h=mod('hydraulics_current',A/'Effects/Hydraulics/Scripts/hydraulics_controls_v001.py');root,ctrl,wrappers=h.create_flow(paths[2]);before_visible=sum(not o.hide_render for o in wrappers);ctrl['operating_mode']=1;ctrl.update_tag();bpy.context.scene.frame_set(2);bpy.context.view_layer.update();after_visible=sum(not o.hide_render for o in wrappers);out['hydraulics_v003']={'wrappers':len(wrappers),'visible_before':before_visible,'visible_mode_off':after_visible,'libraries':libs()};assert before_visible>after_visible
p=A/'Effects/DigitalEnvironment/Scripts/regenerate_context_lines.py';ast.parse(p.read_text());saved_argv=sys.argv[:];sys.argv=[str(p),'--','--help'];buf=io.StringIO()
try:
 with contextlib.redirect_stdout(buf):runpy.run_path(str(p),run_name='__main__')
except SystemExit as e:assert e.code==0
finally:sys.argv=saved_argv
out['digital_regenerator']={'ast_valid':True,'help_exit_zero':True,'required_cli_options_present':all(x in buf.getvalue() for x in ['--consumer-source','--consumer-output','--shared-output','--evidence-output'])}
after={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths};assert before==after;out['native_files_unchanged']=True;out['scope']='Temporary empty sessions only; no saves, renders, archive APIs, or regeneration builds.'
(B/'current-runtime-verification.json').write_text(json.dumps(out,indent=2));print('CURRENT_RUNTIME_SMOKE_PASS',list(out))
