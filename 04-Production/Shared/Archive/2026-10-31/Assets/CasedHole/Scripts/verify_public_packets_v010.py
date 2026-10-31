"""T46 public full-packet verifier against the exact T47 macro successor."""
import bpy,sys,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];A=ROOT/'04-Production/Shared/Assets';T=ROOT/'04-Production/Records/Tasks/T-047';sys.path.insert(0,str(A/'Acoustics/Scripts'))
from acoustic_verify_v002 import verify_packet
p=T/'Scenes/CasedSupport_v010.blend';bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False,use_scripts=False);s=bpy.context.scene;events=json.loads((T/'Evidence/actual-cased-events_v009.json').read_text())['events'];results=[verify_packet(e,frames=range(s.frame_start,s.frame_end+1),fps=24) for e in events]
out=dict(scene=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),passed=all(x['all_pass'] for x in results),public_verifier='Acoustics/Scripts/acoustic_verify_v002.py',public_verifier_sha256=hashlib.sha256((A/'Acoustics/Scripts/acoustic_verify_v002.py').read_bytes()).hexdigest(),packets=results,limits='Saved F-curve location channels authoritative for hidden objects; evaluated world matrices checked while visible. No bake change needed for viewport-hidden matrix cache.')
(T/'Evidence/public-packet-verification_v010.json').write_text(json.dumps(out,indent=2),encoding='utf8');print('T47_PUBLIC_PACKET_VERIFIER',out['passed'],[c for p in results for c in p['checks'] if not c['passed']],flush=True)
