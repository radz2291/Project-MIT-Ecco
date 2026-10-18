"""T45 immutable baseline and shared-event verification (ordinary Python)."""
import argparse
import hashlib
import json
import math
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def check_event(event):
    contract = json.loads((HERE / 'event-contract_v001.json').read_text(encoding='utf-8'))
    checks = []
    def ck(name, value):
        checks.append({'check': name, 'pass': bool(value)})
    ck('required_fields', all(k in event for k in contract['required']))
    if not checks[-1]['pass']:
        return checks
    ck('same_sensor', event['emitter_ref'] == event['receiver_ref'])
    ck('time_order', event['send_s'] < event['contact_s'] < event['receive_s'])
    ck('opacity_lifetime', 0 <= event['opacity'] <= 1 and event['patch_lifetime_s'] > 0)
    ck('provenance', event['provenance'] in contract['provenance_values'])
    ck('finite_timing', all(math.isfinite(event[k]) for k in ['send_s','contact_s','receive_s','patch_lifetime_s']))
    for name in ['emitter_world_m', 'direction_world', 'hit_world_m', 'normal_world']:
        v = event[name]
        ck(name + '_finite_vector', len(v) == 3 and all(math.isfinite(x) for x in v))
        if name in ['direction_world', 'normal_world']:
            ck(name + '_unit', abs(sum(x*x for x in v)-1) < 1e-4)
    delta = [event['hit_world_m'][i]-event['emitter_world_m'][i] for i in range(3)]
    projected = sum(delta[i]*event['direction_world'][i] for i in range(3))
    residual = math.sqrt(sum((delta[i]-projected*event['direction_world'][i])**2 for i in range(3)))
    ck('forward_collinear_hit', projected > 0 and residual < 2e-5)
    ck('wall_normal_faces_emitter', sum(event['normal_world'][i]*event['direction_world'][i] for i in range(3)) < 0)
    source = event['wall_source']
    ck('wall_source_fields', isinstance(source,dict) and all(k in source for k in ['library','object','version','sha256']))
    if checks[-1]['pass']:
        path = Path(source['library'])
        if not path.is_absolute():
            path = ROOT/path
        ck('exact_wall_source_hash', path.is_file() and sha(path)==source['sha256'])
    if event['provenance']=='native_ray_intersection_illustrative_timing':
        ck('native_reference_identity', all(k in event for k in ['reference_world_m','reference_pose_world','emitter_local_m','emitter_surface']))
        surface=event.get('emitter_surface')
        ck('native_surface_metadata',isinstance(surface,dict) and all(k in surface for k in ['object','library','sha256','face_index','offset_from_reference_m']))
        if isinstance(surface,dict) and checks[-1]['pass']:
            path=Path(surface['library'])
            if not path.is_absolute():path=ROOT/path
            ck('exact_emitter_surface_hash',path.is_file() and sha(path)==surface['sha256'])
            offset=surface['offset_from_reference_m']
            ck('bounded_surface_offset',math.isfinite(offset) and 0<=offset<.025)
            if 'reference_world_m' in event:
                measured=sum((event['emitter_world_m'][i]-event['reference_world_m'][i])*event['direction_world'][i] for i in range(3))
                ck('surface_offset_matches_geometry_record',abs(measured-offset)<2e-5)
        packet_fields=contract['packet_timing_extension']['required_native_fields']
        ck('declared_packet_timing',all(k in event for k in packet_fields))
        if all(k in event for k in packet_fields):
            ck('packet_end_and_emitter_hold',abs(event['packet_end_s']-event['receive_s']-.14)<1e-8 and event['hold_emitter_until_s']>=event['packet_end_s'])
            arcs=event['arc_phases']
            ck('exact_three_arc_phases',len(arcs)==3)
            for i,a in enumerate(arcs):
                lag=i*.07
                ck('arc_'+str(i+1)+'_leading_phase',a['arc_index']==i+1 and abs(a['lag_s']-lag)<1e-8 and all(abs(a[k]-event[k]-lag)<1e-8 for k in ['send_s','contact_s','receive_s']))
    return checks

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--events', type=Path)
    p.add_argument('--upstream',choices=['v006','v007'],default='v007')
    p.add_argument('--output', type=Path, default=HERE/'Evidence/baseline-freeze_v001.json')
    args = p.parse_args()
    manifest_path = ROOT/('04-Production/Shared/Assets/World/manifest_'+args.upstream+'.json')
    manifest = json.loads(manifest_path.read_text(encoding='utf-8-sig'))
    rows = []
    for item in manifest['artifacts']:
        path = ROOT/item['path']
        actual = sha(path) if path.exists() else None
        rows.append({'path':item['path'], 'expected_sha256':item['sha256'],
                     'actual_sha256':actual, 'bytes':path.stat().st_size if path.exists() else None,
                     'pass':actual == item['sha256']})
    frozen=json.loads((ROOT/'04-Production/Shared/Assets/World/manifest_v006.json').read_text(encoding='utf-8-sig'))
    for rel in frozen['reused_unchanged']:
        path = ROOT/'04-Production/Shared/Assets'/rel
        rows.append({'path':path.relative_to(ROOT).as_posix(), 'sha256':sha(path),
                     'bytes':path.stat().st_size, 'pass':True, 'role':'frozen_nested_dependency'})
    for item in frozen['artifacts'] if args.upstream=='v007' else []:
        path=ROOT/item['path']
        actual=sha(path) if path.exists() else None
        rows.append({'path':item['path'],'expected_sha256':item['sha256'],'actual_sha256':actual,'pass':actual==item['sha256'],'role':'preserved_predecessor'})
    result = {'task':'T45', 'accepted_source_commit':'a08d0ecfbd6f3241298f506b3ea42613388b3baf' if args.upstream=='v007' else 'df1bc5626e820dc3a0b9af286bfcca4ce498d8c0',
              'manifest_sha256':sha(manifest_path), 'baseline':rows,
              'baseline_pass':all(x['pass'] for x in rows),
              'storage':'Native files local/Git-ignored; no off-machine backup established'}
    if args.events:
        data = json.loads(args.events.read_text(encoding='utf-8-sig'))
        events = data if isinstance(data,list) else data.get('events',[data])
        result['events'] = [{'event_id':e.get('event_id'), 'checks':check_event(e)} for e in events]
        result['events_pass'] = all(c['pass'] for e in result['events'] for c in e['checks'])
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'baseline_pass':result['baseline_pass'], 'baseline_files':len(rows),
                      'events_pass':result.get('events_pass'), 'output':str(args.output)}))
    if not result['baseline_pass'] or result.get('events_pass') is False:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
