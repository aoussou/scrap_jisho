import copy
import os
import time
from itertools import compress

import requests
import re
import pandas as pd
import json
from pathlib import Path

from requests.adapters import HTTPAdapter, Retry

request_session = requests.Session()
retries = Retry(total=10, backoff_factor=1, status_forcelist=[429, 502, 503, 504])

common_words = dict()

furigana = pd.read_csv("./data/hiragana.csv", header=None)
hiragana_char_list = list(furigana.iloc[:, 0])

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
    '        ',
    "<span>",
    "</span>"
]


###############################################################################
def create_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path)

def find_2nd_substring_index(string, substring):
   return string.find(substring, string.find(substring) + 1)

def create_sub_dict(
        word_list,
        hiragana_list,
        is_usually_kana_list,
        jlpt_level_list,
        definition_list,
        selection_list
):
    d = {
        'word': list(compress(word_list, selection_list)),
        'is_usually_kana': list(compress(is_usually_kana_list, selection_list)),
        'hiragana': list(compress(hiragana_list, selection_list)),
        'jlpt': list(compress(jlpt_level_list, selection_list)),
        'definition': list(compress(definition_list, selection_list))
    }

    return d


###############################################################################
root_dir = "./data/"
save_dir = os.path.join(root_dir, "n2")
save_dir_jisho_pages = os.path.join(save_dir, "jisho")
url_base = 'https://jisho.org/search/%20%23jlpt-n2%20%23words?page='

# kanken_kyu =

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
is_onoma_list = []
is_usually_kana_list = []

isLastUrl = False
count = 0
while not isLastUrl:

    count += 1
    path = os.path.join(save_dir_jisho_pages, str(count))

    url = url_base + str(count)

    # page = request_session.get(url)
    # time.sleep(.5)
    # lines = page.text.splitlines()
    # with open(path, 'wb+') as f:
    #     f.write(page.content)

    with open(path) as f:
        lines = f.readlines()

    if "Sorry, couldn't find anything matching" in lines[593]:
        isLastUrl = True

    else:
        print(count)

        for i, l in enumerate(lines):

            if entry_identifier1 in l:
                word = lines[i + 7]
                word = word.replace('        ', '')
                word = word.replace('\n', '')
                word = word.replace('<span>', '')
                word = word.replace('</span>', '')



                furigana = lines[i + 4]
                furigana = re.sub(string_to_remove, '', furigana)
                furigana = furigana.replace('        ', '')

                for h in remove_hiragana:
                    furigana = furigana.replace(h, '')

                furigana = list(furigana)


                new_furigana = ""
                for i, c in enumerate(furigana):

                    if c in hiragana_char_list:
                        new_furigana += c
                hiragana = new_furigana


                for c in word:
                    if c in hiragana_char_list:
                        hiragana += c





                # print(word)

            if entry_identifier2 in l:
                description_line = copy.copy(l)

            if definition_identifier in l:

                definition = lines[i + 1]

                if set(list(word)).issubset(hiragana_char_list):
                    kana = copy.copy(word)
                else:
                    start_identifier = """Sentence search for """
                    i_start = find_2nd_substring_index(description_line,start_identifier) + len(start_identifier)
                    end_identifier = """</a></li><li><a href="/search/"""
                    i_end = find_2nd_substring_index(description_line, end_identifier)
                    kana = description_line[i_start:i_end]




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

                if not is_suru_verb and ("Ichidan" in definition or "Godan" in definition):
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

                if "Onomatopoeic" in definition or "mimetic" in definition:
                    is_onoma = True
                else:
                    is_onoma = False
                is_onoma_list.append(is_onoma)

                if "rentaishi" in definition:
                    is_rentaishi = True
                else:
                    is_rentaishi = False
                is_rentaishi_list.append(is_rentaishi)

                if "Usually written using kana" in definition:
                    is_usually_kana = 1
                else:
                    is_usually_kana = 0
                is_usually_kana_list.append(is_usually_kana)

                # try:
                #     if not is_usually_kana:
                #         _, jotoba_definition = get_jotoba(word)
                #     else:
                #         _, jotoba_definition = get_jotoba(hiragana)
                # except:
                #     jotoba_definition = ""

                # print(jotoba_definition)

                if not is_noun and not is_suru_verb and not is_na_adj and not is_i_adj and not is_taru_adj and not \
                        is_adverb and not is_rentaishi and not is_verb and not is_onoma:

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
                definition_list.append("")

                if furigana:
                    hiragana_list.append(hiragana)
                else:
                    hiragana_list.append(None)

                d_all = {
                    'word': word_list,
                    'hiragana': hiragana_list,
                    'usually_kana': is_usually_kana_list,
                    'jlpt': jlpt_level_list,
                    'noun': is_noun_list,
                    'suru-verb': is_suru_verb_list,
                    'na-adj': is_na_adj_list,
                    'i-adj': is_i_adj_list,
                    'taru-adj': is_taru_adj_list,
                    'adv.': is_adverb_list,
                    'rentaishi': is_rentaishi,
                    'verb': is_verb_list,
                    'onoma': is_onoma_list,
                    'undet.': is_undertemined_list,
                    'definition': definition_list
                }

                d_noun = create_sub_dict(
                    word_list,
                    hiragana_list,
                    is_usually_kana_list,
                    jlpt_level_list,
                    definition_list,
                    is_noun_list
                )

                d_na_adj = create_sub_dict(
                    word_list,
                    hiragana_list,
                    is_usually_kana_list,
                    jlpt_level_list,
                    definition_list,
                    is_na_adj_list
                )

                d_i_adj = create_sub_dict(
                    word_list,
                    hiragana_list,
                    is_usually_kana_list,
                    jlpt_level_list,
                    definition_list,
                    is_i_adj_list
                )

                d_taru = create_sub_dict(
                    word_list,
                    hiragana_list,
                    is_usually_kana_list,
                    jlpt_level_list,
                    definition_list,
                    is_taru_adj_list
                )

                d_adv = create_sub_dict(
                    word_list,
                    hiragana_list,
                    is_usually_kana_list,
                    jlpt_level_list,
                    definition_list,
                    is_adverb_list
                )

                d_rentaishi = create_sub_dict(
                    word_list,
                    hiragana_list,
                    is_usually_kana_list,
                    jlpt_level_list,
                    definition_list,
                    is_rentaishi_list
                )

                d_verb = create_sub_dict(
                    word_list,
                    hiragana_list,
                    is_usually_kana_list,
                    jlpt_level_list,
                    definition_list,
                    is_verb_list
                )

                d_onoma = create_sub_dict(
                    word_list,
                    hiragana_list,
                    is_usually_kana_list,
                    jlpt_level_list,
                    definition_list,
                    is_onoma_list
                )

                d_undet = create_sub_dict(
                    word_list,
                    hiragana_list,
                    is_usually_kana_list,
                    jlpt_level_list,
                    definition_list,
                    is_undertemined_list
                )


