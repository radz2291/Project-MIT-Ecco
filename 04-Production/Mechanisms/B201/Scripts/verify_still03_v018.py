import bpy,json,hashlib,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from bpy_extras.object_utils import world_to_camera_view
P=Path(__file__).resolve().parents[3];E=P/'Records/Tasks/T-007/Evidence/Still_03';M=P/'Mechanisms/B201'
r=json.loads((E/'build-render_still03_v018.json').read_text());checks=[]
def check(name,value):checks.append({'check':name,'pass':bool(value)})
def snapshot():
 s=bpy.context.scene;c=s.camera;o=bpy.data.objects['T6_WALL_CONTACT_SECTION']
 return {'camera':[list(c.location),list(c.rotation_euler),c.data.lens,c.data.sensor_width],'wall':[list(v.co) for v in o.data.vertices],'pose':dict(bpy.data.objects['ASSEMBLY_CONTROL'].items()),'lights':{o.name:[list(o.location),list(o.rotation_euler),o.data.energy,list(o.data.color)] for o in s.objects if o.type=='LIGHT'}}
src=M/'Scenes/B201_wall-interaction_still03_v010.blend';bpy.ops.wm.open_mainfile(filepath=str(src));before=snapshot()
def membranes():
 result={}
 for o in bpy.context.scene.objects:
  if not o.name.startswith('OUTGOING_WAVEFRONT_ILLUSTRATION_'):continue
  nodes=[]
  for n in o.data.materials[0].node_tree.nodes:
   values=[]
   for i in n.inputs:
    if not hasattr(i,'default_value'):continue
    v=i.default_value;values.append(v if isinstance(v,(int,float,str,bool)) else list(v))
   nodes.append([n.bl_idname,getattr(n,'operation',''),values])
  result[o.name]={'mesh_sha256':hashlib.sha256(json.dumps([list(v.co) for v in o.data.vertices]).encode()).hexdigest(),'material':nodes}
 return result
