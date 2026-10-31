"""Fail closed when a baked context-line derivation no longer matches World.

Run with Python from any directory. Regenerate in Blender with the recorded
cap_intersections_v003.py helper after a shape change, then review visually.
"""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
record=ROOT/'04-Production/Records/Tasks/T-054/Evidence/cap-intersections-v003.json'
world=ROOT/'04-Production/Shared/Assets/WellAssembly/World_environment_v010.blend'
data=json.loads(record.read_text(encoding='utf-8-sig'))
with world.open('rb') as handle:actual=hashlib.file_digest(handle,'sha256').hexdigest()
valid=actual==data['world_sha256']
print(json.dumps({'derivation':'S03 shared digital v003 diagnostic','world_current_sha256':actual,'world_recorded_sha256':data['world_sha256'],'valid':valid,'visual_status':'partial; contextual line continuity unresolved','action':'No regeneration required for hash; visual review still incomplete' if valid else 'STOP: regenerate cap_intersections_v003.py in Blender and review; do not use stale curves'},indent=2))
sys.exit(0 if valid else 1)
