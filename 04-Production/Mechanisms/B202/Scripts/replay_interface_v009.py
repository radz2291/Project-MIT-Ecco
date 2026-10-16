"""T27 data/pose adapter; applies a state without adding keyframes or motion."""
def apply_event_pose(control,event):
    p=event['tool_pose'];control['travel_m']=p['translation_m'][0];control['eccentric_y_m']=p['translation_m'][1];control['eccentric_z_m']=p['translation_m'][2];control['rotation_rad']=p['rotation_xyz_rad'][0];control['event_time_s']=event['timestamp_s'];control.update_tag()
def grid_at_time(events,config,case,t):
    # The inverse and aggregation see only available records. No future mean is
    # leaked into early replay. Use this for evolving partial-bin estimates.
    from acquisition_core_v009 import reconstruct,grid_samples
    return grid_samples(reconstruct(events,config),config,case,cutoff=t)
