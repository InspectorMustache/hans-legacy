def create_lessons(crel):
    learned_chars = {}
    # call all lesson functions from here
    lesson_1(crel, learned_chars)


def lesson_1(crel, learned_chars):
    # crel = ComponentRelation('讠', '言')
    jian_list = crel.get_chars('讠')
    print(jian_list)
