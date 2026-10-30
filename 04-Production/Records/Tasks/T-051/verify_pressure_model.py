"""Independent numerical checks of the deliberately assumed pressure proof."""
import importlib.util, pathlib, sys, json, dataclasses, hashlib
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[4]
path = ROOT / '04-Production/Shared/Assets/Acoustics/PressureField_v005/Scripts/pressure_model.py'
spec = importlib.util.spec_from_file_location('pressure_model_review', path)
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)
m = mod.Model()
t = np.arange(0, 70e-6, 1e-8)
base = mod.components(0, t, m)[1]
faster = mod.components(0, t, dataclasses.replace(m, sound_speed_m_s=m.sound_speed_m_s*2))[1]
farther = mod.components(0, t, dataclasses.replace(m, gap_m=m.gap_m*2))[1]
inverted = mod.components(0, t, dataclasses.replace(m, pressure_reflection=-m.pressure_reflection))[1]
roundtrip = 2*m.gap_m/m.sound_speed_m_s
def first_nonzero(v):
    return float(t[np.flatnonzero(np.abs(v)>1e-7)[0]])
checks = {
    'no_echo_before_geometric_delay': bool(np.all(base[t<roundtrip]==0)),
    'double_speed_advances_actual_echo_by_half_roundtrip': abs((first_nonzero(base)-first_nonzero(faster))-roundtrip/2)<2e-8,
    'double_distance_delays_actual_echo_one_roundtrip': abs((first_nonzero(farther)-first_nonzero(base))-roundtrip)<2e-8,
    'signed_reflection_inverts_actual_samples': bool(np.allclose(inverted, -base)),
    'zero_reflection_removes_return': bool(np.all(mod.components(0,t,dataclasses.replace(m,pressure_reflection=0))[1]==0)),
    'pulse_and_echo_end': bool(np.all(mod.components(0,np.array([60e-6,70e-6]),m)[2]==0)),
}
s = np.linspace(0,m.gap_m,128)
for time in [0,10e-6,20e-6,35e-6,50e-6]:
    outgoing, reflected, total = mod.components(s,time,m)
    checks[f'superposition_{time:g}'] = bool(np.allclose(total,outgoing+reflected))
record = {'kind':'independent numerical model verification; not physical calibration',
          'model_path':str(path.relative_to(ROOT)), 'model_sha256':hashlib.sha256(path.read_bytes()).hexdigest(), 'checks':checks,
          'all_pass':all(checks.values()), 'roundtrip_s':roundtrip,
          'observed_first_return_s':first_nonzero(base)}
out=ROOT/'04-Production/Records/Tasks/T-051/Evidence/pressure-model-independent.json'
out.write_text(json.dumps(record,indent=2))
print(json.dumps(record))
if not record['all_pass']: raise SystemExit(1)
