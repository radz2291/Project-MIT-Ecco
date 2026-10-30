"""Re-run the pressure-model consistency/input tests; writes only the task evidence JSON."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'04-Production/Shared/Assets/Acoustics/PressureField_v005/Scripts'))
import pressure_model
result=pressure_model.verify()
(Path(__file__).resolve().parent/'pressure-model-verification_v005.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result))
if not result['all_pass']:raise SystemExit(1)
