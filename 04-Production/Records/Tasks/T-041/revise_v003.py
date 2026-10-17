from pathlib import Path
base=Path(__file__).resolve().parents[3]/'Shots/S02/PREVIS-T041'
src=(base/'Scripts/build_previs_v002.py').read_text().replace('v002','v003')
# Restore source master VERSION REFERENCES after renaming only our outputs.
src=src.replace('ECCO_master_temporary-plugs_v003','ECCO_master_temporary-plugs_v002').replace('ECCO_MASTER_v003','ECCO_MASTER_v002')
src=src.replace("xx=2.745+ii*.11/12","xx=2.775+ii*.05/12")
src=src.replace('math.radians(116+jj*32/24)','math.radians(121+jj*22/24)')
src=src.replace("zz=ii*25+jj;patchfaces.append((zz,zz+1,zz+26,zz+25))","zz=ii*25+jj\n        if ((ii-5.5)/6)**2+((jj-11.5)/12)**2<1:patchfaces.append((zz,zz+1,zz+26,zz+25))")
src=src.replace('(1.92,-.23,.20),(2.80,0,0)','(1.78,-.30,.26),(2.80,0,.045)')
src=src.replace("'Whole tool rotates / readings stay on the wall'","'Wall-fixed outline / x-ray data overlay'")
src=src.replace("s.render.engine='BLENDER_WORKBENCH'","for ob in data.objects:ob.show_in_front=True\nfor ob in gfx.objects:\n    ob.show_in_front=True\n    if ob.type=='FONT':ob.color=(.93,.96,.98,1)\ns.render.engine='BLENDER_WORKBENCH'")
(base/'Scripts/build_previs_v003.py').write_text(src)
for kind in ('render','verify'):
    script=(base/f'Scripts/{kind}_previs_v002.py').read_text().replace('v002','v003')
    (base/f'Scripts/{kind}_previs_v003.py').write_text(script)
