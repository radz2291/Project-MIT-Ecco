"""B102 dimensional gate. No guessed production dimensions or implicit approval."""
import json
import math
from pathlib import Path

INCH = 0.0254
MIN_CASING_ID_M = 12.3 * INCH  # ENP3 datasheet, p3; not an actual well selection.


def radial_clearance(tool_od_m, passage_id_m, eccentricity_m=0.0):
    values = (tool_od_m, passage_id_m, eccentricity_m)
    if not all(isinstance(v, (int, float)) and not isinstance(v, bool)
               and math.isfinite(v) for v in values):
        raise ValueError('Dimensions must be finite numbers in metres')
    if tool_od_m <= 0 or passage_id_m <= 0 or eccentricity_m < 0:
        raise ValueError('Diameters must be positive; eccentricity nonnegative')
    return (passage_id_m - tool_od_m) / 2 - eccentricity_m


def validate_config(c, measured_tool_od_m):
    """Reject missing dimensions, unsupported deployment and conservative clashes.

    This is a straight, parallel-axis envelope check, not a drift/thread/trajectory
    certification. Each value needs a source; variation is illustrative geometry.
    """
    errors = []
    if c.get('scenario_status') != 'confirmed_by_producer':
        errors.append('O05: deployment scenario is not confirmed by producer')
    if not c.get('confirmation_reference'):
        errors.append('Missing inspectable deployment confirmation reference')
    required = ('hole_diameter_m', 'casing_id_m', 'casing_od_m',
                'cement_outer_diameter_m', 'span_m', 'axial_start_m',
                'eccentricity_m', 'irregular_amplitude_m',
                'spiral_amplitude_m', 'spiral_pitch_m')
    sources = c.get('sources', {})
    for k in required:
        v = c.get(k)
        if not isinstance(v, (float, int)) or isinstance(v, bool) or not math.isfinite(v):
            errors.append(f'{k}: missing finite numeric value in metres')
        elif k not in ('axial_start_m', 'eccentricity_m',
                        'irregular_amplitude_m', 'spiral_amplitude_m') and v <= 0:
            errors.append(f'{k}: must be positive')
        elif k in ('eccentricity_m', 'irregular_amplitude_m', 'spiral_amplitude_m') and v < 0:
            errors.append(f'{k}: must be nonnegative')
        if not sources.get(k):
            errors.append(f'{k}: missing source / approved illustrative instruction')
    if errors:
        return {'ready': False, 'errors': errors, 'clearances_m': {}}
    if 2*max(c['irregular_amplitude_m'],c['spiral_amplitude_m']) >= c['hole_diameter_m']:
        return {'ready': False, 'errors': ['Wall perturbation collapses the hole radius'], 'clearances_m': {}}
    if c['casing_id_m'] < MIN_CASING_ID_M:
        errors.append('Casing ID below published ENP3 minimum of 12.3 inches')
    if not c['casing_id_m'] < c['casing_od_m'] < c['cement_outer_diameter_m'] <= c['hole_diameter_m']:
        errors.append('Require casing ID < OD < cement outer diameter <= hole diameter')
    clearances = {
        'nominal': radial_clearance(measured_tool_od_m, c['hole_diameter_m'], c['eccentricity_m']),
        'irregular_conservative': radial_clearance(measured_tool_od_m,
            c['hole_diameter_m'] - 2*c['irregular_amplitude_m'], c['eccentricity_m']),
        'spiral_conservative': radial_clearance(measured_tool_od_m,
            c['hole_diameter_m'] - 2*c['spiral_amplitude_m'], c['eccentricity_m']),
        'cased': radial_clearance(measured_tool_od_m, c['casing_id_m'], c['eccentricity_m']),
    }
    for name, gap in clearances.items():
        if gap <= 0:
            errors.append(f'{name}: envelope contact/interference ({gap:.9f} m)')
    # Do not silently fabricate drill string/bit or assign source-end datums.
    for k in ('bha_library', 'bha_collection', 'bha_source', 'bha_interface_confirmation'):
        if not c.get(k):
            errors.append(f'{k}: missing inspected compatible assembly input')
    return {'ready': not errors, 'errors': errors, 'clearances_m': clearances,
            'limit': 'Straight coaxial envelope only; no thread, drift, shoe or deviated-interval acceptance'}


def brief_fit_study(tool_od_m):
    scenarios = [
        ('Datasheet minimum casing ID', 12.3, 'ID', 'Published minimum only; not selected deployment'),
        ('Chat 9:07 PM open hole example', 12.25, 'hole', 'Generic example; positive ideal gap does not establish deployment'),
        ('Chat 9:07 PM smaller hole example', 8.5, 'hole', 'Incompatible with inspected ENP3 envelope'),
        ('Chat 9:42 PM casing example', 9.625, 'OD', 'Even OD is smaller than tool; ID is smaller still'),
        ('Chat 9:42 PM smaller casing example', 7, 'OD', 'Even OD is smaller than tool; ID is smaller still'),
    ]
    return [{'source': name, 'diameter_inches': d, 'dimension_type': kind,
             'diameter_m': d*INCH, 'ideal_radial_gap_or_upper_bound_m': radial_clearance(tool_od_m,d*INCH),
             'disposition': note} for name,d,kind,note in scenarios]


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('config', type=Path)
    p.add_argument('--tool-od-m', type=float, required=True)
    a = p.parse_args()
    result = validate_config(json.loads(a.config.read_text(encoding='utf-8')), a.tool_od_m)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result['ready'] else 2)
