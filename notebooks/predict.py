from monty.serialization import loadfn
from s4.ml.features import wp_mp, wp_mp_median
from pymatgen.core import Composition
import numpy

response = loadfn("response_1695169832817.json")


def get_melt_features(precursors):
    """
    Gets melting point features
    
    Args:
        precursors (list): list of precursors
    """
    precursors = tuple(sorted(precursors))
    melting_points = [wp_mp.get(Composition(x), wp_mp_median) for x in precursors]
    feature_dict = {
        'feature_exp_min_mp': min(melting_points),
        'feature_exp_max_mp': max(melting_points),
        'feature_exp_mean_mp': numpy.mean(melting_points),
        'feature_exp_div_mp': max(melting_points) - min(melting_points)}
    return feature_dict


# For LiTiO3
print(get_melt_features(["Li2O2", "TiO2"]))