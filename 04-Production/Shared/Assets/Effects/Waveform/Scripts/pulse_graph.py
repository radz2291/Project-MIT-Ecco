"""Small native Geometry Nodes construction helpers; build-time only."""
import bpy
class Graph:
 def __init__(self,name,geometry=True):
  self.g=bpy.data.node_groups.new(name,'GeometryNodeTree');self.g.is_modifier=geometry;self.i=self.node('NodeGroupInput');self.o=self.node('NodeGroupOutput');self.panels={}
  if geometry:self.input('Geometry','NodeSocketGeometry',None);self.output('Geometry','NodeSocketGeometry')
 def panel(self,name,closed=False):
  if name not in self.panels:self.panels[name]=self.g.interface.new_panel(name,default_closed=closed)
  return self.panels[name]
 def input(self,name,typ='NodeSocketFloat',default=0,lo=None,hi=None,panel=None,description=''):
  x=self.g.interface.new_socket(name=name,in_out='INPUT',socket_type=typ,parent=panel);x.description=description
  if default is not None:x.default_value=default
  if lo is not None and hasattr(x,'min_value'):x.min_value=lo
  if hi is not None and hasattr(x,'max_value'):x.max_value=hi
  return self.i.outputs[name]
 def output(self,name,typ='NodeSocketFloat'):self.g.interface.new_socket(name=name,in_out='OUTPUT',socket_type=typ);return self.o.inputs[name]
 def node(self,typ):return self.g.nodes.new(typ)
 def link(self,a,b):self.g.links.new(a,b)
 def set(self,a,b):
  if hasattr(a,'bl_idname'):self.link(a,b)
  else:b.default_value=a
 def op(self,kind,a,b=None):
  n=self.node('ShaderNodeMath');n.operation=kind;self.set(a,n.inputs[0])
  if b is not None:self.set(b,n.inputs[1])
  return n.outputs[0]
 def vec(self,x,y,z):
  n=self.node('ShaderNodeCombineXYZ')
  for j,v in enumerate([x,y,z]):self.set(v,n.inputs[j])
  return n.outputs[0]
 def vop(self,kind,a,b=None):
  n=self.node('ShaderNodeVectorMath');n.operation=kind;self.set(a,n.inputs[0])
  if b is not None:self.set(b,n.inputs[3] if kind=='SCALE' else n.inputs[1])
  return n.outputs['Value'] if kind in ['LENGTH','DOT_PRODUCT','DISTANCE'] else n.outputs['Vector']
 def switch(self,test,yes,no,typ='FLOAT'):
  n=self.node('GeometryNodeSwitch');n.input_type=typ;self.set(test,n.inputs['Switch'])
  if yes is not None:self.set(yes,n.inputs['True'])
  if no is not None:self.set(no,n.inputs['False'])
  return n.outputs[0]
 def attr(self,name,typ='FLOAT'):
  n=self.node('GeometryNodeInputNamedAttribute');n.data_type=typ;n.inputs['Name'].default_value=name;return n.outputs['Attribute']
 def store(self,geo,name,value,typ='FLOAT'):
  n=self.node('GeometryNodeStoreNamedAttribute');n.data_type=typ;n.domain='POINT';self.link(geo,n.inputs['Geometry']);n.inputs['Name'].default_value=name;self.set(value,n.inputs['Value']);return n.outputs['Geometry']
 def sample(self,obj,name):
  info=self.node('GeometryNodeObjectInfo');info.inputs['Object'].default_value=obj;info.transform_space='ORIGINAL';sample=self.node('GeometryNodeSampleIndex');sample.data_type='FLOAT';sample.domain='POINT';sample.inputs['Index'].default_value=0;self.link(info.outputs['Geometry'],sample.inputs['Geometry']);self.link(self.attr('wf17_'+name),sample.inputs['Value']);return sample.outputs['Value']
 def clamp(self,x):return self.op('MINIMUM',self.op('MAXIMUM',x,0),1)
 def delete(self,geo,selection):
  n=self.node('GeometryNodeDeleteGeometry');n.domain='POINT';n.mode='ALL';self.link(geo,n.inputs['Geometry']);self.link(selection,n.inputs['Selection']);return n.outputs['Geometry']

