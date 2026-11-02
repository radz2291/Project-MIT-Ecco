from pathlib import Path
q=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/Shots/S01-S02')
code=(q/'Scripts/render_waveform_v010.py').read_text().replace('v010','v015').replace('frames=[305,497,523]+list(range(299,337))+list(range(489,529))','frames=[303,341,401]+list(range(300,444))')
exec(compile(code,str(q/'Scripts/render_waveform_v015.py'),'exec'))
