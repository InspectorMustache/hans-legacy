# TODO: retrieve comp_type by dictionary to speed things up
from decomposer import Decompose


class ComponentRelation(object):

    def __init__(self,
                 mappings,
                 comp_dict):
        self.jian_pool = mappings.jians.keys()
        self.fan_pool = mappings.fans.keys()
        self.mappings = mappings
        self.comp_dict = comp_dict

    def get_chars(self, component, comp_type=None, charset=None):
        """Return all Hanzi that contain component with positional property
        comp_type."""
        charset = charset or 'jian'

        component_list = []

        if charset == 'jian':
            pool = self.jian_pool
        elif charset == 'fan':
            pool = self.fan_pool

        for char in pool:
            if component in self.comp_dict[char] \
             and self.test_for_comp_type(char, component, comp_type):
                component_list.append(char)
        return component_list

    def test_for_comp_type(self, char, comp, comp_type):
        """Check if one of the parent_comps in char have comp_type. Always
        return True if comp_type is None."""
        if comp_type is None:
            return True

        parent_comps = self.get_parent_comps(char, comp)
        if len(parent_comps) == 0:
            parent_comps.append(Decompose(char))
        for p_comp in parent_comps:
            if p_comp.comp_type == comp_type:
                return True
        return False

    def get_correspondence(self, char, charset=None):
        """Return matching chars from the other charset."""
        mappings = self.mappings
        charset = charset or 'jian'
        if charset == 'jian':
            return mappings.jians[char]
        elif charset == 'fan':
            return mappings.fans[char]

    def get_exceptions(self, jian_comp, fan_comp, comp_type):
        """Get exceptions for the rule [jian_comp -> fan_comp]. Comps
        positional properties have to be comp_type."""
        jians = self.get_chars(jian_comp, comp_type=comp_type)
        exceptions = {}
        for jian in jians:
            fans = self.get_correspondence(jian)
            # if it's a multi mapping automatically consider it an exception
            if len(fans) > 1:
                exceptions[jian] = fans
                continue

            # this is for chars that are only made up of provided comps
            if jian_comp == jian and fan_comp == fans[0]:
                continue

            if fan_comp not in self.comp_dict[fans[0]] \
               and jian_comp not in self.comp_dict[fans[0]]:
                exceptions[jian] = fans[0]
                continue

            if fan_comp not in self.comp_dict[fans[0]]:
                exceptions[jian] = fans[0]

        return exceptions

    def get_parent_comps(self, char, comp):
        """Return a list of all (usually one) parent comps/chars of comp as
        Decompose objects."""
        match_comp = []
        for decomp in Decompose(char).break_down_into_objects():
            parts = [decomp.first_part, decomp.second_part]
            if comp in parts and '*' not in parts:
                match_comp.append(decomp)
        return match_comp

    def count_comp_types(self, decomps, comp_type):
        counter = 0
        for decomp in decomps:
            if decomp.comp_type == comp_type:
                counter += 1
        return counter

    def get_learnables(self, jian_comp, fan_comp, learned_chars):
        """Get all chars that can be learned with the rule [jian_comp ->
        fan_comp]."""
        jians = self.get_chars(jian_comp)
        learnable_pairs = {}
        for jian in jians:

            # this isn't suitable for multi mappings because those need to be
            # learned with a different system
            fan = self.get_correspondence(jian)
            if len(fan) > 1:
                continue
            else:
                fan = fan[0]

            # create copies of comp_lists so no components get lost
            jian_comp_list = self.comp_dict[jian].copy()
            fan_comp_list = self.comp_dict[fan].copy()
            comps = {'jians': jian_comp_list,
                     'fans': fan_comp_list}
            comps['jians'].remove(jian_comp)
            comps['fans'].remove(fan_comp)

            if self.test_learnable(comps, learned_chars):
                learnable_pairs[jian] = fan

        return learnable_pairs

    def test_learnable(self, comps, learned_chars):
        """Check if fan can be learned at this point."""
        # char is learnable if...
        # ... no components are left when all those that are identical have
        # been removed
        comps = self.remove_identical(comps)
        if len(comps['jians']) + len(comps['fans']) == 0:
            return True
        # ... all non-identical components have been learned before
        comps = self.remove_learned(comps, learned_chars)
        if len(comps['jians']) + len(comps['fans']) == 0:
            return True

        # otherwise they can not be learned
        return False

    def remove_identical(self, comps):
        """Remove identical components of two component lists."""
        overlap = set(comps['jians']) & set(comps['fans'])

        for char in overlap:
            comps['jians'].remove(char)
            comps['fans'].remove(char)
        return comps

    def remove_learned(self, comps, learned_chars):
        """Remove all components that have been learned before from two
        component lists."""
        for jian in comps['jians']:
            try:
                if learned_chars[jian] in comps['fans']:
                    comps['jians'].remove(jian)
                    comps['fans'].remove(learned_chars[jian])
            except KeyError:
                pass
        return comps
