import decomposer


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
        return component_list

    def get_correspondence(self, char, charset=None):
        """Return matching chars from the other charset."""
        mappings = self.mappings
        charset = charset or 'jian'
        if charset == 'jian':
            return mappings.jians[char]
        elif charset == 'fan':
            return mappings.fans[char]

    def get_exceptions(self, jian_comp, fan_comp, learned_chars):
        """Get all chars that are an exception to the rule [jian_comp ->
        fan_comp]. This is based on learned rules and thus needs learned_chars.
        Returns lists as values, because multi mappings are also considered
        exceptions."""
        # real exceptions are very hard to find since we'd need all other jian
        # -> fan rules to isolate them, so instead we're using all rules
        # already learned
        jians = self.get_chars(jian_comp)
        exceptions = {}
        for jian in jians:
            fans = self.get_correspondence(jian)
            # if it's a multi mapping automatically consider it an exception
            if len(fans) > 1:
                exceptions[jian] = fans
                continue

            elif jian_comp == jian and fan_comp == fans[0]:
                # this is for chars that are only made up of provided comps
                continue

            elif fan_comp not in self.comp_dict[fans[0]]:
                fan = fans[0]

                # TODO: use Decompose.break_down_into_objects() to compare if
                # components are actually the same by looking at their
                # positional arrangement, i.e. their comp_type

                # jian_comp_list = self.comp_dict[jian].copy()
                # fan_comp_list = self.comp_dict[fan].copy()
                # comps = {'jians': jian_comp_list,
                #          'fans': fan_comp_list}
                # comps = self.remove_identical(comps)
                # # comps = self.remove_learned(comps, learned_chars)

                # # if there's no comps left at this point, it's not an exception
                # if jian == '凤' or jian == '饥':
                #     import pdb; pdb.set_trace()
                # if len(comps['jians']) + len(comps['fans']) == 0:
                #     continue
                # elif jian_comp in jian and fan_comp not in comps['fans']:
                #     exceptions[jian] = fans

        return exceptions

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
