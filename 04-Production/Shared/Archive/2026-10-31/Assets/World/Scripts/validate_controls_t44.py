import bpy,sys,json,runpy,math
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[4];TASK=ROOT/'04-Production/Records/Tasks/T-044';ASSET=ROOT/'04-Production/Shared/Assets'
sys.path.insert(0,str(HERE));from world_controls import create_world
sys.argv=['script','--','noop'];b=runpy.run_path(str(HERE/'build_world_t44.py'))
s=b['clean']();b['settings'](s);s['consumer']='Controls';root,ctrl,instances=create_world(ASSET)
results=[]
def check(name,ok):results.append(dict(name=name,passed=bool(ok)))
for cut in [0,1]:
 for v in [0,1,2]:
  ctrl['variant']=v;ctrl['cutaway']=cut;ctrl.update_tag();bpy.context.view_layer.update()
  selected=[n for n,o in instances.items() if any(q in n for q in ['NOMINAL','IRREGULAR','SPIRAL']) and not o.hide_render]
  check('one wall variant '+str((cut,v)),selected==['WORLD_'+['NOMINAL','IRREGULAR','SPIRAL'][v]+('_CUTAWAY' if cut else '_FULL')])
for prop in ['show_hardware','show_open','show_casing','show_cement','show_formation','show_shoe','show_mud']:
 ctrl[prop]=0;ctrl.update_tag();bpy.context.view_layer.update()
 check('toggle '+prop,not any(not o.hide_render for n,o in instances.items() if {'show_hardware':'HARDWARE','show_open':['NOMINAL','IRREGULAR','SPIRAL'],'show_casing':'CASING','show_cement':'CEMENT','show_formation':'FORMATION','show_shoe':'SHOE','show_mud':'MUD'}[prop] in n) if prop!='show_open' else all(o.hide_render for n,o in instances.items() if any(t in n for t in ['NOMINAL','IRREGULAR','SPIRAL'])))
 ctrl[prop]=1
for f,v,cut,t,r in [(1,1,1,.5,.4),(40,0,1,.3,1.0),(80,2,1,0.,1.8),(120,2,0,-.4,2.4)]:
 for k,value in [('variant',v),('cutaway',cut),('travel_m',t),('rotation_rad',r)]:ctrl[k]=value;ctrl.keyframe_insert(data_path='["'+k+'"]',frame=f)
s.frame_start=1;s.frame_end=120;s.frame_set(1);ctrl.update_tag();bpy.context.view_layer.update()
c=next(c for c in s.collection.children if c.name=='LOCAL_WORLD_INSTANCES')
b['light']('CONTROL_KEY',(1,-2,2),(1,0,0),220,3,c,(.7,.85,1));b['light']('CONTROL_RIM',(3,.5,1),(1,0,0),100,2,c,(1,.7,.4))
from mathutils import Vector
d=bpy.data.cameras.new('CONTROLS_CAMERA');cam=bpy.data.objects.new(d.name,d);c.objects.link(cam);cam.location=(3.6,-5,2.5);cam.rotation_euler=(Vector((1.15,0,0))-cam.location).to_track_quat('-Z','Y').to_euler();d.lens=46;s.camera=cam
b['save'](TASK/'ReuseTests/Controls_stress_v001.blend')
p=TASK/'Evidence/controls-verification_v001.json';p.write_text(json.dumps(dict(checks=results,all_pass=all(x['passed'] for x in results)),indent=2),encoding='utf-8');print('CONTROLS',len(results),all(x['passed'] for x in results),flush=True)
