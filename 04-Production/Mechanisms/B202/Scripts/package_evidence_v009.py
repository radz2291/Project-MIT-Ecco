"""Numerical traces and identical-camera comparison boards. No image alteration
apart from assembling labeled source renders into review sheets.
"""
import sys,csv,math
from pathlib import Path
plot_deps=Path(__file__).resolve().parents[4]/'04-Production/Scratch/T-008/plot-deps'
if plot_deps.exists():sys.path.insert(0,str(plot_deps))
from PIL import Image,ImageDraw,ImageFont
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[2];E=ROOT/'04-Production/Records/Tasks/T-008/Evidence/v009';PRE=BASE/'Previews/Mechanism_v009';DATA=BASE/'Data/v009';sys.path.insert(0,str(BASE/'Scripts'))
from acquisition_core_v009 import *
index=read_json(DATA/'index_v009.json');cases=['irregular_constant','irregular_changed_constant','irregular_material_changed'];rows=[]
for case in cases:
    grid=read_json(DATA/index['cases'][case]['files']['grid']);evs={e['id']:e for e in read_json(DATA/index['cases'][case]['files']['events'])}
    for p in grid['cells']:
        if p['x_m']!=3.0 or not p['measured']:continue
        rows.append({'case':case,'x_m':p['x_m'],'azimuth_deg':math.degrees(p['azimuth_rad']),'radius_mm':1000*p['radius_m'],'delta_radius_mm':1000*p['delta_radius_m'],'mean_tof_microseconds':1e6*sum(evs[i]['tof_2way_s']*w for i,w in zip(p['event_ids'],p['weights'])),'synthetic_echo_strength':p['echo_strength'],'source_event_ids':'|'.join(p['event_ids'])})
with (E/'comparison_trace_depth3m_v009.csv').open('w',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
fig,axes=plt.subplots(3,2,figsize=(12,9),sharex=True);fields=[('mean_tof_microseconds','Round-trip time (µs)'),('radius_mm','Reconstructed radius (mm)'),('synthetic_echo_strength','Synthetic received strength (unitless)')]
for col,other,title in [(0,cases[1],'A / change wall geometry, hold material fixed'),(1,cases[2],'B / change material, hold wall geometry fixed')]:
    for row,(field,label) in enumerate(fields):
        ax=axes[row,col]
        for case,color,name in [(cases[0],'#334f69','T6 irregular / constant material'),(other,'#cb683e','Changed wall' if col==0 else 'Changed material layer')]:
            vals=[p for p in rows if p['case']==case];ax.plot([p['azimuth_deg'] for p in vals],[p[field] for p in vals],label=name,color=color,lw=1.5)
        ax.set_ylabel(label);ax.grid(alpha=.2)
        if row==0:ax.set_title(title,fontsize=11);ax.legend(fontsize=8)
        if row==2:ax.set_xlabel('World azimuth (degrees)')
fig.suptitle('B202 v009 / controlled synthetic mechanism comparisons / X = 3.0 m',fontsize=13)
fig.text(.5,.012,'Synthetic demonstration parameters; no ENP3 calibration, field data or processing-accuracy claim.',ha='center',fontsize=9)
fig.tight_layout(rect=(0,.03,1,.95));fig.savefig(PRE/'B202_numeric_comparison_v009.png',dpi=150);plt.close(fig)
font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',22);small=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',17)
for label,left,right,title in [('geometry','irregular_constant','irregular_changed_constant','A / physical wall change — identical camera and material'),('material','irregular_constant','irregular_material_changed','B / acoustic material change — identical camera and wall')]:
    sheet=Image.new('RGB',(1280,900),(15,20,26));d=ImageDraw.Draw(sheet);d.text((20,14),'B202 v009 / '+title,font=font,fill=(235,240,245))
    for col,case in enumerate([left,right]):
        d.text((col*640+18,48),'Baseline' if col==0 else ('Wall changed' if label=='geometry' else 'Material layer changed'),font=small,fill=(190,206,225))
        for row,field in enumerate(['radius','echo_strength']):
            image=Image.open(PRE/f'{case}_{field}_v009.png').convert('RGB').resize((640,360));sheet.paste(image,(col*640,78+row*390));d.text((col*640+18,440+row*390),'Reconstructed geometry / delta radius' if row==0 else 'Synthetic received echo strength',font=small,fill=(219,227,238))
    d.text((20,875),'Data-derived surfaces; sparse bins remain absent. Synthetic monostatic response, not proprietary ENP3 processing.',font=small,fill=(170,185,202));sheet.save(PRE/f'B202_{label}_comparison_v009.jpg',quality=94)
sheet=Image.new('RGB',(1280,870),(15,20,26));d=ImageDraw.Draw(sheet);d.text((20,14),'B202 v009 / response, spiral, tight and sparse-coverage assets',font=font,fill=(235,240,245))
for i,(case,field,label) in enumerate([('irregular_layers','echo_strength','Synthetic layers + inclined interface + weak patch'),('spiral_layers','radius','Reconstructed T6 spiral; no diagnosed cause'),('tight_layers','radius','Reconstructed tight illustration; no bit passage'),('sparse_irregular','radius','Partial acquisition; missing sectors stay absent')]):
    x=(i%2)*640;y=60+(i//2)*390;image=Image.open(PRE/f'{case}_{field}_v009.png').convert('RGB').resize((640,360));sheet.paste(image,(x,y));d.text((x+16,y+362),label,font=small,fill=(220,228,238))
d.text((20,846),'No cinematic animation built in T8. Playable-proof acceptance test remains with T27.',font=small,fill=(170,185,202));sheet.save(PRE/'B202_mechanism_states_v009.jpg',quality=94)
print('V009_EVIDENCE_PACKAGED')
