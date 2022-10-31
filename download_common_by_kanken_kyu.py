import os
import requests
import re
import pandas as pd

from pathlib import Path
common_words = dict()
kanken_kanjis = pd.read_csv("./data/kanken_kanji.csv")
columns = kanken_kanjis.columns

##############################################################################
entry_identifier = """<div class="concept_light clearfix">"""

definition_identifier = """<div class="concept_light-meanings medium-9 columns">"""

string_to_remove = """<span\s+class\="kanji\-(?:(?!\-up\s+kanji">)(?:.|\n))*\-up\s+kanji">"""

remove_list = [
    ' Noun which may take the genitive case particle &#39;no&#39;',
    '    ',
    # ', ',
    '\n',
    ' Suru verb,',
    ' Transitive verb,',
    'Suru verb',
    'Transitive verb',
    'Godan verb with su ending',
    'used as a suffix',
    'Intransitive verb',
    'Noun',
    #
]

remove_from_split_string = [',','',	", "]

remove_after = ["Wikipedia", "See also"]
###############################################################################
def create_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path)


###############################################################################
root_dir = "./data/"
url_base = 'https://jisho.org/search/'


# kanken_kyu =

kanji_list = kanken_kanjis["3級"].dropna().tolist()

kanji = '費'

all_common_base = url_base + '*' + kanji + '*' + ' %23common %23words?page='

isLastUrl = False
count = 0

while not isLastUrl:
    count += 1
    all_common = all_common_base + str(count)
    page = requests.get(all_common)

    lines = page.text.splitlines()

    path = "./data/test_common" + str(count)
    with open(path, 'wb+') as f:
        f.write(page.content)

    with open(path) as f:
        lines = f.readlines()

    if "Sorry, couldn't find anything matching" in lines[593]:
        isLastUrl = True

    else:
        print(count)




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

                for r in remove_after:
                    if r in definition:
                        definition = definition.split(r)
                        definition.pop(-1)
                        definition = ''.join(definition)
                print(definition)
                for w in remove_list:
                    definition = definition.replace(w, '')
                definition = definition.replace("&#39;", "'")

                definitions_list = re.split("""[0-9]\. """, definition)

                for s in remove_from_split_string:
                    if s in definitions_list:
                        definitions_list.remove(s)

                print(definitions_list)

                entry_dict = dict()
                entry_dict["hiragana"] = hiragana
                entry_dict["english"] = definitions_list
                # entry_dict["kanken_kyu"]

                common_words[word] = entry_dict

###############################################################################
# SAVE A DICTIONARY
dict_ = {}
import json
with open(os.path.join('./data','common.json'), 'w') as fp:
    json.dump(common_words, fp)
fp.close()

###############################################################################