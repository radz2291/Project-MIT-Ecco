"""Compose declared conceptual information; encode and fully decode review cut."""
from pathlib import Path
import json,math,subprocess,hashlib,time,sys
from PIL import Image,ImageDraw,ImageFont
import imageio_ffmpeg
BASE=Path(__file__).resolve().parents[1];PROD=BASE.parents[1];EVID=PROD/'Records/Tasks/T-009/Evidence';PRE=BASE/'Previews/v002'
ff=imageio_ffmpeg.get_ffmpeg_exe()
font=lambda n:ImageFont.truetype('C:/Windows/Fonts/arial.ttf',n)
white='#edf1f6';muted='#aab7c8';blue='#318bd1';gold='#b88a39';cyan='#59d9e2'
titles={'retrieval':'01 / Retrieval into existing upper casing','support':'02 / Casing response: support changes ringing','channel':'03 / Axial channel: cutaway and 360-degree map','wear':'04 / Internal wear: larger inner radius, unchanged exterior'}
rows=json.loads((EVID/'build-render_v002.json').read_text());qa=[];sheet=Image.new('RGB',(1280,4*360),'#101823')
selected=sys.argv[1:] or [r['case'] for r in rows]
for index,row in enumerate(rows):
    case=row['case'];folder=PRE/case;outframes=folder/'Composed/Frames';outframes.mkdir(parents=True,exist_ok=True)
    if case not in selected:
        previous=json.loads((EVID/'video-qa_v002.json').read_text())
        qa.append(next(q for q in previous if q['case']==case))
        pic=Image.open(outframes/'frame_0110.png');sheet.paste(pic.resize((640,360)),((index%2)*640,(index//2)*360))
        continue
    for f in range(1,145):
        im=Image.new('RGB',(1280,720),'#101823');d=ImageDraw.Draw(im)
        d.text((30,18),titles[case],font=font(28),fill=white)
        d.text((30,55),'T9 / B203 v002 | Conceptual mechanism proof | Technical review',font=font(19),fill=muted)
        im.paste(Image.open(folder/f'Frames/frame_{f:04d}.png'),(0,92))
        if case=='retrieval':
            d.text((40,500),'Existing cemented casing (left)     |     Deeper open hole (right)',font=font(25),fill=white)
            d.line((900,560,350,560),fill=cyan,width=4);d.polygon([(350,560),(375,548),(375,572)],fill=cyan)
            d.text((380,578),'Retrieval direction / authored timing / no active drilling',font=font(22),fill=cyan)
            d.text((40,625),'Orange adapters and bit are simplified proxies; deployment and shoe require MIT review.',font=font(20),fill=muted)
        elif case=='support':
            d.text((35,493),'Upper: cement support (outside layer offset)' ,font=font(21),fill=gold)
            d.text((670,493),'Lower: illustrative channel (outside layer offset)',font=font(21),fill=blue)
            for j,(decay,col) in enumerate(((6,gold),(1.7,blue))):
                x0=40+j*635;y0=580;pts=[]
                for k in range(550):
                    t=k/549;amp=48*math.exp(-decay*t)*math.sin(2*math.pi*9*t)
                    pts.append((x0+k,y0-amp))
                d.line((x0,y0,x0+550,y0),fill=muted,width=1)
                d.line(pts[:max(2,int(550*min(1,f/100)))],fill=col,width=2)
            d.text((35,646),'Illustrative ringdown only: faster damping / more persistent response. No calibrated axes.',font=font(20),fill=muted)
        elif case=='channel':
            # Same axial/angular mask as Blender mesh. Full 0..360 map includes hidden rear sectors.
            x0,y0,w,h=330,525,860,108;nx,na=60,72
            progress=(f-1)/143
            for i in range(nx):
                x=-1.6+3.2*(i+.5)/nx
                for j in range(na):
                    a=2*math.pi*(j+.5)/na
                    col=blue if -1.2<=x<=1.2 and .25<=a<=.85 else gold
                    if (i+1)/nx>progress:col='#26313e'
                    d.rectangle((x0+j*w/na,y0+i*h/nx,x0+(j+1)*w/na,y0+(i+1)*h/nx),fill=col)
            d.text((35,523),'Axial position',font=font(20),fill=white)
            d.text((35,552),'top to bottom',font=font(18),fill=muted)
            for deg in (0,90,180,270,360):d.text((x0+deg*w/360-10,498),str(deg)+'°',font=font(16),fill=muted)
            d.text((35,465),'Outside layer offset for visibility; same axial / azimuth coordinates',font=font(19),fill=muted)
            d.text((330,638),'Azimuth around casing  |  Gold: cement  /  Blue: authored water channel',font=font(19),fill=white)
            d.text((35,675),'Conceptual processed interpretation; not live telemetry or measured field data.',font=font(19),fill=muted)
        else:
            # Radial section makes the 4mm authored groove readable at the saved physical scale.
            cx,cy,scale=205,580,420
            ri=12.515*.0254/2;ro=13.375*.0254/2
            d.rectangle((150,510,270,655),fill='#7b8c9d')
            pts=[]
            for k in range(361):
                a=2*math.pi*k/360;aw=(a+math.pi)%(2*math.pi)-math.pi
                r=ri+.004*math.exp(-(aw/.28)**2)
                pts.append((cx+r*scale*math.cos(a),cy-r*scale*math.sin(a)))
            # Magnified local radial section. Both thickness and groove share the same scale.
            edge=[(150+.004*5000*math.exp(-((yy-580)/25)**2),yy) for yy in range(510,656)]
            d.polygon([(55,510)]+edge+[(55,655)],fill='#101823')
            outer=150+(ro-ri)*5000
            d.rectangle((outer,510,270,655),fill='#101823')
            d.line((150,510,150,655),fill=white,width=1)
            d.line((outer,510,outer,655),fill=muted,width=2)
            d.line((70,580,170,580),fill=cyan,width=2)
            d.text((35,662),'Magnified local wall section',font=font(17),fill=muted)
            d.text((340,505),'White reference: nominal inner surface',font=font(24),fill=white)
            d.text((340,548),'Groove cuts into steel from inside; outside stays fixed.',font=font(24),fill=white)
            d.text((340,591),'Longer inner-wall return path supports geometry interpretation.',font=font(22),fill=cyan)
            d.text((340,635),'Authored 4 mm maximum groove; not measured wear or a thickness result.',font=font(19),fill=muted)
        if case!='channel':d.text((30,684),'Illustrative signals and timing | Sources: S04 V2 / accepted T5 v002 + T6 v003 | MIT review pending',font=font(17),fill=muted)
        im.save(outframes/f'frame_{f:04d}.png')
        if f in (1,72,144):im.save(PRE/f'B203_{case}_f{f:03d}_v002.png')
        if f==110:sheet.paste(im.resize((640,360)),((index%2)*640,(index//2)*360))
    video=PRE/f'B203_{case}_v002.mp4';start=time.perf_counter()
    p=subprocess.run([ff,'-y','-framerate','24','-i',str(outframes/'frame_%04d.png'),'-c:v','libx264','-crf','20','-pix_fmt','yuv420p','-an','-movflags','+faststart',str(video)],capture_output=True,text=True)
    (EVID/f'encode-{case}_v002.log').write_text(p.stderr);p.check_returncode()
    reader=imageio_ffmpeg.read_frames(str(video),pix_fmt='rgb24');meta=next(reader);count=sum(1 for _ in reader)
    assert count==144 and meta['size']==(1280,720) and meta['fps']==24
    qa.append({'case':case,'frames':count,'metadata':meta,'video':str(video.relative_to(PROD.parent)).replace('\\','/'),'sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'encode_decode_seconds':time.perf_counter()-start})
sheet.crop((0,0,1280,720)).save(PRE/'B203_review-sheet_v002.jpg')
concat=PRE/'concat_v002.txt';concat.write_text('\n'.join("file '"+str((PROD.parent/q['video']).resolve()).replace('\\','/')+"'" for q in qa))
combined=PRE/'B203_all-proofs_v002.mp4'
subprocess.run([ff,'-y','-f','concat','-safe','0','-i',str(concat),'-c','copy','-movflags','+faststart',str(combined)],capture_output=True,check=True)
reader=imageio_ffmpeg.read_frames(str(combined),pix_fmt='rgb24');meta=next(reader);count=sum(1 for _ in reader);assert count==576
qa.append({'case':'combined','frames':count,'metadata':meta,'sha256':hashlib.sha256(combined.read_bytes()).hexdigest(),'video':str(combined.relative_to(PROD.parent)).replace('\\','/')})
(EVID/'video-qa_v002.json').write_text(json.dumps(qa,indent=2))
# All frames in ordered contact sheets for visual inspection, plus full-size key frames.
for row in rows:
    case=row['case']
    for page in range(6):
        grid=Image.new('RGB',(1280,1080),'#101823')
        for j in range(24):
            f=page*24+j+1;pic=Image.open(PRE/f'{case}/Composed/Frames/frame_{f:04d}.png')
            grid.paste(pic.resize((320,180)),((j%4)*320,(j//4)*180))
        grid.save(PRE/f'{case}/all-frames-{page+1}_v002.jpg')
print('PACKAGE_DECODE_PASS',count)
