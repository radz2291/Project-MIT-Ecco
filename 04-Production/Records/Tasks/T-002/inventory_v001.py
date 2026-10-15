"""Inventory bounded production inputs; no source files are changed."""
from pathlib import Path
import hashlib,json,subprocess
from PIL import Image, ImageOps, ImageDraw
from pypdf import PdfReader
root=Path(__file__).resolve().parents[4]
out=Path(__file__).parent/'Evidence'
out.mkdir(exist_ok=True)
private=Path(__file__).parent/'Private'
private.mkdir(exist_ok=True)
def record(p):
    return dict(path=str(p),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
files=[]
for base in ['01-Brief','02-Reference','04-Production/Shared/Assets']:
    for p in (root/base).rglob('*'):
        if p.is_file(): files.append(record(p))
(out/'local-input-inventory_v001.json').write_text(json.dumps(files,indent=2),encoding='utf-8')
photos=sorted((root/'01-Brief/Image').glob('*'))+sorted((root/'02-Reference').glob('*.png'))
sheet=Image.new('RGB',(1000,((len(photos)+3)//4)*205),'white'); d=ImageDraw.Draw(sheet)
for i,p in enumerate(photos):
    im=Image.open(p); im.thumbnail((240,165)); x=(i%4)*250;y=(i//4)*205
    sheet.paste(im,(x+(240-im.width)//2,y));d.text((x+5,y+168),f'{i+1:02d} {p.name[:28]}',fill='black')
sheet.save(out/'references-contact_v001.jpg')
(out/'references-index_v001.json').write_text(json.dumps([str(p) for p in photos],indent=2))
for p in (root/'01-Brief').glob('*.pdf'):
    r=PdfReader(p)
    name='datasheet' if 'Datasheet' in p.name else 'field-log'
    dest=out if name=='datasheet' else private
    (dest/(name+'-text_v001.txt')).write_text('\n'.join(f'PAGE {i+1}\n{pg.extract_text()}' for i,pg in enumerate(r.pages)),encoding='utf-8')
print(f'{len(files)} source files hashed; {len(photos)} photos indexed')
