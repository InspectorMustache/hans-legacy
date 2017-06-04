from decomposer import Decompose


class ComponentRelation(object):

    def __init__(self, jian_component, fan_component, jian_pool, fan_pool):
        self.jian_component = jian_component
        self.fan_component = fan_component
        self.jian_pool = jian_pool
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
