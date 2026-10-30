"""Targeted existing-video samples only. No Blender rendering or edits."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess, io, json

ROOT = Path(__file__).resolve().parents[4]
TASK = Path(__file__).resolve().parent
OUT = TASK / 'Evidence'
OUT.mkdir(exist_ok=True)
FF = ROOT / '04-Production/Mechanisms/B201/Cache/python/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
sources = [
    ('S02', '05-Previs/Section-02_Measurement-History/v011/Continuation/Previews/S02_wall-build_v011.mp4', [9,34,64,97], 431),
    ('S06', '04-Production/Studies/S06_Report-Recreation_v004/Previews/S06_cinematic-study_v004_polished.mp4', [8,30,52,76], 0),
]
font = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 18)
records = []
for name, video, ordinals, offset in sources:
    sheet = Image.new('RGB', (960,600), (14,18,24))
    draw = ImageDraw.Draw(sheet)
    for i, ordinal in enumerate(ordinals):
        p = subprocess.run([str(FF), '-v','error','-i',str(ROOT/video),'-vf',f'select=eq(n\\,{ordinal-1})','-frames:v','1','-f','image2pipe','-vcodec','png','-'],capture_output=True,check=True)
        im = Image.open(io.BytesIO(p.stdout)).convert('RGB')
        im.thumbnail((480,270))
        x,y=(i%2)*480,(i//2)*300
        sheet.paste(im,(x,y))
        draw.text((x+8,y+273),f'{name} native frame {ordinal+offset}',font=font,fill='white')
    target = OUT/f'{name}_measurement-reveal.jpg'
    sheet.save(target,quality=92)
    records.append({'section':name,'source_movie':video,'video_frames_1based':ordinals,'native_frames':[x+offset for x in ordinals],'sheet':target.name})
(OUT/'measurement-reveal-samples.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
print(json.dumps(records))
