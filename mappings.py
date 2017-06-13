import re

parse_needle = re.compile(r'^([^:]+):(.+)')
rev_parse_needle = re.compile(r'^([^?]+)\?(.+)')


def get_mapping_dicts(mappings_file):
    with open(mappings_file, 'r') as m_file:
        jian_to_fan_dict = {}
        fan_to_jian_dict = {}

        for line in m_file.readlines():
            try:
                parsed = re.match(parse_needle, line)
                jian = parsed.group(1)
                fans = list_char_entrys(parsed.group(2))
                jian_to_fan_dict[jian] = fans

                for char in list_char_entrys(fans):
                    fan_to_jian_dict[char] = list_char_entrys(jian)

            except AttributeError:
                # assume there's a reverse mapping (with ?) in this case
                parsed = re.match(rev_parse_needle, line)
                fan = parsed.group(1)
                jians = list_char_entrys(parsed.group(2))
                fan_to_jian_dict[fan] = jians

    return jian_to_fan_dict, fan_to_jian_dict


def list_char_entrys(entry):
    char_list = []
    for char in entry:
        char_list.append(char)
    return char_list