df_all = pd.DataFrame(data=d_all)
df_all.to_csv(os.path.join(save_dir, 'all.csv'), index=False)

df_verb = pd.DataFrame(data=d_verb)
df_verb.to_csv(os.path.join(save_dir, 'verbs.csv'), index=False)

df_noun = pd.DataFrame(data=d_noun)
df_noun.to_csv(os.path.join(save_dir, 'nouns.csv'), index=False)

df_onoma = pd.DataFrame(data=d_onoma)
df_onoma.to_csv(os.path.join(save_dir, 'onomas.csv'), index=False)

df_i_adj = pd.DataFrame(data=d_i_adj)
df_i_adj.to_csv(os.path.join(save_dir, 'i_adjs.csv'), index=False)

df_na_adj = pd.DataFrame(data=d_na_adj)
df_na_adj.to_csv(os.path.join(save_dir, 'na_adjs.csv'), index=False)

df_taru_adj = pd.DataFrame(data=d_taru)
df_taru_adj.to_csv(os.path.join(save_dir, 'taru_adjs.csv'), index=False)

df_adv = pd.DataFrame(data=d_adv)
df_adv.to_csv(os.path.join(save_dir, 'adverbs.csv'), index=False)

df_rentaishi = pd.DataFrame(data=d_rentaishi)
df_rentaishi.to_csv(os.path.join(save_dir, 'rentaishi.csv'), index=False)

df_undet = pd.DataFrame(data=d_undet)
df_undet.to_csv(os.path.join(save_dir, 'undets.csv'), index=False)

print("*" * 20)
print("DONE")
