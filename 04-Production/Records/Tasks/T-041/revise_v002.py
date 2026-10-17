"""Retain v001, generate independently reproducible v002 source."""
from pathlib import Path
base=Path(__file__).resolve().parents[3]/'Shots/S02/PREVIS-T041'
src=(base/'Scripts/build_previs_v001.py').read_text()
src=src.replace('v001','v002')
src=src.replace("(2.46,-.44,.36),(2.81,-.025,.075)","(2.23,-.26,.25),(2.80,-.10,.105)")
src=src.replace("(2.50,-.41,.34),(2.81,-.025,.075)","(2.26,-.25,.24),(2.80,-.10,.105)")
src=src.replace("(2.54,-.40,.33),(2.81,-.015,.075)","(2.29,-.25,.24),(2.80,-.10,.105)")
src=src.replace("(1.94,-.69,.56),(2.86,0,.015)","(1.92,-.23,.20),(2.80,0,0)")
src=src.replace("18,49,18","18,51,22").replace("18,49,17","18,51,20")
src=src.replace("18,22,10","18,23,12").replace("18,347,9","18,348,11")
src=src.replace("18,322,11","18,320,13").replace("18,315,12","18,316,14")
# A retained exact T6 surface patch makes actual contact visible. It is not
# a planar invented rock card and it uses no inflated annular spacing.
insert='''
patchverts=[];patchfaces=[]
for ii in range(13):
    xx=2.745+ii*.11/12
    for jj in range(25):patchverts.append(hit(math.radians(116+jj*32/24),xx))
for ii in range(12):
    for jj in range(24):
        zz=ii*25+jj;patchfaces.append((zz,zz+1,zz+26,zz+25))
pm=bpy.data.meshes.new('Exact T6 contact surface');pm.from_pydata(patchverts,[],patchfaces);pm.update()
po=bpy.data.objects.new('T41_RETAINED_ROCK_AT_CONTACT',pm);env.objects.link(po);po.color=(.20,.28,.32,1)
visible(po,1,168)
'''
src=src.replace("rig['show_open']=0;rig.update_tag()",insert+"\nrig['show_open']=0;rig.update_tag()")
# Foreground editorial backing so the low-resolution waveform is readable.
panel='''
panelverts=[screen(x,y)+Vector((0,0,-.001)) for x,y in [(12,211),(365,211),(365,331),(12,331)]]
pm=bpy.data.meshes.new('Quiet waveform backing');pm.from_pydata(panelverts,[],[(0,1,2,3)]);pm.update()
po=bpy.data.objects.new('T41_WAVEFORM_READING_FIELD',pm);gfx.objects.link(po);po.parent=cam;po.color=(.015,.028,.038,1);visible(po,73,168)
'''
src=src.replace("# First three contact glimpses;",panel+"\n# First three contact glimpses;")
(base/'Scripts/build_previs_v002.py').write_text(src)
render=(base/'Scripts/render_previs_v001.py').read_text().replace('v001','v002')
(base/'Scripts/render_previs_v002.py').write_text(render.replace("folder=BASE/'Previews/Frames'","folder=BASE/'Previews/v002/Frames'"))
