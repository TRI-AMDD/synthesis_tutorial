from monty.serialization import loadfn
response = loadfn("response_1695169832817.json")
from s4.ml.features import wp_mp, wp_mp_median


def thermonize_reactions(reactions, using_mp=True, using_freed=True, processes=None):
    # Remove all oxygen del_O
    for k, d in reactions.items():
        if d['target'].get('thermo') is not None:
            d['target']['thermo'] = list(filter(
                lambda x: not (x['amts_vars'] or {}).get('del_O', 0.0) > 0.0,
                d['target']['thermo']
            ))

    if using_mp:
        reaction_data_mp = from_reactions_multiprocessing(
            reactions, list(reactions), processes=processes,
            override_fugacity={}, return_errors=True)
        print('Thermonized', len(reaction_data_mp), 'reactions using MP data.')
    else:
        reaction_data_mp = None

    if using_freed:
        reaction_data_freed = from_reactions(
            reactions, list(reactions), #processes=processes,
            override_fugacity={}, use_database='freed')
        print('Thermonized', len(reaction_data_mp), 'reactions using FREED data.')
    else:
        reaction_data_freed = None

    return reaction_data_mp, reaction_data_freed


def get_melt_features(precursor_list):
    precursors = tuple(sorted(precursors))
    melting_points = [wp_mp.get(Composition(x), wp_mp_median) for x in precursors]
    feature_dict = {
        'feature_exp_min_mp': min(melting_points),
        'feature_exp_max_mp': max(melting_points),
        'feature_exp_mean_mp': numpy.mean(melting_points),
        'feature_exp_div_mp': max(melting_points) - min(melting_points)}
    return feature_dict




data = {f"key{n}": value for n, value in enumerate(response['data'])} 
for key in data.keys():
    data[key]['target'].update({"thermo": [{"formula": "LiTiO3", "interpolation": "LiTiO3"}]})
    data[key]['target']['thermo'][0].update(data[key]['target'])


output = thermonize_reactions(data)