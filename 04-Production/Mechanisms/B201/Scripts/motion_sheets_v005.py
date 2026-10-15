from pathlib import Path
from PIL import Image,ImageDraw
p=Path('04-Production/Mechanisms/B201/Previews/Frames/v005');out=p.parents[1]
for page in range(8):
 im=Image.new('RGB',(1280,1080))
 for k in range(54):
  f=page*54+k+1;t=Image.open(p/f'review_{f:04}.png').resize((213,120));ImageDraw.Draw(t).text((3,3),str(f),fill='orange');im.paste(t,((k%6)*213,(k//6)*120))
 im.save(out/f'B201_all-frames_{page+1}_v005.jpg',quality=90)
print('8 ordered motion sheets generated')
