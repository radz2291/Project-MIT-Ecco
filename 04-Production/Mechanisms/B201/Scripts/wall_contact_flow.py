"""Editable wall-material contact response evaluated on real rock coordinates."""
import bpy
from mathutils import Vector

def build_contact_flow(wallob,controller,origin,wall,normal,step):
    ax=Vector((1,0,0));az=Vector((0,-normal.z,normal.y))
    section=wallob;mat=section.data.materials[0];n=mat.node_tree.nodes;l=mat.node_tree.links
    shader=next(x for x in n if x.bl_idname=='ShaderNodeBsdfPrincipled');geometry=next(x for x in n if x.bl_idname=='ShaderNodeNewGeometry')
    for link in list(shader.inputs['Emission Strength'].links):l.remove(link)
    def op(kind,a=None,b=None):
     node=n.new('ShaderNodeMath');node.operation=kind
     for i,v in enumerate((a,b)):
      if v is not None:
       if isinstance(v,(int,float)):node.inputs[i].default_value=v
       else:l.new(v,node.inputs[i])
     return node.outputs[0]
    def control(prop):
     node=n.new('ShaderNodeValue');node.label=prop;d=node.outputs[0].driver_add('default_value').driver;v=d.variables.new();v.name='v';v.targets[0].id=controller;v.targets[0].data_path='["'+prop+'"]';d.expression='v';return node.outputs[0]
    sub=n.new('ShaderNodeVectorMath');sub.operation='SUBTRACT';l.new(geometry.outputs['Position'],sub.inputs[0]);sub.inputs[1].default_value=wall
    for i in range(3):
     d=sub.inputs[1].driver_add('default_value',i).driver;v=d.variables.new();v.name='v';v.targets[0].id=controller;v.targets[0].data_path='location['+str(i)+']';d.expression='v'
    coords=[]
    for axis in (ax,az):
     dot=n.new('ShaderNodeVectorMath');dot.operation='DOT_PRODUCT';l.new(sub.outputs[0],dot.inputs[0]);dot.inputs[1].default_value=axis;coords.append(dot.outputs['Value'])
    x,y=coords;rx=control('scan_radius_x_m');ry=control('scan_radius_y_m');cell=control('cell_size_m')
    ellipse=op('ADD',op('POWER',op('DIVIDE',x,rx),2),op('POWER',op('DIVIDE',y,ry),2))
    # Irregular influence and two cell scales, modulated by rock relief and stable noise.
    noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=330;noise.inputs['Detail'].default_value=2.5;l.new(geometry.outputs['Position'],noise.inputs['Vector'])
    warp=op('ADD',op('MULTIPLY',noise.outputs['Fac'],.85),.55)
    mask=op('EXPONENT',op('MULTIPLY',op('POWER',op('MULTIPLY',ellipse,warp),2),-1.6))
    # Wave/rock intersection controls both the activation footprint and the bright contact band.
    rad=n.new('ShaderNodeVectorMath');rad.operation='DISTANCE';l.new(geometry.outputs['Position'],rad.inputs[0]);rad.inputs[1].default_value=origin
    signed=op('SUBTRACT',control('leading_radius_m'),rad.outputs['Value'])
    # Arrival never precedes actual intersection. Stable local variation affects only maturation.
    age=op('DIVIDE',signed,.0005)
    delay=op('MULTIPLY',noise.outputs['Fac'],1.8)
    maturity=op('MINIMUM',op('MAXIMUM',op('DIVIDE',op('SUBTRACT',age,delay),2.8),0),1)
    decay=op('EXPONENT',op('MULTIPLY',op('MAXIMUM',op('SUBTRACT',age,delay),0),-.12))
    arrived=op('MULTIPLY',maturity,decay)
    band=op('EXPONENT',op('MULTIPLY',op('POWER',op('DIVIDE',signed,control('contact_band_m')),2),-1))
    def cells(cellscale):
     gx=op('DIVIDE',x,cellscale);gy=op('DIVIDE',y,cellscale);lines=[]
     for c in (gx,gy):
      f=op('FRACT',c);near=op('MINIMUM',f,op('SUBTRACT',1,f));lines.append(op('LESS_THAN',near,.045))
     grid=op('MAXIMUM',*lines)
     seed=op('ADD',op('MULTIPLY',op('FLOOR',gx),12.9898),op('MULTIPLY',op('FLOOR',gy),78.233))
     random=op('FRACT',op('MULTIPLY',op('SINE',seed),43758.5453));active=op('GREATER_THAN',random,.47)
     brightness=op('ADD',op('MULTIPLY',random,.75),.25)
     return op('MULTIPLY',op('ADD',op('MULTIPLY',grid,.85),.07),op('MULTIPLY',active,brightness))
    coarse=cells(cell);fine=cells(op('MULTIPLY',cell,.5))
    pattern=op('ADD',coarse,op('MULTIPLY',fine,op('GREATER_THAN',noise.outputs['Fac'],.52)))
    relief=op('ADD',op('MULTIPLY',noise.outputs['Fac'],.65),.35)
    activation=op('MULTIPLY',op('MULTIPLY',pattern,arrived),relief)
    # Narrow curved luminous seam precisely where the membrane intersects the actual rock.
    combined=op('ADD',activation,op('MULTIPLY',band,.22))
    effect=op('MULTIPLY',op('MULTIPLY',mask,combined),control('scan_opacity'));effect=op('MULTIPLY',effect,control('scan_fade'))
    l.new(op('MULTIPLY',effect,3.5),shader.inputs['Emission Strength']);shader.inputs['Emission Color'].default_value=(.10,.5,1,1)
    section['effect']='Localized irregular digital acquisition patch on actual rock; illustrative, not measured data';section['contact_controller']=controller.name

    controller['flow_description']='Actual rock intersection -> varied local cell maturation -> exponential local memory; independent cells do not switch on simultaneously'
    return rad
