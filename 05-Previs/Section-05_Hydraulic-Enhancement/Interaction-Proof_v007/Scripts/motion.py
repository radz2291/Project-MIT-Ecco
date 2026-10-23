"""Independent curvilinear density advection inside a real annular domain."""
import bpy,math,json,time
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
B=Path(__file__).resolve().parents[1];s=bpy.context.scene;s.frame_set(1);bpy.context.view_layer.update();vv=[];ff=[]
for o in bpy.data.collections['S05_LINKED_HARDWARE'].objects:
 off=len(vv);vv.extend(o.matrix_world@v.co for v in o.data.vertices);ff.extend([[off+i for i in p.vertices] for p in o.data.polygons])
tree=BVHTree.FromPolygons(vv,ff);R=.155575;OMEGA=-math.radians(5)
routes=json.loads((B.parent/'Interaction-Proof_v004/Records/planned-routes.json').read_text())
ns=dict(bpy=bpy,math=math,Vector=Vector,tree=tree,R=R,OMEGA=OMEGA,routes=routes)
src=(B.parent/'Interaction-Proof_v006/Scripts/build.py').read_text();exec(src[src.index('def linear('):src.index("fx=bpy.data.collections.new")],ns)
linear=ns['linear'];frame_at=ns['frame_at']
domain=bpy.data.objects['S05_v007_AnnularFluidDomain'];domain.animation_data_clear()
for f in [1,72]:domain.rotation_euler.z=OMEGA*(f-1)/24;domain.keyframe_insert('rotation_euler',frame=f)
linear(domain);domain['boundary_only']='Rotating inner exclusion follows the solid. The outer cylinder is invariant. Fluid density advection and cutting transport are independent world-space fields; domain rotation is not fluid rotation.'
m=bpy.data.materials['S05_v007_SectionedFluid'];n=m.node_tree.nodes;l=m.node_tree.links;vol=next(q for q in n if q.type=='PRINCIPLED_VOLUME')
coord=n.new('ShaderNodeNewGeometry');sep=n.new('ShaderNodeSeparateXYZ');l.new(coord.outputs['Position'],sep.inputs[0])
zmap=n.new('ShaderNodeMapRange');zmap.inputs['From Min'].default_value=-.3;zmap.inputs['From Max'].default_value=1.;l.new(sep.outputs['Z'],zmap.inputs['Value'])
curve=n.new('ShaderNodeFloatCurve');curve.name='Geometry_derived_turn_angle';curve.mapping.initialize();cv=curve.mapping.curves[0];cv.points[0].location=(0,routes[2][0]/math.tau);cv.points[-1].location=(1,routes[2][-1]/math.tau)
for i in range(5,130,5):cv.points.new(i/130,routes[2][i]/math.tau)
for p in cv.points:p.handle_type='VECTOR'
curve.mapping.update();l.new(zmap.outputs['Result'],curve.inputs['Value'])
angle=n.new('ShaderNodeMath');angle.operation='MULTIPLY';angle.inputs[1].default_value=math.tau;l.new(curve.outputs['Value'],angle.inputs[0])
spin=n.new('ShaderNodeMath');spin.operation='ADD';l.new(angle.outputs[0],spin.inputs[0])
for f in [1,72]:spin.inputs[1].default_value=OMEGA*.60*(f-1)/24;spin.inputs[1].keyframe_insert('default_value',frame=f)
rotate=n.new('ShaderNodeVectorRotate');rotate.rotation_type='Z_AXIS';rotate.invert=True;l.new(coord.outputs['Position'],rotate.inputs['Vector']);l.new(spin.outputs[0],rotate.inputs['Angle'])
shift=n.new('ShaderNodeVectorMath');shift.operation='SUBTRACT';l.new(rotate.outputs[0],shift.inputs[0])
for f in [1,72]:shift.inputs[1].default_value=(0,0,.20*(f-1)/24);shift.inputs[1].keyframe_insert('default_value',frame=f)
scale=n.new('ShaderNodeVectorMath');scale.operation='MULTIPLY';scale.inputs[1].default_value=(55,55,22);l.new(shift.outputs[0],scale.inputs[0])
noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=1;noise.inputs['Detail'].default_value=1.5;noise.inputs['Roughness'].default_value=.45;l.new(scale.outputs[0],noise.inputs['Vector'])
density=n.new('ShaderNodeMapRange');density.inputs['From Min'].default_value=.25;density.inputs['From Max'].default_value=.75;density.inputs['To Min'].default_value=.6;density.inputs['To Max'].default_value=10;l.new(noise.outputs['Fac'],density.inputs['Value']);l.new(density.outputs['Result'],vol.inputs['Density']);linear(m.node_tree)
# A few physical fragments use the retained geometry-aware path; no glowing tracers.
tracks=[]
for i,z36 in enumerate([.015,.205,.445]):
 rock=bpy.data.objects[f'S05_v007_SuspendedCutting_{i:02}'];rock.animation_data_clear();heads=[]
 for f in range(1,73):
  t=(f-1)/24;z=z36+.20*(t-35/24);p,u,v,rr,rt=frame_at(z,t);rock.location=p;rock.rotation_euler=(i*.7+.34*t,.4+i+.22*t,.3-.28*t);rock.scale=(1,1,1)
  for prop in ['location','rotation_euler','scale']:rock.keyframe_insert(prop,frame=f)
  heads.append(list(p))
 linear(rock);tracks.append({'name':rock.name,'max_support_radius_m':max(v.co.length for v in rock.data.vertices),'heads':heads})
s.frame_end=72;s.render.fps=24;s['proof_scope']='v007 three-second representation test: full annular fluid, independent curving density advection, three carried matte rocks; not CFD'
s.frame_set(36);s.render.filepath=str(B/'Previews/fluid-treatment_still.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t
result={'static_review':'Agent observed distinct silver steel, continuous amber annulus, grey borehole boundary and three matte fragments. This permits the owner-requested short motion test, not owner acceptance.','static_seconds':dt,'frames':72,'fps':24,'density_field':'World-space upward advection, angular shear from v004 route 2, 60 percent illustrative angular entrainment; not CFD or physical density values','upward_illustrative_speed_m_s':.20,'cuttings':tracks,'camera_unchanged':True,'no_additional_tracer_objects':True}
(B/'Records/motion-build.json').write_text(json.dumps(result,indent=2));bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
