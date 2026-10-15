from pathlib import Path
import hashlib,json,math,shutil
base=Path(r'C:\Users\RZ1\Desktop\RZ')
here=Path(__file__).parent
paths=[
 '261008-MIT-Ecco/03-Assets/PZ12-8301 Main Housing ENP3 _A_ Modified TFA _5_ Ready _TC.stp',
 '261008-MIT-Ecco/04-Project/01-ECCO_First_Ping-Test/01-Blender/Source_Imported_ecco.blend',
 '261008-MIT-Ecco/04-Project/01-ECCO_First_Ping-Test/01-Blender/ECCO_First_Ping.blend',
 '261008-MIT-Ecco/04-Project/01-ECCO_First_Ping-Test/02-Previews/Client_Confirmed_Sensor.png',
 '261008-MIT-Ecco/04-Project/01-ECCO_First_Ping-Test/02-Previews/Motion_Review_Contact_Sheet.jpg',
 '261008-MIT-Ecco/04-Project/01-ECCO_First_Ping-Test/02-Previews/ECCO_First_Ping_Preview.mp4',
 '261008-MIT-Ecco/04-Project/01-ECCO_First_Ping-Test/02-Previews/IMPLEMENTATION_REPORT.md',
 '261008-MIT-Ecco/04-Project/02-ECCO_First_Ping-Side_View-Test/01-Blender/ECCO_First_Ping_Side_View.blend',
 '261008-MIT-Ecco/04-Project/03-ECCO_Transformation_Prototype/V1.1-Final/ECCO_Transformation_V1.1_Final.blend',
 '261008-MIT-Ecco/04-Project/03-ECCO_Transformation_Prototype/V1.1-Final/ECCO_Transformation_V1.1_Final_Playblast.mp4',
 '261008-MIT-Ecco/04-Project/03-ECCO_Transformation_Prototype/V1.1-Final/scene_manifest.json',
 '261006-Rolladice/IntoTheInvisible/Viewport_FullShot_8seconds.blend',
 '261006-Rolladice/IntoTheInvisible/Viewport_FullShot_Review.jpg',
]
records=[]
for rel in paths:
 p=base/rel
 records.append(dict(path=str(p),exists=p.exists(),bytes=p.stat().st_size if p.exists() else None,sha256=hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None))
(here/'Evidence/external-inputs_v001.json').write_text(json.dumps(records,indent=2))
for name in ['Client_Confirmed_Sensor.png','Motion_Review_Contact_Sheet.jpg']:
 p=base/'261008-MIT-Ecco/04-Project/01-ECCO_First_Ping-Test/02-Previews'/name
 shutil.copy2(p,here/'Evidence'/name)
a=json.loads((here/'Evidence/first-ping_v001.json').read_text())
sensor=[o for o in a['objects'] if o['name'].startswith('SENSOR_')]
angles=sorted(math.degrees(math.atan2(o['location_world'][1],o['location_world'][0]))%360 for o in sensor)
result=dict(angles_degrees=angles,spacing_degrees=[(angles[(i+1)%3]-angles[i])%360 for i in range(3)],z_values=[o['location_world'][2] for o in sensor],radius_m=[math.hypot(*o['location_world'][:2]) for o in sensor],note='Scene markers, not independent proof of physical transducer location or shoulder datum.')
(here/'Evidence/sensor-marker-check_v001.json').write_text(json.dumps(result,indent=2))
print(len(records),'external records',result)
