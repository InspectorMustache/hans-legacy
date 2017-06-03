from bs4 import BeautifulSoup
from requests import get as download
import re

WIKI_DECOMP_URL = 'https://commons.wikimedia.org/wiki/Commons:Chinese_characters_decomposition'


def download_table(table_url):
    '''Returns a BeautifulSoup ResultSet with all tables from the WikiCommons
    Hanzi decomposition project. Each table is contained in a <pre> tag.'''
    # get a list of all <pre>-elements
    print('Downloading from {}...'.format(table_url), end='')
    decomp_html = download(table_url).text
    print('Done.')
    decomp_soup = BeautifulSoup(decomp_html,
                                'html.parser').find_all('pre')
    # remove first part that describes the table
    if re.search(r'1\.[^2]+2\.', decomp_soup[0].string, re.DOTALL):
        decomp_soup.pop(0)

    return decomp_soup


def get_decomp_list(decomp_soup):
    '''Make a list out of the table soup object.'''
    decomp_list = []
    for pre in decomp_soup:
        for line in pre.string.splitlines():
            if not re.match(r'^\s*$', line):
                decomp_list.append(line)

    return decomp_list


wiki_decomp_soup = download_table(WIKI_DECOMP_URL)
wiki_decomp_list = get_decomp_list(wiki_decomp_soup)


class Decompose(object):

    def __init__(self, key_char, decomp_table=wiki_decomp_list):
        self.key_char = key_char
        self.decomp_table = decomp_table
        self.value_string = self.get_value_string()
        self.sub_string = re.compile(r'\s+(\d+)\s+(\S+)\s+(\S+)\s+(\d+)\s+(\*| |\?)\s+(\S+)\s+(\d+)\s+(\*| |\?)\s+(\S+)\s+(\S+)$')
        self.strokes_all,\
            self.comp_type,\
            self.first_part,\
            self.strokes_first,\
            self.verify_first,\
            self.second_part,\
            self.strokes_second,\
            self.verify_second,\
            self.cangjie,\
            self.radical = self.get_values(self.value_string)

    def get_value_string(self):
        # handle IndexErrors in case we search for a char that's not in the
        # table, this is mainly needed for the break_down function
        for line in wiki_decomp_list:
            if re.search(r'^\s+{}.+$'.format(self.key_char), line):
                return re.sub(r'^\s+{}(.+$)'.format(self.key_char),
                              r'\1',
                              line)
        return 'Undefined'

#         try:
#             value_string = re.findall(r'^\s+{}.+$'.format(self.key_char), self.decomp_table,
#                     re.M)[0]
#         except IndexError:
#             value_string = 'Undefined'
#         else:
#             value_string = re.sub(r'^\s+{}(.+$)'.format(self.key_char), r'\1',
#                     value_string)

#         return value_string

    def get_values(self, value_string):
        if re.match(self.sub_string, value_string):
            strokes_all, comp_type, first_part, strokes_first, verify_first,\
                second_part, strokes_second, verify_second, cangjie, radical =\
                re.sub(self.sub_string,
                       r'\1°\2°\3°\4°\5°\6°\7°\8°\9°\10',
                       value_string).split('°')
        else:
            strokes_all = comp_type = first_part = strokes_first =\
                 verify_first = second_part = strokes_second = verify_second =\
                 cangjie = radical = 'Undefined'

        return strokes_all, comp_type, first_part, strokes_first,\
            verify_first, second_part, strokes_second, verify_second, cangjie,\
            radical

    def break_down(self):
        if self.first_part == 'Undefined':
            return []

        keychar1 = self.first_part
        keychar2 = self.second_part
        parts = []
        self.break_down_loop(keychar1, keychar2, parts)
        return parts

    def break_down_loop(self, keychar1, keychar2, parts):
        char_list = self.populate_char_list(keychar1, keychar2)
        for char in char_list:
            char_decomp = Decompose(char)
            if char_decomp.first_part == 'Undefined':
                parts.append(char)
            elif char_decomp.strokes_all == 1:
                parts.append(char)
            elif char_decomp.second_part == '*':
                parts.append(char)
            else:
                parts.append(char)
                self.break_down_loop(char_decomp.first_part,
                                     char_decomp.second_part,
                                     parts)

    def split_chars(self, char_string):
        return [char_string[s:s+3] for s in range(0, len(char_string), 3)]

    def populate_char_list(self, keychar1, keychar2):
        char_list = []
        for keychar in [keychar1, keychar2]:
            if not keychar == '*':
                for char in self.split_chars(keychar):
                    if not char == '*':
                        char_list.append(char)

        return char_list
