from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import hashlib,json,shutil
B=Path(__file__).resolve().parents[1];font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',24);small=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',18)
panels=[('A','BOREHOLE / RECONSTRUCTION','Physical context; data surface begins opening.'),('B','UNFOLDING / VISUALIZATION','The same geometry opens; amplitude remains separate.'),('C','LAPTOP / ENGINEERING OUTPUT','Recreated report, close on the laptop screen.')]
strip=Image.new('RGB',(3840,820),(10,18,25));draw=ImageDraw.Draw(strip)
for i,(letter,title,desc) in enumerate(panels):
    im=Image.open(B/f'Previews/S06_{letter}_v004.png').convert('RGB');assert im.size==(1280,720)
    strip.paste(im,(i*1280,0));draw.text((i*1280+32,742),letter+'  '+title,font=font,fill=(224,234,241));draw.text((i*1280+32,782),desc,font=small,fill=(145,165,180))
strip.save(B/'Previews/S06_ABC_review-strip_v004.jpg',quality=95)
files=[p for p in B.rglob('*') if p.is_file() and p.suffix!='.log' and p.name not in ('asset-manifest.json','sync-verification.json')]
manifest=[{'path':p.relative_to(B).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]
(B/'Records/asset-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
backup=Path('D:/MIT-ECCO-Render-Recovery/S06-Report-Recreation_v004');shutil.copytree(B,backup,dirs_exist_ok=True)
assert all(hashlib.sha256((backup/v['path']).read_bytes()).hexdigest()==v['sha256'] for v in manifest)
print('STRIP AND RECOVERY VERIFIED')
