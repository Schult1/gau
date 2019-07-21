import pandas as pd
import numpy as np
import os

def get_traffic_level(provider, json_data, stats = False):
    """Get Traffic Level from API Output.

    Parameters
    ----------
    provider : str
        Name of provider
    json_data:
        json data response
    stats: boolean
        boolean if additional stats are requested

    Returns
    -------
    int
        LOS representing Traffic Level i. e. 0: no traffic, 1: little traffic, 2: heavy traffic

    str
        text representation of loads

    stats:
        dict with additional stats
    """
    LOS_rep = {0: 'no traffic',
        1: 'little traffic',
        2: 'heavy traffic'}

    if provider == 'here':
        try:
            no_incidents = pd.DataFrame(json_data['TRAFFIC_ITEMS']['TRAFFIC_ITEM']).shape[0]
        except:
            no_incidents = 0

        if no_incidents == 0:
            LOS = 0
            rep = LOS_rep[LOS]
        elif no_incidents <=2:
            LOS = 1
            rep = LOS_rep[LOS]
        else:
            LOS = 2
            rep = LOS_rep[LOS]

        stat_dict = {}
        if stats:
            if LOS == 0:
                stat_dict = {'no_incidents': 0,
                    'crit_counts': 'NaN'}
            else:
                crit_counts = {}
                for i, row in pd.DataFrame(json_data['TRAFFIC_ITEMS']['TRAFFIC_ITEM']).iterrows():
                    crit_counts[row.CRITICALITY['ID']] = crit_counts.get(row.CRITICALITY['ID'], 0) + 1

                stat_dict = {'no_incidents': no_incidents,
                    'crit_counts': crit_counts}
            return {'LOS': LOS, 'text_rep': rep, 'stats': stat_dict}
    return {'LOS': LOS, 'text_rep': rep}
