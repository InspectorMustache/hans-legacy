import textwrap
import os
import re

learned_chars = {}

if not os.path.exists('lessons'):
    os.mkdir('lessons')


class Formatter(textwrap.TextWrapper):
    def fill(self, text):
        text = re.sub(r'\s+', ' ', text)
        return super().fill(text)


formatter = Formatter(width=80,
                      initial_indent='# ',
                      subsequent_indent='# ')


def create_lessons(crel):
    # call all lesson functions from here
    lesson_1(crel)


def get_charmap_line(jian, fan, indent='', arrow='-->'):
    line = '{}J[{}] {} F[{}]'.format(indent, jian, arrow, fan)
    return line


def get_compmap_line(jian, fan, indent='', arrow='-->'):
    line = 'J{}<{}> {} F<{}>'.format(indent, jian, arrow, fan)
    return line


def charmap_lines_to_list(rules, lines, indent='\t', arrow='-->'):
    for jian, fan in rules.items():
        lines.append(get_charmap_line(jian, fan, indent='\t'))
    return lines


def write_lesson_file(lines, lesson_name):
    with open('lessons/{}.txt'.format(lesson_name), 'w') as l_file:
        l_file.write('\n'.join(lines))


def lesson_1(crel):
    lines = []
    lines.append(formatter.fill('''This is the first lesson and by all
        probability also the largest. It contains all those simplified
        characters, of which you already know the traditional variant, meaning
        they are identical. These characters are not ordered in any meaningful
        way so this lesson mainly serves to give you a basic overview of the
        number of characters you will not have to learn anew.'''))
    lines.append('')
    lines.append(formatter.fill('''This lesson also establishes the basic
        syntax of this and all following lessons: A character is indicated by
        surrounding square brackets, while square brackets are preceded by
        either J or F, signaling a simplified (J:简体字) or traditional
        character (F:繁體字).'''))
    lines.append('')
    rules = {}
    for jian in crel.jian_pool:
        if crel.test_identical_fan(jian):
            rules[jian] = crel.get_correspondence(jian)[0]

    lines = charmap_lines_to_list(rules, lines)

    write_lesson_file(lines, 'lesson1')


def lesson_2(crel):
    lines = []
    lines.append(get_compmap_line('兑', '兌'))
    rules = crel.get_learnables('兌', '兌', learned_chars)
    lines = charmap_lines_to_list(rules, lines)
    write_lesson_file(lines, 'lesson2')


def lesson_3(crel):
    lines = []
    lines.append(get_compmap_line('讠', '言'))
    rules = crel.get_learnables('讠', '言', learned_chars)
    exceptions = crel.get_exceptions('讠', '言')
    lines = charmap_lines_to_list(rules, lines)
    lines = charmap_lines_to_list(exceptions, lines, arrow='!->')
    write_lesson_file(lines, 'lesson3')
