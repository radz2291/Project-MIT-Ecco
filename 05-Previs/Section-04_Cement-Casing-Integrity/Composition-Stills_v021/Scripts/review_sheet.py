from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json
B=Path(__file__).resolve().parents[1]
font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',20);small=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',16);title=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',27)
order=[('A1','A1 - Casing approach: corrected tilt'),('A2','A2 - Entering the existing casing'),('B1','B1 - Supported: larger interaction'),('C1','C1 - Reduced support: matching scale'),('B2','B2 - After contact: settled'),('C2','C2 - Same delay: retained response'),('D1','D1 - Physical surface only'),('D2','D2 - Same view with measurement graphics')]
sheet=Image.new('RGB',(1280,1664),(16,24,30));d=ImageDraw.Draw(sheet);d.text((22,14),'SECTION 4 - v021 APPROVAL STILLS',font=title,fill=(235,242,246));d.text((22,49),'A orientation | B/C 1.55x closer | Muted channel | Physical/data wear pair',font=small,fill=(175,199,210))
for i,(tag,text) in enumerate(order):
 im=Image.open(B/'Previews'/f'S04_{tag}_v021.png').convert('RGB');assert im.size==(1280,720);im.resize((640,360),Image.Resampling.LANCZOS).save(B/'Previews'/f'Thumbnail_{tag}.jpg',quality=92)
 x=i%2*640;y=80+i//2*396;sheet.paste(im.resize((640,360),Image.Resampling.LANCZOS),(x,y));d.rectangle((x,y+360,x+640,y+396),fill=(16,24,30));d.text((x+14,y+365),text,font=font,fill=(225,236,240))
sheet.save(B/'Previews/S04_approval-series_v021.jpg',quality=95)
rows=json.loads((B/'Records/stills.json').read_text());assert len(rows)==8 and all(r['seconds']<5 and r['geometry_unchanged'] for r in rows)
print('APPROVAL SHEET READY')
