# this should just be a temporary file until I have determined what lists/dicts
# I actually want
# import re
import lessons
import decomposer
from mappings import Mappings

mappings = Mappings('mappings/heisig.txt')
jian_chars = list(mappings.jians.keys())
fan_chars = list(mappings.fans.keys())
all_chars = set(jian_chars + fan_chars)
comp_dict = decomposer.get_comp_dict(all_chars)

lessons.create_lessons(mappings, comp_dict)
