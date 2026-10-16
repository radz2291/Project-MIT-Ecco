"""Pure-Python synthetic forward response and inverse/grid mapping.
The inverse accepts measurement records only; ground-truth intersections are
kept separately by the Blender producer. No proprietary ENP3 processing.
"""
import math,json,gzip,hashlib
from pathlib import Path
def write_json(path,value):
    path=Path(path);raw=json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
    if path.suffix=='.gz':
        with path.open('wb') as f:
            with gzip.GzipFile(filename='',mode='wb',fileobj=f,mtime=0) as z:z.write(raw)
    else:path.write_bytes(raw)
def read_json(path):
    p=Path(path);return json.loads(gzip.decompress(p.read_bytes()) if p.suffix=='.gz' else p.read_text())
def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
def material_response(point,model,c):
    x,y,z=point;zone='constant';scatter=1.;Z=c['constant_impedance_rayl']
    if model=='changed_constant':
        if 2.4<=x<3.35:Z=c['material_change_impedance_rayl'];zone='changed_layer'
    elif model=='layers':
        b=c['inclined_boundary'];boundary=b['x_m']+b['slope_y']*y+b['slope_z']*z
        idx=0 if x<c['layer_first_boundary_x_m'] else (1 if x<boundary else 2)
        Z=c['layer_impedances_rayl'][idx];zone='synthetic_layer_'+str(idx)
        p=c['weak_patch'];inside=sum(((v-a)/r)**2 for v,a,r in zip(point,p['center_m'],p['radii_m']))<1
        if inside:scatter=p['coherent_strength_factor'];zone+=' / synthetic weak patch'
    Zmud=c['mud_density_kg_m3']*c['mud_sound_speed_m_s'];rho=abs(Z-Zmud)/(Z+Zmud)
    return {'material_zone':zone,'impedance_rayl':Z,'mud_impedance_rayl':Zmud,'reflectivity':rho,'coherent_patch_factor':scatter}
def forward_echo(point,stand_off,incidence,model,c):
    m=material_response(point,model,c);incidence_factor=max(0.,min(1.,incidence))**c['incidence_exponent']
    attenuation=math.exp(-2*c['mud_attenuation_np_m']*stand_off)
    range_factor=(c['range_reference_m']/(c['range_reference_m']+stand_off))**2
    strength=c['transmit_scale']*m['reflectivity']*m['coherent_patch_factor']*incidence_factor*attenuation*range_factor
    return strength,{**m,'incidence_factor':incidence_factor,'attenuation_2way':attenuation,'range_factor':range_factor}
def reconstruct(events,c):
    """No wall mesh, truth hits, material properties or source radii accepted."""
    processed=[];ay,az=c['axis_yz_m']
    for e in events:
        if not e['valid_tof']:continue
        d=.5*e['mud_sound_speed_m_s']*e['tof_2way_s'];p=[a+d*b for a,b in zip(e['sensor_origin_m'],e['outward_direction'])]
        theta=math.atan2(p[2]-az,p[1]-ay)%math.tau;r=math.hypot(p[1]-ay,p[2]-az)
        processed.append({'sample_id':e['id'],'timestamp_s':e['timestamp_s'],'sensor_id':e['sensor_id'],'position_m':p,'x_m':p[0],'azimuth_rad':theta,'radius_m':r,'delta_radius_m':r-c['nominal_radius_m'],'echo_strength':e['echo_strength'] if e['valid_amplitude'] else None,'valid_amplitude':e['valid_amplitude']})
    return processed