bpy.ops.wm.open_mainfile(filepath=str(M/'Scenes/B201_wall-interaction_still03_v016.blend'));approved_membranes=membranes();approved_scene=snapshot()
out=P/r['scene'];bpy.ops.wm.open_mainfile(filepath=str(out));s=bpy.context.scene;after=snapshot()
check('all v016 membrane shapes and materials unchanged',membranes()==approved_membranes)
check('v016 camera composition wall pose lights unchanged',after==approved_scene)
for key in before:check('preserved '+key,before[key]==after[key])
check('parent preserved',hashlib.sha256(src.read_bytes()).hexdigest()==r['parent_scene_sha256'])
check('saved scene hash',hashlib.sha256(out.read_bytes()).hexdigest()==r['scene_sha256'])
check('render hash',hashlib.sha256((P/r['image']).read_bytes()).hexdigest()==r['image_sha256'])
for rel,h in r['inputs'].items():check('master unchanged '+rel,hashlib.sha256((P/rel).read_bytes()).hexdigest()==h)
check('relative libraries resolve',all(x.filepath.startswith('//') and Path(bpy.path.abspath(x.filepath)).is_file() for x in bpy.data.libraries))
check('one full-size still',s.frame_start==s.frame_end==1 and s.render.resolution_x==1920 and s.render.resolution_y==1080 and s.render.resolution_percentage==100)
fronts=sorted([o for o in s.objects if o.name.startswith('OUTGOING_WAVEFRONT_ILLUSTRATION_')],key=lambda o:o.name);origin=Vector(r['origin']);wall=Vector(r['wall'])
check('three thin spherical caps',len(fronts)==3 and all(len(o.modifiers)==0 and all(abs((o.matrix_world@v.co-origin).length-radius)<1e-6 for v in o.data.vertices) for o,radius in zip(fronts,r['front_radii_m'])))
check('leading membrane intersects wall at peak arrival',r['front_radii_m'][-1]>(wall-origin).length and abs(r['front_radii_m'][-1]-(wall-origin).length-.002)<1e-7)
check('membranes no refractive glass',all(not any(n.bl_idname in ('ShaderNodeBsdfGlass','ShaderNodeBsdfRefraction') for n in o.data.materials[0].node_tree.nodes) for o in fronts))
check('smooth membranes',all(all(p.use_smooth for p in o.data.polygons) for o in fronts))
check('shared contact controller',all(o['contact_controller']=='ACOUSTIC_CONTACT_CONTROLLER' for o in fronts))
control=bpy.data.objects['ACOUSTIC_CONTACT_CONTROLLER'];check('contact at recorded wall',(control.location-wall).length<1e-7)
section=bpy.data.objects['T6_WALL_CONTACT_SECTION'];check('scan evaluated on rock geometry',section['contact_controller']==control.name and len(section.modifiers)==0)
check('scan controls connected',len(section.data.materials[0].node_tree.animation_data.drivers)>=8)
for name in ('B201_PULSE_ECHO','B201_CONTACT_HISTORY','B201_SPATIAL_GRAPHICS'):check('diagnostics excluded '+name,bpy.data.collections[name].hide_render)
check('no local object motion',all(o.animation_data is None for o in s.objects if o.library is None))
check('no physical acoustic claim','illustration' in r['representation'])
approved=json.loads((E/'build-render_still03_v016.json').read_text())
check('directionally approved v016 scene preserved',hashlib.sha256((P/approved['scene']).read_bytes()).hexdigest()==approved['scene_sha256'])
check('directionally approved v016 image preserved',hashlib.sha256((P/approved['image']).read_bytes()).hexdigest()==approved['image_sha256'])
nodes=section.data.materials[0].node_tree.nodes
check('textured rock tint retained',any(n.label=='ROCK_MATERIAL_DIGITIZATION' and n.inputs[1].is_linked for n in nodes))
check('contact-driven cell maturity at both scales',sum(n.label=='CONTACT_DRIVEN_CELL_MATURITY' for n in nodes)==2)
check('rock bump and roughness retained',next(n for n in nodes if n.bl_idname=='ShaderNodeBsdfPrincipled').inputs['Normal'].is_linked and next(n for n in nodes if n.bl_idname=='ShaderNodeBsdfPrincipled').inputs['Roughness'].default_value>.9)
check('contact-to-edge falloff retained procedurally',any(n.label=='CONTACT_TO_EDGE_GRADIENT' for n in nodes))
check('larger coverage unchanged',abs(control['scan_radius_x_m']/.015-1.35)<1e-6 and abs(control['scan_radius_y_m']-.017)<1e-6)
check('fine cells restored without reducing coverage',abs(control['cell_size_m']-.0018)<1e-8)
check('editable surface acquisition growth',control['acquisition_growth']==1 and any(n.label=='acquisition_growth' for n in nodes))
points=[section.matrix_world@v.co for v in section.data.vertices];tree=BVHTree.FromPolygons(points,[list(f.vertices) for f in section.data.polygons])
normal=(wall-origin).normalized();ax=Vector((1,0,0));az=Vector((0,-normal.z,normal.y));radius=r['front_radii_m'][-1];intersections=[]
for j in range(64):
 phi=math.tau*j/64;side=ax*math.cos(phi)+az*math.sin(phi)
 def sample(theta):return tree.ray_cast(origin,normal*math.cos(theta)+side*math.sin(theta))
 lo=0;hi=.65
 if sample(lo)[0] is None or sample(hi)[0] is None:continue
 if not sample(lo)[3]<radius<sample(hi)[3]:continue
 for k in range(24):
  mid=(lo+hi)/2
  if sample(mid)[3]<radius:lo=mid
  else:hi=mid
 intersections.append(sample((lo+hi)/2)[0])
check('actual sphere-rock intersection curve sampled',len(intersections)>=48)
check('intersection lies on leading sphere',all(abs((p-origin).length-radius)<1e-6 for p in intersections))
check('contact curve visible within unchanged camera',sum(0<q.x<1 and 0<q.y<1 for q in [world_to_camera_view(s,s.camera,p) for p in intersections])>=32)
(E/'contact-correspondence_still03_v018.json').write_text(json.dumps({'intersection_points':[list(p) for p in intersections],'sphere_radius_m':radius,'first_arrival_standoff_m':(wall-origin).length,'peak_advance_m':.002,'wall_geometry_unchanged':before['wall']==after['wall'],'contact_shader':'signed = leading_radius - length(rock_position - sensor_origin); activation and seam use this same field','illustrative_not_acoustic_simulation':True},indent=2))
result={'checks':checks,'passed':all(x['pass'] for x in checks),'executor_self_check':True,'human_visual_approval':'pending','motion_authorized':False}
(E/'verification_still03_v018.json').write_text(json.dumps(result,indent=2));assert result['passed'],[x for x in checks if not x['pass']];print('VERIFY_PASS',len(checks))
