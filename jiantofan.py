class ComponentRelation(object):

    def __init__(self,
                 mappings,
                 comp_dict):
        self.jian_pool = mappings.jians.keys()
        self.fan_pool = mappings.fans.keys()
        self.mappings = mappings
        self.comp_dict = comp_dict

    def get_chars(self, component, charset=None):
        '''Return all Hanzi that contain component'''
        component_list = []

        charset = charset or 'jian'
        if charset == 'jian':
            pool = self.jian_pool
        elif charset == 'fan':
            pool = self.fan_pool

        for char in pool:
            if component in self.comp_dict[char]:
                component_list.append(char)
        print('Done.')
        return component_list

    def get_pairs(self, char, charset=None):
        '''Return matching chars from the other charset.'''
        pair_dict = {}
        mappings = self.mappings
        charset = charset or 'jian'
        if charset == 'jian':
            pair_dict[char] = mappings.jians[char]
        elif charset == 'fan':
            pair_dict[char] = mappings.fans[char]
