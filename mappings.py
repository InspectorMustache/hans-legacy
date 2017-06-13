import re

parse_needle = re.compile(r'^([^:]+):(.+)')
rev_parse_needle = re.compile(r'^([^?]+)\?(.+)')


class Mappings(object):
    def __init__(self, mappings_file):
        self.mappings_file = mappings_file
        self.jians, self.fans = self.get_mapping_dicts()

    def get_mapping_dicts(self):
        with open(self.mappings_file, 'r') as m_file:
            jian_to_fan_dict = {}
            fan_to_jian_dict = {}

            for line in m_file.readlines():
                try:
                    parsed = re.match(parse_needle, line)
                    jian = parsed.group(1)
                    fans = self.list_char_entrys(parsed.group(2))
                    jian_to_fan_dict[jian] = fans

                    for char in self.list_char_entrys(fans):
                        fan_to_jian_dict[char] = self.list_char_entrys(jian)

                except AttributeError:
                    # assume there's a reverse mapping (with ?) in this case
                    parsed = re.match(rev_parse_needle, line)
                    fan = parsed.group(1)
                    jians = self.list_char_entrys(parsed.group(2))
                    fan_to_jian_dict[fan] = jians

        return jian_to_fan_dict, fan_to_jian_dict


    def list_char_entrys(self, entry):
        char_list = []
        for char in entry:
            char_list.append(char)
        return char_list
