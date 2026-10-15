"""Reproduce source-based research arithmetic and comparison diagram; no scene edits."""
import json,math
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[4];TASK=ROOT/'Records/Tasks/T-006'
c=json.loads((ROOT/'Shared/Assets/WellAssembly/config_researched-proposal_v002.json').read_text())
measurement=json.loads((TASK/'Evidence/product-inspection_v002.json').read_text())
tool=measurement['maximum_axis_diameter_m']*1000
upper=c['intervals']['upper_cased'];lower=c['intervals']['lower_open']
inch=25.4
hole=lower['hole_diameter_inches']*inch
host=upper['host_hole_diameter_inches']*inch
od=upper['casing_od_inches']*inch;wall=upper['body_wall_inches']*inch
body_id=od-2*wall;drift=upper['reference_drift_inches']*inch
assert abs(body_id-upper['nominal_body_id_inches']*inch)<1e-9
gaps={'tool_to_open_hole':(hole-tool)/2,'tool_to_nominal_casing_ID':(body_id-tool)/2,
      'tool_to_reference_drift':(drift-tool)/2,'bit_gauge_to_reference_drift':(drift-hole)/2,
      'ideal_cement_annulus':(host-od)/2}
assert min(gaps.values())>0
assert drift>=12.3*inch and body_id>=12.3*inch
assert 12.259*inch<12.3*inch
result={'status':'source-backed illustrative proposal; no MIT deployment approval',
        'measured_tool_od_mm':tool,'reference_dimensions_mm':{'lower_open_hole':hole,'upper_host_hole':host,
        'casing_od':od,'casing_wall':wall,'nominal_casing_id':body_id,'reference_drift':drift},
        'ideal_centered_radial_gaps_mm':gaps,'checks':{'unit_and_wall_conversion':True,
        'positive_centered_envelopes':True,'61lb_ft_drift_above_12_3in':True,
        '68lb_ft_reference_drift_below_12_3in':True},
        'limits':['No tolerance, connection/shoe, dogleg, BHA placement, safety or MIT operational acceptance',
                  'Cement annulus inferred from selected reference geometry, not prescribed cement design']}
(TASK/'Evidence/researched-scenario-checks_v002.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
im=Image.new('RGB',(1440,900),'#101823');d=ImageDraw.Draw(im)
def font(s):return ImageFont.truetype('C:/Windows/Fonts/arial.ttf',s)
d.text((50,30),'T6 / A researched configuration that can fit ENP3',font=font(32),fill='white')
d.text((50,80),'Provisional illustration proposal - two different well intervals, drawn to the same scale',font=font(21),fill='#b9c7d5')
scale=.9;cy=380;cx=360
def circle(x,r,fill,outline=None):d.ellipse((x-r,cy-r,x+r,cy+r),fill=fill,outline=outline,width=2)
circle(cx,host/2*scale,'#766a50','#c1ac78')
circle(cx,od/2*scale,'#8693a1','#b9c7d5')
circle(cx,body_id/2*scale,'#101823','#68cad1')
circle(cx,tool/2*scale,'#536477','#c5d2e0')
d.text((cx-105,cy-15),'12in ENP3 envelope',font=font(22),fill='white')
d.text((140,130),'Upper cased interval',font=font(28),fill='white')
d.text((105,610),'17.5in host hole; ideal cement annulus',font=font(23),fill='#c1ac78')
d.text((105,650),'13.375in casing OD / 12.515in body ID',font=font(23),fill='#b9c7d5')
d.text((105,690),'61lb/ft reference; 12.359in drift',font=font(23),fill='#b9c7d5')
d.text((105,730),f"Tool gap at reference drift: {gaps['tool_to_reference_drift']:.3f}mm",font=font(23),fill='#68cad1')
cx=1060
circle(cx,hole/2*scale,'#101823','#68cad1')
circle(cx,tool/2*scale,'#536477','#c5d2e0')
d.text((cx-105,cy-15),'12in ENP3 envelope',font=font(22),fill='white')
d.text((850,130),'Lower open-hole interval',font=font(28),fill='white')
d.text((835,610),'12.25in nominal hole / bit gauge',font=font(23),fill='#68cad1')
d.text((835,650),'Below the casing shoe; no casing here',font=font(23),fill='#b9c7d5')
d.text((835,690),f"Centered tool-wall gap: {gaps['tool_to_open_hole']:.3f}mm",font=font(23),fill='white')
d.text((835,730),'BHA placement and crossovers unresolved',font=font(22),fill='#b9c7d5')
d.text((50,820),'Sources: SLB well-size progression; Tenaris casing dimensions; accepted T5 v002. See research note for links.',font=font(20),fill='#b9c7d5')
d.text((50,850),'This is a nominal geometry comparison, not a tolerance, drift-through-shoe, dogleg or operating-safety certification.',font=font(20),fill='#b9c7d5')
im.save(TASK/'Previews/researched-scenario_v002.png')
print(json.dumps(result,indent=2))
