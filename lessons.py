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


class LessonWriter(object):
    "ContextManager for writing lessons providing some recurring functions."
    def __init__(self, name, crel):
        self.name = name
        self.crel = crel
        self.lines = []
        self.formatter = Formatter(width=80,
                                   initial_indent='# ',
                                   subsequent_indent='# ')

    def __enter__(self):
        return self

    def get_charmap_line(self, jian, fan, indent='', arrow='-->'):
        line = '{}J[{}] {} F[{}]'.format(indent, jian, arrow, fan)
        return line

    def get_compmap_line(self, jian, fan, indent='', arrow='-->'):
        line = 'J{}<{}> {} F<{}>'.format(indent, jian, arrow, fan)
        return line

    def append_charmap_as_lines(self, rules, indent='\t', arrow='-->',
                                terminator=None):
        for jian, fan in rules.items():
            self.lines.append(self.get_charmap_line(jian, fan, indent='\t'))
        if type(terminator) is str:
            self.lines.append(terminator)

    def append_char_rule_block(self, jian, fan, learned_chars, **kwargs):
        """Get a list of lines consisting of a block of rules: First, the
        underlying char rule, than the resulting char rules. Also update
        learned_chars."""
        learned_chars.update({jian: fan})
        self.lines.append(self.get_charmap_line(jian, fan))
        rules = self.crel.get_learnables(jian, fan, learned_chars)
        if rules is None:
            pass
        else:
            learned_chars.update(rules)
            self.append_charmap_as_lines(rules, **kwargs)

    def append_comp_rule_block(self, jian, fan, learned_chars, **kwargs):
        """Get a list of lines consisting of a block of rules: First, the
        underlying comp rules, than the resulting char rules. Also update
        learned_chars."""
        learned_chars.update({jian: fan})
        self.lines.append(self.get_compmap_line(jian, fan))
        rules = self.crel.get_learnables(jian, fan, learned_chars)
        if rules is None:
            pass
        else:
            learned_chars.update(rules)
            self.append_charmap_as_lines(rules, **kwargs)

    def append_comment(self, comment, terminator=None):
        self.lines.append(self.formatter.fill(comment))
        if type(terminator) is str:
            self.lines.append(terminator)

    def __exit__(self, type, value, traceback):
        with open('lessons/{}.txt'.format(self.name), 'w') as l_file:
            l_file.write('\n'.join(self.lines))


def create_lessons(crel):
    # call all lesson functions from here
    lesson_1(crel)
    lesson_2(crel)
    lesson_3(crel)


def lesson_1(crel):
    with LessonWriter('lesson1', crel) as lesson:
        lesson.append_comment('''This is the first lesson and by all
                probability also the largest. It contains all those simplified
                characters, of which you already know the traditional variant,
                meaning they are identical. These characters are not ordered in
                any meaningful way so this lesson mainly serves to give you a
                basic overview of the number of characters you will not have to
                learn anew.''', terminator='')
        lesson.append_comment('''This lesson also establishes the basic syntax
                of this and all following lessons: A character is indicated by
                surrounding square brackets, while square brackets are preceded
                by either J or F, signaling a simplified (J:简体字) or
                traditional character (F:繁體字).''', terminator='')

        rules = {}
        for jian in crel.jian_pool:
            if crel.test_identical_fan(jian):
                rules[jian] = crel.get_correspondence(jian)[0]

        learned_chars.update(rules)
        lesson.append_charmap_as_lines(rules)


def lesson_2(crel):
    with LessonWriter('lesson2', crel) as lesson:
        lesson.append_comment('''This first rule is more of a variant writing
                (not a variant character). Thus, depending on the font you're
                using, you might not actually see any difference between the
                characters below.  However, simplified and traditional
                characters that only differ with regards to this component,
                still occupy different unicode codepoints.  So it's good to get
                this rule out of the way early on. The simplified character set
                unified this component to 兑, that is the variant with the two
                strokes on the top pointing inward. For traditional characters
                however, both variants are acceptable. From what I can tell,
                the one with the strokes pointing inward is more common in
                writing, while the other (兌) is more prevalent in printed
                text. It's probably sufficient to stick with the version you
                know from the simplified character set.''')
        lesson.append_comp_rule_block('兌', '兌',
                                      learned_chars,
                                      terminator='\n')

        lesson.append_comment('''These next three rules should also be rather
                easy to aquire. There are no exceptions to these rules, they
                cover a lot of characters and the components always occur in
                the same position, that is on the left of anotheer component.
                You should also already be familiar with the traditional form
                of the components as they exist as individual characters in
                both character sets with no differences.''', terminator='')

        lesson.append_comment('''The syntax for component rules differs from
                that for character rules. Angle brackets preceded by either J
                or F denote simplified or traditional components but they don't
                imply identical rules for corresponding characters.''')
        lesson.append_comment('''So J<讠> --> F<言> doesn't mean J[讠] -->
                F[言].''', terminator='')

        lesson.append_comp_rule_block('讠', '言', learned_chars, terminator='')

        lesson.append_comp_rule_block('钅', '金', learned_chars, terminator='')

        lesson.append_comp_rule_block('饣', '食', learned_chars, terminator='')

        lesson.append_comment('''The traditional variant of this one does not
                appear in the simplified charset, however it occurs as commonly
                and is as consistent in its positioning as the other three.''')
        lesson.append_comp_rule_block('纟', '糹', learned_chars)


def lesson_3(crel):
    with LessonWriter('lesson3', crel) as lesson:
        lesson.append_comment('''The rules of this chapter concern characters
                that appear in more diverse positions than those of the last
                lesson but are still rather easy to learn.''', terminator='')
        lesson.append_comment('''Since you are most likely familiar with the
                character "目", this first rule should be simple to learn.''')

        lesson.append_char_rule_block('贝', '貝', learned_chars, terminator='')

        lesson.append_comment('''This is almost the same as the above rule with
                the exception of the right stroke at the bottom.''')
        lesson.append_char_rule_block('见', '見', learned_chars, terminator='')

        lesson.append_char_rule_block('丬', '爿', learned_chars, terminator='')

        lesson.append_char_rule_block('争', '爭', learned_chars, terminator='')

        lesson.append_char_rule_block('单', '單', learned_chars, terminator='')

        lesson.append_comment('''Yes, the "simplification" in this case consists of
                removing the one short line between the two 口.''')

        lesson.append_char_rule_block('吕', '呂', learned_chars)


def lesson_4(crel):
    pass
