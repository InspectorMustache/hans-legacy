# this should just be a temporary file until I have determined what lists/dicts
# I actually want
# import re
from mappings import Mappings
import pickle
import jiantofan
import lessons
if __name__ != '__main__':
    from decomposer import Decompose

mappings = Mappings('mappings/heisig.txt')
jian_chars = list(mappings.jians.keys())
fan_chars = list(mappings.fans.keys())
all_chars = set(jian_chars + fan_chars)

with open('c_dict.pickle', 'rb') as cdp_file:
    comp_dict = pickle.load(cdp_file)

with open('ct_dict.pickle', 'rb') as ctdp_file:
    comp_type_dict = pickle.load(ctdp_file)

crel = jiantofan.ComponentRelation(mappings, comp_dict, comp_type_dict)

if __name__ == '__main__':
    # lessons.create_lessons(crel)
    lessons.lesson_3(crel)
    print('Döne.')
