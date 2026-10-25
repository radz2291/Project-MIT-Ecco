"""One illustrative field for the three review frames; not recovered report measurements."""
from pathlib import Path
import numpy as np,json,hashlib
B=Path(__file__).resolve().parents[1];d=np.load(B/'Data/visual_structure.npz')
# Preserve the reference's relative bands and its independent amplitude pattern.
# Display radius and relief are explicitly authored, not inferred physical measurements.
g=d['geometry_visual'][::2].copy();a=d['amplitude_visual'][::2].copy()
nz,na=g.shape
# Periodic seam: keep source periodicity explicit for the illustrative full circumference.
g=(g+np.roll(g[:,::-1],1,axis=1))*.5
R=.19;H=2.4;r=R+.0025*g
theta=np.linspace(0,2*np.pi,na,endpoint=False);z=np.linspace(H/2,-H/2,nz)
dia=r+np.roll(r,na//2,axis=1)
np.savez_compressed(B/'Data/story_field.npz',radius=r,geometry=g,amplitude=a,theta=theta,z=z,diameter=np.stack([dia.min(1),dia.mean(1),dia.max(1)]),R=R,H=H)
(B/'Records/story-data.json').write_text(json.dumps({'kind':'Illustrative coherent dataset, inspired by anonymous report graphic structure','radius_rule':'0.19 + 0.0025 * normalized graphic color trend; authored scene metres, NOT recovered measurements','nominal_radius_scene_m':R,'relief_scene_m':.0025,'length_scene_m':H,'sample_grid':[nz,na],'source':'Data/visual_structure.npz','same_geometry_in_A_B_C':True,'amplitude':'Independent source visual channel. Not derived from radius.','physical_rock':'Contextual illustrative half borehole. Fixed presentation cut. Never animated to unwrap.','product':'Actual canonical ECCO source retained at native size.','source_identity_on_screen':False},indent=2),encoding='utf-8')
print('COHERENT STORY FIELD READY')
