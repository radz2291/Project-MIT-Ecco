"""Optional persistent handshake beam, with separately traveling message pulses."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import pulse_graph
pulse_graph.TIMING=pulse_graph.TIMING+[
 ('Beam mode','NodeSocketBool',False,None,None),
 ('Beam opening frames','NodeSocketFloat',1.,.1,20.),
 ('Beam setup frames','NodeSocketFloat',3.,1.,40.),
 ('Beam closing frames','NodeSocketFloat',1.,.1,20.)]
exec((Path(__file__).parent/'build_pulse_v018.py').read_text().split('exec(compile(code')[0])
code=code.replace('v018','v019')
code=code.replace("end=tim.switch(reflect,RT,ST);base_speed", "end=tim.switch(reflect,RT,ST);end=op('ADD',end,tim.switch(ti['Beam mode'],op('ADD',ti['Beam setup frames'],ti['Beam closing frames']),0));base_speed")
code=code.replace("values[name]=op('ADD',ti['Start frame'],op('DIVIDE',value,speed))", "values[name]=op('ADD',ti['Start frame'],op('DIVIDE',op('ADD',value,tim.switch(ti['Beam mode'],ti['Beam setup frames'],0)),speed))")
code=code.replace("t=tn.outputs['Time'];RO=", "t=op('SUBTRACT',tn.outputs['Time'],g.switch(local['Beam mode'],local['Beam setup frames'],0));RO=")
needle=" geo=g.delete(g.i.outputs['Geometry'],op('SUBTRACT',1,active))"
insert=""" # Persistent beam is separate from the traveling pulse envelope.
 raw=tn.outputs['Time'];setup=local['Beam setup frames'];beamend=op('ADD',setup,g.switch(local['Reflection enabled'],op('ADD',op('ADD',RO,TR),DR),op('ADD',T,D)))
 length=op('MULTIPLY',g.clamp(op('DIVIDE',raw,local['Beam opening frames'])),g.clamp(op('DIVIDE',op('SUBTRACT',op('ADD',beamend,local['Beam closing frames']),raw),local['Beam closing frames'])))
 return_phase=op('GREATER_THAN',raw,op('SUBTRACT',op('ADD',setup,RO),.000001))
 phase=return_phase if reverse else op('SUBTRACT',1,return_phase)
 beamactive=op('MULTIPLY',enabled,op('MULTIPLY',phase,op('MULTIPLY',op('LESS_THAN',index,N),op('MULTIPLY',op('GREATER_THAN',length,0),op('LESS_THAN',u,op('ADD',length,.000001))))))
 active=g.switch(local['Beam mode'],beamactive,active)
"""
assert needle in code;code=code.replace(needle,insert+needle)
needle=" signal=0\n"
code=code.replace(needle," pulse_edge=edge;edge=g.switch(local['Beam mode'],1,edge)\n"+needle)
code=code.replace(" envelope=op('ADD',p['End height fraction']", " signal=op('MULTIPLY',signal,g.switch(local['Beam mode'],pulse_edge,1))\n envelope=op('ADD',p['End height fraction']")
code=code.replace("show=op('MULTIPLY',stage_active,", "show=op('MULTIPLY',g.switch(local['Beam mode'],0,stage_active),")
exec(compile(code,str(Path(__file__)),'exec'))
import json
interface=Path(__file__).parent.parent/'Waveform_interface_v019.json';data=json.loads(interface.read_text());data['consumers']=['Shots/S01-S02/Scenes/S01-S02_production_v014.blend'];data['extension']='Optional persistent handshake beam, separate message pulses and feedback color';interface.write_text(json.dumps(data,indent=2))
