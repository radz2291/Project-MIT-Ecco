from pathlib import Path
q=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/Shots/S01-S02')
code=(q/'Scripts/render_waveform_v010.py').read_text().replace('v010','v011').replace('frames=[305,497,523]+list(range(299,337))+list(range(489,529))','frames=[313,350]+list(range(299,396))')
exec(compile(code,str(q/'Scripts/render_waveform_v011.py'),'exec'))
