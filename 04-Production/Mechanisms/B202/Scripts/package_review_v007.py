from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
BASE=Path(__file__).resolve().parents[1];out=BASE/'Previews/Stills_v007'
font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',23)
small=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',18)
sheet=Image.new('RGB',(1280,1254),(15,20,26));draw=ImageDraw.Draw(sheet)
draw.text((24,14),'B202-S / The Measured Envelope / v007 — for review',font=font,fill=(232,237,243))
labels={'A':'Circumference / wall-registered samples','B':'Reconstructed geometry through depth','C':'White nominal / blue enlargement','D':'Red tight-spot illustration / centered fit','E':'Spiral geometry / cause unspecified','F':'Echo amplitude / separate illustrative channel'}
for i,(key,label) in enumerate(labels.items()):
    x=(i%2)*640;y=60+(i//2)*392
    image=Image.open(out/f'B202_{key}_v007.png').convert('RGB');image.thumbnail((640,360));sheet.paste(image,(x,y));draw.text((x+16,y+364),f'{key} — {label}',font=small,fill=(217,225,235))
draw.text((24,1230),'D1 concept accepted. Exact v007 stills pending Radzi review. Illustrative data; no animation or engineering approval.',font=small,fill=(170,186,202))
sheet.save(out/'B202_review-sheet_v007.jpg',quality=93)
print(out/'B202_review-sheet_v007.jpg')
