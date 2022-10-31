import os
import requests
import re
import pandas as pd

from pathlib import Path


###############################################################################
def create_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path)


###############################################################################
root_dir = "./data/"
url_base = 'https://jisho.org/search/'

kanji = '費'

all_common = url_base + '*' + kanji + '*' + '%23words %23common'

page = requests.get(all_common)

path = "./data/test_common"
with open(path, 'wb+') as f:
    f.write(page.content)

with open(path) as f:
    lines = f.readlines()

entry_identifier = """<div class="concept_light clearfix">"""

definition_identifier = """<div class="concept_light-meanings medium-9 columns">"""

string_to_remove = """<span\s+class\="kanji\-(?:(?!\-up\s+kanji">)(?:.|\n))*\-up\s+kanji">"""

remove_list = [
    ' Noun which may take the genitive case particle &#39;no&#39;',
    '    ',
    ', ',
    '\n',
    ' Suru verb,',
    ' Transitive verb,',
    'Suru verb',
    'Transitive verb',
    'Godan verb with su ending',
    'used as a suffix',
    'Intransitive verb',
    'Noun',
    ',',
]

for i, l in enumerate(lines):

    if entry_identifier in l:
        word = lines[i + 7]
        hiragana = lines[i + 4]
        hiragana = re.sub(string_to_remove, '', hiragana)
        hiragana = hiragana.replace('        ', '')
        hiragana = hiragana.split("</span>")
        hiragana.remove('\n')
        word = word.replace('        ', '')
        word = word.replace('\n', '')
        word = word.replace('<span>', '')
        word = word.replace('</span>', '')
        print(word)

    if definition_identifier in l:
        definition = lines[i + 1]
        definition = re.sub(r'\<(.+?)\>', '', definition)
        definition = definition.replace("&#8203", '')

        if "Wikipedia" in definition:
            definition = definition.split("Wikipedia")
            definition.pop(-1)
            definition = ''.join(definition)
        print(definition)
        for w in remove_list:
            definition = definition.replace(w, '')
        definition = definition.replace("&#39;", "'")

        definitions_list = re.split("""[0-9]\. """, definition)

        if '' in definitions_list:
            definitions_list.remove('')

        print(definitions_list)
