from bs4 import BeautifulSoup
from requests import get as download
import re

# get a list of all <pre>-elements in WIKI_DECOMP_URL
WIKI_DECOMP_URL = 'https://commons.wikimedia.org/wiki/Commons:Chinese_characters_decomposition'
decomp_html = download(WIKI_DECOMP_URL).text
decomp_soup = BeautifulSoup(decomp_html, 'html.parser').find_all('pre')
if re.search(r'1\.[^2]+2\.', decomp_soup[0].string, re.DOTALL):
    decomp_soup.pop(0)

def get_decomp_list(decomp_soup):
    decomp_list = []
    for pre in decomp_soup:
        for line in pre.string.splitlines():
            if not re.match(r'^\s*$', line):
                decomp_list.append(line)

    return decomp_list

decomp_list = get_decomp_list(decomp_soup)

# deeeebuuug
with open('/tmp/bla', 'w') as blafile:
    counter = 0
    for line in decomp_list:
        blafile.write(str(counter) + line + '\n')
        counter = counter + 1
