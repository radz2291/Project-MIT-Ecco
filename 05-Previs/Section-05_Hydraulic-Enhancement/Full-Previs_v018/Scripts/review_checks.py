import json
from pathlib import Path
from PIL import Image,ImageChops
B=Path(__file__).resolve().parents[1]
p=B/'Records/native-verification.json'
d=json.loads(p.read_text())
a=Image.open(B/'Previews/reopened_native_198.png').convert('RGB')
b=Image.open('D:/MIT-ECCO-Render-Recovery/S05-v018-RenderCache/Frames/S05_0198.png').convert('RGB')
d['reopened_frame_198_pixel_identical']=ImageChops.difference(a,b).getbbox() is None
assert d['reopened_frame_198_pixel_identical'] and not d['missing_libraries']
p.write_text(json.dumps(d,indent=2))
review={'review_status':'Owner review pending','all_432_frames_decoded':True,'chronological_contact_sheet_inspected':True,'normal_speed_visual_review_completed':False,'playback_tool_error':'Browser and Computer Use runtimes both failed to initialize: failed to write kernel assets, system cannot find path (os error 3).','observed_strengths':['Consistent upward screen direction across the three compositions','Steel, matte formation and amber fluid remain distinguishable','Central pad interaction is larger than entry and ending; same fragment group changes position around pad across sampled frames','Final widening reconnects the visible regions of the body'],'remaining_readability_questions':['Acceleration and diffuser flow-management meaning remain qualitative and need owner judgment in motion','Cuttings become less prominent in the wide ending','Low-sample grain remains visible at previs settings'],'geometry_truth':'Sampled clearance and source preservation passed; trajectories remain illustrative, not CFD.'}
(B/'Records/visual-review.json').write_text(json.dumps(review,indent=2))
note='''\n## Final delivery checks\n\nThe saved native was reopened with no missing libraries. Its frame198 rerender is pixel-identical to the delivered frame. All432 encoded frames decode, and the22-frame chronological contact sheet was visually inspected. Normal-speed visual review could not be completed: both browser and Computer Use runtimes failed to initialize with a missing kernel-assets path. The MP4 is provided for owner playback review; decoding and sampled inspection are not a substitute for that acceptance check.\n'''
for name in ['README.md','Records/report.md']:
 p=B/name;p.write_text(p.read_text(encoding='utf-8')+note,encoding='utf-8')
print(json.dumps({'native_matches_render':True,'normal_speed_visual_review_completed':False}))
