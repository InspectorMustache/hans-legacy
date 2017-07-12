# this should just be a temporary file until I have determined what lists/dicts
# I actually want
# import re
from mappings import Mappings
import pickle
import jiantofan
import lessons
import storage
# from decomposer import Decompose, get_comp_dict, get_attr_dict

mappings = Mappings('mappings/heisig.txt')
jian_chars = list(mappings.jians.keys())
fan_chars = list(mappings.fans.keys())
all_chars = set(jian_chars + fan_chars)

comp_dict = storage.unpickle_object('heisig_ct.pickle')
comp_type_dict = storage.unpickle_object('heisig_ctd.pickle')
crel = jiantofan.ComponentRelation(mappings, comp_dict, comp_type_dict)

if __name__ == '__main__':
    # comp_type_dict = get_attr_dict(all_chars, 'comp_type')
    # storage.pickle_object(comp_type_dict, 'heisig_ctd.pickle')
    # comp_dict = get_comp_dict(all_chars)
    # storage.pickle_object(comp_dict, 'heisig_ct.pickle')
    lessons.create_lessons(crel)
    print('Döne.')
