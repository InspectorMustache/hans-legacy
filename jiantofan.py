class ComponentRelation(object):
    """Retrieve information about character correspondences between the two
    charsets."""

    def __init__(self,
                 mappings,
                 comp_dict,
                 comp_type_dict):
        self.jian_pool = mappings.jians.keys()
        self.fan_pool = mappings.fans.keys()
        self.mappings = mappings
        self.comp_dict = comp_dict
        self.comp_type_dict = comp_type_dict

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
        """Check if one of the parent_comps of comp in char have comp_type. If
        comp_type is None, always return True."""
        if comp_type is None:
            return True
        else:
            parent_comps = self.get_parent_comps(char, comp)

            if len(parent_comps) == 0:
                parent_comps.append(char)

            for p_comp in parent_comps:
                if self.comp_type_dict[p_comp] == comp_type:
                    return True
                else:
                    return False

    def get_correspondence(self, char, charset=None):
        """Return matching chars from the other charset."""
        mappings = self.mappings
        charset = charset or 'jian'
        if charset == 'jian':
            return mappings.jians[char]
        elif charset == 'fan':
            return mappings.fans[char]

    def get_exceptions(self, jian_comp, fan_comp, comp_type=None):
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
        """Return a list of all (usually one) parent comps/chars of comp in
        char."""
        match_comp = []
        for char_comp in self.comp_type_dict[char]:
            decomp = self.comp_type_dict[char_comp]
            parts = [decomp.first_part, decomp.second_part]
            if comp in parts and '*' not in parts:
                match_comp.append(char_comp)
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
        lc_local = learned_chars.copy()
        found = 0
        while True:
            for jian in jians:

                # discard jian if it already has been learned
                if jian in lc_local:
                    continue
                else:
                    fan = self.get_correspondence(jian)

                # this isn't suitable for multi mappings because those need to
                # be learned with a different system
                if len(fan) > 1:
                    continue
                else:
                    fan = fan[0]

                # if fan_comp is not in fan, the rule we're checking doesn't apply
                if fan_comp not in self.comp_dict[fan]:
                    continue

                # create copies of comp_lists so no components get lost
                # also remove jian_comp and fan_comp from the respective lists for
                # comparing chars
                jian_comp_list = self.remove_component(jian,
                                                       jian_comp,
                                                       fan_comp)
                fan_comp_list = self.remove_component(fan,
                                                      fan_comp,
                                                      jian_comp)

                comps = {'jians': jian_comp_list,
                         'fans': fan_comp_list}

                if self.test_learnable(comps, lc_local):
                    learnable_pairs[jian] = fan

            if len(learnable_pairs) == found:
                break
            else:
                found = len(learnable_pairs)
                lc_local.update(learnable_pairs)

            return learnable_pairs

    def remove_component(self, char, comp, opposite_comp):
        """Remove comp including ALL of its subcomps from char and return a
        list of all components that are left."""
        # since we are removing things, create a copy of the list first
        comps = self.comp_dict[char].copy()
        comps.remove(comp)

        try:
            subcomps = self.comp_dict[comp]
            for subcomp in subcomps:
                comps.remove(subcomp)
        except ValueError as exc:
            # this should mean comp only has itself as subcomp
            if len(subcomps) == 1:
                pass
            else:
                raise exc

        # safely removing all bigger comps that contain comp should be possible
        # since the parts of them that are relevant have already been broken
        # off
        # also remove the character of the opposite set this should also be
        # safe
        # if it's not we need to change this to only delete comps that have a
        # corresponding component in the opposite comp_list
        comps_copy = comps.copy()
        for c_comp in comps_copy:
            if (comp in self.comp_dict[c_comp] or
                    opposite_comp in self.comp_dict[c_comp]):
                comps.remove(c_comp)

        return comps

    def test_learnable(self, comps, learned_chars):
        """Check if fan can be learned at this point."""
        # char is learnable if...
        # ... no components are left when all those that are identical have
        # been removed
        comps = self.remove_identical_comps(comps)
        if len(comps['jians']) + len(comps['fans']) == 0:
            return True
        # ... all non-identical components have been learned before
        comps = self.remove_learned_comps(comps, learned_chars)
        if len(comps['jians']) + len(comps['fans']) == 0:
            return True

        # otherwise they can not be learned
        return False

    def remove_identical_comps(self, comps):
        """Remove identical components of two component lists."""
        overlap = set(comps['jians']) & set(comps['fans'])

        for char in overlap:
            # also remove duplicates within the comp_lists
            comps['jians'] = [c for c in comps['jians'] if not (c in overlap)]
            comps['fans'] = [c for c in comps['fans'] if not (c in overlap)]
        return comps

    def remove_learned_comps(self, comps, learned_chars):
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

    def test_identical_fan(self, jian):
        """Check if a jian char maps to an identical fan char and no other
        chars."""
        fans = self.get_correspondence(jian)
        if len(fans) == 1 and jian == fans[0]:
            return True
        else:
            return False
