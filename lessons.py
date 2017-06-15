import jiantofan


def create_lessons(mappings, comp_dict):
    CR = jiantofan.ComponentRelation(mappings, comp_dict)
    learned_chars = []
    # call all lesson functions from here
    lesson_1(CR, learned_chars)


def lesson_1(CR, learned_chars):
    # CR = ComponentRelation('讠', '言')
    jian_list = CR.get_chars('讠')
    print(jian_list)
