"""Versioned flat lead/tail controls; zero defaults preserve v017 behavior."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).parent))
import pulse_graph
pulse_graph.STYLE=pulse_graph.STYLE+[
 ('Lead rest frames','NodeSocketFloat',0.,0.,40.,'Pulse train'),
 ('Flat after age','NodeSocketFloat',0.,0.,40.,'Pulse shape')]
code=(Path(__file__).parent/'build_pulse_v017.py').read_text().replace('v017','v018')
code=code.replace("op('ADD',last,p['Tail allowance'])","op('ADD',op('ADD',last,p['Lead rest frames']),p['Tail allowance'])")
code=code.replace("op('SUBTRACT',age,offsets[j])","op('SUBTRACT',op('SUBTRACT',age,offsets[j]),p['Lead rest frames'])")
code=code.replace("signal=op('ADD',signal,op('MULTIPLY'", "wave=g.switch(op('MULTIPLY',op('GREATER_THAN',p['Flat after age'],0),op('GREATER_THAN',agej,p['Flat after age'])),0,wave);tail=g.switch(op('GREATER_THAN',p['Flat after age'],0),0,tail)\n  signal=op('ADD',signal,op('MULTIPLY'")
exec(compile(code,str(Path(__file__)),'exec'))
import json
interface=Path(__file__).parent.parent/'Waveform_interface_v018.json'
data=json.loads(interface.read_text());data['consumers']=['Shots/S01-S02/Scenes/S01-S02_production_v013.blend'];data['extension']='Lead rest frames and Flat after age; zero defaults preserve v017';interface.write_text(json.dumps(data,indent=2))