def socket(group,name):return next(x for x in group.interface.items_tree if getattr(x,'in_out','')=='INPUT' and x.name==name)
def param(mod,name):return getattr(mod.properties.inputs,socket(mod.node_group,name).identifier)
def set_input(mod,name,value):param(mod,name).value=value;mod.id_data.update_tag(refresh={'OBJECT','DATA','TIME'})

STYLE=[
 ('Pulse count','NodeSocketInt',3,1,5,'Pulse train'),('Pulse spacing','NodeSocketFloat',6.4,.5,60.,'Pulse train'),('Spacing variation','NodeSocketFloat',.2,0.,5.,'Pulse train'),('Amplitude variation','NodeSocketFloat',.25,0.,.8,'Pulse train'),('Width variation','NodeSocketFloat',.13,0.,.5,'Pulse train'),('Variation seed','NodeSocketInt',0,0,100,'Pulse train'),('Tail allowance','NodeSocketFloat',7.2,2.,40.,'Pulse train'),
 ('Pulse width','NodeSocketFloat',1.,.25,4.,'Pulse shape'),('Pre dip','NodeSocketFloat',.16,0.,1.,'Pulse shape'),('Spike width','NodeSocketFloat',.27,.1,2.,'Pulse shape'),('Undershoot','NodeSocketFloat',.45,0.,1.,'Pulse shape'),('Rebound','NodeSocketFloat',.18,0.,1.,'Pulse shape'),('Ringing','NodeSocketFloat',.08,0.,.5,'Pulse shape'),('Ring period','NodeSocketFloat',2.4,.5,12.,'Pulse shape'),('Ring decay','NodeSocketFloat',2.4,.2,20.,'Pulse shape'),('Dispersion','NodeSocketFloat',.12,0.,1.,'Pulse shape'),('Attenuation','NodeSocketFloat',.25,0.,3.,'Pulse shape'),
 ('Height m','NodeSocketFloat',.011,.0001,.2,'Strands and size'),('Ribbon depth m','NodeSocketFloat',.003,0.,.1,'Strands and size'),('Strand count','NodeSocketInt',5,1,17,'Strands and size'),('Strand separation','NodeSocketFloat',.65,0.,.9,'Strands and size'),('Strand phase offset','NodeSocketFloat',.10,0.,1.,'Strands and size'),('Strand radius m','NodeSocketFloat',.00008,.000005,.002,'Strands and size'),('End height fraction','NodeSocketFloat',.35,0.,1.,'Strands and size'),('Head fade','NodeSocketFloat',.8,.05,8.,'Strands and size'),('Tail fade','NodeSocketFloat',1.2,.05,8.,'Strands and size'),
 ('Echo strength','NodeSocketFloat',.75,0.,1.,'Reflection and markers'),('Show head tail','NodeSocketBool',True,None,None,'Reflection and markers'),('Head radius m','NodeSocketFloat',.00035,.00001,.01,'Reflection and markers'),('Tail radius m','NodeSocketFloat',.0002,.00001,.01,'Reflection and markers'),('Reference FPS','NodeSocketFloat',24.,1.,120.,'Pulse train')]
COLORS=[('Outgoing color',(.02,.85,1.,1.)),('Reflected color',(.75,.22,1.,1.))]
TIMING=[('Enabled','NodeSocketBool',True,None,None),('Mode 0 Both 1 Send 2 Return','NodeSocketInt',0,0,2),('Start frame','NodeSocketFloat',5.,-100000.,100000.),('Travel frames','NodeSocketFloat',16.,.1,1000.),('Train duration override','NodeSocketFloat',0.,0.,1000.),('Reflection enabled','NodeSocketBool',True,None,None),('Reflection after tail','NodeSocketBool',True,None,None),('Reflection delay','NodeSocketFloat',2.,0.,1000.),('Return travel override','NodeSocketFloat',0.,0.,1000.),('Return train scale','NodeSocketFloat',1.,.1,4.),('Flip reflected pulse','NodeSocketBool',False,None,None),('Speed','NodeSocketFloat',1.,.05,8.),('Fit end frame','NodeSocketFloat',0.,0.,100000.),('Follow scene FPS','NodeSocketBool',True,None,None),('Loop','NodeSocketBool',True,None,None),('Loop quiet frames','NodeSocketFloat',22.,0.,1000.),('Loop period override','NodeSocketFloat',0.,0.,10000.)]
