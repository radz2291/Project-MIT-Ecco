"""Complete per-case configuration provenance on the existing candidate.
No measurements, ground truth, grids, native scenes or images are changed.
The producer now writes these same effective parameters on a fresh build.
"""
import sys,hashlib
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[2];E=ROOT/'04-Production/Records/Tasks/T-008/Evidence/v009';sys.path.insert(0,str(BASE/'Scripts'))
from acquisition_core_v009 import *
path=BASE/'Data/v009/index_v009.json';index=read_json(path);config=read_json(BASE/'acquisition_config_v009.json');before=hashlib.sha256(path.read_bytes()).hexdigest()
for case,meta in index['cases'].items():
    meta['case_parameters']={'minimum_echo_strength':.9 if case=='weak_nominal' else config['minimum_echo_strength'],'orientations_per_depth':10 if case=='sparse_irregular' else config['tool_orientations_per_depth'],'max_ray_distance_m':.001 if case=='missed_nominal' else config['max_ray_distance_m'],'known_eccentric_yz_m':[.0007,-.0006] if case=='eccentric_nominal' else [0.,0.]}
write_json(path,index);after=hashlib.sha256(path.read_bytes()).hexdigest()
manifest=read_json(E/'consumer_manifest_v009.json');manifest['source_data_index_sha256']=after;write_json(E/'consumer_manifest_v009.json',manifest)
build=read_json(E/'build_acquisition_v009.json');build['index_sha256']=after;build['cases']=index['cases'];write_json(E/'build_acquisition_v009.json',build)
write_json(E/'metadata_completion_v009.json',{'before_index_sha256':before,'after_index_sha256':after,'scope':'Explicit effective per-case threshold/range/orientation/known-pose parameters only; no measurement, grid, scene or image edits. Producer emits same metadata on fresh build.'})
print('CASE_METADATA_COMPLETED')
