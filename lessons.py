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
    pass


def get_charmap_line(jian, fan, indent='', arrow='-->'):
    line = '{}J[{}] {} F[{}]'.format(indent, jian, arrow, fan)
    return line


def get_compmap_line(jian, fan, indent='', arrow='-->'):
    line = 'J{}<{}> {} F<{}>'.format(indent, jian, arrow, fan)
    return line


def charmap_list_to_lines(rules, lines, indent='\t', arrow='-->'):
    for jian, fan in rules.items():
        lines.append(get_charmap_line(jian, fan, indent='\t'))
    return lines


def get_rule_block(crel, jian, fan, learned_chars, **kwargs):
    """Get a list of lines consisting of a block of rules: First, the comp
    rules, than the resulting char rules. Also update learned_chars."""
    lines = []
    learned_chars.update({jian: fan})
    lines.append(get_compmap_line(jian, fan))
    rules = crel.get_learnables(jian, fan, learned_chars)
    learned_chars.update(rules)
    lines = charmap_list_to_lines(rules, lines, **kwargs)
    return lines


def write_lesson_file(lines, lesson_name):
    with open('lessons/{}.txt'.format(lesson_name), 'w') as l_file:
        l_file.write('\n'.join(lines))


def lesson_1(crel):
    lines = []
    lines.append(formatter.fill("""This is the first lesson and by all
        probability also the largest. It contains all those simplified
        characters, of which you already know the traditional variant, meaning
        they are identical. These characters are not ordered in any meaningful
        way so this lesson mainly serves to give you a basic overview of the
        number of characters you will not have to learn anew."""))
    lines.append('')
    lines.append(formatter.fill("""This lesson also establishes the basic
        syntax of this and all following lessons: A character is indicated by
        surrounding square brackets, while square brackets are preceded by
        either J or F, signaling a simplified (J:简体字) or traditional
        character (F:繁體字)."""))
    lines.append('')
    rules = {}
    for jian in crel.jian_pool:
        if crel.test_identical_fan(jian):
            rules[jian] = crel.get_correspondence(jian)[0]

    learned_chars.update(rules)
    lines = charmap_list_to_lines(rules, lines)

    write_lesson_file(lines, 'lesson1')


def lesson_2(crel):
    lines = []
    lines.append(formatter.fill("""This first rule is more of a variant writing
        (not a variant character). Thus, depending on the font you're using,
        you might not actually see any difference between the characters below.
        However, simplified and traditional characters that only differ with
        regards to this component, still occupy different unicode codepoints.
        So it's good to get this rule out of the way early on. The simplified
        character set unified this component to 兑, that is the variant with
        the two strokes on the top pointing inward. For traditional characters
        however, both variants are acceptable. From what I can tell, the one
        with the strokes pointing inward is more common in writing, while the
        other (兌) is more prevalent in printed text. It's probably sufficient
        to stick with the version you know from the simplified character
        set."""))
    lines.append('')
    lines.append(get_compmap_line('兑', '兌'))
    rules = crel.get_learnables('兌', '兌', learned_chars)
    learned_chars.update(rules)
    lines = charmap_list_to_lines(rules, lines)
    lines.append('\n')
    lines.append(formatter.fill("""These next three rules should also be rather
        easy to aquire. There are no exceptions to these rules, they cover a
        lot of characters and the components always occur in the same position,
        that is on the left of anotheer component. You should also already be
        familiar with the traditional form of the components as they exist as
        individual characters in both character sets with no differences."""))
    lines.append('')
    lines.append(formatter.fill("""The syntax for component rules differs from
        that for character rules. Angle brackets preceded by either J or F
        denote simplified or traditional components but they don't imply
        identical rules for corresponding characters."""))
    lines.append(formatter.fill("""So J<讠> --> F<言> doesn't mean J[讠] -->
        F[言]."""))
    lines.append('')

    lines.extend(get_rule_block(crel, '讠', '言', learned_chars))
    lines.append('')

    lines.extend(get_rule_block(crel, '钅', '金', learned_chars))
    lines.append('')

    lines.extend(get_rule_block(crel, '饣', '食', learned_chars))

    write_lesson_file(lines, 'lesson2')


def lesson_3(crel):
    print(learned_chars)
    lines = []
    lines.extend(get_rule_block(crel, '戋', '戔', learned_chars))
    write_lesson_file(lines, 'lesson3')
