"""Render editable review graphics from B201 event record and encode all frames."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,math,subprocess,time,hashlib
import imageio_ffmpeg
from functools import lru_cache
ROOT=Path(__file__).resolve().parents[3];M=ROOT/'Mechanisms/B201';R=ROOT/'Records/Tasks/T-007'
E=json.loads((R/'Evidence/build_v005.json').read_text());events=E['events']
FR=M/'Previews/Frames/v005';OUT=M/'Previews/B201_pulse-echo_v005.mp4'
fontfile='C:/Windows/Fonts/segoeui.ttf'
@lru_cache
def font(n):return ImageFont.truetype(fontfile,n)
BG=(16,23,33);WHITE=(226,232,240);MUTED=(151,168,186);CYAN=(83,207,237);GOLD=(247,187,89)
def pos(v):return (20+325-v[1]*650/.415,62+325-v[2]*650/.415)
def compose(f):
    im=Image.new('RGB',(1280,720),BG);im.paste(Image.open(FR/f'raw_{f:04}.png').resize((650,650)),(20,62))
    d=ImageDraw.Draw(im)
    def text(x,y,t,size=21,fill=WHITE):d.text((x,y),t,font=font(size),fill=fill)
    text(30,16,'B201  /  Pulse → wall → same sensor',27)
    text(810,22,'TECHNICAL PREVIEW  ·  v005',17,MUTED)
    d.rectangle((0,655,1280,720),fill=BG)
    text(30,661,'Illustrative signals and waveform · slowed schematic time · no measured data',19,MUTED)
    text(30,690,'Accepted T5 v002 / T6 v003  |  Section through sensor plane  |  Step-and-hold acquisition',16,MUTED)
    e=events[min(5,(f-1)//72)]
    if f<e['emit']:phase='Ready at sensor 01';col=CYAN
    elif f<e['contact']:phase='Transmit toward wall';col=CYAN
    elif f==e['contact']:phase='Wall interaction';col=WHITE
    elif f<=e['receive']:phase='Echo returns to sensor 01';col=GOLD
    elif f<e['start']+60:phase='Round trip complete';col=GOLD
    else:phase='Comparison complete' if e['cycle']==6 else 'Whole tool rotates to next station';col=MUTED
    text(720,83,f"{e['cycle']:02}  /  {phase}",22,col)
    text(720,117,'Cyan: outgoing   /   Amber: returning',17,MUTED)
    # Graphic lines are explicit spatial annotation, not additional acoustic energy.
    if e['emit']<=f<=e['receive']:
        p,q=pos(e['origin']),pos(e['wall'])
        d.line((p,q),fill=(84,109,128),width=1)
        d.ellipse((p[0]-4,p[1]-4,p[0]+4,p[1]+4),outline=CYAN,width=2)
    if f<217:
        text(720,206,'First, reveal isolated wall spots.',25)
        for j,t in enumerate(['One transmitting sensor.','A brief spot at wall contact.','An echo back to the same sensor.']):text(720,257+j*43,t,21,MUTED)
        text(720,449,'Three early pings precede the chart.',20)
        text(720,489,'Three sensors share one plane,',19,MUTED)
        text(720,516,'120° apart. Sensor 01 is isolated here.',19,MUTED)
        text(720,562,'No full measured ring is built in this proof.',17,MUTED)
    else:
        text(720,165,'Echo arrival shifts with stand-off.',24)
        text(720,204,'Stand-off = c_mud × Δt / 2',25)
        text(720,246,'Mud sound-speed correction is required.',17,MUTED)
        text(720,273,'Axis radius also needs sensor offset / eccentricity.',17,MUTED)
        for j,ev in enumerate(events[3:]):
            y=377+j*90;x0=774;scale=8;xe=x0+(ev['receive']-ev['emit'])*scale
            text(720,y-9,chr(65+j),19,MUTED)
            d.line((x0-10,y,x0+365,y),fill=(72,87,105),width=1)
            if f<ev['start']:continue
            elapsed=min(46,max(-2,f-ev['emit']))
            pts=[]
            for k in range(0,366):
                t=k/scale
                if t>elapsed:break
                # A conceptual glyph, not a synthesized or measured instrument trace.
                v=42*math.exp(-((t-.7)/.65)**2)-14*math.exp(-((t-2)/.8)**2)
                delay=ev['receive']-ev['emit']
                v+=30*math.exp(-((t-delay)/.7)**2)-10*math.exp(-((t-delay-1.3)/.8)**2)
                pts.append((x0+k,y-v))
            if len(pts)>1:d.line(pts,fill=CYAN,width=2)
            if f>=ev['emit']:text(x0-7,y+11,'Tx',15,CYAN)
            if f>=ev['receive']:
                d.line((x0,y-52,xe,y-52),fill=GOLD,width=2)
                for x in (x0,xe):d.line((x,y-57,x,y-47),fill=GOLD,width=2)
                text(1150,y-59,'Δt',16,GOLD);text(xe-16,y+11,'Echo',15,GOLD)
            elif f>=ev['emit']:
                x=x0+elapsed*scale;d.line((x,y-46,x,y+5),fill=GOLD,width=1)
        text(720,590,'Δt: round trip  |  Common schematic time →',16,MUTED)
        text(720,617,'Peak height is illustrative; it does not encode radius.',16,MUTED)
    text(30,620,'Exterior cap marker is provisional; acoustic face unverified.',16,WHITE)
    return im
t=time.perf_counter()
for f in range(1,433):compose(f).save(FR/f'review_{f:04}.png',compress_level=1)
ff=imageio_ffmpeg.get_ffmpeg_exe()
cmd=[ff,'-y','-v','error','-framerate','24','-i',str(FR/'review_%04d.png'),'-c:v','libx264','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(OUT)]
subprocess.run(cmd,check=True)
subprocess.run([ff,'-v','error','-i',str(OUT),'-f','null','-'],check=True)
preview_frames=[1,11,21,31,83,100,115,155,171,185,227,235,243,299,311,323,371,387,403,432]
sheet=Image.new('RGB',(1280,math.ceil(len(preview_frames)/2)*360),BG)
for k,f in enumerate(preview_frames):
    thumb=compose(f).resize((640,360));ImageDraw.Draw(thumb).text((12,5),f'frame {f}',font=font(14),fill=GOLD);sheet.paste(thumb,((k%2)*640,(k//2)*360))
sheet.save(M/'Previews/B201_review-sheet_v005.jpg',quality=90)
for f in (21,243,323,403,432):compose(f).save(M/f'Previews/B201_review_f{f:04}_v005.png')
qa={'frames':432,'fps':24,'duration_s':18,'resolution':[1280,720],'audio':False,'encode_and_graphics_seconds':time.perf_counter()-t,'decode_all_frames':'pass','video_sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'scene_sha256':E['scene_sha256'],'command':cmd,'review_frames':preview_frames}
(R/'Evidence/video-qa_v005.json').write_text(json.dumps(qa,indent=2))
print(json.dumps(qa,indent=2))
