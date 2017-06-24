from textwrap import dedent
import os

if not os.path.exists('lessons'):
    os.mkdir('lessons')


def create_lessons(crel):
    learned_chars = {}
    # call all lesson functions from here
    lesson_1(crel, learned_chars)


def get_charmap_line(jian, fan):
    line = 'J[{}] -> F[{}]'.format(jian, fan)
    return line


def get_compmap_line(jian, fan):
    line = 'J<{}> -> F<{}>'.format(jian, fan)
    return line


def write_lesson_file(lines, lesson_name):
    with open('lessons/{}.txt'.format(lesson_name), 'w') as l_file:
        l_file.write('\n'.join(lines))


def lesson_1(crel, learned_chars):
    lines = []
    lines.append(dedent('''# This is the first lesson and by all probability also the largest. It contains all those simplified characters, of which you already know the traditional variant, meaning they are identical. These characters are not ordered in any meaningful way so this lesson mainly serves to give you a basic overview of the number of characters you will not have to learn anew.'''))
    lines.append('')
    rules = {}
    for jian in crel.jian_pool:
        if crel.test_identical_fan(jian):
            rules[jian] = crel.get_correspondence(jian)[0]

    for jian, fan in rules.items():
        lines.append(get_charmap_line(jian, fan))

    write_lesson_file(lines, 'lesson1')
