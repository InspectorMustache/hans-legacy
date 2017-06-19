# this should just be a temporary file until I have determined what lists/dicts
# I actually want
# import re
from mappings import Mappings
import pickle
import jiantofan

mappings = Mappings('mappings/heisig.txt')
jian_chars = list(mappings.jians.keys())
fan_chars = list(mappings.fans.keys())
all_chars = set(jian_chars + fan_chars)

with open('crpickle', 'rb') as crp:
    comp_dict = pickle.load(crp)

crel = jiantofan.ComponentRelation(mappings, comp_dict)


# lessons.create_lessons(crel)
