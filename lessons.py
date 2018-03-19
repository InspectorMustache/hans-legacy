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

    def get_charmap_line(self, jian, fan, rule=None, indent='', arrow='-->'):
        rule_frag = ' !{}'.format(rule) if rule else ''
        line = 'J{}<{}> {} F<{}>{}'.format(indent, jian, arrow, fan, rule_frag)
        return line

    def get_compmap_line(self, jian, fan, rule=None, indent='', arrow='-->'):
        rule_frag = ' !{}'.format(rule) if rule else ''
        line = 'J{}<{}> {} F<{}>{}'.format(indent, jian, arrow, fan, rule_frag)
        return line

    def append_charmap_as_lines(self, rules, terminator=None, **kwargs):
        for jian, fan in rules.items():
            self.lines.append(self.get_charmap_line(jian, fan, **kwargs))
        if type(terminator) is str:
            self.lines.append(terminator)

    def append_char_rule_block(self, jian, fan,
                               learned_chars, comp_type=None, **kwargs):
        """Get a list of lines consisting of a block of rules: First, the
        underlying char rule, than the resulting char rules. Also update
        learned_chars."""
        learned_chars.update({jian: fan})
        self.lines.append(self.get_charmap_line(jian, fan, comp_type))
        rules = self.crel.get_learnables(jian, fan, learned_chars, comp_type)
        if rules is None:
            pass
        else:
            learned_chars.update(rules)
            self.append_charmap_as_lines(rules, **kwargs)

    def append_comp_rule_block(self, jian, fan,
                               learned_chars, comp_type=None, **kwargs):
        """Get a list of lines consisting of a block of rules: First, the
        underlying comp rules, than the resulting char rules. Also update
        learned_chars."""
        learned_chars.update({jian: fan})
        self.lines.append(self.get_compmap_line(jian, fan, comp_type))
        rules = self.crel.get_learnables(jian, fan, learned_chars, comp_type)
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
    lesson_4(crel)


def lesson_1(crel):
    with LessonWriter('lesson1', crel) as lesson:
        rules = {}
        for jian in crel.jian_pool:
            if crel.test_identical_fan(jian):
                rules[jian] = crel.get_correspondence(jian)[0]
        learned_chars.update(rules)
        lesson.append_charmap_as_lines(rules)


def lesson_2(crel):
    with LessonWriter('lesson2', crel) as lesson:
        lesson.append_comp_rule_block('兌', '兌', learned_chars, terminator='')
        lesson.append_comp_rule_block('钅', '金', learned_chars, terminator='')
        lesson.append_comp_rule_block('饣', '食', learned_chars, terminator='')
        lesson.append_comp_rule_block('纟', '糹', learned_chars)


def lesson_3(crel):
    with LessonWriter('lesson3', crel) as lesson:
        lesson.append_char_rule_block('贝', '貝', learned_chars, terminator='')
        lesson.append_char_rule_block('见', '見', learned_chars, terminator='')
        # lesson.append_char_rule_block('丬', '爿', learned_chars, terminator='')
        lesson.append_char_rule_block('争', '爭', learned_chars, terminator='')
        # lesson.append_char_rule_block('单', '單', learned_chars, terminator='')
        lesson.append_char_rule_block('吕', '呂', learned_chars, terminator='')
        lesson.append_comp_rule_block('艹', '炏', learned_chars, comp_type='冖')


def lesson_4(crel):
    with LessonWriter('lesson4', crel) as lesson:
        lesson.append_char_rule_block('鱼', '魚', learned_chars, terminator='')
        lesson.append_char_rule_block('马', '馬', learned_chars, terminator='')
        lesson.append_char_rule_block('鸟', '鳥', learned_chars, terminator='')
        lesson.append_char_rule_block('乌', '烏', learned_chars, terminator='')
        lesson.append_char_rule_block('龙', '龍', learned_chars, terminator='')
        lesson.append_char_rule_block('黾', '黽', learned_chars, terminator='')
        lesson.append_char_rule_block('龟', '龜', learned_chars, terminator='')
        lesson.append_char_rule_block('东', '東', learned_chars, terminator='')
        # what's going on here?
        lesson.append_comp_rule_block('柬', '東', learned_chars, terminator='')
        lesson.append_comp_rule_block('车', '車', learned_chars)
