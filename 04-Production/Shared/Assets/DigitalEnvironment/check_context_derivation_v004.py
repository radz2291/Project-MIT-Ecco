"""Validate derived contextual lines before use; exits nonzero on stale World."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
record=ROOT/'04-Production/Records/Tasks/T-054/Evidence/cap-intersections-v004.json'
world=ROOT/'04-Production/Shared/Assets/WellAssembly/World_environment_v010.blend'
def valid(current,recorded):return current==recorded
if __name__=='__main__':
 data=json.loads(record.read_text(encoding='utf-8-sig'));actual=hashlib.sha256(world.read_bytes()).hexdigest();ok=valid(actual,data['world_sha256'])
 print(json.dumps({'valid':ok,'current_world_sha256':actual,'recorded_world_sha256':data['world_sha256'],'action':'Derived geometry current; owner visual approval separate' if ok else 'STOP: regenerate successor shared collection and consumer, then verify/render; stale curves must not be used'},indent=2));sys.exit(0 if ok else 1)
