import copy
import os
import requests
import re
import pandas as pd
import json
from pathlib import Path

from requests.adapters import HTTPAdapter, Retry

request_session = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])

common_words = dict()
kanken_kanjis = pd.read_csv("./data/kanken_kanji.csv")
columns = kanken_kanjis.columns

##############################################################################
entry_identifier1 = """<div class="concept_light clearfix">"""
entry_identifier2 = """<span class="concept_light-tag concept_light-common success label">"""

definition_identifier = """<div class="concept_light-meanings medium-9 columns">"""

string_to_remove = """<span\s+class\="kanji\-(?:(?!\-up\s+kanji">)(?:.|\n))*\-up\s+kanji">"""

remove_list = [
    'Noun,',
    ' Suru verb,',
    ' Ichidan verb,',
    "Godan verb with u ending, ",
    "Godan verb with ku ending, ",
    "Godan verb with gu ending, ",
    'Godan verb with su ending, ',
    "Godan verb with tsu ending, ",
    "Godan verb with nu ending, ",
    "Godan verb with bu ending, ",
    "Godan verb with mu ending, ",
    "Godan verb with ru ending, ",

    ' Transitive verb,',
    ' Intransitive verb,',
    "Na-adjective (keiyodoshi), ",
    "I-adjective (keiyoushi), ",
    ' Noun which may take the genitive case particle &#39;no&#39;',
    '    ',

    '\n',

    'Suru verb',
    'Transitive verb',
    "Adverb (fukushi)",

    'Godan verb with su ending',

    'used as a suffix',
    'Intransitive verb',

    "Noun",
    "Ichidan verb, ",
    " - special class, ",
    "Na-adjective (keiyodoshi)",
    "I-adjective (keiyoushi)"
]

remove_from_split_string = [',', '', ", ", " ", "   , "]

remove_after = ["Wikipedia", "See also", "Other forms"]

remove_hiragana = [
    "<ruby class=\"furigana-justify\"><rb>",
    "</rt></ruby>\n",
    "</rt></ruby>",
    "</rb><rt>",
    '        '
]


###############################################################################
def create_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path)


###############################################################################
root_dir = "./data/"

url_base = 'https://jisho.org/search/%20%23common%20%23words?page='

# kanken_kyu =

columns = kanken_kanjis.columns
word_list = []
is_noun_list = []
is_suru_verb_list = []
is_na_adj_list = []
is_i_adj_list = []
is_taru_adj_list = []
is_undertemined_list = []
is_adverb_list = []
is_rentaishi_list = []
definition_list = []
is_verb_list = []
jlpt_level_list = []
hiragana_list = []

isLastUrl = False
count = 0
while not isLastUrl:

    count += 1
    url = url_base + str(count)

    page = request_session.get(url)

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

            if entry_identifier1 in l:
                word = lines[i + 7]
                hiragana = lines[i + 4]
                hiragana = re.sub(string_to_remove, '', hiragana)
                hiragana = hiragana.replace('        ', '')

                for h in remove_hiragana:
                    hiragana = hiragana.replace(h, '')

                hiragana = hiragana.split("</span>")

                # print(hiragana)

                hiragana = [y for y in hiragana if y not in ["<span>", '\n', ""]]

                word = word.replace('        ', '')
                word = word.replace('\n', '')
                word = word.replace('<span>', '')
                word = word.replace('</span>', '')

                print(word)

            if entry_identifier2 in l:
                description_line = copy.copy(l)

            if definition_identifier in l:

                definition = lines[i + 1]

                # print(description_line)
                # print(definition)

                if "JLPT" in description_line:
                    if "N1" in description_line:
                        jlpt_level_list.append("N1")
                    elif "N2" in description_line:
                        jlpt_level_list.append("N2")
                    elif "N3" in description_line:
                        jlpt_level_list.append("N3")
                    elif "N4" in description_line:
                        jlpt_level_list.append("N4")
                    elif "N5" in description_line:
                        jlpt_level_list.append("N5")
                    else:
                        jlpt_level_list.append(None)
                else:
                    jlpt_level_list.append(None)

                if "Noun" in definition:
                    is_noun = True
                else:
                    is_noun = False
                is_noun_list.append(is_noun)

                if "Suru verb" in definition:
                    is_suru_verb = True
                else:
                    is_suru_verb = False
                is_suru_verb_list.append(is_suru_verb)

                if not is_suru_verb and " verb" in definition:
                    is_verb = True
                else:
                    is_verb = False
                is_verb_list.append(is_verb)

                if "Na-adjective" in definition:
                    is_na_adj = True
                else:
                    is_na_adj = False
                is_na_adj_list.append(is_na_adj)

                if "I-adjective" in definition:
                    is_i_adj = True
                else:
                    is_i_adj = False
                is_i_adj_list.append(is_i_adj)

                if """'taru' adjective""" in definition:
                    is_taru_adj = True
                else:
                    is_taru_adj = False
                is_taru_adj_list.append(is_taru_adj)

                if "Adverb" in definition:
                    is_adverb = True
                else:
                    is_adverb = False
                is_adverb_list.append(is_adverb)

                if "rentaishi" in definition:
                    is_rentaishi = True
                else:
                    is_rentaishi = False
                is_rentaishi_list.append(is_rentaishi)

                if not is_noun and not is_suru_verb and not is_na_adj and not is_i_adj and not is_taru_adj and not \
                        is_adverb and not is_rentaishi and not is_verb:

                    is_undertemined_list.append(True)
                else:
                    is_undertemined_list.append(False)

                definition = re.sub(r'\<(.+?)\>', '', definition)
                definition = definition.replace("&#8203", '')

                for r in remove_after:
                    if r in definition:
                        definition = definition.split(r)
                        definition.pop(-1)
                        definition = ''.join(definition)

                # print(definition)

                for w in remove_list:
                    definition = definition.replace(w, '')
                definition = definition.replace("&#39;", "'")

                definitions_list = re.split("""[0-9]\. """, definition)

                for s in remove_from_split_string:
                    if s in definitions_list:
                        definitions_list.remove(s)

                # print(definitions_list)
                word_list.append(word)
                definition_list.append(definition)

                if hiragana:
                    hiragana_list.append('・'.join(hiragana))
                else:
                    hiragana_list.append(None)

                d = {
                    'word': word_list,
                    'hiragana': hiragana_list,
                    'jlpt': jlpt_level_list,
                    'noun': is_noun_list,
                    'suru-verb': is_suru_verb_list,
                    'na-adj': is_na_adj_list,
                    'i-adj': is_i_adj_list,
                    'taru-adj': is_taru_adj_list,
                    'adv.': is_adverb_list,
                    'rentaishi': is_rentaishi,
                    'verb': is_verb_list,
                    'undet.': is_undertemined_list,
                    'definition': definition_list
                }

        df = pd.DataFrame(data=d)
        df.to_csv(os.path.join('./data', 'jisho_all_common.csv'), index=False)

print("*" * 20)
print("DONE")
