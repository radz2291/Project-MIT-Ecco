import bpy,math,json
from pathlib import Path
B=Path(__file__).resolve().parents[1];R=B.parents[2]
src=R/'05-Previs/Section-02_Measurement-History/v011/Continuation/Scenes/S01-S02_continuous_v011.blend'
p=B/'Scenes/S04_cinematic-previs_v006.blend'
bpy.ops.wm.open_mainfile(filepath=str(src),use_scripts=False,load_ui=False)
names=['light','studio_light','color_type','show_shadows','show_cavity','cavity_type','curvature_ridge_factor','curvature_valley_factor','cavity_ridge_factor','cavity_valley_factor','background_type','background_color','show_specular_highlight','studiolight_rotate_z']
sh=bpy.context.scene.display.shading
settings={n:(list(getattr(sh,n)) if n=='background_color' else getattr(sh,n)) for n in names}
view={n:getattr(bpy.context.scene.view_settings,n) for n in ['view_transform','look','exposure','gamma']}
print('S02_STYLE',json.dumps(settings),flush=True)
bpy.ops.wm.open_mainfile(filepath=str(p),use_scripts=False,load_ui=False);s=bpy.context.scene;s.render.engine='BLENDER_WORKBENCH'
for n,v in settings.items():setattr(s.display.shading,n,v)
# Material mode retains cyan explanatory effects and the distinct casing layers.
s.display.shading.color_type='MATERIAL'
for n,v in view.items():setattr(s.view_settings,n,v)
s.display.render_aa='FXAA';s.render.resolution_x=1280;s.render.resolution_y=720
def smooth(t):
 t=max(0,min(1,t));return t*t*t*(10+t*(-15+6*t))
def color_mat(name,color):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);return m
static={};animated=[]
for o in list(s.objects):
 if o.name=='Section 2 retained opposite ground':o.hide_render=True;o.hide_viewport=True;continue
 if o.type not in ['MESH','CURVE','FONT']:continue
 if o.hide_render and not (o.get('shared_package')=='Acoustics' or 'Stationary organic fluid' in o.name or o.animation_data):continue
 issteel=o.name.startswith('Steel -');iscement=o.name.startswith('Cement ');isground=o.name.startswith('Section 2 ')
 if issteel or iscement or isground:
  o.data=o.data.copy();o.data.materials.clear();o['geometry_policy']='Workbench preview copy; vertex coordinates/topology unchanged; face material alpha only'
  base=(.26,.32,.36) if issteel else ((.48,.39,.26) if iscement else (.42,.28,.15))
  groups={}
  for poly in o.data.polygons:
   point=o.matrix_world@poly.center;a=math.atan2(point.z,point.y)
   inx=-2.85<point.x<110
   if not inx or a<(-1.48 if isground else -1.4):key='solid'
   elif isground:key='hidden' if a<1.48 else 'solid'
   else:key=round(a/.06)*.06 if a<1.2 else 'solid'
   if key not in groups:
    m=color_mat('WB '+o.name+' '+str(key),base);groups[key]=len(o.data.materials);o.data.materials.append(m)
    if key=='hidden':m.diffuse_color=(*base,0)
    elif key!='solid':animated.append((m,float(key),issteel,base))
   poly.material_index=groups[key]
  for slot in o.material_slots:slot.link='DATA'
 elif o.name.startswith('MUD_'):
  o.hide_render=True;o.hide_viewport=True
 elif 'Stationary organic fluid' in o.name:
  m=color_mat('WB restrained cyan fluid',(.06,.43,.55));m.diffuse_color=(.06,.43,.55,.50)
  for slot in o.material_slots:slot.link='OBJECT';slot.material=m
 else:
  for slot in o.material_slots:
   if not slot.material:continue
   old=slot.material;copy=old.copy();copy.name='WB '+old.name
   if old.node_tree:
    em=next((n for n in old.node_tree.nodes if n.type=='EMISSION'),None)
    if em:copy.diffuse_color=tuple(em.inputs[0].default_value)
   slot.link='OBJECT';slot.material=copy
   if o.get('shared_package')=='Acoustics':
    fc=copy.driver_add('diffuse_color',3);d=fc.driver;d.expression='alpha';v=d.variables.new();v.name='alpha';v.targets[0].id=o;v.targets[0].data_path='color[3]'
   if 'surface - reference' in o.name or 'wear - source mesh section' in o.name:
    for f in range(1,433):copy.diffuse_color[3]=smooth(((f-1)/24-15.7)/.9);copy.keyframe_insert('diffuse_color',frame=f)
for f in range(1,433):
 t=(f-1)/24;high=.23+.9*(smooth((t-1.4)/1.)-smooth((t-8.7)/.7));strength=1-smooth((t-16.4)/.7)
 for m,a,steel,base in animated:
  cut=smooth((high-a+.04)/.08)
  m.diffuse_color=(*base,1-cut*(strength if steel else 1));m.keyframe_insert('diffuse_color',frame=f)
s.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(p))
(B/'Records/preview-style.json').write_text(json.dumps(dict(source=str(src),source_settings=settings,view_settings=view,engine=s.render.engine,output_resolution=[1280,720],adaptation='Same studio preview look; shader cutaways baked to preview-only face materials with animated alpha. Geometry coordinates unchanged; material colors preserve cyan fluid/effects.'),indent=2))
