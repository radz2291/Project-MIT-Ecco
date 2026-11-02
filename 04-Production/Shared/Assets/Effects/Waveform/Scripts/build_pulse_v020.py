"""Optional live amplitude breathing, independent of beam/pulse travel."""
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import pulse_graph
pulse_graph.TIMING=pulse_graph.TIMING+[
 ('Amplitude breath','NodeSocketFloat',0.,0.,.8),
 ('Breath period frames','NodeSocketFloat',48.,4.,240.)]
exec((Path(__file__).parent/'build_pulse_v019.py').read_text().rsplit('exec(compile(code',1)[0])
code=code.replace('v019','v020')
code=code.replace("op('SUBTRACT',op('ADD',setup,RO),.000001)","op('SUBTRACT',op('ADD',setup,RO),.0001)")
needle=" envelope=op('ADD',p['End height fraction']"
code=code.replace(needle," signal=op('MULTIPLY',signal,op('ADD',1,op('MULTIPLY',local['Amplitude breath'],op('SINE',op('DIVIDE',op('MULTIPLY',6.283185307179586,stage),local['Breath period frames'])))))\n"+needle)
exec(compile(code,str(Path(__file__)),'exec'))
interface=Path(__file__).parent.parent/'Waveform_interface_v020.json';data=json.loads(interface.read_text());data['consumers']=['Shots/S01-S02/Scenes/S01-S02_production_v015.blend'];data['extension']='Optional live amplitude breathing on persistent beam';interface.write_text(json.dumps(data,indent=2))
