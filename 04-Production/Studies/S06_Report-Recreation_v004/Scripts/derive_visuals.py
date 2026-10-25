"""Trace anonymous visual structure, never recover or claim calibrated measurements."""
from pathlib import Path
import numpy as np
from PIL import Image
import json,hashlib
B=Path(__file__).resolve().parents[1]
SRC=B.with_name('S06_Anonymous-Report_v003')/'Media'
for d in ('Data','Scenes','Previews','Records'):(B/d).mkdir(exist_ok=True)
def rgb(name,size=None):
    im=Image.open(SRC/(name+'.png')).convert('RGB')
    if size:im=im.resize(size,Image.Resampling.LANCZOS)
    return np.asarray(im,dtype=float)/255
def smooth(a,n=5):
    return np.convolve(np.pad(a,(n//2,n//2),mode='edge'),np.ones(n)/n,mode='valid')
# These are dimensionless image observations, not a decoded measurement palette.
geo=rgb('geometry',(96,384));v=geo[:,:,2]-geo[:,:,0]
v=(v-np.median(v))/max(np.percentile(abs(v-np.median(v)),98),1e-8)
v=np.clip(v,-1,1)
amp=rgb('amplitude',(96,384)).mean(2)
amp=(amp-np.percentile(amp,2))/(np.percentile(amp,98)-np.percentile(amp,2))
amp=np.clip(amp,0,1)
im=rgb('shape');width=[]
for row in im:
    valid=np.where((row.min(1)<.94)&(np.arange(len(row))>25)&(np.arange(len(row))<len(row)-25))[0]
    width.append(valid[-1]-valid[0] if len(valid) else np.nan)
width=np.array(width);width=np.interp(np.arange(len(width)),np.where(np.isfinite(width))[0],width[np.isfinite(width)])
width=smooth(width,7);radius=np.interp(np.linspace(0,len(width)-1,384),np.arange(len(width)),width)/np.median(width)
im=rgb('profile');profile=[]
for row in im:
    ids=np.where((row[:,2]>.2)&(row[:,0]<.40)&(row[:,1]<.40))[0]
    profile.append(np.median(ids) if len(ids) else np.nan)
p=np.array(profile);p=np.interp(np.arange(len(p)),np.where(np.isfinite(p))[0],p[np.isfinite(p)])
p=(p-p.min())/(p.max()-p.min());profile=np.interp(np.linspace(0,len(p)-1,512),np.arange(len(p)),p)
im=rgb('sections');sections=[]
for ya,yb in ((0,im.shape[0]//2),(im.shape[0]//2,im.shape[0])):
    yy,xx=np.where(im[ya:yb].max(2)<.30);yy=yy+ya
    cx=(xx.min()+xx.max())/2;cy=(yy.min()+yy.max())/2
    ang=np.arctan2(yy-cy,xx-cx);r=np.hypot(xx-cx,yy-cy);rr=[]
    for a in np.linspace(-np.pi,np.pi,181):
        dist=np.abs(np.angle(np.exp(1j*(ang-a))));rr.append(np.median(r[dist<.035]))
    rr=np.array(rr);rr=np.interp(np.arange(len(rr)),np.where(np.isfinite(rr))[0],rr[np.isfinite(rr)])
    sections.append(rr/np.mean(rr))
np.savez_compressed(B/'Data/visual_structure.npz',geometry_visual=v,amplitude_visual=amp,silhouette_radius=radius,profile_visual=profile,sections_visual=np.array(sections))
(B/'Records/visual-provenance.json').write_text(json.dumps({'kind':'Report-inspired graphic reconstruction; illustrative, uncalibrated','method':'Silhouette and line tracing; separate color-trend sampling; new mesh colors and editable curves. No source textures displayed.','geometry':'Axisymmetric display reconstruction from visible silhouette only; unseen azimuthal shape is not recovered.','contrast':'Geometry and amplitude independently normalized for legibility; no measurement units or calibration recovered.','profile':'Source graphic shape traced; no physical values assigned.','sections':'Two near-circular source outlines traced in image space.','source_hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in SRC.glob('*.png')},'same_dataset_as_unfolding':False},indent=2),encoding='utf-8')
print('VISUAL STRUCTURE READY')
