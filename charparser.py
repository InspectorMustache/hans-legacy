# this should just be a temporary file until I have determined what lists/dicts
# I actually want

import re

def get_char_list(input_file):
    char_list = []
    with open(input_file, 'r') as f:
        for line in f.readlines():
            char = re.sub(r'\d+\s+(\S+).+\n', r'\1', line)
            char_list.append(char)
    return char_list


rsh_chars = get_char_list('heisig/RSH.txt') 
rth_chars = get_char_list('heisig/RTH.txt') 
