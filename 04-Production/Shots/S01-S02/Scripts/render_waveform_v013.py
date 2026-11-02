from pathlib import Path
q=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/Shots/S01-S02')
code=(q/'Scripts/render_waveform_v010.py').read_text().replace('v010','v013').replace('frames=[305,497,523]+list(range(299,337))+list(range(489,529))','frames=[310,332,570]+list(range(299,397))+list(range(539,589))')
exec(compile(code,str(q/'Scripts/render_waveform_v013.py'),'exec'))
