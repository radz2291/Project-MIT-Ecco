from pathlib import Path
import shutil
B=Path(__file__).resolve().parents[1];P=B.parent/'Sequence_v001'
shutil.copy2(P/'Records/build.json',B/'Records/build.json')
verify=(P/'Scripts/verify.py').read_text().replace('S07_Monumental-Precision_v001.blend','S07_Monumental-Precision_v002.blend')
(B/'Scripts/verify.py').write_text(verify)
package=(P/'Scripts/package.py').read_text().replace('S07_Monumental-Precision_v001','S07_Monumental-Precision_v002').replace('S06-to-S07_transition_v001','S06-to-S07_transition_v002').replace('S07_final-product-hero_v001','S07_final-product-hero_v002')
package=package.replace("shutil.copy2(B/'Cache/frames/0192.png',B/'Previews/S07_final-product-hero_v002.png')","shutil.copy2(B/'Cache/frames/0192.png',B/'Previews/S07_final-product-hero_v002.png')\nshutil.copy2(B/'Cache/frames/0076.png',B/'Previews/S07_second-beauty_v002.png')")
package=package.replace('[1,8,16,24,32,40,48,64,80,96,112,128,144,152,164,192]','[1,24,48,60,61,72,84,94,100,108,120,132,144,152,164,192]')
package=package.replace("'review_status':'Full S07 candidate awaiting owner review; no full-film assembly or final finishing'","'new_render_seconds':sum(r['seconds'] for r in timings if not r.get('reused_from')),'newly_rendered_frames':85,'reused_unchanged_frames':107,'review_status':'S07 v002 adds second beauty angle; owner review pending'")
(B/'Scripts/package.py').write_text(package)
