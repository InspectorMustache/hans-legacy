from decomposer import Decompose


class ComponentRelation(object):

    def __init__(self,
                 jian_component,
                 fan_component,
                 jian_pool,
                 mappings,
                 **kwargs):
        self.jian_component = jian_component
        self.fan_component = fan_component
        self.jian_pool = jian_pool
        self.jian_mappings = mappings.jians
        self.fan_mappings = mappings.fans
        if not fan_pool in kwargs:
            self.fan_pool = self.mappings.fans.keys()
        else:
            self.fan_pool = fan_pool
        self.jian_list = self.get_list_by_component(jian_component, jian_pool)
        self.fan_list = self.get_list_by_component(fan_component, fan_pool)

    def get_list_by_component(self, component, pool):
        '''Get a list of all Hanzi in $pool that contain $component.'''
        component_list = []
        for char in pool:
            print('Processing {}...'.format(char))
            if component in Decompose(char).break_down():
                component_list.append(char)
        return component_list

    def get_pairs(self, *args):
        pair_list = []
        if 'jian' in args:
            for char in self.jian_list:
                pair_list.append(self.make_pair_dict(char,
                                                     self.jian_mappings[char]))
        elif 'fan' in args:
            for char in self.fan_list:
                pair_list.append(self.make_pair_dict(char,
                                                     self.fan_mappings[char]))

    # def connect_pairs(self, chars, opposite_chars, mapping):
    #     pair_list = []
    #     for char in char_list:
    #         opposite = mapping[char]
    #         if opposite in opposite_chars

    def make_pair_dict(self, jian, fan):
        pair_dict = {}
        pair_dict['jian'] = jian
        pair_dict['fan'] = fan
        return pair_dict
