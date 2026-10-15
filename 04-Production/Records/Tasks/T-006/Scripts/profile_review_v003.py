"""Readable static comparison of actual evaluated saved-wall slices."""
import json,math
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[4];TASK=ROOT/'Records/Tasks/T-006'
data=json.loads((TASK/'Evidence/profile-slices_v003.json').read_text())
im=Image.new('RGB',(1440,690),'#101823');d=ImageDraw.Draw(im)
font=lambda size:ImageFont.truetype('C:/Windows/Fonts/arial.ttf',size)
d.text((40,25),'T6 v003 / Wall profiles from the saved master',font=font(30),fill='white')
d.text((40,75),'Illustrative outward enlargement; nominal 12.25in reference. Same scale; actual saved mesh samples.',font=font(20),fill='#b9c7d5')
for i,name in enumerate(('Nominal','Irregular','Spiral')):
    cx=240+i*480;cy=350;scale=900;nom=.31115/2;tool=.304800154/2
    d.text((cx-90,145),name,font=font(26),fill='white')
    d.ellipse((cx-nom*scale,cy-nom*scale,cx+nom*scale,cy+nom*scale),outline='#748292',width=2)
    d.ellipse((cx-tool*scale,cy-tool*scale,cx+tool*scale,cy+tool*scale),fill='#465465')
    if i==0:points=[(cx+nom*scale*math.cos(a),cy+nom*scale*math.sin(a)) for a in [2*math.pi*j/96 for j in range(97)]]
    else:
        points=sorted(data[str(i)]['points_m'],key=lambda p:math.atan2(p[2],p[1]))
        points=[(cx+p[1]*scale,cy+p[2]*scale) for p in points];points.append(points[0])
    d.line(points,fill='#68cad1',width=4)
    d.text((cx-140,540),'Grey disk = ENP3 envelope',font=font(18),fill='#b9c7d5')
    d.text((cx-140,570),'Line = authored wall profile',font=font(18),fill='#68cad1')
d.text((40,635),'Sample plane X = 2.8125m in lower interval. No field measurements, acoustic result or actual MIT deployment claimed.',font=font(19),fill='#b9c7d5')
im.save(TASK/'Previews/v003/B102_profile-comparison_v003.png')
# Compact mosaics retain every frame for continuous sequence inspection.
base=TASK/'Previews/v003'
for name in ('nominal','irregular','spiral','cased','interval-transition'):
    sheets=sorted((base/name).glob('all-frames-*_v003.jpg'))
    mosaic=Image.new('RGB',(1280,600*((len(sheets)+1)//2)),'#101823')
    for j,p in enumerate(sheets):
        with Image.open(p) as sheet:mosaic.paste(sheet.resize((640,600)),((j%2)*640,(j//2)*600))
    mosaic.save(base/name/'all-frames-mosaic_v003.jpg')
