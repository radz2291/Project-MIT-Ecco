# ECCO_RUNTIME_PATH_MIGRATION_20261031
"""Validate derived contextual lines before use; exits nonzero on stale World."""


def _ecco_repo_root():
    from pathlib import Path
    for candidate in Path(__file__).resolve().parents:
        if (candidate / '04-Production').is_dir():
            return candidate
    raise RuntimeError('ECCO repository root not found')

import hashlib,json,sys
from pathlib import Path
ROOT=_ecco_repo_root()
record=ROOT/'04-Production/Shared/Assets/Effects/DigitalEnvironment/Metadata/context-derivation.json'
world=ROOT/'04-Production/Shared/Assets/Environment/Borehole/World_environment_v010.blend'
def valid(current,recorded):return current==recorded
if __name__=='__main__':
 data=json.loads(record.read_text(encoding='utf-8-sig'));actual=hashlib.sha256(world.read_bytes()).hexdigest();ok=valid(actual,data['world_sha256'])
 print(json.dumps({'valid':ok,'current_world_sha256':actual,'recorded_world_sha256':data['world_sha256'],'action':'Derived geometry current; owner visual approval separate' if ok else 'STOP: regenerate successor shared collection and consumer, then verify/render; stale curves must not be used'},indent=2));sys.exit(0 if ok else 1)
