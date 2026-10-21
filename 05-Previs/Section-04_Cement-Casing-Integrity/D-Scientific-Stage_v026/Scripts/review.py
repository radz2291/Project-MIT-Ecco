from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json
B=Path(__file__).resolve().parents[1]
font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',23);small=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',12)
sheet=Image.new('RGB',(1280,3*768),(14,25,34))
labels={'A':'A — Soft transparent tool','B':'B — CAD feature-edge wireframe','C':'C — Transparent tool + restrained wireframe'}
for i,(tag,title) in enumerate(labels.items()):
 im=Image.new('RGB',(1280,768),(14,25,34));d=ImageDraw.Draw(im);d.text((20,10),title,font=font,fill=(225,235,240));im.paste(Image.open(B/'Previews'/f'S04_D_{tag}_raw_v026.png').convert('RGB'),(0,48));d=ImageDraw.Draw(im);d.rectangle((0,740,1280,768),fill=(14,25,34));d.text((20,747),'ILLUSTRATIVE GEOMETRY AND COMPUTED WEAR — NOT FIELD DATA',font=small,fill=(195,214,222));im.save(B/'Previews'/f'S04_D_{tag}_review_v026.png');sheet.paste(im,(0,i*768))
sheet.save(B/'Previews/S04_D_treatment-comparison_v026.jpg',quality=94)
p=json.loads((B/'Records/proof.json').read_text());p['wireframe_method']='Polyline curves follow sharp/boundary edges of copied actual tool meshes, with40degree feature threshold. No triangulation grid and no new measurement geometry.';p['recommendation']='C balances contextual tool recognition and wear visibility. B is busier; A is quietest but weakens tool identity.';(B/'Records/proof.json').write_text(json.dumps(p,indent=2))
