import os
import requests
import re
import pandas as pd
import json
from pathlib import Path

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
    "</rb><rt>",
    '        '
]


###############################################################################
def create_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path)


###############################################################################
root_dir = "./data/"
url_base = 'https://jisho.org/search/%20%23words%20%23jlpt-n1%20%23adjective?page='

# kanken_kyu =

columns = kanken_kanjis.columns

for kyu in columns:
    kanji_list = kanken_kanjis[kyu].dropna().tolist()



    for kanji in kanji_list:

        isLastUrl = False
        count = 0

        while not isLastUrl:

            count += 1
            all_common = url_base + str(count)

            print(all_common)

            page = requests.get(all_common)

            lines = page.text.splitlines()

            path = "./data/test_common" + str(count)
            with open(path, 'wb+') as f:
                f.write(page.content)

            with open(path) as f:
                lines = f.readlines()

            STOP

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

                        print(kyu, word)

                    if entry_identifier2 in l:

                        if "JLPT N1" in l and "adjective" in l:

                            if "I-adjective" in l:
                                type_ = "i-adj"

                            elif "Noun" in l:
                                type_ = "noun"

                            elif "Na-adjective" in l:
                                type_ = "na-adj"
                            else:
                                type_ = None

                        dict_ = dict()

                        dict_[""]

                    # if definition_identifier in l:
                    #     definition = lines[i + 1]
                    #     definition = re.sub(r'\<(.+?)\>', '', definition)
                    #     definition = definition.replace("&#8203", '')
                    #
                    #     for r in remove_after:
                    #         if r in definition:
                    #             definition = definition.split(r)
                    #             definition.pop(-1)
                    #             definition = ''.join(definition)
                    #
                    #     # print(definition)
                    #
                    #     for w in remove_list:
                    #         definition = definition.replace(w, '')
                    #     definition = definition.replace("&#39;", "'")
                    #
                    #     definitions_list = re.split("""[0-9]\. """, definition)
                    #
                    #     for s in remove_from_split_string:
                    #         if s in definitions_list:
                    #             definitions_list.remove(s)
                    #
                    #     # print(definitions_list)
                    #     if hiragana:
                    #         if kanji in word:
                    #             entry_dict = dict()
                    #             entry_dict["hiragana"] = hiragana
                    #             entry_dict["english"] = definitions_list
                    #             entry_dict["kanken_kyu"] = kyu
                    #
                    #             common_words[word] = entry_dict

    # with open(os.path.join('./data', 'common_' + kyu + '.json'), 'w') as fp:
    #     json.dump(common_words, fp)
    # fp.close()

###############################################################################
# SAVE A DICTIONARY




###############################################################################
