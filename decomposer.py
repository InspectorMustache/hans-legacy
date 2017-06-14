'''This module contains mainly things to determine what components a character
is made up of.'''
import re
import sys
from multiprocessing import Pool
from bs4 import BeautifulSoup
from requests import get as download

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
    '''This is an object that holds all information about a character from the
    Wikicommons decomposition project.'''

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
        for line in wiki_decomp_list:
            if re.search(r'^\s+{}.+$'.format(self.key_char), line):
                return re.sub(r'^\s+{}(.+$)'.format(self.key_char),
                              r'\1',
                              line)
        return 'Undefined'

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
        """This returns a list of all the character's components. Components
        are broken down recursively, down to the smallest one that can be
        found."""
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

    # this headache inducing method was necessary in python 2 to split strings
    # into single chinese characters
    # def split_chars(self, char_string):
    #     return [char_string[s:s+3] for s in range(0, len(char_string), 3)]

    def populate_char_list(self, keychar1, keychar2):
        char_list = []
        for keychar in [keychar1, keychar2]:
            if not keychar == '*':
                for char in keychar:
                    if not char == '*':
                        char_list.append(char)

        return char_list


def get_comp_dict(char_list):
    """Takes a list of chars and breaks them all down to their components.
    Returns a dict with chars as keys and lists of their components as
    values."""
    # this is quite an extensive process and since I don't understand asyncio,
    # we're using multiprocessing to speed it up (which I barely understand as
    # well)
    pool = Pool()
    global comp_dict
    comp_dict = {}
    print("Breaking down all characters... This can take quite a while and "
          "take up some resources. For your entertainment, here are the "
          "characters as they are processed:")
    for char in char_list:
        pool.apply_async(get_single_comp_dict,
                         args=(char, ),
                         callback=update_comp_dict)
    pool.close()
    pool.join()
    print()
    return comp_dict


def update_comp_dict(single_comp_dict):
    char = list(single_comp_dict.keys())[0]
    dynamic_print(char)
    comp_dict.update(single_comp_dict)


def get_single_comp_dict(char):
    """Component dict for a single char."""
    return_dict = {}
    comps = Decompose(char).break_down()
    return_dict[char] = comps
    return return_dict


def dynamic_print(msg):
    '''Update a single line on the terminal'''
    sys.stdout.write('\r\x1b[K' + str(msg))
    sys.stdout.flush()
