from PIL import Image,ImageDraw
from pathlib import Path
T=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/Records/Tasks/T-056');sheet=Image.new('RGB',(1280,792),(18,20,25));d=ImageDraw.Draw(sheet)
for i,f in enumerate(range(6,97,6)):
 im=Image.open(T/f'Previews/Ribbon_v013/Context/frame_{f:04d}.png').convert('RGB').resize((320,180));x=(i%4)*320;y=(i//4)*198;sheet.paste(im,(x,y));d.text((x+8,y+182),f'Frame {f:02d} | {(f-1)/24:.2f} s',fill=(230,235,240))
sheet.save(T/'Previews/field_sequence_v013.png')