def grid_samples(samples,c,case,cutoff=None,interpolate=False):
    depths=c['depths_m'];n=c['azimuth_bins'];bins=[[] for _ in range(len(depths)*n)]
    for p in samples:
        if cutoff is not None and p['timestamp_s']>cutoff:continue
        di=min(range(len(depths)),key=lambda i:abs(depths[i]-p['x_m']))
        if abs(depths[di]-p['x_m'])>.126:continue
        ai=int(p['azimuth_rad']/math.tau*n)%n;bins[di*n+ai].append(p)
    cells=[]
    for i,ps in enumerate(bins):
        di,ai=divmod(i,n);cell={'index':i,'x_m':depths[di],'azimuth_rad':(ai+.5)*math.tau/n,'measured':bool(ps),'interpolated':False,'valid_geometry':bool(ps),'valid_amplitude':False,'radius_m':None,'delta_radius_m':None,'echo_strength':None,'event_ids':[],'weights':[],'first_timestamp_s':None,'ready_timestamp_s':None,'count':len(ps)}
        if ps:
            r=sum(p['radius_m'] for p in ps)/len(ps);amp=[p for p in ps if p['valid_amplitude']]
            cell.update(radius_m=r,delta_radius_m=r-c['nominal_radius_m'],event_ids=[p['sample_id'] for p in ps],weights=[1/len(ps)]*len(ps),first_timestamp_s=min(p['timestamp_s'] for p in ps),ready_timestamp_s=max(p['timestamp_s'] for p in ps))
            if amp:cell.update(valid_amplitude=True,echo_strength=sum(p['echo_strength'] for p in amp)/len(amp),amplitude_event_ids=[p['sample_id'] for p in amp],amplitude_weights=[1/len(amp)]*len(amp))
        cells.append(cell)
    # Optional isolated one-bin gap fill only. Never bridge large sparse arcs or
    # extrapolate depth; provenance records contributing bins/events/weights.
    if interpolate:
        measured=[dict(x) for x in cells]
        for i,p in enumerate(measured):
            if p['measured']:continue
            di,ai=divmod(i,n);left=measured[di*n+(ai-1)%n];right=measured[di*n+(ai+1)%n]
            if left['measured'] and right['measured']:
                r=.5*(left['radius_m']+right['radius_m']);ampvalid=left['valid_amplitude'] and right['valid_amplitude']
                cells[i].update(interpolated=True,valid_geometry=True,radius_m=r,delta_radius_m=r-c['nominal_radius_m'],valid_amplitude=ampvalid,echo_strength=.5*(left['echo_strength']+right['echo_strength']) if ampvalid else None,interpolation_sources=[left['index'],right['index']],event_ids=left['event_ids']+right['event_ids'],weights=[.5*w for w in left['weights']]+[.5*w for w in right['weights']],first_timestamp_s=max(left['first_timestamp_s'],right['first_timestamp_s']),ready_timestamp_s=max(left['ready_timestamp_s'],right['ready_timestamp_s']))
                if ampvalid:cells[i].update(amplitude_event_ids=left['amplitude_event_ids']+right['amplitude_event_ids'],amplitude_weights=[.5*w for w in left['amplitude_weights']]+[.5*w for w in right['amplitude_weights']])
    return {'case':case,'source_kind':'synthetic_illustrative','depths_m':depths,'azimuth_bins':n,'reference_axis_yz_m':c['axis_yz_m'],'interpolation_enabled':interpolate,'aggregation':'arithmetic mean of valid hits assigned to nearest configured depth and azimuth bin; fixed grid centers','cells':cells}
def mesh_from_grid(grid,cutoff=None,show_interpolated=False):
    """All positions from reconstructed radii, never source wall coordinates.
    At a time cutoff use the raw-event regridding function first; default ready
    timestamps conservatively reveal only completed bins, not future averages.
    """
    vs=[];indices=[];mapping={};n=grid['azimuth_bins'];ay,az=grid['reference_axis_yz_m']
    for p in grid['cells']:
        if not p['valid_geometry'] or (p['interpolated'] and not show_interpolated):continue
        if cutoff is not None and p['ready_timestamp_s']>cutoff:continue
        r=p['radius_m'];theta=p['azimuth_rad'];mapping[p['index']]=len(vs);indices.append(p['index']);vs.append((p['x_m'],ay+r*math.cos(theta),az+r*math.sin(theta)))
    faces=[]
    for di in range(len(grid['depths_m'])-1):
        for ai in range(n):
            ids=[di*n+ai,di*n+(ai+1)%n,(di+1)*n+(ai+1)%n,(di+1)*n+ai]
            if all(i in mapping for i in ids):faces.append(tuple(mapping[i] for i in ids))
    return vs,faces,indices
